# Video Types

Classify the request against this table **before** breaking it into scenes (Section 3, Step 1 of the main skill). Building the wrong type of video for the request — a long narrated explainer when a 6-second sting was wanted, or a static product shot when a demo was wanted — is itself a source of the gap between what was expected and what gets delivered, independent of execution quality.

These are deliberately kept to the main categories that actually come up for Remotion work, each with its own detailed how-to-build guide in `video-types/`. Read the matched category's file before planning scenes — this index is for routing, not building from.

| Category | Typical length | Narration | Read this when the request is... |
|---|---|---|---|
| [Brand Sting / Recurring Intro](video-types/brand-sting.md) | 2–8s | None | A logo animation, a recurring show/app intro, anything played repeatedly |
| [Title Card / Kinetic Typography](video-types/title-card.md) | 5–15s | Rarely | Words themselves are the visual — a quote, a headline, a section title |
| [Motion Graphic / Data Reveal](video-types/data-reveal.md) | 5–20s | None | One stat or chart animating in, unnarrated |
| [Social Promo / Ad Clip](video-types/social-promo.md) | 6–30s | Often none | A platform is named (Reels, TikTok, a story), or it's meant to stop a scroll |
| [Product Demo / Launch Video](video-types/product-demo.md) | 30–90s | Usually | "Make a product video" with no platform named — the default for product requests |
| [Faceless Explainer](video-types/faceless-explainer.md) | 30–90s (60s+ for the slow/documentary variant) | Yes | "Explain this," "make a video about this topic/idea" — includes slower brand-film pacing as a variant, not a separate category |

## Resolving ambiguity

- A short, unnarrated piece where **motion is the message** is a data reveal or a sting, even if it uses a stat or a screenshot as source material. A narrated, multi-scene piece built from the same material is a faceless explainer or product demo instead.
- "Make a product video" with no further detail defaults to **product demo**, not social promo — a named platform or an explicit "for Reels/TikTok/a story" is what moves it to social promo instead.
- A request that names a specific platform usually means **social promo** regardless of subject, because the platform's pacing and aspect-ratio contract dominates over subject matter.
- A slow, atmospheric, 60s+ "brand film" request is the **faceless explainer** category's slow variant, not a separate category — same structure, different pacing (see that file's pacing section).
- Length is a strong signal, not a hard rule: a 45-second piece with one chart and no narration is still closer to a data reveal in spirit than an explainer — match the "narration" and "dominant technique" columns, not just the duration.

## Special case: porting existing footage

If the request is explicitly to reproduce an existing edit (another video, existing Remotion source, or a confirmed storyboard) in code rather than to design something new, the category above doesn't apply in the normal sense — match the source's existing length, scene count, and pacing instead of this table, and treat the port as successful when it's indistinguishable from the source in timing and framing. The "how to build it" steps in the matched category file still apply to *how* each individual scene is implemented, just not to the overall length/pacing decisions.
