#!/usr/bin/env python3
"""Slots exhaustifs, un fond par vers distinct, réutilisation si texte identique."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=json.loads((ROOT/'work/timings_validated.json').read_text())
DIR=ROOT/'assets/nonvi_konou'
START={0:'s00_intro',1:'s01_wolof',2:'s02_yeah',3:'s03_on_est_la',4:'ancre_01',
       5:'s05_misere',6:'s06_dokpe',7:'s07_vivi',8:'s08_beat',9:'s09_millions'}
unique=list(dict.fromkeys(line['text'] for line in REPORT['lines']))
slots=[dict(index=0,slot=START[0],text='INTRO INSTRUMENTALE',occurrences=[],
            image=f'{START[0]}_habillee.png')]
for i,text in enumerate(unique,1):
    slug=START.get(i,f's{i:02d}')
    slots.append(dict(index=i,slot=slug,text=text,
                      occurrences=[l['start'] for l in REPORT['lines'] if l['text']==text],
                      image=f'{slug}_habillee.png'))
slots.append(dict(index=len(unique)+1,slot=f's{len(unique)+1:02d}_endcard',
                  text='ENDCARD',occurrences=[],image=f's{len(unique)+1:02d}_endcard_habillee.png'))
for s in slots:s['status']='created' if (DIR/s['image']).exists() else 'pending'
assert len(slots)==37 and sum(s['status']=='created' for s in slots)>=10
path=DIR/'plan_images.json'
path.write_text(json.dumps(slots,ensure_ascii=False,indent=2)+'\n')
print(path, len(slots),'slots,',sum(s['status']=='created' for s in slots),'réalisés')
