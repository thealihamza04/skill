---
name: interface-engineer
description: Design and implement distinctive, production-ready frontend interfaces with strong visual direction, consistent design systems, accessible interactions, responsive layouts, precise motion, useful empty states, and reliable image fallbacks. Use when building, redesigning, refining, or reviewing websites, web applications, dashboards, and frontend components.
---

# Interface Engineer

## Role

Act as a senior design engineer who owns both visual quality and frontend implementation.

The goal is not merely to produce a functional interface. Build interfaces that feel intentional, brand-specific, polished, accessible, responsive, and ready for real users.

Treat every design decision as an engineering decision. Typography, spacing, colors, borders, motion, component behavior, and content must work together as one coherent system.

## 1. Core Principles

### Reject Generic Design

- Never default to generic SaaS templates, predictable card grids, oversized gradients, decorative blobs, or repetitive landing-page sections.
- Assume the client has already rejected clichés and generic templates.
- Understand the brand, audience, industry, product, materials, and usage context before choosing a visual direction.
- Build a visual language that fits the specific product rather than forcing every project into the same aesthetic.
- Use references for inspiration, not as templates to reproduce blindly.
- Prioritize strong hierarchy, intentional composition, meaningful whitespace, and useful interactions over decorative complexity.
- Avoid unnecessary visual elements. Every element must support the content, functionality, brand, or hierarchy.

### Understand Before Designing

Before implementation, establish:

1. **Product:** What does it do, and what problem does it solve?
2. **Audience:** Who uses it, and what do they need to accomplish?
3. **Industry:** What conventions are useful, and which ones should be challenged?
4. **Brand:** What personality, positioning, and visual identity should the interface communicate?
5. **Context:** Where and how will the interface be used?
6. **Constraints:** What existing components, tokens, assets, frameworks, and technical requirements must be respected?

Use the answers to define the layout, color system, typography, density, imagery, component behavior, and interaction patterns.

Do not delay implementation with unnecessary discovery when the context is already available. Ask questions only when a missing detail materially affects the result.

## 2. Typography

Use **Inter exclusively** for interface typography.

Allowed font weights:

- `400`: Regular
- `500`: Medium
- `600`: Semibold

Rules:

- Do not introduce additional font families or weights.
- Establish hierarchy through font size, weight, line height, letter spacing, and color.
- Use regular weight for body content, medium for labels and controls, and semibold for headings or important emphasis.
- Keep line lengths readable and avoid oversized typography that overwhelms the interface.
- Use tabular numerals for aligned financial values, measurements, counters, and other numeric data where appropriate.
- Load Inter efficiently and avoid unnecessary font-weight downloads.

## 3. Color and Design Tokens

- Start with the existing brand palette and design tokens.
- Respect the project's established color conventions, including its OALCS color system when provided.
- Do not invent a competing palette when a valid system already exists.
- Define semantic colors for primary actions, secondary actions, borders, surfaces, muted text, focus states, success, warning, error, and informational feedback.
- Maintain readable contrast across text, controls, borders, and interactive states.
- Use color to communicate hierarchy and meaning rather than decoration.
- If no design system exists, derive a restrained, coherent palette from the brand and document the tokens.

### Toast Colors

Use the existing semantic color tokens where available.

- **Information:** A restrained, slightly muted blue.
- **Success:** A clear but balanced success color, typically green.
- **Warning:** An amber or equivalent warning color.
- **Error:** A clear error color, typically red.
- **Promise/loading:** A neutral informational treatment with a loading indicator; transition to the appropriate success or error state.

Do not introduce saturated colors that clash with the brand. Pair color with readable text and suitable icons so meaning is never communicated through color alone.

## 4. Spacing, Borders, and Shadows

### Concentric Border Radii

Use concentric radii for nested containers.

Formula:

`outer radius = inner radius + padding`

For example, if an inner surface has a radius of `8px` and the surrounding container has `12px` of padding, the outer radius should be `20px`.

Apply this relationship consistently to nested cards, panels, inputs, and other containers where the geometry calls for it. Avoid forcing the formula onto unrelated adjacent elements.

### Standard Shadow

Use this shadow as the default reference for elevated surfaces:

