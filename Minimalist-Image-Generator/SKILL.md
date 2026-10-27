---
name: minimalist-brand-image-generator
description: Generate or edit premium minimalist, light-first branded images (social posts, thumbnails, covers, product visuals, promo graphics, slide visuals) using the user's brand palette and Inter typography. Use when the user asks for a branded, minimal, clean or premium image, or says "in my brand style". Not for vibrant, cinematic, painterly or photoreal images (use vibrant-imggen) and not for UI/code work (use design-system).
---

# Minimalist Brand Image Generator

## 1. Purpose

Create premium, minimalist visual assets that follow the user's brand identity.

Every output should feel intentional, refined, high-contrast and art-directed. Prioritize one clear focal point, negative space, precise composition and restrained color.

Minimal is not the goal by itself. The goal is: the subject stays **instantly recognizable**, and the image still looks like the same brand every time.

## 2. When to Use This Skill

Activate when the user:
- Asks for an image in their brand, their style, or "minimal / clean / premium / dark" style.
- Asks for a social post, carousel slide, YouTube thumbnail, cover, banner, ad, product visual or slide graphic and has not named another style.
- Asks to restyle or refine an existing image to match the brand.
- Asks for changes (iterations) on an image made with this skill.

Do not use when:
- The user asks for a different style (vibrant, cinematic, anime, realistic photo, etc.). Follow the current request. Use `vibrant-imggen` for those.
- The task is a UI, website or document layout. Use `design-system`.
- The user did not ask for their brand. Do not force these rules onto unrelated images.

If a request mixes both ("minimal but with a colorful sunset"), follow the explicit request and keep as much of the brand structure (layout, type, spacing) as possible.

## 3. Brand Identity

This skill uses the same tokens as the `design-system` skill. If the two ever disagree, `design-system` is the source of truth. Update this file to match.

### Core palette

| Token | Hex | Role |
|---|---|---|
| Canvas | `#08090a` | Dark-mode background (alternate; see Light first, dark second below) |
| Surface | `#0f1011` | Cards, panels, inset areas on dark |
| Primary text (dark mode) | `#f7f8f8` | Headlines and main text on dark; also the default light-mode canvas |
| Highlight | `#e5e5e6` | Strokes, dark-mode surface; chips/badges only if the user explicitly asks for one |
| Supporting text | `#d0d6e0` | Subtitles and secondary copy on dark |
| Quiet text | `#8a8f98` | Captions, labels, dividers. **Dark backgrounds only** |

### Graphics palette (for shapes, icons, illustration)

| Token | Hex | Role |
|---|---|---|
| Charcoal | `#2a2d33` | Linework, borders, neutral fills |
| Slate | `#5c6370` | Secondary lines and shapes. Also quiet text on light backgrounds |
| Indigo | `#4f46e5` | The single accent. One key shape or symbol only |
| Deep navy | `#0f172a` | Alternative dark graphic background |
| White | `#ffffff` | Crisp highlights and cutouts |

### Light first, dark second

- **Default is light/white.** Use `#ffffff` (or `#f7f8f8`) canvas, near-black `#08090a` text, and near-black/charcoal (`#08090a` to `#2a2d33`) for drawn assets, icons, and people — unless the user asks for dark or the placement needs it (a night theme, a dark app UI, a dark slide deck).
  - **Why:** image models reproduce brand colors far more reliably on a light/white canvas. A near-black `#08090a` canvas is harder for most models to hold cleanly and tends to drift off-palette (banding, muddy grays, wrong accent hue). Default to white until generation quality on dark canvases improves.
- **Dark mode (when asked for, or the placement needs it):** canvas `#08090a`, surface `#0f1011`, primary text `#f7f8f8`, secondary text `#d0d6e0`, quiet text `#8a8f98` (dark backgrounds only).
- Never mix both modes in one image except for a deliberate single contrast block.

### Contrast rules (measured)

