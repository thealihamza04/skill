# Launch spot — motion video plan

## Brief
- One sentence: "Describe a video, plan every scene, and get a checked motion-design film in HTML."
- Type: Social promo / launch (video-types.md) · Length: 17.9s · Size: 1920×1080 @ 30fps · Platform: portfolio card, LinkedIn/X
- Named reference: Apple product-film type pacing (one idea per card, hard cuts on the beat) + a
  storyboard-into-frame match cut in the manner of Ordinary Folk's explainer reels
- Brand: ground #0E0E11 · ink #F3F1EC · accent #FF5B37 (#D63F1A on the light end card for 3:1 contrast) · Inter 500/800, Source Serif 4, JetBrains Mono
- Sound mode: music + SFX. Music: `bed.mp3` (electronic-chill), 114.1 BPM (beat 0.526s), kicks enter at 4.228s → trim 1.628s puts the drop on the hook→plan cut (2.60s)
- Assumptions: no voiceover; the install command and repo are the user's real ones
- Sources: "8 video types" = the 8 rows of `references/video-types.md`; "0 errors, 0 warnings" = this project's real `npx hyperframes check` output; `npx skills add thealihamza04/skill` = the repo README

## Scenes
### 1 — hook: the brief is the input (2.60s)
- On screen: heading "Describe the video." / visual: prompt field typing "a 15-second launch video for my app"
- Composition: heading upper-middle, field below, generous negative space; field is the focal motion
- Duration: 2.6s, because the drop lands on the cut out and the typed line needs ~1.7s
- Motion: "a 15-second" already typed on frame 0 (thumbnail), the rest types 0.15→1.85s with a seeded jitter; caret blinks by time (0.5s); submit press scale 0.86 (0.12s in, 0.2s out, power2.out) at 2.05s; camera locked
- Enter: none (frame 0 = thumbnail, heading and field already on screen)
- Sound: click.wav peak on 2.15s (the press), volume 0.35
- Status: validated

### 2 — plan: storyboard (3.16s = 6 beats)
- On screen: heading "Plan every scene first." / visual: five storyboard cards
- Duration: 6 beats, so the match cut lands on a beat
- Motion: cards rise 70px, spring ζ0.8, 0.75s, stagger 0.08 (group 0.4s); then one log-space camera driver 1→1.035 (hold) →6.4 (power2.in, accelerating into the cut = peak velocity)
- Enter: hard cut on the drop
- Sound: none (the drop is the sound)
- Status: validated

### 3 — data: the card becomes the frame (2.63s = 5 beats)
- On screen: the number 0→8 / support "video types. One workflow."
- Motion: match cut: starts at scale 0.885 (measured: card 3's size on plan's last frame) and keeps pushing IN to 1 (expo.out), radius 91→0 and border dissolve in 0.5s; countUp 0→8 power2.out 1.15s; label masked rise 100px expo.out 0.7s
- Enter: match cut (cut + shared element)
- Sound: sub-swoosh.wav peak on the cut, volume 0.9, music ducked −6 dB
- Status: validated

### 4 — motion: three beat words (3.61s incl. 0.45s push)
- On screen: "Springs." → "Staggers." → "On the beat.", one word per 2 beats, accent ground
- Motion: each word demonstrates itself: spring ζ0.72 scale 0.55→1 (the film's one overshoot) / chars rise 90px stagger 0.028 expo.out / hard cut + punch 1.08→1 0.3s; every word drifts 14px
- Enter: push-up 0.45s power3.inOut (the accent transition, landing on a beat)
- Sound: digital-snap.wav on the 2nd and 3rd word cuts, volume 0.62, ducked
- Status: validated

### 5 — check: proof (3.16s)
- On screen: heading "Checked by HyperFrames." / visual: terminal typing `npx hyperframes check` → "✓ 0 errors, 0 warnings"
- Motion: terminal spring ζ0.82 rise 40px; typing 0.034s/char; result line (accent) 0.95s; hold = slow 16px rise (not another push)
- Enter: hard cut on a beat
- Sound: click.wav on the enter press (0.9s), volume 0.3
- Status: validated

### 6 — end: card (3.61s incl. 0.45s push)
- On screen: "Motion design, in HTML." (serif accent) / "npx skills add thealihamza04/skill"
- Motion: title masked rise 160px expo.out 0.8s at 0.4s; command (54px, ink) rise 0.6s at 0.85s; accent underline draws 1.5→2.2s (second beat); push 1→1.035
- Enter: push-up 0.45s (same accent as scene 4: one primary + one accent overall)
- Sound: crystal-chime.wav at 0.95s (title landing), volume 1.0, ducked; digital-snap.wav at 2.2s (underline lands), volume 0.6, ducked
- Status: validated

## Validation
- check: 0 errors, 0 warnings (lint, runtime, layout, motion, contrast 13/13, craft, audio)
- Match-cut seam (f172 → f173): card and number within ~2% size, same direction of travel
- Audio (delivery render): −18.4 LUFS integrated (SFX leading), −3.0 dBTP true peak; every cue +4.4 … +8.0 dB over the music
- Independent critic, round 1: hook 6 · readability 5 · motion 7 · variety 6 · composition 7 · accuracy 8 · sound 7
  - Issues → fixes: empty thumbnail → pre-typed prompt; illegible card labels → removed; same push in every scene →
    locked/drift/rise/push varied per scene; small terminal → 60px mono, fitted box, accent result; Staggers fade-rise →
    masked rise at full opacity (mask to the descender line); end CTA tiny grey → 54px ink + underline second beat;
    product unnamed → "Checked by HyperFrames."; end tick +1.3 dB → volume 0.6 + duck (+7.9 dB)
- Independent critic, final: hook 7 · readability 8 · motion 8 · variety 7 · composition 8 · accuracy 8 · sound 7 (by ear unverified)
- Not verified: playback by ear on speakers; a real phone (390px sheet only)
