#!/usr/bin/env bash
# ⚙️  SETUP_VENV.SH — Recrée l'environnement Python en 1 commande
# Usage : bash setup_venv.sh
# Garanti anti-reset : pas besoin de venv préexistant, pip + imageio-ffmpeg le rebuild.
set -e
cd "$(dirname "$0")"
if [ -x tools_venv/bin/python3 ]; then
  echo "✅ venv existe déjà"
else
  echo "🔧 Création du venv..."
  python3 -m venv tools_venv
fi
# shellcheck disable=SC1091
source tools_venv/bin/activate
pip install --upgrade pip >/dev/null 2>&1
pip install imageio-ffmpeg pillow mutagen numpy >/dev/null 2>&1
# Lien ffmpeg (fourni par imageio-ffmpeg) dans tools_venv/bin/
FF_BIN=$(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
ln -sf "$FF_BIN" tools_venv/bin/ffmpeg 2>/dev/null || true
echo ""
echo "✅ Environnement prêt"
python -c "import PIL, mutagen, numpy, imageio_ffmpeg; print('  pillow', PIL.__version__); print('  mutagen', mutagen.version_string); print('  numpy', numpy.__version__); print('  ffmpeg:', imageio_ffmpeg.get_ffmpeg_exe())"
