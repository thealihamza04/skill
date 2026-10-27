# UI Elements Rendered Inside a Video

When a scene's content is a UI element built in code — a card, a terminal/CLI window, a dashboard, a button, an app screen mockup — that element is an interface-engineering problem, not a motion-design one. The motion-design rules elsewhere in this skill (easing, timing, transitions) still apply to *how it animates*, but *how it looks at rest* is governed by this repo's `interface-engineer` and `design-system` skills, exactly as if it were being built for a real app. Building it from scratch with ad hoc styling instead of those rules is the single most common reason a code-rendered UI element inside a video looks cheap even when the surrounding motion is good.

Before building any such element: read `interface-engineer`'s SKILL.md for the specific element type (cards, typography, spacing/shadows, icons, components — its section numbers below), and `design-system` for the actual color/type tokens. Don't paraphrase those rules from memory — read them, because they carry exact values that are easy to get slightly wrong.

**Use real shadcn/ui components as the baseline, not hand-rolled divs that visually imitate one.** `interface-engineer` already builds on shadcn registries for specialized sources (Brainless for terminals, Gauge UI for gauges) — the same applies to ordinary elements: install shadcn/ui's own components (`npx shadcn@latest add card`, `add button`, `add badge`, etc.) and use their actual structure (e.g. a card is `<Card><CardHeader><CardTitle>/<CardDescription></CardHeader><CardContent>...</CardContent></Card>`, not a plain bordered `<div>` with text inside it). A hand-rolled div that only copies a card's border and padding is missing everything a real component gives you for free — correct internal spacing, correct content slots, a structure that doesn't leave dead space when content is shorter than expected.

## Internal composition and spacing

Neither `interface-engineer` nor `design-system` defines a numeric spacing scale — they assume a project already has one to reuse. A video scene usually doesn't, so use this skill's own default scale rather than picking arbitrary pixel values per element: **4 / 8 / 12 / 16 / 24 / 32 / 48 / 64px**, each a multiple of 4. Pick values from this scale consistently across every UI element in the project the way a real design system would; if the project being represented already has its own spacing tokens (because it's a real product being faithfully recreated), use those instead.

- **Icon + text pairing:** size the icon to roughly 1.1–1.2× the adjacent text's line height, with a consistent gap (pick one value from the scale above and reuse it everywhere icons sit next to text) — an icon that's a different size relative to its label in every instance reads as sloppy even if each instance looks fine alone.
- **Label/value pairs** (a stat with its caption, a setting with its description): keep a consistent vertical order and gap across every instance in the scene — all labels above their values, or all below, never mixed.
- **Rows and lists:** consistent row height and consistent internal padding across every row — a list where rows have slightly different heights because content length wasn't accounted for looks unfinished.
- **Avatars/profile elements:** a real initial, a real (or faithfully mocked) image, or a simple geometric placeholder consistent with the project's graphics palette — never a generic stock silhouette icon, which reads as the least-finished option available.

## Cards and panels

- **Border radius:** use `interface-engineer`'s concentric-radii formula (outer radius = inner radius + padding) for any nested container — a card with an inner element should not have an arbitrarily-picked outer radius.
- **Shadow:** use the exact standard shadow value `interface-engineer` defines (`shadow-[0px_2px_3px_-1px_rgba(0,0,0,0.1),0px_1px_0px_0px_rgba(25,28,33,0.02),0px_0px_0px_1px_rgba(25,28,33,0.08)]` or its equivalent in whatever styling system the composition uses) rather than an invented drop-shadow. Use it only where separation is actually needed — not on every surface.
- **No pill shapes.** `interface-engineer`'s non-negotiable rule against pill/capsule styling on buttons, badges, labels, and containers applies here exactly as it would in a real app.
- **One card/panel as the scene's dominant element**, per this skill's own Section 2 one-idea-per-scene rule — a scene showing a grid of five cards at equal weight usually means the actual subject is one of them, with the rest as unfocused context.
- **No forced dead space.** A card's height should come from its actual content (padding from the spacing scale above, plus whatever's really in it) — never a fixed min-height that leaves a large unexplained blank gap because there was no icon or visual to fill it. If the design calls for a visual in the card, add a real one (an icon per `interface-engineer` Section 5, or a real generated asset); if there isn't one, let the card size to its title and description and don't manufacture space for content that doesn't exist.

## Terminal / CLI windows

