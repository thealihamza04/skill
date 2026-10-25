---
name: interface-animations
description: Design, implement, and review purposeful interface animation for web products. Use when adding UI motion, transitions, gesture interactions, animated feedback, or improving animation timing, easing, accessibility, and performance.
---

# Interface Animations

## Purpose

Use motion to clarify state changes, preserve spatial context, and make direct manipulation feel responsive. Keep the interface still when motion adds no usable information.

## Decide Whether to Animate

- Consider how often an interaction occurs. Frequent actions need immediate feedback and little or no added motion; occasional transitions can use restrained motion; rare or first-run moments may support more expressive pacing when it serves the product.
- Keep essential feedback immediate even when decorative motion is reduced.
- Animate only properties that support the intended state change. Prefer opacity and transforms for simple transitions.
- Avoid defaulting to animated entrances, `scale(0)`, or motion on every element.

## Timing and Easing

Use existing project motion tokens and conventions first. As starting ranges:

| Interaction | Typical duration |
|---|---:|
| Press feedback | 100–160 ms |
| Tooltip or small popover | 125–200 ms |
| Dropdown or select | 150–250 ms |
| Modal or drawer | 200–500 ms |

Let marketing and explanatory motion follow the content's purpose and pacing. Avoid `ease-in` for ordinary UI transitions. Do not invent parallel easing or spring systems; when the project lacks suitable tokens, choose a documented curve from a reputable reference such as easing.dev or easings.co.

## Gestures and Interruption

- Gesture-driven motion must track the active gesture continuously.
- Use direct manipulation for motion that needs to be grabbed, reversed, or interrupted; do not rely on CSS transitions or keyframes for that behavior.
- Use spring motion when it improves continuity or interruption handling.
- Ensure a transition can be interrupted and reversed without jumping to an unrelated state.
- Give pointer-down feedback immediately for press interactions.

## Accessibility and Input

- Respect `prefers-reduced-motion`; remove nonessential motion or replace it with a minimal state change.
- Do not rely on motion alone to communicate meaning or action results.
- Gate hover effects to devices that support hover, and preserve keyboard interaction and visible focus.
- Ensure animation does not trap focus, delay an essential action, or make content difficult to follow.

## Performance and Tool Choice

- Use CSS for simple, non-gesture transitions.
- Use Motion (the current Framer Motion library) when layout or exit animation, springs, or gesture-driven values justify it.
- Inspect existing dependencies before adding a library. Do not add a motion dependency for a small fade or hover state.
- Keep animated work smooth by favoring composited properties and avoiding repeated layout or paint work.

## Review Checklist

For each motion, check:

- Does it communicate a real state change or improve spatial understanding?
- Is its duration appropriate to the frequency and importance of the interaction?
- Does it use the project's established timing and easing?
- Can it be interrupted or reversed where needed?
- Does reduced-motion preference produce a usable result?
- Does it work with keyboard, touch, and pointer input?
- Does it avoid unnecessary layout work and visual distraction?

If motion does not improve the experience, remove it.
