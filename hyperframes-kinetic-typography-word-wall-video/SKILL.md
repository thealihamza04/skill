---
name: hyperframes-kinetic-typography-word-wall-video
description: Plan, build and validate text-only kinetic-typography promo videos as HyperFrames HTML compositions. The format is a typed setup line, a full-screen "word wall" montage that highlights one word per hard cut (values, services, features, skills…), a payoff statement and a logo or wordmark reveal, with cuts locked to the music's drop and beat, SFX on every cut, and measured loudness. A bundled generator writes the whole project (scene sub-compositions, one seek-safe GSAP timeline each, framework-owned audio), so it passes `hyperframes check` with zero findings. Scales from a 6-second sting to multi-act 60s+ pieces in any aspect ratio. Use it whenever someone wants this kind of typography-only or no-images promo, services/values/skills montage, personal-brand reel made of text, or kinetic text video synced to music, and they want it in HyperFrames / HTML / GSAP rather than Remotion ("make it with hyperframes", "an HTML video", "a word-wall video without React"), or they're working in a HyperFrames project. Plan first, then generate, then verify with the bundled checks. For the same format in Remotion, use remotion-kinetic-typography-word-wall-video.
---

# Kinetic typography word-wall video (HyperFrames)

The same proven format as the Remotion version of this skill: **typed setup → word wall → payoff
statement → end card**, repeated as acts for longer videos. Here the output is a HyperFrames
project: plain HTML, one paused GSAP timeline per scene, and audio owned by the framework. The
planner and the audio checkers are shared with the Remotion skill; a generator replaces its
React engine and writes motion identical to it, frame for frame.

```
"I can build you"  →  [web apps][mobile apps][APIs]…[landing pages]  →  "…anything that works."  →  logo
   typed (setup)          wall: one serif highlight per hard cut         statement (payoff)         end card
```

Run the CLI as the version the scaffold pins in its `package.json` (`npx -y hyperframes@<pin> …`);
the bare `npx hyperframes` below is shorthand. Before writing anything by hand, read `/hyperframes-core` (the composition contract) and
`/hyperframes-cli` (commands). The generator already follows them; you need them to extend it
(custom end cards) or diagnose a finding.

## Workflow

Work through these in order. **Planning is the first deliverable, and nothing is generated before
it.** Most rework comes from skipping it: copy that doesn't read as a sentence, words too fast to
read, or music whose drop wasn't checked.

### 1. Plan (read `references/planning.md`)
1. **Brief.** Subject, the one-sentence message, wall items, brand (colors, fonts, logo), length
   and platform, and sound mode (music + SFX by default, SFX-only, or voiceover). Infer what you
   can from the repo or profile; ask only what you can't. Record your assumptions.
2. **Structure.** One act for 5–10s; several acts for longer pieces, each act its own idea, with
   varied wall shapes and colors so a long video doesn't repeat one rhythm.
3. **Copy, with the sentence test.** Read `<typed line> <wall word> … <statement>` aloud with
   every wall word. Fix articles and plurals ("build you **a** APIs" ✘). Every wall item must be
   true and traceable; never invent claims or stats.
