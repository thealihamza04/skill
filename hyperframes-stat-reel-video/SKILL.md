---
name: hyperframes-stat-reel-video
description: Plan, generate and validate "stat reel" brag videos as HyperFrames HTML compositions — a ~20–25s typographic portfolio reel where numbers do the talking. A project-shot collage opens with a title and stat pill, one-word beats swap on light then dark backgrounds with drawn squiggles, a counter is swept by a text caret that turns into a highlight box, a giant ghost number sits behind a letter-scattered word, a badge counter climbs in steps, an arrow pulls the viewer to "my latest case studies", a search bar types the portfolio URL, the work bursts into a collage, and a logo end card fades to black. A bundled generator turns one reel.json into a HyperFrames project (one sub-composition per beat, seek-safe GSAP timelines, framework-owned audio, bundled Figtree) that passes `hyperframes check` with zero findings and matches the measured 60fps reference. Use it whenever someone wants a brag/portfolio/agency stats reel, a "we reached X views / Y followers / Z clients" promo, a personal-brand milestone video, a video "like ReachReel" or "like this Behance / orbix studio reel", or to rebuild a similar counter-and-collage reference in HyperFrames / HTML / GSAP rather than React — even if they never say "stat reel". For the same format in Remotion, use remotion-stat-reel-video.
---

# Stat reel (HyperFrames)

A proven format, ported frame by frame from a 720×540 @ 60fps reference and rebuilt for a real
user (`src/ReachReel/` is the Remotion twin). Here the output is a HyperFrames project generated
from one config file; you write **copy and assets**, not motion.

```
collage + title → Hi / I'm / Building → I / have / built → 22+ public repositories (caret → box)
→ 4 · Shipped · to · Production → [7+] projects built → Taking [4+] products from…
→ Check out ⟶ My latest · Case studies · from here → 🔍 url → collage → (Thanks) → logo · fade
```

`references/format.md` is the source of truth for every beat: timing, sizes, palette, copy rules,
sound and the still-frame checklist. Read it before planning. Run the CLI as the version the
scaffold pins (`npx -y hyperframes@<pin> …`; bare `npx hyperframes` below is shorthand). Read
`/hyperframes-core` before extending the generator.

## Workflow

### 1. Brief — verified facts only
1. Collect the subject's **true** numbers and where each came from: GitHub (repos, stars,
   contributions), the portfolio (shipped apps, case studies), analytics they show you. **Never
   invent views, followers, clients or awards to fill a slot.** No true number for a beat → use
   another true one, or switch the beat off. Record each source in `reel.json`'s `_sources`.
2. Brand: name/wordmark, logo (an SVG or a mark you can rebuild as shapes), palette (or keep
   the reference lime/teal), the URL the search bar should type, 7–8 landscape project shots.
3. Sound: a music bed and up to 7 SFX (defaults in `format.md` § Sound), or none.

### 2. Copy table — one row per beat
Fill the table in `format.md` order and read it aloud as one piece. Beats 2–3 are one sentence
("Hi / I'm / Building … I / have / built"), beat 4's label continues it, beat 5 reads as a phrase
("4 · Shipped · to · Production"), beat 8 reads "Check out → My latest → Case studies → from
here". Keep swap words ≤ 10 characters and arrow phrases ≤ 2 words. Show the table to the user
before generating if they're around.

### 3. reel.json
Copy `assets/examples/reel.json` (the finished Ali Hamza reel) next to the project and edit it:

| Key | What it sets |
|---|---|
| `scale` | stage multiplier: 720×540 × scale (2 → 1440×1080) |
| `fps` | root frame rate (default 60, the reference's) |
| `baseDir` | where relative asset paths resolve from (relative to reel.json) |
| `beats` | switch any beat off, e.g. `{"thanks": false}`; later beats move up |
| `palette` | lime, ink, cream, ghost, accent, pill, squiggleDark, end, brand (wordmark dot) |
| `images` | 8 shots: first 7 = intro, all 8 = outro collage (index 7 is the hero) |
| `collageTitle` … `endCard` | the copy per beat (see the example); `icon` is `code`, `eye`, `none` or an inline `<svg>` |
| `badgeCounter.steps` | 8 values: climb, hold, climb, hold, climb, hold, then the drop |
| `badgeSentence.extraHold` | seconds added so the sentence clears HyperFrames' readability floor (default 0.3) |
| `endCard.logoSvg` | inline SVG; parts with `data-dx/dy/rot/delay` fly in, parts with `data-at` snap on (see the AH mark in the example). Omit for a neutral placeholder |
| `music`, `sfx` | `{src, gain}`; each SFX is `{src, beat, at, volume}` with `at` in beat-local seconds |

### 4. Generate
```bash
HYPERFRAMES_SKIP_SKILLS=1 npx -y hyperframes init <project> --non-interactive
python3 <skill>/scripts/build_reel.py reel.json --project <project>
```
It writes `index.html` (beat hosts + audio) and `compositions/beat-N-<name>.html`, and copies
fonts, images and audio into `assets/`. **Edit reel.json and rebuild; never hand-edit the
generated HTML.** A rebuild replaces it, including edits made in Studio.

### 5. Validate (details in `references/hyperframes-notes.md`)
- `npx hyperframes check`: the example passes with **0 errors, 0 warnings, 0 infos**. Keep it
  that way; the notes map each likely finding to its fix.
- `npx hyperframes snapshot --at <beat midpoints> --no-end --output stills`, tile them and
  look. The still times in `format.md` apply up to 12.2s; after that, add `extraHold` (0.3)
  and subtract any switched-off beats' lengths. Check: no clipped labels, numbers match the
  copy, caret/box land on the number, the URL is fully visible, the wordmark is centred.
- Porting from a reference video? `snapshot --against <reference.mp4>` saves its frames at the
  same times as a side-by-side sheet. Text width is the quickest tell for a wrong size.
- Draft render to check playback and sound: `npx hyperframes render --quality draft --fps 30
  --workers 2 -o draft.mp4`, then `ffmpeg -i draft.mp4 -af ebur128=peak=true -f null -`.
  The reference mix sits around −20 LUFS with peaks under −6 dBFS; report the numbers.
- Render the delivery file (`npx hyperframes render`, 60fps) only after the user approves.
  Say what you didn't verify (by ear, phone width).

## Rules

- **True numbers or no number.** This format exists to brag; a fabricated stat is the one
  failure that can't be fixed later. Keep `_sources` in reel.json current.
- **Don't fork the motion.** Every timing and size comes from the measured reference. If a
  user wants a beat to feel different, change the copy or switch the beat off. Change the generator
  only for a new capability, and re-run `check` and the stills afterwards.
- **Don't reuse someone else's brand.** When recreating a reference, keep its structure and
  rhythm, but use the user's name, logo, shots, URL and colours, never the reference's mark or claims.
- **One idea per beat**: one word per swap, no eyebrow labels or extra chrome beyond what the
  format has (pill, badges, caret box, search pill).
- **Undo means fully undo**: remove the config change, rebuild, and re-check.

## Bundled files

| Path | What it is |
|---|---|
| `scripts/build_reel.py` | reel.json → `index.html` + one sub-composition per beat; copies assets; seeded scatter order; driver tweens for counters, caret, typing, arrow and squiggle sway |
| `assets/examples/reel.json` | The finished Ali Hamza reel (verified facts, AH mark, no thanks beat), validated end to end |
| `assets/fonts/` | Figtree variable (300–900) + 300 italic, woff2, SIL OFL 1.1 |
| `references/format.md` | The format: beats, timings, layout, palette, copy rules, sound, validation (shared with the Remotion skill) |
| `references/hyperframes-notes.md` | How the generator stays seek-safe, the project layout, `check` findings → fixes, extending a beat |

Needs Python 3, ffmpeg/ffprobe on PATH, and Node.js 22+ for HyperFrames.
