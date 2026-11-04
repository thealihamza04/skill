# Validation

Check rendered pixels and rendered sound, not code. A video that wasn't checked, scored and seen
at phone size isn't finished. Run everything from the project directory with the pinned CLI.
Say plainly what wasn't verified (by ear, on a real phone).

## The loop
```
check (0/0) ─► snapshots + sheet ─► phone sheet ─► bursts around fast moves ─► seams of match cuts
          ─► draft renders (mix + music-only) ─► audio_check ─► critic pass ─► fix ─► repeat
```

## 1. Static and browser audit
```bash
npx hyperframes check
```
Target **0 errors and 0 warnings**. Infos are fine when they're intentional (overflowing
camera layers, `audio_none` on a silent film). `hyperframes-build.md` maps each finding to its fix.
A lint error disables the browser audits, so fix lint first.

## 2. Pictures
```bash
npx hyperframes snapshot --at <scaffold.py's printed list> --no-end --output stills
python3 <skill>/scripts/contact_sheet.py stills stills/sheet.jpg --timing storyboard.timing.json
python3 <skill>/scripts/contact_sheet.py stills stills/phone.jpg --timing storyboard.timing.json --tile 390
```
Look at both sheets and check:
- frame 0 works as a thumbnail; each scene's one idea is obvious in its still
- every word is readable at 390px; nothing clips at the frame edge or in safe zones
- nothing is on screen that isn't in PLAN.md (stray chrome, placeholder, leftover label)
- holds are still moving (compare 30% and 85% stills of the same scene: the frame differs)
- the palette and type are consistent across scenes, and the accent is used once per frame
- **Bursts**: around every fast move, snapshot 6–9 consecutive frames
  (`--at t, t+1/fps, …`). Look for pops, a direction reversal, smear on text meant to be read, or
  an element appearing a frame early.
- **Match-cut seams**: the last frame of the outgoing scene next to the first of the incoming
  one. The shared element should match in size and position within a few percent, and travel the
  same way.
- **Reference ports**: `npx hyperframes snapshot --against <reference.mp4>` gives side-by-side
  frames at the same times. Text width is the quickest tell of a wrong size.

## 3. Sound
```bash
python3 <skill>/scripts/scaffold.py storyboard.json --project . --mute sfx --out music-only.html
npx hyperframes render --quality draft --workers 2 --output renders/mix.mp4
npx hyperframes render --composition music-only.html --quality draft --workers 2 --output renders/music.mp4
rm music-only.html          # a second root makes check fail
python3 <skill>/scripts/audio_check.py renders/mix.mp4 --music renders/music.mp4 --timing storyboard.timing.json
```
| Check | Target |
|---|---|
| True peak | ≤ −1.3 dBTP (exit 1 above −1.0) |
| Integrated loudness | see `audio.md` §6 for the mix type; report the number |
| Every SFX vs music | ≥ +3 dB (≥ +2 passes) |
| Cue timing | each cue lands on its planned frame (`storyboard.timing.json` → `cues[].at`) |

Fix order: hot peak → duck or lower that cue; quiet hit → raise its volume (≤ 3.98) or duck
the music under it; consistent sync offset → nudge `music.trim`. Re-scaffold, then re-render both.

## 4. Independent critic pass (required)
The builder grades too kindly. Give a **fresh subagent** only the sheets, the bursts, PLAN.md
and this rubric (not the conversation or the code), and ask for scores and a ranked list of
concrete fixes. If no subagent is available, do it yourself as a separate pass, written as a
harsh motion director rather than a proud author.

| Axis | 1–10: what it checks |
|---|---|
| Hook | first 2–3s state the subject; frame 0 is a usable thumbnail |
| Readability | every line readable at normal speed and at phone width |
| Motion | easing and physics follow the plan; nothing arbitrary, uniform or stuttery |
| Variety | pacing and technique vary on purpose; one primary transition + one accent |
| Composition | one idea per scene, depth, negative space, no stray chrome |
| Accuracy | every number, logo and claim traces to a source in PLAN.md |
| Sound sync | cues on meaningful frames at measured levels (note if unverified by ear) |

**Anything below 8 gets fixed and re-checked before delivery.** Write the scores, the
issues and the fixes into PLAN.md's Validation section.

## 5. Delivery
- Show the preview (`npx hyperframes preview --background`) or a draft. Render the delivery file
  after approval: `npx hyperframes render --quality delivery --workers 2 --output renders/<name>.mp4`.
- `ffprobe` it: duration matches `storyboard.timing.json → duration`, plus size, fps and an audio stream.
- Web/portfolio copies: `ffmpeg -i in.mp4 -vf scale=1280:-2 -c:v libx264 -crf 24 -preset slow -movflags +faststart -c:a aac -b:a 128k out.mp4`
  and a poster from the best frame (not an arbitrary one).
- Report: the check result, the critic scores, LUFS/true peak, and what wasn't verified.
