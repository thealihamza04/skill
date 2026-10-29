#!/usr/bin/env python3
"""Measure each SFX file's peak offset — the `peakOffset` a SoundHit needs.

    python3 sfx_peaks.py public/sfx/*.wav public/pop.wav --fps 24

A hit is placed at (event frame − peakOffset) so its LOUDEST moment lands on
the cut, not its first sample. Whooshes and risers usually peak several
frames in; clicks and impacts peak at 0. Needs numpy and ffmpeg.
"""
import argparse
import subprocess

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--fps", type=float, default=24)
    a = ap.parse_args()
    sr = 48000
    spf = int(sr / a.fps)
    print(f"{'file':40s} {'frames':>6s} {'onset':>5s} {'peakOffset':>10s} {'peak dBFS':>9s}")
    for f in a.files:
        x = np.frombuffer(
            subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "f32le", "pipe:1"],
                           capture_output=True, check=True).stdout, dtype="<f4")
        e = [np.abs(x[i : i + spf]).max() for i in range(0, max(1, len(x) - spf + 1), spf)] or [0]
        pk = int(np.argmax(e))
        on = next((i for i, v in enumerate(e) if v > max(e) * 0.1), 0)
        print(f"{f[-40:]:40s} {len(e):6d} {on:5d} {pk:10d} {20 * np.log10(max(max(e), 1e-9)):9.1f}")


if __name__ == "__main__":
    main()
