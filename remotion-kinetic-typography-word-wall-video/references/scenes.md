# Scene types and motion

All motion lives in `assets/engine/KineticWordWall.tsx`. This file explains what each scene does,
its limits, and how to extend it, so you can configure it rather than rewrite it.

Geometry is in a 736×414 reference space scaled by `S = min(width/736, height/414)`, so 1920×1080,
1080×1080 and 1080×1920 all work. Every value is a pure function of the frame, so renders are
seek-safe and repeatable.

## Contents
1. typed, 2. wall, 3. statement, 4. wordmark, 5. custom end cards, 6. palette and type,
7. porting a reference video

---

## 1. `typed`: the setup line
- Words **hard-cut on** at `wordOn` frames (no fade). The line re-centers as it grows.
- Before each new word: a −2px ease-in dip. In the last 7 frames: an accelerating left drift
  (−0.5 … −19px), so the cut into the wall happens at peak velocity.
- Minimum frames: last `wordOn` + 2 (hold) + 7 (run). The planner computes this.
- One typed line per act. 2–6 words reads best.

## 2. `wall`: the word wall
- A full-bleed field of rows in `wallInk` on `wall`, with **one** centered serif highlight in
  `highlight`. Each segment is a **hard cut** to a new seeded arrangement with the next word.
- Inside a segment the whole wall drifts left about 15px on a fast–slow–fast curve, resampled to
  the segment's length. So shorter segments move faster: different durations also mean different speeds.
- **Readability: ≥ 7 frames (0.29s) for 1–2 words at 24fps.** 3–4 frame flashes are glimpsed,
  not read. Use them only if the user wants a subliminal montage.
- **Vary durations.** Equal lengths read as mechanical. Default shape: two quick, three slowing,
  accelerating, last held. With `distinct`, no two are equal. Hold the last word longest: it
  hands off to the statement.
- Background rows are deterministic (seeded). Changing `vocab` changes every arrangement.

## 3. `statement`: the payoff
- `lead` (sans) + `accent` (serif, accent color) + `tail`. Lands loose and right, then tightens
  to center over about 19 frames (gap and tracking shrink geometrically). Then it holds.
- ≥ 20 frames; 28–42 typical. In a long video, earlier acts' statements can be shorter.

## 4. `wordmark`: the two-group logo reveal
- A bar over the center narrows while `left` and `right` slide outward from under its edges
  (each clipped to its side). One curve drives everything: p = 1 − 0.765^f. It settles in
  about 15 frames.
- `slant` (degrees) turns the bar into a slash (≈ 28° for a "/"). `finalBar` (px @736) keeps a
  thin bar as part of the mark; 0 makes it vanish at `hideAt` (default 15). `gap` is the final
  space between the groups.
- Use `fonts.display` / `displayWeight` / `displayCapRatio` to match the brand face.
- The whole mark is centered on the frame (not the bar), and its size auto-fits to ~84% of the
  frame width. So long names on portrait frames shrink instead of running off the edge.

## 5. `custom`: bespoke end cards (real logos)
When the user has a logo, rebuild it as vector shapes, not a placed PNG. It stays crisp, and its
parts can move independently:
1. Measure the logo image: find its grid or key edges, the colors (dominant-color histogram), and
   any accent shape (e.g. a 45° triangle).
2. Write a component (`useCurrentFrame()` is scene-relative) that draws it in SVG units and
   reveals it in the same motion language. The reference project's AH mark: a vertical bar
   narrows into the letter gap while the letters slide out, then the accent fold snaps on at the
   next beat (an `extraHits` entry).
3. Compare the final frame side by side with the source logo (aspect ratio, accent position)
   before calling it done.
4. Register it: spec `"end": {"kind": "custom", "ref": "Logo", "frames": 36, "extraHits": [15]}`,
   config `scenesFromTiming(SCENES, { Logo })`.

A trademarked third-party logo is fine for private practice; say so, and don't publish it.

## 6. Palette and type
- `wall` is one saturated brand color. `wallInk` is the **same hue, much darker**: the body
  recedes and the white serif highlight pops. Check the highlight at phone size.
- `paper` near-white, `ink` near-black. `accent` is usually the wall color.
- Sans for body (Inter / Inter Tight); a transitional serif for highlights and the accent
  (Source Serif 4). The contrast between the two is the look. Load them with `@remotion/google-fonts`.

## 7. Porting a reference video
If the user provides a video to recreate:
- `ffprobe` it, extract every frame, find hard cuts (`select='gt(scene,0.25)'`), and build contact sheets.
- Track motion numerically (ink bounding boxes per frame, frame differencing, offset alignment);
  don't eyeball it. Write the per-frame offsets as tables.
- Fit text sizes by comparing ink boxes of your render (scaled to the source size) against the
  source, and iterate until within 1–3px.
- Render to a **fresh** output directory each time. Re-rendering into an existing frames
  directory can leave stale PNGs, which once made a fix look like it hadn't worked.
