#!/usr/bin/env python3
"""Solve the frame timeline for a kinetic word-wall video from a plan spec.

    python3 plan_timeline.py spec.json --out src/MyVideo/

Writes <out>/timing.json (read by check_audio.py) and <out>/timing.ts (imported
by the video config), and prints the timeline table to paste into PLAN.md.

Spec (JSON):
{
  "fps": 24,
  "music": {"bpm": 100, "dropFrame": 20, "grid": "beat"},   // or null for SFX-only
  "minReadable": 7,                    // frames a wall word must stay up to be read
  "acts": [
    {
      "typed":     {"words": ["I", "can", "build", "you"], "wordGap": 3},
      "wall":      {"words": ["web apps", "..."], "vocab": ["..."],
                    "shape": "fast-slow-accel-hold", "distinct": true},
      "statement": {"lead": "…anything ", "accent": "that works", "tail": ".", "minFrames": 28}
    }
  ],
  "end": {"kind": "wordmark", "left": "ALI", "right": "HAMZA", "frames": 36}
      // or {"kind": "custom", "ref": "AhLogo", "frames": 36, "extraHits": [15]}
      // extraHits: frames after the end card starts, snapped to the nearest beat
}

Rules it enforces (learned the hard way; see references/audio-sync.md):
- With music, the first wall cut lands on the drop (dropFrame), and every later
  structural cut (wall → statement, statement → end, act → act) lands on the
  beat grid (grid: "beat" | "half" | "bar"), within ±0.5 frame.
- Wall words are ≥ minReadable frames. With distinct=true no two share a length
  (so no two drift at the same speed). The wall grows to the smallest length
  that satisfies both and ends on the grid.
- Typed words cut on every `wordGap` frames; the typed scene is long enough to
  hold the last word, then run 7 frames into the cut.
"""
import argparse
import json
import math
import sys


def shape_weights(shape, n):
    if shape == "even":
        return [1.0] * n
    if shape == "accelerate":
        return [float(n - i) for i in range(n)]
    if shape == "decelerate":
        return [float(i + 1) for i in range(n)]
    if shape == "accelerate-hold":
        # speeds up through the list, then holds the last word (it hands off to the statement)
        return [float(n - i) for i in range(n - 1)] + [float(n) + 1.5]
    if shape == "fast-slow-accel-hold":
        # quick start, slowing, accelerating, last word held
        if n < 4:
            return [1.0] * (n - 1) + [1.8]
        k1 = max(1, round(n * 0.22))
        k2 = max(1, round(n * 0.33))
        k3 = n - k1 - k2 - 1
        w = [1.0 - 0.06 * i for i in range(k1)]
        w += [1.45 + 0.15 * i for i in range(k2)]
        top = w[-1]
        w += [top - (top - 1.05) * (i + 1) / max(1, k3) for i in range(k3)]
        w += [max(w) + 0.35]
        return w
    raise SystemExit(f"unknown wall shape {shape!r}")


def distinct_solve(weights, total, lo):
    """Distinct integers ≥ lo, ordered like `weights`, summing to `total`."""
    n = len(weights)
    order = sorted(range(n), key=lambda i: (weights[i], i))
    rank = [0] * n
    for r, i in enumerate(order):
        rank[i] = r
    vals = [lo + rank[i] for i in range(n)]
    extra = total - sum(vals)
    if extra < 0:
        raise ValueError("total too small")
    target = [total * w / sum(weights) for w in weights]
    # add +1 to every element with rank ≥ j (keeps order and distinctness),
    # choosing j to reduce error against the targets
    while extra > 0:
        best = None
        for j in range(n):
            cost = n - j
            if cost > extra:
                continue
            err = sum(
                abs(vals[i] + (1 if rank[i] >= j else 0) - target[i]) for i in range(n)
            )
            if best is None or err < best[0]:
                best = (err, j, cost)
        _, j, cost = best
        for i in range(n):
            if rank[i] >= j:
                vals[i] += 1
        extra -= cost
    return vals


def plain_solve(weights, total, lo):
    target = [total * w / sum(weights) for w in weights]
    vals = [max(lo, round(t)) for t in target]
    while sum(vals) > total and max(vals) > lo:
        vals[vals.index(max(vals))] -= 1
    while sum(vals) < total:
        vals[vals.index(max(vals))] += 1
    return vals


