# Micro-Motion Inside UI Elements

`motion-rules.md` and Section 2 of the main skill cover **scene-level** motion: camera moves, zooms, cuts, the physics of a whole element entering or leaving a frame. This file covers a different scale entirely: the small, fast motion *inside* a UI element being shown in a scene — a button being pressed, a dropdown opening, a list revealing its items, a toggle switching, a spinner loading. Conflating the two is itself a source of bad output: a card's whole-scene entrance uses the spring-damping/log-zoom defaults from `motion-rules.md`, but once it's on screen, anything that moves *within* it (its own controls, its own list items) is a micro-interaction and follows this file instead.

## Defer to `interface-animations` for timing and easing

This repo already has a dedicated skill for exactly this: `interface-animations`. Read it, and use its real conventions rather than inventing new ones:

- **Press feedback:** 100–160ms, triggered on pointer-down, not pointer-up — a control should react the instant it's "pressed," never waiting for release.
- **Tooltip or small popover:** 125–200ms.
- **Dropdown or select:** 150–250ms.
- **Modal or drawer:** 200–500ms.
- **Use spring motion, not a CSS-style ease, for anything that needs to feel continuous or interruptible** — a dropdown opening and closing rapidly should track smoothly, not restart a fixed-duration tween.
- **Animate only the properties that support the state change** — opacity and transform, not everything at once.

A video is pre-rendered, not live, so there's no real pointer to respond to — but the same timing conventions still apply, because they're what makes a *simulated* interaction read as authentic rather than as an animation loosely imitating software. If the scene is showing a product faithfully (per `product-demo.md`), its micro-interactions need to look like the real product's, not like a generic motion-graphics approximation of one.

## Choreographing a simulated interaction

When a scene shows a cursor or finger interacting with a UI element (clicking a button, opening a menu, toggling a switch):

1. **Anticipation before the action** — a brief pause or a slight cursor settle before the click, not an instant teleport-and-click. This mirrors the anticipation principle in `motion-design-references.md`, applied at a much smaller, faster scale.
2. **The press itself**, per `interface-animations`: the control reacts immediately on press (scale down slightly, ~0.95–0.97, over the 100–160ms press-feedback window), not after a delay.
3. **The release/result** follows immediately after — a menu opening, a value changing, a toggle completing its slide — using the matching duration from the table above for whatever UI element just responded.
4. **Cursor movement between actions is eased, not linear** — it should decelerate into each target, the same ease-out logic as any other motion in this skill.

## Lists, grids, and staggered reveals

When several items in a list or grid appear together (card grid contents, a dropdown's options, a list of features), stagger their entrance rather than having them all animate in simultaneously — simultaneous entry on more than two or three items reads as a single clumsy block, not a designed reveal.

- Offset each item's start by roughly 30–80ms from the previous one — fast enough that the whole group still reads as one reveal, not a slow roll-call.
- Keep the per-item animation itself consistent with Section 2's one-motion-technique-per-scene rule — every item uses the *same* entrance motion, just offset in time; varying the technique per item is its own form of uniform-motion-everywhere's opposite failure (randomness instead of deliberate variation).
- A stagger is still motion that must resolve — the whole group should finish settling within roughly the scene's dead-air ceiling budget (`motion-rules.md`), not spend a full second just revealing a list before anything else happens.

## Loading, counters, and status

- **Spinners:** a continuously-rotating spinner is one of the few legitimate uses of linear motion (rotation at constant angular velocity reads as "still working," not as a failure of easing) — the no-linear-easing rule in Section 1 is about motion that starts and stops, not indefinite looping.
- **Skeleton/shimmer loading states:** a single soft sweep across the placeholder shape, not a pulsing glow — keep it quiet, it's meant to be ignored, not to compete for attention.
- **Counters:** ease-out into the final value (decelerating, not constant-speed), per `data-reveal.md`'s rule that the value must be legible mid-animation, not just at rest.
- **Success/checkmark confirmations:** a brief draw-on stroke (the check's path animating in, not just fading in as a static shape) reads as more considered than an instant pop; keep it under the press-feedback-scale timing window above — this is a confirmation, not a celebration.
- **Status pulses (a dot or badge that pulses to indicate "live" or "active"):** only ever use this for a real, current state — this is the one legitimate exception to Section 1's ban on decorative status dots, specifically because it's communicating something true and current, not sitting there as unexplained decoration.

## Checklist addition

Before delivering a scene with any UI-component-internal motion:

- [ ] Scene-level motion (`motion-rules.md`) and component-internal micro-motion (this file) weren't confused with each other — a card's entrance uses scene physics; what moves inside it uses `interface-animations`' timing.
- [ ] Any simulated click/interaction used anticipation → immediate press feedback → eased result, not an instant teleport.
- [ ] Any list/grid of more than two or three items staggered its reveal rather than entering all at once.
- [ ] A spinner (if any) is the only element using constant linear motion; everything else that starts and stops still eases.
- [ ] A status pulse, if present, reflects a real current state — not decoration.
