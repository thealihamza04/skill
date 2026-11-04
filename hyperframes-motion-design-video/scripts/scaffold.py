#!/usr/bin/env python3
"""storyboard.json -> a HyperFrames project: timing, transitions and sound in one file.

    python3 scaffold.py storyboard.json --project <dir>
    python3 scaffold.py storyboard.json --project <dir> --mute sfx --out music-only.html

What it owns (regenerated on every run; never hand-edit it):
  <dir>/index.html            root "main": one host clip per scene at its computed start,
                              scene-to-scene transitions on the root timeline, every <audio>
                              (music with a per-frame fade/duck automation lane, SFX, voiceover)
  <dir>/storyboard.timing.json the computed start/end of every scene and cue (read by
                              contact_sheet.py and audio_check.py)

What you own (written ONCE as a starting skeleton, then never touched again unless you pass
--force-scenes):
  <dir>/compositions/<scene-id>.html   one <template> sub-composition per scene with its own
                              paused GSAP timeline in scene-local seconds, the bundled
                              @font-face rules, the palette as CSS variables and a helper prelude
                              (eases, spring(), r(), drive(), countUp(), zoomLog(), split(), rng()).

So: change a duration, a transition or a sound -> edit storyboard.json and re-run. Change what a
scene looks like or how it moves -> edit that scene's file. Re-running is always safe.

Transitions ("enter" on a scene; it overlaps the previous scene by its duration):
  cut (default) | crossfade | blur | push-left | push-right | push-up | push-down |
  wipe-left | wipe-right | wipe-up | wipe-down | zoom | iris
Match cuts are authored inside scenes (a shared element), not here: see references/transitions.md.

Needs Python 3 and ffprobe on PATH.
"""
import argparse
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GSAP = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"
VOLUME_CAP = 3.98
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")

DEFAULT_FONTS = [
    {"family": "Inter", "weight": 500, "src": "assets/fonts/inter-latin-500-normal.woff2"},
    {"family": "Inter", "weight": 800, "src": "assets/fonts/inter-latin-800-normal.woff2"},
    {"family": "Source Serif 4", "weight": 400, "src": "assets/fonts/source-serif-4-latin-400-normal.woff2"},
]
DEFAULT_PALETTE = {"ground": "#0E0E11", "ink": "#F3F1EC", "muted": "#8C8A92", "accent": "#FF5B37"}