- **Don't hand-roll a terminal mockup.** Use `interface-engineer`'s curated source for this — Brainless (`bunx shadcn@latest registry add @brainless=https://brainless.swerdlow.dev/r/{name}.json`), which already covers sessions, messages, tool calls, diffs, permissions, and slash menus — and adapt its visual hierarchy rather than building window chrome and prompt styling from scratch.
- **Syntax highlighting, not flat colored text.** Use a real highlighter (`interface-engineer` names Shiki) if any code is shown — hand-picked colors per token read as fake the moment someone who writes code looks closely.
- **Typing rhythm, if animated, should look like real typing**, not a uniform per-character reveal — vary per-character timing slightly, and let the cursor behave like a real terminal cursor (blink when idle, not while text is appearing).
- **Keep window chrome minimal** — traffic-light dots or a title bar if they're genuinely part of the reference being matched, nothing skeuomorphic beyond that.

## Grid items (feature cards, capability cards)

A grid of cards is where generic-SaaS-template chrome shows up most — name and ban each of these specifically rather than trusting the general minimalism rules to catch them:

- **No numbered index badges ("01", "02", "03"...)** unless the number carries real, meaningful sequence the user actually asked to show in order (real step 1 → step 2 → step 3, not four unordered feature cards wearing numbers as decoration).
- **No decorative corner dot or status dot** on a card with no function — a dot that doesn't indicate a real state (online/offline, active/inactive) is chrome, not information.
- **No eyebrow/kicker label** above the grid's section headline (see the main skill's Section 1 "Generic SaaS-template chrome").
- **Every card's visual slot is either a real asset or doesn't exist.** If a card is meant to have an icon or image, render a real one (this repo's image-generation skills, or a real icon per `interface-engineer` Section 5) before delivering — a blank or gray placeholder box is a failure, not a stand-in. A card with no real visual to show is better built with no visual slot at all than with an empty one.
- **Cards in a grid still obey the one-dominant-idea budget per card**: a title and one short description line is usually enough — don't let each card individually accumulate its own eyebrow, badge, and dot on top of the grid-level ones.
- **Build the grid from real shadcn/ui `Card` components**, not bordered divs — and give each card either a real icon or no icon slot at all, never an empty reserved area. A grid of cards that are each just a title, a description, and a large blank gap is the single most common version of this category's generic-template failure.

## Buttons, inputs, badges, and other controls

- Defer entirely to `interface-engineer` Sections 5 and 8 (icons, logos, badges/labels, button copy) — action-describing labels, no pill shapes, Lucide/React Icons (never emoji) for any icon shown.
- A control shown in a video is usually static (not actually interactive), but it should still look like it *could* be clicked — correct affordance, correct contrast, no fake hover state baked in unless the scene specifically simulates a pointer move.
- If the scene does simulate a click, hover, toggle, dropdown, or any other interaction, that motion is covered in `../micro-interactions.md`, not here — this section covers how the control looks at rest.

## Typography and color inside the UI element

- Use `design-system`'s actual tokens (Inter, weights 400/500/600, the documented color palette) for any text or color inside the rendered UI — not a visually-similar substitute. If the element represents a real product that has its own brand tokens, use those instead and say so; don't silently default to this repo's palette for someone else's product.
- This is what makes a code-rendered mockup indistinguishable from a real screenshot, which `product-demo.md` already requires ("mockups must be faithful to the real product") — faithfulness includes the actual design tokens, not just the right layout.

## Checklist addition

Before delivering a scene that renders a UI element in code, confirm:

- [ ] The element was built from a real shadcn/ui (or other named, real) component — not a hand-rolled div that only copies the look of one.
- [ ] Concentric radii and the standard shadow value were used, not invented ones.
- [ ] No pill/chip/badge shapes anywhere in the element.
- [ ] No card or panel has forced dead space — height comes from real content, not a fixed min-height with nothing to fill it.
- [ ] No eyebrow/kicker label, numbered index badge, decorative accent dot, or separator glyph that wasn't explicitly asked for.
- [ ] No empty/placeholder visual slot — every icon or image area shows a real rendered asset, or doesn't exist.
- [ ] A terminal/CLI element used Brainless (or an equivalent real component source) rather than being hand-built from scratch.
- [ ] Any code shown uses real syntax highlighting, not flat hand-picked colors.
- [ ] Typography and color inside the element use real design tokens (this repo's `design-system`, or the represented product's own brand if different).
