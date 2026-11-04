# Scene recipes

Ten scene archetypes that cover most videos. Every snippet goes inside a scene's `<script>`
after the scaffold prelude (`tl`, `$`, `spring`, `bez`, `r`, `drive`, `countUp`, `zoomLog`,
`split`, `rng`), uses scene-local seconds, and is seek-safe. The worked versions of 1, 3, 4, 5, 6,
8 and 9 are in `assets/examples/launch-spot/compositions/`, and they pass `check` with zero
findings. Prefix every id with the scene id (`#hook-title`) so ids stay unique on the
assembled page.

Before hand-building a named look (terminal, chart, map, CRT, grain, glitch, confetti, motion
blur), search the registry: `/hyperframes-registry`. Before a complex 4–5 phase scene, check
`/hyperframes-animation` → `blueprints-index.md`.

---

## 1. Title card: masked line rise
Display type rising out of its own line box reads more premium than fade+rise.
```html
<div class="mask" style="overflow:hidden;height:150px"><h1 id="end-title" style="line-height:150px">Motion design, <em>in HTML.</em></h1></div>
```
```js
tl.fromTo("#end-title", { y: 160 }, { y: 0, duration: 0.8, ease: "expo.out" }, 0.4);
zoomLog("#end-cam", 1, 1.035, 0, D, "none");   // the hold keeps moving
```
Several lines stagger by 0.08–0.12s. The key word gets the serif or the accent, not both plus a
weight change.

## 2. Word beats (kinetic type)
One word per beat, each its own timed clip, so the runtime owns visibility and seeking is exact.
```html
<div id="s-w1" class="word clip" data-start="0" data-duration="1.05" data-track-index="0"><h1 id="s-t1">Fast.</h1></div>
<div id="s-w2" class="word clip" data-start="1.05" data-duration="1.05" data-track-index="1"><h1 id="s-t2">Honest.</h1></div>
```
```js
tl.fromTo("#s-t1", { scale: 0.55 }, { scale: 1, duration: 0.75, ease: spring(0.72) }, 0.05);
tl.fromTo("#s-t2", { scale: 1.08 }, { scale: 1, duration: 0.3, ease: "expo.out" }, 1.05);  // punch on the cut
```
Use readable lengths (≥ 0.4s; ≥ 1s when it's the beat's only content), distinct durations,
and one overshoot in the whole run at most. A whole film of this is the word-wall format, so route to
that skill.

## 3. Typing (prompt, terminal, search bar)
Text recomputed from time in one driver; a seeded jitter makes it human but repeatable.
```js
const TXT = "a 15-second launch video for my app", rand = rng("type"), at = [];
let acc = 0.15; for (let i = 0; i < TXT.length; i++) { at.push(acc); acc += 0.034 + rand() * 0.026; }
drive(0, D, (t) => {
  let n = 0; while (n < at.length && at[n] <= t) n++;
  $("#s-text").textContent = TXT.slice(0, n);
  $("#s-caret").style.opacity = (n < at.length && t > 0.15) || Math.floor(t / 0.5) % 2 === 0 ? 1 : 0;
});
```
Mono type from a shipped file (bundled JetBrains Mono). Show only real commands and real
output.

## 4. Storyboard / grid assemble
```js
for (let i = 0; i < 5; i++)
  tl.fromTo("#plan-card-" + i, { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.75, ease: spring(0.8) }, 0.12 + i * 0.08);
```
Cap the group at ~0.5s total. Small labels inside cards are texture, so give the cards
`data-layout-ignore`, or `check` flags text under the 28px phone floor.

## 5. Camera push → match cut
One driver owns the camera scale for the whole scene. Accelerate into the cut so it lands at peak velocity:
```js
zoomLog("#plan-cam", [1, 1.035, 6.4], [0, 2.15, D], ["none", "power2.in"]);
```
The incoming scene starts where the last outgoing frame was (snapshot it and measure; here the
card filled 0.885 of the frame) and keeps moving in the **same direction**:
```js
tl.fromTo("#data-cam", { scale: 0.885 }, { scale: 1, duration: D, ease: "expo.out" }, 0);
tl.fromTo("#data-cam", { borderRadius: 91 }, { borderRadius: 0, duration: 0.5, ease: "power2.out" }, 0);
```
Remove anything in the outgoing frame that isn't in the incoming one (here a label) before the cut.

