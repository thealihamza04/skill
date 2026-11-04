# Motion language: the numbers

Motion reads as designed when every choice has a reason and a number. Pick 2–4 of these per
scene, write them into PLAN.md, then build them. All values are starting points measured or
sourced from studio practice (Figma's "Principles in Motion", the howseen-ai motion-design skill,
the measured references behind the word-wall and stat-reel skills); tune per project, and never
leave a library default in place without deciding on it.

## Contents
1. Timing, 2. Easing, 3. Springs, 4. Choreography, 5. Camera, 6. Type in motion,
7. Tone → numbers, 8. Motion inside UI, 9. Motion blur

---

## 1. Timing

| Move | Duration |
|---|---|
| UI-scale feedback (press, toggle, tick) | 0.1–0.25s |
| Text or element entrance | 0.45–0.8s |
| Hero entrance, logo resolve | 0.8–1.4s |
| Scene transition | 0.3–0.6s (calm up to 0.8s; high-energy 0.15–0.3s) |
| Exit (only on the final scene, or as a transition) | 60–70% of its entrance |
| Max fully-still time on screen | ~1s |
| Slower than ~1.2s for one move | only as a deliberate slow reveal with nothing competing |

**Overlap the next beat** before the previous one settles (start beat 2 at ~60–70% of beat 1),
so a sequence feels orchestrated rather than queued.

## 2. Easing (GSAP names)

| Use | Ease |
|---|---|
| Arriving / settling (default entrance) | `power3.out`, `expo.out`, or `bez(0.16, 1, 0.3, 1)` |
| Leaving | `power2.in`, `power3.in` |
| Repositioning on screen, camera moves | `power2.inOut`, `bez(0.65, 0, 0.35, 1)` |
| Snap / punch | `expo.out` over 0.25–0.4s |
| Physical, with tiny overshoot | `spring(0.75–0.85)` (prelude) or `back.out(1.2–1.4)` |
| Continuous loops, drifts under a hold, counters' last digits | `none` (linear) is fine only here |

Never leave GSAP's default `power1.out` on a hero move, and never use linear on a discrete move.

## 3. Springs

`spring(zeta)` in the scene prelude is a damped spring normalised to the tween's duration:
- ζ **0.72–0.85** is the premium default, with 1–4% overshoot and a calm settle.
- ζ 0.6–0.7 is playful (about 5–9% overshoot); use it on one element per scene at most.
- ζ ≥ 1 gives no overshoot (critically damped), heavy and deliberate.
- Below ζ 0.55 reads as a cartoon bounce. Avoid it unless the brand is literally playful.
The duration is the settle time: 0.6–0.9s for text, 0.9–1.3s for a large object.

## 4. Choreography

- **Stagger** related items: text words 0.04–0.08s, list rows/cards 0.06–0.12s, chars
  0.015–0.03s. Cap the whole group at ~0.5s (`items × stagger`), or it reads as a queue.
- **Order** follows meaning: reading order (L→R, top→bottom) for content to read, center-out
  or seeded-random (`rng(seed)`) for texture to feel.
- **Distance**: entrances travel 24–64px at 1080p (scale with frame height). Big travel
  reads as a slide, not an entrance.
- **Anticipation**: a 2–6% counter-move 0.08–0.15s before a big move (a logo pulling back
  before it punches in). Use it rarely; it costs time.
- **Follow-through**: secondary elements settle 0.05–0.15s after the primary.
- **Hold and settle**: after a beat lands, give it ≥ 0.4s before the next beat competes.
- **One focal motion at a time**. Anything else on screen is static or drifting slowly.

## 5. Camera

- **Push-in on a hold**: scale 1 → 1.03–1.06 over the shot, eased `none` or `sine.inOut`.
  This is the default cure for dead air.
- **Zooms in log space** (`zoomLog()`): a ×1.5 geometric step reads as constant camera speed. A
  linear scale tween slows down visually as it grows.
- **Push into a detail → match cut**: zoom ×2–×4 into an element, then cut while the scale is still
  accelerating (peak velocity) into a scene where that element is already big.
- **Parallax**: background layers move 20–40% of the foreground distance.
- Never put a CSS `transform` on an element GSAP also moves (`gsap_css_transform_conflict`).
  Wrap it instead.

## 6. Type in motion

- Pick one reading unit per card: line, word or char. Words for punchy declaratives, lines
  for calm statements, chars only when the word is the payoff.
- Scale contrast carries meaning: the key word 1.4–2× the rest, or a weight jump
  (500 → 800), or the accent color. Use one of them, not all three.
- Masked reveals (text rising inside an `overflow:hidden` line box, y 100% → 0, `expo.out`
  0.6–0.8s) read more premium than fade+rise on big display type.
- Tracking tightens as type settles: letter-spacing from +0.02em to −0.04em over the entrance,
  for display type only.
- Typing effects: 0.03–0.06s per char with a seeded jitter, and a caret blink of 0.5s on and
  0.5s off driven by time, never by an interval.
- Counters: `countUp()` with `power2.out`/`expo.out` so most of the value appears early, then hold ≥ 1s.
- Readability floor: ≥ 0.4s for 1–2 words; long lines 0.3s/word after settling; text under
  0.5 opacity doesn't count as read (HyperFrames' `line_unread` audit).

## 7. Tone → numbers

| Brief says | Durations | Ease | Stagger | Transitions | Music |
|---|---|---|---|---|---|
| snappy, punchy, launch | 0.3–0.5s | `expo.out`, `power4.out` | 0.03–0.05 | hard cut, whip, zoom | 120–128 BPM |
| elegant, premium, calm | 0.7–1.1s | `power2.inOut`, spring 0.85 | 0.08–0.12, overlapping | blur crossfade, slow push | 70–100 BPM |
| playful | 0.4–0.7s | spring 0.65–0.7, `back.out(1.6)` | center-out 0.04 | iris, push | 105–120 BPM |
| corporate, clean, explainer | 0.45–0.7s | `power3.out`, no overshoot | 0.05–0.08 | push, wipe | 90–110 BPM |
| cinematic, trailer | 0.8–1.6s holds, hard hits | `expo.inOut` | sparse | hard cut to black, zoom | 60–90 BPM + impacts |
| no tone given | use the corporate/clean row | | | | |

## 8. Motion inside UI

A simulated interaction is micro-motion and follows interface timing, not scene timing: press
feedback 0.1–0.16s (scale 0.97, `power2.out`), dropdown/popover 0.15–0.25s, modal 0.2–0.5s,
toast 0.3s, list stagger 0.03–0.05s. A cursor travels on `power2.inOut` 0.5–0.9s, rests
0.15s, then clicks. UI at rest follows the product's real design system: real radii, shadows,
syntax highlighting and copy. A rendered card or terminal is an interface-engineering problem
first (`interface-engineer`/`design-system` skills if installed).

## 9. Motion blur

Blur only motion that crosses more than about one element-width per frame: whips, slams,
snap zooms, with 1–3 per piece. Never blur text meant to be read at that moment (blur the approach,
land sharp). Use the `motion-blur` registry component per element, or the renderer's
`motionBlur` option for the whole frame (`hyperframes-animation/references/motion-blur.md`).
Studio target: a 180° shutter (0.5) with 6–8 sub-frames on the fast move.
