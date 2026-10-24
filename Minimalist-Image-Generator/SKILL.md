---
name: minimalist-brand-image-generator
description: Generate or edit premium minimalist images that follow the user's established visual brand identity. Use when the user requests a branded image, social media graphic, product visual, promotional creative, or other visual asset following their brand guidelines.
---

# Minimalist Brand Image Generator

## 1. Purpose

Create premium, minimalist visual assets that consistently follow the user's brand identity.

Every output should feel intentional, refined, high-contrast, and professionally art-directed. Prioritize visual hierarchy, negative space, precise composition, and restrained use of color.

The goal is not simply to make an image look minimal. The goal is to make the requested subject recognizable while maintaining a coherent visual identity.

## 2. Activation Rules

Activate this skill when the user:
- Requests an image following their brand or visual identity.
- Requests a branded social media post, advertisement, product visual, or promotional graphic.
- Asks to adapt an existing visual to the established brand guidelines.
- Requests iterations or refinements of an image governed by these brand rules.

Do not force these rules onto unrelated images when the user has not requested their brand identity.

If the user explicitly requests a different style, follow the current request unless they ask to preserve the established brand.

## 3. Brand Identity

### Color Palette

Use the following palette as the source of truth.

**Dark backgrounds and surfaces**
- `#08090a`
- `#0f1011`

**Light backgrounds and surfaces**
- `#f7f8f8`
- `#e5e5e6`

**Neutral and supporting colors**
- `#8a8f98`
- `#d0d6e0`

### Color Usage Rules

- Prefer one dominant background color and a limited number of supporting colors.
- Use dark and light combinations to create strong, accessible contrast.
- Use gray tones for secondary information, subtle dividers, and supporting visual details.
- Avoid introducing additional accent colors unless the user explicitly requests them or the subject requires a justified exception.
- Do not use gradients, multicolor effects, or decorative color transitions by default.
- Avoid textures, glows, and visual effects that weaken the minimalist aesthetic.
- Keep text readable against its background.

### Default Visual Direction

The default aesthetic is:
- Premium and minimalist.
- Clean, modern, and editorial.
- High contrast with restrained color.
- Spacious, precise, and balanced.
- Inspired by the clarity of modern software product brands.

Use references to brands or design styles as directional inspiration, not as a requirement to copy their exact layouts or assets.

## 4. Composition and Layout

### Negative Space

- Preserve generous, intentional negative space.
- Give the primary subject enough room to stand out.
- Avoid filling every empty area.
- Maintain a clear relationship between the focal subject, supporting elements, and surrounding space.

### Visual Hierarchy

Each image must have one clearly dominant focal point.

Use the following hierarchy when appropriate:
1. Primary subject or headline.
2. One supporting visual or secondary information element.
3. Optional subtle detail, label, or accent.

Not every image needs all three levels.

### Maximum Item Count

Use a maximum of three distinct primary visual elements by default.

Count major objects, illustrations, product representations, or distinct visual components. Do not count every word, letter, or minor decorative mark as a separate item.

For text-led graphics, keep the composition focused on a headline, an optional supporting line, and one primary visual element.

Avoid unnecessary icons, floating objects, decorative shapes, and redundant illustrations.

### Alignment and Spacing

- Use consistent alignment and spacing.
- Prefer simple grids and deliberate positioning.
- Avoid accidental crowding or uneven visual weight.
- Keep margins appropriate to the intended output dimensions.
- Ensure the image remains visually balanced at its final display size.

## 5. Typography

### Font Family

Use Inter exclusively for rendered text whenever the image-generation workflow supports reliable font selection.

### Permitted Weights

- Inter Regular: 400
- Inter Medium: 500
- Inter Semibold: 600

Do not introduce extra font families or decorative typefaces by default.

### Type Hierarchy

- Use weight, size, spacing, and positioning to establish hierarchy.
- Keep headlines concise and visually dominant.
- Use secondary text sparingly.
- Avoid excessive capitalization, unnecessary letter spacing, and overly dense text blocks.
- Maintain comfortable readability at the intended display size.

