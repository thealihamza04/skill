#!/usr/bin/env python3
"""Find a music track's tempo, drops and the trim that puts a drop on a frame.

    python3 analyze_music.py track.mp3 --fps 24 --drop-frame 20

Prints: tempo from the kick grid (more reliable than autocorrelation, which
often locks onto off-beat patterns), integrated loudness / peak, a short-term
loudness map, drop candidates (a quiet stretch followed by an energy jump,
refined to the first kick + cymbal attack), and for each drop the `trimBefore`
(source frames) that lands it on --drop-frame.

After wiring the trim in, verify on a music-only render with check_audio.py —
the first estimate is often 1–2 frames off (attack vs. onset), then nudge
trimBefore by (measured offset ms / 1000 × fps). Fractional values work.
Needs numpy, scipy and ffmpeg.
"""
import argparse
import re
import subprocess

import numpy as np
from scipy.signal import butter, sosfilt


def decode(path, sr, start=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start)]
    if dur:
        cmd += ["-t", str(dur)]
    cmd += ["-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "pipe:1"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype="<f4").astype(float)


def loudness_map(path):
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    st = {}
    for m in re.finditer(r"t:\s*([0-9.]+).*?S:\s*(-?[0-9.]+)", err):
        t = float(m.group(1))
        st[int(t)] = float(m.group(2))  # last value in each second
    summ = err[err.rfind("Summary"):]
    I = re.search(r"I:\s*(-?[0-9.]+)", summ)
    P = re.search(r"Peak:\s*(-?[0-9.]+)", summ)
    return st, float(I.group(1)) if I else None, float(P.group(1)) if P else None


def kick_attacks(x, sr):
    low = sosfilt(butter(4, [40, 120], "band", fs=sr, output="sos"), x)
    hop, win = int(sr * 0.002), int(sr * 0.008)
    env = np.array([np.abs(low[i : i + win]).sum() for i in range(0, len(low) - win, hop)])
    d = np.diff(env, prepend=env[0])
    th = np.percentile(d, 99.0)
    pk = [i for i in range(3, len(d) - 3) if d[i] > th and d[i] == d[i - 3 : i + 4].max()]
    t = [p * hop / sr for p in pk]
    # merge attacks closer than 80 ms (double triggers)
    out = []
    for v in t:
        if not out or v - out[-1] > 0.08:
            out.append(v)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("track")
    ap.add_argument("--fps", type=float, default=24)
    ap.add_argument("--drop-frame", type=float, default=None, help="frame the drop should land on")
    a = ap.parse_args()

    st, I, P = loudness_map(a.track)
    print(f"integrated {I} LUFS, true peak {P} dBFS, length {max(st) if st else 0}s")
    if P is not None and P > -1.0:
        print("  note: the master is hot/clipping; plan to turn it down (gain < 1) in the mix")

    sr = 8000
    x = decode(a.track, sr)
    kicks = kick_attacks(x, sr)
    ioi = np.diff(kicks)
    ioi = ioi[(ioi > 0.25) & (ioi < 1.2)]
    if len(ioi):
        hist, edges = np.histogram(ioi, bins=np.arange(0.25, 1.2, 0.005))
        beat = edges[np.argmax(hist)] + 0.0025
        near = ioi[np.abs(ioi - beat) < 0.02]
        beat = float(np.median(near)) if len(near) else beat
        bpm = 60 / beat
        print(f"tempo ≈ {bpm:.1f} BPM (kick interval {beat:.3f}s) → {a.fps * beat:.2f} frames/beat at {a.fps:g}fps")
    else:
        print("tempo: no steady kick found; use the energy map below and the ear")

    secs = sorted(st)
    print("\nshort-term loudness (LUFS, 1 per second):")
    print(" ".join(f"{s}:{st[s]:.0f}" for s in secs))

    # drop candidates: ≥3 s that sit ≥4 LU below the next 3 s
    cands = []
    for s in secs:
        before = [st.get(s - k) for k in range(1, 4)]
        after = [st.get(s + k) for k in range(0, 3)]
        if None in before or None in after:
            continue
        if np.mean(after) - np.mean(before) >= 4 and min(after) > -20:
            if not cands or s - cands[-1] > 6:
                cands.append(s)
    print("\ndrop candidates (energy jumps after a quieter stretch):")
    hi_sr = 22050
    for s in cands:
        seg = decode(a.track, hi_sr, max(0, s - 3), 5)
        hi = sosfilt(butter(4, 6000, "high", fs=hi_sr, output="sos"), seg)
        lo = sosfilt(butter(4, [40, 120], "band", fs=hi_sr, output="sos"), seg)
        w = int(hi_sr * 0.05)
        hb = [20 * np.log10(np.sqrt(np.mean(hi[i : i + w] ** 2)) + 1e-9) for i in range(0, len(hi) - w, w)]
        lb = [20 * np.log10(np.sqrt(np.mean(lo[i : i + w] ** 2)) + 1e-9) for i in range(0, len(lo) - w, w)]
        jump = [((hb[i + 2] - hb[i - 2]) + (lb[i + 2] - lb[i - 2])) / 2 if 2 <= i < len(hb) - 2 else -99
                for i in range(len(hb))]  # mean rise of the kick and cymbal bands
        i = int(np.argmax(jump))
        t = max(0, s - 3) + i * 0.05
        k_after = [k for k in kicks if t - 0.1 <= k <= t + 0.4]
        t_drop = k_after[0] if k_after else t
        line = f"  {t_drop:7.3f}s  (kick+cymbal bands rise {jump[i]:+.0f} dB)"
        if a.drop_frame is not None:
            trim = (t_drop - a.drop_frame / a.fps) * a.fps
            line += f"  → trimBefore ≈ {trim:.1f} source frames to land on frame {a.drop_frame:g}"
        print(line)
    if not cands:
        print("  none found — pick a strong downbeat from the kick list instead")
    print("\nfirst kicks after each candidate are the sync points; bars are 4 beats from the drop.")


if __name__ == "__main__":
    main()
