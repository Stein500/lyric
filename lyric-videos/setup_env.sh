#!/usr/bin/env bash
# =============================================================================
#  DSKY LYRIC VIDEOS — préparation de l'environnement
#  (le sandbox n'a NI ffmpeg NI pillow au départ — tout est installé ici)
# =============================================================================
set -e

echo "▸ python : $(python3 -V 2>&1)"

# --- 1) ffmpeg -----------------------------------------------------------------
if command -v ffmpeg >/dev/null 2>&1; then
  echo "▸ ffmpeg système : $(ffmpeg -version 2>/dev/null | head -1)"
else
  echo "▸ pas de ffmpeg système → binaire embarqué imageio-ffmpeg (aucune compilation)"
fi

# --- 2) paquets python ---------------------------------------------------------
PIP_FLAGS=""
if ! pip3 install --quiet --dry-run pillow >/dev/null 2>&1; then
  PIP_FLAGS="--break-system-packages"      # Debian/Ubuntu PEP-668
fi
pip3 install --quiet $PIP_FLAGS --upgrade pillow numpy imageio-ffmpeg

# --- 3) vérification -----------------------------------------------------------
python3 - <<'PY'
import PIL, numpy, imageio_ffmpeg, shutil
ff = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()
print(f"▸ pillow  : {PIL.__version__}")
print(f"▸ numpy   : {numpy.__version__}")
print(f"▸ ffmpeg  : {ff}")
import subprocess
v = subprocess.run([ff, "-version"], capture_output=True, text=True).stdout.splitlines()[0]
print(f"            {v}")
PY

echo
echo "✅ environnement prêt."
echo "   test rapide : python3 lyricvideo.py --song \"Noukiko\" --preview \\"
echo "                        --photo \"../Snapchat-539918723.jpg\""
echo
echo "── Termux (Android) ────────────────────────────────────────────────────────"
echo "   pkg update -y; pkg install -y python ffmpeg"
echo "   pip install pillow numpy"
echo "   # puis : python3 lyricvideo.py --song \"Noukiko\" --photo \"/storage/emulated/0/DCIM/photo.jpg\""
