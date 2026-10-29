#!/usr/bin/env python3
"""Generate a HyperFrames composition (index.html) for a kinetic word-wall video.

    python3 build_composition.py --timing timing.json --config video.json --project <dir> \
        [--mute sfx|music|all] [--out index.html]

Inputs
  timing.json  from plan_timeline.py: scenes (typed / wall / statement / wordmark /
               custom), hits and structural frames.
  video.json   per-video look and sound (see assets/examples/video.json):
               width/height, palette, fonts, lineTracking, textScale, sound kit,
               sfxGain, extraHitSound, music, custom end-card fragments.

Output: <project>/<out> (default index.html), a standalone HyperFrames composition:
- one root (data-composition-id "main") with a finite data-duration;
- every scene, and every word-wall segment, is a timed .clip (hard cuts);
- all motion is per-frame tl.set() calls on ONE paused GSAP timeline, written
  from the same tables as the Remotion engine, so the motion matches it frame for
  frame and every frame is a pure function of time (seek-safe);
- every SFX hit is its own <audio id> placed at (hit frame − peakOffset);
- music is one <audio> with data-media-start (the trim), and its fades and ducks
  are a data-automation volume lane sampled per frame;
- fonts are local @font-face files (HyperFrames requires shipped fonts). The
  bundled Inter / Source Serif 4 are copied into <project>/assets/fonts when the
  config doesn't name its own.

--mute sfx writes a music-only variant (for check_audio.py's music render); use a
different --out, e.g. music-only.html, then render it with `--entry` or copy it to
a sibling project (see references/validation.md).
"""
import argparse
import html
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLED_FONTS = {
    "sans": {"family": "Inter", "files": {"500": "inter-latin-500-normal.woff2"}},
    "serif": {"family": "Source Serif 4", "files": {"400": "source-serif-4-latin-400-normal.woff2"}},
    "display": {"family": "Inter", "files": {"800": "inter-latin-800-normal.woff2"}, "weight": 800, "capRatio": 0.727},
}
VOLUME_MAX = 3.98  # HyperFrames data-volume ceiling (+12 dB)

# Reference metrics (px @736 × 414), identical to the Remotion engine.
LINE_SIZE, LINE_BASELINE_OFFSET = 37, 15
WALL_SIZE, WALL_PITCH, WALL_HL_BASELINE_OFFSET, HIGHLIGHT_SIZE = 46, 54, 13, 49
ACCENT_SCALE = 0.92
TYPED_RUN = [-0.5, -1, -2, -4, -6, -10, -19]
SEG_DRIFT = [0, -4.5, -6, -7, -8, -8, -8, -9, -9.5, -11, -15]
ST_CENTER = [57.5, 39, 27.5, 20.5, 15, 11.5, 8.5, 7, 5.5, 4, 3, 2.5, 1.5, 1.5, 1, 1, 0.5, 0.5, 0]
ST_EXTRA = [43, 28, 19, 13, 10, 7, 5, 4, 3, 2, 1, 1, 0.5, 0.5, 0]
DUCK = 0.5  # −6 dB


def px(v):
    return f"{v:.2f}px"


def num(v):
    return round(v, 3)


def seg_drift(f, n):
    if n < 2:
        return 0.0
    x = f * (len(SEG_DRIFT) - 1) / (n - 1)
    i = min(len(SEG_DRIFT) - 2, int(math.floor(x)))
    return SEG_DRIFT[i] + (SEG_DRIFT[i + 1] - SEG_DRIFT[i]) * (x - i)


def word_run(vocab, seed, count, avoid=None):
    rnd = random.Random(seed)
    out = []
    for _ in range(count):
        w = vocab[int(rnd.random() * len(vocab))]
        if (out and w == out[-1]) or w == avoid:
            w = vocab[(vocab.index(w) + 1) % len(vocab)]
        out.append(w)
    return " ".join(out)


