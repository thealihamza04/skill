#!/usr/bin/env python3
"""Measure where each SFX file is loudest, so its peak lands on the motion beat.

    python3 sfx_peaks.py assets/sfx/*.wav --fps 30

Prints, per file: length, onset and peak (in frames at --fps and in seconds) and
peak level. Put the seconds value in storyboard.json as the cue's `"peak"`:
scaffold.py then starts the file `peak` seconds early, so its LOUDEST moment sits on
the cue time instead of its first sample. Whooshes and risers usually peak a few
hundred ms in; clicks, pops and impacts peak at ~0. Needs numpy and ffmpeg.
"""
import argparse
import subprocess

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--fps", type=float, default=30)
    a = ap.parse_args()
    sr = 48000
    spf = int(sr / a.fps)
    print(f"{'file':40s} {'len s':>6s} {'onset f':>7s} {'peak f':>6s} {'peak s':>7s} {'dBFS':>6s}")
    for f in a.files:
        x = np.frombuffer(
            subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "f32le", "pipe:1"],
                           capture_output=True, check=True).stdout, dtype="<f4")
        e = [np.abs(x[i: i + spf]).max() for i in range(0, max(1, len(x) - spf + 1), spf)] or [0]
        pk = int(np.argmax(e))
        on = next((i for i, v in enumerate(e) if v > max(e) * 0.1), 0)
        print(f"{f[-40:]:40s} {len(x) / sr:6.2f} {on:7d} {pk:6d} {pk / a.fps:7.3f} "
              f"{20 * np.log10(max(max(e), 1e-9)):6.1f}")


if __name__ == "__main__":
    main()
