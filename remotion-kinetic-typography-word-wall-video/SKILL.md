---
name: remotion-kinetic-typography-word-wall-video
description: Plan, build and validate text-only kinetic-typography promo videos in Remotion. The format is a typed setup line, a full-screen "word wall" montage that highlights one word per hard cut (values, services, features, skills…), a payoff statement and a logo or wordmark reveal, with cuts locked to the music's drop and beat, SFX on every cut, and measured loudness. It scales from a 6-second sting to a multi-act 60s+ piece and any aspect ratio. Use it whenever someone wants a typography-only or no-images promo, a "words on screen" brand spot, a services/values/skills montage, a personal-brand or portfolio reel made of text, a kinetic text video synced to music, or a recreation of a similar ad ("make a video like this RE/MAX one", "show what services I provide", "animate my values"), even if they never say "kinetic typography" or "word wall". Plan first: brief, copy, spec, timeline, PLAN.md. Then build on the bundled engine. Then verify with the bundled audio and frame checks.
---

# Kinetic typography word-wall video (Remotion)

A proven format: **typed setup → word wall → payoff statement → end card**, repeated as acts for
longer videos. The engine, planner and checkers in this skill came out of a long iteration with a
real user. The motion numbers were measured from a professional reference spot, and the rules
below are the corrections that user asked for, so new videos start from the finished state.

```
"I can build you"  →  [web apps][mobile apps][APIs]…[landing pages]  →  "…anything that works."  →  ALI/HAMZA
   typed (setup)          wall: one serif highlight per hard cut         statement (payoff)        end card
```

## Workflow

Work through these in order. **Planning is the first deliverable, and nothing is built before it.**
Most rework comes from skipping it: copy that doesn't read as a sentence, words too fast to read,
or music whose drop wasn't checked.

### 1. Plan (read `references/planning.md`)
1. **Brief.** Subject, the one-sentence message, wall items, brand (colors, fonts, logo), length
   and platform, and sound mode (music + SFX by default, SFX-only, or voiceover). Infer what you
   can from the repo or profile; ask only what you can't. Record your assumptions.
2. **Structure.** One act for 5–10s; several acts for longer pieces, each act its own idea, with
   varied wall shapes and colors so a long video doesn't repeat one rhythm.
3. **Copy, with the sentence test.** Read `<typed line> <wall word> … <statement>` aloud with
   every wall word. Fix articles and plurals ("build you **a** APIs" ✘). Every wall item must be
   true and traceable; never invent claims or stats.
4. **Music** (if any): copy the track into `public/music/`, then run
   `python3 <skill>/scripts/analyze_music.py public/music/<track> --fps 24 --drop-frame <f>`
   for BPM, drops and `trimBefore`. Pick a drop whose energetic section outlasts the edit.
5. **Spec → timeline.** Write `spec.json` (format in `planning.md`) and run
   `python3 <skill>/scripts/plan_timeline.py spec.json --out src/<Comp>/`. It writes
   `timing.json` and `timing.ts` and prints the timeline tables. It enforces readable, distinct
   wall durations and puts every structural cut on the beat.
6. **PLAN.md, before any composition code**, even when nobody is around to approve it. Write it
   next to the composition (template in `planning.md`): brief, brand, copy, the timeline tables,
   the sound plan, and every assumption you made. If the user is around, show the plan before
   building; for anything beyond a one-act sting, wait for approval. Writing it first is what
   catches copy and timing problems while they're cheap.

### 2. Build (read `references/scenes.md` for motion details and custom end cards)
1. Copy `assets/engine/KineticWordWall.tsx` and `assets/engine/example.config.tsx` into
   `src/<Comp>/` (next to `timing.ts`). Rename the example's exports. **Configure the engine,
   don't fork its motion.** Everything per-video lives in the config: palette, fonts, sound kit,
   music, and custom end-card components.
2. Measure each SFX file: `python3 <skill>/scripts/sfx_peaks.py public/<files> --fps 24`, and set
   each kit entry's `peakOffset` (see `references/audio-sync.md` for the kit).
3. A real logo → rebuild it as vector shapes in a `custom` end card (`scenes.md` §5). A plain
   name → a `wordmark` end card.
4. Register the composition in `src/Root.tsx` with `DURATION` / `FPS` from `timing.ts` and
   `defaultProps={{ mute: "none" }}`. Then run `npx tsc --noEmit`.

### 3. Validate (read `references/validation.md`)
Check renders, not code. Keep it light, since many users have modest machines:
- **Stills** at the frames `plan_timeline.py` prints as "suggested stills" (the middle of every scene and wall segment), with `--scale=0.25 --concurrency=2`, into a fresh directory, tiled into a sheet and looked at.
- **Two audio-only renders** (mix, plus music-only via `--props='{"mute":"sfx"}'`), then
  `python3 <skill>/scripts/check_audio.py mix.wav music.wav src/<Comp>/timing.json`.
