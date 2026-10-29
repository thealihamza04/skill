#!/usr/bin/env python3
"""Tile rendered stills into one labelled contact sheet.

    npx remotion render <Comp> /tmp/<comp>-stills --frames=<planner's suggested stills> \
        --image-format=jpeg --scale=0.25 --concurrency=2
    python3 contact_sheet.py /tmp/<comp>-stills /tmp/<comp>-sheet.jpg [--cols 4] [--timing src/<Comp>/timing.json]

Each tile is labelled with its frame number (read from Remotion's element-NNN
filenames) and, with --timing, the scene or wall word on screen at that frame.
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
    files = sorted(glob.glob(os.path.join(a.stills_dir, "element-*.*")),
                   key=lambda p: int(re.search(r"element-(\d+)", p).group(1)))
    if not files:
        raise SystemExit("no element-*.jpeg/png stills found")
    timing = json.load(open(a.timing)) if a.timing else None
    ims = [Image.open(f).convert("RGB") for f in files]
    w, h = ims[0].size
    cols = a.cols or max(1, round(math.sqrt(len(ims) * h / w)))
    rows = math.ceil(len(ims) / cols)
    sheet = Image.new("RGB", (cols * w + (cols - 1) * 4, rows * h + (rows - 1) * 4), "black")
    d = ImageDraw.Draw(sheet)
    for i, (f, im) in enumerate(zip(files, ims)):
        x, y = (i % cols) * (w + 4), (i // cols) * (h + 4)
        sheet.paste(im, (x, y))
        frame = int(re.search(r"element-(\d+)", f).group(1))
        label = f"f{frame}" + (f"  {what_at(timing, frame)}" if timing else "")
        d.rectangle((x, y, x + 8 + 7 * len(label), y + 16), fill="black")
        d.text((x + 4, y + 2), label, fill="yellow")
    sheet.save(a.out)
    print(f"{len(ims)} stills → {cols}×{rows} sheet: {a.out}")


if __name__ == "__main__":
    main()
