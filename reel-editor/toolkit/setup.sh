#!/usr/bin/env bash
# One-time setup on Rayan's Mac (or any new machine). Everything here is free and open source.
# Needs: Homebrew, Python 3.10+, Node 20+.
set -euo pipefail
cd "$(dirname "$0")"
command -v ffmpeg >/dev/null || brew install ffmpeg
python3 -m pip install -r requirements.txt
python3 -m pip install faster-whisper || echo "faster-whisper skipped (captions can still come from an SRT)"
npm install                       # playwright for the map renderer
npx playwright install chromium
npm install -g hyperframes@0.9.3  # HTML-to-video renderer (open source). Never run `hyperframes publish`.
hyperframes telemetry disable || true
echo "Ready. From reel-editor/: python3 toolkit/build_reel.py configs/<reel>.json"