- `#8a8f98` is about 6:1 on `#08090a`. Good for captions on dark.
- `#8a8f98` is only about 3:1 on `#f7f8f8`. **Too weak for small text on light.** Use `#5c6370` (about 5.7:1) instead.
- Indigo `#4f46e5` is about 3:1 on dark. Use it for large shapes or symbols only, never for small text on dark. On light it is about 6:1 and is fine for text.
- Body and caption text should reach at least 4.5:1. Large headlines at least 3:1.
- These numbers can drift if the palette ever changes. Do not trust memory for a pairing not listed above (a new accent color, a supplied logo color on a brand surface) — run `scripts/check_contrast.py <fg_hex> <bg_hex>` and use the real ratio.

### Color rules

- One dominant background. One or two supporting colors. Indigo at most once.
- No gradients, glows, neon, textures or multicolor effects by default.
- No new accent colors unless the user asks or the subject needs one (for example, a recognizable product color). If you add one, use it once, small, and say so.
- Real logos or product photos the user supplies keep their original colors. Do not recolor them.

## 4. Visual Language

"Minimalist" needs a concrete look. Use this.

**Shapes and forms**
- Crisp geometric silhouettes: circles, rounded rectangles, lines, simple solids.
- Flat fills with clean edges. No photographic lighting, no painterly texture, no heavy 3D.
- If depth is needed, use a restrained isometric view with fine edge lines, or one soft shadow. No glossy renders.

**Linework and icons**
- Thick, consistent strokes with soft rounded ends.
- Do not mix thin delicate lines with bold lines in the same image.
- Corner radius: consistent across the image (rounded, not sharp, not pill unless it is a chip).

**Photos and people**
- Default to illustration or abstract form, not photos.
- If the user supplies a photo or a person: keep it, crop cleanly, and place it on the palette background. Do not generate a realistic face unless asked. Prefer a clean cutout, simple silhouette or the supplied photo.

**Recognizability test (the "squint test")**
Name the 1 to 3 features that make the subject recognizable (for example: for a brain, the two-lobe outline; for a rocket, the nose cone and fins). Keep exactly those. Remove everything else. If the subject is not recognizable when squinting, add back detail, not decoration.

## 5. Composition and Layout

### Hierarchy and element budget
A brand image is built from **at most three slots** — nothing else by default:
1. **Heading** — the one idea, if the image needs words at all.
2. **Subheading** — only if the heading genuinely needs support. Skip it by default; most images don't need it.
3. **Visual asset** — one icon, illustration, product shot or photo. Skip it if the heading alone communicates the idea.

Decide per request which of these three the content actually needs — one, two, or all three, never more. A text-only graphic is heading (+ optional subheading), no visual. An icon-only graphic (profile picture, logo mark) is the visual alone, no text. Most posts need two of the three, not all three — do not default to using all three just because they're available.

**No pills, chips, badges, tags, dividers, stat callouts, or other decorative marks by default** — they are not one of the three slots. Add one only if the user explicitly asks for it, and then treat it as a slot they asked for, not something to add on top of heading/subheading/visual.

### Space and alignment
- Outer margin: at least **8% of the shorter side**.
- Focal subject occupies roughly **30 to 50%** of the frame. The rest is breathing room.
- Use a simple grid. Align to one axis (left edge or center). Do not mix both.
- Place the focal point on a thirds line or the center, not randomly.
- Keep visual weight balanced. Do not push everything to one corner without a reason.

## 6. Typography

### Font and weights
Inter only: Regular 400, Medium 500, Semibold 600.

| Use | Weight |
|---|---|
| Big headline / cover statement | Medium 500 |
| Section label, short title | Medium 500 |
| Body and supporting text | Regular 400 |
| One short high-priority detail (a number, a name) | Semibold 600 |

### Scale (relative to image height)
- Headline: about **6 to 10%** of image height.
- Supporting line: about **2.5 to 3.5%**.
- Caption / handle: about **1.8 to 2.5%**, never below readable size at the final display size.
- Headline: tight but natural spacing, line height about 1.1 to 1.2. Supporting text line height about 1.4 to 1.5.
- Headline max about **8 words**. Supporting line max about **16 words**. Never long paragraphs.
- Sentence case by default. Avoid ALL CAPS and wide letter spacing.

### Exact text rules
When the user gives exact copy:
- Keep spelling, punctuation, capitalization and wording.
- Do not add slogans, claims or labels that were not asked for.
- Do not invent text. No pseudo-text, no gibberish characters.

