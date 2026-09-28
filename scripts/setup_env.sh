#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${LYRIC_VENV:-/tmp/lyric-venv}"
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --no-cache-dir -r "$ROOT/scripts/requirements-media.txt"
printf '\nPython média : %s/bin/python\n' "$VENV"
"$VENV/bin/python" -c 'import imageio_ffmpeg; print("FFmpeg :", imageio_ffmpeg.get_ffmpeg_exe())'
