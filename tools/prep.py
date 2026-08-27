# -*- coding: utf-8 -*-
"""Préparation des frames : upscale (cover) + badge statique en bas-gauche.
Mode 'portrait' (9:16) ou 'landscape' (16:9). Le badge n'est JAMAIS peint dans
l'image source (assets/raw) -> on travaille dans work/prep/<mode>/.
"""
import os, sys, glob
from PIL import Image, ImageDraw, ImageFont
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
spec = importlib.util.spec_from_file_location('timeline', os.path.join(ROOT, 'tools', 'timeline.py'))
tl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tl)

MODE = sys.argv[1] if len(sys.argv) > 1 else 'portrait'
W, H, _ = tl.dims_for_mode(MODE)
SRC = os.path.join(ROOT, 'assets', 'raw', 'portrait' if MODE == 'portrait' else 'landscape')
PREP = os.path.join(ROOT, 'work', 'prep', MODE)
os.makedirs(PREP, exist_ok=True)

CYAN = (77, 210, 255)      # #4DD2FF
AMBER = (232, 163, 61)     # #E8A33D
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def cover_fit(im, w, h):
    ratio = max(w / im.width, h / im.height)
    nw, nh = int(im.width * ratio + 0.5), int(im.height * ratio + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return im.crop((x, y, x + w, y + h))


def draw_bolt(d, cx, cy, s, color):
    pts = [
        (cx + 0.50 * s, cy - 0.55 * s),
        (cx - 0.05 * s, cy + 0.05 * s),
        (cx + 0.20 * s, cy + 0.05 * s),
        (cx - 0.15 * s, cy + 0.55 * s),
        (cx + 0.30 * s, cy - 0.10 * s),
        (cx + 0.05 * s, cy - 0.10 * s),
    ]
    d.polygon(pts, fill=color)


def badge(img):
    """Badge bas-gauche : ?? DAISKY PROD (cyan/ambre), position + taille adaptées."""
    d = ImageDraw.Draw(img, 'RGBA')
    text = 'DAISKY PROD'
    fs = 44 if MODE == 'portrait' else 40
    font = ImageFont.truetype(FONT_BOLD, fs)
    tb = d.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 26, 14
    bolt_s = 40 if MODE == 'portrait' else 36
    box_x0 = 50 if MODE == 'portrait' else 40
    box_w = pad_x + bolt_s + 14 + tw + pad_x
    box_h = pad_y + th + pad_y + 6
    box_y0 = H - 50 - box_h
    d.rounded_rectangle([box_x0, box_y0, box_x0 + box_w, box_y0 + box_h],
                        radius=18, fill=(5, 6, 10, 165), outline=CYAN, width=3)
    lx = box_x0 + pad_x - 4
    ly = box_y0 + box_h / 2
    draw_bolt(d, lx, ly, bolt_s, AMBER)
    tx = box_x0 + pad_x + bolt_s + 14
    ty = box_y0 + (box_h - th) / 2 - tb[1]
    d.text((tx, ty), text, font=font, fill=CYAN)


def main():
    files = sorted(glob.glob(os.path.join(SRC, '*.jpg')))
    for f in files:
        base = os.path.basename(f).replace('.jpg', '')
        im = Image.open(f).convert('RGB')
        im = cover_fit(im, W, H)
        badge(im)
        out = os.path.join(PREP, base + '.jpg')
        im.save(out, quality=92, subsampling=2)
        print('prep', MODE, base, im.size)
    print('TOTAL', MODE, len(files))


if __name__ == '__main__':
    main()