- Fix, re-check, write the numbers into PLAN.md, and offer the MP4 render. Say what wasn't
  verified (by ear, phone width).

## Rules that came from real feedback

These are the defaults because a user asked for each one. Explain the trade-off rather than
silently breaking one:

- **Every wall word is readable**: ≥ 7 frames (0.29s) at 24fps for 1–2 words, more for longer
  phrases. 3–4 frame flashes look fast but read as noise.
- **Vary durations, and no two equal** (`distinct: true`). Equal segments feel mechanical. Since
  each segment covers the same drift distance in its own time, different lengths also give
  different speeds. Default shape: two quick, three slowing, accelerating, last word held.
  Distinct and readable means ≥ n·min + n(n−1)/2 frames, so a longer list makes a longer wall.
  Tell the user when that grows the video.
- **The drop lands on the cut into the wall.** The typed line plays over the pre-drop break.
  Later structural cuts land on beats (the planner snaps them). Wall swaps run free.
- **SFX louder than the music**: every hit ≥ ~3 dB over the music around it, measured with
  `check_audio.py`. Duck the music under the statement and reveal hits, **never under the drop**.
- **True peak ≤ −1.3 dBTP.** A hot peak is almost always one SFX stacking on a music hit.
  `check_audio.py` lists the loudest frames and the hit at each, so duck under that one hit
  (`music.duckFrames`) before lowering the whole bed. With the SFX leading, about −16 to −17 LUFS is fine; report it.
- **Don't time-stretch music** more than ~3% to force a grid.
- **Sound follows structure.** Hits are derived from scene boundaries, so never hand-place a hit
  that the engine can derive. Re-run the planner instead of editing `timing.ts`.
- **Text only, no chrome**: no eyebrow labels, badges, numbering or separators. One saturated wall
  color, its darker twin for the body text, a white serif highlight.
- **Undo means fully undo**: when asked to revert something (an effect, a voice), remove its code,
  config and generated files, then re-verify the output matches the earlier state.

## Scaling up

- **More words:** wall lengths grow with distinct ≥ 7f words. 12 words need ≥ 150 frames (6.3s).
  For very long lists, split them into two acts with a new typed line rather than one marathon wall.
- **Longer videos:** chain acts in one spec (the grid continues). Give each act its own wall
  color (an act-level `palette` in the spec) and its own `shape` (`fast-slow-accel-hold`,
  `accelerate-hold`, `decelerate`). Set the length with `targetFrames` instead of hand-tuning
  scene frames. Give each act's wall a high-energy music section. Only the last statement is the
  big payoff.
- **Other formats:** the engine scales to the frame width and enlarges type ×1.35 on portrait
  frames (`textScale` overrides it). For 1080×1920, keep wall words short, since the center row
  is narrower.
- **Other sound modes:** `"music": null` for SFX-only. Remove the music block, `EXTRA_HIT_FRAMES`
  and the `Logo` stub from the example config if unused, and check with `check_audio.py mix.wav none
  timing.json`. For a voiceover, timing follows speech (`audio-sync.md` §7).

## Bundled files

| Path | What it is |
|---|---|
| `assets/engine/KineticWordWall.tsx` | The engine: scene types `typed`, `wall`, `statement`, `wordmark`, `custom`; SFX kit and music with ducking; `mute` prop for validation renders |
| `assets/engine/example.config.tsx` | A complete config (palette, fonts, kit volumes that put SFX over a 0.4 music bed) to copy and edit |
| `scripts/plan_timeline.py` | spec.json → timing.json + timing.ts + timeline tables (readable, distinct, beat-locked) |
| `scripts/analyze_music.py` | Tempo from the kick grid, loudness map, drop candidates, `trimBefore` |
| `scripts/sfx_peaks.py` | `peakOffset` for each SFX file |
| `scripts/check_audio.py` | Loudness, true peak, the loudest frames and their hits, SFX-over-music margin per hit, beat sync per cut (`none` for SFX-only); exits 1 on failure |
| `scripts/contact_sheet.py` | Tiles the planner's suggested stills into one sheet, each labelled with its frame and what should be on screen |
| `references/planning.md` | Brief, structures from sting to multi-act, the copy test, the spec format, PLAN.md template |
| `references/scenes.md` | What each scene does and its limits, custom logo end cards, palette/type, porting a reference video |
| `references/audio-sync.md` | Sound modes, drop and beat locking, the SFX kit, levels and ducking, loudness, voiceover variant |
| `references/validation.md` | The light-weight render checks and pass criteria |

The scripts need Python 3 with numpy and scipy, plus ffmpeg on PATH.
