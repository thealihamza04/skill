---
name: vibrant-imggen
description: Generate or edit vibrant, cinematic images with expressive color, layered depth, atmospheric lighting, dreamy landscapes, anime-inspired environments, macro bokeh, or ethereal night scenes. Use when the user asks for a vibrant, cinematic, painterly, dreamy, anime-style, photoreal nature, macro, or atmospheric/night image. Not for a minimal, clean, dark-first or branded image (use minimalist-brand-image-generator) and not for UI/code work.
---

# Vibrant Image Generation

## Purpose

Create and generate vibrant, cinematic images using deliberate color contrast, layered depth, atmospheric lighting, and carefully controlled visual detail.

The goal is to produce images that feel immersive, polished, emotionally evocative, and compositionally intentional rather than merely colorful.

## When to Use This Skill

Activate when the user asks for an image that is vibrant, cinematic, painterly, dreamy, anime-style, photoreal nature/landscape, macro, or atmospheric/night, and has not asked for their brand.

Do not use when:
- The user asks for their brand, or for something minimal, clean, dark-first, or premium-corporate. Use `minimalist-brand-image-generator` instead.
- The task is a UI, website, or document layout.

If a request mixes both ("vibrant sunset but keep it on-brand"), follow the explicit request and borrow structure (layout, restraint, focal point) from `minimalist-brand-image-generator` rather than ignoring it.

## Core Visual Styles

### 1. Vibrant Foreground Framing

**Visual direction:** Bold, high-contrast compositions with foreground elements framing a central subject.

- **Palette:** Magenta, coral, vivid red, sunny yellow, fiery orange, cobalt blue, and azure.
- **Lighting:** Direct sunlight, crisp highlights, defined shadows, and natural reflections.
- **Textures:** Organic petals, foliage, matte surfaces, and realistic material details.
- **Composition:** Close foreground framing, low-angle perspectives, selective focus, and strong separation between foreground and background.
- **Depth:** Use blurred foreground elements to guide attention toward the main subject.

### 2. Painterly Anime Landscapes

**Visual direction:** Expansive, dreamlike environments with hand-painted charm and cinematic scale.

- **Palette:** Azure skies, golden fields, emerald hills, warm earth tones, and soft cloud whites.
- **Lighting:** Golden-hour sunlight, atmospheric haze, soft sunbeams, and gentle ambient illumination.
- **Textures:** Painterly brushwork, clean cel-shaded forms, organic terrain, and stylized environmental details.
- **Composition:** Wide landscapes, dramatic cloud formations, distant hills, winding paths, and small human figures that establish scale.
- **Surreal elements:** Floating islands, isolated hilltop houses, impossible terrain, or other fantastical details when appropriate.

Use anime-inspired environmental art as a visual direction; do not assume every scene requires the same recognizable style.

### 3. Macro Bokeh & Meadow Photography

**Visual direction:** Soft, natural imagery emphasizing delicate details, shallow depth of field, and fresh color.

- **Palette:** Clover green, emerald, pastel white, sunny yellow, and sky blue.
- **Lighting:** Dappled sunlight, soft highlights, gentle backlighting, and natural diffusion.
- **Textures:** Grass blades, flower petals, dew, and subtle organic surface detail.
- **Composition:** Ground-level viewpoints, flowers in the foreground, distant meadows, and open skies.
- **Focus:** Keep the intended subject sharp while using foreground and background bokeh to create depth.

### 4. Ethereal Night & Starlight

**Visual direction:** Dreamy nighttime scenes with luminous details and a strong sense of wonder.

- **Palette:** Deep navy, indigo, midnight blue, warm amber, golden yellow, and crisp starlight white.
- **Lighting:** Localized lantern or window glow, subtle rim lighting, luminous flowers, and restrained lens flares.
- **Atmosphere:** Soft haze, delicate film grain, distant stars, and gentle light diffusion.
- **Composition:** Wide cinematic framing, low-angle perspectives, illuminated foreground subjects, and expansive night skies.
- **Contrast:** Preserve dark shadow areas while allowing important light sources to glow naturally.

