#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""facescan.py — trouve le bas du visage pour ne jamais poser de lettres dessus.

Détecte la plus grande tache de couleur peau de la moitié haute, puis renvoie son
bas. Écrit `typo_offsets.json` : décalage vertical du bloc de paroles par plan.

  python3 facescan.py            # analyse tous les fonds, écrit les décalages
  python3 facescan.py --show     # n'écrit rien, affiche seulement
"""
import glob, json, os, sys
import numpy as np
from PIL import Image

from lettering import BOX

HERE = os.path.dirname(os.path.abspath(__file__))
S = 4                       # sous-échantillonnage de l'analyse


def face_bottom(im):
    """(x0, y0, x1, y1, aire) du plus gros amas de peau dans la moitié haute, en natif."""
    a = np.asarray(im.convert("RGB"), dtype=np.int16)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    mx, mn = a.max(axis=2), a.min(axis=2)
    skin = ((r > 70) & (r < 245) & (r > g + 14) & (g > b - 4) & (g < r - 6)
            & ((mx - mn) > 26) & (b < 190))
    small = skin[::S, ::S].copy()
    small[:, :] &= np.arange(small.shape[1])[None, :] > 40          # ignore les bords
    H2 = small.shape[0]
    small[int(H2 * 0.62):, :] = False                               # moitié haute seulement
    lab = np.zeros(small.shape, dtype=np.int32)
    best, cur = None, 0
    h, w = small.shape
    for y in range(h):
        for x in range(w):
            if not small[y, x] or lab[y, x]:
                continue
            cur += 1
            stack, lab[y, x] = [(y, x)], cur
            n, ys, xs = 0, [], []
            while stack:
                cy, cx = stack.pop()
                n += 1
                ys.append(cy); xs.append(cx)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and small[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = cur
                            stack.append((ny, nx))
            if n > 900 and (best is None or n > best[0]):
                best = (n, min(xs), min(ys), max(xs), max(ys))
    if not best:
        return None
    n, x0, y0, x1, y1 = best
    return (x0 * S, y0 * S, x1 * S, y1 * S, n)


def main():
    show = "--show" in sys.argv
    off = {}
    for p in sorted(glob.glob(os.path.join(HERE, "fonds", "*.png"))):
        name = os.path.basename(p)
        f = face_bottom(Image.open(p))
        if not f:
            print("%-16s pas de visage détecté" % name)
            continue
        x0, y0, x1, y1, n = f
        dy = max(0, y1 + 26 - BOX[1])
        if y1 + 26 > 1376 - (BOX[3] - BOX[1]):
            dy = 0                       # impossible : on ne pousse pas hors cadre
        off[name] = int(dy)
        print("%-16s menton y=%-4d boîte x %d→%d  aire %-6d  dy=%d"
              % (name, y1, x0, x1, n, dy))
    if not show:
        json.dump(off, open(os.path.join(HERE, "typo_offsets.json"), "w"), indent=1, sort_keys=True)
        print("\nécrit typo_offsets.json —", len(off), "plans")


if __name__ == "__main__":
    main()
