# HyperFrames notes for the stat reel

## Project layout the generator writes

```
<project>/
  index.html                       root "main": one host <div class="clip"> per beat + every <audio>
  compositions/beat-N-<name>.html  one <template> sub-composition per beat, own paused timeline
  assets/fonts/  assets/images/  assets/audio/
```

- Each beat's root is styled by its id (`#beat-3-cursorCounter { … }`), never a class
  (`subcomposition_root_styled_by_class`).
- Inside a beat, a `.stage` div (720×540) is scaled by `scale` with a CSS transform. GSAP never
  tweens `.stage`, so there's no `gsap_css_transform_conflict`.
- Times inside a beat are beat-local (the generator calls each beat with `L = 0`), so nested clip
  `data-start`s are local, which `npx hyperframes timeline` confirms ("local 0.4–0.8s").
- Each beat's script is wrapped in an IIFE: every beat declares its own `tl` and helpers.
- `index.html` registers an empty `main` timeline; the runtime nests the beat timelines.
- Old `compositions/beat-*.html` are deleted on every build, because switching a beat off renames
  the later files.

## How it stays seek-safe

HyperFrames seeks to arbitrary times in parallel workers, so every frame has to be a pure function
of time.

| Need | Technique |
|---|---|
| Something appears at a moment (word swaps, ghost words, caret, box, phrases, pill, collage shots) | Make it its own timed clip (`data-start`/`data-duration`, unique `id`). The runtime owns visibility, so a `fromTo` starting at opacity 0.55 can't leak before its slot. |
| Counters, caret position, blink, typing, arrow geometry, squiggle sway, badge size steps | `drive(start, dur, fn)`: a proxy `fromTo` with `immediateRender:false` whose `onUpdate` calls `fn(localSeconds)`, and `fn` recomputes the DOM from scratch (textContent, `style.left = calc(…)`, SVG attributes). No state carried between frames. |
| "Random" letter order | `rng(seed)` (a hashed mulberry32), seeded per beat, so every render gets the same order. |
| Reference easings | `bez()` (cubic-bezier) for the reference's `(0.16,1,0.3,1)` / `(0.65,0,0.35,1)` / `(0.5,0,0.75,0)`, passed as GSAP ease functions; `r()` is a clamped piecewise interpolate with per-segment easing, like Remotion's. |
| Shots | `background-image` divs, not `<img>`. Reused images otherwise trip `duplicate_media_discovery_risk`, and nothing here needs media decoding. |
| Squiggle draw-on | `stroke-dasharray: 1 1.2; stroke-dashoffset: 1.1 → 0` with `pathLength=1`, a gap longer than the path so the round cap can't paint a dot (`svg_round_cap_hidden_dash`). |

Seeking never relies on `tl.set` at position 0 (`gsap_timeline_set_initial_hide`): initial states
live in CSS/attributes or in a `fromTo` at the beat start.

## `check` findings you may hit and the fix

| Finding | Cause here | Fix |
|---|---|---|
| `line_unread` (craft) | a swap word or sentence held under the floor: 0.4s for 1–2 words, 0.75·(0.5+0.3·words)s for longer ones; text under 0.5 opacity doesn't count as read | Words already enter at 0.55 opacity. For a longer `badgeSentence`, raise `extraHold`. For longer swap words, shorten the copy rather than the rhythm. |
| `text_box_overflow` on `#bc-l` | a long `badgeCounter.label` at its 42px peak | Shorten the label (≤ 16 chars), or raise the 400px max-width in `badgeCounter()` |
| contrast on `#gc-n` | the ghost number is meant to be faint | Already `data-layout-ignore` (set dressing). Don't put that attribute on readable text. |
| `container_overflow` / `canvas_overflow` | shots and squiggles bleed off the frame; "Check out" rides off the left edge | Already `data-layout-allow-overflow` on exactly those elements. Keep it narrow. |
| `studio_missing_editable_id` | a new timed element without an id | `clip()` auto-assigns `c<N>`; pass `id_=` for anything JS touches. |
| `font_family_without_font_face` | a font swapped in without shipping it | Put the woff2 in `assets/fonts/`, add `@font-face` in `css()`, and copy it in `build()`. |

A lint **error** disables the layout and contrast audits (they report 0 samples), so clear errors
first before trusting a clean pass.

## Extending a beat

1. Change the beat method in `build_reel.py`. Keep times beat-local and add anything new that
   appears at a moment as a `clip()`.
2. If you change a beat's length, change it in `BEATS`; everything after it moves.
3. Rebuild, `check` (aim for zero findings), snapshot the beat's start, middle and end, and
   compare with the Remotion twin (`src/ReachReel/`) if the change should exist in both.

## Rendering

- `snapshot` is fast for stills. `render --quality draft --fps 30 --workers 2` renders the full
  example in about 40s on a laptop with software GL.
- On Linux without `chrome-headless-shell` the renderer falls back to screenshot capture (slower but
  correct). That's normal and not a project bug.
