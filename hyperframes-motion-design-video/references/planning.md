# Planning: brief, copy, storyboard.json, PLAN.md

Planning is the first deliverable. Most rework traces back to a decision that could have been made
up front: the wrong type, copy that doesn't read, a scene too short to read, music whose
structure wasn't checked, or a number nobody could source.

## Contents
1. The brief, 2. Scene breakdown, 3. Copy tests, 4. storyboard.json, 5. PLAN.md template

---

## 1. The brief

Infer from the repo, portfolio, brand docs and GitHub profile, and ask only what you can't infer.
Record every assumption so the user can correct it in one pass.

| Question | Why it matters |
|---|---|
| What is it for, and what's the **one sentence** it says? | Every scene serves that sentence. |
| Audience, platform, aspect ratio | Pacing, safe zones, 16:9 vs 9:16 vs 1:1 vs 4:5. |
| Length | Checked against the type's range (`video-types.md`). |
| Brand: palette, type, logo | One ground, one ink, one accent. A real logo gets rebuilt as SVG. |
| Source material | Real UI, screenshots, footage, data. **No source, no claim.** |
| Sound mode | Music + SFX, SFX only, voiceover, or silent. Music sets a grid; VO sets timing. |
| Named reference | A studio (Ordinary Folk, FEVR, BUCK, Apple product films), a real video or a precise technique ("Swiss grid, hard cuts on the kick"). Never just "premium". |

Sizes: 1920×1080 (16:9), 1080×1920 (9:16), 1080×1080 (1:1), 1080×1350 (4:5). Use 30fps by
default, 24 for filmic pieces and 60 only for fast UI or a port of a 60fps reference.

## 2. Scene breakdown

- One dominant idea per scene, with three slots max: heading, optional support line, optional
  visual. If it needs more, it's two scenes.
- Give each scene a **duration and its reason** ("1.6s: snappy hook, one word"). Vary durations
  on purpose, because equal lengths read as mechanical.
- Read budget: ~0.4s minimum for 1–2 words, ~0.3s per word for a sentence once settled, plus
  the entrance. The final line holds ≥ 2s.
- Plan the **first frame** (it's the thumbnail) and the **last beat** (mark, CTA or URL).
- Look for reuse: a format skill's scene, a registry block (`/hyperframes-registry` for named
  looks such as a terminal, chart, map, grain or glitch), or a previous project's scene.
- Storyboard images: one still per key scene from an image skill if available
  (`minimalist-brand-image-generator` or similar), or snapshot a static draft. Put the path in
  PLAN.md.

## 3. Copy tests

- **Sentence test**: read all on-screen copy aloud in order as one piece. Fix grammar across
  cuts (articles, plurals, tense).
- **Trace test**: every number, logo, quote and claim has a source written in PLAN.md (user
  message, repo file, URL). No source means cut it or ask for one.
- **Squint test**: at phone width (390px) every word on screen is still readable. Use fewer, larger
  words.
- **No template words**: "Streamline your workflow", "Unlock the power of…" and "Next-gen"
  are banned. Use the product's own copy.

## 4. storyboard.json

The single source of **time and sound**. `scaffold.py` reads it; scene files never hold their
own start time.

```json
{
  "title": "Launch spot",
  "width": 1920, "height": 1080, "fps": 30,
  "palette": { "ground": "#0E0E11", "ink": "#F3F1EC", "muted": "#8C8A92", "accent": "#FF5B37" },
  "fonts": [
    { "family": "Inter", "weight": 500, "src": "assets/fonts/inter-latin-500-normal.woff2" },
    { "family": "Inter", "weight": 800, "src": "assets/fonts/inter-latin-800-normal.woff2" }
  ],
  "scenes": [
    { "id": "hook",  "duration": 2.4, "text": "Describe the video.", "plan": "word rise, stagger 0.07" },
    { "id": "plan",  "duration": 3.2, "enter": "push-left" },
    { "id": "data",  "duration": 2.6, "enter": { "type": "wipe-up", "duration": 0.4, "ease": "expo.inOut" } },
    { "id": "end",   "duration": 3.0, "enter": "cut", "palette": { "ground": "#F3F1EC", "ink": "#0E0E11" } }
  ],
  "music": { "src": "assets/music/bed.mp3", "gain": 0.35, "trim": 4.2, "fadeIn": 0.2, "fadeOut": 1.2, "duckDb": -6 },
  "audio": [
    { "src": "assets/sfx/swoosh.wav", "scene": "plan", "at": 0.0, "peak": 0.28, "volume": 0.6 },
    { "src": "assets/sfx/chime.wav",  "scene": "end",  "at": 0.9, "volume": 0.5, "duck": true },
    { "src": "assets/vo/line-1.wav",  "kind": "vo", "scene": "hook", "at": 0.1, "volume": 1 }
  ]
}
```

| Field | Meaning |
|---|---|
| `scenes[].id` | lowercase-dash id, which is also the file name `compositions/<id>.html` and the timeline key |
| `scenes[].duration` | seconds, including any transition overlap at its start |
| `scenes[].enter` | transition from the previous scene (`transitions.md`): a name, or `{type, duration, ease}`. It overlaps the previous scene by `duration` |
| `scenes[].text`, `support`, `plan`, `palette` | only used to write the first skeleton (and to label contact sheets) |
| `music.trim` | seconds skipped at the start of the file (puts a drop where you want it) |
| `music.duckDb` | dip under cues with `"duck": true` (1-frame attack, 2 hold, 6 release) |
| `music.voDuckDb` | carve under `kind: "vo"` cues (default −9 dB, 150 ms ramps) |
| `audio[]` | `src`; `scene` + `at` (scene-local s) or `t` (absolute s); `volume` (≤ 3.98); `peak` (s, from `sfx_peaks.py`); `kind` `sfx` / `vo`; `duck` |

Re-run `scaffold.py` after every storyboard edit. It never overwrites an existing scene file
(only `--force-scenes` does), and it warns about scene files that are no longer in the storyboard.

## 5. PLAN.md template

Write it in the project root before any scene is authored, and keep it the truth (edit the plan
first, then the code). On a resumed session, read PLAN.md before reading code.

```markdown
# <Project> — motion video plan

## Brief
- One sentence: …
- Type: <video-types.md row> · Length: <s> · Size: <WxH @ fps> · Platform: …
- Named reference: <studio / video / technique>
- Brand: ground … ink … accent … · type … · logo …
- Sound mode: … · Music: <file, BPM, drop at …s, license/source>
- Assumptions: …
- Sources: <every number/claim → where it came from>

## Scenes
### 1 — <id>: <one idea>
- On screen: heading "…" / support "…" / visual …
- Composition: <what's where, where the negative space is, depth layers>
- Storyboard still: <path>
- Duration: <s>, because <pacing reason>
- Motion: <one technique> · principle <ease-out / overshoot / follow-through / …> ·
  numbers <ease or spring(ζ), distance px, stagger s, zoom ×, blur> · keeps moving via <drift/push>
- Enter: <cut / push-left 0.45s power3.inOut …>, because …
- Sound: none | <file> peak on <scene-local s>, volume <…>, duck <y/n>
- Status: planned | built | validated

## Validation (filled in by the critic pass)
- check: <errors/warnings>
- Scores 1–10: hook _ · readability _ · motion _ · variety _ · composition _ · accuracy _ · sound _
- Audio: <LUFS> LUFS, <TP> dBTP, cue margins …
- Issues → fixes: …
- Not verified: …
```
