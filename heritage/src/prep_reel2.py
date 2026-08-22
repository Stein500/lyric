#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prep_reel2.py — Idem prep_reel.py mais générique : dossier passé en argument.
Usage : python3 prep_reel2.py reel2
- Canvas 1400×2489, badge « Daïsky Prod » haut-gauche MÊME position partout
- CTA jaunes sur la 1ʳᵉ et la dernière image (par ordre alphabétique) + @daiskypro sur la dernière
- Raws sauvegardés dans assets/raw/<dossier>/
"""
import glob, os, shutil, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = sys.argv[1] if len(sys.argv) > 1 else "reel"
IMG = os.path.join(ROOT, "assets", "images", DOSSIER)
RAW = os.path.join(ROOT, "assets", "raw", DOSSIER)
os.makedirs(RAW, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H = 1400, 2489
S = W / 1080.0
JAUNE = (255, 214, 60); NOIR = (15, 12, 20); OR = (242, 179, 61); IVOIRE = (245, 239, 223)

def font(px, path=FB):
    return ImageFont.truetype(path, int(px * S))

def prep(im):
    tr = W / H
    w, h = im.size
    if w / h > tr:
        nw = int(h * tr); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / tr); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    return im.resize((W, H), Image.LANCZOS)

def badge(d):
    f = font(30)
    x, y = 56*S, 44*S
    px, py = 22*S, 10*S
    b = d.textbbox((0, 0), "Daïsky Prod", font=f)
    w = (b[2]-b[0]) + 2*px; h2 = (b[3]-b[1]) + 2*py
    d.rounded_rectangle([x, y, x+w, y+h2], radius=h2/2, fill=(15,12,20,190), outline=OR, width=int(3*S))
    d.text((x+px, y+py - b[1]), "Daïsky Prod", font=f, fill=OR)

def pill_jaune(d, cx, cy, txt, f):
    px, py = 26*S, 14*S
    b = d.textbbox((0, 0), txt, font=f)
    w = (b[2]-b[0]) + 2*px; h2 = (b[3]-b[1]) + 2*py
    x0, y0 = cx - w/2, cy - h2/2
    d.rounded_rectangle([x0, y0, x0+w, y0+h2], radius=h2/2, fill=JAUNE, outline=NOIR, width=int(4*S))
    d.text((x0+px, y0+py - b[1]), txt, font=f, fill=NOIR)
    return x0 + w

def cta_row(d, cy):
    labels = ["\u2665 LIKE", "\u271A ABONNE-TOI", "\u2197 PARTAGE"]
    f = font(30)
    ws = [(d.textbbox((0,0),t,font=f)[2] - d.textbbox((0,0),t,font=f)[0]) + 2*26*S for t in labels]
    gap = 22*S
    x = (W - (sum(ws) + 2*gap)) / 2
    for t, w in zip(labels, ws):
        pill_jaune(d, x + w/2, cy, t, f)
        x += w + gap

def main():
    fichiers = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(IMG, "r*.jpg")))
    assert fichiers, f"Aucune image dans {IMG}"
    premier, dernier = fichiers[0], fichiers[-1]
    for n in fichiers:
        src = os.path.join(IMG, n + ".jpg")
        raw_dst = os.path.join(RAW, n + ".jpg")
        if not os.path.exists(raw_dst):
            shutil.copy2(src, raw_dst)
        im = prep(Image.open(os.path.join(RAW, n + ".jpg")).convert("RGB"))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        badge(d)
        if n in (premier, dernier):
            cta_row(d, 170*S)
        if n == dernier:
            b = d.textbbox((0, 0), "@daiskypro", font=font(30))
            d.text(((1080-56)*S - (b[2]-b[0]), 44*S + 10*S - b[1]), "@daiskypro", font=font(30),
                   fill=IVOIRE, stroke_width=int(3*S), stroke_fill=NOIR)
        Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").save(src, quality=93)
        print("OK", n)
    print(f"Terminé ({DOSSIER}) : {len(fichiers)} images, CTA sur {premier} + {dernier}")

if __name__ == "__main__":
    main()
