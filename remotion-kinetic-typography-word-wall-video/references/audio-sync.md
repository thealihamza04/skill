# Audio: music, beat sync, SFX, mix

Sound is what makes this style feel edited instead of animated. The reference project went
through six music/voice passes; these are the conclusions, so the next video starts at the end.

## Contents
1. Choosing the sound mode, 2. Analyzing a music track, 3. Locking cuts to the beat,
4. The SFX kit, 5. Levels: SFX over music, 6. Loudness and true peak, 7. Voiceover variant

---

## 1. Sound mode
| Mode | When | Timing |
|---|---|---|
| **Music + SFX** (default) | Most promos | The first wall cut on the drop; later cuts on the beat grid. |
| **SFX only** | User asks, or no fitting track | Free timing; spec `"music": null`. |
| **Voiceover** | Explainers, "speak what's on screen" | Timing follows speech; see §7. |

Users of this style consistently wanted the **SFX louder than the music** and the **drop on the
cut into the wall**. Start there.

## 2. Analyzing a track
```bash
python3 <skill>/scripts/analyze_music.py public/music/track.mp3 --fps 24 --drop-frame 20
```
- **Tempo from the kick grid.** Autocorrelation alone mis-read a 100 BPM jazz track as 66
  (off-beat spacing). The kick interval is the truth. Frames per beat = fps × 60 / BPM.
- **`dropFrame`** is where the first wall cut lands. Make it the typed line's natural length
  (last word + 9 frames; the planner tells you if the line would sit idle for more than ~8
  frames waiting for the drop).
- **Drops** = a quiet stretch followed by a jump in the kick and cymbal bands. Choose one whose
  following high-energy section is at least as long as the wall + statement + end card.
- The master is often loud or clipping (−11 LUFS, +1 dBFS). Plan a gain well under 1.
- Copy a user-supplied track into `public/music/` first; never reference files outside `public/`.

## 3. Locking to the beat
- **The drop goes on the first wall cut** (spec `dropFrame`, usually the typed line's length).
  The typed line plays over the pre-drop break.
- **Later structural cuts** (statement, end card, next act) land on beats, within ±0.5 frame.
  The planner does this by growing scenes to the next grid line.
- **Wall swaps run free** unless the 8th note happens to equal a readable length. Locking every
  swap to the grid forces equal lengths, and users want varied ones.
- **Don't time-stretch to force a grid.** 3% (+0.5 semitone) is inaudible; 15–20% (+3 semitones)
  is obviously wrong.
- **Verify on a render, then nudge.** A trim from onset analysis is typically 1–2 frames early or
  late (onset vs attack). Run `check_audio.py`. If kicks are consistently +N ms late, increase
  `trimBefore` by N/1000 × fps (fractional values work).

## 4. The SFX kit
One file per event (`HitKind`). The engine fires them from scene boundaries, so they follow any
retime automatically:

| Hit | Fires at | Good sounds |
|---|---|---|
| `typeWord` | each typed word | soft pop / key tick |
| `wallIn` | the cut into a wall | air whoosh / riser that **peaks on the cut** |
| `wallSwap` | each highlight swap | short digital tick / snap |
| `statement` | statement start | chime / bell |
| `reveal` + `revealImpact` | end card start | swoosh + low impact |
| `extraSfx` | any frame (e.g. a logo's second beat) | pop |

- Measure every file: `python3 <skill>/scripts/sfx_peaks.py public/sfx/*.wav --fps 24`. Set
  `peakOffset` so the **loudest** moment lands on the event (a whoosh peaks ~9 frames in).
- Use files already in the project's `public/`, ask the user, or source royalty-free ones. Don't
  ship unlicensed audio.
- Effects like echo or reverb aren't available at render time. If one is wanted, bake it into a
  new WAV offline, and keep the dry hit's timing. (One user asked for a wall-tick echo, then had
  it removed, so offer it rather than assume it.)

## 5. Levels: SFX over music
Target: **every hit peaks ≥ ~3 dB over the music around it.** Measured, not guessed:
1. Start with the music at gain ≈ 0.4 and the kit volumes from `example.config.tsx`. Those were
   tuned against one loud, punchy track, so treat them as a starting point and expect to adjust
   per track.
2. Render the mix and a music-only pass (`--props='{"mute":"sfx"}'`) and run `check_audio.py`.
3. Raise each hit by its shortfall (multiply volume by 10^(dB/20)). Volumes > 1 are fine for
   quiet files.
4. `duckOn` dips the music −6 dB under every hit of the chosen kinds (1-frame attack, 2 hold,
   6 release). Use it for typed pops, the statement and the reveal. `duckFrames` adds one-off dips
   at absolute frames, for a single hit that stacks hot on a music accent. **Never duck the drop's `wallIn`**; that kills
   the drop. Don't duck every swap tick either: it pumps against the music's own tempo.

## 6. Loudness and true peak
- **True peak ≤ −1.3 dBTP.** `check_audio.py` prints the four loudest frames with the music
  level, the SFX level and the hit at each. It's almost always an SFX stacking on a music hit, so
  add that frame to `music.duckFrames` before lowering everything.
- **SFX-only mixes** are mostly silence, so LUFS reads low (−20 to −23) and that's expected.
  Raise `sfxGain` until the loudest hit sits near −2 dBTP, and check with
  `check_audio.py mix.wav none timing.json`.
- With the SFX leading, integrated loudness lands around −16 to −17 LUFS. That's acceptable.
  Platforms normalize, and pushing to −14 would mean clipping or pumping. Report it honestly.
- A voice or music bed that needs more level without clipping: bake a limited copy offline
  (`ffmpeg -af "volume=…,alimiter=limit=…"` or `loudnorm`) into `public/`.

## 7. Voiceover variant
- Natural voices: Microsoft Edge TTS (`pip install edge-tts` in a venv; almost no local compute,
  but the text is sent online) or a local Piper / Kokoro model (offline, needs a download). Ask
  before installing either. eSpeak is robotic; use it only as a timing placeholder.
- Generate each line separately with word boundaries, trim silence, then set each scene and wall
  segment to its spoken length (+1–2 frames). Typed words cut on at their spoken onsets.
- Vary delivery per line (rate and pitch; Edge applies pitch at about half strength, so ±20–35Hz
  ≈ ±1.5–3 semitones). A list that accelerates and rises, then a slow, low payoff, sounds natural.
- Don't voice the end card unless asked. The free Edge service sometimes returns no audio, so retry.
