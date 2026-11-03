#!/usr/bin/env python3
"""Generate a HyperFrames stat-reel project from reel.json.

    python3 build_reel.py reel.json --project <hyperframes-project>

Relative paths in reel.json resolve against "baseDir" (itself relative to
reel.json, default "."). Writes <project>/index.html (the root: one host per beat + all audio) and
<project>/compositions/beat-N-<name>.html (one sub-composition per beat, each
with its own paused, beat-local GSAP timeline), and copies fonts, images and audio into <project>/assets/. All
motion is the measured reference choreography from references/format.md,
written in beat-local seconds, so dropping a beat (e.g. "beats": {"thanks":
false}) pulls every later beat earlier.

Seek safety:
- things that appear at a moment are their own timed clips (data-start /
  data-duration), so the runtime owns their visibility;
- counters, the caret, typing, the arrow and the squiggle sway are "drivers":
  a proxy tween whose onUpdate recomputes the DOM from local time, so any seek
  lands on the same pixels;
- the scattered letter order comes from a seeded PRNG.
Edit reel.json and rebuild; don't hand-edit the generated HTML.
"""
import argparse
import html
import json
import os
import shutil
import subprocess
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE_W, STAGE_H = 720, 540

# (beat, length in seconds) in reference order; times inside each beat are local.
BEATS = [
    ("collageTitle", 0.80),
    ("wordsLight", 1.80),
    ("wordsDark", 1.90),
    ("cursorCounter", 1.90),
    ("ghostCounter", 3.25),
    ("badgeCounter", 2.55),
    ("badgeSentence", 1.05),
    ("arrowSearch", 6.75),  # arrowWords + searchCollage share one background crossfade
    ("thanks", 1.80),
    ("endCard", 3.52),
]

PALETTE = {
    "lime": "#ecfaa8",
    "ink": "#004449",
    "cream": "#f2ffc3",
    "ghost": "#d2e59c",
    "accent": "#dcf36a",
    "pill": "#eef9b8",
    "squiggleDark": "#1f5c60",
    "end": "#fcfcfc",
    "brand": "#9ccc2c",
}

INTRO_SHOTS = [(37, 0, 118, 90), (356, 0, 143, 104), (617, 40, 103, 98), (219, 117, 86, 67),
               (497, 208, 173, 135), (559, 421, 161, 119), (360, 474, 123, 66)]
OUTRO_SHOTS = [(-10, -10, 188, 114, 18.90), (548, 447, 172, 93, 19.00), (159, 465, 232, 75, 19.10),
               (-10, 383, 99, 113, 19.10), (372, -10, 177, 72, 19.25), (634, 90, 96, 218, 19.30),
               (86, 200, 136, 106, 19.40), (259, 130, 316, 247, 19.55)]

SQ_LIGHT = ["M -20 40 C 40 70, 90 105, 140 102 C 190 98, 215 50, 222 -10",
            "M 740 440 C 690 480, 640 505, 590 505 C 530 505, 480 478, 420 478 C 360 478, 325 500, 322 560"]
SQ_DARK = ["M 380 -10 C 420 40, 470 45, 530 35 C 600 22, 660 20, 740 45",
           "M -20 540 C 10 505, 60 490, 110 505 C 140 515, 150 530, 155 545"]

ICONS = {
    "code": '<svg width="46" height="28" viewBox="0 0 50 30" style="margin-left:10px"><g fill="none" stroke="currentColor" '
            'stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="14,5 4,15 14,25"/>'
            '<polyline points="36,5 46,15 36,25"/><line x1="29" y1="4" x2="21" y2="26"/></g></svg>',
    "eye": '<svg width="52" height="31" viewBox="0 0 50 30" style="margin-left:8px"><path d="M3 15 C 12 3, 38 3, 47 15 '
           'C 38 27, 12 27, 3 15 Z" fill="none" stroke="currentColor" stroke-width="2.6"/><circle cx="25" cy="15" r="6.5" '
           'fill="none" stroke="currentColor" stroke-width="2.6"/><circle cx="25" cy="15" r="2" fill="currentColor"/></svg>',
    "none": "",
}

# Neutral three-blade placeholder; parts fly in from data-dx/dy with data-rot, staggered by data-delay.
PLACEHOLDER_MARK = (
    '<svg width="60" height="60" viewBox="-24 -24 48 48" style="overflow:visible">'
    + "".join(
        f'<g data-dx="{dx}" data-dy="{dy}" data-rot="90" data-delay="{d}" data-svg-origin="0 0">'
        f'<path d="M 0 -2 C 6 -8, 8 -16, 4 -22 C -2 -16, -6 -8, 0 -2 Z" transform="rotate({a})" fill="{c}"/></g>'
        for a, dx, dy, d, c in [(0, 0, -40, 0, "#9ccc2c"), (120, 34.6, 20, 0.06, "#6aa21e"), (240, -34.6, 20, 0.12, "#9ccc2c")]
    )
    + "</svg>"
)

