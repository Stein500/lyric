#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prep_story.py — Covers pro 1080×1920 pour Story / Statut WhatsApp (promo).
4 visuels : Reel 1, Reel 2, vidéo YouTube complète, son en streaming.
Style : sticker-bomb vivant (fonds raws) + blocs de texte pro (pilules jaunes, panneau sombre),
badge Daïsky Prod haut-gauche fixe, lien bio en bas.
Sortie : livrables/Story_*.jpg
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIV = os.path.join(ROOT, "livrables")
os.makedirs(LIV, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
W, H = 1080, 1920
JAUNE = (255, 214, 60); NOIR = (15, 12, 20); OR = (242, 179, 61)
IVOIRE = (245, 239, 223); BLANC = (255, 255, 255)

def font(px, path=FB):
    return ImageFont.truetype(path, px)

def load_bg(rel, lum=0.85):
    im = Image.open(os.path.join(ROOT, rel)).convert("RGB")
    tr = W / H
    w, h = im.size
    if w / h > tr:
        nw = int(h * tr); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / tr); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    im = im.resize((W, H), Image.LANCZOS)
    return ImageEnhance.Brightness(im).enhance(lum)

def badge(d):
    f = font(30)
    x, y = 56, 44
    b = d.textbbox((0, 0), "Daïsky Prod", font=f)
    w = (b[2]-b[0]) + 44; h2 = (b[3]-b[1]) + 20
    d.rounded_rectangle([x, y, x+w, y+h2], radius=h2/2, fill=(15,12,20,190), outline=OR, width=3)
    d.text((x+22, y+10 - b[1]), "Daïsky Prod", font=f, fill=OR)

def pill(d, cx, cy, txt, f, fill=JAUNE, fg=NOIR, pad=(30, 16), bord=4):
    b = d.textbbox((0, 0), txt, font=f)
    w = (b[2]-b[0]) + 2*pad[0]; h2 = (b[3]-b[1]) + 2*pad[1]
    x0, y0 = cx - w/2, cy - h2/2
    d.rounded_rectangle([x0, y0, x0+w, y0+h2], radius=h2/2, fill=fill, outline=NOIR, width=bord)
    d.text((x0+pad[0], y0+pad[1] - b[1]), txt, font=f, fill=fg)

def text_center(d, cx, y, txt, f, fill, stroke=0, sf=NOIR):
    b = d.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    d.text((cx - (b[2]-b[0])/2, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sf)

def panel(d, cy, lignes):
    """Panneau sombre arrondi centré avec lignes (txt, font, couleur, saut)."""
    hauteurs = []
    for txt, f, coul in lignes:
        b = d.textbbox((0, 0), txt, font=f)
        hauteurs.append(b[3]-b[1])
    pad_v, pad_h, inter = 34, 44, 14
    htot = sum(hauteurs) + inter*(len(lignes)-1) + 2*pad_v
    y0 = cy - htot/2
    d.rounded_rectangle([70, y0, W-70, y0+htot], radius=36, fill=(15, 12, 20, 205))
    yy = y0 + pad_v
    for (txt, f, coul), th in zip(lignes, hauteurs):
        text_center(d, W/2, yy, txt, f, coul)
        yy += th + inter

def footer(d):
    b = d.textbbox((0, 0), "linktr.ee/daiskypro", font=font(28))
    d.rounded_rectangle([(W-(b[2]-b[0]))/2-24, 1780, (W+(b[2]-b[0]))/2+24, 1780+52],
                        radius=26, fill=(15,12,20,190), outline=OR, width=2)
    text_center(d, W/2, 1780+12, "linktr.ee/daiskypro", font(28), OR)

def carte(bg_rel, tag, lignes, cta, out_name):
    im = load_bg(bg_rel)
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    badge(d)
    pill(d, W/2, 150, tag, font(44))
    panel(d, 1450, lignes)
    pill(d, W/2, 1700, cta, font(38))
    footer(d)
    out = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    out.save(os.path.join(LIV, out_name), quality=95)
    print("OK", out_name)

carte("assets/raw/reel/r01_pere.jpg", "\u2605 NOUVEAU REEL \u2605",
      [("ELLE METTAIT DU SEL", font(54), OR),
       ("DANS L'EAU…", font(54), OR),
       ("L'histoire que tout le monde partage \u2665", font(28), IVOIRE)],
      "\u25BA REGARDE \u00C7A", "Story_Reel1_Viral_1080x1920.jpg")

carte("assets/raw/reel2/r201_maman_etudes.jpg", "\u2605 NOUVEAU REEL 2 \u2605",
      [("MAMAN A ARRÊTÉ", font(54), OR),
       ("SES ÉTUDES POUR MOI…", font(54), OR),
       ("Partie 2 — encore plus forte \u2665", font(28), IVOIRE)],
      "\u25BA REGARDE \u00C7A", "Story_Reel2_Viral_1080x1920.jpg")

carte("assets/raw/10_cover.jpg", "\u2605 SUR YOUTUBE \u2605",
      [("LA VIDÉO COMPLÈTE", font(50), IVOIRE),
       ("HÉRITAGE DE MES PARENTS", font(52), OR),
       ("3:21 d'émotion pure — Daïsky", font(28), IVOIRE)],
      "\u271A ABONNE-TOI", "Story_YouTube_1080x1920.jpg")

carte("assets/raw/reel2/r210_envol.jpg", "\u2605 LE SON EST DISPO \u2605",
      [("HÉRITAGE DE MES PARENTS", font(50), OR),
       ("Master disponible partout", font(30), IVOIRE),
       ("Lien en bio \u2665", font(30), IVOIRE)],
      "\u2665 \u00C9COUTER", "Story_Son_1080x1920.jpg")

print("Terminé : 4 covers story.")