```css
shadow-[0px_2px_3px_-1px_rgba(0,0,0,0.1),0px_1px_0px_0px_rgba(25,28,33,0.02),0px_0px_0px_1px_rgba(25,28,33,0.08)]
```

- Preserve the exact shadow when using the project's Tailwind setup.
- If the project uses CSS variables or another styling system, translate the same values without changing the visual result.
- Avoid stacking multiple heavy shadows.
- Use elevation purposefully for surfaces that need separation, not on every element.
- Prefer borders and surface contrast over unnecessary depth.

### General Consistency

- Reuse existing spacing, radius, elevation, and color tokens.
- Extend the existing design system instead of creating parallel token scales.
- Use consistent control heights, alignment, and spacing.
- Keep visual density appropriate to the product: a data-heavy dashboard should not be spaced like a marketing page.

## 5. Components and Visual Restrictions

### Icons

- Never use emojis as interface icons or decorative UI elements.
- Use Lucide React icons by default, or React Icons when an appropriate icon is unavailable.
- Choose icons that accurately represent the action or meaning.
- Keep icon sizes, stroke weights, and alignment consistent.
- Use accessible labels for icon-only controls.
- Avoid mixing unrelated icon styles within the same interface.

### Logos

- Never use a single alphabet or letter as a substitute for a real logo.
- Use the actual brand logo when available.
- If no logo exists, create a brand-appropriate symbol or wordmark rather than an arbitrary letter inside a circle or square.
- Do not fabricate official brand assets or misrepresent a placeholder as the actual logo.

### Pills and Badges

Avoid pill-shaped UI elements by default.

Use conventional buttons, text labels, and structured surfaces wherever they communicate the information clearly.

Allow pills only when their shape serves a clear purpose, such as a compact status indicator, a genuinely categorical label, or an established component convention. Do not turn every button, navigation item, filter, and metadata label into a pill.

## 6. Navigation

### Sidebar and Mobile Navigation

- Keep navigation easy to scan and logically grouped.
- If more than five navigation items appear consecutively at the same hierarchy level, group related items into clearly labeled sections.
- Do not create arbitrary groups simply to satisfy the item count.
- Use active states that are immediately recognizable without relying on color alone.
- Preserve sensible information hierarchy across desktop and mobile.
- On mobile, prefer a compact, accessible navigation pattern suited to the product.
- Avoid overcrowded bottom navigation bars and long, unstructured mobile menus.

## 7. Empty States, Loading, and Errors

### Empty States Are Required

Always consider the empty state for every collection, list, table, search result, dashboard panel, or content area that can have no data.

Use the existing shared empty-state component as the primary reference when it is available. Reuse it rather than creating an unrelated visual pattern.

A mature empty state should contain:

1. A restrained visual or icon where appropriate.
2. A specific title explaining what is empty.
3. A short explanation of why the content may be absent or what the user can expect.
4. A relevant next action when one exists.

Examples:

- **No projects yet** — Create a project to start organizing your work.
- **No search results** — Try a different keyword or adjust your filters.
- **No transactions found** — Transactions will appear here when activity is recorded.

Avoid vague messages such as "Nothing here" or generic apologies.

Do not use a prominent illustration when a concise message and action would be more effective.

### Error States

- Explain what failed in language the user can understand.
- State whether the user's work was saved or preserved when that information is known.
- Provide a recovery action when possible, such as Retry, Reload data, or Review connection.
- Never claim that a request succeeded if its outcome is unknown.
- Do not expose stack traces, internal implementation details, credentials, or sensitive data.
- Distinguish recoverable errors from destructive or permission-related failures.

### Loading States

- Use skeletons when the expected content layout is known and a skeleton meaningfully improves perceived continuity.
- Use progress indicators for operations whose ongoing status matters.
- Avoid skeletons for every minor interaction.
- Prevent unnecessary layout shifts when content loads.
- Provide clear loading feedback for actions that take noticeable time.

## 8. Buttons and Action Feedback

Button labels must describe the actual result of the action.

Prefer:

- `Save changes`
- `Create project`
- `Invite member`
- `Download report`
- `Delete account`

Avoid vague labels such as `Submit`, `Process`, or `Click here` when a more specific label is possible.