JS_PRELUDE = r"""
const tl = gsap.timeline({ paused: true });
const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));
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
const E = {
  lin: (t) => t,
  out: bez(0.16, 1, 0.3, 1),
  inOut: bez(0.65, 0, 0.35, 1),
  in: bez(0.5, 0, 0.75, 0),
  outCubic: (t) => 1 - Math.pow(1 - t, 3),
};
// Clamped piecewise interpolation, easing applied per segment (like Remotion's interpolate).
function r(t, xs, ys, e = E.lin) {
  if (t <= xs[0]) return ys[0];
  for (let i = 0; i < xs.length - 1; i++) {
    if (t <= xs[i + 1]) return ys[i] + (ys[i + 1] - ys[i]) * e((t - xs[i]) / (xs[i + 1] - xs[i]));
  }
  return ys[ys.length - 1];
}
// A driver: recompute DOM from local time on every seek inside [start, start + dur].
function drive(start, dur, fn) {
  const o = { t: 0 };
  tl.fromTo(o, { t: 0 }, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => fn(o.t) }, start);
  fn(0);
}
// Seeded PRNG (cyrb-style hash + mulberry32) for the scattered letter order.
function rng(seed) {
  let h = 1779033703 ^ seed.length;
  for (const c of seed) { h = Math.imul(h ^ c.charCodeAt(0), 3432918353); h = (h << 13) | (h >>> 19); }
  let a = h >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function scatter(sel, seed, start, spread) {
  const rand = rng(seed);
  $$(sel).forEach((el) => tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.14, ease: "none" }, start + rand() * spread));
}
"""


def n(v):
    return f"{round(v, 4):g}"


def esc(s):
    return html.escape(str(s))


_IDS = iter(range(1, 10 ** 6))


def clip(start, dur, inner, cls="", style="", id_=None, extra=""):
    i = f' id="{id_ or f"c{next(_IDS)}"}"'

    return (f'<div{i} class="clip {cls}" data-start="{n(start)}" data-duration="{n(dur)}"'
            + (f' style="{style}"' if style else "") + (f" {extra}" if extra else "") + f">{inner}</div>")


def letters(text, cls, colors=None):
    out = []
    for i, ch in enumerate(text):
        c = f' style="color:{colors(i)}"' if colors else ""
        out.append(f'<span class="{cls}"{c}>{esc(ch)}</span>')
    return "".join(out)