### Text Accuracy

When the user supplies exact copy:
- Preserve spelling, punctuation, capitalization, and wording.
- Do not invent additional claims, slogans, or labels.
- Avoid pseudo-text, random characters, and misspelled words.
- Do not silently rewrite text that must remain exact.

If the image-generation tool cannot reliably render exact text or the requested font, use an available text-layout or image-editing workflow when possible. Never claim exact typography has been applied unless the output supports that claim.

## 6. Image Generation Workflow

### Step 1: Understand the Request

Identify:
- The subject and purpose of the image.
- The intended platform or placement.
- The desired aspect ratio or dimensions, if specified.
- Any exact text, reference images, or required objects.
- Whether the task is image creation or editing.

Do not ask questions when reasonable defaults are sufficient.

### Step 2: Establish Art Direction

Choose:
- A dominant background color from the approved palette.
- One primary focal point.
- A clear composition and visual hierarchy.
- Appropriate negative space.
- Inter typography when text is required and supported.
- An aspect ratio suited to the intended use.

Treat the palette and composition as constraints, not merely suggestions.

### Step 3: Construct the Generation Prompt

Describe the requested subject first, followed by the relevant art direction.

Include:
- The exact subject and intended visual message.
- The premium minimalist aesthetic.
- Approved color values and intended color roles.
- Composition, alignment, and negative space.
- A maximum of three primary visual elements by default.
- Typography and exact copy when applicable.
- The requested aspect ratio.
- Specific elements to avoid.

Be concrete and concise. Avoid contradictory style instructions.

### Step 4: Generate or Edit

Use the available image-generation or editing capability to produce the visual.

For an existing image:
- Preserve elements the user explicitly wants to retain.
- Apply the requested brand treatment without unnecessarily changing the content.
- Do not remove essential information simply to make the composition more minimal.

If image generation is unavailable, explain the limitation and provide a ready-to-use generation prompt instead.

### Step 5: Review and Refine

Evaluate the result against the brand requirements.

Check for:
- Palette consistency.
- Clear focal point.
- Sufficient negative space.
- Appropriate visual complexity.
- Correct typography and supplied text.
- Readability and contrast.
- Correct dimensions and aspect ratio.
- Unwanted colors, gradients, textures, or decorative clutter.

If a requirement fails, refine the image when tools permit. Do not describe an unverified requirement as satisfied.

## 7. Platform Adaptation

Preserve the brand identity while adapting the layout to the intended placement.

- Social media posts: prioritize readability and a clear focal point.
- Product visuals: emphasize the product and minimize surrounding decoration.
- Promotional graphics: establish a clear message and restrained supporting detail.
- Presentation graphics: prioritize legibility at viewing distance.
- Website visuals: consider the surrounding interface, available space, and responsive cropping.

Do not assume one aspect ratio fits every platform. Follow the user's specified dimensions when provided.

## 8. Instruction Priority

Apply requirements in this order:

1. Explicit instructions in the current request.
2. Required content, reference-image constraints, and exact copy.
3. Established brand colors, typography, and visual identity.
4. Composition and item-count defaults.
5. General aesthetic preferences.

When two requirements conflict, satisfy the higher-priority requirement and preserve as much of the brand identity as possible.

## 9. Final Quality Checklist

Before delivering an image, verify:

- Does it communicate the requested subject clearly?
- Does it follow the approved color palette?
- Is the primary focal point immediately recognizable?
- Is negative space intentional and sufficient?
- Are there no more than three primary visual elements unless justified?
- Is the typography consistent with the specified font and weights where supported?
- Is all supplied text accurate?
- Are contrast and readability adequate?
- Does the image match the intended platform and dimensions?
- Have unnecessary effects and decorative elements been avoided?

The final output should feel consistent with the user's brand without sacrificing the purpose of the image.