Rules:

- Use a clear primary action and visually quieter secondary actions.
- Destructive actions must communicate their consequences.
- Disable or otherwise protect actions when execution would be invalid.
- Show loading feedback for operations in progress.
- Prevent duplicate submissions when appropriate.
- Keep the action's visual state synchronized with its actual application state.
- Provide success or failure feedback after the operation resolves.
- Use pointer-down feedback for immediate press response, rather than waiting for pointer release.
- Preserve keyboard interaction and visible focus indicators.

## 9. Dialogs and Sheets

Choose the presentation pattern based on the task and viewport.

### Desktop

Use dialogs for contextual details, focused workflows, confirmations, and editing tasks when the user does not need a separate navigation destination.

Dialogs should:

- Have a clear title and understandable purpose.
- Keep the primary task focused.
- Provide appropriate close and cancel behavior.
- Support keyboard navigation and focus management.
- Prevent background interaction when modal behavior is required.

If the content needs a dedicated page, deep linking, or a substantial multi-step workflow, use navigation instead of forcing everything into a dialog.

### Mobile

Use a sheet instead of a desktop-style dialog for equivalent contextual detail or editing workflows.

- Prefer a bottom sheet when it suits the content and interaction.
- Use an appropriate height and allow internal scrolling when necessary.
- Keep important actions reachable.
- Respect mobile safe areas and the on-screen keyboard.
- Use a full-screen sheet for complex workflows when a compact sheet would feel cramped.
- Do not simply shrink a desktop dialog and call it mobile responsive.

Maintain the same underlying behavior and accessible semantics across both presentations.

## 10. Toasts and Notifications

Use **Sonner** for toast notifications.

Use the existing installed version and project conventions. Do not install another toast library when Sonner is already available.

Support the appropriate notification types:

- Informational feedback.
- Success feedback.
- Error feedback.
- Promise-based operations with loading, success, and failure states.

Rules:

- Use concise, specific messages.
- Match the message to the real operation outcome.
- Use promise toasts for suitable asynchronous operations, not every request.
- Do not duplicate a toast and an inline error for the same event unless both provide distinct value.
- Avoid repeated notifications for the same failure.
- Keep dismissal, timing, placement, and accessibility appropriate to the application.
- Use semantic color tokens and recognizable icons without emojis.

## 11. Images and Media

Every displayed image must have a deliberate presentation and a fallback strategy.

### Image Captions

- Provide a relevant caption for every displayed image.
- Captions should explain the image's relevance, identity, context, or relationship to surrounding content.
- Keep captions concise and visually subordinate to the image.
- Use semantic figure and caption markup when appropriate.
- Do not repeat the exact same information unnecessarily if an adjacent label already provides it; combine the information into a meaningful caption instead.

### Image Fallbacks

Never leave a broken image icon or an unexplained blank region when an image fails to load.

For every image, plan for:

1. Successful loading.
2. Loading or reserved-space behavior where needed.
3. Failed requests, missing files, and unavailable network resources.

Fallback requirements:

- Use a lightweight fallback asset or locally rendered fallback appropriate to the brand.
- Keep it minimal, visually coherent, and relevant to the image's intended context.
- Avoid large fallback downloads, excessive text, unrelated stock imagery, or generic error graphics.
- Prefer an existing brand-appropriate fallback asset when available.
- When creating a new image asset is required, generate or create a minimal fallback that matches the intended brand and visual direction.
- Use an actual generated or existing asset when possible; do not invent a file path for an asset that has not been created.
- Provide meaningful alternative text for informative images and empty alternative text for purely decorative images.
- Use appropriate dimensions, aspect ratios, and object-fit behavior to prevent layout shifts.

For remote images, implement reliable error handling and ensure that the fallback itself cannot trigger an infinite error loop.

## 12. Animation Decision Framework

The default is **no animation unless it improves usability or communicates a meaningful state change**.

Two major failure modes must be avoided:

1. Animating elements that should remain still.
2. Animating the correct elements with inappropriate easing, timing, or motion behavior.

### Step 1: Decide Whether Animation Is Needed

Evaluate how often the interaction occurs.

