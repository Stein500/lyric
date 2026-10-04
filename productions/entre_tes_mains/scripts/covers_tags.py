#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Covers + tags ID3v2.4 — « Entre Tes Mains » (v5.5 §D.9 / §E.5)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/user/lyric'
P = os.path.join(ROOT, 'productions', 'entre_tes_mains')
LIV = os.path.join(P, 'livrables')
FONT_C = os.path.join(P, 'assets', 'GreatVibes-Regular.ttf')
FONT_UI = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
os.makedirs(LIV, exist_ok=True)

GOLD = (255, 214, 120)
CREAM = (250, 246, 238)

def fc(s): return ImageFont.truetype(FONT_C, s)
def fui(s): return ImageFont.truetype(FONT_UI, s)

def tsize(d, t, f):
    l, t_, r, b = d.textbbox((0, 0), t, font=f)
    return r - l, b - t_

def cover_fit(bg_path, W, H):
    im = Image.open(bg_path).convert('RGB')
    sc = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * sc + 0.5), int(im.height * sc + 0.5)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def draw_shadow(d, xy, txt, f, fill, off=3, sh=(0, 0, 0, 200)):
    x, y = xy
    d.text((x + off, y + off + 1), txt, font=f, fill=sh)
    d.text((x, y), txt, font=f, fill=fill)

def benin_band(d, W, hgt):
    d.rectangle([0, 0, W // 3, hgt], fill=(0, 135, 81))
    d.rectangle([W // 3, 0, W, hgt // 2], fill=(252, 209, 22))
    d.rectangle([W // 3, hgt // 2, W, hgt], fill=(232, 17, 45))

def badge_picto(d, x, y, s=1.0):
    w, h = int(34 * s), int(24 * s)
    d.rectangle([x, y, x + w // 3, y + h], fill=(0, 135, 81))
    d.rectangle([x + w // 3, y, x + w, y + h // 2], fill=(252, 209, 22))
    d.rectangle([x + w // 3, y + h // 2, x + w, y + h], fill=(232, 17, 45))
    return w, h

BG = os.path.join(P, 'work', 'bg_s05_portrait.png')

# ------------------------------------------------ cover carree 1080
im = cover_fit(BG, 1080, 1080)
ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
d.rectangle([0, 0, 1080, 1080], fill=(10, 8, 6, 120))
title = 'Entre Tes Mains'
f = fc(132)
w, h = tsize(d, title, f)
draw_shadow(d, ((1080 - w) // 2, 300), title, f, GOLD + (255,), 4)
f2 = fui(58)
w2, h2 = tsize(d, 'Dsky', f2)
bw, bh = badge_picto(d, 0, 0, 0)  # mesure
bx = (1080 - w2 - 14 - 34) // 2
draw_shadow(d, (bx, 470), 'Dsky', f2, CREAM + (255,), 3)
badge_picto(d, bx + w2 + 14, 470 + (h2 - 24) // 2)
# bande Benin 30 px en bas
band = Image.new('RGBA', (1080, 30))
bd = ImageDraw.Draw(band)
benin_band(bd, 1080, 30)
ov.paste(band, (0, 1050))
out = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
out.save(os.path.join(LIV, 'cover_Entre_Tes_Mains_1080.png'))

# ------------------------------------------------ cover 1080x1920
im = cover_fit(BG, 1080, 1920)
ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
d.rectangle([0, 0, 1080, 1920], fill=(10, 8, 6, 100))
f = fc(132)
w, h = tsize(d, title, f)
draw_shadow(d, ((1080 - w) // 2, 240), title, f, GOLD + (255,), 4)
f2 = fui(58)
w2, h2 = tsize(d, 'Dsky', f2)
bx = (1080 - w2 - 14 - 34) // 2
draw_shadow(d, (bx, 420), 'Dsky', f2, CREAM + (255,), 3)
badge_picto(d, bx + w2 + 14, 420 + (h2 - 24) // 2)
band = Image.new('RGBA', (1080, 54))
bd = ImageDraw.Draw(band)
benin_band(bd, 1080, 54)
ov.paste(band, (0, 1866))
out = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
out.save(os.path.join(LIV, 'cover_Entre_Tes_Mains_1080x1920.png'))

# ------------------------------------------------ cover 1920x1080 (texte tiers gauche)
im = cover_fit(BG, 1920, 1080)
ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
d.rectangle([0, 0, 700, 1080], fill=(10, 8, 6, 150))
f = fc(110)
for i, part in enumerate(['Entre', 'Tes Mains']):
    draw_shadow(d, (70, 330 + i * 130), part, f, GOLD + (255,), 4)
f2 = fui(52)
draw_shadow(d, (72, 640), 'Dsky', f2, CREAM + (255,), 3)
w2, h2 = tsize(d, 'Dsky', f2)
badge_picto(d, 72 + w2 + 14, 640 + (h2 - 24) // 2)
band = Image.new('RGBA', (1920, 30))
bd = ImageDraw.Draw(band)
benin_band(bd, 1920, 30)
ov.paste(band, (0, 1050))
out = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
out.save(os.path.join(LIV, 'cover_Entre_Tes_Mains_1920x1080.png'))
print('covers ok')

# ------------------------------------------------ tags ID3v2.4
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TXXX, USLT, APIC, TSSE
src = os.path.join(ROOT, 'Entre tes mains.txt')
lyr = []
for line in open(src, encoding='utf-8'):
    line = line.strip()
    if line.startswith('[') and ']' in line:
        line = line.split(']', 1)[1].strip()
    if line:
        lyr.append(line)
lyrics = '\n'.join(lyr[1:])  # sans le tag length

import shutil
mp3_path = os.path.join(LIV, 'Entre_Tes_Mains_master.mp3')
shutil.copyfile(os.path.join(P, 'work', 'master_brut.mp3'), mp3_path)
audio = MP3(mp3_path)
audio.tags = ID3()
t = audio.tags
t.add(TIT2(encoding=3, text='Entre Tes Mains'))
t.add(TPE1(encoding=3, text='TechStein'))
t.add(TALB(encoding=3, text='Entre Tes Mains'))
t.add(TDRC(encoding=3, text='2026'))
t.add(TXXX(encoding=3, desc='contact', value='WhatsApp +229 01 61 16 24 08 / +229 01 49 11 49 51'))
t.add(TXXX(encoding=3, desc='email', value='daiskyproduction@gmail.com'))
t.add(USLT(encoding=3, lang='fra', desc='', text=lyrics))
cov = open(os.path.join(LIV, 'cover_Entre_Tes_Mains_1080.png'), 'rb').read()
t.add(APIC(encoding=3, mime='image/png', type=3, desc='cover', data=cov))
audio.save()
print('tags ok:', [k for k in audio.tags.keys()])
