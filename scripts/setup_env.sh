#!/usr/bin/env bash
# Setup env pour le rendu — Termux ou Linux.
# Crée un venv temporaire HORS dépôt, installe Pillow + imageio-ffmpeg + numpy + mutagen.
set -e
cd "$(dirname "$0")/.."
python3 -m venv /tmp/lyric-venv
/tmp/lyric-venv/bin/pip install --no-cache-dir -q pillow imageio-ffmpeg numpy mutagen
echo "Env OK : /tmp/lyric-venv"
