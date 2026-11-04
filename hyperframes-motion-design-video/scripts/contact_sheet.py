#!/usr/bin/env python3
"""Tile `hyperframes snapshot` stills into one sheet, each labelled with its scene.

    npx hyperframes snapshot --at <scaffold.py's list> --no-end --output stills
    python3 contact_sheet.py stills stills/sheet.jpg --timing storyboard.timing.json
    python3 contact_sheet.py stills stills/phone.jpg --timing storyboard.timing.json --tile 390

Labels come from the time in HyperFrames' `frame-NN-at-<t>s.png` names: the frame number
at the project fps, the scene on screen (both scenes mid-transition) and its local time.
`--tile 390` scales every tile to about phone width, the legibility check. Needs Pillow.
"""
import argparse
import glob
import json
import math
import os
import re

from PIL import Image, ImageDraw


def label(timing, t):
    if not timing:
        return f"{t:.2f}s"
    on = [s for s in timing["scenes"] if s["start"] <= t < s["end"] + 1e-6]
    f = round(t * timing["fps"])
    names = " + ".join(f"{s['id']} @{t - s['start']:.2f}" for s in on) or "past the end"
    return f"{t:.2f}s  f{f}  {names}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stills_dir")
    ap.add_argument("out")
    ap.add_argument("--timing", help="storyboard.timing.json from scaffold.py")
    ap.add_argument("--cols", type=int, default=0, help="default: about square")
    ap.add_argument("--tile", type=int, default=480, help="tile width in px (390 = phone check)")
    a = ap.parse_args()
    timing = json.load(open(a.timing)) if a.timing else None
    files = []
    for p in glob.glob(os.path.join(a.stills_dir, "*.png")):
        m = re.search(r"at-([0-9.]+)s\.png$", p)
        if m:
            files.append((float(m.group(1)), p))
    if not files:
        raise SystemExit(f"no frame-NN-at-<t>s.png stills in {a.stills_dir}")
    files.sort()
    cols = a.cols or math.ceil(math.sqrt(len(files)))
    rows = math.ceil(len(files) / cols)
    first = Image.open(files[0][1])
    tw = a.tile
    th = round(first.height * tw / first.width)
    pad, bar = 8, 22
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + bar + pad) + pad), (28, 28, 30))
    d = ImageDraw.Draw(sheet)
    for i, (t, p) in enumerate(files):
        x = pad + (i % cols) * (tw + pad)
        y = pad + (i // cols) * (th + bar + pad)
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y + bar))
        d.text((x + 2, y + 5), label(timing, t), fill=(235, 235, 235))
    sheet.save(a.out, quality=88)
    print(f"{a.out}: {len(files)} stills, {cols}x{rows}, tiles {tw}px wide")


if __name__ == "__main__":
    main()
