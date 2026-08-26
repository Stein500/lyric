#!/usr/bin/env python3
"""
🔨 BUILD COVER PRO UNIQUE — Lightning Is My Name (Daïsky)
- Génère une cover MP3 carrée 1400x1400 (standard Spotify/Apple/YouTube Music)
- À partir de l'image portrait 19 (cover officielle), avec badge, titre & artiste incrustés
- Exports: assets/cover/cover_Lightning_pro.jpg (carré)
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path("/home/user/lyric")
OUT = ROOT/"assets"/"cover"
OUT.mkdir(parents=True, exist_ok=True)
SRC = ROOT/"assets/raw/portrait/19_cover_single_portrait.jpg"

# 1. Charger source & recadrer en carré
src = Image.open(SRC).convert("RGB")
sw, sh = src.size
side = min(sw, sh)  # on prend le carré le plus large possible, centré sur le haut (visage)
left = (sw - side)//2
top = 10  # légèrement plus haut que le centre pour cadrer le visage
if top + side > sh: top = sh - side
cover = src.crop((left, top, left+side, top+side)).resize((1400, 1400), Image.LANCZOS)

# 2. Léger vignettage + rehaussement cyan
cover = ImageEnhance.Contrast(cover).enhance(1.15)
cover = ImageEnhance.Color(cover).enhance(1.1)
# overlay gradient bas pour lisibilité titre
grad = Image.new("RGBA", (1400,1400), (0,0,0,0))
gdraw = ImageDraw.Draw(grad)
for y in range(700, 1400):
    alpha = int(255 * ((y-700)/700)**1.3)
    gdraw.line([(0,y),(1400,y)], fill=(5,6,10, min(alpha, 200)))
# fin halo cyan en haut
for y in range(0, 400):
    alpha = int(80 * (1 - y/400))
    gdraw.line([(0,y),(1400,y)], fill=(77,210,255, alpha))
cover = cover.convert("RGBA")
cover.alpha_composite(grad)

# 3. Charger polices
def find_font(size, bold=False):
    cands = []
    if bold:
        cands += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
    else:
        cands += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
    for fp in cands:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

draw = ImageDraw.Draw(cover)

# ⚡ Éclair icône en haut-gauche (petit)
f_icon = find_font(60, bold=True)
draw.text((60, 60), "⚡", fill=(77,210,255,255), font=f_icon)

# TITRE — bas de cover, grand
f_title = find_font(110, bold=True)
f_title2 = find_font(110, bold=True)
title1 = "LIGHTNING"
title2 = "IS MY NAME"
# ombre portée
draw.text((70, 930), title1, fill=(0,0,0,180), font=f_title)
draw.text((70, 1050), title2, fill=(0,0,0,180), font=f_title2)
# texte cyan éclair
draw.text((65, 925), title1, fill=(245,249,255,255), font=f_title)
draw.text((65, 1045), title2, fill=(77,210,255,255), font=f_title2)

# Artiste — sous le titre, or
f_art = find_font(62, bold=True)
draw.text((70, 1175), "DAÏSKY", fill=(232,163,61,255), font=f_art)

# Prod — petit sous artiste
f_prod = find_font(32, bold=False)
draw.text((70, 1245), "Daïsky Prod  •  TechStein  •  2026", fill=(245,249,255,220), font=f_prod)

# Liseré cyan bas
draw.rectangle([0, 1380, 1400, 1388], fill=(77,210,255,255))
# Liseré ambre fin au-dessus
draw.rectangle([0, 1376, 1400, 1380], fill=(232,163,61,255))

# 4. Export final
out_jpg = OUT/"cover_Lightning_pro.jpg"
cover.convert("RGB").save(out_jpg, "JPEG", quality=95)
print(f"✅ Cover carrée 1400×1400 : {out_jpg}  ({out_jpg.stat().st_size/1e3:.0f} KB)")

# Export 3000x3000 pour distrib HD
cover.resize((3000,3000), Image.LANCZOS).convert("RGB").save(OUT/"cover_Lightning_pro_3000.jpg", "JPEG", quality=92)
print(f"✅ Cover HD 3000×3000 : {OUT/'cover_Lightning_pro_3000.jpg'}")
