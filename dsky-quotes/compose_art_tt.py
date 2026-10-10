#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSKY QUOTES — Variantes TIKTOK v2 (zone sûre réelle).

TikTok recouvre : ~250 px en HAUT (barre de recherche) et ~330 px en BAS
(pseudo, légende, titre musical, barre de progression).

Recette :
  · l'œuvre est décalée vers le bas de 250 px (sa citation passe SOUS la
    barre de recherche) ; on rogne 250 px en bas de la base (zone sombre) ;
  · TOUT le branding (badge DSKY + N° + signature + CTA) est dans le bloc
    bas, qui se termine ~y=1570 → plus rien n'est masqué.
Sortie : saison-02/tiktok/quote-NN-tiktok.jpg

v3 (demande user) : TikTok ONLY pour les nouvelles salves ; bloc bas
aéré (badge 1345, signature 1478, CTA 1560, gaps elargis) ; filtre argv
pour ne composer que les numeros donnes : python3 compose_art_tt.py 191 192 ...
"""
import os
import sys
from PIL import Image, ImageDraw
from compose import (ROOT, montserrat, draw_tracking, tracking_w, draw_badge,
                     draw_flag, grain, STYLES)
from compose_s2 import icon_heart, icon_comment, icon_share, icon_plus
from compose_art import ART

W, H = 1080, 1920
SHIFT = 250          # décalage vertical de l'œuvre (sous la barre TikTok)


def brand_tiktok(num):
    src = os.path.join(ROOT, f"assets/bases/base-{num}.jpg")
    base = Image.open(src).convert("RGB")
    if base.size != (W, H):
        r = max(W/base.width, H/base.height)
        base = base.resize((int(base.width*r)+1, int(base.height*r)+1), Image.LANCZOS)
        x0 = (base.width-W)//2; y0 = (base.height-H)//2
        base = base.crop((x0, y0, x0+W, y0+H))
    # on garde le haut de l'œuvre (citation intacte) et on rogne le bas sombre
    base = base.crop((0, 0, W, H-SHIFT))

    img = Image.new("RGB", (W, H), (8, 8, 10))
    img.paste(base, (0, SHIFT))
    img = img.convert("RGBA")

    acc = STYLES[ART[num]]["accent"]
    txt = STYLES[ART[num]]["text"]
    d = ImageDraw.Draw(img)
    m = int(W*0.06)

    # fondu noir en haut (asseye l'œuvre, aucun texte essentiel ici)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for i in range(0, 400):
        od.line([(0, i), (W, i)], fill=(8, 8, 10, max(0, 235 - int(235*i/400))))
    # léger voile bas derrière le branding
    for i in range(1280, H):
        t = (i-1280)/(H-1280)
        od.line([(0, i), (W, i)], fill=(8, 8, 10, int(150*t*t)))
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)

    # ---- bloc bas ZONE SÛRE : badge + N° ----
    yb = 1345
    draw_badge(img, m, yb, acc)
    fnum = montserrat(26, 700)
    t = f"N° {num}"
    wnum = tracking_w(d, t, fnum, 3)
    draw_tracking(d, (W-m-wnum, yb+14), t, fnum, acc+(255,), tr=3, shadow=(0, 0, 0, 170))

    # ---- signature + drapeaux ----
    fy = 1478
    d.rectangle([W/2-28, fy-36, W/2+28, fy-33], fill=acc+(255,))
    fsig = montserrat(25, 700)
    draw_tracking(d, (0, fy-10), "C. JÉSUTONDJI SAMUEL STEIN", fsig,
                  txt+(240,), tr=3.2, anchor_center_x=W/2, shadow=(0, 0, 0, 170))
    fsub = montserrat(14, 500)
    sub = "LYRICISTE  ·  BÉNIN"
    subw = tracking_w(d, sub, fsub, 3.6)
    draw_tracking(d, (0, fy+22), sub, fsub, acc+(220,), tr=3.6,
                  anchor_center_x=W/2, shadow=(0, 0, 0, 170))
    fw2, fh2, gap = 25, 17, 15
    for fx in (W/2-subw/2-gap-fw2, W/2+subw/2+gap):
        mflag = Image.new("L", (fw2, fh2), 0)
        ImageDraw.Draw(mflag).rounded_rectangle([0, 0, fw2, fh2], radius=3, fill=255)
        fl = Image.new("RGBA", (fw2, fh2))
        draw_flag(ImageDraw.Draw(fl), 0, 0, fw2, fh2)
        img.paste(fl, (int(fx), fy+23), mflag)

    # ---- CTA (aéré : gap 46, se termine ~y=1582, loin des overlays TikTok) ----
    cta = [("LIKE", icon_heart), ("COMMENTE", icon_comment),
           ("PARTAGE", icon_share), ("ABONNE-TOI", icon_plus)]
    fi = montserrat(19, 700); tr = 2; dotw, gaps = 24, 46
    blocks = [(w_, ic, tracking_w(d, w_, fi, tr)) for w_, ic in cta]
    total = sum(22+9+ww for _, _, ww in blocks) + 3*(dotw+gaps)
    x = W/2 - total/2; ycta = fy + 82
    for i, (word, icon, ww) in enumerate(blocks):
        icon(d, x+11, ycta+11, 22, acc+(255,))
        draw_tracking(d, (x+22+9, ycta), word, fi, txt+(235,), tr=tr, shadow=(0, 0, 0, 160))
        x += 22+9+ww
        if i < 3:
            d.ellipse([x+dotw/2-3, ycta+8, x+dotw/2+3, ycta+14], fill=acc+(255,))
            x += dotw+gaps

    grain(img, amount=4)
    out = os.path.join(ROOT, f"saison-02/tiktok/quote-{num}-tiktok.jpg")
    img.convert("RGB").save(out, quality=92, subsampling=0, optimize=True)
    print("✔", f"quote-{num}-tiktok.jpg  [TIKTOK v2 · {ART[num]}]")


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "saison-02/tiktok"), exist_ok=True)
    nums = [int(a) for a in sys.argv[1:]] or list(ART)
    for n in nums:
        brand_tiktok(n)
