# Validation

Don't call a video done from reading code. Check rendered frames and rendered audio, and say
plainly what wasn't checked (by ear, at phone width).

Keep it light. These commands are sized for modest machines (`--concurrency=2`, scaled JPEG
stills, audio-only WAV renders). A full MP4 render happens once, at the end, when the user asks.

## 1. Types
```bash
npx tsc --noEmit
```

## 2. Picture: stills at the moments that matter
Use the "suggested stills" line that `plan_timeline.py` prints: the middle of every scene and wall
segment, plus the last frame. `contact_sheet.py` sizes the grid to fit them all and labels each tile
with its frame and what should be on screen (from timing.json).

```bash
npx remotion render <Comp> /tmp/<comp>-stills --frames=<f1>,<f2>,... \
  --image-format=jpeg --scale=0.25 --concurrency=2
python3 <skill>/scripts/contact_sheet.py /tmp/<comp>-stills /tmp/<comp>-sheet.jpg \
  --timing src/<Comp>/timing.json
```
Render into a **new** directory each time; stale files in an old one hide changes. Then look at
the sheet:
- The right word is up in each wall segment, readable, and the highlight centered.
- The typed line is complete before the cut. The statement has settled by its hold.
- The end card matches the brand (side by side with the source logo for a custom card).
- At phone size (scale the sheet to ~390px wide), the highlight word and statement still read.

## 3. Sound: two audio-only renders
```bash
npx remotion render <Comp> /tmp/<comp>-mix.wav   --codec=wav --concurrency=2
npx remotion render <Comp> /tmp/<comp>-music.wav --codec=wav --concurrency=2 --props='{"mute":"sfx"}'
python3 <skill>/scripts/check_audio.py /tmp/<comp>-mix.wav /tmp/<comp>-music.wav src/<Comp>/timing.json
```
For an SFX-only video (`music: null`), skip the music-only render and pass `none`:
`check_audio.py /tmp/<comp>-mix.wav none src/<Comp>/timing.json`.
Pass criteria:
| Check | Target |
|---|---|
| True peak | ≤ −1.3 dBTP |
| Integrated loudness | about −14 to −17 LUFS (report the number) |
| Every hit vs music | ≥ +3 dB target, ≥ +2 pass |
| Structural cuts vs kicks | within ±1 frame (±42ms at 24fps; the script fails beyond that); a consistent offset means nudge `trimBefore` |

Fix order for failures: a hot true peak → add the frame the script names to `music.duckFrames`; a quiet hit → raise its volume;
consistent beat offset → nudge `trimBefore`; then re-run both renders.

## 4. Report
Write the numbers into PLAN.md's Validation section, and tell the user what was verified and
what wasn't. Offer the final MP4 render:
```bash
npx remotion render <Comp> out/<Comp>.mp4 --concurrency=2
```
