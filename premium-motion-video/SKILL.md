---
name: premium-motion-video
description: Generate premium, minimal motion-design videos in Remotion (code-driven React video) through a required storyboard-first workflow with deliberate per-scene motion and sound design, concrete motion-physics and audio-mix defaults, and an independent critic pass before delivery. Use whenever the user asks to create, build, or render a video, motion graphic, animated explainer, product demo, launch video, promo, or anything described as a "Remotion video" or "motion design video" — even if they don't use those exact words. Critical for avoiding generic "AI slop" video output, enforcing real animation-principle discipline, minimal visual language, and a scored validation pass before delivery. Not for a single static image (use the image-generation skills) and not for in-app UI animation (use interface-animations).
---

# Premium Motion Video

## Quick start

1. **Classify** the request against `references/video-types.md`, then start `PLAN.md` (`references/project-plan-format.md`).
2. **Storyboard**: break it into scenes, render a reference image per scene, write them into `PLAN.md`.
3. **Decide motion + sound** per scene with concrete numbers from `references/motion-rules.md`, written into `PLAN.md` — before any code.
4. **Implement** in Remotion against that plan (delegate Remotion mechanics to `remotion-dev/skills`).
5. **Validate**: cheap frame checks (`scripts/export-validation-frames.sh`), a phone-width preview, and an independent 1–10 critic pass — fix anything below 8 before delivering.

Resuming an existing project? Read `PLAN.md` first instead of re-deriving the plan from the code.

## Why this skill exists

Past attempts at AI-generated motion design video have tended to produce "AI slop": technically-working Remotion output that still feels generic, busy, and cheap compared to real studio work. The problem usually isn't the code — it's that the video was designed and built in one pass, with motion choices invented element-by-element while writing the implementation, instead of being planned deliberately with real numbers, and then graded by the same agent that built it.

This skill exists to force the planning and the grading that separate premium motion design from slop: storyboard first, decide the motion and sound for every scene in writing with concrete defaults (not vague adjectives), implement against that plan instead of improvising, then have an independent pass actually score the result against a threshold before calling it done.

## 1. Recognize "AI Slop" and refuse to ship it

Treat any of the following as a failure, not a stylistic choice, unless the user explicitly asked for that specific effect:

