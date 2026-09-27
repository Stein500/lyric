#!/usr/bin/env python3
"""Crée les covers post-produites et le master audio de Nonvi Konou.

Le MP3 source contient une image attachée : toutes les commandes audio mappent
explicitement 0:a:0 et désactivent la vidéo. Le loudnorm est réellement exécuté
en deux passes. Les caches WAV et journaux restent dans work/.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
from mutagen.id3 import (APIC, TALB, TCOM, TCON, TDRC, TIT2, TPE1, TPE2,
                         TPUB, TXXX, USLT, ID3)
from mutagen.mp3 import MP3
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'nonvi_konou'
FONTS = ROOT / 'assets' / 'fonts'
OUT = ROOT / 'livrables'
WORK = ROOT / 'work' / 'final_nonvi'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
DURATION = 193.48
TITLE = 'Nonvi Konou'
ARTIST = 'Daïsky'
EMAIL = 'daiskyproduction@gmail.com'
PHONES = '+229 01 61 16 24 08 / +229 01 49 11 49 51'


def run(args: list[str], *, capture=False):
    print('+', ' '.join(map(str, args)))
    return subprocess.run(args, check=True, text=True, capture_output=capture)


def flag(draw: ImageDraw.ImageDraw, bounds):
    x0, y0, x1, y1 = map(int, bounds)
    split = x0 + (x1 - x0) // 3
    middle = y0 + (y1 - y0) // 2
    draw.rectangle((x0, y0, split - 1, y1), fill='#008751')
    draw.rectangle((split, y0, x1, middle - 1), fill='#FCD116')
    draw.rectangle((split, middle, x1, y1), fill='#E8112D')


def fit_font(text, path, maximum, max_width, draw):
    size = maximum
    while size > 24:
        font = ImageFont.truetype(path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(path, size)


def dark_gradient(im, top_alpha=80, bottom_alpha=150):
    w, h = im.size
    layer = Image.new('RGBA', im.size)
    d = ImageDraw.Draw(layer)
    for y in range(h):
        # Discret en haut, plus dense dans le tiers inférieur pour les titres.
        p = y / max(1, h - 1)
        alpha = round(top_alpha * max(0, 1 - p * 3) + bottom_alpha * max(0, (p - .48) / .52) ** 1.5)
        d.line((0, y, w, y), fill=(3, 12, 20, min(210, alpha)))
    return Image.alpha_composite(im.convert('RGBA'), layer)


def draw_badge(im, y, scale=1.0):
    w, _ = im.size
    bw, bh = round(350 * scale), round(79 * scale)
    x0 = (w - bw) // 2
    layer = Image.new('RGBA', im.size)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x0, y, x0 + bw, y + bh), radius=round(30 * scale),
                        fill=(3, 18, 26, 216), outline=(248, 218, 154, 215), width=max(1, round(2 * scale)))
    font = ImageFont.truetype(FONTS / 'DejaVuSans-Bold.ttf', round(48 * scale))
    d.text((x0 + round(26 * scale), y + round(7 * scale)), 'Dsky', font=font,
           fill=(255, 250, 232, 255), stroke_width=max(1, round(scale)), stroke_fill=(4, 10, 18, 240))
    flag(d, (x0 + round(222 * scale), y + round(17 * scale),
             x0 + round(301 * scale), y + round(65 * scale)))
    im.alpha_composite(layer)


def cover_vertical():
    base = Image.open(ASSETS / 's00_intro_habillee.png').convert('RGBA')
    base = dark_gradient(base, 55, 170)
    # Le voile ne doit pas ternir les éléments nationaux : les recomposer après l'étalonnage.
    draw_badge(base, 160, 1.0)
    d = ImageDraw.Draw(base)
    d.rectangle((0, 1864, 1080, 1865), fill=(236, 194, 101, 255))
    flag(d, (0, 1866, 1080, 1920))
    title_font = fit_font(TITLE, FONTS / 'GreatVibes-latin.ttf', 178, 900, d)
    artist_font = ImageFont.truetype(FONTS / 'DejaVuSans-Bold.ttf', 47)
    bbox = d.textbbox((0, 0), TITLE, font=title_font, stroke_width=2)
    tw = bbox[2] - bbox[0]
    y = 1215
    # Ombre chaude et titre exact en post-production.
    d.text(((1080 - tw) / 2 + 3, y + 6), TITLE, font=title_font,
           fill=(0, 0, 0, 155), stroke_width=5, stroke_fill=(0, 0, 0, 140))
    d.text(((1080 - tw) / 2, y), TITLE, font=title_font,
           fill=(255, 223, 156, 255), stroke_width=2, stroke_fill=(10, 23, 30, 230))
    aw = d.textlength(ARTIST.upper(), font=artist_font)
    d.text(((1080 - aw) / 2, y + 190), ARTIST.upper(), font=artist_font,
           fill=(246, 246, 236, 245), stroke_width=2, stroke_fill=(6, 16, 24, 230))
    path = OUT / 'cover_nonvi_konou_9x16.jpg'
    base.convert('RGB').save(path, quality=95, subsampling=0, optimize=True)
    return path


def cover_square():
    src = Image.open(ASSETS / 's00_intro_habillee.png').convert('RGB')
    # Le crop exclut volontairement les éléments déjà incrustés ; ils sont recomposés aux bonnes proportions.
    square = src.crop((0, 375, 1080, 1455)).convert('RGBA')
    square = dark_gradient(square, 120, 185)
    draw_badge(square, 62, .75)
    d = ImageDraw.Draw(square)
    title_font = fit_font(TITLE, FONTS / 'GreatVibes-latin.ttf', 154, 830, d)
    artist_font = ImageFont.truetype(FONTS / 'DejaVuSans-Bold.ttf', 40)
    bbox = d.textbbox((0, 0), TITLE, font=title_font, stroke_width=2)
    tw = bbox[2] - bbox[0]
    y = 670
    d.text(((1080 - tw) / 2 + 3, y + 5), TITLE, font=title_font,
           fill=(0, 0, 0, 170), stroke_width=5, stroke_fill=(0, 0, 0, 150))
    d.text(((1080 - tw) / 2, y), TITLE, font=title_font,
           fill=(255, 223, 156, 255), stroke_width=2, stroke_fill=(8, 19, 27, 235))
    aw = d.textlength(ARTIST.upper(), font=artist_font)
    d.text(((1080 - aw) / 2, y + 165), ARTIST.upper(), font=artist_font,
           fill=(248, 247, 238, 250), stroke_width=2, stroke_fill=(5, 14, 22, 230))
    fd = ImageDraw.Draw(square)
    footer_h = 30  # même proportion 2,8 % que 54 px sur 1920
    fd.rectangle((0, 1080 - footer_h - 2, 1080, 1080 - footer_h - 1), fill=(236, 194, 101, 255))
    flag(fd, (0, 1080 - footer_h, 1080, 1080))
    apic = OUT / 'cover_nonvi_konou_1080.jpg'
    universal = OUT / 'cover_nonvi_konou_universelle_3000.jpg'
    square.convert('RGB').save(apic, quality=95, subsampling=0, optimize=True)
    square.convert('RGB').resize((3000, 3000), Image.Resampling.LANCZOS).save(
        universal, quality=94, subsampling=0, optimize=True)
    return apic, universal


def loudnorm_passes():
    source = ROOT / 'Nonvi Konou.mp3'
    pass1_filter = 'highpass=f=30,lowpass=f=18000,loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json'
    first = run([FFMPEG, '-hide_banner', '-v', 'info', '-i', str(source), '-map', '0:a:0', '-vn',
                 '-af', pass1_filter, '-f', 'null', '-'], capture=True)
    blocks = re.findall(r'\{\s*"input_i".*?\}', first.stderr, re.S)
    if not blocks:
        raise RuntimeError('Mesures loudnorm passe 1 introuvables')
    measured = json.loads(blocks[-1])
    second_filter = (
        'highpass=f=30,lowpass=f=18000,'
        'loudnorm=I=-14:TP=-1.8:LRA=11:'
        f'measured_I={measured["input_i"]}:measured_TP={measured["input_tp"]}:'
        f'measured_LRA={measured["input_lra"]}:measured_thresh={measured["input_thresh"]}:'
        f'offset={measured["target_offset"]}:linear=true:print_format=json'
    )
    normalized = WORK / 'nonvi_konou_normalise_48k.wav'
    second = run([FFMPEG, '-hide_banner', '-y', '-v', 'info', '-i', str(source), '-map', '0:a:0', '-vn',
                  '-af', second_filter, '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le',
                  '-t', f'{DURATION:.3f}', str(normalized)], capture=True)
    blocks2 = re.findall(r'\{\s*"input_i".*?\}', second.stderr, re.S)
    second_stats = json.loads(blocks2[-1]) if blocks2 else {}
    verify = run([FFMPEG, '-hide_banner', '-v', 'info', '-i', str(normalized),
                  '-af', 'loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json', '-f', 'null', '-'], capture=True)
    verify_blocks = re.findall(r'\{\s*"input_i".*?\}', verify.stderr, re.S)
    verification = json.loads(verify_blocks[-1]) if verify_blocks else {}
    report = {'pass1': measured, 'pass2': second_stats, 'verification': verification,
              'filter_pass2': second_filter}
    (WORK / 'loudnorm.json').write_text(json.dumps(report, indent=2) + '\n')
    return normalized, report


def master_mp3(normalized: Path, cover: Path):
    master = OUT / 'Nonvi_Konou_master_320k.mp3'
    run([FFMPEG, '-hide_banner', '-y', '-v', 'warning', '-i', str(normalized), '-map', '0:a:0', '-vn',
         '-c:a', 'libmp3lame', '-b:a', '320k', '-ar', '48000', '-t', f'{DURATION:.3f}', str(master)])
    lyrics = []
    for line in (ROOT / 'Nonvi Konou.lrc').read_text(encoding='utf-8').splitlines():
        if line.startswith('[ti:') or line.startswith('[ar:'):
            continue
        text = re.sub(r'^\[\d\d:\d\d\.\d\d\]', '', line).strip()
        if text:
            lyrics.append(text)
    tags = ID3()
    tags.add(TIT2(encoding=3, text=TITLE))
    tags.add(TPE1(encoding=3, text=ARTIST))
    tags.add(TALB(encoding=3, text=TITLE))
    tags.add(TPE2(encoding=3, text=ARTIST))
    tags.add(TPUB(encoding=3, text='Dsky Production'))
    tags.add(TCOM(encoding=3, text='TechStein'))
    tags.add(TCON(encoding=3, text='Afrobeat'))
    tags.add(TDRC(encoding=3, text='2026'))
    tags.add(TXXX(encoding=3, desc='contact', text=PHONES))
    tags.add(TXXX(encoding=3, desc='email', text=EMAIL))
    tags.add(TXXX(encoding=3, desc='producer', text='TechStein'))
    tags.add(TXXX(encoding=3, desc='label', text='Dsky Production'))
    tags.add(USLT(encoding=3, lang='fra', desc='', text='\n'.join(lyrics)))
    tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover.read_bytes()))
    tags.save(master, v2_version=4)
    info = MP3(master)
    return master, {'duration': info.info.length, 'bitrate': info.info.bitrate,
                    'sample_rate': info.info.sample_rate, 'tag_keys': sorted(info.tags.keys())}


def main():
    OUT.mkdir(exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    vertical = cover_vertical()
    apic, universal = cover_square()
    normalized, loud = loudnorm_passes()
    master, audio_info = master_mp3(normalized, apic)
    report = {'covers': [str(vertical.relative_to(ROOT)), str(apic.relative_to(ROOT)),
                         str(universal.relative_to(ROOT))],
              'master': str(master.relative_to(ROOT)), 'audio': audio_info, 'loudnorm': loud}
    (WORK / 'audio_covers_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
