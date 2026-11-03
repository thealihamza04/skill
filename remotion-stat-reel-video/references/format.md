# The stat-reel format

A short (≈20–26s) typographic brag reel: a portfolio collage opens, a few spoken-rhythm words build
up, then **numbers do the talking** (counters, badges, a giant ghost number), an arrow walks the
viewer to "your work", a search bar types the URL, the work explodes into a collage, and a logo
end card closes. Ported frame-by-frame from a 720×540 @ 60fps reference (`src/ReachReel/` in the
project where this skill was made is the first finished instance).

Everything below is measured on that **720×540 stage**. Build at that size and scale the stage
(×2 → 1440×1080, ×1.5 → 1080×810…). For 16:9 or 9:16 see "Other aspect ratios" at the end.

## The beats

| # | Beat | Ref. time | Len | What happens |
|---|---|---|---|---|
| 1 | **collageTitle** | 0.00–0.80 | 0.80 | 7 project shots scattered on lime; 3-line title at left: `line1` / `[stat + icon pill] line2` / **line3**. Text slides left (0→−150px, ease-in) and fades out 0.30–0.75; shots drift up and fade 0.45–0.78. |
| 2 | **words (light)** | 0.80–2.60 | 1.80 | One word at a time, centered, hard swaps at 0.80 / 1.20 / 1.60. Each word: opacity 0.35→1 in 0.12s, scale 0.95→1.03 over 1s. Two white squiggles (top-left, bottom-right) draw on 1.1–1.7s and sway. |
| 3 | **words (dark)** | 2.60–4.50 | 1.90 | Hard cut to teal. 0.1s empty, then words at 2.70 / 3.20 / 4.00; last word larger (66 vs 57). Dark-teal squiggles (top-right, bottom-left) draw 2.6–3.3. |
| 4 | **cursorCounter** | 4.50–6.40 | 1.90 | `N{suffix} label` counts up 4.5–5.3 (ease-out cubic) while a text caret sweeps left→right across the line (4.5–5.25), blinks at the end (to 5.5), walks back to the end of the number (5.5–5.85), then widens leftwards into a rounded box behind the number (5.85–6.15); number turns accent. Whole line scales 0.62→1 over the beat. |
| 5 | **ghostCounter** | 6.40–9.65 | 3.25 | Giant number (470px, ghost color) counts 0→N 6.4–7.2; over it a small bold word fades in **letter by letter in random order** 7.25–7.95. Hard cut at 8.40 to word 2 (48px), at 9.00 to word 3 (52px), each fading 0.4→1 in 0.12s. |
| 6 | **badgeCounter** | 9.65–12.20 | 2.55 | Badge `N+` with a label. Stepped count: climb (9.65→10.2), hold, climb (10.35→10.85), hold, climb (11.0→11.5), hold to 11.75, then the label collapses and the number **drops** quickly (ease-in) to 12.15. Badge font 28→60→60→26. |
| 7 | **badgeSentence** | 12.20–13.25 | 1.05 | Two centered lines, 28px: `lead [badge N+] tail` / `line2`. Badge number snaps from `from` to `to` in 0.18s. Scale 0.93→1.04. |
| 8 | **arrowWords** | 13.30–17.60 | 4.30 | "Check out" fades in (50px). 13.85: an arrow is pulled out of its right side; the text rides off the left edge (13.85–14.35) while the arrow's tip settles at x≈205. Then 2-word phrases appear right of the arrow (x=272, 51px) at 14.70 / 15.90 / 17.00, words staggered 0.08s, each fading to 0.35 in its last 0.1s. |
| 9 | **searchCollage** | 17.60–20.00 | 2.40 | Everything slides left + blurs out while the background crossfades lime→teal (17.62–18.35). A search pill (76px tall, pale) rises and scales in, types the URL (17.8–18.5, each char 0.3→1), holds, deletes it (18.75–19.1, ease-in), collapses to a circle and fades (19.2–19.5). From 18.9, 8 shots pop in from the centre outward on teal, staggered, the largest one in the middle last (19.55). |
| 10 | **thanks** *(optional)* | 20.00–21.80 | 1.80 | "Thanks For watching", letters fade in random order over 0.95s; first word in accent. Scale 1.06→0.9. Cut it and the end card moves up. |
| 11 | **endCard** | 21.80–25.32 | 3.52 | Near-white. The logo mark assembles (0.45s, parts fly in), then the wordmark wipes open to the right of it (22.45–22.95). 23.2–24.8 a black overlay fades the whole frame to black; 0.5s of black. |

Total with every beat: 25.32s (1519 frames @ 60). Without `thanks`: 23.52s.

## Layout & type (720×540 stage)

- Font: a geometric grotesque with double-storey `a`, single-storey `g`. Figtree (Google Fonts) is
  the free match; weights 300/500/600/700, italic 300 for a light wordmark half.
