#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bake.py — cuit le lettrage du moteur dans chaque plan (ce que la vidéo montre).

v6.2 : le générateur ne peint aucun mot ; c'est lettering.py qui pose les paroles,
dans la boîte x 150→590 / y 470→750 du repère natif 768×1376.

  python3 bake.py            # tous les plans présents
  python3 bake.py v-01-nuit  # un seul
Sortie : fonds/cuits/<plan>.png (+ planche CONTROLE-paroles.jpg)
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deseam, lettering

FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "fonds", "cuits")
DOC = json.load(open(os.path.join(HERE, "verses_map.json"), encoding="utf-8"))


def lignes_par_plan():
    d = {}
    for v in DOC["vers"]:
        d.setdefault(v["image"], v.get("lignes") or [""])
    return d


def bake_one(name, lignes, clean=True):
    src = os.path.join(HERE, "fonds", name)
    im = Image.open(src).convert("RGB")
    if im.size != (768, 1376):
        im = im.resize((768, 1376), Image.LANCZOS)
    if clean:                     # pas de réparation sur les fonds v6.2 : ils sont déjà sains
        im = deseam.clean(im)
    l1 = lignes[0] if lignes else ""
    l2 = lignes[1] if len(lignes) > 1 else ""
    im = lettering.draw_lettering(im, l1, l2, os.path.join(FONTS, "Montserrat-ExtraBold.ttf"),
                                  dy=lettering.dy_for(name))
    os.makedirs(OUT, exist_ok=True)
    im.save(os.path.join(OUT, name))
    return im


def planche(noms, out):
    cols, tw = 5, 380
    th = int(tw * 1376 / 768)
    rows = (len(noms) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 10, rows * (th + 26) + 10), (10, 12, 16))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat-SemiBold.ttf"), 15)
    for k, n in enumerate(noms):
        im = Image.open(os.path.join(OUT, n)).resize((tw, th), Image.LANCZOS)
        x, y = 10 + (k % cols) * (tw + 10), 10 + (k // cols) * (th + 26)
        sheet.paste(im, (x, y))
        d.text((x + 3, y + th + 5), n.replace(".png", ""), font=f, fill=(232, 238, 248))
    sheet.save(out, quality=90)
    print(out, sheet.size)


def main():
    lp = lignes_par_plan()
    want = sys.argv[1:] or sorted(lp)
    done = []
    for name in want:
        name = os.path.basename(name)          # les clés de verses_map portent déjà "fonds/"
        if not name.endswith(".png"):
            name += ".png"
        if not os.path.exists(os.path.join(HERE, "fonds", name)):
            print("absent :", name)
            continue
        bake_one(name, lp.get("fonds/" + name, [""]))
        done.append(name)
        print("cuit :", name, "|", " / ".join(lp.get("fonds/" + name, [""])))
    planche(done, os.path.join(HERE, "CONTROLE-paroles.jpg"))


if __name__ == "__main__":
    main()
