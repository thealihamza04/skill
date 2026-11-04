#!/usr/bin/env python3
"""Measure a render's mix: loudness, true peak, and whether every cue reads over the music.

    python3 audio_check.py renders/mix.mp4 --timing storyboard.timing.json
    python3 audio_check.py renders/mix.mp4 --music renders/music.mp4 --timing storyboard.timing.json

Without --music: integrated loudness (LUFS), true peak (dBTP) and the loudest moments.
With --music (a render of `scaffold.py --mute sfx --out music-only.html`): for every SFX/VO
cue, its level in the mix vs the music alone in the same 80 ms window. A hit that doesn't
clear the music by ~2-3 dB is felt as mush, not a beat. Exits 1 when true peak > -1.0 dBTP
or any SFX is under the music. Needs numpy and ffmpeg.
"""
import argparse
import json
import re
import subprocess
import sys

import numpy as np

SR = 48000


def decode(path):
    """Per-sample max |level| across the two channels (a mono downmix would sum them and read ~3 dB hot)."""
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "pipe:1"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(out, dtype="<f4").astype(float)
    return np.abs(x[: len(x) // 2 * 2].reshape(-1, 2)).max(axis=1)


def ebur128(path):
    err = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    tail = err[err.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", tail)
    p = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", tail)
    return (float(i.group(1)) if i else float("nan")), (float(p.group(1)) if p else float("nan"))


def db(x):
    return 20 * np.log10(max(x, 1e-9))


def window_peak(x, t, w=0.08):
    a, b = int(max(0, t - 0.01) * SR), int((t + w) * SR)
    seg = x[a:b]
    return db(np.abs(seg).max()) if len(seg) else -180.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mix")
    ap.add_argument("--music", help="music-only render, for the cue-over-music margins")
    ap.add_argument("--timing", help="storyboard.timing.json")
    ap.add_argument("--target-margin", type=float, default=3.0)
    a = ap.parse_args()
    lufs, tp = ebur128(a.mix)
    print(f"integrated loudness: {lufs:.1f} LUFS   true peak: {tp:.1f} dBTP")
    print("  targets: true peak <= -1.3 dBTP; ~-14 LUFS for music-led mixes, -16..-19 with SFX leading,"
          " lower is expected for sparse SFX-only pieces")
    x = decode(a.mix)
    hop = int(SR * 0.05)
    env = np.array([np.abs(x[i:i + hop]).max() for i in range(0, len(x) - hop, hop)] or [0])
    top = sorted(np.argsort(env)[-4:] * 0.05)
    print("loudest moments: " + ", ".join(f"{t:.2f}s ({db(env[int(t / 0.05)]):.1f} dBFS)" for t in top))
    fail = tp > -1.0
    if a.timing:
        timing = json.load(open(a.timing))
        cues = timing.get("cues", [])
        m = decode(a.music) if a.music else None
        if cues:
            print(f"\n{'cue':32s} {'lands':>6s} {'mix dB':>7s} {'music dB':>8s} {'margin':>7s}")
        for c in cues:
            mix_db = window_peak(x, c["at"])
            if m is None:
                print(f"{c['src'][-32:]:32s} {c['at']:6.2f} {mix_db:7.1f}")
                continue
            mus_db = window_peak(m, c["at"])
            margin = mix_db - mus_db
            if c["kind"] == "vo":
                verdict = ""
            elif margin >= a.target_margin:
                verdict = "ok"
            elif margin >= 1.95:
                verdict = "pass (raise a little)"
            else:
                verdict = "UNDER: raise its volume or set duck: true"
                fail = True
            print(f"{c['src'][-32:]:32s} {c['at']:6.2f} {mix_db:7.1f} {mus_db:8.1f} {margin:+7.1f}  {verdict}")
    if tp > -1.0:
        print(f"\nTRUE PEAK {tp:.1f} dBTP is hot: duck the music under the loudest hit, lower that cue, or lower music.gain")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