- Sizes: title lines 62 / 51 / 70; word beats 61 (light), 57 & 66 (dark); counter line 45;
  ghost number 470 / ghost word 32; badge 28→60; sentence 28; arrow words 50–51; pill text 22;
  wordmark 60, mark 60×40.
- Intro shots (x, y, w, h): (37,0,118,90) (356,0,143,104) (617,40,103,98) (219,117,86,67)
  (497,208,173,135) (559,421,161,119) (360,474,123,66). Title left edge x=58, line centres
  y=268 / 355 / 440.
- Outro collage (x, y, w, h, enter s): (−10,−10,188,114,18.90) (548,447,172,93,19.00)
  (159,465,232,75,19.10) (−10,383,99,113,19.10) (372,−10,177,72,19.25) (634,90,96,218,19.30)
  (86,200,136,106,19.40) (259,130,316,247,19.55 — the hero).
- Squiggle paths (light): `M -20 40 C 40 70, 90 105, 140 102 C 190 98, 215 50, 222 -10` and
  `M 740 440 C 690 480, 640 505, 590 505 C 530 505, 480 478, 420 478 C 360 478, 325 500, 322 560`,
  white, 7px, round caps. Dark: `M 380 -10 C 420 40, 470 45, 530 35 C 600 22, 660 20, 740 45` and
  `M -20 540 C 10 505, 60 490, 110 505 C 140 515, 150 530, 155 545`, 6px.
- Arrow: 2.6px stroke, round caps, chevron head ≤ 11px, at y=270.

## Palette (reference)

| Token | Hex | Use |
|---|---|---|
| lime | `#ecfaa8` | light background |
| ink | `#004449` | text on light, dark background, badges |
| cream | `#f2ffc3` | text on dark, badge text |
| ghost | `#d2e59c` | giant ghost number |
| accent | `#dcf36a` | highlighted number, first word of the thanks line |
| pill | `#eef9b8` | search pill |
| squiggleDark | `#1f5c60` | squiggles on teal |
| end | `#fcfcfc` | end-card background |

To rebrand, keep the structure: one pale background, one deep ink that doubles as the dark
background, a cream for text on dark, a ghost just darker than the background, one accent.

## Copy rules

1. **Every number is a verified fact** (GitHub, portfolio, analytics the user shows you). Never
   invent views, followers, clients or awards to fill a slot. When a beat has no true number,
   pick a different true one (repos, shipped apps, projects, years, contributions) or drop the
   beat. Leave a comment next to the copy saying where each number came from.
2. **Read it as speech**: beats 2–3 form a sentence ("Hi / I'm / Building … I / have / built"), beat
   4's label continues it ("22+ public repositories"), beat 5 reads as one phrase ("4 · Shipped ·
   to · Production"), beat 8 reads "Check out → My latest → Case studies → from here".
3. One word per swap in beats 2–3 (≤ 10 characters); beat-8 phrases ≤ 2 words.
4. The intro stat and the counters should agree with each other (same number, same source).
5. Shots: real project screenshots or mockups, landscape. 7 for the intro, 8 for the outro (reuse
   is fine; the hero slot gets the best one).

## Sound

The reference's own soundtrack isn't reused. Default plan: one music bed (fade in 10 frames, fade
out the last 1.5s) plus a few SFX on structural moments, all ≤ 0.45 volume:

| Moment | Time | SFX character |
|---|---|---|
| cut to dark | 2.55 | swoosh |
| box snaps behind the number | 5.88 | digital snap |
| ghost word starts | 7.25 | soft highlighter |
| arrow pulled out | 13.85 | air |
| transition to dark | 17.60 | sub-swoosh |
| collage pops | 18.90 | soft pulse |
| logo assembles | end-card start + 0.05 | chime |

## Validation (applies to both builds)

Render stills at the middle of each beat at ¼–½ scale and tile them into a sheet; check for:
clipped text (labels are the usual culprit at their largest size), numbers matching the copy,
the caret/box landing exactly on the number, the arrow tip not touching the phrase, the pill URL
fully visible, the wordmark centred with the mark. If you're porting from a reference video,
extract the reference frames at the **same timestamps** and compare them side by side; text width
is the quickest tell for a wrong font size.

Useful still times (s): 0.1, 1.8, 4.2, 6.3, 7.8, 9.3, 11.6, 12.6, 14.1, 15.2, 18.5, 19.9,
(21.4 thanks), end-card start + 1.2.

## Other aspect ratios

The stage is designed at 4:3. For 16:9, keep a 720×540 stage centered on a 960×540 canvas and
extend the backgrounds full-bleed (collage shots can use the side margins). For 9:16, use a
540×960 stage: stack the intro title under the shots, drop type sizes ×0.85 for lines wider than
480px, and move the arrow to y=480 with phrases below it. Always re-check the stills.
