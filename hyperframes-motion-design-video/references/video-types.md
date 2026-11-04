# Video types

Classify the deliverable before planning scenes. The type sets length, scene count, pacing,
transition family and how much sound the piece wants. Match the **narration** and **dominant
technique** columns, not just the length: a 40s unnarrated piece about one chart is still a
data reveal in spirit.

| Type | Length | Scenes | Narration | Dominant technique | Transitions | Sound |
|---|---|---|---|---|---|---|
| Brand sting / intro | 2–8s | 1 gesture (≤ 2 beats) | none | one gesture resolving into the mark | none, or a match cut inside | one hit on the resolve |
| Title card / kinetic type | 5–15s | 1–3 cards | rarely | type scale, weight, rhythm | hard cut or push between cards | usually none, or one hit on the key word |
| Data reveal | 5–20s per stat | 1 per number | none | legible counter or chart build, then a hold | same transition between every stat | one hit when the number lands |
| Social promo / ad | 6–30s | 4–8 fast beats | often none | hook in 2s, muted-first | hard cuts and whips, one match cut on the reveal | hook and closing beat only |
| Product demo / launch | 30–90s | 4–8 | usually | real UI, highlighted, one camera language | ONE style for every screen change | soft UI clicks on highlights, ducked under VO |
| Explainer (punchy or documentary) | 30–90s+ | 5–10 (fewer, longer if slow) | yes | one visual metaphor per narration beat | match cuts for related beats, hard cuts for unrelated, a dissolve only at a tonal shift | narration carries; SFX sparse and ducked |
| Portfolio / brag reel | 15–30s | 6–12 | none | proof: real work, real numbers, a URL or CTA end | hard cuts on the beat, one big reveal | music-led, hits on structure |
| Reference port | the source's | the source's | the source's | match the source frame by frame | the source's | the source's |

## Resolving ambiguity
- "Make a product video" with no platform → **product demo**. A named platform (Reels, TikTok,
  Shorts, a story) → **social promo**, which brings 9:16 and muted-first rules.
- "Animate our logo" / "an intro for my videos" → **brand sting**, even if they say "video".
- A single number or chart, unnarrated → **data reveal**. The same number inside a narrated
  piece is one scene of an explainer or demo.
- "Words on screen", "animate this quote", "a title sequence" → **title card**. A whole promo
  made of text that's beat-synced to music is the word-wall format (route to its skill).
- Slow, atmospheric, 60s+ "brand film" → the explainer's **documentary variant**: same
  structure, fewer and longer shots, calmer tempo, and still no dead air.
- An existing edit, video or Remotion source to reproduce → **reference port**. Measure the
  source (`snapshot --against <video>`, ffprobe, frame-stepping) and match its timing. The
  per-scene rules below still decide *how* each scene is built.

## Per-type build notes

### Brand sting
One gesture: a shape resolving into the mark, the mark drawing on, or one camera move revealing
it. Spend 1–2s on the gesture, then hold the resolved mark ≥ 0.5–1s. Design it to survive the
50th viewing, which means understated and confident and never reliant on surprise. If it loops, check
that the first and last frames don't jump. Rebuild the logo as SVG so its parts can move.
No CTA, no story.

### Title card / kinetic typography
Choose one reading unit (whole line, word, or char) and commit. Type does the work a visual
would: a size jump or weight change on the one important word. Per-word timing follows weight,
not length (connectives fast, content words held). Letter-by-letter only when the word *is* the
payoff. Background stays near inert. Long copy → several cards, not one paragraph.

### Data reveal
The value must be readable **mid-animation**, not just at rest: ease-out counters (most of the
travel early, a long settle), with scale context visible (unit, timeframe, comparison). One
accent on the number, with axes and labels in a quiet neutral. Source every value in PLAN.md
before animating. End on a ≥ 1s hold. Several stats are several reveals that share one transition.

### Social promo / ad
Design the first 2s first: it must work muted at phone size. Beats: hook (0–2s) → setup (2–8s) →
payoff (8–20s) → closing beat/CTA (last 2–4s), and the closing beat gets its own moment. Cut
fast but keep one technique per beat. Keep text inside platform safe zones (avoid the bottom ~20%
and right ~12% on 9:16 for UI overlays). Sound is reinforcement only.

### Product demo / launch
Source real screens first (captures, `npx hyperframes capture <url>`, or UI rebuilt to match the
real product exactly). Structure by capability, leading with the one that matters most, not by
click path. Every screen **highlights** something (push-in, focus dim, cursor), and the camera
language and transition are the same across the piece. VO or copy says *why*; the screen shows
*what*. Close on the name or mark plus one next step.

### Explainer
Hook in the first 3–5s: the problem, the surprising fact or the payoff, with no wind-up. Write the script
first; scenes illustrate beats, one visual idea per beat. Punchy = short holds, 115+ BPM;
documentary = long, deep shots with continuing motion and a 60–90 BPM bed. Numbers are written
the way they're spoken ("nearly half"), and every claim is sourced.

### Portfolio / brag reel
Proof over adjectives: real project shots, real numbers (GitHub, analytics the user shows you),
the user's own mark. Rhythm comes from the music, with structural cuts on the beat. End on the
URL or handle and the mark. If it's the stat-reel shape, route to that format skill.

## Expected bar per type
- Sting: identical, clean playback; the mark reads instantly on repeat viewing.
- Title card: every word's timing feels deliberate on a second watch.
- Data reveal: pause anywhere past the first third and the approximate value is readable.
- Social: muted, phone width, first 2s, a stranger knows whether to keep watching.
- Demo: someone new can say what the product does and why it matters after one watch.
- Explainer: a newcomer can explain the idea back, and the first 5s make them stay.
- Brag reel: every number is true, and the viewer knows where to go next.
