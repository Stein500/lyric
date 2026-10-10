#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detection de la tete/du visage dans un fond de la production (echelle source).

Pourquoi : la regle v5.7 « paroles centrees sur H/2 » peut poser le bloc de texte sur un
gros plan de visage. Le moteur de rendu appelle `face_box()` pour deplacer le bloc sous le
menton quand il y a chevauchement, puis `audit_overlap()` verifiera que **zero frame** ne
montre d'encre de parole dans la boite du visage.

Heuristique (volontairement simple, mesurable et reproductible, pas de modele externe) :
  1. cheveux = rangee sombre (Y < 60) de largeur 6 a 50 % de la frame, dans la colonne centrale ;
  2. visage = peau du rendu 3D (Cr 112-148, Cb 124-160, Y 35-215) dans la meme colonne ;
  3. boite = du sommet des cheveux jusqu'au bas du visage, elargie d'un padding.
"""
import os
import numpy as np
from PIL import Image

CENTER = (0.18, 0.82)      # bande de colonnes consideree (fraction de la largeur)
HAIR_Y = 60
PADDING = 0.035            # en fraction de la hauteur


def _masks(im):
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    y = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    cr = 128 - 0.168736 * a[..., 0] - 0.331264 * a[..., 1] + 0.5 * a[..., 2]
    cb = 128 + 0.5 * a[..., 0] - 0.418688 * a[..., 1] - 0.081312 * a[..., 2]
    hair = y < HAIR_Y
    skin = (cr > 112) & (cr < 148) & (cb > 124) & (cb < 160) & (y > 35) & (y < 215)
    return hair, skin, y


def face_box(path, scale=1.0):
    """Retourne (x0, y0, x1, y1) en pixels d'affichage (scale = 1080 / largeur source)."""
    im = Image.open(path)
    w, h = im.size
    hair, skin, _ = _masks(im)
    c0, c1 = int(w * CENTER[0]), int(w * CENTER[1])
    band = slice(c0, c1)
    bw = c1 - c0
    fg = (hair | skin)

    # sommet des cheveux : premiere rangee dont la contiguiter sombre depasse 6 % de la bande
    y_top = None
    for i in range(int(h * 0.03), int(h * 0.62)):
        row = hair[i, band]
        if not row.any():
            continue
        # plus longue sequence continue de cheveux
        idx = np.flatnonzero(row)
        runs = np.split(idx, np.where(np.diff(idx) > 2)[0] + 1)
        if max(len(r) for r in runs) / bw > 0.06:
            y_top = i
            break
    if y_top is None:
        rows = np.flatnonzero(fg[:, band].sum(axis=1) > bw * 0.10)
        rows = rows[(rows > h * 0.03) & (rows < h * 0.62)]
        if len(rows) == 0:
            return None
        y_top = int(rows[0])

    # bas du visage : derniere rangee (dans 45 % de hauteur) ou peau + cheveux tiennent >= 12 %
    lim = min(h, y_top + int(h * 0.45))
    y_bot = y_top
    last_ok = None
    for i in range(y_top, lim):
        cov = fg[i, band].mean()
        if cov >= 0.12:
            last_ok = i
        elif last_ok is not None and i - last_ok > int(h * 0.03):
            break
    y_bot = last_ok if last_ok is not None else min(lim, y_top + int(h * 0.12))

    # largeur : etendue horizontale des pixels visage sur les rangees retenues
    sub = skin[y_top:y_bot + 1, :]
    cols = np.flatnonzero(sub.any(axis=0))
    if len(cols) > 4:
        x0, x1 = int(cols[0]), int(cols[-1])
        pad = int((x1 - x0) * 0.18 + w * 0.02)
        x0, x1 = max(0, x0 - pad), min(w - 1, x1 + pad)
    else:
        x0, x1 = c0, c1
    pad_y = int(h * PADDING)
    y0 = max(0, y_top - pad_y)
    y1 = min(h - 1, y_bot + int(pad_y * 1.6))
    return tuple(int(v * scale) for v in (x0, y0, x1, y1))


def audit_overlap(frame_rgb, box, ink_mask):
    """Recouvrement encre de paroles / boite du visage, en pixels carres."""
    a = np.asarray(frame_rgb.convert("L")).astype(np.int16)
    del a
    x0, y0, x1, y1 = box
    inter = ink_mask[y0:y1 + 1, x0:x1 + 1]
    return int(inter.sum()) if inter.size else 0


if __name__ == "__main__":
    import glob, sys
    from PIL import ImageDraw
    pers = os.path.join(os.path.dirname(os.path.abspath(__file__)), "personnages")
    files = sorted(glob.glob(os.path.join(pers, "anim-*.png")))
    tw, th = 200, 358
    cols, rows = 5, (len(files) + 4) // 5
    sheet = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 24) + 8), (12, 12, 14))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB")
        box = face_box(f)
        ox, oy = 8 + (i % cols) * (tw + 8), 24 + (i // cols) * (th + 24)
        t = im.copy(); t.thumbnail((tw, th))
        sheet.paste(t, (ox, oy))
        d.text((ox + 2, oy + th + 4), os.path.basename(f).replace(".png", ""), fill=(235, 235, 235))
        if box:
            s_ = t.size[0] / im.size[0]
            d.rectangle([ox + box[0] * s_, oy + box[1] * s_, ox + box[2] * s_, oy + box[3] * s_],
                        outline=(255, 60, 60), width=2)
            print(os.path.basename(f).replace(".png", ""), "boite", box, "-> bas/hauteur %.3f" % (box[3] / im.size[1]))
        else:
            print(os.path.basename(f).replace(".png", ""), "AUCUNE BOITE")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "QC-boites-visage.jpg")
    sheet.save(out, quality=90)
    for f in files:
        print(os.path.basename(f).replace(".png", ""), face_box(f))
    print("QC ->", out)
