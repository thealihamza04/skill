# Motion Rules Quick Reference

A fast-lookup version of every numeric rule the main skill applies while deciding Section 3, Step 2 for a scene. The main `SKILL.md` explains *why* each rule exists (read it first) — this file exists so a specific number can be looked up directly instead of re-reading the surrounding prose every time. Sourced from `motion-design-references.md`; nothing here is invented or re-derived independently.

## Easing and physics

| Situation | Default |
|---|---|
| Anything that should feel physical (not a mechanical UI snap) | Spring, damping ratio ≥ 0.72, small overshoot only — never a cartoon bounce |
| Zoom or scale move | Interpolate in log space, not linearly |
| Exit zoom | ~×1.5 geometric step outward |
| Fast pan, snap zoom, whip transition | Motion blur equivalent to 180° shutter (0.5), 6–8 blended sub-frames |
| Cutting between two shots | Cut at the point of peak velocity; match direction and speed across the cut |
| Linear easing, or no easing, on anything physical | Never — this is an anti-slop failure, not a style choice |

## Timing and pacing

| Situation | Default |
|---|---|
| Maximum time anything sits completely static | ~1 second ("dead air" past this is a failure) |
| Calm, considered, documentary mood | Slower, held pacing |
| Energetic, urgent mood | Quick, snappy pacing |
| Every scene defaulting to the same duration | Never — vary duration by content weight and mood, deliberately |
| Music tempo by mood | 60–80 BPM calm/regal · 90–110 smooth · 115–123 upbeat · 125+ high-energy |

## Composition

| Situation | Default |
|---|---|
| Elements per scene | One dominant subject, optionally one supporting line of text — no more |
| Animation techniques stacked on one element | One. Never a slide-in + scale + blur + color-shift combo |
| Decorative chrome (pills, chips, badges, headers, footers) | Off by default; only if the content genuinely needs it |
| Transition between related shapes | Prefer a match cut (transforming the shared element) over cutting to something unrelated |
| Which transition technique to use per cut | See `transitions.md` — hard cut, match cut, whip pan, wipe, push, or cross-dissolve are different tools; pick deliberately, don't default to one for every cut |
| "Minimal" composition that reads as flat/empty | Keep real depth (foreground/midground/background, one accent, a sense of scale) even at a low element count |

## Audio and mix

| Situation | Default |
|---|---|
| Does this scene need a dedicated SFX? | Usually no — only add one that reinforces a specific motion beat |
| SFX peak placement | Aligned to the frame the motion resolves, not when it starts |
| SFX relative gain | ~0.04–0.3 for a small hit, scaled to project levels |
| Music under voiceover | Duck ~9 dB while the voiceover plays |
| Final mix loudness | ~−14 LUFS integrated, true peak ≤ ~−1.3 dB |
| Generic stock whoosh on every cut | Never — only where a specific beat calls for one |

## Validation scoring rubric

Score the finished render 1–10 on each axis below in an independent critic pass (Section 4 of the main skill). Fix and re-render anything below 8:

| Axis | What it's checking |
|---|---|
| Hook / opening | Does the first 3–5 seconds state the problem, payoff, or focal subject before any setup? |
| Readability | Can the message be followed at normal speed, and at phone width? |
| Motion quality | Does motion follow the easing/physics defaults above, or does it feel arbitrary? |
| Variety | Is pacing/technique varied across scenes, or does everything feel the same? |
| Composition | One dominant idea per scene, correct element count, no stray chrome? |
| Accuracy | Does every number or claim on screen trace to a real source? |
| Sound sync | Does every SFX land on its intended frame at the intended level? |

## Video type defaults

See `video-types.md` for the full taxonomy (length, scene count, narration, dominant technique, and the expected-output bar per type) — classify the request against it before applying any rule above, since the right duration and pacing bar depend on which type of video this is.