class Reel:
    def __init__(self, cfg, cfg_dir, project):
        self.c, self.dir, self.project = cfg, cfg_dir, project
        self.p = {**PALETTE, **cfg.get("palette", {})}
        on = cfg.get("beats", {})
        self.beats, t = [], 0.0
        for name, length in BEATS:
            if name == "badgeSentence":
                length += cfg.get("badgeSentence", {}).get("extraHold", 0.3)
            if on.get(name, True):
                self.beats.append((name, t, length))
                t += length
        self.total = t
        self.starts = {name: s for name, s, _ in self.beats}
        self.html, self.js, self.copied = [], [], {}
        self.warnings = []

    # ------------------------------------------------------------ assets
    def asset(self, src, sub):
        """Copy a file referenced by reel.json into <project>/assets/<sub>/ and return its project path."""
        if src in self.copied:
            return self.copied[src]
        base = os.path.join(self.dir, self.c.get("baseDir", "."))
        path = src if os.path.isabs(src) else os.path.join(base, src)
        if not os.path.exists(path):
            sys.exit(f"file not found: {src} (resolved to {path})")
        os.makedirs(os.path.join(self.project, "assets", sub), exist_ok=True)
        rel = f"assets/{sub}/{os.path.basename(path)}"
        shutil.copyfile(path, os.path.join(self.project, rel))
        self.copied[src] = rel
        return rel

    def image(self, i):
        imgs = self.c["images"]
        return self.asset(imgs[i % len(imgs)], "images")

    # ------------------------------------------------------------ beats
    def section(self, name, start, length, bg, inner):
        self.html.append(f'<div id="b-{name}" class="beat" style="background:{bg}">{inner}</div>')

    def collageTitle(self, L, D):
        c, p = self.c["collageTitle"], self.p
        shots = "".join(
            f'<div class="shot" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background-image:url(\'{self.image(i)}\')"></div>'
            for i, (x, y, w, h) in enumerate(INTRO_SHOTS))
        icon = c.get("icon", "code")
        icon = ICONS.get(icon, icon)
        title = (
            f'<div id="ct-title" class="ct-title">'
            f'<div class="ct-line" style="top:268px;font-size:62px">{esc(c["line1"])}</div>'
            f'<div class="ct-line ct-row" style="top:355px;font-size:51px">'
            f'<div class="ct-pill">{esc(c["stat"])}{icon}</div><span style="margin-left:20px">{esc(c["line2"])}</span></div>'
            f'<div class="ct-line" style="top:440px;font-size:70px;font-weight:600">{esc(c["line3"])}</div></div>')
        self.section("collageTitle", L, D, p["lime"], f'<div id="ct-shots" class="full shots">{shots}</div>{title}')
        self.js.append(f"""
tl.fromTo("#ct-title", {{ x: 0 }}, {{ x: -150, duration: 0.75, ease: "power2.in" }}, {n(L)});
tl.fromTo("#ct-title", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.45, ease: "none" }}, {n(L + 0.3)});
tl.fromTo("#ct-shots .shot", {{ y: 0, scale: 1 }}, {{ y: -11.2, scale: 1.04, duration: 0.8, ease: "none" }}, {n(L)});
tl.fromTo("#ct-shots", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.33, ease: "none" }}, {n(L + 0.45)});""")

    def _words(self, name, L, D, words, offsets, sizes, bg, color, paths, stroke, width, draw, sway):
        sq = "".join(f'<path id="{name}-sq{i}" d="{d}" pathLength="1" fill="none" stroke="{stroke}" stroke-width="{width}" '
                     f'stroke-linecap="round" style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1"/>' for i, d in enumerate(paths))
        inner = f'<svg class="full" width="720" height="540" viewBox="0 0 720 540" data-layout-allow-overflow>{sq}</svg>'
        ends = offsets[1:] + [D]
        for i, w in enumerate(words):
            inner += clip(L + offsets[i], ends[i] - offsets[i],
                          f'<span id="{name}-w{i}" class="word" style="font-size:{sizes[i]}px;color:{color}">{esc(w)}</span>',
                          cls="full center")
            self.js.append(f"""
tl.fromTo("#{name}-w{i}", {{ opacity: 0.55 }}, {{ opacity: 1, duration: 0.12, ease: "none" }}, {n(L + offsets[i])});
tl.fromTo("#{name}-w{i}", {{ scale: 0.95 }}, {{ scale: 1.03, duration: 1, ease: "none" }}, {n(L + offsets[i])});""")
        self.section(name, L, D, bg, inner)
        (d0, dd), (amp, freq, k) = draw, sway
        self.js.append(f"""
tl.fromTo(["#{name}-sq0", "#{name}-sq1"], {{ strokeDashoffset: 1.1 }}, {{ strokeDashoffset: 0, duration: {dd}, ease: E.out }}, {n(L + d0)});
drive({n(L)}, {n(D)}, (t) => {{
  const d = Math.sin(({n(L)} + t) * {freq}) * {amp};
  $("#{name}-sq0").setAttribute("transform", `translate(${{{k[0]} * d}} ${{{k[1]} * d}})`);
  $("#{name}-sq1").setAttribute("transform", `translate(${{{k[2]} * d}} ${{{k[3]} * d}})`);
}});""")

    def wordsLight(self, L, D):
        self._words("wordsLight", L, D, self.c["wordsLight"], [0, 0.4, 0.8], [61, 61, 61], self.p["lime"], self.p["ink"],
                    SQ_LIGHT, "#fff", 7, (0.3, 0.6), (6, 2, (-1, 0.5, 1, -0.4)))

    def wordsDark(self, L, D):
        self._words("wordsDark", L, D, self.c["wordsDark"], [0.1, 0.6, 1.4], [57, 57, 66], self.p["ink"], self.p["cream"],
                    SQ_DARK, self.p["squiggleDark"], 6, (0, 0.7), (10, 1.6, (1, 0, -1, 0)))

    def cursorCounter(self, L, D):
        c, p = self.c["cursorCounter"], self.p
        caret = f"position:absolute;top:-0.12em;width:3px;height:1.3em;background:{p['ink']}"
        inner = (
            f'<div class="full center"><div id="cc-line" class="cc-line">'
            f'<span class="rel">'
            f'<span class="rel">'
            + clip(L + 1.35, D - 1.35, "", id_="cc-box",
                   style=f"position:absolute;right:-4px;top:-18px;bottom:-14px;width:3px;border-radius:10px;background:{p['ink']}")
            + f'<span id="cc-n" class="rel" style="color:{p["ink"]}">{c.get("from", 0)}{esc(c["suffix"])}</span></span>'
            f'<span class="rel" style="margin-left:0.28em">{esc(c["label"])}'
            + clip(L + 0.75, 0.6, "", id_="cc-c2", style=caret)
            + "</span>"
            + clip(L, 0.75, "", id_="cc-c1", style=caret)
            + "</span></div></div>")
        self.section("cursorCounter", L, D, p["lime"], inner)
        self.js.append(f"""
tl.fromTo("#cc-line", {{ scale: 0.62 }}, {{ scale: 1, duration: 1.85, ease: "power1.out" }}, {n(L)});
drive({n(L)}, 0.8, (t) => {{ $("#cc-n").textContent = Math.round(r(t, [0, 0.8], [{c.get("from", 0)}, {c["to"]}], E.outCubic)) + {json.dumps(c["suffix"])}; }});
drive({n(L)}, 0.75, (t) => {{ const q = E.inOut(t / 0.75); $("#cc-c1").style.left = `calc(${{q * 100}}% + ${{-12 + 18 * q}}px)`; }});
drive({n(L + 0.75)}, 0.6, (t) => {{
  const b = r(t, [0.25, 0.6], [0, 1], E.inOut);
  const el = $("#cc-c2");
  el.style.left = `calc(${{(1 - b) * 100}}% + ${{6 - 12 * b}}px)`;
  el.style.opacity = t < 0.25 ? (Math.floor(({n(L + 0.75)} + t) * 8) % 2 === 0 ? 1 : 0.2) : 1;
}});
drive({n(L + 1.35)}, {n(D - 1.35)}, (t) => {{ const q = r(t, [0, 0.3], [0, 1], E.out); $("#cc-box").style.width = `calc(${{q * 100}}% + ${{3 + 22 * q}}px)`; }});
tl.fromTo("#cc-n", {{ color: "{p['ink']}" }}, {{ color: "{p['accent']}", duration: 0.23, ease: "none" }}, {n(L + 1.42)});""")

    def ghostCounter(self, L, D):
        c, p = self.c["ghostCounter"], self.p
        a, b = c["then"]
        inner = clip(L, 2.0,
                     f'<div class="full center"><div id="gc-n" class="gc-n" data-layout-ignore style="color:{p["ghost"]}">0</div></div>'
                     f'<div class="full center"><div class="gc-w" style="color:{p["ink"]}">{letters(c["word"], "gc-l")}</div></div>',
                     cls="full")
        inner += clip(L + 2.0, 0.6, f'<span id="gc-t1" class="word" style="font-size:48px;font-weight:600;color:{p["ink"]}">{esc(a)}</span>', cls="full center")
        inner += clip(L + 2.6, D - 2.6, f'<span id="gc-t2" class="word" style="font-size:52px;font-weight:600;color:{p["ink"]}">{esc(b)}</span>', cls="full center")
        self.section("ghostCounter", L, D, p["lime"], inner)
        self.js.append(f"""
drive({n(L)}, 0.8, (t) => {{ $("#gc-n").textContent = Math.round(r(t, [0, 0.8], [0, {c["count"]}], E.outCubic)); }});
tl.fromTo("#gc-n", {{ opacity: 0.5 }}, {{ opacity: 1, duration: 0.1, ease: "none" }}, {n(L)});
scatter(".gc-l", "ghost-word", {n(L + 0.85)}, 0.55);
tl.fromTo("#gc-t1", {{ opacity: 0.4 }}, {{ opacity: 1, duration: 0.12, ease: "none" }}, {n(L + 2.0)});
tl.fromTo("#gc-t2", {{ opacity: 0.4 }}, {{ opacity: 1, duration: 0.12, ease: "none" }}, {n(L + 2.6)});""")

    def badgeCounter(self, L, D):
        c, p = self.c["badgeCounter"], self.p
        steps = c["steps"]
        if len(steps) != 8:
            sys.exit("badgeCounter.steps needs 8 values: climb, hold, climb, hold, climb, hold, drop")
        inner = (f'<div class="full center"><div id="bc-g" class="row" style="color:{p["ink"]}">'
                 f'<span id="bc-b" class="badge">{steps[0]}+</span>'
                 f'<div id="bc-lw" style="overflow:hidden;max-width:400px"><span id="bc-l" style="display:inline-block;'
                 f'font-weight:500;padding-left:12px;white-space:nowrap">{esc(c["label"])}</span></div></div></div>')
        self.section("badgeCounter", L, D, p["lime"], inner)
        self.js.append(f"""
tl.fromTo("#bc-g", {{ opacity: 0.5 }}, {{ opacity: 1, duration: 0.15, ease: "none" }}, {n(L)});
drive({n(L)}, {n(D)}, (t) => {{
  const ks = [0, 0.55, 0.7, 1.2, 1.35, 1.85, 2.1, 2.5], vs = {json.dumps(steps)};
  let v = vs[vs.length - 1];
  for (let i = 0; i < ks.length - 1; i++) {{
    if (t <= ks[i + 1]) {{ v = r(t, [ks[i], ks[i + 1]], [vs[i], vs[i + 1]], vs[i + 1] < vs[i] ? E.in : E.inOut); break; }}
  }}
  $("#bc-b").textContent = Math.round(v) + "+";
  $("#bc-b").style.fontSize = r(t, [0, 1.85, 2.1, 2.5], [28, 60, 60, 26], E.inOut) + "px";
  $("#bc-l").style.fontSize = r(t, [0, 1.85], [26, 42]) + "px";
  $("#bc-lw").style.opacity = r(t, [2.07, 2.15], [1, 0]);
  $("#bc-lw").style.maxWidth = r(t, [2.07, 2.21], [400, 0]) + "px";
}});""")

    def badgeSentence(self, L, D):
        c, p = self.c["badgeSentence"], self.p
        inner = (f'<div class="full center"><div id="bs" class="bs" style="color:{p["ink"]}">'
                 f'<div>{esc(c["lead"])} <span id="bs-n" class="badge" style="font-size:23px;margin:0 6px;padding:0.4em 0.85em;'
                 f'vertical-align:1px">{c["from"]}+</span> {esc(c["tail"])}</div><div>{esc(c["line2"])}</div></div></div>')
        self.section("badgeSentence", L, D, p["lime"], inner)
        self.js.append(f"""
drive({n(L)}, 0.18, (t) => {{ $("#bs-n").textContent = Math.round(r(t, [0, 0.18], [{c["from"]}, {c["to"]}])) + "+"; }});
tl.fromTo("#bs", {{ opacity: 0.55 }}, {{ opacity: 1, duration: 0.1, ease: "none" }}, {n(L)});
tl.fromTo("#bs", {{ scale: 0.93 }}, {{ scale: 1.04, duration: {n(D)}, ease: "none" }}, {n(L)});""")

    def arrowSearch(self, L, D):
        c, p = self.c["arrowSearch"], self.p
        A = lambda x: L + x - 13.25  # reference seconds → reel time
        ph_times = [(14.7, 15.85), (15.9, 16.95), (17.0, 18.0)]
        group_end = 17.9
        g = clip(A(13.3), 1.1, f'<span id="as-ct" class="word">{esc(c["checkOut"])}</span>', id_="as-check",
                 style=f"position:absolute;left:240px;top:238px;width:240px;text-align:center;font-size:50px;"
                       f"font-weight:500;white-space:nowrap;color:{p['ink']}", extra="data-layout-allow-overflow")
        g += clip(A(13.85), group_end - 13.85,
                  f'<svg width="720" height="540" viewBox="0 0 720 540"><g stroke="{p["ink"]}" stroke-width="2.6" '
                  f'stroke-linecap="round" stroke-linejoin="round" fill="none"><line id="as-line" x1="0" y1="270" x2="0" y2="270"/>'
                  f'<polyline id="as-head" points=""/></g></svg>', cls="full", id_="as-arrow", extra="data-layout-allow-overflow")
        for i, (s, e) in enumerate(ph_times):
            words = "".join(f'<span class="as-w{i}">{" " if j else ""}{esc(w)}</span>' for j, w in enumerate(c["phrases"][i]))
            g += clip(A(s), min(e, group_end) - s, f'<div id="as-ph{i}">{words}</div>',
                      style=f"position:absolute;left:272px;top:239px;font-size:51px;font-weight:500;white-space:pre;color:{p['ink']}")
            self.js.append(f"""
$$(".as-w{i}").forEach((el, j) => tl.fromTo(el, {{ opacity: 0.3 }}, {{ opacity: 1, duration: 0.12, ease: "none" }}, {n(A(s))} + j * 0.08));""")
            if e <= group_end:
                self.js.append(f"""
tl.fromTo("#as-ph{i}", {{ opacity: 1 }}, {{ opacity: 0.35, duration: 0.1, ease: "none" }}, {n(A(e - 0.1))});""")
        group = clip(A(13.3), group_end - 13.3, f'<div id="as-gi" class="full">{g}</div>', cls="full")
        url = c["url"]
        pill = clip(A(17.75), 19.5 - 17.75,
                    f'<div id="as-po"><div id="as-pill" class="pill" style="background:{p["pill"]};color:{p["ink"]}">'
                    f'<svg width="28" height="28" viewBox="0 0 24 24"><circle cx="13.5" cy="10.5" r="7" fill="none" '
                    f'stroke="{p["ink"]}" stroke-width="2.4"/><path d="M8.5 15.5 L3.5 20.5" stroke="{p["ink"]}" '
                    f'stroke-width="2.4" stroke-linecap="round"/></svg>'
                    f'<span id="as-url">{letters(url, "as-c")}</span></div></div>', cls="full center")
        shots = ""
        for i, (x, y, w, h, at) in enumerate(OUTRO_SHOTS):
            shots += clip(A(at), 20.0 - at,
                          f'<div id="cl-d{i}" class="fill"><div id="cl-i{i}" class="fill shot-bg" style="background-image:url(\'{self.image(i)}\')"></div></div>',
                          style=f"position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px",
                          extra="data-layout-allow-overflow")
            cx, cy = x + w / 2 - STAGE_W / 2, y + h / 2 - STAGE_H / 2
            self.js.append(f"""
tl.fromTo("#cl-i{i}", {{ x: {n(-cx * 0.25)}, y: {n(-cy * 0.25)}, scale: 0.55 }}, {{ x: 0, y: 0, scale: 1, duration: 0.3, ease: E.out }}, {n(A(at))});
tl.fromTo("#cl-i{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, ease: "none" }}, {n(A(at))});
tl.fromTo("#cl-d{i}", {{ scale: 1 }}, {{ scale: {n(1 + 0.03 * (20.0 - at))}, duration: {n(20.0 - at)}, ease: "none" }}, {n(A(at))});""")
        inner = f'<div id="as-bg" class="full" style="background:{p["lime"]}"></div>{group}{pill}{shots}'
        self.section("arrowSearch", L, D, p["lime"], inner)
        self.js.append(f"""
tl.fromTo("#as-bg", {{ backgroundColor: "{p['lime']}" }}, {{ backgroundColor: "{p['ink']}", duration: 0.73, ease: E.inOut }}, {n(A(17.62))});
tl.fromTo("#as-ct", {{ opacity: 0.6, scale: 0.96 }}, {{ opacity: 1, scale: 0.988, duration: 0.1, ease: "none" }}, {n(A(13.3))});
tl.fromTo("#as-ct", {{ scale: 0.988 }}, {{ scale: 1.02, duration: 0.6, ease: "none", immediateRender: false }}, {n(A(13.4))});
tl.fromTo("#as-check", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.15, ease: "none" }}, {n(A(14.15))});
drive({n(A(13.3))}, {n(group_end - 13.3)}, (t) => {{
  const T = 13.3 + t;
  const left = r(T, [13.85, 14.0, 14.1, 14.2, 14.35], [240, 207, 93, -60, -300]);
  $("#as-check").style.left = left + "px";
  if (T < 13.85) return;
  const tip = r(T, [13.85, 14.0, 14.1, 14.2, 14.3, 14.4, 14.5, 14.7, 15.0], [492, 501, 462, 384, 315, 270, 237, 210, 205]);
  const tail = Math.min(left + 254, tip);
  const len = tip - tail, head = Math.min(11, len * 0.5);
  const line = $("#as-line"), hd = $("#as-head");
  line.setAttribute("x1", tail); line.setAttribute("x2", tip);
  line.style.opacity = hd.style.opacity = len < 2 ? 0 : 1;
  hd.setAttribute("points", `${{tip - head}},${{270 - head}} ${{tip}},270 ${{tip - head}},${{270 + head}}`);
}});
tl.fromTo("#as-gi", {{ x: 0 }}, {{ x: -160, duration: 0.25, ease: E.in }}, {n(A(17.6))});
tl.fromTo("#as-gi", {{ filter: "blur(0px)" }}, {{ filter: "blur(8px)", duration: 0.25, ease: "none" }}, {n(A(17.6))});
tl.fromTo("#as-gi", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.23, ease: "none" }}, {n(A(17.62))});
tl.fromTo("#as-po", {{ y: 26, scale: 0.35 }}, {{ y: 0, scale: 1, duration: 0.45, ease: E.out }}, {n(A(17.75))});
tl.fromTo("#as-po", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, ease: "none" }}, {n(A(17.75))});
tl.fromTo("#as-pill", {{ scale: 1 }}, {{ scale: 0.8, duration: 0.3, ease: "none" }}, {n(A(19.15))});
tl.fromTo("#as-pill", {{ backgroundColor: "{p['pill']}" }}, {{ backgroundColor: "rgba(238,249,184,0.35)", duration: 0.3, ease: "none" }}, {n(A(19.2))});
tl.fromTo("#as-pill", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.12, ease: "none" }}, {n(A(19.38))});
drive({n(A(17.75))}, 1.75, (t) => {{
  const T = 17.75 + t, chars = $$(".as-c"), N = chars.length;
  const typed = T < 18.75 ? r(T, [17.8, 18.5], [0, N]) : r(T, [18.75, 19.1], [N, 0], E.in);
  const vis = Math.ceil(typed - 1e-6);
  chars.forEach((el, i) => {{ el.style.display = i < vis ? "inline" : "none"; el.style.opacity = r(typed - i, [0, 1], [0.3, 1]); }});
  $("#as-url").style.display = vis ? "inline" : "none";
  $("#as-pill").style.padding = vis ? "0 30px 0 28px" : "0";
}});""")

    def thanks(self, L, D):
        c, p = self.c["thanks"], self.p
        text = c["accent"] + c["rest"]
        k = len(c["accent"])
        inner = (f'<div class="full center"><div id="th" class="th">'
                 f'{letters(text, "th-l", lambda i: p["accent"] if i < k else p["cream"])}</div></div>')
        self.section("thanks", L, D, p["ink"], inner)
        self.js.append(f"""
tl.fromTo("#th", {{ scale: 1.06 }}, {{ scale: 0.9, duration: {n(D)}, ease: "none" }}, {n(L)});
scatter(".th-l", "thanks", {n(L)}, 0.95);""")

    def endCard(self, L, D):
        c, p = self.c["endCard"], self.p
        wm = c["wordmark"]
        mark = c.get("logoSvg") or PLACEHOLDER_MARK
        text_len = len(wm.get("bold", "")) + len(wm.get("dot", "")) + len(wm.get("light", ""))
        reveal_w = max(520, round(text_len * 36))  # ≈0.6em per glyph at 60px
        if text_len * 36 + 72 > STAGE_W - 40:
            self.warnings.append(f"wordmark is long ({text_len} chars); check it fits the end card")
        inner = (
            f'<div class="full center"><div class="row">'
            f'<div id="ec-mark" class="row">{mark}</div>'
            f'<div id="ec-ww" style="overflow:hidden;white-space:nowrap;max-width:0px">'
            f'<div id="ec-wm" style="padding-left:12px;font-size:60px;line-height:1.2">'
            f'<span style="font-weight:700;color:#111">{esc(wm.get("bold", ""))}</span>'
            f'<span style="font-weight:700;color:{p["brand"]}">{esc(wm.get("dot", ""))}</span>'
            f'<span id="ec-light" class="it" style="color:#888">{esc(wm.get("light", ""))}</span>'
            f'</div></div></div></div>'
            f'<div id="ec-black" class="full" style="background:#000;opacity:0"></div>')
        self.section("endCard", L, D, p["end"], inner)
        self.js.append(f"""
$$("#ec-mark [data-dx]").forEach((el) => {{
  const d = parseFloat(el.dataset.delay || 0);
  const o = el.dataset.svgOrigin ? {{ svgOrigin: el.dataset.svgOrigin }} : {{}};
  tl.fromTo(el, {{ x: +el.dataset.dx || 0, y: +el.dataset.dy || 0, rotation: +el.dataset.rot || 0, ...o }},
    {{ x: 0, y: 0, rotation: 0, duration: 0.45, ease: E.out, ...o }}, {n(L)} + d);
  tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.14, ease: "none" }}, {n(L)} + d);
}});
$$("#ec-mark [data-at]").forEach((el) => tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.02, ease: "none" }}, {n(L)} + parseFloat(el.dataset.at)));
tl.fromTo("#ec-ww", {{ maxWidth: 0 }}, {{ maxWidth: {reveal_w}, duration: 0.5, ease: E.out }}, {n(L + 0.65)});
tl.fromTo("#ec-wm", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05, ease: "none" }}, {n(L + 0.65)});
tl.fromTo("#ec-light", {{ color: "#888888" }}, {{ color: "#111111", duration: 0.4, ease: "none" }}, {n(L + 0.75)});
tl.fromTo("#ec-black", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.6, ease: "power1.inOut" }}, {n(L + 1.4)});""")

    # ------------------------------------------------------------ audio
    def seconds(self, rel):
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                              os.path.join(self.project, rel)], capture_output=True, text=True).stdout.strip()
        return float(out or 0)

    def audio(self):
        tags, total = [], self.total
        m = self.c.get("music")
        if m:
            rel = self.asset(m["src"], "audio")
            g = m.get("gain", 0.5)
            lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
                {"t": 0, "v": 0}, {"t": round(10 / 60, 4), "v": g},
                {"t": round(total - 1.5, 4), "v": g}, {"t": round(total, 4), "v": 0}]}]})
            dur = min(self.seconds(rel), total)
            tags.append(f'<audio id="music" src="{esc(rel)}" data-start="0" data-duration="{n(dur)}" '
                        f'data-track-index="1" data-volume="1" data-automation=\'{lane}\'></audio>')
        ends = {}
        for i, s in enumerate(self.c.get("sfx", [])):
            if s["beat"] not in self.starts:
                continue
            rel = self.asset(s["src"], "audio")
            start = max(0.0, self.starts[s["beat"]] + s.get("at", 0))
            dur = min(self.seconds(rel), total - start)
            if dur <= 0:
                continue
            track = next(k for k in range(2, 99) if ends.get(k, -1) <= start)
            ends[track] = start + dur
            tags.append(f'<audio id="sfx-{i}" src="{esc(rel)}" data-start="{n(start)}" data-duration="{n(dur)}" '
                        f'data-track-index="{track}" data-volume="{n(min(s.get("volume", 0.4), 1))}"></audio>')
        return tags

    # ------------------------------------------------------------ document
    def css(self, W, H, scale):
        p = self.p
        return f"""@font-face {{ font-family: "Figtree"; font-style: normal; font-weight: 300 900; font-display: block;
        src: url("assets/fonts/figtree-latin-variable-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Figtree"; font-style: italic; font-weight: 300; font-display: block;
        src: url("assets/fonts/figtree-latin-300-italic.woff2") format("woff2"); }}
      #{{cid}} {{ position: absolute; inset: 0; overflow: hidden; background: #000; font-family: "Figtree", sans-serif; }}
      .stage {{ position: absolute; left: 0; top: 0; width: {STAGE_W}px; height: {STAGE_H}px; overflow: hidden;
        transform: scale({scale}); transform-origin: 0 0; }}
      .beat, .full {{ position: absolute; inset: 0; overflow: hidden; }}
      .center {{ display: flex; align-items: center; justify-content: center; }}
      .row {{ display: flex; align-items: center; }}
      .rel {{ position: relative; display: inline-block; }}
      .fill {{ width: 100%; height: 100%; display: block; object-fit: cover; }}
      .word {{ display: inline-block; font-weight: 500; white-space: nowrap; line-height: 1.2; }}
      .shot {{ position: absolute; background-size: cover; background-position: center; }}
      .shot-bg {{ background-size: cover; background-position: center; }}
      .ct-title {{ position: absolute; left: 58px; top: 0; width: 640px; height: 540px; color: {p["ink"]}; font-weight: 500; line-height: 1; }}
      .ct-line {{ position: absolute; left: 0; white-space: nowrap; transform: translateY(-50%); }}
      .ct-row {{ display: flex; align-items: center; }}
      .ct-pill {{ display: flex; align-items: center; height: 60px; padding: 0 18px 0 20px; border-radius: 30px;
        background: {p["ink"]}; color: {p["cream"]}; font-size: 34px; }}
      .cc-line {{ display: inline-block; font-size: 45px; font-weight: 500; white-space: nowrap; }}
      .gc-n {{ font-size: 470px; font-weight: 600; letter-spacing: -0.02em; line-height: 1; }}
      .gc-w {{ font-size: 32px; font-weight: 600; white-space: pre; }}
      .badge {{ display: inline-block; font-weight: 600; line-height: 1; padding: 0.32em 0.3em 0.28em; border-radius: 0.2em;
        background: {p["ink"]}; color: {p["cream"]}; }}
      .bs {{ display: inline-block; font-size: 28px; font-weight: 500; text-align: center; line-height: 1.9; }}
      .pill {{ display: flex; align-items: center; justify-content: center; height: 76px; min-width: 76px;
        border-radius: 38px; font-size: 22px; font-weight: 500; white-space: pre; }}
      #as-url {{ margin-left: 18px; }}
      .th {{ display: inline-block; font-size: 53px; font-weight: 500; white-space: pre; }}
      .it {{ font-style: italic; font-weight: 300; }}"""

    def build(self):
        """Return (index.html, [(relative path, sub-composition html)])."""
        fonts_dir = os.path.join(self.project, "assets", "fonts")
        os.makedirs(fonts_dir, exist_ok=True)
        for f in ("figtree-latin-variable-normal.woff2", "figtree-latin-300-italic.woff2", "OFL-Figtree.txt"):
            shutil.copyfile(os.path.join(SKILL, "assets", "fonts", f), os.path.join(fonts_dir, f))
        scale = self.c.get("scale", 2)
        W, H = round(STAGE_W * scale), round(STAGE_H * scale)
        css_t = self.css(W, H, scale)
        files, hosts = [], []
        for i, (name, start, length) in enumerate(self.beats):
            # Each beat is its own sub-composition with a beat-local timeline (L = 0).
            self.html, self.js = [], []
            getattr(self, name)(0, length)
            cid = f"beat-{i}-{name}"
            rel = f"compositions/{cid}.html"
            files.append((rel, f"""<!doctype html>
<html>
  <head><meta charset="UTF-8" /></head>
  <body>
    <!-- Generated by build_reel.py from reel.json — edit the config and rebuild, not this file. -->
    <template>
      <style>
      {css_t.replace("{cid}", cid)}
      </style>
      <div id="{cid}" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-duration="{n(length)}">
        <div class="stage">{"".join(self.html)}</div>
      </div>
      <script>
(() => {{{JS_PRELUDE}{"".join(self.js)}
window.__timelines["{cid}"] = tl;
}})();
      </script>
    </template>
  </body>
</html>
"""))
            hosts.append(f'<div id="{cid}" class="clip" data-composition-id="{cid}" data-composition-src="{rel}" '
                         f'data-start="{n(start)}" data-duration="{n(length)}" data-track-index="0" '
                         f'data-width="{W}" data-height="{H}"></div>')
        audio = self.audio()
        index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{esc(self.c.get("title", "Stat reel"))}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }}
    </style>
  </head>
  <body>
    <!-- Generated by build_reel.py from reel.json — edit the config and rebuild, not this file. -->
    <div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}" data-duration="{n(self.total)}" data-fps="{self.c.get('fps', 60)}">
{chr(10).join("      " + h for h in hosts)}
{chr(10).join("      " + a for a in audio)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
        return index, files


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config", help="reel.json")
    ap.add_argument("--project", required=True, help="HyperFrames project directory (index.html is written here)")
    a = ap.parse_args()
    cfg = json.load(open(a.config))
    reel = Reel(cfg, os.path.dirname(os.path.abspath(a.config)), os.path.abspath(a.project))
    doc, files = reel.build()
    comp_dir = os.path.join(a.project, "compositions")
    os.makedirs(comp_dir, exist_ok=True)
    for f in os.listdir(comp_dir):  # beats can be switched off: drop files from an earlier build
        if f.startswith("beat-") and f.endswith(".html"):
            os.remove(os.path.join(comp_dir, f))
    for rel, text in files:
        open(os.path.join(a.project, rel), "w").write(text)
    out = os.path.join(a.project, "index.html")
    open(out, "w").write(doc)
    for w in reel.warnings:
        print("warning:", w, file=sys.stderr)
    beats = ", ".join(f"{name}@{s:.2f}s" for name, s, _ in reel.beats)
    print(f"wrote {out}: {reel.total:.2f}s, {len(reel.beats)} beats ({beats})")


if __name__ == "__main__":
    main()
