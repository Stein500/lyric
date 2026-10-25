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


def heal(img, seams, band=36):
    if not seams:
        return img
    w, h = img.size
    for (y, _lvl) in seams:
        y0, y1 = max(0, y - band // 2), min(h, y + band // 2)
        patch = img.crop((0, y0, w, y1)).filter(ImageFilter.GaussianBlur(9))
        mask = Image.new("L", (w, y1 - y0), 0)
        px = mask.load()
        for j in range(y1 - y0):
            u = 1 - abs((j - (y1 - y0) / 2) / ((y1 - y0) / 2))     # 0 aux bords, 1 au centre
            v = int(255 * max(0.0, u) ** 0.8)
            for x in range(w):
                px[x, j] = v
        img = img.copy()
        img.paste(patch, (0, y0), mask)
    return img


def clean(img, step_min=14.0):
    return heal(img, find_seams(img, step_min=step_min))

if __name__ == "__main__":
    import sys, glob, os
    for f in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else "fonds/v-*-nuit.png")):
        im = Image.open(f).convert("RGB")
        s = find_seams(im)
        print(f"{os.path.basename(f):18s} coutures: {[(y, round(v,1)) for y, v in s]}")
