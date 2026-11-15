#!/usr/bin/env python3
"""Build a provisional verse/image inventory; no end times are inferred."""
import json, re
from pathlib import Path
root = Path(__file__).resolve().parent.parent
repo = root.parent.parent
images = [
'scene-01-ancre','scene-02-correction','scene-03-correction','scene-04-correction','scene-05-correction','scene-06-correction','scene-01-ancre',
'scene-07','scene-08-correction','scene-09-correction','scene-10-correction','scene-11-correction','scene-12','scene-13-correction',
'scene-14','scene-15','scene-16','scene-17-correction','scene-18','scene-03-correction','scene-04-correction','scene-05-correction',
'scene-06-correction','scene-01-ancre','scene-19-correction','scene-20','scene-21','scene-22','scene-23','scene-24',
'scene-25','scene-26','scene-15','scene-16','scene-17-correction','scene-18','scene-27-correction',
'scene-28','scene-29','scene-30-correction','scene-31-aube','scene-32-aube','scene-33-aube',
'scene-34-aube','scene-35-aube','scene-35-aube']
lines=[]
for line in (repo/'Sanguin.txt').read_text(encoding='utf-8').splitlines():
    m=re.match(r'^\[(\d+):(\d+\.\d+)\](.*)$', line)
    if m:
        timestamp=f'{m[1]}:{m[2]}'
        text=m[3].replace('\u200e','').strip()
        lines.append((timestamp,text))
if len(lines)!=len(images): raise ValueError('Le nombre de vers a changé : mise à jour de la carte nécessaire')
seen=set(); rows=[]
for i, ((t,text),name) in enumerate(zip(lines,images),1):
    image=f'portrait-1080x1920/{name}.jpg'
    display='WTBW' if text.startswith('Wolof TechStein beat') else text
    rows.append(dict(i=i, t=t, fin=None, texte_source=text, texte_affiche=display, image=image,
                     disponible=(root/image).exists(), reprise=name in seen, statut='provisoire_a_controler'))
    seen.add(name)
(root/'verses_map.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# Sanguin — carte des vers provisoire','', 'Horodatages source inchangés. Fins et durées non déterminées ; images et conformité à contrôler. La signature chantée est affichée WTBW sur décision de l’artiste.','', '| # | Début | Parole affichée | Image | Disponible |','|---|---|---|---|---|']
for r in rows:
    md.append(f"| {r['i']} | {r['t']} | {r['texte_affiche'].replace('|','/')} | {r['image']} | {'oui' if r['disponible'] else 'non'} |")
(root/'CARTE-VERS.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(f'{len(rows)} vers ; {sum(r["disponible"] for r in rows)} images disponibles ; fins non déterminées')
