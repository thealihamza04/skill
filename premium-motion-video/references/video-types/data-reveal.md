# Motion Graphic / Data Reveal

**What it is:** An unnarrated piece where one number, chart, or comparison animates in — a stat hit, a chart building up, a before/after metric. Motion itself communicates the information, there's no voiceover walking through it.

**When to use this category:** The request centers on showing a specific number or dataset with impact — "animate this stat," "I want this chart to build in," "show the growth from X to Y." If the number is one beat inside a longer narrated piece, it's a scene within a product demo or explainer, not its own data-reveal video.

**Length:** 5–20s per stat/chart. One data reveal = one number or one comparison; a dashboard of several numbers is several short reveals in sequence, not one crowded scene.

## How to build it

1. **The number must be legible mid-animation, not just at rest.** A counter ticking up too fast to read, or a bar growing with no visible scale reference, fails even if the final held frame looks clean. Design the animation curve so the value is readable for a meaningful portion of its motion, not just the last frame.
2. **One accent color, used on the number or the one data series that matters.** Everything else (axis lines, labels, grid) stays in a quiet neutral so the eye goes to the number first.
3. **Source every value before animating it.** This category is the highest-risk one for the "invented numbers" anti-pattern in Section 1 of the main skill — write down exactly where each value came from before building the scene, never estimate a plausible-looking number to fill the frame.
4. **Give scale context, don't just animate a shape growing.** A bar or line that grows with no axis, no comparison point, or no unit label can look like generic motion-graphics filler rather than actual data. Keep at least one piece of context (a unit, a comparison value, a timeframe) visible.
5. **If the chart/number sits inside a card or dashboard-style container**, that container is an interface-engineering problem — see `../ui-elements-in-video.md` for the concentric-radii/shadow/no-pills rules rather than inventing a container style.
6. **End on a hold, not a cut.** The whole point is the number landing — give it the ~1s+ hold the main skill's dead-air rule allows for before cutting away, so it actually registers.

**Pitfalls specific to this category:**
- A counter or bar animating purely for spectacle with no real data behind the specific value shown.
- Multiple stats crammed into one scene competing for attention — split into sequential reveals instead.
- Decorative chart-junk (3D bevels, drop shadows, gratuitous color) standing in for an actually well-designed, legible chart.

**Transitions:** If several stats play in sequence, use the same transition between every pair — usually a match cut on the shared accent color or a consistent push — so the set reads as one piece rather than separate clips. See `../transitions.md`.

**Sound:** A single, restrained hit when the number lands on its hold (point 6 above), not on every incremental tick of a counter — the hold is the moment that deserves emphasis, not the counting itself. See `../motion-rules.md` for gain/peak-placement defaults.

**Expected output bar:** Someone could pause the video at any point past the first third of the animation and already read the approximate value; the final number is traceable to a real source.
