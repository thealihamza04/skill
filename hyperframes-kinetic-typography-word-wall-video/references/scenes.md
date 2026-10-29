# Scenes, motion and the generated HyperFrames project

`scripts/build_composition.py` writes the whole composition from `timing.json` and `video.json`.
This file explains what it writes, why, and how to extend it. Configure it instead of hand-editing
the generated HTML; a rebuild overwrites hand edits.

## Contents
1. Generated project structure, 2. typed, 3. wall, 4. statement, 5. wordmark,
6. custom end cards (real logos), 7. palette, type and fonts, 8. HyperFrames rules the generator obeys

---

## 1. Generated project structure
```
<project>/
  index.html                     root "main": one host per scene + every <audio>, global time
  compositions/scene-N-<kind>.html one sub-composition per scene: <template> with styles, markup
                                 and its OWN paused GSAP timeline in scene-local time
  assets/fonts/*.woff2           bundled Inter / Source Serif 4 (copied in) or your own
  assets/music/, assets/sfx/     the media the config references
  timing.json, timing.ts         from plan_timeline.py (timing.ts is unused here; harmless)
  spec.json, video.json          your inputs; rebuild after editing either
```
- One sub-composition per scene is what HyperFrames expects: `lint` flags a root that holds nested
  scene markup (`nested_structure_needs_subcomposition`), big files and dense tracks.
- Host id = sub-composition `data-composition-id` = `window.__timelines` key (`scene-N-<kind>`).
  A mismatch silently renders frozen frames.
- **All motion is per-frame `tl.set()` calls** written from the same tables as the Remotion
  version of this skill, so the motion matches it frame for frame. Sets are discrete and
  reversible, so any seek lands on the exact frame (no clocks, no random, no tweens between).
- Background words come from a seeded PRNG at build time, so every build is identical.

## 2. `typed`: the setup line
- Words hard-cut on (`display` set at each `wordOn`); the line stays centered as it grows.
- A −2px dip on the frame before each new word; the last 7 frames run left (−0.5 … −19px) into the
  cut. `firstWordAt` 0 puts the first word on frame 0, the thumbnail.

## 3. `wall`: the word wall
- Every segment is its own timed clip (a hard cut) on its own Studio track. The rows sit in a
  `#…-drift` wrapper that moves left about 15px on a fast–slow–fast curve resampled to the
  segment's length, so different lengths also give different speeds.
- Background rows and the text beside the highlight carry `data-layout-ignore`: they're texture,
  so HyperFrames' contrast and readability audits skip them. The **highlight word stays audited**.
- ≥ 10 frames per word reads (HyperFrames' `line_unread` floor is 0.4s); distinct lengths avoid a
  mechanical rhythm.

## 4. `statement`: the payoff
- `lead` + serif `accent` + `tail`. Lands loose and right, then tightens to center over about 19
  frames (gap, tracking and offset shrink per frame), then holds.
- As the film's last text line it needs ≥ 2s (48 frames at 24fps), or `check` warns.

## 5. `wordmark`: the two-group reveal
- SVG: a bar over the mark narrows while `left` and `right` slide out from under its edges, each
  clipped by a polygon at the bar's edge (p = 1 − 0.765^f, settled by ~15 frames).
- `slant` (degrees) makes it a slash; `finalBar` (px @736) keeps a thin bar; `gap` (px @736, default
  14) sets spacing and widens itself to clear a slanted or kept bar, so a slash never touches a letter.
- The whole mark is centered and auto-fits to ~84% of the frame width (letter widths are estimated
  at 0.68em, so a very wide or narrow face may sit a little off-center; check the final frame).

## 6. `custom`: bespoke end cards (real logos)
Rebuild a real logo as vector shapes rather than placing a PNG, so it's crisp and its parts can move.
A custom scene is an **HTML fragment** file in the project, named in `video.json → custom`:

```html
<svg id="{{ID}}-mark" width="100%" height="100%" style="position:absolute;inset:0;"> … </svg>
<script data-hf-scene>
  // runs once at load as function (tl, T0, FPS, W, H, ID); add tl.set(...) at T0 + f / FPS
  for (let f = 0; f <= 15; f++) tl.set("#" + ID + "-bar", { attr: { width: 3 * Math.pow(0.765, f) } }, T0 + f / FPS);
</script>
```
- `{{ID}}` becomes the scene id, keeping element ids unique across the assembled page.
- Keep it deterministic: frame-indexed `tl.set` loops; no clocks, `Math.random`, media calls or
  network. Don't tween `visibility`/`display` on the scene clip itself.
- Comments are stripped before parsing, so a comment may mention `<script data-hf-scene>`.
- `assets/examples/custom-end-card-ah-mark.html` is a complete worked example: a pixel-grid "AH"
  monogram whose bar narrows into the letter gap, then a lavender fold snaps on at the next beat
  (spec `extraHits: [15]`, sounded by `extraHitSound`).
- Compare the final frame side by side with the source logo before calling it done.

## 7. Palette, type and fonts
- Palette tokens: `paper`, `ink`, `wall`, `wallInk` (the wall's hue, much darker, so the body text
  recedes), `highlight`, `accent`, `endBg`, `endInk`, `bar`. Any scene can override tokens; a
  multi-act spec's act-level `palette` changes the wall color per act.
- HyperFrames requires local fonts (`@font-face` to a shipped file, or `lint` errors). The bundled
  Inter (500, 800) and Source Serif 4 (400) are SIL OFL 1.1 (licenses in `assets/fonts/`) and are
  copied into the project automatically. To use a brand face, put its `.woff2` in
  `<project>/assets/fonts/` and set `fonts.sans` / `serif` / `display` in `video.json` to
  `{"family": "…", "files": {"500": "assets/fonts/….woff2"}}` (display also takes `weight`,
  `capRatio`).
- `textScale` multiplies type (default 1.35 on portrait frames, else 1).

## 8. HyperFrames rules the generator already obeys
So you don't break them in a custom fragment or a hand fix:
- One paused GSAP timeline per composition, registered last.
- Every `<audio>` has an `id`; no `crossorigin`; no media `play()`/`pause()` calls.
- No CSS `transform` on anything GSAP moves (the generator only animates `x` and SVG attrs).
- Styles and scripts live **inside** each sub-composition's `<template>`; the root is styled by id.
- Every SFX gets a real `data-duration` and the first free track, so audio tracks never overlap.
- CSS font families inside `style="…"` use single quotes. A double-quoted family ends the attribute
  early and silently drops every style after it (a bug this generator once had).