- **Uniform motion everywhere.** Every element enters with the same fade+scale+blur combo, every transition is the same duration, every easing curve is the same. Real motion varies with content weight and mood.
- **Decorative noise with no content relationship.** Floating particles, generic gradient blobs, glow/bevel effects, rainbow gradients, glowing chrome, emoji used as icons, gratuitous 3D flips/spins on elements that have no reason to rotate, or background shapes that aren't about anything in the scene.
- **Competing elements.** More than one thing animating independently for attention at the same moment, instead of one clear focal motion per scene (unless a single continuous driver, like a slider or a tracked scroll, legitimately moves several things together).
- **Chrome that wasn't asked for.** Pills, chip-shaped badges, extra header/footer bars, watermarks, placeholder/lorem-ipsum text, or UI decoration that doesn't serve the scene's one idea.
- **Dead air.** Any shot held completely static for more than about 1 second. Real motion design keeps something advancing — even a slow push or a held frame should still be going somewhere.
- **Generic stock-library audio.** A whoosh or swoosh dropped on every single cut regardless of whether that cut needs one, or SFX that doesn't line up with any specific frame.
- **Letter-by-letter kinetic typography used reflexively** rather than because the text itself is the subject of that scene.
- **Linear easing**, or no easing at all, on anything meant to feel physical.
- **Invented numbers on screen.** Any stat, metric, or data point shown in the video that doesn't trace back to something the user supplied or a source you can name. A fabricated "47% faster" is worse than no stat at all.
- **Vague self-description instead of a reference.** Describing the target look only as "premium," "modern," or "clean" and never anchoring it to one specific named style or reference (see Section 2) is itself how the generic look creeps back in — those adjectives mean something different to every renderer.
- **Generic SaaS-template chrome.** The same clichés `interface-engineer` already rejects for web UI apply here just as much: an uppercase "eyebrow"/kicker label sitting above a headline for no reason (e.g. "CAPABILITIES" above "Engineering Craft"), numbered index badges on grid items ("01", "02", "03"...) used purely as decoration rather than a real, meaningful sequence, a lone accent dot or status dot with no function, or a middle-dot ("•") used as a reflexive separator between two unrelated pieces of text where a simple space or line break would do. These pass a lazy glance as "clean," which is exactly why they're a common failure mode — they're generic precisely because they're everywhere in template-generated UI.
- **Empty placeholder visual slots.** A reserved icon or image area left as a blank or gray box in the delivered output. If a scene needs a visual, render a real one (this repo's image-generation skills, or a real icon per `interface-engineer`) before delivering — an empty box is never an acceptable stand-in unless the user explicitly asked for an unfinished template.

If a render has any of these, it is not finished — go back to Section 4 (Validation) before delivering.

## 2. The core discipline: minimal and premium, not generic

Real premium motion work is restrained, not spectacular — but restrained is not the same as empty. A video frame is watched at scale and at a distance, so a composition that would read as clean on a web page can read as flat and lifeless on a screen; keep real depth (foreground/midground/background separation, one considered accent, a sense of scale) even while keeping the element count low. See `references/motion-design-references.md` for researched studios, numeric defaults, and sources to calibrate against — read it before making Section 3 Step 2 decisions, not after.

Working rules:

- **Name a specific reference, not an adjective.** Before designing a scene, name one concrete reference point for its look (a studio from `references/motion-design-references.md`, a specific real video the user pointed at, or a precise description of a technique) — not just "premium" or "minimal." The named reference is what you check the output against in Section 4.
- **One dominant idea per scene, with a hard slot limit.** Practically: one heading, optionally one supporting line, optionally one visual — nothing else by default. No eyebrow/kicker label above the heading, no numbered badges, no accent/status dots, no separator glyphs between pieces of text (use a space or a line break instead). This is the exact three-slot discipline `minimalist-brand-image-generator` already enforces for static images — apply it here too, since a video scene is under the same constant pressure to accumulate "just one more small element," and each one of those small elements is how the generic-template look gets back in. If a scene genuinely needs more than three slots to communicate, it's two scenes, not one busy scene.
- **One motion technique per scene.** Don't stack a slide-in, a scale, a blur, and a color shift on the same element. Pick the one movement that best expresses what's happening and commit to it.
- **Pick one transition technique per cut, deliberately** — hard cut, match cut on a shared element, whip pan, wipe, push, or cross-dissolve are different tools for different reasons, not interchangeable defaults. See `references/transitions.md` for when to use each and how to implement it in Remotion; a reflexive cross-dissolve on every cut is the same uniform-motion failure Section 1 already bans within a single scene.
- **No decorative chrome by default.** No pills, chips, badges, headers, or footers unless the content genuinely needs them. This mirrors the no-pills rule already used across this repo's UI skills — the same discipline, applied to video frames.
- **Motion follows real animation principles with real numbers**, not arbitrary tweening or a default curve left in place:
  - Springs, not generic eases, for anything that should feel physical: damping ratio around **0.72 or higher**, with only a small overshoot — never a cartoonish bounce.
  - Zoom and scale moves read more naturally interpolated in **log space** rather than linearly; an exit zoom is typically a roughly **×1.5** geometric step outward, not a linear crawl.
  - A fast move (a quick pan, a snap zoom, a whip transition) needs motion blur to avoid looking like a stutter: aim for the equivalent of a **180° shutter (0.5)** with **6–8 sub-frames** blended per fast move.
  - Cut on a match: when cutting between shots, cut at the point of peak velocity and keep direction and speed consistent across the cut, so the eye doesn't stumble.
- **No shot sits dead for more than ~1 second.** If nothing would be moving for longer than that, something in the plan is missing — either the shot is too long, or it needs its own small continuing motion.
- **Timing is intentional, not uniform.** Slower, held pacing reads as considered or documentary; quick, snappy pacing reads as energetic. Pick the pacing the content's mood calls for, scene by scene — don't default every scene to the same duration.
- **Reuse before rebuilding.** Before hand-building an effect or scene type from scratch, check whether this project (or a previous one) already has a composition that does something close, and adapt it instead of reinventing it — consistent reuse is itself part of what makes a body of work look designed rather than improvised each time.
- **Any number shown on screen must be traceable.** If the video displays a stat, metric, date, or claim, write down where it came from (something the user supplied, or a named source) before it goes in the composition. Never invent a plausible-sounding number to fill a scene.
- **A rendered UI element is an interface-engineering problem, not a motion one.** If a scene shows a card, terminal/CLI window, dashboard, button, or app screen built in code, its look-at-rest is governed by this repo's `interface-engineer` and `design-system` skills — read `references/ui-elements-in-video.md` before building one. Ad hoc card/terminal styling independent of those rules is the most common reason a code-rendered UI element looks cheap even when the surrounding motion is good.

## 3. Required workflow

Follow this order. Do not skip ahead to implementation because the plan feels obvious — the whole point of this skill is that the planning step is what prevents slop.

### Step 1: Storyboard first

Before writing any Remotion code:

- **Classify the request against `references/video-types.md` first.** Building the wrong type of video for the request — a long narrated explainer when a 6-second sting was wanted, or a static product shot when a demo was wanted — is itself a source of the gap between what was expected and what gets delivered, independent of execution quality. The matched type sets the expected duration, scene count, narration, and pacing bar for everything that follows. Open that category's own guide in `references/video-types/` and follow its specific how-to-build steps alongside this one.
- **Create `PLAN.md`** (format in `references/project-plan-format.md`) and fill in its Classification section now — video type, target length, and a named reference (see Section 2). This is the file every later step writes into; it's what makes the plan real instead of just a thing said in conversation.
- Break the video into scenes. For each scene, define: the one dominant subject, any supporting text, the composition (what's in frame, where the negative space is), and a rough duration. Add each as its own scene block in `PLAN.md`.
- Check for a close existing match first — a previous project's scene, or a registry/library of effects if one is available — before planning a from-scratch build for a scene type you (or this project) have already solved before.
- Actually render a reference image per scene using an available image-generation capability (this repo's `minimalist-brand-image-generator` or `vibrant-image-generator` skill, whichever visual direction fits) — don't just describe the frame in prose. A rendered image exposes composition and clutter problems that a text description hides. Record each image's path in its scene's `PLAN.md` block.
- If the user is available to review, show them the storyboard before moving on. If not, treat the storyboard as locked once it passes Section 2's rules, and move forward.

### Step 2: Decide motion and sound per scene — in writing, before implementation

For every scene in the storyboard, write the following into that scene's block in `PLAN.md` (not just into the conversation):

- The one motion idea, which animation principle from Section 2 it uses, and the concrete numbers (damping ratio, zoom factor, shutter/sub-frame count) it will use rather than a default.
- Entry and exit easing, including any anticipation or overshoot.
- How this scene transitions in from the previous one (hard cut, match cut, whip pan, wipe, push, or cross-dissolve — see `references/transitions.md`) and why that technique over the others.
- The duration, and the one-line reason for that specific duration (what mood or pacing it's matching) — confirm it's under the ~1 second dead-air ceiling unless the shot has its own continuing motion.
- Whether this scene needs sound at all. Most scenes don't need a dedicated SFX — only add one when it actually reinforces a specific motion beat.
- If a sound is used, write down concrete mix values rather than "quieter than the music":
  - Which exact frame its peak should land on — align the strongest part of the sound with the moment the motion resolves, not its start.
  - A relative gain in roughly the **0.04–0.3** range for a small SFX hit (scaled to the project's overall levels), never as loud as the music bed.
  - If there's a voiceover, duck the music roughly **9 dB** under it while the voiceover plays.
  - Normalize the final mix to around **−14 LUFS integrated**, with true peak at or below about **−1.3 dB**, so the delivered file doesn't clip or sit inconsistently loud compared to other media.
  - If music drives the piece, pick its tempo to match mood (roughly: 60–80 BPM reads calm/regal, 90–110 smooth, 115–123 upbeat, 125+ high-energy) rather than defaulting to whatever track was handy.
  - Find the actual beat/drop by measuring the track (e.g. a waveform/energy view, or `ffmpeg`'s `astats`/`silencedetect`), not by trusting an assumed or auto-detected beat grid — an auto grid is frequently off by a frame or two, which is enough to make a synced hit feel wrong even when the plan was correct.

Do this for every scene before writing a line of Remotion code, and keep `PLAN.md` as the single copy of these decisions. If a decision changes once you see it rendered, that's fine — but it should change as a deliberate update to the plan file, not as an improvisation made silently while coding.

### Step 3: Implement in Remotion

- This skill owns the art-direction and workflow discipline above; it does not reinvent Remotion's own API and rendering mechanics. Use the official `remotion-dev/skills` package for that — install it with `npx skills add remotion-dev/skills` if it isn't already available, and consult its composition/markup/rendering/audio sub-skills for how to actually build compositions, timing, assets, fonts, and exports.
- Build each scene as its own composition/sequence that matches the storyboard frame and the Step 2 decisions exactly, including the concrete numbers written down. If something needs to deviate from the plan, update `PLAN.md` first, then implement — don't let the implementation quietly drift from what the file says. Mark each scene's status `implemented` in `PLAN.md` as it's finished.
- Keep renders deterministic and seek-safe (per `remotion-dev/skills`' own rules): every frame must be a pure function of time, with no timers, accumulated state, or non-reproducible randomness, so the same frame looks identical whether it's rendered in order or seeked to directly. This is what makes the next step's frame-by-frame checks meaningful at all.

### Step 4: Validate before delivering — score it, and don't grade your own work

Do not claim the video is done from reading the code, and do not treat your own first impression of the full playback as sufficient — it's easy to go easy on something you just built.

- **Render cheap checks before the full render where possible.** Run `scripts/export-validation-frames.sh <comp-id> <out-dir> <frames>` (wraps the real Remotion CLI render command) to export a handful of still frames spread across the timeline, plus a short burst of consecutive frames around any fast-motion moment specifically, to check for stutter or smear instead of only watching it at full speed.
- **Check it at small size.** Preview at roughly phone width, not just full resolution — motion and text that read fine large can disappear or feel cluttered small, and that's how most of this will actually be watched.
- **Run an independent critic pass.** Review the finished render as if you had not built it — or better, have a separate pass/agent do this review without the builder's context, since the builder is biased toward liking their own choices. Score the result 1–10 on each of: hook/opening, readability, motion quality, variety (not repetitive), composition, factual accuracy of anything shown, and sound sync. Write the real scores into `PLAN.md`'s Validation section. If anything scores below 8, fix it and re-render before delivering, not after. The standard here is to be a harsh motion director, not a proud author.
- Re-check the finished render against every item in Section 1 specifically — slop patterns creep in during implementation even when the plan was clean.
- Confirm each scene's actual duration and pacing matches what Step 2 decided, and that the overall rhythm varies rather than feeling uniform, and that no shot exceeds the ~1 second dead-air ceiling.
- Confirm every sound lands on the frame it was designed for, at the gain/ducking/loudness values decided in Step 2.
- Confirm nothing is in frame that wasn't in the storyboard — no stray chrome, no leftover placeholder, no watermark, no invented stat.
- If anything fails, fix it and re-render before delivering. One render that wasn't watched, scored, and checked at small size is not a finished video.

## 4. Quality Checklist

- [ ] The request was classified against `references/video-types.md` before scenes were planned, that category's own guide in `references/video-types/` was followed, and the actual length/scene count/pacing matches its expected bar.
- [ ] `PLAN.md` exists, with every scene's decisions and the final validation scores actually filled in — not left as placeholders.
- [ ] A rendered storyboard image exists for every scene, made before any code was written, and any close existing match was reused rather than rebuilt from scratch.
- [ ] Every scene's motion and sound decisions were written down with concrete numbers (Section 3, Step 2) before implementation began — not vague adjectives.
- [ ] A specific named reference (not just "premium" or "minimal") was chosen for the project's look before designing scenes.
- [ ] No scene stacks more than one animation technique, and no shot sits dead for more than ~1 second.
- [ ] Each cut's transition technique was chosen deliberately (not a reflexive default) and isn't the only technique used across the whole piece unless the category calls for that.
- [ ] Easing and timing follow real animation principles with concrete values (spring damping, log-space zoom, shutter/sub-frames) and vary intentionally by scene.
- [ ] No pills, chips, badges, headers, footers, placeholder text, or other chrome that wasn't in the storyboard.
- [ ] Any SFX is synced to a specific frame, within the 0.04–0.3 gain range, with voiceover ducking (~9 dB) and final loudness (~−14 LUFS / −1.3 dB true peak) set deliberately.
- [ ] Any number or stat shown on screen traces back to a real source, never invented.
- [ ] Any rendered UI element (card, terminal, dashboard, app screen) followed `interface-engineer`/`design-system` rules — concentric radii, the standard shadow, no pills, real syntax highlighting, real design tokens — not ad hoc styling.
- [ ] No eyebrow/kicker labels, numbered index badges, decorative accent/status dots, or reflexive separator glyphs that weren't explicitly asked for; no empty placeholder visual slots anywhere in the output.
- [ ] `remotion-dev/skills` (or equivalent current Remotion guidance) was used for the implementation mechanics, not reinvented here; renders are deterministic and seek-safe.
- [ ] The final render was checked with cheap frame-level checks, previewed at small/phone size, and scored by an independent critic pass (1–10 across hook, readability, motion, variety, composition, accuracy, sound sync) — not just watched once by the builder.
- [ ] None of the Section 1 anti-slop patterns are present in the delivered output.

## References

- `references/video-types.md` — the video-type taxonomy and routing index. Read this first, in Section 3 Step 1, before breaking any request into scenes.
- `references/video-types/*.md` — a detailed how-to-build guide per category (brand sting, title card, data reveal, social promo, product demo, faceless explainer), each with its own structure, techniques, pitfalls, expected-output bar, and a category-specific transitions note. Read the matched category's file, not just the index row.
- `references/transitions.md` — the transition techniques (hard cut, match cut, whip pan, wipe, push, cross-dissolve), when to use each, and how to implement them in Remotion. Decide the transition for every cut in Section 3 Step 2, same as any other motion decision.
- `references/ui-elements-in-video.md` — how to build a card, terminal/CLI window, dashboard, or app screen that's rendered in code inside a scene, by deferring to this repo's `interface-engineer`/`design-system` skills rather than inventing ad hoc styling. Read this whenever a scene's content is a UI element, not a motion effect.
- `references/project-plan-format.md` — the `PLAN.md` template every project writes to and resumes from. Create it in Step 1; every later step writes into it.
- `references/motion-rules.md` — every numeric rule from Sections 1–4 as fast-lookup tables (easing/physics, timing, composition, audio/mix, the validation scoring rubric). Use it to look up a specific number without re-reading the surrounding prose.
- `references/motion-design-references.md` — researched real studios, animation-principle sources, and the sourcing behind the numeric defaults, with URLs. Read this for the *why* behind the numbers; `motion-rules.md` is the *what*.
- `scripts/export-validation-frames.sh` — exports specific frames of a composition as PNGs for the Section 4 cheap checks, wrapping the real, verified Remotion CLI render command. Run it directly; don't re-derive the CLI syntax.
