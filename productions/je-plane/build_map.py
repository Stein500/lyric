#!/usr/bin/env python3
"""Reconstitue la carte à partir des horodatages fournis, sans inventer les fins."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
source = ROOT / 'Je plane.txt'
pattern = re.compile(r'^\[(\d+):(\d+\.\d+)\](.*)$')
entries = []
seen = set()
for line in source.read_text(encoding='utf-8').splitlines():
    m = pattern.match(line)
    if not m:
        continue
    i = len(entries) + 1
    text = m.group(3)
    # Réutilisation expressément demandée ; le refrain final reprend des images d'aube.
    reuse = {18: 2, 22: 5, 23: 6, 24: 7, 27: 20, 28: 15, 31: 19,
             32: 16, 33: 17, 34: 2, 35: 19, 37: 36, 38: 40, 39: 36,
             41: 40, 42: 40, 43: 36, 44: 36, 45: 40, 46: 40, 47: 36, 48: 40}
    image = f'fonds/vers-{reuse.get(i, i):02d}.png'
    if 'Wolof TechStein beat' in text:
        displayed = 'WTBW'  # Décision explicite de l'artiste, sans modification de l'audio.
    else:
        # [reference:0] est un marqueur technique, pas une parole ; source conservée intacte.
        displayed = re.sub(r'\[reference:\d+\]', '', text)
    entries.append({
        'i': i, 'debut_source': round(int(m.group(1)) * 60 + float(m.group(2)), 2),
        'fin': None, 'texte_source': text, 'texte_affiche': displayed,
        'image': image, 'disponible': (OUT / image).is_file(),
        'reprise': text in seen, 'statut_controle': 'non contrôlé',
    })
    seen.add(text)
(OUT / 'verses_map.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
lines = ['# Je plane — carte des vers', '', 'Débuts conservés ; fins, calage mot à mot et affichages signalés restent à vérifier.', '', '| N° | Début (s) | Paroles source | Image |', '|---:|---:|---|---|']
for row in entries:
    text = row['texte_source'].replace('|', '\\|')
    status = 'générée, à contrôler' if row['disponible'] else 'à générer'
    lines.append(f"| {row['i']} | {row['debut_source']:.2f} | {text} | {row['image']} — {status} |")
(OUT / 'CARTE-VERS.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'{len(entries)} vers ; {sum(e["disponible"] for e in entries)} plans disponibles ; {len({e["image"] for e in entries})} images distinctes utilisées')
