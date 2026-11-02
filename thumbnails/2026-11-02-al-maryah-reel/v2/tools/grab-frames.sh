#!/usr/bin/env bash
# Pull candidate 9:16 cover frames from a video with FFmpeg, plus a contact sheet to pick from.
# Usage: tools/grab-frames.sh <video> [every_n_seconds=2] [outdir=inputs/frames]
set -euo pipefail
VID="$1"; EVERY="${2:-2}"; OUT="${3:-inputs/frames}"
mkdir -p "$OUT"
# Scale to cover 1080x1920 and centre-crop, one frame every N seconds, high quality JPG.
ffmpeg -v error -y -i "$VID" -vf "fps=1/${EVERY},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -q:v 2 "$OUT/frame-%03d.jpg"
# Contact sheet (numbered) to choose the best blue-hour skyline frame.
ffmpeg -v error -y -i "$OUT/frame-%03d.jpg" -vf "scale=216:384,drawtext=text='%{n}':x=8:y=8:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6,tile=6x4" -frames:v 1 "$OUT/contact-sheet.jpg" || true
ls "$OUT" | wc -l | xargs echo "frames written to $OUT:"
