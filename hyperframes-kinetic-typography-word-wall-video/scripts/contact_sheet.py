#!/usr/bin/env python3
"""Tile snapshot stills into one labelled contact sheet.

    npx hyperframes snapshot --at <planner's suggested stills ÷ fps> --no-end --output stills
    python3 contact_sheet.py stills stills/sheet.jpg --timing timing.json [--cols 4]

Each tile is labelled with its frame number (from HyperFrames' frame-NN-at-<t>s.png
names, converted with timing.json's fps; Remotion's element-NNN names work too)
and, with --timing, the scene or wall word that should be on screen at that frame.
The grid grows to fit every still. Needs Pillow.
"""
import argparse
import glob
import json
import math
import os
import re

from PIL import Image, ImageDraw


def what_at(timing, frame):
    t = 0
    for s in timing["scenes"]:
        if s["kind"] == "wall":
            for g in s["segments"]:
                if frame < t + g["frames"]:
                    return f"wall: {g['word']}"
                t += g["frames"]
            continue
        if frame < t + s["frames"]:
            return s["kind"]
        t += s["frames"]
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stills_dir")
    ap.add_argument("out")
    ap.add_argument("--cols", type=int, default=0, help="default: about square")
    ap.add_argument("--timing")
    a = ap.parse_args()
    timing = json.load(open(a.timing)) if a.timing else None
    fps = timing["fps"] if timing else 24

    def frame_of(path):
        m = re.search(r"element-(\d+)", path)
        if m:
            return int(m.group(1))
        m = re.search(r"at-([0-9.]+)s", path)
        return round(float(m.group(1)) * fps) if m else None

    files = [f for f in glob.glob(os.path.join(a.stills_dir, "*.*"))
             if f.lower().endswith((".png", ".jpg", ".jpeg")) and frame_of(f) is not None]
    files.sort(key=frame_of)
    if not files:
        raise SystemExit("no frame-NN-at-<t>s.png (or element-NNN) stills found")
    ims = [Image.open(f).convert("RGB") for f in files]
    # full-size snapshots → 480px tiles, so the labels stay legible
    ims = [im.resize((480, round(480 * im.height / im.width))) if im.width > 640 else im for im in ims]
    w, h = ims[0].size
    cols = a.cols or max(1, round(math.sqrt(len(ims) * h / w)))
    rows = math.ceil(len(ims) / cols)
    sheet = Image.new("RGB", (cols * w + (cols - 1) * 4, rows * h + (rows - 1) * 4), "black")
    d = ImageDraw.Draw(sheet)
    for i, (f, im) in enumerate(zip(files, ims)):
        x, y = (i % cols) * (w + 4), (i // cols) * (h + 4)
        sheet.paste(im, (x, y))
        frame = frame_of(f)
        label = f"f{frame}" + (f"  {what_at(timing, frame)}" if timing else "")
        d.rectangle((x, y, x + 8 + 7 * len(label), y + 16), fill="black")
        d.text((x + 4, y + 2), label, fill="yellow")
    sheet.save(a.out)
    print(f"{len(ims)} stills → {cols}×{rows} sheet: {a.out}")


if __name__ == "__main__":
    main()
