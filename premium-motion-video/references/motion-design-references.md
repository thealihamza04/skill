# Motion Design References

Researched via web search so the calibration is grounded in real, human studio work and documented animation theory — not invented or AI-generated reference material. Treat studio sites as moving targets: visit them directly for current work rather than relying on a memorized description, since portfolios change.

## Real studios to calibrate "premium and minimal" against

- **[Ordinary Folk](https://ordinaryfolk.co)** — Vancouver-based motion design and animation studio. Confirmed via a [School of Motion interview](https://students.schoolofmotion.com/blog/how-to-design-for-animation-with-ordinary-folk). Known for restrained, deliberate branded motion work (clients have included Google, Webflow, Procreate). The calibration point: craft and precision over spectacle — nothing on screen that isn't earning its place.
- **[FEVR](https://wearefevr.com)** — New York/LA studio doing motion graphics, 2D/3D animation, and creative direction (clients cited include Netflix, Dior, Coinbase). Site copy is spare and text-led ("We make things move"). Calibration point: confident restraint in both message and motion — short, punchy statements rather than crowded screens.
- **[BUCK](https://en.wikipedia.org/wiki/Buck_(design_company))** — one of the most awarded motion studios globally (founded 2004, offices in NY/LA/Sydney/Amsterdam). This is the high end of the craft, well beyond most production budgets, but useful as a ceiling reference: motion is always subordinate to the idea and the brand, never decoration for its own sake.

When in doubt about whether a scene reads as "premium," ask: would this sit comfortably in one of these studios' reels, or does it look like a generic template? If it's the latter, go back to Section 2 of the main skill.

## Animation principles (grounded, not invented)

Source: [Figma — "Principles in Motion"](https://www.figma.com/blog/principles-in-motion/). The core vocabulary to use when deciding Section 3 Step 2 for each scene:

- **Ease in / ease out** — motion accelerates and decelerates like a physical object, never starts or stops instantly.
- **Anticipation** — a small counter-movement before the main action (can be subtle or dramatic) that makes the eye ready for what's coming.
- **Overshoot** — motion passes slightly past its resting point before settling, the way a real object with momentum would.
- **Follow-through and overlap** — secondary elements (or parts of an element) continue moving briefly after the primary motion stops, rather than everything locking in sync.
- **Hold and settle** — motion needs a moment of stillness to register before the next beat; don't chain actions back-to-back with no rest.

Use these as the vocabulary for the "which animation principle" question in Section 3 Step 2 — naming the actual principle forces a deliberate choice instead of an arbitrary default curve.

## Sound design for motion (grounded, treat numbers as starting points)

Source: [Pixflow — cinematic transition sounds](https://pixflow.net/blog/enhancing-motion-graphics-with-cinematic-transition-sounds/) and [Motion the Agency — sound design examples](https://www.motiontheagency.com/blog/sound-design-examples-before-after-in-motion).

- **Align the peak of a sound with the moment the motion resolves**, not with when it starts. The strongest part of the sound should land on the exact frame the movement finishes.
- **Layer a soft movement sound under a stronger accent** for transitions that have both a directional motion and a final emphasis — e.g. a quiet whoosh under a sharper impact hit at the landing frame.
- **Keep layered sounds in separate frequency ranges** so they don't mask each other.
- **Keep UI-scale sounds tiny** — subtle clicks on snaps, gentle whooshes between screens, confirmations quiet enough not to distract. This is the opposite of a generic stock-library whoosh dropped on every cut.
- These sources are blog/vendor content, not a formal standard — treat specific numbers (e.g. exact dB levels) as starting points to tune per project, not fixed rules.

## Remotion implementation

Remotion's own team publishes an official agent-skill package covering the technical implementation side (composition structure, markup, rendering, audio, assets, fonts, timing): **`remotion-dev/skills`**, documented at [remotion.dev/skills](https://remotion.dev/skills) and [remotion.dev/docs/ai/skills](https://www.remotion.dev/docs/ai/skills). Install with:

```bash
npx skills add remotion-dev/skills
```

This main skill (`premium-motion-video`) deliberately does not duplicate Remotion API guidance — use `remotion-dev/skills`'s own sub-skills (the umbrella `remotion-best-practices` skill, plus `remotion-markup` and the rendering/audio-specific ones) for how to actually build the composition once Section 3's plan is written.
