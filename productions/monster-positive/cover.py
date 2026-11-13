#!/usr/bin/env python3
"""cover.py — couverture TikTok 1080x1920 (v6.4 §7.5).
Entrée : fonds/cover-tiktok.png (768x1376, générateur, NO TEXT AT ALL).
Sortie : livrables/COVER-tiktok-1080x1920.jpg (qualité 95, 4:4:4) avec titre cuit par le moteur :
veile d'encre dégradé sur les 300 px du bas (alpha max 0.72), titre 2 lignes largeur <= 900 px
(x 90->990, auto-réduction par pas de 2 px), contour par dilatation, Daïsky y1495 entre filets or,
série « Wolof TechStein beat 웨 » y1560.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
MON = os.path.join(ROOT, "fonts", "Montserrat.ttf")
NOTO = os.path.join(ROOT, "fonts", "NotoSansKR.ttf")
def noto(size):
    f = ImageFont.truetype(NOTO, size)
    try: f.set_variation_by_axes([600])
    except Exception: pass
    return f
W, H = 1080, 1920
S = 1080 / 768.0
OR = (232, 168, 62)

def mont(size, wght=800):
    f = ImageFont.truetype(MON, size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f

def text_w(d, text, f, tr=0):
    return sum(d.textlength(c, font=f) for c in text) + tr * max(0, len(text) - 1)

def draw_tracked_contour(img, xy, text, size, wght, fill, tr=0):
    """contour par dilatation du masque + texte par-dessus."""
    f = mont(size, wght)
    d0 = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    w = text_w(d0, text, f, tr)
    pad = size // 6
    m = Image.new("L", (int(w) + 2 * pad, size + 2 * pad), 0)
    d = ImageDraw.Draw(m)
    x = pad
    for c in text:
        d.text((x, pad), c, font=f, fill=255)
        x += d.textlength(c, font=f) + tr
    cont = m.filter(ImageFilter.MaxFilter(2 * pad + 1))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    layer.paste(Image.new("RGBA", m.size, (5, 6, 8, 255)), (int(xy[0] - pad), int(xy[1] - pad)), cont)
    img.alpha_composite(layer)
    d = ImageDraw.Draw(img)
    x = xy[0]
    for c in text:
        fc = noto(f.size) if ord(c) >= 0xAC00 else f
        d.text((x, xy[1]), c, font=fc, fill=fill)
        x += d.textlength(c, font=f) + tr

def main():
    src = os.path.join(ROOT, "fonds", "cover-tiktok.png")
    im = Image.open(src).convert("RGB")
    im = im.resize((W, int(round(im.height * S))), Image.LANCZOS).crop((0, 0, W, H))
    ov = im.convert("RGBA")
    # voile d'encre dégradé sur les 300 px du bas (alpha max 0.72 = 184)
    veil = Image.new("L", (W, 300), 0)
    for i in range(300):
        veil.putpixel((0, i), 0)
    vd = ImageDraw.Draw(veil)
    for i in range(300):
        vd.line([(0, i), (W, i)], fill=int(184 * (1 - i / 300) ** 1.2 + 184 * (i / 300) * 0))
    # dégradé vertical croissant vers le bas
    import numpy as np
    a = (np.linspace(0, 184, 300) ** 1.1).astype(np.uint8)
    veil = Image.fromarray(np.tile(a[:, None], (1, W)))
    ink = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ink.paste(Image.new("RGBA", (W, 300), (4, 5, 7, 255)), (0, H - 300), veil)
    ov.alpha_composite(ink)
    # titre 2 lignes, largeur utile <= 900 (x 90 -> 990)
    lines = [("MONSTER", 128, 800), ("POSITIVE", 104, 800)]
    d0 = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    size1, size2 = 128, 104
    while text_w(d0, lines[0][0], mont(size1, 800), 4) > 900 or text_w(d0, lines[1][0], mont(size2, 800), 4) > 900:
        size1 -= 2; size2 -= 2
    y = 1180
    draw_tracked_contour(ov, (540 - text_w(d0, "MONSTER", mont(size1, 800), 4) / 2, y), "MONSTER", size1, 800, (255, 255, 255, 255), tr=4)
    y += int(size1 * 1.25)
    draw_tracked_contour(ov, (540 - text_w(d0, "POSITIVE", mont(size2, 800), 4) / 2, y), "POSITIVE", size2, 800, (255, 255, 255, 255), tr=4)
    # Daïsky entre deux filets or, y 1495
    d = ImageDraw.Draw(ov)
    fw = text_w(d, "DSKY", mont(60, 700), 16)
    d.line([540 - fw / 2 - 40, 1495, 540 - fw / 2 - 16, 1495], fill=OR + (255,), width=3)
    d.line([540 + fw / 2 + 16, 1495, 540 + fw / 2 + 40, 1495], fill=OR + (255,), width=3)
    x = 540 - fw / 2
    f = mont(60, 700)
    for c in "DSKY":
        d.text((x, 1462), c, font=f, fill=(255, 255, 255, 255))
        x += d.textlength(c, font=f) + 16
    tracked = "Wolof TechStein beat 웨"
    f2 = mont(26, 600)
    w2 = text_w(d, tracked, f2, 3)
    x = 540 - w2 / 2
    for c in tracked:
        fc = noto(f2.size) if ord(c) >= 0xAC00 else f2
        d.text((x, 1560), c, font=fc, fill=(255, 255, 255, 200))
        x += d.textlength(c, font=f2) + 3
    ov.convert("RGB").save(os.path.join(ROOT, "livrables", "COVER-tiktok-1080x1920.jpg"), quality=95, subsampling=0)
    print("cover écrite, tailles titre:", size1, size2)

if __name__ == "__main__":
    main()
