---
name: premium-motion-video
description: Generate premium, minimal motion-design videos in Remotion (code-driven React video) through a required storyboard-first workflow with deliberate per-scene motion and sound design. Use whenever the user asks to create, build, or render a video, motion graphic, animated explainer, product demo, launch video, promo, or anything described as a "Remotion video" or "motion design video" — even if they don't use those exact words. Critical for avoiding generic "AI slop" video output, enforcing real animation-principle discipline, minimal visual language, and a validation pass before delivery. Not for a single static image (use the image-generation skills) and not for in-app UI animation (use interface-animations).
---

# Premium Motion Video

## Why this skill exists

Past attempts at AI-generated motion design video have tended to produce "AI slop": technically-working Remotion output that still feels generic, busy, and cheap compared to real studio work. The problem usually isn't the code — it's that the video was designed and built in one pass, with motion choices invented element-by-element while writing the implementation, instead of being planned deliberately first.

This skill exists to force the planning that separates premium motion design from slop: storyboard first, decide the motion and sound for every scene in writing before touching code, implement against that plan instead of improvising, then actually watch the result before calling it done.

## 1. Recognize "AI Slop" and refuse to ship it

Treat any of the following as a failure, not a stylistic choice, unless the user explicitly asked for that specific effect:

- **Uniform motion everywhere.** Every element enters with the same fade+scale+blur combo, every transition is the same duration, every easing curve is the same. Real motion varies with content weight and mood.
- **Decorative noise with no content relationship.** Floating particles, generic gradient blobs, glow/bevel effects, or background shapes that aren't about anything in the scene.
- **Competing elements.** More than one thing animating independently for attention at the same moment, instead of one clear focal motion per scene.
- **Chrome that wasn't asked for.** Pills, chip-shaped badges, extra header/footer bars, watermarks, or UI decoration that doesn't serve the scene's one idea.
- **Generic stock-library audio.** A whoosh or swoosh dropped on every single cut regardless of whether that cut needs one, or SFX that doesn't line up with any specific frame.
- **Letter-by-letter kinetic typography used reflexively** rather than because the text itself is the subject of that scene.
- **Linear easing**, or no easing at all, on anything meant to feel physical.

If a render has any of these, it is not finished — go back to Section 4 (Validation) before delivering.

## 2. The core discipline: minimal and premium, not generic

Real premium motion work is restrained, not spectacular. See `references/motion-design-references.md` for researched studios and principles to calibrate against — read it before making Section 3 Step 2 decisions, not after.

Working rules:

- **One dominant idea per scene.** One subject, optionally one line of supporting text. If a scene needs more than that to communicate, it's two scenes, not one busy scene.
- **One motion technique per scene.** Don't stack a slide-in, a scale, a blur, and a color shift on the same element. Pick the one movement that best expresses what's happening and commit to it.
- **No decorative chrome by default.** No pills, chips, badges, headers, or footers unless the content genuinely needs them. This mirrors the no-pills rule already used across this repo's UI skills — the same discipline, applied to video frames.
- **Motion follows real animation principles**, not arbitrary tweening: ease in/out, anticipation, overshoot, follow-through, hold, and settle. A beginning and end that happen because physics would produce them, not because a default curve was left in place.
- **Timing is intentional, not uniform.** Slower, held pacing reads as considered or documentary; quick, snappy pacing reads as energetic. Pick the pacing the content's mood calls for, scene by scene — don't default every scene to the same duration.

## 3. Required workflow

Follow this order. Do not skip ahead to implementation because the plan feels obvious — the whole point of this skill is that the planning step is what prevents slop.

### Step 1: Storyboard first

Before writing any Remotion code:

- Break the video into scenes. For each scene, define: the one dominant subject, any supporting text, the composition (what's in frame, where the negative space is), and a rough duration.
- Actually render a reference image per scene using an available image-generation capability (this repo's `minimalist-brand-image-generator` or `vibrant-image-generator` skill, whichever visual direction fits) — don't just describe the frame in prose. A rendered image exposes composition and clutter problems that a text description hides.
- If the user is available to review, show them the storyboard before moving on. If not, treat the storyboard as locked once it passes Section 2's rules, and move forward.

### Step 2: Decide motion and sound per scene — in writing, before implementation

For every scene in the storyboard, write down:

- The one motion idea, and which animation principle from Section 2 it uses.
- Entry and exit easing, including any anticipation or overshoot.
- The duration, and the one-line reason for that specific duration (what mood or pacing it's matching).
- Whether this scene needs sound at all. Most scenes don't need a dedicated SFX — only add one when it actually reinforces a specific motion beat.
- If a sound is used: which exact frame its peak should land on (align the strongest part of the sound with the moment the motion resolves, not its start), and its relative level — SFX sits quieter than music, and both sit quieter than any voiceover.

Do this for every scene before writing a line of Remotion code. If a decision changes once you see it rendered, that's fine — but it should change as a deliberate update to this plan, not as an improvisation made silently while coding.

### Step 3: Implement in Remotion

- This skill owns the art-direction and workflow discipline above; it does not reinvent Remotion's own API and rendering mechanics. Use the official `remotion-dev/skills` package for that — install it with `npx skills add remotion-dev/skills` if it isn't already available, and consult its composition/markup/rendering/audio sub-skills for how to actually build compositions, timing, assets, fonts, and exports.
- Build each scene as its own composition/sequence that matches the storyboard frame and the Step 2 decisions exactly. If something needs to deviate from the plan, update the plan first, then implement — don't let the implementation quietly drift from what was decided.
- Keep renders deterministic and seek-safe (per `remotion-dev/skills`' own rules) — no animation driven by non-reproducible randomness.

### Step 4: Validate before delivering

Do not claim the video is done from reading the code. Actually render it and watch it.

- Re-check the finished render against every item in Section 1. Slop patterns creep in during implementation even when the plan was clean — catch them here.
- Confirm each scene's actual duration and pacing matches what Step 2 decided, and that the overall rhythm varies rather than feeling uniform.
- Confirm every sound lands on the frame it was designed for, at the right relative level.
- Confirm nothing is in frame that wasn't in the storyboard — no stray chrome, no leftover placeholder, no watermark.
- If anything fails, fix it and re-render before delivering. One render that wasn't watched is not a finished video.

## 4. Quality Checklist

- [ ] A rendered storyboard image exists for every scene, made before any code was written.
- [ ] Every scene's motion and sound decisions were written down (Section 3, Step 2) before implementation began.
- [ ] No scene stacks more than one animation technique.
- [ ] Easing and timing follow real animation principles and vary intentionally by scene — not uniform linear fades.
- [ ] No pills, chips, badges, headers, footers, or other chrome that wasn't in the storyboard.
- [ ] Any SFX is synced to a specific frame and sits quieter than music/voiceover.
- [ ] `remotion-dev/skills` (or equivalent current Remotion guidance) was used for the implementation mechanics, not reinvented here.
- [ ] The final render was actually watched end to end, not just reviewed as code.
- [ ] None of the Section 1 anti-slop patterns are present in the delivered output.

## References

- `references/motion-design-references.md` — researched real studios, animation-principle sources, and sound-design guidance with URLs. Read this before Section 3 Step 2 on any real project; it's the calibration material, not boilerplate.
