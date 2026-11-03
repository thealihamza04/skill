---
name: remotion-stat-reel-video
description: Plan, build and validate "stat reel" brag videos in Remotion + GSAP — a ~20–25s typographic portfolio reel where numbers do the talking. A project-shot collage opens with a title and stat pill, spoken-rhythm words swap on light then dark backgrounds with drawn squiggles, a counter is underlined by a moving text caret that turns into a highlight box, a giant ghost number sits behind a letter-scattered word, a badge counter climbs in steps, an arrow pulls the viewer to "my latest case studies", a search bar types the portfolio URL, the work bursts into a collage, and a logo end card fades to black. A bundled config-driven engine reproduces a measured 60fps reference frame-for-frame (useGsapTimeline for letters, collage and logo assembly). Use it whenever someone wants a brag/portfolio/agency stats reel, a "we reached X views / Y followers / Z clients" promo, a personal-brand milestone video, a video "like ReachReel" or "like this Behance/orbix studio reel", or to port a similar counter-and-collage reference video into Remotion — even if they never say "stat reel". For the same format as HTML, use hyperframes-stat-reel-video.
---

# Stat reel (Remotion + GSAP)

```
collage + title → Hi / I'm / Building → I / have / built → 22+ public repositories (caret → box)
→ giant 4 · "Shipped" → to → Production → [7+] projects built → Taking [4+] products from…
→ Check out ⟶ My latest / Case studies / from here → 🔍 typed URL → collage burst → logo → black
```

`references/format.md` is the spec: every beat, its reference timing, sizes on the 720×540
stage, palette, copy rules and sound plan. Read it before planning. The bundled engine
implements it exactly. **Configure the engine, don't fork its motion.**

## Workflow

### 1. Plan (nothing is built before this)
1. **Facts first.** Collect the true numbers the reel will show (GitHub repos, shipped apps,
   projects, followers, clients, views), each with its source: the repo, the user's profile, the
   README, or what the user tells you. **Never invent a number to fill a beat.** If a beat has
   no true number, swap in a different true one or drop the beat. Ask only for what you can't
   find.
2. **Copy table**, one row per beat (format.md §Copy rules). Read it aloud as speech: words
   beats → counter label → ghost phrase → badge sentence → arrow phrases. Words ≤ 10 chars,
   arrow phrases ≤ 2 words, the intro stat agrees with the counters.
3. **Media.** 7+ landscape project screenshots/mockups into `public/` (the outro hero slot gets
   the best one). Logo: a real logo → rebuild it as SVG shapes in a `Mark` component (see
   `example.config.tsx`'s `AhMark`); otherwise the default monogram tile. Music bed + SFX kit
   (format.md §Sound).
4. **Write `PLAN.md`** next to the composition: facts with sources, the copy table, beat list
   with durations (`thanks` on or off), palette, media, sound. If the user is around, show
   it before building.

### 2. Build
1. Copy `assets/engine/StatReel.tsx` and `assets/engine/example.config.tsx` into
   `src/<Comp>/`. Rename the example's exports and edit only the config: `colors`, `images`,
   `beats` (order, subset, copy), `Mark`, `music`, `sfx`.
2. Register it in `src/Root.tsx`: `durationInFrames={statReelDuration(config)}`, `fps={60}`,
   width/height a multiple of 720×540 (1440×1080 default; the stage scales to the width),
   `defaultProps={{ mute: "none" }}`.
3. Needs `remotion`, `@remotion/media`, `@remotion/gsap` (+ `gsap`) and
   `@remotion/google-fonts`. Install any that are missing at the project's Remotion version.
   Then run `npx tsc --noEmit`.

### 3. Validate (check renders, not code)
```bash
python3 <skill>/scripts/stills_sheet.py <Comp> --out <scratch>/stills
```
That renders the middle of every beat at ½ scale into one sheet. Look at it: no clipped
labels (badge labels at their largest), numbers match the copy table, the caret/box lands on
the number, the arrow tip clears the phrase, the URL fits the pill, the wordmark is centered
with the mark. When porting or re-creating a reference video, add `--reference ref.mp4` for
side-by-side pairs and a per-frame difference percentage (`--shift-after` if beats were cut).
Then render the MP4 (`npx remotion render <Comp> out/<Comp>.mp4`) and say what wasn't checked
(by ear, phone size).

## Engine notes

- **Beats** (`Beat` union in `StatReel.tsx`): `collageTitle`, `words` (light|dark, custom
  `times`/`duration` allowed), `cursorCounter`, `ghostCounter`, `badgeCounter` (8 `steps`:
  climb/hold ×3 then drop), `badgeSentence`, `arrowWords`, `searchCollage`, `thanks`,
  `endCard`. Any order or subset; the total length is computed.
- Each beat runs on its **reference clock**, so motion keyframes stay as measured. The
  `arrowWords` beat overlaps 0.3s into the next one; its exit plays over `searchCollage`'s
  background crossfade, so keep those two adjacent.
- **GSAP where it earns it.** `useGsapTimeline` (paused, seeked from the Sequence's frame; never
  `.play()`) handles the many-element choreography: seeded random letter reveals, the
  outro collage's expo-out pop from the center plus a slow zoom, and the end-card mark. Single
  values (counters, caret, colors) stay as `interpolate`, which is simpler and seek-safe.
- **SFX are derived from structure** (`SFX_POINTS`): the cut to dark, box snap, ghost word,
  arrow pull, transition to dark, collage pop, logo. Set the kit in config; never hand-place
  hits. `mute: "sfx" | "music"` renders stems for level checks.
- **Rebrand by palette, not layout**: one pale background, a deep ink that doubles as the dark
  background, cream for text on dark, a ghost just darker than the background, one accent, a
  brand color for the wordmark dot.

## Porting a new reference video into this format

When the user brings a different reel to recreate, see `references/porting.md`. In short:
timestamped contact sheets (10fps) → a beat table with times → full-resolution frames for layout
and color samples → font size from **text width ratios** against your first render → a
side-by-side stills check with `--reference`. Keep the reference's own branding, logo and
soundtrack out of the result. Use the user's brand and true facts.

## Bundled files

| Path | What it is |
|---|---|
| `assets/engine/StatReel.tsx` | The engine: 10 beat types, stage scaling, GSAP choreography, structural SFX, music fades, `mute` stems |
| `assets/engine/example.config.tsx` | A complete, verified example (Ali Hamza: 22+ repos, 4 shipped, 7 projects) with a custom GSAP-assembled SVG logo mark |
| `scripts/stills_sheet.py` | Stills at beat midpoints → one labelled sheet; `--reference` for side-by-side pairs and a difference % |
| `references/format.md` | The format spec: beats, timings, sizes, palette, copy rules, sound, validation, aspect ratios |
| `references/porting.md` | How to measure and port another reference video |
