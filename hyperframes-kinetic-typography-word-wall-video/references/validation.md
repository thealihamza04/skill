# Validation

Check rendered pixels and rendered sound, not code. Say plainly what wasn't checked (by ear, phone
width). These commands are sized for modest machines: `--workers 2`, `--quality draft` while
validating. The delivery render happens once, at the end, when the user approves.

Run every command from the project directory. A scaffolded project pins the CLI version in its
`package.json`; use that version (`npx -y hyperframes@<pin> …`) so results are reproducible.

## 1. Static and browser audit
```bash
npx hyperframes check
```
`check` runs `lint` first, then one browser pass for runtime errors, layout, motion, contrast and
craft. **Target: 0 errors and 0 warnings.** The usual warnings and what they mean here:

| Warning | Fix |
|---|---|
| `line_unread` on a wall word | re-plan with the current planner (it applies the per-phrase floor: 3 words ≥ 26f); with explicit `frames`, raise that word |
| `line_unread` on the closing line | the statement is the last text: `statement.minFrames` ≥ 48 |
| `first_frame_empty` | `typed.firstWordAt: 0` |
| contrast on the wall body text | it should carry `data-layout-ignore` (generator does this); if you hand-edited, rebuild |
| `duplicate_audio_track` | rebuild, since the generator packs SFX into free tracks; check no SFX file has a silent multi-second tail |
| text "at 16px" / unstyled | an inline `style` was cut short. Rebuild, and in a custom fragment never put double quotes inside `style="…"` |
| `nested_structure_needs_subcomposition` | hand-edited index.html; rebuild |

A lint **error** switches off the browser audits (`0 samples`), so clear errors first. **Info**
notes are fine: the wall's background rows always overflow the frame on purpose (about one note per
wall scene and statement).

## 2. Picture: snapshots at the moments that matter
The planner prints the suggested stills as frames and as a ready `snapshot --at` list in seconds:
```bash
npx hyperframes snapshot --at 0.417,1.042,1.5,… --no-end --output stills
```
It writes `stills/frame-NN-at-<t>s.png` plus contact sheets. Look at them:
- The right word is up in each wall segment, readable, and the highlight centered.
- The typed line is complete before the cut; the statement has settled by its hold.
- The end card matches the brand; for a custom logo, snapshot a few frames inside its first 15
  frames to see the reveal animate, and compare the last frame with the source logo.
- At phone size (scale a sheet to ~390px wide), the highlight word and statement still read.

## 3. Sound: two renders and the checker
```bash
python3 <skill>/scripts/build_composition.py --timing timing.json --config video.json --project . \
  --mute sfx --out music-only.html
npx hyperframes render --quality draft --workers 2 --output renders/mix.mp4
npx hyperframes render --composition music-only.html --quality draft --workers 2 --output renders/music.mp4
python3 <skill>/scripts/check_audio.py renders/mix.mp4 renders/music.mp4 timing.json
```
Then **delete `music-only.html`** (`rm music-only.html`): while a second root composition sits in
the project, `check` fails with `multiple_root_compositions` and skips its browser audits. For
SFX-only videos (`music: null`), skip the music build and render and pass `none` instead of music.mp4.

| Check | Target |
|---|---|
| True peak | ≤ −1.3 dBTP |
| Integrated loudness | about −14 to −19 LUFS with SFX leading (report the number) |
| Every hit vs music | ≥ +3 dB target, ≥ +2 pass |
| Structural cuts vs kicks | within ±1 frame (±42ms at 24fps). A consistent offset means nudge `music.trimBefore`; "no kick here" means the cut falls in a break or fade (not scored). On the drop cut that's a wrong trim: re-run `analyze_music.py` and use the time where it says "kicks enter" |

Fix order: hot true peak → add the frame the checker names to `music.duckFrames` (unless it's the drop's `wallIn`: lower that SFX instead, `audio-sync.md` §5); a quiet hit →
raise its kit `volume` (≤ 3.98, else bake a louder file); consistent beat offset → nudge
`music.trimBefore`. Then rebuild both HTML files and re-render both.

## 4. Preview, approval, delivery
- `npx hyperframes preview --background` opens the Studio editor on the project. The user can
  click to edit there; rebuilding from the spec overwrites those edits, so say so.
- Render the delivery file only after the user approves:
  `npx hyperframes render --quality delivery --workers 2 --output renders/<name>.mp4`, then
  `ffprobe` it and confirm the duration matches `timing.json`.
- Read the render summary's second line: `screenshot capture · software gpu` is the slower Linux
  path. It's fine for short spots.
- Write the numbers into PLAN.md's Validation section.
