# Porting a reference video

The method that produced `format.md` and the engine. Use it when a user brings a new reel to
recreate, whether it's a variant of this format or a different one. All scratch files go in the
session's scratchpad, never the repo.

## 1. Probe and look at the whole thing

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact ref.mp4
ffmpeg -v error -i ref.mp4 -vf "fps=2,scale=360:-1,tile=5x4" sheet_%02d.png
```
The 2fps sheets show the beats. Then make **timestamped 10fps sheets** for timing:
```bash
ffmpeg -v error -i ref.mp4 -vf "fps=10,scale=240:-1,drawtext=text='%{pts\:flt}':x=4:y=4:fontsize=14:fontcolor=red,tile=8x6" d_%02d.png
```
Read every sheet. Write a beat table: start, end, what enters and exits, and how
(fade/slide/scale/wipe/letter scatter/typing/counting). Note counters' values at several
timestamps. That gives the curve: fast-then-slow is ease-out, holds are steps.

## 2. Layout and color from full-resolution frames

```bash
for t in 0.0 1.8 6.3 12.6 15.2 18.5 19.9; do ffmpeg -v error -y -ss $t -i ref.mp4 -frames:v 1 -update 1 f_$t.png; done
```
(`-update 1` is required for a single image output.) Read positions and sizes in the reference's
own pixel space and build on that stage, scaling it up at the end. Sample colors with Pillow at
flat areas (`im.getpixel((5, 5))` for backgrounds).

## 3. Font

Identify the traits (storey of `a`/`g`, terminals, width) and pick the closest Google Font. Then
**size by width**: render once, measure the same text's width in both (sheets at the same scale)
and multiply each font size by `ref_width / your_width`. Your first guesses will be 1.3–2×
too small. That's normal; correct per element.

## 4. Iterate with side-by-side stills

`scripts/stills_sheet.py <Comp> --out <dir> --reference ref.mp4 --times <beat midpoints>`.
Fix whatever the pairs show (size, position, timing, clipping), re-run, and stop when
differences are only content (different images, copy, logo).

## 5. Make it the user's

- Replace the reference's brand: name, logo mark, URL, and **its numbers**. Its stats are its
  own claims; use the user's verified facts only.
- Don't extract or reuse the reference's soundtrack, project images or logo. Use the user's
  media and a licensed or local music bed.
- Move every piece of copy and media into the config, with a comment on where each number came
  from.
