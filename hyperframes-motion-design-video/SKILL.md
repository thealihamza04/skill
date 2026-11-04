---
name: hyperframes-motion-design-video
description: Plan, build and validate any motion-design video as a HyperFrames HTML composition, using a storyboard-first workflow, a written motion and sound plan per scene, real motion numbers (springs, log-space zooms, staggers, eases), deliberate transitions, measured audio and an independent critic pass. It works for any format: brand stings, title cards, kinetic type, data reveals, social promos, product demos, launch films, explainers and portfolio reels, in any aspect ratio. A bundled scaffold turns one storyboard.json into the project (scene sub-compositions, root-timeline transitions, music fades and ducks, SFX on their measured peaks), while you author each scene's look and motion. Use it whenever someone wants a video, motion graphic, promo, explainer, intro or launch film made with HyperFrames / HTML / GSAP, or a premium, non-generic video and no fixed format skill fits. For word-wall or stat-reel formats use their HyperFrames skills; for Remotion use premium-motion-video.
---

# Motion design video (HyperFrames)

One workflow for any video: **brief → classify → plan → scaffold → author scenes → validate →
deliver.** The format skills next to this one are finished recipes for one video each. This one
is the method behind them, so it works for a video nobody has made before.

```
brief ─► classify (video-types.md) ─► PLAN.md (scenes + motion + sound, with numbers)
      ─► storyboard.json ─► scaffold.py ─► author compositions/<scene>.html
      ─► check · snapshots · phone sheet · audio_check ─► independent critic ≥ 8 ─► render
```

Run the CLI at the version the scaffold pins in `package.json` (`npx -y hyperframes@<pin> …`).
Bare `npx hyperframes` below is shorthand. Read `/hyperframes-core` (the composition contract)
before writing scene HTML, and use `/hyperframes-animation` for runtime APIs and named rules.

## Route first: is there a finished format?

| The request is… | Use |
|---|---|
| Text-only promo: typed line → word wall → payoff → logo, beat-synced | `hyperframes-kinetic-typography-word-wall-video` |
| Numbers-first portfolio / milestone reel (counters, caret box, collage, URL) | `hyperframes-stat-reel-video` |
| A launch video made from the current repo's website, `/brag` | `brag` |
| The same video in React / Remotion | `premium-motion-video` (+ the `remotion-*` format skills) |
| **Anything else**, or a mix of scene types | **this skill** |

A format skill can still borrow from this one (the critic pass, the audio check), and this
skill can borrow a format's scene (a word wall inside a longer explainer). Reuse first, then
rebuild.

## Workflow

### 1. Brief (read `references/planning.md` §1)
Subject, the **one sentence** the video says, audience and platform, length, aspect ratio,
brand (palette, type, logo), source material (real UI, screenshots, footage, data), sound mode
(music + SFX, SFX only, voiceover, silent) and one **named reference** for the look. A named
reference is a studio, a real video or a precise technique. "Premium" or "clean" isn't one.
Infer what you can from the repo, profile or brand files, ask only what you can't, and write
down every assumption.

### 2. Classify (read `references/video-types.md`)
Match the deliverable to one type: brand sting, title card / kinetic type, data reveal, social
promo, product demo / launch, explainer, portfolio / brag reel, or a reference port. The type
sets length, scene count, pacing, transition family and how much sound the video needs.
Building the wrong type is the most expensive mistake, because nothing done later fixes it.

### 3. Plan, then write PLAN.md (read `references/planning.md`, `references/motion-language.md`, `references/transitions.md`)
Write the plan before any HTML exists, even when nobody is around to approve it:
- **Script/copy first** when there are words. Run the sentence test (read it aloud as one
  piece) and keep every claim and number traceable to a source.
- **Scenes**: one dominant idea each, three slots max (heading, optional support line,
  optional visual). Give each scene a duration *and the reason for it*.
- **Motion per scene**: the one technique, its animation principle and its numbers (ease or
  spring damping, distance, stagger, zoom factor), plus entry easing and what keeps it moving
  so it never sits still for more than ~1s.
- **Transition per cut**: which one and why, using one primary technique plus at most one
  accent for the whole piece.
- **Sound per scene**: none, or a cue with the frame its peak lands on and its gain.
- Storyboard frames: render one still per key scene if an image skill is available, or
  snapshot a static draft of the scene. A picture shows clutter that prose hides.

If the user is around, show PLAN.md and wait for approval on anything longer than a sting.

### 4. Scaffold (read `references/hyperframes-build.md`)
```bash
HYPERFRAMES_SKIP_SKILLS=1 npx -y hyperframes init <project> --non-interactive
rm <project>/index.html     # scaffold.py writes the root from storyboard.json
# copy media into <project>/assets/{music,sfx,vo,images,video}/ (paths outside the project don't render)
python3 <skill>/scripts/sfx_peaks.py <project>/assets/sfx/* --fps 30   # → each cue's "peak"
python3 <skill>/scripts/analyze_music.py <project>/assets/music/<track> --fps 30   # if music drives cuts
python3 <skill>/scripts/scaffold.py storyboard.json --project <project>
```
`storyboard.json` owns **time and sound**: size, fps, palette, fonts, scenes (id, duration,
`enter` transition), music (gain, trim, fades, ducking) and audio cues. `scaffold.py` writes
`index.html` and `storyboard.timing.json` on every run, plus a starter skeleton for each *new*
scene. `assets/examples/launch-spot/storyboard.json` is a complete example.

