#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COVERS + TAGS ID3 — « Dès le début »
· cover carrée 1080×1080 (APIC), + variantes 1080×1920 et 1920×1080
· titre exact, artiste, badge Dsky + drapeau Bénin, bandeau — ajoutés EN POST
· tags ID3v2.4 + USLT (paroles nettoyées) + APIC
"""
import os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(PROD, "..", ".."))
FONDS = os.path.join(PROD, "fonds")
LIVR = os.path.join(ROOT, "livrables")
WORK = os.path.join(PROD, "work")
FONT_LYR = os.path.join(ROOT, "assets", "fonts", "BarlowCondensed-Bold.ttf")
FONT_UI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BENIN = ((0, 135, 81), (252, 209, 22), (232, 17, 45))
TITRE, ARTISTE = "Dès le début", "Daïsky"
EMAIL = "daiskyproduction@gmail.com"
TEL = "+229 01 61 16 24 08"
os.makedirs(LIVR, exist_ok=True)


def f(path, size):
    from PIL import ImageFont
    return ImageFont.truetype(path, size)


def flag(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    t = w // 3
    d.rectangle([0, 0, t, h], fill=BENIN[0] + (255,))
    d.rectangle([t, 0, w, h // 2], fill=BENIN[1] + (255,))
    d.rectangle([t, h // 2, w, h], fill=BENIN[2] + (255,))
    d.rectangle([0, 0, w - 1, h - 1], outline=(8, 8, 10, 200), width=2)
    return im


def badge(scale=1.0):
    s = int(46 * scale)
    txt_f = f(FONT_UI, s)
    txt = "Dsky"
    bb = txt_f.getbbox(txt)
    fw, fh = int(s * 1.45), s
    pad = int(s * 0.42)
    w = (bb[2] - bb[0]) + int(s * 0.6) + fw + pad * 2
    h = int(s * 1.75)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=(8, 12, 22, 210),
                        outline=(255, 196, 78, 220), width=max(2, int(scale * 2)))
    d.text((pad - bb[0], (h - (bb[3] - bb[1])) // 2 - bb[1]), txt, font=txt_f, fill=(255, 240, 205, 255))
    im.alpha_composite(flag(fw, fh), (pad - bb[0] + (bb[2] - bb[0]) + int(s * 0.6), (h - fh) // 2))
    return im


def band(im, h):
    W, H = im.size
    d = ImageDraw.Draw(im, "RGBA")
    t = W // 3
    d.rectangle([0, H - h, t, H], fill=BENIN[0] + (255,))
    d.rectangle([t, H - h, W, H - h + h // 2], fill=BENIN[1] + (255,))
    d.rectangle([t, H - h + h // 2, W, H], fill=BENIN[2] + (255,))
    return im


def vignette_scrim(im, cx, cy, rw, rh, strength=0.55, blur=120):
    W, H = im.size
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle([cx - rw, cy - rh, cx + rw, cy + rh], radius=int(min(rw, rh) * 0.5), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(m, dtype=np.float32) / 255.0 * strength
    arr = np.asarray(im.convert("RGB"), dtype=np.float32)
    arr = arr * (1 - a[:, :, None]) + (arr * 0.45 + 8) * a[:, :, None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def make_cover(slot, size, kind="square"):
    """kind : square | portrait | landscape"""
    src = Image.open(os.path.join(FONDS, "portrait" if kind != "landscape" else "paysage", slot + ".jpg")).convert("RGB")
    W, H = (size, size) if kind == "square" else ((1080, 1920) if kind == "portrait" else (1920, 1080))
    # cadrage "cover"
    r = max(W / src.width, H / src.height)
    src = src.resize((int(src.width * r + 1), int(src.height * r + 1)), Image.LANCZOS)
    x = (src.width - W) // 2
    y = (src.height - H) // 2
    im = src.crop((x, y, x + W, y + H))

    if kind == "square":
        im = vignette_scrim(im, W // 2, int(H * 0.52), int(W * 0.44), int(H * 0.30), 0.60, 110)
        y_title, y_art, y_mail = int(H * 0.40), int(H * 0.55), int(H * 0.70)
        size_title, size_art, size_ui = 150, 66, 34
    elif kind == "portrait":
        im = vignette_scrim(im, W // 2, int(H * 0.30), int(W * 0.42), int(H * 0.14), 0.55, 120)
        y_title, y_art, y_mail = int(H * 0.23), int(H * 0.30), int(H * 0.35)
        size_title, size_art, size_ui = 118, 52, 30
    else:
        im = vignette_scrim(im, int(W * 0.26), int(H * 0.50), int(W * 0.20), int(H * 0.32), 0.55, 120)
        y_title, y_art, y_mail = int(H * 0.40), int(H * 0.57), int(H * 0.74)
        size_title, size_art, size_ui = 118, 50, 28

    d = ImageDraw.Draw(im, "RGBA")
    xc = W // 2 if kind != "landscape" else int(W * 0.26)
    d.text((xc, y_title), TITRE, font=f(FONT_LYR, size_title), fill=(255, 240, 210, 255), anchor="mm",
           stroke_width=6, stroke_fill=(0, 0, 0, 190))
    d.text((xc, y_art), ARTISTE, font=f(FONT_UI, size_art), fill=(255, 196, 78, 255), anchor="mm",
           stroke_width=4, stroke_fill=(0, 0, 0, 180))
    d.line([(xc - int(W * 0.10), y_art + int(size_art * 0.75)), (xc + int(W * 0.10), y_art + int(size_art * 0.75))],
           fill=(255, 196, 78, 190), width=3)
    d.text((xc, y_mail), EMAIL, font=f(FONT_UI, size_ui), fill=(240, 240, 245, 235), anchor="mm",
           stroke_width=3, stroke_fill=(0, 0, 0, 170))
    d.text((xc, y_mail + int(size_ui * 1.5)), TEL, font=f(FONT_UI, size_ui), fill=(240, 240, 245, 235),
           anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 170))
    b = badge(1.0 if kind == "square" else 0.85)
    im.alpha_composite(b, (int(xc - b.width / 2), int(H * 0.085)))
    band_h = 54 if kind != "landscape" else 30
    im = band(im, band_h)
    return im


if __name__ == "__main__":
    slot = sys.argv[1] if len(sys.argv) > 1 else "s15"
    outs = []
    for kind, size, name in [("square", 1080, "cover_Des_le_debut_1080x1080.jpg"),
                             ("portrait", 1080, "cover_Des_le_debut_9x16.jpg"),
                             ("landscape", 1920, "cover_Des_le_debut_16x9.jpg")]:
        im = make_cover(slot, size, kind)
        p = os.path.join(LIVR, name)
        im.save(p, quality=93)
        outs.append(p)
        print("cover:", p, im.size)
    # planche de contrôle
    ims = [Image.open(p).convert("RGB") for p in outs]
    th = 520
    ims = [im.resize((int(im.width * th / im.height), th), Image.LANCZOS) for im in ims]
    W = sum(i.width for i in ims) + 40
    c = Image.new("RGB", (W, th + 40), (12, 12, 16))
    x = 20
    for i in ims:
        c.paste(i, (x, 20)); x += i.width + 20
    c.save(os.path.join(LIVR, "_PLANCHE_COVERS.jpg"), quality=92)
    print("planche covers OK")
