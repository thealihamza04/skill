# Product Demo / Launch Video

**What it is:** A piece built around real product content — actual screens, actual UI, actual shots of the thing — carried by a consistent motion treatment, not a generic template with the product dropped in. The default category for "make a product video" with no platform or format named.

**When to use this category:** The request is about showing what a specific product does and why it matters, without a named social platform driving the pacing (if a platform is named, see `social-promo.md` instead). Covers launch videos, feature announcements, and walkthrough-style demos.

**Length:** 30–90s, 4–8 scenes.

## How to build it

1. **Source real content first.** Before planning motion, gather the actual screens, UI states, or product shots this video will use — mockups must be faithful to the real product, not idealized or invented. A demo that shows a UI that doesn't exist is a credibility problem, not just an anti-slop one.
   - If any UI is being rendered in code rather than captured as a real screenshot (a recreated card, dashboard, or terminal window), that's an interface-engineering problem before it's a motion one — read `../ui-elements-in-video.md` and build it using this repo's `interface-engineer`/`design-system` rules, not ad hoc styling. This is the category where getting that wrong is most visible, since the UI itself is the subject.
2. **The motion treatment is consistent across every scene**, even as the content changes screen to screen: the same camera language (e.g. a consistent push-in style for revealing UI), the same transition type between screens, the same accent color on highlighted elements. This consistency is what separates "designed" from "a template with screenshots pasted in."
3. **Structure by capability, not by UI navigation order.** Lead with the capability that matters most to the viewer, not with whatever screen happens to be first in the app. A demo that walks the literal click-path of the app usually buries the actual value.
4. **Highlight, don't just display.** When a screen is on frame, something should draw attention to the specific element that matters (a subtle scale-up, a focus dim on the rest of the frame, a cursor/pointer move) rather than just cutting to a static screenshot and hoping the viewer finds the relevant part themselves.
5. **A VO or on-screen copy carries the "why," the visuals carry the "what."** Don't make the narration describe what's already visually obvious on screen — use it to explain the benefit or context the screen alone can't show.
6. **Close on the product's name/mark and (if relevant) a single clear next step**, not on the last feature shown — the ending is a brand/CTA beat, structurally similar to a brand sting (see `brand-sting.md`).

**Sound:** A restrained, UI-style sound (a soft click or snap) is appropriate on the moment something is highlighted, not on every screen appearance — keep it as consistent across the piece as the motion treatment itself (point 2 above). If there's a voiceover, duck any SFX under it the same as music. See `../motion-rules.md` for gain/peak-placement/ducking defaults.

**Pitfalls specific to this category:**
- Generic stock-footage-style B-roll standing in for actual product content.
- Showing every feature at equal weight instead of leading with what matters.
- A motion treatment that changes style scene-to-scene, making it feel like separate clips stitched together rather than one piece.
- Narration that reads the screen text aloud instead of adding context.

**Transitions:** Pick one transition style for moving between screens/features and reuse it for every single transition in the piece — this is part of point 2's consistency requirement above, and inconsistent transition styles are one of the fastest ways a demo starts feeling like stitched-together clips. A consistent push or a consistent match cut on a recurring UI element (the same button, the same accent) both work well. See `../transitions.md`.

**Expected output bar:** Someone who's never seen the product understands what it does and why it matters, and could describe the product's core value after one watch.