4. **Project.** Scaffold it: `HYPERFRAMES_SKIP_SKILLS=1 npx -y hyperframes init <project> --non-interactive`
   (the generator writes `index.html` from `video.json`'s `width`/`height`, so those set the size). Copy the music into `<project>/assets/music/`
   and the SFX into `<project>/assets/sfx/`.
5. **Music** (if any): `python3 <skill>/scripts/analyze_music.py <project>/assets/music/<track> --fps 24 --drop-frame <f>`
   gives BPM, drops and `trimBefore`, each aligned to where the kicks enter (sometimes a bar after
   the energy rise). Pick a drop whose energetic section outlasts the edit, so the
   payoff and end card still land on kicks.
6. **Spec → timeline.** Write `<project>/spec.json` (format in `planning.md`; `assets/examples/spec.json`
   is a full example) and run `python3 <skill>/scripts/plan_timeline.py spec.json --out <project>/`.
   It writes `timing.json` and prints the timeline tables, enforcing readable, distinct wall
   durations and putting every structural cut on the beat.
7. **PLAN.md, before generating anything**, even when nobody is around to approve it: brief,
   brand, copy, the timeline tables, the sound plan, every assumption. If the user is around, show
   it first; for anything beyond a one-act sting, wait for approval.

### 2. Build (read `references/scenes.md`)
1. Write `<project>/video.json`, the per-video look and sound (`assets/examples/video.json` is a
   full example): size, palette, fonts (bundled Inter / Source Serif 4 by default), the SFX kit,
   music, and any custom end-card fragments. Measure each SFX file's peak first:
   `python3 <skill>/scripts/sfx_peaks.py <project>/assets/sfx/* --fps 24` → each kit entry's `peakOffset`.
2. A real logo → a `custom` end card: an HTML fragment that rebuilds it as vector shapes
   (`scenes.md` §6, worked example `assets/examples/custom-end-card-ah-mark.html`). A plain name →
   a `wordmark` end card.
3. Generate: `python3 <skill>/scripts/build_composition.py --timing timing.json --config video.json --project <project>`.
   It writes `index.html` and one sub-composition per scene in `compositions/`, and copies the
   fonts in. **Configure and rebuild; don't hand-edit the generated HTML.** A rebuild overwrites
   it, including edits made in Studio.

### 3. Validate (read `references/validation.md`)
Check renders, not code. Keep it light: `--workers 2`, `--quality draft` while validating.
- `npx hyperframes check`: **0 errors and 0 warnings.** `validation.md` maps each warning to its fix.
- `npx hyperframes snapshot --at <the planner's "snapshot --at" list> --no-end --output stills`, then
  `python3 <skill>/scripts/contact_sheet.py stills stills/sheet.jpg --timing timing.json` for a
  sheet labelled with what each tile should show. Look at it.
- Sound: build `music-only.html` (`--mute sfx`), render it and the mix, **delete
  `music-only.html`** (a second root makes `check` fail), then
  `python3 <skill>/scripts/check_audio.py renders/mix.mp4 renders/music.mp4 timing.json`
  (`none` for SFX-only).
- Fix, re-check, write the numbers into PLAN.md, open the Studio preview
  (`npx hyperframes preview --background`), and render the delivery file only on approval.
  Say what wasn't verified (by ear, phone width).

## Rules that came from real feedback

These are the defaults because a user asked for each one, and HyperFrames' own audits enforce
several. Explain the trade-off rather than silently breaking one:

- **Every wall word is readable**: ≥ 10 frames (0.42s) at 24fps for 1–2 words, more for phrases
  (3 words 1.05s), the floor HyperFrames' `line_unread` audit uses. The planner applies it per word.
  Flashes look fast but read as noise.
- **Vary durations, and no two equal** (`distinct: true`). Each segment covers the same drift
  distance in its own time, so different lengths also give different speeds. Default shape: two
  quick, three slowing, accelerating, last word held. Distinct and readable means
  ≥ n·min + n(n−1)/2 frames, so a longer list makes a longer wall. Tell the user when that grows
  the video.
- **The first frame isn't empty** (`firstWordAt: 0`): it's the thumbnail on social players.
- **The last line holds ≥ 2s**: a wordmark end card's `frames` ≥ 48, or with a shape-only logo the
  statement's `minFrames` ≥ 48.
- **The drop lands on the cut into the wall.** The typed line plays over the pre-drop break.
  Later structural cuts land on beats (the planner snaps them). Wall swaps run free.
- **SFX louder than the music**: every hit ≥ ~3 dB over the music around it, measured with
  `check_audio.py`. Duck the music under the statement and reveal, **never under the drop**.
- **True peak ≤ −1.3 dBTP.** A hot peak is usually one SFX on a music hit. `check_audio.py` names
  the frame and hit, so duck that one (`music.duckFrames`) before lowering the bed. The drop's own
  hit is the exception: change that SFX, never duck under it. With SFX
  leading, about −16 to −19 LUFS is fine; report it.
- **Verify the trim on a render.** Decoders differ (HyperFrames vs Remotion measured ~30ms apart
  on the same MP3), so nudge `music.trimBefore` by the measured offset.
- **Don't time-stretch music** more than ~3% to force a grid.
- **Sound follows structure.** Hits come from scene boundaries; re-run the planner and the
  generator instead of hand-placing audio.
- **Text only, no chrome**: no eyebrow labels, badges, numbering or separators. One saturated wall
  color, its darker twin for the body text, a white serif highlight.
- **Undo means fully undo**: remove the config, the generated files and any baked assets, rebuild,
  and re-verify the output matches the earlier state.

## Scaling up

- **More words:** 12 distinct readable words need ≥ 186 frames (7.8s). For long lists, split them
  into two acts with a new typed line rather than one marathon wall.
- **Longer videos:** chain acts in one spec (the grid continues). Give each act its own wall color
  (an act-level `palette`) and `shape` (`fast-slow-accel-hold`, `accelerate-hold`, `decelerate`).
  Set the length with `targetFrames`. Give each act's wall a high-energy music section, and keep
  the payoff and end card inside it.
- **Other formats:** set `width`/`height` in `video.json` (the generated `index.html` takes its
  size from there). Type scales with the frame and is enlarged ×1.35 on portrait (`textScale`
  overrides). Keep wall words short on 1080×1920.
- **Other sound modes:** `"music": null` for SFX-only (check with `check_audio.py mix.mp4 none
  timing.json`). For a voiceover, timing follows speech (`audio-sync.md` §7); place it as another
  `<audio>` with the HyperFrames voiceover-carve recipe in `/hyperframes-audio`.

## Bundled files

| Path | What it is |
|---|---|
| `scripts/build_composition.py` | timing.json + video.json → `index.html` + `compositions/scene-N-*.html` (one seek-safe timeline per scene, SFX/music `<audio>` with automation lanes, local fonts); `--mute sfx` for the music-only check |
| `scripts/plan_timeline.py` | spec.json → timing.json (+ timing.ts) + timeline tables (readable, distinct, beat-locked, multi-act, target length) |
| `scripts/analyze_music.py` | Tempo from the kick grid, loudness map, drop candidates, `trimBefore` |
| `scripts/sfx_peaks.py` | `peakOffset` for each SFX file |
| `scripts/check_audio.py` | Loudness, true peak, loudest frames and their hits, SFX-over-music margin per hit, beat sync per cut (skips cuts with no kick under them; `none` for SFX-only); exits 1 on failure |
| `scripts/contact_sheet.py` | Tiles `hyperframes snapshot` stills into one sheet labelled with frame and expected content |
| `assets/fonts/` | Inter 500/800 and Source Serif 4 400 (woff2, SIL OFL 1.1, licenses included) |
| `assets/examples/` | `spec.json`, `video.json` and a custom logo end card, validated end to end |
| `references/planning.md` | Brief, structures from sting to multi-act, the copy test, the spec format, PLAN.md template |
| `references/scenes.md` | The generated project, each scene's motion, custom end-card fragments, fonts, HyperFrames rules |
| `references/audio-sync.md` | Sound modes, drop and beat locking, the SFX kit, levels and ducking, loudness, voiceover |
| `references/validation.md` | `check` warnings → fixes, snapshots, the two-render audio check, delivery |

The scripts need Python 3 with numpy and scipy, plus ffmpeg on PATH; HyperFrames needs Node.js 22+.
