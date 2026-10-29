# Planning a word-wall video

Planning is the first deliverable. Nothing gets built until the spec and `PLAN.md` exist. Most
revisions on the reference project came from decisions that could have been made up front: copy
that didn't read as a sentence, durations too short to read, and music chosen without checking its
structure.

## Contents
1. The brief: what to ask or infer
2. Choosing a structure (short sting → long multi-act)
3. Writing the copy (the sentence test)
4. Writing spec.json
5. PLAN.md template

---

## 1. The brief

Answer these before writing anything. Infer from context (a portfolio, a GitHub profile, brand
files in the repo) and ask only what you can't infer:

| Question | Why it matters |
|---|---|
| Who or what is it for, and what's the one message? | The whole video is one sentence; decide it first. |
| What goes on the wall? (values, services, features, skills, cities…) | The wall is a list of parallel nouns or noun phrases, 4–12 per act. |
| Brand: colors, fonts, logo? | One saturated "wall" color, a near-white paper, a near-black ink. The logo decides the end card (wordmark vs custom). |
| Length / platform? | Sets the number of acts. Social cutdown 5–10s, spot 10–20s, long piece 30–90s. |
| Sound: music, SFX only, or voiceover? | Music sets the beat grid every cut snaps to. SFX-only frees the timing. A voiceover makes timing follow speech. |
| A reference video to match? | If given, measure it frame by frame (see `scenes.md`, "Porting a reference"). |

Write down anything you assumed, so the user can correct it in one pass.

## 2. Structure

The unit is an **act**: `typed setup → word wall → statement payoff`. One end card closes the video.

| Length | Shape | Notes |
|---|---|---|
| 5–10s (sting / cutdown) | 1 act + end card | The reference spot: 6–8s. |
| 10–20s (spot) | 1 act with a longer wall (10–14 words), or 2 short acts | Second act = a new setup line and a different wall color or vocab. |
| 30–90s (long piece) | 3–6 acts + end card, each act its own idea | Vary between acts: wall shape (accelerate / decelerate / fast-slow-accel-hold), wall color, highlight count. A long piece repeating one rhythm is the main failure mode. |

Long-video rules:
- **Each act gets one new idea.** Act 1 says what you do, act 2 how, act 3 for whom, for example.
  Each act's statement can be a mini-payoff; only the last one is the big one.
- **Alternate energy.** A dense, fast wall, then a slower one; a typed line can be a single word.
- **Music must cover the length.** Find a section map (`analyze_music.py`) and give each act's wall
  a high-energy section. Use a later drop for a later act if the track has one.
- **Plan acts as separate specs only if they need different music.** Otherwise one spec chains all
  acts and the grid continues across them.
- **Give each act its own wall color** with an act-level `palette`, and a different `shape`.
  Set the length with `targetFrames` rather than hand-tuning scene frames.

## 3. Copy: the sentence test

The video reads as one sentence: `<typed line> <each wall word> … <statement>`. Read it aloud
with *every* wall word:

> "I can build you **web apps** … **APIs** … **AI agents** … anything that works." ✔
> "I can build you **a** APIs" ✘ (article clash; drop the article, use plurals)
> "You build it with **trust**." ✔ (the statement completes the typed line)

Rules:
- All wall words share one grammatical form (all plural nouns, or all "-ing", or all values).
- Each wall word must be true of the subject and traceable (a service on their profile, a value
  in their brand doc). Never invent claims or stats.
- Keep wall words to 1–3 words. A 20-character phrase is about the longest that fits the center
  row at 1080p.
- The statement's accent is 1–3 words. It goes in the serif, in the accent color.
- No eyebrow labels, badges, numbering or separators. The type *is* the design.

## 4. spec.json

`scripts/plan_timeline.py` turns this into frame-exact timing. Fields:

```json
{
  "fps": 24,
  "music": {"bpm": 100, "dropFrame": 20, "grid": "beat"},
  "minReadable": 10,
  "acts": [
    {
      "typed": {"words": ["I", "can", "build", "you"], "wordGap": 3},
      "wall": {
        "words": ["web apps", "mobile apps", "dashboards", "APIs"],
        "vocab": ["web apps", "mobile apps", "dashboards", "APIs", "SaaS products", "admin panels"],
        "shape": "fast-slow-accel-hold",
        "distinct": true
      },
      "statement": {"lead": "…anything ", "accent": "that works", "tail": ".", "minFrames": 28}
    }
  ],
  "end": {"kind": "wordmark", "left": "ALI", "right": "HAMZA", "frames": 36}
}
```

