#!/usr/bin/env python3
"""Render stills of a Remotion composition at given times and tile them into
one labelled sheet. With --reference, each still is paired with the reference
video's frame at the same time (reference left, render right) and the
percentage of clearly-different pixels is printed — the quickest way to catch
a wrong font size, a mistimed beat or clipped text.

  python3 stills_sheet.py <CompositionId> --out <dir> [--entry src/index.ts]
      [--times 0.1,1.8,...] [--fps 60] [--scale 0.5] [--reference ref.mp4]
      [--shift-after 20.0:-1.8]

--shift-after T:D shifts reference times >= T by -D when your edit drops or
adds a beat (e.g. no `thanks` beat: --shift-after 20.0:1.8 compares render
time t with reference time t+1.8 for t >= 20.0).

Needs ffmpeg on PATH and Pillow.
"""
import argparse
import os
import subprocess
import sys

from PIL import Image, ImageChops, ImageDraw

DEFAULT_TIMES = "0.1,1.8,4.2,6.3,7.8,9.3,11.6,12.6,14.1,15.2,18.5,19.9,21.0"


def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(res.stdout[-2000:] + res.stderr[-2000:])
        raise SystemExit(f"command failed: {' '.join(cmd[:4])}…")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("composition")
    ap.add_argument("--out", required=True)
    ap.add_argument("--entry", default=None, help="Remotion entry point (default: project's)")
    ap.add_argument("--times", default=DEFAULT_TIMES)
    ap.add_argument("--fps", type=float, default=60)
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--reference")
    ap.add_argument("--shift-after", default=None)
    ap.add_argument("--cols", type=int, default=4)
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    times = [float(x) for x in a.times.split(",") if x.strip()]
    shift_t, shift_d = (None, 0.0)
    if a.shift_after:
        s, d = a.shift_after.split(":")
        shift_t, shift_d = float(s), float(d)

    tiles = []
    for t in times:
        frame = round(t * a.fps)
        still = os.path.join(a.out, f"render_{t:06.2f}.png")
        cmd = ["npx", "remotion", "still"]
        if a.entry:
            cmd.append(a.entry)
        cmd += [a.composition, still, f"--frame={frame}", f"--scale={a.scale}", "--log=error"]
        run(cmd)
        img = Image.open(still).convert("RGB")
        label = f"{t:.2f}s  f{frame}"
        if a.reference:
            rt = t + (shift_d if shift_t is not None and t >= shift_t else 0)
            ref = os.path.join(a.out, f"ref_{t:06.2f}.png")
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{rt}", "-i", a.reference, "-frames:v", "1", "-update", "1", ref])
            rimg = Image.open(ref).convert("RGB").resize(img.size)
            diff = ImageChops.difference(img, rimg).convert("L").histogram()
            pct = 100 * sum(diff[40:]) / (img.size[0] * img.size[1])
            print(f"{t:6.2f}s  differing pixels: {pct:5.2f}%")
            pair = Image.new("RGB", (img.size[0] * 2, img.size[1]))
            pair.paste(rimg, (0, 0))
            pair.paste(img, (img.size[0], 0))
            img, label = pair, f"{label}  ref | render  Δ{pct:.1f}%"
        ImageDraw.Draw(img).text((6, 4), label, fill=(255, 0, 0))
        tiles.append(img)

    w, h = tiles[0].size
    cols = min(a.cols if not a.reference else max(1, a.cols // 2), len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), "black")
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    if sheet.size[0] > 2400:
        k = 2400 / sheet.size[0]
        sheet = sheet.resize((2400, int(sheet.size[1] * k)))
    path = os.path.join(a.out, "sheet.png")
    sheet.save(path)
    print(path)


if __name__ == "__main__":
    main()