When the user does not give copy and text is needed:
- Write it in the brand voice (below) and show the text you used.

### Reliable text workflow
AI image models often misspell text and cannot guarantee Inter. So:

1. **Preferred for any image with text:** generate the visual with **no text** (add "no text, no letters, no logos" to the prompt), leave a clean empty area for the copy, then add the text in a layout step (HTML/CSS, SVG, or Pillow with the Inter font file) and export to PNG.
2. **Only if the model renders text reliably** (short headline, a few words) may you let the model draw it. Then check every character.
3. Never say "Inter was used" or "text is exact" unless you placed it yourself or verified it.

**Getting the Inter font file for the layout step**
Before promising Inter, confirm you actually have it:
- Check the project for a bundled font first (`find . -iname "*inter*" -name "*.ttf" -o -iname "*inter*" -name "*.otf"`, or a `fonts/`/`assets/` folder).
- If none exists, download the static weights you need (Regular/Medium/SemiBold) from Google Fonts (`fonts.google.com/specimen/Inter`) into the scratchpad or a project `assets/fonts/` folder before running a Pillow/SVG layout step.
- If you cannot fetch or locate the font, say so and fall back to the closest available system sans-serif rather than silently substituting and claiming it is Inter.

## 7. Brand Voice (when you write the copy)

Clear, thoughtful, confident, human. Lead with the problem or the outcome.
- Short headlines with one idea.
- Action words: build, solve, simplify, automate, improve, scale.
- No hype, no buzzwords, no empty promises, no jargon for its own sake.
- Connect tech and AI to a real benefit.

## 8. Platform and Size Guide

Use the user's size if given. Otherwise pick from this table. Do not assume one ratio fits everything.

| Placement | Size | Ratio | Notes |
|---|---|---|---|
| Instagram / LinkedIn feed post | 1080 × 1350 | 4:5 | Best default for feed |
| Square post | 1080 × 1080 | 1:1 | |
| Story / Reel / Short cover | 1080 × 1920 | 9:16 | Keep text out of top 14% and bottom 20% |
| LinkedIn / link-share image | 1200 × 627 | ~1.91:1 | Keep key content centered |
| YouTube thumbnail | 1280 × 720 | 16:9 | One big focal point, max about 4 words, readable at tiny size. Keep bottom-right corner free (timestamp badge) |
| YouTube channel banner | 2560 × 1440 | 16:9 | Keep important content inside the central 1546 × 423 safe area |
| Slide / presentation | 1920 × 1080 | 16:9 | Large text, readable from far |
| Website hero | 1600 × 900 or as given | 16:9 | Keep subject away from edges for responsive crop |
| Profile picture / logo mark | 1000 × 1000 | 1:1 | Must work as a circle crop |

If the tool only supports certain ratios, generate the closest one and crop or extend on the canvas color. Tell the user.

### Transparent backgrounds
If the deliverable is a logo mark, icon, badge, or anything meant to be layered onto another surface later (not a finished post or thumbnail), generate or export it with a **transparent background** rather than the canvas color, and say so when delivering it.

## 9. Workflow

### Step 1: Read the request
Find: subject, purpose, platform, size, exact text, supplied images or logos, create vs. edit, light vs. dark.
Do not ask questions when reasonable defaults work. If something is truly blocking (for example exact copy is missing for a text-heavy design), make a sensible choice, say what you chose, and continue.