class Grid:
    def __init__(self, fps, music):
        self.on = bool(music)
        if not self.on:
            return
        self.beat = fps * 60.0 / music["bpm"]
        self.origin = music["dropFrame"]
        self.step = {"beat": 1.0, "half": 0.5, "bar": 4.0}[music.get("grid", "beat")] * self.beat

    def offset(self, frame):
        """Signed distance (frames) from `frame` to the nearest grid line."""
        if not self.on:
            return 0.0
        k = round((frame - self.origin) / self.step)
        return frame - (self.origin + k * self.step)

    def snap_up(self, frame):
        """Smallest integer ≥ frame within ±0.5 of a grid line."""
        f = math.ceil(frame)
        while self.on and abs(self.offset(f)) > 0.5:
            f += 1
        return f

    def nearest_beat(self, frame):
        if not self.on:
            return frame
        k = round((frame - self.origin) / self.beat)
        return round(self.origin + k * self.beat)

    def beat_offset(self, frame):
        if not self.on:
            return None
        k = round((frame - self.origin) / self.beat)
        return frame - (self.origin + k * self.beat)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", required=True, help="directory for timing.json / timing.ts")
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    fps = spec.get("fps", 24)
    grid = Grid(fps, spec.get("music"))
    lo = spec.get("minReadable", 7)

    scenes, labels, t, extra_hits = main_layout(spec, grid, lo)
    main_tail(a, spec, fps, grid, scenes, labels, t, extra_hits)


