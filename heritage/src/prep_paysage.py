#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prep_paysage.py — Version YouTube 16:9 (1920×1080).
- Canvas de travail 2496×1404 (Ken Burns), sorties propres dans assets/images/paysage/
- Badge « Daïsky Prod » en HAUT-GAUCHE, EXACTEMENT à la même position sur TOUTES les images
- Intro : titre + CTA (LIKE / ABONNE-TOI / PARTAGE) + mention Prod/Studio
- Outro : carte de crédits complète (slogan, prod, studio, contacts, lien)
- Cover : titrée + export livrables/Cover_Heritage_YT thumbnails
Règle durée : chaque image garde le même placement du badge (constante BADGE_POS).
"""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "images", "paysage")
RAWL = os.path.join(ROOT, "assets", "raw", "paysage")
LIV = os.path.join(ROOT, "livrables")
os.makedirs(RAWL, exist_ok=True)
os.makedirs(LIV, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

W, H = 2496, 1404          # ~16:9 (1.7774) — cible 1920×1080 après Ken Burns
S = W / 1920.0
BLEU = (11, 16, 38); OR = (242, 179, 61); CUIVRE = (217, 122, 43); IVOIRE = (245, 239, 223); NOIR = (5, 7, 15)

BADGE_POS = (56, 44)       # position du badge Daïsky Prod (réf. 1920×1080) — IDENTIQUE PARTOUT

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

def text_center(d, cx, y, txt, f, fill, stroke=0, sf=NOIR):
    box = d.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    d.text((cx - (box[2]-box[0])/2, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sf)

def pill(d, cx, cy, txt, f, pad=(26, 14)):
    px, py = pad[0]*S, pad[1]*S
    b = d.textbbox((0, 0), txt, font=f)
    w = (b[2]-b[0]) + 2*px; h2 = (b[3]-b[1]) + 2*py
    x0, y0 = cx - w/2, cy - h2/2
    d.rounded_rectangle([x0, y0, x0+w, y0+h2], radius=h2/2, fill=(5,7,15,168), outline=OR, width=int(3*S))
    d.text((x0+px, y0+py - b[1]), txt, font=f, fill=IVOIRE)
    return x0 + w

def badge_daisky(d_overlay):
    """Badge Daïsky Prod — MÊME POSITION sur toutes les images."""
    f = font(30)
    x, y = BADGE_POS[0]*S, BADGE_POS[1]*S
    px, py = 22*S, 10*S
    b = d_overlay.textbbox((0, 0), "Daïsky Prod", font=f)
    w = (b[2]-b[0]) + 2*px; h2 = (b[3]-b[1]) + 2*py
    d_overlay.rounded_rectangle([x, y, x+w, y+h2], radius=h2/2, fill=(5,7,15,160), outline=OR, width=int(2.5*S))
    d_overlay.text((x+px, y+py - b[1]), "Daïsky Prod", font=f, fill=OR)

def base_with_badge(im):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    badge_daisky(ImageDraw.Draw(ov))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"), ov

def main():
    noms = ["01_intro","02_refrain","03_couplet1_pere","04_couplet1_mere","05_prerefrain",
            "06_couplet2","07_pont","08_refrain_final","09_outro","10_cover"]
    for n in noms:
        src = os.path.join(IMG, n + ".jpg")
        raw_dst = os.path.join(RAWL, n + ".jpg")
        if not os.path.exists(raw_dst):
            shutil.copy2(src, raw_dst)
        im = prep(Image.open(src).convert("RGB"))

        if n == "01_intro":
            base, ov = base_with_badge(im)
            d = ImageDraw.Draw(ov)
            text_center(d, W/2, 70*S, "HÉRITAGE DE MES PARENTS", font(52), OR, stroke=1)
            text_center(d, W/2, 140*S, "Daïsky  •  Wolof TechStein beat wê !", font(30, FR), IVOIRE)
            labels = ["\u2665 LIKE", "\u271A ABONNE-TOI", "\u2197 PARTAGE"]
            f = font(28)
            ws = [(d.textbbox((0,0),t,font=f)[2] - d.textbbox((0,0),t,font=f)[0]) + 2*26*S for t in labels]
            gap = 26*S; x = (W - (sum(ws) + 2*gap)) / 2
            for t, w in zip(labels, ws):
                pill(d, x + w/2, 218*S, t, f); x += w + gap
            d.text((56*S, (1080-64)*S), "Prod : Daïsky Prod  •  Studio : TechStein",
                   font=font(24, FR), fill=IVOIRE, stroke_width=int(1.5*S), stroke_fill=NOIR)
            Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").save(os.path.join(IMG, "01_intro_cta.jpg"), quality=93)
            print("OK 01_intro_cta")

        elif n == "09_outro":
            base, ov = base_with_badge(im)
            d = ImageDraw.Draw(ov)
            x0 = 90*S
            d.text((x0, 150*S), "HÉRITAGE DE MES PARENTS", font=font(46), fill=OR, stroke_width=1, stroke_fill=NOIR)
            d.text((x0, 215*S), "DAÏSKY", font=font(38, FSB), fill=IVOIRE)
            d.text((x0, 275*S), "Wolof TechStein beat wê !", font=font(28, FS), fill=CUIVRE)
            d.line([(x0, 330*S), (x0+640*S, 330*S)], fill=CUIVRE, width=int(2*S))
            d.text((x0, 352*S), "Prod : Daïsky Prod", font=font(27, FR), fill=IVOIRE)
            d.text((x0, 396*S), "Studio : TechStein", font=font(27, FR), fill=IVOIRE)
            d.text((x0, 452*S), "Contact : +229 01 61 16 24 08 / 01 49 11 49 51", font=font(25, FR), fill=IVOIRE)
            d.text((x0, 494*S), "techsteinsecureway@gmail.com", font=font(25, FR), fill=IVOIRE)
            d.text((x0, 536*S), "daiskyproduction@gmail.com", font=font(25, FR), fill=IVOIRE)
            d.text((x0, 592*S), "linktr.ee/daiskypro", font=font(27, FB), fill=OR)
            Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").save(os.path.join(IMG, "09_outro_card.jpg"), quality=93)
            print("OK 09_outro_card")

        elif n == "10_cover":
            base, ov = base_with_badge(im)
            d = ImageDraw.Draw(ov)
            text_center(d, W/2, 60*S, "DAÏSKY", font(34, FB), IVOIRE, stroke=1)
            text_center(d, W/2, 115*S, "HÉRITAGE", font(120), OR, stroke=2)
            text_center(d, W/2, 275*S, "DE MES PARENTS", font(42, FSB), IVOIRE, stroke=2)
            d.line([(W/2 - 320*S, 348*S), (W/2 + 320*S, 348*S)], fill=OR, width=int(2*S))
            # tagline déplacée en bas à droite (la barque lumineuse occupe le centre)
            bt = "Wolof TechStein beat wê !"
            f = font(26, FS)
            b = d.textbbox((0, 0), bt, font=f)
            d.text((W - (b[2]-b[0]) - 56*S, (1080-60)*S), bt, font=f, fill=CUIVRE,
                   stroke_width=int(1.5*S), stroke_fill=NOIR)
            cov = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
            cov.save(os.path.join(IMG, "10_cover_titled.jpg"), quality=93)
            cov.resize((1920, 1080), Image.LANCZOS).save(os.path.join(LIV, "Cover_Heritage_YT_1920x1080.jpg"), quality=95)
            cov.resize((1280, 720), Image.LANCZOS).save(os.path.join(LIV, "Cover_Heritage_YT_1280x720.jpg"), quality=95)
            print("OK cover YT")

        else:
            base, _ = base_with_badge(im)
            base.save(os.path.join(IMG, n + ".jpg"), quality=93)
            print("OK", n)
    print("Terminé.")

if __name__ == "__main__":
    main()
