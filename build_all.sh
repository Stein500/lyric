#!/usr/bin/env bash
# 🚀 BUILD_ALL.SH — Build complet (cover + vidéos + MP3) — 1 commande
# Usage : bash build_all.sh
# Ce script ne dépend de rien d'autre que du venv (setup_venv.sh) et des assets commitées.
set -e
cd "$(dirname "$0")"
source tools_venv/bin/activate

echo ""
echo "==========================================================="
echo " 🎨 1/3  Cover pro"
echo "==========================================================="
python build_cover.py

echo ""
echo "==========================================================="
echo " 🎬 2/3  Vidéos lyrics (9:16 + 16:9 + vérifications auto)"
echo "==========================================================="
python build_video.py

echo ""
echo "==========================================================="
echo " 🎧 3/3  MP3 320kbps (tags propres + cover, 0 suno/c2pa)"
echo "==========================================================="
python build_mp3.py

echo ""
echo "==========================================================="
echo " 🏁 TOUS LES LIVRABLES SONT DANS ./livrables/"
echo "==========================================================="
ls -lh livrables/
