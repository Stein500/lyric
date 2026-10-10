#!/usr/bin/env python3
"""Controle des fonds 9:16 d'une production (ici : Gbetche vivi, version anim/studio).

Verifie ce que l'artiste a demande a l'artiste : aucune coupe en haut ni en bas.
  - ratio reel de chaque fichier (le montage applique un scale pur, jamais un crop)
  - presence de bandes noires en tete / en queue (interdites par v5.7 S2)
  - marge estimee au-dessus du sommet de la tete (zone badge y 0 -> 144)
  - densite de contours dans les 8 % hauts et les 18 % bas (zones a preserver)
  - planche contact JPG pour la validation de l'artiste

Usage : venv/bin/python productions/gbetche-vivi/qa_fonds.py
"""
import glob, os, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
PERS = os.path.join(ROOT, "personnages")
TOP, BOT = 0.08, 0.18          # safe zones 9:16 (144/1920 et 346/1920)
HEADROOM_MIN = 0.06            # 6 % d'air mini au-dessus du crane


def measure(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    g = np.asarray(im.convert("L")).astype(np.int16)
    rowmax = g.max(axis=1)
    def run(a):
        c = 0
        for v in a:
            if v < 10:
                c += 1
            else:
                break
        return c
    black_top, black_bot = run(rowmax), run(rowmax[::-1])
    gy = np.abs(np.diff(g, axis=0))[:, :-1]
    gx = np.abs(np.diff(g, axis=1))[:-1, :]
    edges = np.maximum(gy, gx) > 28
    t, b = int(h * TOP), int(h * BOT)
    band = edges[: int(h * 0.5)]
    head = int(np.argmax(band.any(axis=1))) / h if band.any() else 1.0
    # artefact "cadre blanc" : liseré clair parallèle a un bord, a 2-14 % de celui-ci
    lum = g.astype(np.float32)
    def line(ax, axis):
        prof = ax.max(axis=axis)
        n = len(prof)
        for i in range(int(n * 0.02), int(n * 0.14)):
            if prof[i] > 175 and prof[max(0, i - 4):i + 5].min() > 120:
                return True
        return False
    framed = line(lum, 1) or line(lum[::-1], 1) or line(lum, 0) or line(lum[:, ::-1], 0)
    return dict(size=(w, h), ratio=w / h, black_top=black_top, black_bot=black_bot,
                edge_top=float(edges[:t].mean()) if t else 0.0,
                edge_bot=float(edges[-b:].mean()) if b else 0.0,
                framed=framed,
                headroom=head, ok=(abs(w / h - 9 / 16) < 0.01 and black_top == 0
                                   and black_bot == 0 and head >= HEADROOM_MIN))


def contact_sheet(files, out, cols=3, tw=300):
    th = int(tw * 16 / 9)
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 40) + 12), (16, 16, 18))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB")
        im.thumbnail((tw, th))
        x = 12 + (i % cols) * (tw + 12)
        y = 12 + (i // cols) * (th + 40)
        sheet.paste(im, (x, y))
        d.text((x + 2, y + th + 10), os.path.basename(f).replace(".png", ""), fill=(238, 238, 238))
    sheet.save(out, quality=90)
    return sheet.size


def main():
    pat = sys.argv[1] if len(sys.argv) > 1 else "anim-*"
    files = sorted(glob.glob(os.path.join(PERS, pat)))
    ancre = os.path.join(PERS, "ancre-anim-01.png")
    if os.path.exists(ancre):
        files = [ancre] + files
    if not files:
        print(f"aucun fichier pour {pat}")
        return 1
    bad = []
    print(f"{'fichier':18s}{'taille':>11s}{'ratio':>8s}{'noirH':>6s}{'noirB':>6s}{'airTete':>9s}{'cdtH8%':>8s}{'cdtB18%':>8s}{'liseré':>8s} verdict")
    for p in files:
        r = measure(p)
        v = "OK" if r["ok"] else "A VERIFIER"
        if not r["ok"]:
            bad.append(os.path.basename(p))
        print(f"{os.path.basename(p).replace('.png',''):18s}{r['size'][0]}x{r['size'][1]:>5d}"
              f"{r['ratio']:8.4f}{r['black_top']:6d}{r['black_bot']:6d}{r['headroom']*100:8.1f}%"
              f"{r['edge_top']*100:7.1f}%{r['edge_bot']*100:7.1f}%{'oui' if r['framed'] else 'non':>8s} {v}")
    out = os.path.join(ROOT, "PLANCHE-%s.jpg" % pat.replace("*", "all"))
    print("planche :", contact_sheet(files, out), out)
    print("alertes :", bad if bad else "aucune")
    return 0 if not bad else 2


if __name__ == "__main__":
    sys.exit(main())