### Step 2: Art direction (decide before prompting)
Write down in one line each:
- Background (light/white default) and text colors.
- Which of the three slots this needs — heading, subheading, visual asset — and why not the others.
- Focal point and the 1 to 3 recognizable features of the subject (if there's a visual asset).
- Layout: where the subject sits, where the text sits.
- Size and ratio.
- Whether text will be placed in a layout step or by the model.

**Series (carousel, multi-post set):** write this art-direction block once, then paste it verbatim into the prompt for every image in the set, changing only the subject/text per slide. Do not re-derive decisions like accent position or margin per image — that drift is what makes a "set" look like unrelated images.

### Step 3: Build the prompt
Put the **subject first**, then style, then color, then layout, then exclusions. Use plain color names together with hex, because image models often follow words better than hex codes alone (for example "near-black `#08090a`").

Template:

```
[Subject and what it must communicate], shown as [simple form: flat geometric / rounded-line icon / restrained isometric].
Premium minimalist brand graphic. [Light | Dark] canvas, off-white #f7f8f8 or white #ffffff [or near-black #08090a].
Colors: [list only the colors used with roles], one indigo #4f46e5 accent on [one element] only.
Composition: [heading only | heading + subheading | heading + visual | visual only | all three], [position], generous negative space, [margin], [aspect ratio and size].
[Clean empty area at (position) reserved for headline text.] | [Text: "EXACT COPY" in Inter Medium.]
Flat color fills, crisp edges, consistent rounded line weight.
Avoid: gradients, glow, neon, textures, drop-shadow clutter, pills, chips, badges, tags, extra icons, floating particles, stock-photo look, gibberish text, watermarks, logos, anything beyond the heading/subheading/visual slots used.
```

Keep it concrete and short. Remove contradictions (do not say "minimal" and "highly detailed").

### Step 4: Generate or edit
- Use the available image tool. State the size/ratio you asked for.
- **Editing an existing image:** keep what the user wants kept (subject, supplied text, logo, faces, product). Apply the brand treatment (background, palette, spacing, type) without changing content. Never remove essential information just to look more minimal.
- **Series (carousel, set of posts):** reuse the same background, margins, type scale, icon style and accent position in every image so they look like one set.
- **No image tool available:** say so, and give the ready-to-use prompt from Step 3 instead.

### Step 5: Check the result (actually look at it)
Open or view the output. Then check:
- Colors: only palette colors appear. Sample pixels if you can.
- No gradients, glow, texture or stray accent colors.
- One clear focal point; squint test passes.
- Only the heading/subheading/visual slots decided in Step 2 are present — no pills, chips, badges, tags or other decorative extras that weren't asked for.
- Margins at least 8%; nothing cropped by mistake.
- Text: every word and character matches the copy; font and weights as specified; contrast meets Section 3.
- Correct size and ratio. Safe areas respected for the platform.
- Small-size test: still readable and recognizable when shrunk to thumbnail size.

If something fails, fix it and regenerate or re-layout (maximum 2 refinement rounds on your own, then deliver the best one and say what is still off). Do not describe a check as passed if you did not run it.

### Step 6: Deliver
Save the final file to the project working directory or scratchpad with a descriptive name (e.g. `brand-post-launch-1080x1350.png`), then send it to the user as a file, not just a description. Add one or two lines: the size, dark/light choice, and anything the user should know (for example "text was added in a layout step with Inter"). Offer one useful variation (light version, other size), not a list.

## 10. Instruction Priority

When rules conflict, follow this order:
1. Explicit instructions in the current request.
2. Required content: exact copy, supplied logos and photos, reference-image constraints.
3. Legibility and accessibility (contrast, readable size).
4. Brand colors, typography and visual language.
5. Composition and item-count defaults.
6. General aesthetic preferences.

Keep as much of the brand as possible when a higher rule wins.

## 11. Final Checklist

- [ ] Subject is clear in one second (squint test).
- [ ] Only palette colors; indigo used at most once; no gradients or effects.
- [ ] Light/white by default, or dark with correct dark-mode tokens. Not mixed.
- [ ] Only the needed slots from heading/subheading/visual — no pills, chips, badges or other decorative extras added by default.
- [ ] One focal point, 8%+ margins, real negative space.
- [ ] Inter, weights 400/500/600, hierarchy by size and weight.
- [ ] Text is exact, placed reliably, and spelled correctly.
- [ ] Contrast OK (4.5:1 body, 3:1 large). `#8a8f98` not used as small text on light.
- [ ] Right size, ratio and platform safe areas.
- [ ] Series members match each other (same art-direction block reused, not re-derived).
- [ ] Any color pairing not already in Section 3 was checked with `scripts/check_contrast.py`, not guessed.
- [ ] If Inter was promised, the font file was actually located or downloaded, not assumed.
- [ ] Output was visually checked, and claims made to the user are true.
