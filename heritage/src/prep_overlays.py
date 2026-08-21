#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prep_overlays.py — Prépare les visuels finaux 1400x2489 (9:16) à partir des images générées.
- Recadre/upscale proprement (Lanczos)
- 01_intro_cta.jpg       : intro + badges CTA (LIKE / ABONNE-TOI / PARTAGE) + titre + @daiskypro
- 09_outro_card.jpg      : outro + carte de fin (artiste + linktree)
- out/Cover_Heritage_1080x1920.jpg : couverture plateforme titrée
- out/pochette_1400.jpg  : pochette carrée pour le tag APIC du MP3 propre
Les originaux bruts sont sauvegardés dans assets/raw/ (une seule fois).
"""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "images")
RAW = os.path.join(ROOT, "assets", "raw")
OUT = os.path.join(ROOT, "livrables")
os.makedirs(RAW, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H = 1400, 2489  # canvas de travail 9:16 (zoompan y piochera)
S = W / 1080.0     # facteur d'échelle vs 1080

BLEU_NUIT = (11, 16, 38)
OR = (242, 179, 61)
CUIVRE = (217, 122, 43)
IVOIRE = (245, 239, 223)

def font(px):
    return ImageFont.truetype(FONT_BOLD, int(px * S))

def prep_cover(im):
    """Recadre centre au ratio 9:16 puis redimensionne en W x H."""
    tr = W / H
    w, h = im.size
    r = w / h
    if r > tr:   # trop large -> coupe les côtés
        nw = int(h * tr); x = (w - nw) // 2
        im = im.crop((x, 0, x + nw, h))
    else:        # trop haut -> coupe haut/bas (léger ici)
        nh = int(w / tr); y = (h - nh) // 2
        im = im.crop((0, y, w, y + nh))
    return im.resize((W, H), Image.LANCZOS)

def text_center(d, cx, y, txt, f, fill, stroke=0, stroke_fill=(0,0,0)):
    box = d.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    tw = box[2] - box[0]
    d.text((cx - tw/2, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)

def pill(d, cx, cy, txt, f, pad_x=26*S, pad_y=14*S):
    box = d.textbbox((0, 0), txt, font=f)
    tw, th = box[2]-box[0], box[3]-box[1]
    w = tw + 2*pad_x; h2 = th + 2*pad_y
    x0, y0 = cx - w/2, cy - h2/2
    d.rounded_rectangle([x0, y0, x0+w, y0+h2], radius=h2/2,
                        fill=(5, 7, 15, 165), outline=OR, width=int(3*S))
    d.text((x0 + pad_x, y0 + pad_y - box[1]), txt, font=f, fill=IVOIRE)
    return x0+w

def badges_cta(d, cy):
    labels = ["\u2665 LIKE", "\u271A ABONNE-TOI", "\u2197 PARTAGE"]
    f = font(30)
    boxes = [d.textbbox((0,0), t, font=f) for t in labels]
    ws = [(b[2]-b[0]) + 2*26*S for b in boxes]
    gap = 24*S
    total = sum(ws) + 2*gap
    x = (W - total)/2
    for t, w in zip(labels, ws):
        pill(d, x + w/2, cy, t, f)
        x += w + gap

def main():
    names = ["01_intro", "02_refrain", "03_couplet1_pere", "04_couplet1_mere",
             "05_prerefrain", "06_couplet2", "07_pont", "08_refrain_final",
             "09_outro", "10_cover"]
    for n in names:
        src = os.path.join(IMG, n + ".jpg")
        if not os.path.exists(src):
            src = os.path.join(RAW, n + ".jpg")  # déjà déplacé
        dst_raw = os.path.join(RAW, n + ".jpg")
        if not os.path.exists(dst_raw):
            shutil.copy2(src, dst_raw)
        im = prep_cover(Image.open(src).convert("RGB"))

        if n == "01_intro":
            im.save(os.path.join(RAW, "01_intro_clean.jpg"), quality=95)
            overlay = Image.new("RGBA", (W, H), (0,0,0,0))
            d = ImageDraw.Draw(overlay)
            text_center(d, W/2, 190*S, "HÉRITAGE DE MES PARENTS", font(40), OR, stroke=1)
            text_center(d, W/2, 250*S, "Daïsky  •  Wolof TechStein beat wê !", font(26), IVOIRE)
            badges_cta(d, 350*S)
            d.text((52*S, 2240*S), "@daiskypro", font=font(28), fill=IVOIRE, stroke_width=2, stroke_fill=(5,7,15))
            im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
            im.save(os.path.join(IMG, "01_intro_cta.jpg"), quality=93)
            print("OK 01_intro_cta.jpg")

        elif n == "09_outro":
            overlay = Image.new("RGBA", (W, H), (0,0,0,0))
            d = ImageDraw.Draw(overlay)
            text_center(d, W/2, 200*S, "HÉRITAGE DE MES PARENTS", font(38), IVOIRE, stroke=1)
            text_center(d, W/2, 262*S, "DAÏSKY", font(52), OR, stroke=1)
            d.line([(W/2 - 320*S, 348*S), (W/2 + 320*S, 348*S)], fill=CUIVRE, width=int(2*S))
            text_center(d, W/2, 372*S, "linktr.ee/daiskypro", font(30), OR)
            im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
            im.save(os.path.join(IMG, "09_outro_card.jpg"), quality=93)
            print("OK 09_outro_card.jpg")

        elif n == "10_cover":
            overlay = Image.new("RGBA", (W, H), (0,0,0,0))
            d = ImageDraw.Draw(overlay)
            text_center(d, W/2, 175*S, "DAÏSKY", font(40), IVOIRE, stroke=1)
            text_center(d, W/2, 255*S, "HÉRITAGE", font(120), OR, stroke=2, stroke_fill=(5,7,15))
            text_center(d, W/2, 445*S, "DE MES PARENTS", font(52), IVOIRE, stroke=2, stroke_fill=(5,7,15))
            d.line([(W/2 - 290*S, 545*S), (W/2 + 290*S, 545*S)], fill=OR, width=int(2*S))
            text_center(d, W/2, 575*S, "Wolof TechStein beat wê !", font(30), CUIVRE)
            cov = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
            cov.save(os.path.join(IMG, "10_cover_titled.jpg"), quality=93)
            cov1080 = cov.resize((1080, 1920), Image.LANCZOS)
            cov1080.save(os.path.join(OUT, "Cover_Heritage_1080x1920.jpg"), quality=95)
            # pochette carrée pour APIC
            sq = cov.crop(((W-1400)//2, (H-1400)//2, (W+1400)//2, (H+1400)//2))
            sq.save(os.path.join(OUT, "pochette_1400.jpg"), quality=95)
            print("OK cover + pochette")

        else:
            im.save(os.path.join(IMG, n + ".jpg"), quality=93)
            print("OK", n)
    print("Terminé.")

if __name__ == "__main__":
    main()
