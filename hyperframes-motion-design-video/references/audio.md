# Audio: music, cues, voiceover, mix

Sound is what makes motion feel edited instead of animated. Every value lives in
`storyboard.json`, and every cue hangs off a scene id, so a retime moves the sound with it.

## Contents
1. Sound modes, 2. Music and beats, 3. SFX cues, 4. Levels and ducking, 5. Voiceover,
6. Loudness targets, 7. Sourcing

---

## 1. Sound modes
| Mode | When | Timing driver |
|---|---|---|
| Music + SFX | promos, launches, reels | structural cuts on the beat; the drop on the biggest cut |
| SFX only | stings, UI demos, or no fitting track | free timing; each hit is the beat |
| Voiceover (+ bed) | explainers, demos | scenes follow speech; music carved −9 dB under VO |
| Silent | captions-only social, loops | design for muted playback anyway |

Design every video to work muted first (most social viewing starts muted). Sound reinforces.

## 2. Music and beats
```bash
python3 <skill>/scripts/analyze_music.py <project>/assets/music/track.mp3 --fps 30
```
- Read the tempo from the kick grid (`beat = 60 / BPM` seconds) and where the **kicks enter**
  after a quiet stretch (the drop).
- `music.trim` = (time the drop is in the file) − (time you want it in the video). Put the drop
  on the biggest cut, usually hook → first content.
- Make structural scene lengths **whole beats** (or the transition's landing on a beat:
  `duration = overlap + n·beat`). Free-running inner motion doesn't need to lock.
- Pick a section whose energy outlasts the edit, so the end card still sits on kicks.
- Tempo by mood: 60–80 BPM calm/regal, 90–110 smooth, 115–123 upbeat, 125+ high-energy.
- Don't time-stretch more than ~3%. Choose a different section or track instead.
- Verify on a render: if hits feel early or late, nudge `trim` by the measured offset (decoders
  differ by tens of ms).

## 3. SFX cues
```bash
python3 <skill>/scripts/sfx_peaks.py <project>/assets/sfx/* --fps 30
```
- `peak` = the seconds value printed. The scaffold starts the file that much early, so the
  **loudest** moment sits on `at`. Whooshes peak 0.1–0.6s in; clicks, pops and impacts at ~0.
- Put the peak where the motion **resolves** (a card landing, the cut of a whip, a press),
  not where it starts.
- Give the cut that matters a cue, and leave most cuts without one. Good homes: the
  drop/match cut (whoosh), a press (click), a number landing (soft hit), the end-card resolve
  (chime or low impact).
- Layered hits: a soft movement sound under a sharper accent at the landing, in different
  frequency ranges (a sub swoosh + a high tick).
- UI-scale sounds stay tiny (volume 0.2–0.4).
- `volume` is capped at 3.98 (+12 dB). For a quiet file that needs more, bake a louder copy:
  `ffmpeg -i in.wav -af "volume=9dB,alimiter=limit=0.89" out.wav`.
- Effects (EQ, reverb, delay, compressor, buses): `/hyperframes-audio`. The scaffold places
  dry files. For a one-off effect, bake a processed WAV offline.

## 4. Levels and ducking
- Start the music at `gain` 0.3–0.5 and SFX at 0.3–1.0, then **measure** with `audio_check.py`.
- Target: every SFX peaks **≥ 3 dB over the music** in its 80 ms window (≥ 2 passes).
- `"duck": true` on a cue dips the music by `music.duckDb` (default −6 dB: 1-frame attack,
  2-frame hold, 6-frame release) around its peak. Use it on the drop/match-cut whoosh, the
  end chime and any hit that sits on a loud music accent. Don't duck every tick, because it
  pumps against the tempo.
- Fades: `music.fadeIn` (0.1–0.3s) and `fadeOut` (1–1.5s, so the last frame is never cut mid-bar).
- The scaffold writes fades and ducks as one `data-automation` volume lane on the music
  `<audio>`, sampled per frame. The music-only check render keeps the same lane.

## 5. Voiceover
- Script first, then generate each line separately (`npx hyperframes tts`, `/media-use`, or a
  local model; ask before installing anything or sending text online).
- Trim silence, then set each scene's duration to its line (+0.15–0.3s). On-screen words appear
  at their spoken onsets (word timestamps from `npx hyperframes transcribe`).
- Add each line as `{"kind": "vo", "src": …, "scene": …, "at": …}`. The music is carved by
  `music.voDuckDb` (default −9 dB) across the whole line with 150 ms ramps.
- Narration says *why*; the screen shows *what*. Never read the on-screen text aloud.

## 6. Loudness targets
| Mix | Integrated | True peak |
|---|---|---|
| Music-led promo | about −14 to −16 LUFS | ≤ −1.3 dBTP |
| SFX leading / dynamic | −16 to −19 LUFS (report it) | ≤ −1.3 dBTP |
| SFX-only, sparse | −20 to −24 LUFS is expected | ≤ −1.3 dBTP |
| Voiceover explainer | −16 LUFS, VO peaks around −6 dBFS | ≤ −1.3 dBTP |

A hot peak is almost always one SFX stacked on a music accent: duck that cue or lower it before
lowering the whole bed. The scaffold has no master limiter, so to push louder without
clipping, bake a limited music copy (`loudnorm` or `alimiter`) into `assets/music/`.

## 7. Sourcing
Use files the user has. Otherwise resolve licensed ones with `/media-use` (`--type sfx` needs no
account; music via the host's own tools or `--type bgm`). Never ship unlicensed audio, and write
each file's source into PLAN.md.
