# -*- coding: utf-8 -*-
"""Préparation des frames : upscale 1080x1920 (cover) + badge statique en bas-gauche.
Le badge n'est JAMAIS peint dans l'image source (assets/raw) -> on travaille dans work/prep/.
"""
import os, glob
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'assets', 'raw', 'portrait')
PREP = os.path.join(ROOT, 'work', 'prep')
os.makedirs(PREP, exist_ok=True)

W, H = 1080, 1920

CYAN = (77, 210, 255)      # #4DD2FF
AMBER = (232, 163, 61)     # #E8A33D
WHITE = (245, 249, 255)    # #F5F9FF
DARK = (5, 6, 10)          # #05060A

FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def cover_fit(im, w, h):
    """Resize pour couvrir w x h puis centre-crop."""
    ratio = max(w / im.width, h / im.height)
    nw, nh = int(im.width * ratio + 0.5), int(im.height * ratio + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return im.crop((x, y, x + w, y + h))


def draw_bolt(draw, cx, cy, s, color):
    """Petit éclair (polygone) autour de (cx, cy), taille s."""
    pts = [
        (cx + 0.50 * s, cy - 0.55 * s),
        (cx - 0.05 * s, cy + 0.05 * s),
        (cx + 0.20 * s, cy + 0.05 * s),
        (cx - 0.15 * s, cy + 0.55 * s),
        (cx + 0.30 * s, cy - 0.10 * s),
        (cx + 0.05 * s, cy - 0.10 * s),
    ]
    draw.polygon(pts, fill=color)


def badge(img):
    """Incruste un badge bas-gauche : ?? DAISKY PROD (cyan/ambre)."""
    d = ImageDraw.Draw(img, 'RGBA')
    text = 'DAISKY PROD'
    fs = 44
    font = ImageFont.truetype(FONT_BOLD, fs)
    tb = d.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 26, 14
    bolt_s = 40
    box_x0, box_y0 = 50, H - 150
    box_w = pad_x + bolt_s + 14 + tw + pad_x
    box_h = pad_y + th + pad_y + 6
    box_y0 = H - 50 - box_h
    # fond translucide
    d.rounded_rectangle([box_x0, box_y0, box_x0 + box_w, box_y0 + box_h],
                        radius=18, fill=(5, 6, 10, 165), outline=CYAN, width=3)
    # éclair
    lx = box_x0 + pad_x - 4
    ly = box_y0 + box_h / 2
    draw_bolt(d, lx, ly, bolt_s, AMBER)
    # texte
    tx = box_x0 + pad_x + bolt_s + 14
    ty = box_y0 + (box_h - th) / 2 - tb[1]
    d.text((tx, ty), text, font=font, fill=CYAN)


def main():
    files = sorted(glob.glob(os.path.join(RAW, '*.jpg')))
    for f in files:
        base = os.path.basename(f).replace('.jpg', '')
        im = Image.open(f).convert('RGB')
        im = cover_fit(im, W, H)
        badge(im)
        out = os.path.join(PREP, base + '.jpg')
        im.save(out, quality=92, subsampling=2)
        print('prep', base, im.size)
    print('TOTAL', len(files))


if __name__ == '__main__':
    main()
