# PLAN.md Format

Section 3 of the main skill says to "write down" the type classification and the per-scene motion/sound decisions. This file defines where that actually goes: a `PLAN.md` written to the project's root directory, created in Step 1 and filled in through Step 2, then updated (never silently overwritten) through Step 3 and 4.

This exists because a plan that only lives in conversation turns can drift or get lost across a long implementation session — a file on disk is the thing both you and the user can actually check against, and it's what makes "don't improvise mid-implementation" (Section 3, Step 3) a checkable rule instead of an intention.

## Template

```markdown
# <Project name> — Motion Video Plan

## Classification
- Video type: <one category from references/video-types.md, e.g. "Product Demo / Launch Video">
- Target length: <Xs>
- Named reference: <a studio from motion-design-references.md, a specific video the user pointed at, or a precise technique description — never just "premium" or "minimal">

## Scenes

### Scene 1 — <short label>
- Subject / supporting text: ...
- Composition: <what's in frame, where the negative space is>
- Storyboard image: <path to the rendered reference image from Step 1>
- Duration: <Xs> — reason: <mood/pacing this matches>
- Motion: <the one technique, the animation principle from motion-rules.md, and the concrete numbers (damping ratio / zoom factor / shutter+sub-frames) it uses>
- Easing: entry <...> / exit <...>, anticipation/overshoot if any
- Sound: none | <description, peak frame, gain (0.04–0.3 range), ducking if voiceover present>
- Status: planned | implemented | validated

### Scene 2 — ...
(repeat per scene)

## Validation (filled in during Section 4, by the independent critic pass)
- Scores (1–10): hook __ · readability __ · motion __ · variety __ · composition __ · accuracy __ · sound sync __
- Issues found: ...
- Fixes applied and re-checked: ...
```

## Rules for using it

- Write `PLAN.md` before any Remotion code exists for the project. An empty or missing `PLAN.md` at implementation time means Step 1–2 were skipped — go back, don't improvise forward.
- Every scene in the implementation must correspond to a scene block in the plan. If implementation reveals a decision needs to change, edit the plan first, then the code — the file should always describe what the current implementation actually does, not what was originally intended and then silently abandoned.
- Update `Status` per scene as it moves through the workflow, and fill in the `Validation` section for real during Section 4 — don't leave placeholder scores.
- On a resumed session (the user comes back later, or a new conversation picks up the project), read `PLAN.md` first instead of re-deriving the plan from the existing code — it's the authoritative record of what was decided and why.
