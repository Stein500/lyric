#!/usr/bin/env bash
set -e

echo "=== Setup Environnement de Production Lyrics (v5.1.1) ==="

# 1. Vérification Python et dépendances
python3 -m pip install --break-system-packages pillow mutagen numpy scipy fonttools brotli imageio-ffmpeg

# 2. Création des répertoires de travail
mkdir -p scripts work livrables assets/raw/portrait assets/raw/landscape assets/fonts

# 3. Lien ffmpeg si besoin
if ! command -v ffmpeg &> /dev/null; then
    FFMPEG_BIN=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
    sudo ln -sf "$FFMPEG_BIN" /usr/local/bin/ffmpeg
fi

echo "=== Environnement prêt ==="