### 5. Author each scene (read `references/scene-recipes.md`)
Each `compositions/<id>.html` is yours. It is a `<template>` holding its own paused GSAP
timeline in scene-local seconds, and the prelude gives you `spring()`, `bez()`, `drive()`,
`countUp()`, `zoomLog()`, `split()` and `rng()`. Build exactly what PLAN.md says. If a decision
changes, update PLAN.md first. Retime in `storyboard.json` and re-run the scaffold. Never
hand-edit `index.html`.

### 6. Validate (read `references/validation.md`): check renders, not code
- `npx hyperframes check` → **0 errors, 0 warnings** (the reference maps findings to fixes).
- `npx hyperframes snapshot --at <scaffold's list> --no-end --output stills`, then
  `contact_sheet.py stills stills/sheet.jpg --timing storyboard.timing.json`, and the same with
  `--tile 390` for the phone-width check. Look at both.
- A burst of consecutive frames around every fast move, to catch stutter, smear and pops.
- Sound: render the mix and a music-only root (`--mute sfx --out music-only.html`, delete it
  after), then `audio_check.py renders/mix.mp4 --music renders/music.mp4 --timing storyboard.timing.json`.
- **Independent critic pass.** Score 1–10 for hook, readability, motion, variety, composition,
  accuracy and sound sync, without the builder's bias: use a subagent given only the stills,
  PLAN.md and the rubric. Anything below 8 gets fixed and re-checked. Write the scores into PLAN.md.

### 7. Deliver
Draft renders while iterating (`--quality draft --workers 2`). Render the delivery file once,
on approval, then `ffprobe` it to confirm duration and size. Report the scores, the loudness and
anything you didn't verify (playback by ear, a real phone).

## Anti-slop: treat these as failures unless the brief asked for them
- **Uniform motion**: every element with the same fade+rise and duration, every cut the same
  transition. Motion should vary with what the content weighs.
- **Stacked techniques** on one element (slide + scale + blur + color). Pick one.
- **Competing focal points**: two independent things moving for attention at once.
- **Dead air**: a shot fully still for more than ~1s. A hold still drifts, pushes or breathes.
- **Flashed text**: a line gone before it can be read (floor ~0.4s for 1–2 words, ~0.3s/word
  for sentences, ≥2s for the last line).
- **Linear or default easing** on anything physical, and cartoon bounce (overshoot > ~10%).
- **Decorative noise**: particles, gradient blobs, glows, lens flares, emoji icons and
  unmotivated 3D spins that aren't about anything in the scene.
- **Template chrome**: eyebrow/kicker labels, "01/02/03" badges, accent dots, pills, separator
  glyphs, fake browser bars, placeholder boxes or lorem ipsum.
- **Invented facts**: any number, logo, quote or claim on screen that doesn't trace to the user
  or a named source. A missing stat beats a fake one.
- **Reflexive letter-by-letter type** when the word isn't the payoff.
- **SFX on every cut** regardless of meaning, or a hit that peaks off its frame.
- **Too bare**: a "minimal" frame that reads as an empty web page. Keep depth (foreground,
  midground, background), scale contrast and one accent.

## Rules that hold for every video
- **One paused timeline per composition**, seek-safe: no clocks, no unseeded random, no
  network, no media `play()`. Every frame is a pure function of time (`hyperframes-core`).
- **Frame 0 is the thumbnail.** Content is on screen at t=0.
- **Truth over polish.** Real UI, real numbers and real logos (rebuilt as vectors where
  possible) are the user's. Never put someone else's brand or claims into a video, even when
  recreating a reference's structure.
- **Sound follows structure.** Cues hang off scene ids in `storyboard.json`, so a retime
  moves them. Peaks land where the motion resolves.
- **Undo means fully undo**: revert the storyboard or scene, re-run the scaffold, re-check.

## Bundled files

| Path | What it is |
|---|---|
| `scripts/scaffold.py` | storyboard.json → `index.html` (scene hosts, transitions, music automation, cues) + `storyboard.timing.json` + skeletons for new scenes |
| `scripts/sfx_peaks.py` | Where each SFX is loudest, in seconds, which is the cue's `peak` |
| `scripts/analyze_music.py` | Tempo from the kick grid, loudness map, drop candidates |
| `scripts/contact_sheet.py` | Labelled contact sheet of snapshot stills; `--tile 390` for phone width |
| `scripts/audio_check.py` | LUFS, true peak, loudest moments, every cue's margin over the music |
| `assets/fonts/` | Inter 500/800, Source Serif 4 400 (woff2, SIL OFL 1.1) |
| `assets/examples/launch-spot/` | A finished 6-scene example: storyboard.json, PLAN.md, every scene; passes `check` |
| `references/video-types.md` | The taxonomy: length, scenes, pacing, transitions, sound and the bar per type |
| `references/planning.md` | Brief, copy tests, storyboard.json format, PLAN.md template |
| `references/motion-language.md` | Timing, easing, springs, choreography, camera, type in motion, tone → numbers |
| `references/transitions.md` | Picking a transition, and building cuts, match cuts, pushes, wipes and whips in HyperFrames |
| `references/scene-recipes.md` | Ten scene archetypes with seek-safe GSAP code |
| `references/hyperframes-build.md` | Project layout, the contract in short, media, fonts, `check` findings → fixes |
| `references/audio.md` | Sound modes, music and beats, SFX placement, ducking, voiceover, loudness |
| `references/validation.md` | The check loop, snapshots, phone sheet, audio check, critic rubric, delivery |

Needs Node.js 22+ (HyperFrames), Python 3 with numpy (scipy for `analyze_music.py`, Pillow for
the contact sheet) and ffmpeg/ffprobe on PATH.