class Builder:
    def __init__(self, timing, cfg, project, mute):
        self.t, self.c, self.project, self.mute = timing, cfg, project, mute
        self.fps = timing["fps"]
        self.W, self.H = cfg.get("width", 1920), cfg.get("height", 1080)
        base = min(self.W / 736, self.H / 414)
        ts = cfg.get("textScale")
        self.S = base * (ts if ts is not None else (1.35 if self.H > self.W else 1))
        self.cx, self.cy = self.W / 2, self.H / 2
        self.pal = cfg["palette"]
        self.fonts = self._fonts()
        self.body, self.js, self.sets, self.audio = [], [], [], []
        self.warnings = []
        self._durations = {}

    # ------------------------------------------------------------ fonts
    def _fonts(self):
        fonts = {}
        for role, default in BUNDLED_FONTS.items():
            f = dict(default, **self.c.get("fonts", {}).get(role, {}))
            files = {}
            for weight, path in f["files"].items():
                if os.sep not in path and "/" not in path:  # a bundled file name
                    dst = os.path.join(self.project, "assets", "fonts", path)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    if not os.path.exists(dst):
                        shutil.copy(os.path.join(SKILL_DIR, "assets", "fonts", path), dst)
                    path = f"assets/fonts/{path}"
                elif not os.path.exists(os.path.join(self.project, path)):
                    sys.exit(f"font file not found in the project: {path}")
                files[weight] = path
            f["files"] = files
            fonts[role] = f
        return fonts

    def font_css(self):
        out, seen = [], set()
        for f in self.fonts.values():
            for weight, path in f["files"].items():
                key = (f["family"], weight)
                if key in seen:
                    continue
                seen.add(key)
                out.append(
                    f'@font-face {{ font-family: "{f["family"]}"; font-weight: {weight}; '
                    f'src: url("{path}") format("woff2"); font-display: block; }}'
                )
        return "\n      ".join(out)

    def fam(self, role):
        # single quotes: this goes inside style="…" attributes
        return f"'{self.fonts[role]['family']}'"

    # ------------------------------------------------------------ helpers
    def palette_for(self, scene):
        return {**self.pal, **scene.get("palette", {})}

    def sec(self, frame):
        return num(frame / self.fps)

    def set(self, sel, props, frame):
        self.sets.append([sel, props, self.sec(frame)])

    def line_style(self, color, tracking_px=None):
        S = self.S
        fs = LINE_SIZE * S
        tr = tracking_px if tracking_px is not None else self.c.get("lineTracking", -0.02) * fs
        return (
            f"position:absolute;left:0;right:0;top:{px(self.cy + (LINE_BASELINE_OFFSET - LINE_SIZE) * S)};"
            f"height:{px(fs)};display:flex;justify-content:center;align-items:baseline;"
            f"font-family:{self.fam('sans')};font-weight:500;font-size:{px(fs)};line-height:1;"
            f"letter-spacing:{px(tr)};color:{color};white-space:pre;"
        )

    def section(self, sid, start, frames, bg, inner, track=0):
        self.body.append(
            f'<section id="{sid}" class="clip scene" data-start="{self.sec(start)}" '
            f'data-duration="{self.sec(frames)}" data-track-index="{track}" style="background:{bg};">\n'
            f"{inner}\n</section>"
        )

    # ------------------------------------------------------------ scenes
    def typed(self, i, s, t0):
        p = self.palette_for(s)
        sid = f"s{i}"
        words = "".join(
            f'<span id="{sid}-w{j}" class="w">{html.escape(("" if j == 0 else " ") + w)}</span>'
            for j, w in enumerate(s["words"])
        )
        self.section(sid, t0, s["frames"], p["paper"], f'  <div id="{sid}-line" style="{self.line_style(p["ink"])}">{words}</div>')
        for j, on in enumerate(s["wordOn"]):
            self.set(f"#{sid}-w{j}", {"display": "inline"}, t0 + on)
        run0 = s["frames"] - len(TYPED_RUN)
        last = None
        for f in range(s["frames"]):
            dx = (-2 if (f + 1) in s["wordOn"][1:] else 0) + (TYPED_RUN[f - run0] if f >= run0 else 0)
            if dx != last:
                self.set(f"#{sid}-line", {"x": num(dx * self.S)}, t0 + f)
                last = dx

    def wall(self, i, s, t0):
        p = self.palette_for(s)
        S = self.S
        text = (
            f"font-family:{self.fam('sans')};font-weight:500;font-size:{px(WALL_SIZE * S)};"
            f"line-height:1;color:{p['wallInk']};white-space:pre;"
        )
        rows_each = math.ceil(self.H / 2 / (WALL_PITCH * S)) + 1
        acc = 0
        for j, g in enumerate(s["segments"]):
            sid, seed = f"s{i}-g{j}", f"w{i}-s{j}"
            rnd = random.Random(seed + "-anchor")
            anchor = self.cx + (-2 + rnd.random() * 16) * S
            half = 2400 * S
            rows = []
            for r in range(-rows_each, rows_each + 1):
                top = self.cy + (WALL_HL_BASELINE_OFFSET + r * WALL_PITCH - WALL_SIZE * 0.9) * S
                if r == 0:
                    left = html.escape(word_run(s["vocab"], seed + "-l", 8, g["word"]) + " ")
                    right = html.escape(" " + word_run(s["vocab"], seed + "-r", 8, g["word"]))
                    rows.append(
                        f'    <div style="position:absolute;top:{px(top)};left:{px(anchor - half)};width:{px(half * 2)};'
                        f'display:flex;align-items:baseline;{text}">'
                        f'<span data-layout-ignore style="flex:1 1 0;text-align:right;">{left}</span>'
                        f'<span id="{sid}-hl" style="font-family:{self.fam("serif")};font-weight:400;'
                        f'font-size:{px(HIGHLIGHT_SIZE * S)};color:{p["highlight"]};letter-spacing:-0.01em;">'
                        f'{html.escape(g["word"])}</span>'
                        f'<span data-layout-ignore style="flex:1 1 0;">{right}</span></div>'
                    )
                else:
                    x = (-60 - random.Random(f"{seed}-x{r}").random() * 220) * S
                    rows.append(
                        # background rows are texture, not reading text: keep them out of the
                        # contrast/legibility audits (the highlight word stays audited)
                        f'    <div data-layout-ignore style="position:absolute;top:{px(top)};left:{px(x)};{text}">'
                        f'{html.escape(word_run(s["vocab"], f"{seed}-r{r}", 18))}</div>'
                    )
            inner = f'  <div id="{sid}-drift" style="position:absolute;inset:0;">\n' + "\n".join(rows) + "\n  </div>"
            self.section(sid, t0 + acc, g["frames"], p["wall"], inner, track=j)  # one Studio lane per segment
            for f in range(g["frames"]):
                self.set(f"#{sid}-drift", {"x": num(seg_drift(f, g["frames"]) * S)}, t0 + acc + f)
            acc += g["frames"]

    def statement(self, i, s, t0):
        p = self.palette_for(s)
        S = self.S
        sid = f"s{i}"
        fs = LINE_SIZE * S
        base_tr = self.c.get("lineTracking", -0.02) * fs
        glyphs = max(1, len(s["lead"] + s["accent"] + s.get("tail", "")))
        inner = (
            f'  <div id="{sid}-line" style="{self.line_style(p["ink"])}">'
            f'{html.escape(s["lead"])}<span id="{sid}-gap" style="display:inline-block;width:0px;"></span>'
            f'<span style="font-family:{self.fam("serif")};font-weight:400;color:{p["accent"]};'
            f'font-size:{px(fs * ACCENT_SCALE)};">{html.escape(s["accent"])}</span>'
            f'{html.escape(s.get("tail", ""))}</div>'
        )
        self.section(sid, t0, s["frames"], p["paper"], inner)
        for f in range(min(s["frames"], len(ST_CENTER))):
            extra = ST_EXTRA[min(f, len(ST_EXTRA) - 1)]
            self.set(f"#{sid}-line", {"x": num(ST_CENTER[f] * S),
                                      "letterSpacing": px(base_tr + extra * 0.2 / glyphs * S)}, t0 + f)
            self.set(f"#{sid}-gap", {"width": px(extra * 0.8 * S)}, t0 + f)

    def wordmark(self, i, s, t0):
        p = self.palette_for(s)
        S, W, H, cy = self.S, self.W, self.H, self.cy
        sid = f"s{i}"
        d = self.fonts["display"]
        cap_ratio = d.get("capRatio", 0.727)
        final_bar = s.get("finalBar", 0) * S
        lean = math.tan(math.radians(s.get("slant", 0)))
        gap_px = s.get("gap", 14) * S
        for _ in range(3):  # a slanted or kept bar needs room: widen the gap until it clears the letters
            fit = (0.84 * W - gap_px) / (0.68 * (len(s["left"]) + len(s["right"])))
            fsz = min(38 * S / cap_ratio, fit)
            cap_h = fsz * cap_ratio
            gap_px = max(gap_px, final_bar + cap_h * lean + (8 * S if final_bar or lean else 0))
        gh = gap_px / 2
        ax = W / 2 + 0.68 * fsz * (len(s["left"]) - len(s["right"])) / 2  # center the whole mark
        hide_at = s.get("hideAt", 15)
        yT, yB = cy - cap_h / 2, cy + cap_h / 2

        def state(f):
            k = 0.765 ** f
            bar_on = final_bar > 0 or f < hide_at
            bl, br = ax - final_bar / 2 - 12 * S * k, ax + final_bar / 2 + 40 * S * k
            edge = lambda x, y: x + (cy - y) * lean
            cl, cr = (bl, br) if bar_on else (ax, ax)
            return {
                "clipL": f"0,0 {edge(cl, 0):.2f},0 {edge(cl, H):.2f},{H} 0,{H}",
                "clipR": f"{edge(cr, 0):.2f},0 {W},0 {W},{H} {edge(cr, H):.2f},{H}",
                "lx": num(ax - gh + 37 * S * k),
                "rx": num(ax + gh - 43 * S * k),
                "bar": f"{edge(bl, yT):.2f},{yT:.2f} {edge(br, yT):.2f},{yT:.2f} {edge(br, yB):.2f},{yB:.2f} {edge(bl, yB):.2f},{yB:.2f}",
                "barOpacity": 1 if bar_on else 0,
            }

        s0 = state(0)
        txt = (f'font-family="{html.escape(self.fam("display"))}" font-weight="{d.get("weight", 800)}" '
               f'font-size="{fsz:.2f}" fill="{p["endInk"]}"')
        inner = (
            f'  <svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;inset:0;">\n'
            f'    <defs>\n'
            f'      <clipPath id="{sid}-cl"><polygon id="{sid}-clpoly" points="{s0["clipL"]}"/></clipPath>\n'
            f'      <clipPath id="{sid}-cr"><polygon id="{sid}-crpoly" points="{s0["clipR"]}"/></clipPath>\n'
            f'    </defs>\n'
            f'    <g clip-path="url(#{sid}-cl)"><text id="{sid}-left" x="{s0["lx"]}" y="{yB:.2f}" text-anchor="end" {txt}>{html.escape(s["left"])}</text></g>\n'
            f'    <g clip-path="url(#{sid}-cr)"><text id="{sid}-right" x="{s0["rx"]}" y="{yB:.2f}" text-anchor="start" {txt}>{html.escape(s["right"])}</text></g>\n'
            f'    <polygon id="{sid}-bar" points="{s0["bar"]}" fill="{p["bar"]}"/>\n'
            f'  </svg>'
        )
        self.section(sid, t0, s["frames"], p["endBg"], inner)
        prev = None
        for f in range(min(s["frames"], 40)):
            st = state(f)
            if st == prev:
                continue
            self.set(f"#{sid}-clpoly", {"attr": {"points": st["clipL"]}}, t0 + f)
            self.set(f"#{sid}-crpoly", {"attr": {"points": st["clipR"]}}, t0 + f)
            self.set(f"#{sid}-left", {"attr": {"x": st["lx"]}}, t0 + f)
            self.set(f"#{sid}-right", {"attr": {"x": st["rx"]}}, t0 + f)
            self.set(f"#{sid}-bar", {"attr": {"points": st["bar"]}, "opacity": st["barOpacity"]}, t0 + f)
            prev = st

    def custom(self, i, s, t0):
        ref = s["ref"]
        path = self.c.get("custom", {}).get(ref)
        if not path:
            sys.exit(f'custom scene "{ref}" has no fragment in config "custom"')
        frag = open(os.path.join(self.project, path)).read()
        frag = re.sub(r"<!--.*?-->", "", frag, flags=re.S)  # docs in comments may mention the tag
        # A <script data-hf-scene> block becomes a function of (tl, T0, FPS, W, H, ID)
        script = ""
        if "<script data-hf-scene>" in frag:
            a = frag.index("<script data-hf-scene>")
            b = frag.index("</script>", a)
            script = frag[a + len("<script data-hf-scene>"):b]
            frag = frag[:a] + frag[b + len("</script>"):]
        p = self.palette_for(s)
        self.section(f"s{i}", t0, s["frames"], p["endBg"], frag.replace("{{ID}}", f"s{i}"))
        if script:
            self.js.append(
                f"(function (tl, T0, FPS, W, H, ID) {{{script.replace('{{ID}}', f's{i}')}}})"
                f"(tl, {self.sec(t0)}, {self.fps}, {self.W}, {self.H}, 's{i}');"
            )

    # ------------------------------------------------------------ audio
    def media_seconds(self, src):
        if src not in self._durations:
            out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                  os.path.join(self.project, src)], capture_output=True, text=True).stdout.strip()
            self._durations[src] = float(out or 0)
        return self._durations[src]

    def audio_tags(self):
        total = self.t["durationInFrames"]
        dur = self.sec(total)
        m = self.c.get("music")
        if m and self.mute not in ("music", "all"):
            if not os.path.exists(os.path.join(self.project, m["src"])):
                sys.exit(f"music file not found in the project: {m['src']}")
            duck_kinds = m.get("duckOn", [])
            ducks = [h["frame"] for h in self.t["hits"] if h["kind"] in duck_kinds] + m.get("duckFrames", [])
            fi, fo, gain = m.get("fadeIn", 8), m.get("fadeOut", 24), m["gain"]

            def env(f):
                fade = min(1.0, f / fi if fi else 1.0, (total - f) / fo if fo else 1.0)
                d = 1.0
                for h in ducks:
                    if h - 1 <= f < h:
                        d = min(d, 1 - (1 - DUCK) * (f - (h - 1)))
                    elif h <= f <= h + 2:
                        d = min(d, DUCK)
                    elif h + 2 < f <= h + 8:
                        d = min(d, DUCK + (1 - DUCK) * (f - (h + 2)) / 6)
                return max(0.0, fade) * d * gain

            pts, last = [], None
            for f in range(total + 1):
                v = round(env(f), 4)
                if v != last or f == total:
                    pts.append({"t": self.sec(f), "v": v})
                    last = v
            lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": pts}]})
            rate = m.get("rate", 1)
            self.audio.append(
                f'<audio id="music" src="{html.escape(m["src"])}" data-start="0" data-duration="{dur}" '
                f'data-media-start="{num(m["trimBefore"] / self.fps)}" data-track-index="1" data-volume="1" '
                + (f'data-playback-rate="{rate}" ' if rate != 1 else "")
                + f"data-automation='{lane}'></audio>"
            )
        if self.mute in ("sfx", "all"):
            return
        kit, gain = self.c.get("sound", {}), self.c.get("sfxGain", 1)
        track_ends = {}  # track index -> frame the last sound on it ends
        hits = [(h, kit.get(h["kind"])) for h in self.t["hits"] if h["kind"] != "extra"]
        hits += [(h, self.c.get("extraHitSound")) for h in self.t["hits"] if h["kind"] == "extra"]
        for n, (h, s) in enumerate(hits):
            if not s:
                continue
            if not os.path.exists(os.path.join(self.project, s["src"])):
                sys.exit(f"SFX file not found in the project: {s['src']}")
            vol = s["volume"] * gain
            if vol > VOLUME_MAX:
                self.warnings.append(f"{s['src']} volume {vol:.2f} capped at {VOLUME_MAX}; "
                                     f"bake a louder copy of the file instead")
                vol = VOLUME_MAX
            start = max(0, h["frame"] - s.get("peakOffset", 0))
            length = min(math.ceil(self.media_seconds(s["src"]) * self.fps), total - start)
            if length <= 0:
                continue
            # first track (from 2; 0 = scenes, 1 = music) that's free: no overlapping audio on a track
            track = next(k for k in range(2, 999) if track_ends.get(k, -1) <= start)
            track_ends[track] = start + length
            self.audio.append(
                f'<audio id="sfx-{n}-{h["kind"]}" src="{html.escape(s["src"])}" '
                f'data-start="{self.sec(start)}" data-duration="{self.sec(length)}" '
                f'data-track-index="{track}" data-volume="{num(vol)}"></audio>'
            )

    # ------------------------------------------------------------ document
    def scene_file(self, cid, frames):
        """One scene as a sub-composition: styles, markup and its own scene-local timeline."""
        sets = json.dumps(self.sets, separators=(",", ":"))
        extra = "\n        ".join(self.js)
        return f"""<!doctype html>
<html>
  <head><meta charset="UTF-8" /></head>
  <body>
    <!-- Generated by build_composition.py — edit the spec / video.json and rebuild, not this file. -->
    <template>
      <style>
        {self.font_css()}
        #{cid} {{ position: absolute; inset: 0; overflow: hidden; }}
        #{cid} .scene {{ position: absolute; inset: 0; overflow: hidden; }}
        #{cid} .w {{ display: none; }}
      </style>
      <div id="{cid}" data-composition-id="{cid}" data-width="{self.W}" data-height="{self.H}"
        data-duration="{self.sec(frames)}">
{chr(10).join(self.body)}
      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
        {sets}.forEach(([sel, props, t]) => tl.set(sel, props, t));
        {extra}
        window.__timelines["{cid}"] = tl;
      </script>
    </template>
  </body>
</html>
"""

    def build(self, mute_suffix=""):
        os.makedirs(os.path.join(self.project, "compositions"), exist_ok=True)
        hosts, files, t0 = [], [], 0
        for i, s in enumerate(self.t["scenes"]):
            frames = sum(g["frames"] for g in s["segments"]) if s["kind"] == "wall" else s["frames"]
            self.body, self.js, self.sets = [], [], []
            getattr(self, s["kind"])(i, s, 0)  # scene-local time
            cid = f"scene-{i}-{s['kind']}"
            rel = f"compositions/{cid}.html"
            files.append((rel, self.scene_file(cid, frames)))
            hosts.append(
                f'<div id="{cid}" class="clip" data-composition-id="{cid}" data-composition-src="{rel}" '
                f'data-start="{self.sec(t0)}" data-duration="{self.sec(frames)}" data-track-index="0" '
                f'data-width="{self.W}" data-height="{self.H}"></div>'
            )
            t0 += frames
        self.audio = []
        self.audio_tags()
        total = self.t["durationInFrames"]
        index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={self.W}, height={self.H}" />
    <title>Kinetic word wall</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {self.W}px; height: {self.H}px; overflow: hidden; background: {self.pal["paper"]}; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {self.pal["paper"]}; }}
    </style>
  </head>
  <body>
    <!-- Generated by build_composition.py — edit the spec / video.json and rebuild, not this file. -->
    <div id="root" data-composition-id="main" data-start="0" data-width="{self.W}" data-height="{self.H}"
      data-duration="{self.sec(total)}" data-fps="{self.fps}">
      {chr(10).join("      " + h for h in hosts).strip()}
{chr(10).join("      " + a for a in self.audio)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
        return index, files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timing", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--mute", choices=["none", "sfx", "music", "all"], default="none")
    ap.add_argument("--out", default="index.html")
    a = ap.parse_args()
    timing, cfg = json.load(open(a.timing)), json.load(open(a.config))
    if timing.get("fps") and cfg.get("fps") and cfg["fps"] != timing["fps"]:
        sys.exit("fps differs between timing.json and video.json")
    b = Builder(timing, cfg, a.project, a.mute)
    doc, files = b.build()
    for rel, text in files:
        open(os.path.join(a.project, rel), "w").write(text)
    out = os.path.join(a.project, a.out)
    open(out, "w").write(doc)
    for w in b.warnings:
        print("warning:", w, file=sys.stderr)
    print(f"wrote {out}: {timing['durationInFrames']} frames @ {timing['fps']}fps, "
          f"{len(files)} scene sub-compositions, {len(b.audio)} audio clips"
          + (f", muted: {a.mute}" if a.mute != "none" else ""))


if __name__ == "__main__":
    main()