## 6. Data reveal: counter
```js
countUp("#data-num", 0, 8, 0.2, 1.15, "power2.out");                 // integers
countUp("#rev", 0, 1.8, 0.2, 1.4, "expo.out", (v) => "$" + v.toFixed(1) + "M");
```
Use `font-variant-numeric: tabular-nums` so digits don't jitter. Keep the unit and timeframe on
screen, and hold ≥ 1s after landing. Only use sourced values.

## 7. Bar / line chart build
```js
// bars: scaleY from 0 with transform-origin bottom (set in CSS), staggered
["#c-b0", "#c-b1", "#c-b2"].forEach((s, i) =>
  tl.fromTo(s, { scaleY: 0 }, { scaleY: 1, duration: 0.7, ease: "power3.out" }, 0.2 + i * 0.1));
// line: SVG path with pathLength="1", stroke-dasharray "1 1.2", dashoffset 1.1 → 0
tl.fromTo("#c-line", { attr: { "stroke-dashoffset": 1.1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 1.1, ease: "power2.inOut" }, 0.3);
```
A gap longer than the path (1.2) stops a round cap from painting a dot (`svg_round_cap_hidden_dash`).
Use one accent series with neutral axes, and add a value label at the end of the series.

## 8. UI card / terminal with an interaction
Build the UI to the product's real system (radii, shadow, type, copy), with no fake traffic-light
chrome. Then do micro-interactions at interface timing:
```js
tl.fromTo("#ui-card", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: spring(0.82) }, 0);
tl.fromTo("#ui-btn", { scale: 1 }, { scale: 0.96, duration: 0.12, ease: "power2.out", immediateRender: false }, 1.4);
tl.fromTo("#ui-btn", { scale: 0.96 }, { scale: 1, duration: 0.2, ease: "power2.out", immediateRender: false }, 1.52);
```
A result that appears at a moment should be its own timed clip
(`class="clip" data-start="0.95" data-duration="…"`). Animate an inner span, never the clip's
visibility. Give the container a fixed height so the new line can't shift the layout.

## 9. Highlight on a screenshot / product shot
Push toward the element that matters and dim the rest:
```js
zoomLog("#shot-cam", 1, 1.6, 0.3, 1.2, "power2.inOut");                 // the cam is the shot's wrapper
tl.fromTo("#shot-dim", { opacity: 0 }, { opacity: 0.55, duration: 0.5, ease: "power2.out" }, 0.6);
// #shot-dim: a full-frame dark layer with a clip-path hole around the element
```
Images go in `assets/images/` as `background-image` divs or `<img>` (reusing one image as
several `<img>` trips `duplicate_media_discovery_risk`; use backgrounds for repeats).

## 10. Logo resolve (sting / end card)
Rebuild the mark as SVG parts so they can move; one gesture, then a ≥ 0.5–1s hold.
```js
// parts fly in from offsets on a spring and settle into the lockup
[["#m-a", -60, 0], ["#m-b", 60, 0], ["#m-c", 0, 50]].forEach(([s, dx, dy], i) =>
  tl.fromTo(s, { x: dx, y: dy, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.8, ease: spring(0.8) }, 0.1 + i * 0.06));
tl.fromTo("#m-word", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "expo.out" }, 0.7);
```
Compare the final frame with the source logo side by side. Never ship someone else's mark.

---

## Patterns every recipe relies on
- **Initial states live in `fromTo`** (or CSS on things nothing tweens). No `tl.set` at 0 to
  hide later content (`gsap_timeline_set_initial_hide`); make it a timed clip instead.
- **Holds keep moving**: a 1→1.03–1.06 push on a camera wrapper, or a 10–20px drift.
- **Exit = the next transition.** Don't fade content out before a cut (only the final scene may
  fade out).
- **One driver per element+property.** Several phases → `r()` or a multi-phase `zoomLog()` in
  one driver.
- **Ids prefixed by scene id**; style the scene root by id, never by class
  (`subcomposition_root_styled_by_class`).