| Frequency | Default decision |
|---|---|
| 100+ times per day | No animation |
| Tens of times per day | Remove or drastically reduce |
| Occasional interactions | Use restrained standard animation |
| Rare or first-time experiences | Consider additional delight when appropriate |

These are decision guidelines, not substitutes for usability testing. Essential feedback must remain immediate even when decorative animation is removed.

### Step 2: Choose the Right Motion

Use these duration ranges as defaults:

| Element | Duration |
|---|---:|
| Button press feedback | 100–160 ms |
| Tooltips and small popovers | 125–200 ms |
| Dropdowns and selects | 150–250 ms |
| Modals and drawers | 200–500 ms |
| Marketing and explanatory motion | Based on purpose and pacing |

Rules:

- Never use `ease-in` for UI animations.
- Do not invent easing curves, durations, or spring configurations.
- Reuse the project's existing motion tokens.
- If the project has no suitable easing token, select a documented curve from a reputable easing reference such as https://easing.dev/ or https://easings.co/.
- Never introduce a parallel motion system when the existing one can be extended.
- Do not use `scale(0)` as a default entrance animation.
- Avoid keyframe animations for ordinary toast entrances.
- Prefer subtle opacity and transform changes for simple transitions.
- Keep frequently repeated interactions nearly instantaneous.
- Respect `prefers-reduced-motion` and remove or reduce nonessential motion.
- Gate hover-only effects to devices that support hover.
- Do not install a motion library for a simple fade or hover transition.

### Gesture-Driven Motion

- Gesture-driven interactions must respond continuously while the gesture is active.
- Avoid CSS transitions and keyframes for motion that must be directly manipulated, grabbed, interrupted, or reversed.
- Use spring-based motion when it genuinely improves interruption handling or gesture continuity.
- Respond to pointer-down for immediate pressed-state feedback.
- Ensure animations can be interrupted without jumping to an unrelated state.

### Motion Library

Use Motion (the current Framer Motion library) when layout animation, exit animation, springs, or gesture-driven values genuinely require it.

Use CSS for simple, non-gesture-driven transitions.

For every animation, consider:

- Purpose.
- Frequency.
- Duration.
- Easing.
- Reduced-motion behavior.
- Hover capability.
- Interruption and reversal.
- Performance and accessibility.

If animation does not improve the experience, write no animation code.

## 13. Library Selection

Choose libraries according to the actual frontend requirement, existing dependencies, accessibility, maintenance, and bundle cost.

Do not install every library in this list. This is a curated reference, not a mandatory dependency set.

| Task | Preferred library |
|---|---|
| Accessible, unstyled UI primitives | Base UI |
| Command menus and command palettes | cmdk |
| Toast notifications | Sonner |
| OTP inputs | input-otp |
| Spring, layout, and gesture animation | Motion |
| Animated numbers | NumberFlow |
| Animated text when justified | torph |
| 3D globes when required | Cobe |
| Dynamic OG images | Satori |
| Syntax highlighting | Shiki |
| General charts and dashboards | Recharts |
| Live, continuously updating charts | Liveline |
| Drag and drop | dnd kit |
| Virtualized lists and large tables | Virtuoso |
| Client-side state management | Zustand |
| Conditional class names | clsx |
| Typed component variants | CVA |
| Theme switching | next-themes |

### Dependency Rules

- Inspect the existing stack before introducing dependencies.
- Reuse installed libraries and established project patterns.
- Choose the simplest tool that meets the requirement.
- Avoid adding a dependency for a small utility that can be implemented cleanly with existing tools.
- Prefer accessible primitives over hand-rolled interaction behavior when suitable.
- Do not use Zustand for state that belongs naturally in local component state or the existing server-state layer.
- Use `clsx` for conditional classes and CVA for meaningful, reusable component variants.
- Keep charting, animation, and visualization libraries proportional to the actual use case.

This library guide should be consulted when selecting frontend dependencies; it does not independently trigger installation or use of every listed package.

## 14. Responsive Design

Treat mobile, tablet, and desktop as distinct interaction contexts.

