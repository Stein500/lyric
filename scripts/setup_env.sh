#!/usr/bin/env bash
# Environnement régénérable ; aucun binaire ni cache ne doit être versionné.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r scripts/requirements-audio.txt
mkdir -p work/je_maime_tellement
printf '\nAnalyse : .venv/bin/python scripts/analyse_je_maime.py\n'
