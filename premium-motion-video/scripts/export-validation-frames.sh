#!/usr/bin/env bash
# Export specific frames of a Remotion composition as PNGs for the Section 4
# validation pass (cheap frame-level checks before/without a full render).
#
# Wraps the real Remotion CLI command (verified against remotion.dev/docs/cli/still,
# which points to `remotion render --frames` for exporting more than one still,
# available since Remotion v4.0.502):
#   npx remotion render <comp-id> <output-dir> --frames=<csv> --image-format=png
#
# Usage:
#   ./export-validation-frames.sh <composition-id> <output-dir> <frame1,frame2,...>
#
# Examples:
#   # A handful of stills spread across the timeline
#   ./export-validation-frames.sh MyComp out/validation 0,30,60,90,120
#
#   # A burst of consecutive frames around a fast cut at frame 60, to check
#   # for stutter/smear per the main skill's Section 4 fast-motion check
#   ./export-validation-frames.sh MyComp out/validation 57,58,59,60,61,62,63

set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <composition-id> <output-dir> <frame1,frame2,...>" >&2
  exit 1
fi

COMP_ID="$1"
OUT_DIR="$2"
FRAMES="$3"

mkdir -p "$OUT_DIR"

npx remotion render "$COMP_ID" "$OUT_DIR" --frames="$FRAMES" --image-format=png

echo "Exported frames [$FRAMES] of composition '$COMP_ID' to $OUT_DIR — open them (Read tool / an image viewer) as part of Section 4 validation, don't just trust that the command succeeded."
