# Example: launch spot (17.9s, 1920×1080 @ 30fps)

The film on the portfolio card for this skill, built with this skill. Six scenes: a typed brief,
a storyboard that match-cuts into a counter, three beat words, a real `hyperframes check`, an end card.
It passes `npx hyperframes check` with 0 errors and 0 warnings.

To rebuild it:
```bash
HYPERFRAMES_SKIP_SKILLS=1 npx -y hyperframes init launch-spot --non-interactive && cd launch-spot && rm index.html
cp -r <skill>/assets/examples/launch-spot/{storyboard.json,PLAN.md,compositions} .
# audio is not bundled: put your own files at the storyboard's paths
#   assets/music/bed.mp3 (114 BPM, kicks enter at 4.228s), assets/sfx/{click,sub-swoosh,digital-snap,crystal-chime}.wav
python3 <skill>/scripts/scaffold.py storyboard.json --project .
npx hyperframes check
```
For a silent build, delete `"music"` and `"audio"` from storyboard.json first.
A silent rebuild reports one `film_silent` warning (the film has no sound), which is expected.