def layout(spec, grid, lo, wall_extra):
    scenes, labels = [], []
    t = 0
    wall_i = 0
    for ai, act in enumerate(spec["acts"]):
        ty = act.get("typed")
        if ty:
            gap = ty.get("wordGap", 3)
            on = [2 + gap * i for i in range(len(ty["words"]))]
            need = on[-1] + 2 + 7  # hold the last word, then the 7-frame run
            if ai == 0 and grid.on:
                frames = spec["music"]["dropFrame"] - t
                if frames > need + 8:
                    print(f"note: the typed line needs {need} frames but holds {frames} until the drop; "
                          f"consider dropFrame ≈ {need} (re-run analyze_music.py for the trim) or a slower wordGap",
                          file=sys.stderr)
                if frames < need:
                    sys.exit(f"typed line needs {need} frames but the drop is at {frames}; "
                             f"lower wordGap, cut words, or trim the music so the drop lands later")
            else:
                frames = grid.snap_up(t + max(need, ty.get("frames", need))) - t
            scenes.append({"kind": "typed", "frames": frames, "words": ty["words"], "wordOn": on,
                           **pal(act, ty)})
            labels.append((f"act {ai + 1} typed", t))
            t += frames
        wl = act.get("wall")
        if wl:
            n = len(wl["words"])
            distinct = wl.get("distinct", True)
            if "frames" in wl:  # explicit
                segs = wl["frames"]
                if min(segs) < lo:
                    print(f"warning: act {ai + 1} wall has a {min(segs)}-frame word (< minReadable {lo})",
                          file=sys.stderr)
                if distinct and len(set(segs)) < len(segs):
                    print(f"warning: act {ai + 1} wall repeats a length: {segs}", file=sys.stderr)
            else:
                w = shape_weights(wl.get("shape", "fast-slow-accel-hold"), n)
                min_total = n * lo + (n * (n - 1) // 2 if distinct else 0)
                total = max(min_total, wl.get("minTotal", 0)) + wall_extra[wall_i]
                total = grid.snap_up(t + total) - t
                segs = (distinct_solve if distinct else plain_solve)(w, total, lo)
            labels.append((f"act {ai + 1} wall (cut in)", t))
            scenes.append({
                "kind": "wall",
                "segments": [{"word": word, "frames": f} for word, f in zip(wl["words"], segs)],
                "vocab": wl.get("vocab", wl["words"]),
                **pal(act, wl),
            })
            t += sum(segs)
            wall_i += 1
        st = act.get("statement")
        if st:
            frames = grid.snap_up(t + st.get("minFrames", 28)) - t
            labels.append((f"act {ai + 1} statement", t))
            scenes.append({"kind": "statement", "frames": frames, "lead": st["lead"],
                           "accent": st["accent"], "tail": st.get("tail", ""), **pal(act, st)})
            t += frames
    end = spec.get("end")
    extra_hits = []
    if end:
        labels.append(("end card", t))
        e = dict(end)
        # extra hits (e.g. a logo's second beat) snap to the nearest beat
        extra_hits = [grid.nearest_beat(t + h) for h in e.pop("extraHits", [])]
        for h in extra_hits:
            labels.append(("end card extra hit", h))
        scenes.append(e)
        t += e["frames"]
    return scenes, labels, t, extra_hits


def pal(act, section):
    """palette override: the act's `palette`, then the section's own, merged."""
    p = {**act.get("palette", {}), **section.get("palette", {})}
    return {"palette": p} if p else {}


def main_layout(spec, grid, lo):
    walls = [act["wall"] for act in spec["acts"] if act.get("wall") and "frames" not in act["wall"]]
    n_walls = sum(1 for act in spec["acts"] if act.get("wall"))
    extra = [0] * n_walls
    scenes, labels, t, extra_hits = layout(spec, grid, lo, extra)
    target = spec.get("targetFrames")
    if target and t < target and walls:
        # grow the auto-solved walls toward the target, in proportion to their word counts
        for _ in range(4):
            short = target - t
            if short <= 2:
                break
            auto = [k for k, act in enumerate([a for a in spec["acts"] if a.get("wall")]) if "frames" not in act["wall"]]
            words = sum(len([a for a in spec["acts"] if a.get("wall")][k]["wall"]["words"]) for k in auto)
            for k in auto:
                wc = len([a for a in spec["acts"] if a.get("wall")][k]["wall"]["words"])
                extra[k] += max(0, int(short * wc / words))
            scenes, labels, t, extra_hits = layout(spec, grid, lo, extra)
    if target:
        print(f"target {target} frames → got {t} ({t - target:+d})", file=sys.stderr)
    return scenes, labels, t, extra_hits


def main_tail(a, spec, fps, grid, scenes, labels, t, extra_hits):

    # hits — mirrors hitsFor() in KineticWordWall.tsx
    hits, s0 = [], 0
    for s in scenes:
        fr = sum(g["frames"] for g in s["segments"]) if s["kind"] == "wall" else s["frames"]
        if s["kind"] == "typed":
            hits += [{"kind": "typeWord", "frame": s0 + f} for f in s["wordOn"]]
        if s["kind"] == "wall":
            hits.append({"kind": "wallIn", "frame": s0})
            acc = 0
            for j, g in enumerate(s["segments"]):
                if j:
                    hits.append({"kind": "wallSwap", "frame": s0 + acc})
                acc += g["frames"]
        if s["kind"] == "statement":
            hits.append({"kind": "statement", "frame": s0})
        if s["kind"] in ("wordmark", "custom"):
            hits += [{"kind": "reveal", "frame": s0}, {"kind": "revealImpact", "frame": s0}]
        s0 += fr
    hits += [{"kind": "extra", "frame": h} for h in extra_hits]

    structural = [{"label": l, "frame": f, "beatOffset": grid.beat_offset(f)} for l, f in labels]
    out = {
        "fps": fps,
        "durationInFrames": t,
        "music": spec.get("music"),
        "beatFrames": grid.beat if grid.on else None,
        "scenes": scenes,
        "hits": hits,
        "structural": structural,
    }
    import os

    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "timing.json"), "w"), indent=2, ensure_ascii=False)
    with open(os.path.join(a.out, "timing.ts"), "w") as f:
        f.write("// Generated by plan_timeline.py — edit the spec and re-run, not this file.\n")
        f.write('import type { TimingScene } from "./KineticWordWall";\n\n')
        f.write(f"export const DURATION = {t};\n")
        f.write(f"export const FPS = {fps};\n")
        f.write("export const SCENES: TimingScene[] = ")
        f.write(json.dumps(scenes, indent=2, ensure_ascii=False))
        f.write(";\n")
        f.write(f"export const EXTRA_HIT_FRAMES: number[] = {json.dumps(extra_hits)};\n")

    # report
    print(f"duration {t} frames = {t / fps:.2f}s @ {fps}fps" + (f", beat {grid.beat:.2f}f" if grid.on else ""))
    if grid.on:
        print("\n| Moment | Frame | Time | Off the beat |\n|---|---|---|---|")
    else:
        print("\n| Moment | Frame | Time |\n|---|---|---|")
    for s in structural:
        bo = f" {s['beatOffset']:+.1f}f |" if grid.on else ""
        print(f"| {s['label']} | {s['frame']} | {s['frame'] / fps:.2f}s |{bo}")
    s0 = 0
    for s in scenes:
        if s["kind"] == "wall":
            print("\n| Wall word | Frames | Seconds | Starts |\n|---|---|---|---|")
            acc = s0
            for g in s["segments"]:
                print(f"| {g['word']} | {g['frames']} | {g['frames'] / fps:.2f}s | {acc} |")
                acc += g["frames"]
            fr = [g["frames"] for g in s["segments"]]
            print(f"(min {min(fr)}f, distinct: {len(set(fr)) == len(fr)})")
            if max(fr) > 2 * fps:
                print(f"note: a word stays up {max(fr) / fps:.1f}s; past ~2s a wall drags, so add words "
                      f"or an act rather than stretching", file=sys.stderr)
        s0 += sum(g["frames"] for g in s["segments"]) if s["kind"] == "wall" else s["frames"]

    # suggested stills: the middle of every scene and wall segment, plus the last frame
    stills, s0 = [], 0
    for s in scenes:
        if s["kind"] == "wall":
            acc = s0
            for g in s["segments"]:
                stills.append(acc + g["frames"] // 2)
                acc += g["frames"]
            s0 = acc
        else:
            stills.append(s0 + s["frames"] // 2)
            s0 += s["frames"]
    stills.append(t - 1)
    print(f"\nsuggested stills (--frames=): {','.join(map(str, stills))}")


if __name__ == "__main__":
    main()
