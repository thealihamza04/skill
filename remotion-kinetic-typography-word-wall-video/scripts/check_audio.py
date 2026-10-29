#!/usr/bin/env python3
"""Validate a rendered mix: loudness, true peak, SFX-over-music margins, beat sync.

Render twice from the same code (the engine's `mute` prop makes this a flag):
    npx remotion render <Comp> mix.wav   --codec=wav --concurrency=2
    npx remotion render <Comp> music.wav --codec=wav --concurrency=2 --props='{"mute":"sfx"}'
then:
    python3 check_audio.py mix.wav music.wav path/to/timing.json [--min-margin 2] [--max-tp -1.3]
SFX-only videos (music: null): pass `none` instead of music.wav. Margins and beat
sync are skipped; loudness/true peak and the loudest frames are still checked.

- SFX layer = mix − music (two renders differ by ~150 samples of jitter; harmless).
- Margin = SFX peak minus music peak in a 2-frame window at each hit. The bar
  for "SFX louder than the music" is ≥ ~+3 dB (target); ≥ +2 passes.
- Beat sync: the sharpest kick attack within ±60 ms of each structural frame.
  A consistent offset of the same sign means nudge music.trimBefore by
  (offset ms / 1000 × fps). Scattered ±40 ms readings are other instruments.
Exit code 1 if true peak or any margin fails. Needs numpy, scipy and ffmpeg.
"""
import argparse
import json
import re
import subprocess
import sys

import numpy as np
from scipy.signal import butter, sosfilt


def load(p, sr=48000):
    """→ (mono mix for comparisons, per-sample stereo peak for peak reports), sr."""
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(sr), "-f", "f32le", "pipe:1"],
                                     capture_output=True, check=True).stdout, dtype="<f4").astype(float).reshape(-1, 2)
    return x.mean(1), np.abs(x).max(1), sr


def ebur(p):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = err[err.rfind("Summary"):]
    return float(re.search(r"I:\s*(-?[0-9.]+)", s).group(1)), float(re.search(r"Peak:\s*(-?[0-9.]+)", s).group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mix")
    ap.add_argument("music")
    ap.add_argument("timing")
    ap.add_argument("--min-margin", type=float, default=2.0)
    ap.add_argument("--max-tp", type=float, default=-1.3)
    a = ap.parse_args()
    tm = json.load(open(a.timing))
    fps = tm["fps"]
    ok = True

    I, TP = ebur(a.mix)
    print(f"mix: {I} LUFS integrated, {TP} dBTP" + ("" if TP <= a.max_tp else f"   ✗ true peak above {a.max_tp}"))
    ok &= TP <= a.max_tp

    mix, mixpk, sr = load(a.mix)
    sfx_only = a.music.lower() == "none"
    if sfx_only:
        mus, muspk = np.zeros_like(mix), np.zeros_like(mixpk)
    else:
        mus, muspk, _ = load(a.music)
    n = min(len(mix), len(mus))
    mix, mus, mixpk, muspk = mix[:n], mus[:n], mixpk[:n], muspk[:n]
    sfx = mix - mus
    spf = int(sr / fps)
    db = lambda v: 20 * np.log10(max(v, 1e-9))

    # where the peaks are: the fix for a hot peak is usually a duck under that one hit
    per = lambda x: [np.abs(x[i * spf:(i + 1) * spf]).max() for i in range(n // spf)]
    pm, pu, ps = per(mixpk), per(muspk), per(sfx)
    hit_at = {h["frame"]: h["kind"] for h in tm["hits"]}
    print("loudest frames (stereo sample peak; true peak runs up to ~0.5 dB higher):")
    for i in sorted(sorted(range(len(pm)), key=lambda i: -pm[i])[:4]):
        near = [f"{hit_at[f]}@{f}" for f in range(i - 2, i + 1) if f in hit_at]
        print(f"  frame {i:4d}: mix {db(pm[i]):6.1f}  music {db(pu[i]):6.1f}  sfx {db(ps[i]):6.1f}  {' '.join(near)}")
    if sfx_only:
        print("\nSFX-only: no music to beat, margins and beat sync skipped.")
        print("For SFX-only, aim for the loudest hit ≈ −2 dBTP (raise sfxGain until close) and accept a low LUFS:")
        print("it's mostly silence between hits.")
        print("\nPASS" if ok else "\nFAIL")
        sys.exit(0 if ok else 1)
    print(f"\n{'hit':12s} {'frame':>5s} {'sfx':>7s} {'music':>7s} {'margin':>7s}")
    worst = 99.0
    for h in tm["hits"]:
        f = h["frame"]
        a0, b0 = f * spf, (f + 2) * spf
        if b0 > n:
            continue
        s, m = np.abs(sfx[a0:b0]).max(), np.abs(mus[a0:b0]).max()
        if db(s) < -45:
            print(f"{h['kind']:12s} {f:5d}   (silent — no sound mapped to this hit)")
            continue
        mg = db(s) - db(m)
        worst = min(worst, mg)
        flag = "" if mg >= 3.0 else ("  (under the +3 target)" if mg >= a.min_margin else "  ✗ fails")
        print(f"{h['kind']:12s} {f:5d} {db(s):7.1f} {db(m):7.1f} {mg:+7.1f}{flag}")
    if worst < 99:
        print(f"worst margin {worst:+.1f} dB")
        ok &= worst >= a.min_margin

    if tm.get("beatFrames") and np.abs(mus).max() > 1e-4:
        low = sosfilt(butter(4, [40, 120], "band", fs=sr, output="sos"), mus)
        hop, win = int(sr * 0.002), int(sr * 0.008)
        env = np.array([np.abs(low[i : i + win]).sum() for i in range(0, len(low) - win, hop)])
        d = np.diff(env, prepend=env[0])
        frame_ms = 1000 / fps
        print(f"\nbeat sync (structural cut vs nearest kick attack; fails beyond ±{frame_ms:.0f} ms = 1 frame):")
        for s in tm["structural"]:
            if s["frame"] == 0:
                continue  # the opening isn't meant to sit on a beat
            c = int(s["frame"] / fps / 0.002)
            lo, hi = max(0, c - 30), min(len(d), c + 30)
            if hi <= lo:
                continue
            i = lo + int(np.argmax(d[lo:hi]))
            off = (i * 0.002 - s["frame"] / fps) * 1000
            bad = abs(off) > frame_ms
            ok &= not bad
            print(f"  {s['label']:24s} frame {s['frame']:4d}  kick {off:+5.0f} ms" + ("  ✗ more than a frame off" if bad else ""))
    print("\nPASS" if ok else "\nFAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
