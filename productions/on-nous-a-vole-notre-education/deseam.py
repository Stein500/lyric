# -*- coding: utf-8 -*-
"""deseam.py — répare la couture horizontale pleine largeur produite par le générateur.

Mesure : certaines images sortent avec une marche de niveau nette sur toute la largeur
(v-01 : +51 niveaux à y 1009 sur 93 % des colonnes), là où le modèle a « collé » deux
zones. On détecte la marche, puis on adoucit une bande de 36 px avec un masque fondu :
la couture disparaît sans toucher au reste de l'image.
"""
import numpy as np
from PIL import Image, ImageFilter

def find_seams(img, step_min=5.0, frac_min=0.50, ymin=120, ymax=1300):
    g = np.asarray(img.convert("L"), dtype=np.float32)
    d = np.diff(g, axis=0)
    level = np.abs(d.mean(axis=1))
    frac = (np.abs(d) > 5).mean(axis=1)
    out, last = [], -99
    for y in range(ymin, min(ymax, len(level))):
        if level[y] > step_min and frac[y] > frac_min and y - last > 40:
            out.append((y, float(level[y])))
            last = y
    return out


def heal(img, seams, band=70):
    """correction MINIMALE : on compense la marche de niveau sans toucher la texture.
    Trois tentatives mesurées et rejetées : flou local (bande lisse, écart-type 26->7),
    étirement vertical (traînées), miroir (duplique les stickers : cœur fantôme).
    On lisse donc uniquement la MOYENNE de chaque ligne sur 5 px, ce qui efface le
    saut de niveau en gardant chaque détail à sa place."""
    if not seams:
        return img
    w, h = img.size
    for (y, _lvl) in seams:
        y0, y1 = max(0, y - band), min(h, y + band)
        strip = img.crop((0, y0, w, y1))
        px = strip.load()
        rows = []
        for j in range(y1 - y0):
            row = [px[x, j] for x in range(w)]
            rows.append([sum(c) / 3.0 for c in row])
        # moyenne glissante sur 5 lignes -> on retire la marche, on garde le détail
        win = 5
        target = []
        for j in range(len(rows)):
            a, b = max(0, j - win // 2), min(len(rows), j + win // 2 + 1)
            target.append(sum(sum(r) for r in rows[a:b]) / ((b - a) * w))
        for j in range(len(rows)):
            delta = target[j] - (sum(rows[j]) / w)
            if abs(delta) < 0.6:
                continue
            k = 1.0 + delta / max(6.0, sum(rows[j]) / w)
            k = min(1.35, max(0.72, k))
            for x in range(w):
                r, g, b = px[x, j][:3]
                px[x, j] = (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)))
        img = img.copy()
        img.paste(strip, (0, y0))
    return img


def clean(img, step_min=14.0):
    return heal(img, find_seams(img, step_min=step_min))

if __name__ == "__main__":
    import sys, glob, os
    for f in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else "fonds/v-*-nuit.png")):
        im = Image.open(f).convert("RGB")
        s = find_seams(im)
        print(f"{os.path.basename(f):18s} coutures: {[(y, round(v,1)) for y, v in s]}")
