#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 -m venv .venv
.venv/bin/pip install --no-cache-dir pillow numpy mutagen imageio-ffmpeg fonttools brotli
echo "OK env → $ROOT/.venv"
.venv/bin/python - <<'PY'
import imageio_ffmpeg
print("ffmpeg", imageio_ffmpeg.get_ffmpeg_exe())
PY
