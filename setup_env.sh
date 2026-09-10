#!/usr/bin/env bash
# Reconstruction de l'environnement (règle §4 — work/ non versionné, régénérable)
set -e
cd "$(dirname "$0")"
python3 -m venv venv
./venv/bin/pip install --quiet --upgrade pip
./venv/bin/pip install --quiet imageio-ffmpeg mutagen numpy pillow matplotlib scipy
mkdir -p bin
FF=$(./venv/bin/python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
ln -sf "$FF" bin/ffmpeg
echo "OK — $(./bin/ffmpeg -version | head -1)"
