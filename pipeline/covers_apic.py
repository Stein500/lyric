#!/usr/bin/env python3
"""Covers §10 + APIC §3 : badge DSKY en post, crédits propres, sorties JPEG q92,
APIC 1080x1080 embarqué dans le master.
Usage: work/venv/bin/python pipeline/covers_apic.py
"""
import os, shutil
from PIL import Image, ImageDraw, ImageFont
from mutagen.id3 import ID3, APIC

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FONT_B = "assets/fonts/DejaVuSans-Bold.ttf"
def font(sz): return ImageFont.truetype(FONT_B, sz)

def cover_fit(path, W, H):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def badge_sprite():
    txt = "✓DSKY"; f = font(30); pad = 10
    b = f.getbbox(txt); chk = 26
    wtot = chk + 6 + (b[2] - b[0]) + pad * 2
    htot = (b[3] - b[1]) + pad * 2
    im = Image.new("RGBA", (int(wtot) + 4, int(htot) + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=14,
                        fill=(10, 14, 20, 175), outline=(255, 255, 255, 120), width=2)
    cx0, cy0 = pad, (im.height - chk) // 2
    d.rounded_rectangle([cx0, cy0, cx0 + chk, cy0 + chk], radius=6, fill=(250, 200, 60, 255))
    d.text((cx0 + 5, cy0 + 2), "✓", font=font(20), fill=(20, 20, 25, 255))
    d.text((cx0 + chk + 6, 4 + pad - 5), txt, font=f, fill=(240, 248, 252, 255))
    return im
BADGE = badge_sprite()

CREDITS = "Daïsky Prod / TechStein · Afro-Rock · 2026 · @daiskypro"

def finish(im):
    im = im.convert("RGBA")
    d = ImageDraw.Draw(im)
    W, H = im.size
    # crédits bas, petits, propres
    f = font(26)
    b = f.getbbox(CREDITS)
    x = (W - int(f.getlength(CREDITS))) // 2
    d.text((x + 2, H - 52 + 2), CREDITS, font=f, fill=(0, 0, 0, 200))
    d.text((x, H - 52), CREDITS, font=f, fill=(235, 240, 245, 235),
           stroke_width=2, stroke_fill=(5, 8, 12, 200))
    # badge haut-centre (post, jamais généré)
    bw, bh = BADGE.size
    im.paste(BADGE, ((W - bw) // 2, 22), BADGE)
    return im.convert("RGB")

outs = [
    ("assets/covers/cover_9x16_base.png", 1080, 1920, "livrables/cover_Guerrier_9x16.jpg"),
    ("assets/covers/cover_16x9_base.png", 1920, 1080, "livrables/cover_Guerrier_16x9.jpg"),
    ("assets/covers/cover_square_base.png", 1080, 1080, "livrables/cover_Guerrier_1x1.jpg"),
]
apic_path = None
for src, W, H, dst in outs:
    im = finish(cover_fit(src, W, H))
    im.save(dst, quality=92)
    print("cover ->", dst)
    if W == H:
        apic_path = dst

# APIC dans le master
tags = ID3("work/master_guerrier.mp3")
with open(apic_path, "rb") as fh:
    data = fh.read()
tags.delall("APIC")
tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="cover", data=data))
tags.save()
shutil.copy("work/master_guerrier.mp3", "livrables/Guerrier - Daïsky (master 320k).mp3")
print("APIC embarqué + master recopié")
