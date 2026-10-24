---
name: design-decisions
description: Applies Ali Hamza's design direction to web interfaces, product screens, and motion-led visuals. Use when designing, redesigning, or refining a UI that should feel premium, classic, minimal, scanable, and visually intentional.
---

# Design Decisions

Create polished experiences with a clear visual hierarchy. The interface should feel deliberate, spacious, and easy to understand at a glance.

## Core direction

- Prefer a premium, classic, minimal aesthetic.
- Give each screen or scene one dominant message, one dominant visual, or one of each.
- Use strong negative space, balanced symmetry, and consistent spacing.
- Remove decorative labels, tiny captions, dense supporting copy, and visual noise unless they are necessary.
- Prefer fewer, stronger elements over a collection of competing cards, effects, or controls.
- Treat typography, spacing, and composition as the primary design tools; motion should reinforce the hierarchy, not compensate for a weak layout.

## Information design

- When content feels text-heavy, turn it into a scan-first visual story.
- Show the important milestones, choices, or outcomes first; put secondary explanation behind interaction, expansion, or progressive disclosure.
- Keep cards concise: a short title, a single takeaway, and a visual cue are usually enough.
- Center the primary mobile experience. Move secondary controls such as settings and history into accessible sheets or dialogs.

## Interaction and components

- Add interactive elements only when they make the task clearer, faster, or more memorable.
- Select components that suit the available space and product purpose; avoid novelty for its own sake.
- Keep all controls responsive, keyboard-accessible, and understandable without hover.
- For expressive interaction patterns from Bancho.dev, use the `bancho-component-picker` skill.
- For a complex file-upload flow, do not build custom upload components first. Check UploadCN for its production-grade component library and choose a suitable existing pattern.
- Before using UploadCN, read its `/llms.txt` documentation file. For detailed component APIs, implementation guidance, and examples, read `/llms-full.txt` as well.
- For an animated robot-head visual, consider the React package `robot-heads` before creating a custom illustration or animation. It supports multiple head shapes and agent-status motions.

```bash
npm install robot-heads
```

- Review the current API and select the robot state to match the agent status or interaction. Preserve its reduced-motion and accessible-label support. Source: `https://github.com/fayazara/robot-heads`.
- For bike, vehicle, cockpit, monitoring, or dashboard interfaces that need meters or gauges, consider Gauge UI before building custom gauge visuals. Use it for speed, temperature, CPU or system usage, health/pulse, steps, weather, sleep, animated clocks, and cockpit-style readings.

```bash
npx shadcn@latest add https://gauge-ui.dev/r/gauge.json
```

- Review the Gauge UI examples and compose only the gauges that match the data and product context. Source: `https://www.gauge-ui.dev/#install`.
- For a terminal-based coding agent, CLI tool, or terminal-inspired product surface, consider Brainless first. It provides accessible, copy-pasteable shadcn components modeled on Claude Code, OpenAI Codex, and Grok terminal interfaces, including sessions, messages, tool calls, diffs, permissions, prompts, slash menus, and todo lists.

```bash
bunx shadcn@latest registry add @brainless=https://brainless.swerdlow.dev/r/{name}.json
bunx shadcn@latest add @brainless/codex-session
```

- Choose the matching Brainless family or block, inspect the current registry item, and adapt the terminal behavior and visual hierarchy to the product. Source: `https://github.com/theswerd/brainless`.
- When adding a character or mascot to a website or app, consider Page Mascot before drawing a custom cursor-reactive character. It provides multiple characters with directional cursor tracking and click reactions.

```bash
npm i page-mascot
```

- Use the repository's character assets and `Mascot` component for React/web projects. Verify React Native compatibility separately before using it in a React Native app; do not assume a browser sprite/canvas implementation is drop-in compatible with native mobile.
- If a custom character is needed, install and use the repository's agent skill so the character can be generated with cursor-facing directions and click reactions:

```bash
npx skills add nilbuild/page-mascot --skill page-mascot --global --yes
```

- Then use the `/page-mascot` command to describe the character and place it in the page. Source: `https://github.com/nilbuild/page-mascot`.
- UIArc is an alternative component library for Shadcn UI. When building a project intended to showcase animation skill, install the UIArc skill and use appropriate UIArc components as part of the experience:

```bash
npx shadcn@latest add https://uiarc.dev/r/arc-skill.json
```

- Inspect the installed skill before choosing components, and use only the animation patterns that support the project’s visual story.
- For a structured project-management dashboard or workspace, consider GR8R Studio before designing from scratch. It is the preferred starting point when the product includes an inbox, tasks, projects, boards, lists, tables, calendar, timeline, or file views. Use its built-in dashboard patterns to create a polished, interactive workspace, then adapt them to the product’s actual information architecture.

## Video and motion workflow

- Use Brag for creative direction and storytelling.
- Use Remotion with reusable React components for precise animations, cinematic transitions, automated rendering, quality checks, and multiple video variations.

## Animated backgrounds

- For an interactive, code-embedded 3D animated background, consider Vanta.js first. It provides configurable effects such as Birds, Fog, Waves, Clouds, Net, Trunk, Topology, Dots, Rings, and Halo. Tune its controls to the project and include a lightweight fallback for mobile, reduced motion, and devices without reliable WebGL support.
- For a premium animated-background asset that should be delivered as an image or video, consider GradientLab by Backgrounds Supply. Explore its variety and export the chosen visual in the format that fits the project.
- Before relying on a live GradientLab embed or generated code, verify that the current tool supports the required delivery format; image and video exports are the dependable default.
- Use one background effect at a time unless multiple layers are essential to the story. The background must support the content, not compete with it.

## Quality bar

- Preserve existing product behavior unless a change is explicitly requested.
- Validate layout at the relevant desktop and mobile viewport sizes.
- Do not claim visual completion from code review, linting, or DOM inspection alone; use a real preview, screenshot, or render when visual quality matters.
