#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyse du signal (PAS une ecoute humaine) pour les bornes du teaser 15,00 s."""
import array, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from outils import ffmpeg_exe
FF, VER = ffmpeg_exe()
AUDIO = os.path.abspath(os.path.join(HERE, "..", "..", "Grand marcheur 2.mp3"))
SR = 16000
raw = subprocess.check_output([FF, "-hide_banner", "-loglevel", "error", "-i", AUDIO,
                               "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
s = array.array("h"); s.frombytes(raw)
WIN = int(0.02 * SR)                      # 20 ms
rms = []
for k in range(0, len(s) - WIN, WIN):
    chunk = s[k:k + WIN]
    rms.append((k / SR, (sum(v * v for v in chunk) / WIN) ** 0.5))
def best(t, span=1.2):
    cands = [(t0, r) for t0, r in rms if abs(t0 - t) <= span]
    return min(cands, key=lambda x: x[1])
a = best(164.99); b = best(179.99)
# 15,00 s exactes : on cale la fin sur le debut retenu + 15,00
start = round(a[0], 2)
end = round(start + 15.00, 2)
rep = {"outil": VER, "methode": "RMS par fenetre de 20 ms sur PCM decode 16 kHz mono ; minimum local d'energie autour des bornes proposees",
       "attention": "analyse de signal, PAS ecoute humaine ; ne garantit pas l'absence de coupe de syllabe tenue",
       "bornes_proposees": [164.99, 179.99],
       "minimum_energie_debut": {"t": round(a[0], 2), "rms": round(a[1], 1)},
       "minimum_energie_fin": {"t": round(b[0], 2), "rms": round(b[1], 1)},
       "bornes_ajustees_15s": [start, end], "duree": round(end - start, 2),
       "etat": "PROPOSITION, a valider"}
with open(os.path.join(HERE, "teaser_bounds.json"), "w", encoding="utf-8") as fh:
    json.dump(rep, fh, ensure_ascii=False, indent=2); fh.write("\n")
print("ffmpeg:", VER)
print("minimum debut:", rep["minimum_energie_debut"], "| minimum fin:", rep["minimum_energie_fin"])
print("bornes ajustees 15,00 s:", rep["bornes_ajustees_15s"])
