#!/usr/bin/env bash
# Pipeline complet : 9:16 -> 16:9 -> master + covers.
# Pré-requis : 5 fonds dans assets/raw/portrait/ ET 5 dans assets/raw/landscape/.
set -e
cd "$(dirname "$0")/.."
PY=/tmp/lyric-venv/bin/python
$PY scripts/rendu_9x16.py
$PY scripts/rendu_16x9.py
$PY scripts/master_et_covers.py
echo
echo "=== TOUT EST DANS livrables/ ==="
ls -lh livrables/