- `music`: `null` for SFX-only or voiceover. With music, `bpm` and the drop come from
  `analyze_music.py`. `dropFrame` is where the first wall cut should land (≥ the typed line's need).
  `grid`: "beat" (default), "half" or "bar" for later cuts.
- `minReadable`: **10 frames (0.42s)** by default, HyperFrames' floor for 1–2 word lines. Longer
  phrases need more and the planner applies it per word: 3 words 1.05s (26f), 4 words 1.28s (31f),
  hyphens split words ("single-origin beans" is 3). A long phrase therefore grows the wall a lot;
  shorten it ("single-origin") if the length matters. Raise `minReadable` for a slower mood.
- `typed.firstWordAt`: frame the first typed word cuts on, default **0**, so the first frame (the
  social thumbnail) isn't empty. `check` warns `first_frame_empty` otherwise.
- **The closing line.** When the end card has no text (a logo made of shapes), the statement is the
  film's last line, and `check` wants it held for **≥ 2s**: set `statement.minFrames` ≥ 48 at 24fps.
  A `wordmark` end card is text, so it is the last line itself: give it `frames` ≥ 48. The planner
  warns about both cases.
- `wall.shape`: `fast-slow-accel-hold` (quick start, slowing, accelerating, last held; the
  default), `accelerate-hold` (speeds up, then holds the last word), `decelerate`, `accelerate`
  (ends on its shortest word, which suits a hard cut but not a hand-off), `even`, or explicit
  `"frames": [...]` (then leave `shape` out). The planner warns if those break a reading floor or
  repeat a length, and with music it lengthens the last word so the next cut lands on the grid.
  Prefer a shape: it solves floors, distinctness and the grid together.
- `wall.distinct`: no two words share a length, so no two move at the same speed. It needs
  ≥ n·min + n(n−1)/2 frames; the planner grows the wall to fit and to end on the grid.
- `vocab`: background-row words. Include the wall words plus 3–6 related extras for texture.
- `palette` (on an act, or on its `typed` / `wall` / `statement`): overrides palette tokens for
  those scenes, e.g. `{"wall": "#0E9F7E", "wallInk": "#053D31", "accent": "#0E9F7E"}`. This is how
  a multi-act video changes the wall color per act.
- `targetFrames` (top level): a desired total length. The planner grows the auto-solved walls
  toward it, in proportion to their word counts, and reports what it got. It warns when a word
  would stay up for more than ~2s; then add words or an act instead of stretching.
- `wall.minTotal`: a floor for one wall's length, if you need it longer than its words require.
- **Filling a length with few words.** `targetFrames` only grows walls, and a word held past ~2s
  drags. So for, say, 30s from 13 short items, also lengthen the other scenes: `typed.frames` (how
  long the typed scene runs before its cut; default is just long enough for the words) and
  `statement.minFrames` (both then snap up to the grid). Then let `targetFrames` absorb the rest.
- `end.kind`: `"wordmark"` (two text groups split by a bar: `left`, `right`, optional `slant`,
  `finalBar`, `gap`; the gap widens itself to clear a slanted or kept bar) or `"custom"` with `"ref"`, for a bespoke logo component (see `scenes.md`).
  `extraHits` are frames after the end card starts, snapped to the nearest beat; use them for a
  second beat in the logo animation.

Run it, read the table, and adjust the spec, not the generated files:

```bash
python3 <skill>/scripts/plan_timeline.py spec.json --out <project>/
```

## 5. PLAN.md template

Write this file next to the composition before building. Keep it current: change the plan first,
then the code.

```markdown
# <project> — Kinetic word-wall plan (HyperFrames)

## Classification
- Type: text-only kinetic typography promo (typed → word wall → statement → end card), <N> acts
- Length: <s> (<frames> @ <fps>), <W×H>
- Message: "<the full sentence>"
- Reference: <video / brand / "the house style of this skill">

## Brand
| Token | Value | Source |
(paper, ink, wall, wallInk, highlight, accent, endBg, endInk, bar; fonts)

## Copy
- Typed line, wall words (with the source for each claim), statement, end card.
- Sentence test: passed / changes made.

## Timeline
(paste plan_timeline.py's tables: moments vs beats, wall words with frames/seconds/starts)

## Sound
- Music: file, BPM, drop at <s>, trimBefore, gain, duckOn; or "none".
- SFX kit: hit → file, peakOffset, volume.
- Targets: SFX ≥ +3 dB over music at every hit; true peak ≤ −1.3 dBTP; ≈ −14 to −17 LUFS.

## Validation
(check_audio.py output summary, frames checked, what's not yet verified: by ear, phone width)
```
