# -*- coding: utf-8 -*-
"""Couvertures TikTok — 1080x1920 JPEG, typographie cuite par le moteur.

Trois couvertures, trois usages :
  1. `MESIAS_couverture_TikTok_1080x1920.jpg` — portrait, visage dégagé sous le titre,
     bloc bilingue en bas ;
  2. `MESIAS_couverture_variante_visage_1080x1920.jpg` — gros visage, texte minimal,
     pour les vignettes recadrées au centre ;
  3. `MESIAS_couverture_paysage_1080x1920.jpg` — la marche sur l'eau, contemplative.

Zones sûres respectées : badge en haut, rien d'essentiel sous y=1574, **aucun texte
sur le visage**. Tout vient du pool du clip, aucune image étrangère au morceau.

Usage : python3 scripts/make_cover.py
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import render as R

W, H = 1080, 1920
CREAM = (246, 240, 228)
AMBER = (232, 163, 61)
INDIGO = (10, 14, 30)
LIV = os.path.join(ROOT, "livrables")
BASE = os.path.join(ROOT, "work", "base")


def load(name):
    return Image.open(os.path.join(BASE, name)).convert("RGB")


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def scrim(base, points):
    """Assombrit selon une COURBE lissée.

    points = [(y, alpha), ...] en ordre croissant. L'interpolation passe par un
    smoothstep entre chaque paire : pas de marche visible, donc pas de bande
    horizontale dans le dégradé (défaut de la première version).
    """
    ov = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(ov)
    for i in range(len(points) - 1):
        y0, a0 = points[i]
        y1, a1 = points[i + 1]
        for y in range(max(0, int(y0)), min(H, int(y1))):
            r = smoothstep((y - y0) / max(1.0, (y1 - y0)))
            d.line([(0, y), (W, y)], fill=int(a0 + (a1 - a0) * r))
    y_last, a_last = points[-1]
    if y_last < H:
        d.rectangle([0, y_last, W, H], fill=int(a_last))
    out = base.copy()
    out.paste(Image.new("RGB", (W, H), INDIGO), (0, 0), ov)
    return out


def push_down(base, top_h):
    """Décale le sujet vers le bas pour dégager la zone du titre.

    La bande supérieure est comblée par un étirement très flou du haut de l'image,
    fondu sur 220 px avec le contenu : aucune couture visible.
    """
    body_h = H - top_h
    body = base.resize((W, int(body_h * 1.06)), Image.LANCZOS)
    body = body.crop((0, 0, W, body_h))
    strip = base.crop((0, 0, W, 90)).resize((W, top_h), Image.LANCZOS)
    strip = strip.filter(ImageFilter.GaussianBlur(70))
    # la bande haute est franchement assombrie : c'est la zone du titre, et cela
    # rend la couture de raccord invisible sous le voile
    strip = Image.blend(strip, Image.new("RGB", (W, top_h), INDIGO), 0.80)
    canvas = Image.new("RGB", (W, H), INDIGO)
    canvas.paste(strip, (0, 0))
    canvas.paste(body, (0, top_h))
    # fondu de raccord
    fade_h = 300
    mask = Image.new("L", (W, fade_h), 0)
    md = ImageDraw.Draw(mask)
    for y in range(fade_h):
        md.line([(0, y), (W, y)], fill=int(255 * smoothstep(y / fade_h)))
    canvas.paste(body.crop((0, 0, W, fade_h)), (0, top_h), mask)
    return canvas


def text(lay, s, size, y, fill, stroke=6):
    f = R.font(size)
    d = ImageDraw.Draw(lay)
    tw = d.textlength(s, font=f)
    x = (W - tw) / 2
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).text((x, y), s, font=f, fill=255)
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    lay.paste(Image.new("RGBA", (W, H), (4, 6, 16, 255)), (0, 0),
              sh.point(lambda v: int(v * 0.85)))
    d.text((x, y), s, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=(8, 10, 22, 240))
    return lay


def badge(lay, artist=True):
    d = ImageDraw.Draw(lay)
    d.line([(170, 186), (910, 186)], fill=(96, 102, 120, 190), width=2)
    if artist:
        d.text((46, 46), "AVERLY MORILLO", font=R.font(42), fill=(240, 236, 226, 255))
        d.text((46, 98), "WTBW", font=R.font(32), fill=(232, 163, 61, 255))
    return lay


def cover_portrait():
    base = load("pool_02_visage_calme.png")
    base = push_down(base, 430)                     # visage descendu sous le titre
    base = scrim(base, [(0, 216), (300, 196), (420, 150), (560, 60), (900, 10),
                        (1180, 45), (1500, 175), (H, 205)])
    lay = base.convert("RGBA")
    badge(lay)
    text(lay, "MESÍAS", 150, 210, CREAM + (255,), stroke=8)
    text(lay, "AVERLY MORILLO", 50, 372, AMBER + (255,), stroke=5)
    text(lay, "EN DIRECTO · 12:24", 34, 442, (200, 206, 222, 255), stroke=3)
    text(lay, "« VEN, SEÑOR »", 54, 1330, (208, 214, 230, 255), stroke=5)
    text(lay, "VIENS, MESÍAS", 88, 1402, CREAM + (255,), stroke=7)
    text(lay, "Traduction française à l'écran", 34, 1512, (196, 202, 218, 255), stroke=3)
    out = os.path.join(LIV, "MESIAS_couverture_TikTok_1080x1920.jpg")
    lay.convert("RGB").save(out, quality=94, progressive=True, optimize=True)
    print("couverture 1 :", out)


def cover_face():
    base = load("pool_13_larmes_lumiere.png")
    base = scrim(base, [(0, 120), (300, 25), (1350, 10), (H, 215)])
    lay = base.convert("RGBA")
    badge(lay, artist=False)
    text(lay, "MESÍAS", 126, 1430, CREAM + (255,), stroke=7)
    text(lay, "Averly Morillo · WTBW", 38, 1560, AMBER + (255,), stroke=4)
    out = os.path.join(LIV, "MESIAS_couverture_variante_visage_1080x1920.jpg")
    lay.convert("RGB").save(out, quality=94, progressive=True, optimize=True)
    print("couverture 2 :", out)


def cover_landscape():
    base = load("pool_17_marche_eau.png")
    base = push_down(base, 300)
    base = scrim(base, [(0, 140), (280, 35), (1100, 15), (1300, 55), (1550, 180), (H, 205)])
    lay = base.convert("RGBA")
    badge(lay)
    text(lay, "MESÍAS", 165, 150, CREAM + (255,), stroke=8)
    text(lay, "AVERLY MORILLO", 52, 330, AMBER + (255,), stroke=5)
    text(lay, "VIENS, MESÍAS", 92, 1360, CREAM + (255,), stroke=7)
    text(lay, "« Ven, Señor » · traduction à l'écran", 34, 1492, (200, 206, 222, 255), stroke=3)
    out = os.path.join(LIV, "MESIAS_couverture_paysage_1080x1920.jpg")
    lay.convert("RGB").save(out, quality=94, progressive=True, optimize=True)
    print("couverture 3 :", out)


if __name__ == "__main__":
    cover_portrait()
    cover_face()
    cover_landscape()