# Root-timeline tweens per transition: (outgoing from, outgoing to, incoming from, incoming to, ease)
TRANSITIONS = {
    "crossfade": (None, None, {"opacity": 0}, {"opacity": 1}, "sine.inOut"),
    "blur": ({"filter": "blur(0px)"}, {"filter": "blur(12px)"},
             {"opacity": 0, "filter": "blur(18px)"}, {"opacity": 1, "filter": "blur(0px)"}, "sine.inOut"),
    "push-left": ({"xPercent": 0}, {"xPercent": -100}, {"xPercent": 100}, {"xPercent": 0}, "power3.inOut"),
    "push-right": ({"xPercent": 0}, {"xPercent": 100}, {"xPercent": -100}, {"xPercent": 0}, "power3.inOut"),
    "push-up": ({"yPercent": 0}, {"yPercent": -100}, {"yPercent": 100}, {"yPercent": 0}, "power3.inOut"),
    "push-down": ({"yPercent": 0}, {"yPercent": 100}, {"yPercent": -100}, {"yPercent": 0}, "power3.inOut"),
    "wipe-left": (None, None, {"clipPath": "inset(0% 0% 0% 100%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, "power3.inOut"),
    "wipe-right": (None, None, {"clipPath": "inset(0% 100% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, "power3.inOut"),
    "wipe-up": (None, None, {"clipPath": "inset(100% 0% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, "power3.inOut"),
    "wipe-down": (None, None, {"clipPath": "inset(0% 0% 100% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, "power3.inOut"),
    "zoom": ({"scale": 1, "opacity": 1}, {"scale": 1.5, "opacity": 0},
             {"scale": 0.86, "opacity": 0}, {"scale": 1, "opacity": 1}, "power3.inOut"),
    "iris": (None, None, {"clipPath": "circle(0% at 50% 50%)"}, {"clipPath": "circle(75% at 50% 50%)"}, "power2.inOut"),
}
DEFAULT_TRANSITION_DUR = {"crossfade": 0.5, "blur": 0.6, "zoom": 0.5, "iris": 0.6}

PRELUDE = r"""
const tl = gsap.timeline({ paused: true });
const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));
// Cubic-bezier as a GSAP ease function: ease: bez(0.16, 1, 0.3, 1)
function bez(x1, y1, x2, y2) {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const sx = (t) => ((ax * t + bx) * t + cx) * t, sy = (t) => ((ay * t + by) * t + cy) * t;
  return (x) => {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    let lo = 0, hi = 1, t = x;
    for (let i = 0; i < 40; i++) { if (sx(t) < x) lo = t; else hi = t; t = (lo + hi) / 2; }
    return sy(t);
  };
}
// Damped spring as a GSAP ease (settles exactly at 1). zeta 0.72-0.85 = premium, tiny overshoot.
function spring(zeta = 0.78) {
  const w = 6.4 / Math.min(zeta, 0.999), wd = w * Math.sqrt(Math.max(1e-6, 1 - zeta * zeta));
  return (t) => {
    if (t <= 0) return 0;
    if (t >= 1) return 1;
    if (zeta >= 1) return 1 - (1 + w * t) * Math.exp(-w * t);
    return 1 - Math.exp(-zeta * w * t) * (Math.cos(wd * t) + (zeta * w / wd) * Math.sin(wd * t));
  };
}
// Clamped piecewise interpolation with an ease per segment: r(t, [0, 1, 2], [0, 100, 40], "power2.out")
function r(t, xs, ys, ease = "none") {
  const e = typeof ease === "function" ? ease : gsap.parseEase(ease);
  if (t <= xs[0]) return ys[0];
  for (let i = 0; i < xs.length - 1; i++)
    if (t <= xs[i + 1]) return ys[i] + (ys[i + 1] - ys[i]) * e((t - xs[i]) / (xs[i + 1] - xs[i]));
  return ys[ys.length - 1];
}
// Driver: fn(localSeconds) recomputes DOM from scratch on every seek inside [start, start + dur].
// ONE driver per element+property, spanning everything it does (use r() for several phases):
// two drivers on one property fight, because each sets its own value at build time.
function drive(start, dur, fn) {
  const o = { t: 0 };
  tl.fromTo(o, { t: 0 }, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => fn(o.t) }, start);
  fn(0);
}
// Counter that stays legible mid-move. fmt(v) returns the string to show.
function countUp(sel, from, to, start, dur, ease = "power2.out", fmt = (v) => Math.round(v).toLocaleString("en-US")) {
  const el = $(sel), e = gsap.parseEase(ease);
  drive(start, dur, (t) => { el.textContent = fmt(from + (to - from) * e(Math.min(1, t / dur))); });
}
// Zoom interpolated in log space (reads as constant camera speed). Never put CSS transform on sel.
// Several phases on one element: pass arrays, zoomLog(sel, [1, 1.05, 6], [0, 2.2, 3.1], ["none", "power2.in"])
function zoomLog(sel, from, to, start, dur, ease = "power2.inOut") {
  const el = $(sel);
  if (Array.isArray(from)) {  // multi-phase: from = scales, to = times (scene-local s), start = eases
    const S = from, T = to, E = Array.isArray(start) ? start : T.slice(1).map(() => start || "none");
    const L = S.map(Math.log), d = T[T.length - 1] - T[0];
    drive(T[0], d, (t) => {
      const x = T[0] + t; let i = 0;
      while (i < T.length - 2 && x > T[i + 1]) i++;
      const e = gsap.parseEase(E[i]), p = Math.min(1, Math.max(0, (x - T[i]) / (T[i + 1] - T[i])));
      gsap.set(el, { scale: Math.exp(L[i] + (L[i + 1] - L[i]) * e(p)) });
    });
    return;
  }
  const e = gsap.parseEase(ease);
  drive(start, dur, (t) => gsap.set(el, { scale: from * Math.pow(to / from, e(Math.min(1, t / dur))) }));
}
// Split an element's text into inline-block word or char spans at build time (deterministic).
function split(sel, by = "words") {
  const el = $(sel), text = el.textContent.trim(), out = [];
  el.textContent = "";
  const parts = by === "chars" ? Array.from(text) : text.split(/\s+/);
  parts.forEach((p, i) => {
    const s = document.createElement("span");
    s.style.display = "inline-block";
    s.style.whiteSpace = "pre";
    s.textContent = p === " " ? " " : p;
    el.appendChild(s);
    out.push(s);
    if (by !== "chars" && i < parts.length - 1) el.appendChild(document.createTextNode(" "));
  });
  return out;
}
// Seeded PRNG (mulberry32 over a string hash): same "random" layout on every render.
function rng(seed) {
  let h = 1779033703 ^ String(seed).length;
  for (const c of String(seed)) { h = Math.imul(h ^ c.charCodeAt(0), 3432918353); h = (h << 13) | (h >>> 19); }
  let a = h >>> 0;
  return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
"""


def num(x):
    s = f"{x:.4f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        sys.exit(f"ffprobe could not read {path}")


def tween_js(target, frm, to, at, dur, ease):
    return (f'  tl.fromTo("#{target}", {json.dumps(frm)}, '
            f'{json.dumps(dict(to, duration=round(dur, 4), ease=ease))}, {num(at)});')


def font_css(fonts):
    rules = []
    for f in fonts:
        rel = "../" + f["src"]  # scene files live in compositions/
        rules.append(f"@font-face {{ font-family: '{f['family']}'; font-weight: {f.get('weight', 400)}; "
                     f"font-style: {f.get('style', 'normal')}; font-display: block; src: url('{rel}') format('woff2'); }}")
    return "\n        ".join(rules)


def scene_skeleton(scene, sb, W, H, first=False):
    sid, dur = scene["id"], scene["duration"]
    pal = {**DEFAULT_PALETTE, **sb.get("palette", {}), **scene.get("palette", {})}
    vars_css = " ".join(f"--{k}: {v};" for k, v in pal.items())
    fam = (sb.get("fonts") or DEFAULT_FONTS)[0]["family"]
    heading = html.escape(scene.get("text") or scene["id"].replace("-", " ").title())
    support = html.escape(scene.get("support", ""))
    size = round(min(W, H) * 0.11)
    # Frame 0 of the film is the thumbnail: the first scene's title is already on screen at t=0.
    entry_from = "{ y: 14, opacity: 1 }" if first else "{ y: 48, opacity: 0 }"
    support_html = (f'\n          <p id="{sid}-support" class="support">{support}</p>' if support else "")
    support_js = (f'\ntl.fromTo("#{sid}-support", {{ y: 18, opacity: 0 }}, '
                  f'{{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, 0.28);' if support else "")
    return f"""<!doctype html>
<html>
  <head><meta charset="UTF-8" /></head>
  <body>
    <!-- Scene "{sid}" ({num(dur)}s, scene-local time 0..{num(dur)}). YOURS to edit: look and motion live here.
         Its start, length, transition and sound live in storyboard.json (re-run scaffold.py after changing them).
         Plan: {html.escape(scene.get("plan", "see PLAN.md"))} -->
    <template>
      <style>
        {font_css(sb.get("fonts") or DEFAULT_FONTS)}
        #{sid} {{ {vars_css} position: relative; width: 100%; height: 100%; overflow: hidden;
          background: var(--ground); color: var(--ink); font-family: '{fam}', sans-serif; }}
        #{sid} .stage {{ position: absolute; inset: 0; display: flex; flex-direction: column;
          align-items: center; justify-content: center; gap: {round(size * 0.3)}px; }}
        #{sid}-title {{ font-weight: 800; font-size: {size}px; line-height: 1; letter-spacing: -0.045em; }}
        #{sid} .support {{ font-weight: 500; font-size: {round(size * 0.3)}px; color: var(--muted); }}
      </style>
      <div id="{sid}" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-duration="{num(dur)}">
        <div id="{sid}-stage" class="stage" data-layout-allow-overflow>
          <h1 id="{sid}-title">{heading}</h1>{support_html}
        </div>
      </div>
      <script>
(() => {{{PRELUDE}
const ID = "{sid}", D = {num(dur)};
// Placeholder motion: one entrance + a slow push so the shot never sits dead. Replace with the plan.
tl.fromTo("#{sid}-title", {entry_from}, {{ y: 0, opacity: 1, duration: 0.7, ease: spring(0.8) }}, 0);{support_js}
zoomLog("#{sid}-stage", 1, 1.04, 0, D, "none");
window.__timelines["{sid}"] = tl;
}})();
      </script>
    </template>
  </body>
</html>
"""


class Board:
    def __init__(self, sb, project, mute):
        self.sb, self.project, self.mute = sb, project, mute
        self.W, self.H = sb.get("width", 1920), sb.get("height", 1080)
        self.fps = sb.get("fps", 30)
        self.scenes = sb.get("scenes") or sys.exit("storyboard.json needs a non-empty \"scenes\" list")
        self.layout()

    def layout(self):
        seen, t = set(), 0.0
        for i, s in enumerate(self.scenes):
            sid = s.get("id", "")
            if not ID_RE.match(sid) or sid == "main" or sid in seen:
                sys.exit(f"scene id {sid!r}: needs lowercase letters, digits and dashes, unique, not 'main'")
            seen.add(sid)
            if not s.get("duration") or s["duration"] <= 0:
                sys.exit(f"scene {sid}: duration (seconds) must be > 0")
            enter = s.get("enter", "cut")
            if isinstance(enter, str):
                enter = {"type": enter}
            kind = enter.get("type", "cut")
            if kind != "cut" and kind not in TRANSITIONS:
                sys.exit(f"scene {sid}: unknown transition {kind!r}; use cut or one of {', '.join(TRANSITIONS)}")
            if i == 0 and kind != "cut":
                sys.exit(f"scene {sid}: the first scene has nothing to transition from; use \"cut\"")
            d = 0.0 if kind == "cut" else float(enter.get("duration", DEFAULT_TRANSITION_DUR.get(kind, 0.45)))
            if i and d >= min(s["duration"], self.scenes[i - 1]["duration"]):
                sys.exit(f"scene {sid}: transition ({d}s) must be shorter than both scenes it joins")
            s["_enter"] = dict(enter, type=kind, duration=d)
            s["_start"] = t - d if i else 0.0
            s["_end"] = s["_start"] + s["duration"]
            t = s["_end"]
        self.total = t
        self.by_id = {s["id"]: s for s in self.scenes}

    def cue_time(self, c):
        if "t" in c:
            return float(c["t"])
        if c.get("scene") not in self.by_id:
            sys.exit(f"audio cue {c.get('src')}: give \"t\" (absolute s) or \"scene\" (an id) + \"at\" (scene-local s)")
        return self.by_id[c["scene"]]["_start"] + float(c.get("at", 0))

    def media(self, rel):
        p = os.path.join(self.project, rel)
        if not os.path.exists(p):
            sys.exit(f"media not found inside the project: {rel} (copy it into {self.project}/assets/ first)")
        return p

    def audio(self):
        tags, cues, used = [], [], []  # used: per-track list of (start, end)
        fr = 1.0 / self.fps
        for c in self.sb.get("audio", []):
            kind = c.get("kind", "sfx")
            at = self.cue_time(c)
            start = max(0.0, at - float(c.get("peak", 0)))
            length = min(probe_duration(self.media(c["src"])), self.total - start)
            if length <= 0:
                print(f"warning: cue {c['src']} at {at:.2f}s starts after the video ends; skipped")
                continue
            vol = float(c.get("volume", 0.5))
            if vol > VOLUME_CAP:
                print(f"warning: {c['src']} volume {vol} > {VOLUME_CAP} cap; clamped. Bake a louder file instead.")
                vol = VOLUME_CAP
            track = next((k for k, spans in enumerate(used) if all(start >= e or start + length <= s for s, e in spans)), None)
            if track is None:
                used.append([])
                track = len(used) - 1
            used[track].append((start, start + length))
            cues.append({"src": c["src"], "kind": kind, "at": round(at, 4), "start": round(start, 4),
                         "length": round(length, 4), "volume": vol, "duck": bool(c.get("duck", kind == "vo")),
                         "track": track + 3})
        m = self.sb.get("music")
        if m and self.mute not in ("music", "all"):
            src_len = probe_duration(self.media(m["src"]))
            trim = float(m.get("trim", 0))
            if src_len - trim < self.total - 0.05:
                print(f"warning: music has {src_len - trim:.2f}s after the trim but the video is {self.total:.2f}s")
            gain, fi, fo = float(m.get("gain", 0.4)), float(m.get("fadeIn", 0.25)), float(m.get("fadeOut", 1.0))
            sfx_duck = 10 ** (float(m.get("duckDb", -6)) / 20)
            vo_duck = 10 ** (float(m.get("voDuckDb", -9)) / 20)

            def env(t):
                fade = min(1.0, t / fi if fi else 1.0, (self.total - t) / fo if fo else 1.0)
                d = 1.0
                for c in cues:
                    if not c["duck"]:
                        continue
                    if c["kind"] == "vo":  # carve under the whole line, 150 ms ramps
                        s, e, r = c["start"], c["start"] + c["length"], 0.15
                        if s - r <= t <= e + r:
                            k = 1.0 if s <= t <= e else 1 - min(abs(t - s), abs(t - e)) / r
                            d = min(d, 1 - (1 - vo_duck) * max(0.0, k))
                    else:  # 1-frame attack, 2-frame hold, 6-frame release around the hit's peak
                        h = c["at"]
                        if h - fr <= t < h:
                            d = min(d, 1 - (1 - sfx_duck) * (t - (h - fr)) / fr)
                        elif h <= t <= h + 2 * fr:
                            d = min(d, sfx_duck)
                        elif h + 2 * fr < t <= h + 8 * fr:
                            d = min(d, sfx_duck + (1 - sfx_duck) * (t - (h + 2 * fr)) / (6 * fr))
                return max(0.0, fade) * d * gain

            pts, last, n = [], None, int(round(self.total * self.fps))
            for f in range(n + 1):
                t = f / self.fps
                v = round(env(t), 4)
                if v != last or f == n:
                    pts.append({"t": round(t, 4), "v": v})
                    last = v
            lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": pts}]})
            tags.append(f'<audio id="music" src="{html.escape(m["src"])}" data-start="0" data-duration="{num(self.total)}" '
                        f'data-media-start="{num(trim)}" data-track-index="2" data-volume="1" data-automation=\'{lane}\'></audio>')
        # Muted cues still shape the music's duck envelope, so a music-only render measures the real bed.
        for i, c in enumerate(cues):
            if self.mute in ("sfx", "all") and c["kind"] in ("sfx", "vo"):
                continue
            tags.append(f'<audio id="{c["kind"]}-{i}" src="{html.escape(c["src"])}" data-start="{num(c["start"])}" '
                        f'data-duration="{num(c["length"])}" data-track-index="{c["track"]}" data-volume="{num(c["volume"])}"></audio>')
        return tags, cues

    def transitions_js(self):
        js = []
        for i, s in enumerate(self.scenes[1:], 1):
            e = s["_enter"]
            if e["type"] == "cut":
                continue
            of, ot, inf, int_, ease = TRANSITIONS[e["type"]]
            ease = e.get("ease", ease)
            prev = self.scenes[i - 1]["id"]
            if of is not None:
                js.append(tween_js(prev, of, ot, s["_start"], e["duration"], ease))
            js.append(tween_js(s["id"], inf, int_, s["_start"], e["duration"], ease))
        return js

    def write(self, out_name, force_scenes):
        comp_dir = os.path.join(self.project, "compositions")
        os.makedirs(comp_dir, exist_ok=True)
        fonts = self.sb.get("fonts") or DEFAULT_FONTS
        for f in fonts:  # copy bundled fonts in when the project doesn't have them yet
            dst = os.path.join(self.project, f["src"])
            bundled = os.path.join(SKILL, "assets", "fonts", os.path.basename(f["src"]))
            if not os.path.exists(dst):
                if not os.path.exists(bundled):
                    sys.exit(f"font {f['src']} is not in the project and not bundled; put the .woff2 there first")
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(bundled, dst)
                lic = {"Inter": "OFL-Inter.txt", "Source Serif 4": "OFL-SourceSerif4.txt", "JetBrains Mono": "OFL-JetBrainsMono.txt"}.get(f["family"])
                if lic:
                    shutil.copyfile(os.path.join(SKILL, "assets", "fonts", lic), os.path.join(os.path.dirname(dst), lic))
        created = []
        for s in self.scenes:
            p = os.path.join(comp_dir, f"{s['id']}.html")
            if force_scenes or not os.path.exists(p) or os.path.getsize(p) == 0:
                text = scene_skeleton(s, self.sb, self.W, self.H, first=s is self.scenes[0])  # build, then write
                with open(p, "w") as fh:
                    fh.write(text)
                created.append(s["id"])
        known = {f"{s['id']}.html" for s in self.scenes}
        orphans = sorted(f for f in os.listdir(comp_dir) if f.endswith(".html") and f not in known)

        hosts = []
        for i, s in enumerate(self.scenes):
            track = i % 2 if any(x["_enter"]["type"] != "cut" for x in self.scenes) else 0
            hosts.append(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" '
                         f'data-composition-src="compositions/{s["id"]}.html" data-start="{num(s["_start"])}" '
                         f'data-duration="{num(s["duration"])}" data-track-index="{track}" '
                         f'data-width="{self.W}" data-height="{self.H}"></div>')
        audio, cues = self.audio()
        ground = {**DEFAULT_PALETTE, **self.sb.get("palette", {})}["ground"]
        trans = self.transitions_js()
        index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={self.W}, height={self.H}" />
    <title>{html.escape(self.sb.get("title", "Motion video"))}</title>
    <script src="{GSAP}"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {self.W}px; height: {self.H}px; overflow: hidden; background: {ground}; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {ground}; }}
    </style>
  </head>
  <body>
    <!-- Generated by scaffold.py from storyboard.json: edit the storyboard and re-run, not this file. -->
    <div id="root" data-composition-id="main" data-start="0" data-width="{self.W}" data-height="{self.H}" data-duration="{num(self.total)}" data-fps="{self.fps}">
{chr(10).join("      " + h for h in hosts)}
{chr(10).join("      " + a for a in audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // Scene-to-scene transitions (from storyboard.json "enter"); scene timelines nest automatically.
{chr(10).join(trans) if trans else "      // all hard cuts"}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
        open(os.path.join(self.project, out_name), "w").write(index)
        if out_name == "index.html":
            timing = {"fps": self.fps, "width": self.W, "height": self.H, "duration": round(self.total, 4),
                      "scenes": [{"id": s["id"], "start": round(s["_start"], 4), "end": round(s["_end"], 4),
                                  "enter": s["_enter"], "label": s.get("text") or s["id"]} for s in self.scenes],
                      "cues": cues}
            json.dump(timing, open(os.path.join(self.project, "storyboard.timing.json"), "w"), indent=2)
        return created, orphans, cues


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyboard")
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", default="index.html", help="root file name (music-only.html for the audio check)")
    ap.add_argument("--mute", choices=["sfx", "music", "all"], help="leave out SFX+voiceover, music, or both")
    ap.add_argument("--force-scenes", action="store_true", help="OVERWRITE every scene file with a fresh skeleton")
    a = ap.parse_args()
    sb = json.load(open(a.storyboard))
    project = os.path.abspath(a.project)
    if not os.path.isdir(project):
        sys.exit(f"{project} doesn't exist; run `npx hyperframes init` first")
    board = Board(sb, project, a.mute)
    created, orphans, cues = board.write(a.out, a.force_scenes)

    print(f"{a.out}: {board.W}x{board.H} @ {board.fps}fps, {board.total:.2f}s, {len(board.scenes)} scenes, {len(cues)} audio cues")
    print(f"\n{'scene':18s} {'start':>7s} {'end':>7s} {'len':>6s}  enter")
    for s in board.scenes:
        e = s["_enter"]
        tr = e["type"] if e["type"] == "cut" else f"{e['type']} {e['duration']}s"
        print(f"{s['id']:18s} {s['_start']:7.2f} {s['_end']:7.2f} {s['duration']:6.2f}  {tr}")
    if cues:
        print(f"\n{'cue':34s} {'kind':5s} {'lands':>7s} {'starts':>7s} {'vol':>5s}")
        for c in cues:
            print(f"{c['src'][-34:]:34s} {c['kind']:5s} {c['at']:7.2f} {c['start']:7.2f} {c['volume']:5.2f}")
    mids = [round(s["_start"] + s["duration"] * f, 2) for s in board.scenes for f in (0.3, 0.85)]
    print("\nsnapshot list (30% and 85% into each scene):")
    print("  npx hyperframes snapshot --at " + ",".join(num(m) for m in mids) + " --no-end --output stills")
    if created:
        print("\nnew scene skeletons (now yours to edit): " + ", ".join(f"compositions/{c}.html" for c in created))
    if orphans:
        print("\nwarning: scene files no longer in the storyboard (delete them if unused): " + ", ".join(orphans))
    if a.out != "index.html":
        print(f"\nremember: delete {a.out} after rendering it; a second root makes `check` fail")


if __name__ == "__main__":
    main()