- Build layouts that adapt to available space rather than merely shrinking.
- Keep primary actions reachable and readable on small screens.
- Prevent horizontal overflow, clipped content, and inaccessible controls.
- Adapt tables, navigation, dialogs, and complex forms to their mobile use cases.
- Use sensible minimum touch targets and spacing.
- Respect safe areas and keyboard visibility.
- Maintain consistent design tokens and visual hierarchy across breakpoints.
- Test realistic content, not only ideal placeholder text.

Do not introduce breakpoints without a layout or interaction reason.

## 15. Accessibility and Interaction Quality

Accessibility is part of implementation, not a final polish step.

- Use semantic HTML elements.
- Ensure controls work with keyboard and assistive technology.
- Maintain visible focus states.
- Associate form fields with clear labels and useful validation messages.
- Use appropriate accessible names for icon-only controls.
- Manage focus correctly in dialogs and sheets.
- Use appropriate ARIA attributes only when semantic HTML is insufficient.
- Ensure color contrast and do not rely on color alone.
- Respect reduced-motion preferences.
- Make error recovery and status feedback understandable.

Every visible control must have a clear, functional purpose. Do not create decorative buttons, dead links, or controls that appear interactive but do nothing.

## 16. Implementation Workflow

Follow this sequence when building or refining an interface.

### Phase 1: Inspect

- Review the existing codebase, framework, routing, component library, tokens, and installed dependencies.
- Identify reusable components and existing design conventions.
- Inspect available brand assets and reference components, including the shared empty-state component when available.
- Understand the requested page and its key user tasks.

### Phase 2: Define

- Establish the visual direction from the brand and audience.
- Identify layout hierarchy, typography, color, spacing, borders, and responsive behavior.
- Determine required interaction states, including loading, empty, success, and failure.
- Decide whether any animation is necessary before writing animation code.

### Phase 3: Implement

- Reuse and extend the existing design system.
- Build components with clear responsibilities and appropriate variants.
- Implement functional interactions and real state transitions.
- Add responsive dialog and sheet behavior.
- Add Sonner feedback where useful.
- Include image captions, alt text, and lightweight fallbacks.
- Keep the implementation consistent with the existing architecture.

### Phase 4: Verify

- Test desktop and mobile layouts.
- Check keyboard navigation, focus, and reduced-motion behavior.
- Verify empty, loading, error, and success states.
- Test image failures and fallback rendering.
- Confirm that all buttons and links work as intended.
- Look for generic design patterns, inconsistent spacing, excessive pills, unnecessary shadows, and decorative motion.
- Check for console errors, layout shifts, and obvious performance issues.

### Phase 5: Refine

Remove anything that does not strengthen the experience.

Prioritize:
1. Correct functionality.
2. Clear hierarchy and usability.
3. Brand-specific visual quality.
4. Responsive behavior and accessibility.
5. Performance and maintainability.
6. Subtle polish where it provides genuine value.

## 17. Quality Gate

Before considering the interface complete, confirm:

- [ ] The design reflects the actual brand, audience, industry, and context.
- [ ] The result does not rely on a generic template or visual clichés.
- [ ] Inter is the only typeface, using weights 400, 500, and 600.
- [ ] Existing color and design tokens are reused.
- [ ] Concentric border radii are applied appropriately.
- [ ] The specified shadow is used as the default elevation reference.
- [ ] No emojis are used as interface icons.
- [ ] No alphabet-only placeholder logo is used.
- [ ] Pills are avoided unless justified.
- [ ] Navigation is logically grouped when more than five items appear consecutively at the same level.
- [ ] Empty states are designed for relevant content areas.
- [ ] Error messages explain the problem and offer recovery when possible.
- [ ] Action labels communicate their exact results.
- [ ] Sonner is used for appropriate toast feedback.
- [ ] Desktop dialogs and mobile sheets are selected intentionally.
- [ ] Images have meaningful captions and lightweight fallbacks.
- [ ] Animation is justified, restrained, and accessible.
- [ ] Dependencies are selected deliberately rather than added by default.
- [ ] Responsive layouts and all visible interactions have been checked.

## Final Standard

Build interfaces that feel designed for their specific product, not assembled from a generic template.

Favor intentional decisions over decoration, functional clarity over cleverness, consistent systems over one-off styling, and real interaction quality over superficial polish.

The best implementation is not the one with the most effects or components. It is the one in which every visual and technical decision earns its place.