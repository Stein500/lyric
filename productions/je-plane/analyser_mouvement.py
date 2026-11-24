#!/usr/bin/env python3
"""Mesure le mouvement sur des fenêtres temporelles ; ne confond pas bruit et travelling."""
from pathlib import Path
import cv2
import numpy as np
import sys

video = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'livrables/JE-PLANE-DSKY-LYRICS-9x16.mp4'
cap = cv2.VideoCapture(str(video))
if not cap.isOpened(): raise SystemExit(f'Impossible de lire {video}')
fps=cap.get(cv2.CAP_PROP_FPS)
print(f'Vidéo: {video.name} ; cadence {fps:g} i/s')
# Les analyses de translation portent sur le décor autour du personnage, au-dessus des sous-titres.
for start in (7.0, 16.0, 46.0, 80.0, 115.0, 130.0, 160.0, 174.0):
    cap.set(cv2.CAP_PROP_POS_FRAMES,round(start*fps)); frames=[]
    for i in range(61):
        ok,img=cap.read()
        if not ok: break
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray=cv2.resize(gray[200:900,140:940],(400,350),interpolation=cv2.INTER_AREA)
        frames.append(gray)
    if len(frames)<61: print(f'{start:g}s : trames insuffisantes'); continue
    diffs=np.array([np.mean(cv2.absdiff(a,b)) for a,b in zip(frames,frames[1:])])
    identical=sum(np.array_equal(a,b) for a,b in zip(frames,frames[1:]))
    a,b=frames[0].astype(np.float32),frames[30].astype(np.float32)
    shift,score=cv2.phaseCorrelate(a,b)
    print(f'{start:6.2f}–{start+2:6.2f}s : diff moyenne {diffs.mean():.3f}/255 par image, '
          f'{identical}/60 paires identiques dans la zone ; translation sur 1 s '
          f'({shift[0]*2:+.2f}, {shift[1]*2:+.2f}) px natifs, fiabilité {score:.2f}')
cap.release()
