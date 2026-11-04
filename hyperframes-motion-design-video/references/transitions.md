# Transitions

A transition says how two scenes relate: a hard cut says "next", a push says "next point in a
sequence", a match cut says "this continues", and a dissolve says "time passed" or "the mood
changed". Decide one per cut, write why in PLAN.md, and keep the family small: **one primary
technique (60–70% of cuts) plus at most one accent** for a piece under ~8 scenes.

## Choosing

1. **Shared element?** If the outgoing and incoming scenes share a shape, color field, word or
   position, use a **match cut**. It's the most designed-looking choice.
2. **Pacing of the type** (`video-types.md`): social and brag reels use hard cuts and whips;
   demos use one consistent push or wipe; explainers vary with meaning; stings have none.
3. **Motion through the cut**: cut at the outgoing move's peak velocity and keep the direction
   and speed into the incoming scene. A cut on a dead moment, or one that reverses direction,
   feels wrong even when both shots are good.
4. **Exits are the transition.** Inside a scene, don't fade content out before the cut. The
   outgoing scene is fully visible when the transition starts. Only the final scene fades out.

| Technique | `enter` value | Default | Use it when |
|---|---|---|---|
| Hard cut | `cut` | 0s | rhythm is the point; scenes are different enough not to need a bridge |
| Match cut | `cut` + a shared element authored in both scenes | 0s | a shape, word or color carries across |
| Push | `push-left` / `push-right` / `push-up` / `push-down` | 0.45s `power3.inOut` | sequence or comparison; spatial "next" |
| Wipe | `wipe-left` / `-right` / `-up` / `-down` | 0.45s `power3.inOut` | graphic, controlled change; the wipe direction echoes motion in frame |
| Zoom through | `zoom` | 0.5s `power3.inOut` | energy, "go deeper" |
| Iris | `iris` | 0.6s `power2.inOut` | playful focus on a center subject |
| Crossfade | `crossfade` | 0.5s `sine.inOut` | a real tonal shift or time passing, used sparingly |
| Blur crossfade | `blur` | 0.6s `sine.inOut` | calm, dreamy pieces |
| Whip pan | authored: `push-*` at 0.2–0.3s `expo.inOut` + motion blur on both scenes' content | 0.25s | energetic, continuous space |

`duration` and `ease` override the defaults: `"enter": {"type": "push-up", "duration": 0.3, "ease": "expo.inOut"}`.

## How scaffold.py builds them

A scene with a non-cut `enter` starts `duration` seconds **before** the previous scene ends, so
the two overlap. The root `main` timeline tweens the two **host clips** across that overlap:
`xPercent`/`yPercent` for pushes, `clipPath: inset(…)` / `circle(…)` on the incoming host for
wipes and iris, `opacity` (+`filter: blur`) for fades, `scale`+`opacity` for zoom. The incoming
host comes later in the DOM, so it paints on top. The runtime owns each clip's visibility, so
nothing tweens `visibility`/`display`. That would break `gsap_animates_clip_element`.

Each scene's own timeline still starts at its local 0, which is the start of the overlap, so
entrance motion plays *during* the incoming transition. To have the content arrive once the
push lands, delay the entrance by the transition duration inside the scene.

## Authoring a match cut

The shared element exists in both scenes at the same position, size and color on the cut frame:

```js
// outgoing scene "plan" (D = 3.2): push into card 3 until the cut, accelerating
zoomLog("#plan-cam", 1, 3.2, D - 0.9, 0.9, "power2.in");
// incoming scene "data": its full-frame panel IS card 3 at scale 3.2, settling to 1
tl.fromTo("#data-panel", { scale: 1.12 }, { scale: 1, duration: 0.8, ease: "expo.out" }, 0);
```
Snapshot the last frame of the outgoing scene and the first frame of the incoming one, and lay
them side by side. They should look nearly identical except for the motion direction.

Other match cuts: a word that grows to fill the frame and becomes the next background; a
color block wiping across that becomes the next scene's ground; a dot that becomes the
next scene's logo mark.

## Hard cut to black, flash and dip
- Cut to black for 2–6 frames before a big reveal: make a tiny `black` scene (0.1–0.2s) in the
  storyboard. It's an explicit beat, not a fade.
- A white flash frame on a music hit: a 1–2 frame scene with `ground` set to the ink color. Use it once
  per piece at most.

## Shader transitions
For glitch, light-leak, burn, domain-warp and other shader transitions, see
`/hyperframes-animation` → `transitions/catalog.md` and the registry (`/hyperframes-registry`).
With shader transitions or HDR media, root fills are forced transparent, so every scene
paints its ground on a full-bleed child (the skeleton's scene root is already a child of its
host, so this is fine).

## check findings around transitions
- `content_overlap` during a crossfade/blur window: two scenes' text overlapping mid-fade is
  expected. Add `data-layout-allow-overlap` to the outgoing scene's text container, or use a
  push or wipe instead if the overlap is ugly in the stills.
- Text pushed half off-frame mid-push isn't a bug. Check the frames just after the push lands.
