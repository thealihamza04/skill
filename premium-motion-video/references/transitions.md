# Transitions Between Scenes

A transition is a Section 2 decision like any other scene element — pick one technique per cut, name why, and write it into that scene's `PLAN.md` block (the "from" scene's Motion field, or its own line). "Fade to black then fade in" as a reflexive default is itself a mild anti-slop failure: it's not wrong, but using it on every single cut regardless of content is the same "uniform motion everywhere" failure Section 1 already bans for in-scene motion.

## The techniques

| Technique | What it is | Use it when |
|---|---|---|
| **Hard cut** | No transition at all — one frame ends, the next begins. | The two shots are different enough that bridging them would feel unnecessary; fast-paced categories (social promo) default to this. |
| **Match cut (shared element)** | An element present in both shots — a shape, a color field, a position — continues across the cut, so the eye has something to track through it. | The default for most premium work: a shape resolving into a logo, a color block becoming the next scene's background. This is the "transform instead of cut" rule from Section 2 — prefer it over an unrelated hard cut whenever a shared element is available. |
| **Whip pan / snap zoom** | The camera or frame moves fast enough to blur through the transition, arriving at the next shot mid-motion. | Energetic pacing, a sense of continuous space between two subjects. Needs the motion-blur defaults from `motion-rules.md` (180° shutter, 6–8 sub-frames) or it reads as a stutter instead of a deliberate whip. |
| **Wipe / reveal** | The next scene uncovers the previous one via a moving edge (a shape sliding across, a mask revealing). | A controlled, graphic way to move between unrelated content without a jarring cut — reads as more designed than a cross-dissolve when the wipe's shape/direction means something (e.g. echoes an element already in frame). |
| **Push / slide** | The outgoing and incoming scenes occupy the same frame briefly, one pushing the other off. | Sequential or comparative content (before/after, step 1 → step 2) where the spatial relationship between the two scenes itself carries meaning. |
| **Cross-dissolve (fade)** | The outgoing scene's opacity falls as the incoming scene's opacity rises, overlapping briefly. | Sparingly — a genuine mood shift (time passing, a tonal change) or when no other technique fits. This is the technique most likely to be used reflexively; if there's no specific reason for it over a match cut, use a match cut instead. |

## Choosing one

1. **Check for a shared element first.** Before picking anything else, ask whether the outgoing and incoming scene share a shape, color, or position that could carry across the cut. If yes, a match cut is almost always the premium choice over a generic fade.
2. **Match the transition to the category's pacing**, not just to taste — see the "Transitions" note in the matched file under `video-types/`. A social promo that cross-dissolves every cut will feel slow regardless of how good any individual scene is; a documentary-paced explainer that hard-cuts every beat will feel choppy regardless of how good the shots are.
3. **Don't mix more than two transition techniques across one video** unless the piece is long enough (8+ scenes) that variety itself is part of the design. A short piece using four different transition styles reads as indecisive, the same way Section 1 bans stacking multiple animation techniques inside one scene.
4. **Cut on a match for anything with motion through the cut.** Whether it's a hard cut or a whip pan, cut at the point of peak velocity in the outgoing shot and keep direction/speed consistent into the incoming shot (the `motion-rules.md` easing/physics row) — a cut on a dead moment, or one that reverses direction, is what makes an otherwise well-designed cut feel wrong.

## Implementing in Remotion

- A hard cut is just two adjacent `Sequence`s with no overlap.
- A match cut/cross-dissolve needs the two `Sequence`s to overlap by the transition's duration, with the shared element either genuinely the same component instance (ideal — true continuity) or two instances cross-faded/interpolated against each other.
- `remotion-dev/skills` (Section 3, Step 3 of the main skill) owns the actual composition/sequencing API for this — consult its transition-related guidance for the current recommended pattern rather than hand-rolling overlap logic here. This file owns *which* transition to choose and *why*; the implementation mechanics live there.
- Whatever technique is chosen, keep it deterministic and seek-safe per Section 3 Step 3 — the transition's progress must be a pure function of the current frame, not an accumulated or timer-driven state.