## Universal Design Principles

### Color & Contrast
Use a deliberate palette with a clear dominant color and a smaller number of supporting accents. Pair cool backgrounds with warm foreground highlights when it strengthens the composition.

### Depth & Layering
Build scenes with distinct foreground, middle-ground, and background elements. Use perspective, scale, atmospheric haze, and selective focus to create spatial depth.

### Lighting
Choose a lighting direction that supports the mood: direct sunlight for vivid scenes, golden hour for warmth, diffused daylight for softness, or localized illumination for nighttime imagery.

### Composition
Establish one clear focal point. Use framing, leading lines, negative space, scale, and visual hierarchy to direct attention. Avoid filling every area with competing details.

### Texture & Detail
Match texture to the medium. Photography should feel optically plausible; painterly scenes should have cohesive brushwork; surreal scenes should maintain intentional visual consistency.

### Mood
Make the emotional atmosphere explicit in the prompt, such as joyful, tranquil, nostalgic, wondrous, mysterious, or dreamlike.

## Prompt Generation Workflow

When creating an image prompt:

1. **Identify the subject:** Define the main subject, environment, and intended purpose.
2. **Choose a visual direction:** Select one core style or combine compatible styles intentionally.
3. **Define the palette:** Specify dominant colors and meaningful accent colors.
4. **Describe the composition:** Include viewpoint, framing, focal point, and spatial layers.
5. **Specify lighting:** Describe its direction, softness, intensity, and atmospheric effect.
6. **Add material details:** Include only textures and details that strengthen the image.
7. **Set the mood:** Communicate the intended emotional response.
8. **Refine constraints:** Specify aspect ratio, text placement, subject positioning, or exclusions when relevant.
9. **Generate or edit:** Use the available image-generation tool to produce the image from the finished prompt. If no image tool is available, say so and give the ready-to-use prompt instead.
10. **Review the result:** Open or view the output and check it against the Quality Checklist below, plus: correct aspect ratio, no unintended text or watermarks, and palette matches what was specified. Do not describe a check as passed if you did not run it.
11. **Deliver:** Save the file with a descriptive name and send it to the user. Note anything the user should know (style combined, aspect ratio, any deviation from the request).

### Text in vibrant scenes
These styles are predominantly textless (landscapes, macro, night scenes). If the user needs text (a quote over an image, a title card):
- Prefer adding it in a separate layout step after generating a textless image, since image models render text unreliably — add "no text, no letters" to the generation prompt, leave a clean area for it, then overlay the text yourself.
- If the user gives exact copy, preserve spelling, punctuation, and wording exactly. Do not invent slogans or captions that were not requested.

### Platform and size
Use the user's requested size if given. Otherwise pick a size that fits the intended use (e.g. 1080×1350 for a feed post, 1920×1080 for a wide cinematic scene, 1080×1920 for a story/reel). Do not default to one ratio for every request — a landscape composition usually wants to breathe wider than a square crop allows.

## Output Standards

- Write prompts that are specific, coherent, and ready to use in an image-generation model.
- Prefer concrete visual descriptions over vague terms such as “beautiful” or “cinematic.”
- Keep the subject, composition, lighting, and palette aligned.
- Combine styles only when their visual characteristics complement each other.
- Avoid unnecessary adjectives, conflicting instructions, excessive effects, and random decorative elements.
- Do not add text, logos, watermarks, or UI elements unless requested.
- Adapt aspect ratio and composition to the intended use when specified.
- Never assume that every prompt needs flowers, stars, intense saturation, or lens flares.

## Quality Checklist

Before finalizing a prompt, verify:

- Is the main subject immediately understandable?
- Is the visual style consistent?
- Is the color palette intentional?
- Are lighting and depth clearly described?
- Does the composition guide attention toward the focal point?
- Do the details support the intended mood?
- Are unnecessary elements and conflicting instructions removed?

The final prompt should produce a cohesive visual scene with intentional color, cinematic depth, and a clearly defined atmosphere.