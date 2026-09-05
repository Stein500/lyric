#!/usr/bin/env python3
"""Prépare une planche de salve (10 images max) et un aperçu typographique.

Usage : .venv/bin/python scripts/planche_je_maime.py \
          projets/je_maime_tellement/salves/portrait_01.json
Ne génère pas de nouvelle scène IA. Sources brutes préservées, dérivés séparés.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from maquette_je_maime import make_badge

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path('/usr/share/fonts/truetype/dejavu')


def font(size, bold=False):
    return ImageFont.truetype(str(FONTS / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')), size)


def wrap(text, face, max_width):
    lines, line = [], ''
    for word in text.split():
        candidate = f'{line} {word}'.strip()
        if face.getlength(candidate) <= max_width:
            line = candidate
        else:
            if not line:
                raise ValueError(f'Mot trop large : {word}')
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def prepare(asset):
    original = ROOT / asset['source_image']
    if hashlib.sha256(original.read_bytes()).hexdigest() != asset['sha256']:
        raise ValueError(f'Source modifiée : {original}')
    with Image.open(original) as opened:
        image = opened.convert('RGB')
    if asset.get('preparation'):
        spec = asset['preparation']
        if spec['method'] != 'extend_own_sky_over_top_band':
            raise ValueError('Préparation inconnue')
        # Uniquement S01 : remplacer la marge rectangulaire produite par le modèle
        # par un prolongement doux de SON PROPRE ciel. Aucun personnage redessiné,
        # aucune image d'un autre vers, aucun nouvel appel de génération.
        n, sample = spec['band_height_px'], spec['sample_height_px']
        width, height = image.size
        if not (0 < n < height / 4 and 0 < sample <= 32):
            raise ValueError('Paramètres de marge invalides')
        sky = ImageOps.flip(image.crop((0, n, width, n + sample)))
        sky = sky.resize((width, n), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(5))
        pixels = np.asarray(sky).astype(np.float32)
        factors = np.linspace(0.65, 1.0, n, dtype=np.float32)[:, None, None]
        pixels *= factors
        image.paste(Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8)), (0, 0))
        # La jonction reste dans le ciel, bien au-dessus de la tête.
        arr = np.asarray(image).copy()
        edge = arr[n - 1].astype(np.float32)
        for row in range(sample):
            alpha = (row + 1) / sample
            arr[n + row] = np.clip(edge * (1 - alpha) + arr[n + row] * alpha, 0, 255).astype(np.uint8)
        image = Image.fromarray(arr)
        prepared = ROOT / asset['render_source']
        prepared.parent.mkdir(parents=True, exist_ok=True)
        image.save(prepared, optimize=True)
    return image


def proof(asset, image, destination):
    width, height = 1080, 1920
    result = ImageOps.fit(image, (width, height), Image.Resampling.LANCZOS).convert('RGBA')
    shade = Image.new('RGBA', (1, height))
    pixels = shade.load()
    for y in range(height):
        alpha = int(90 * max(0, min(1, (y - height * .68) / (height * .3))))
        pixels[0, y] = (5, 12, 17, alpha)
    result = Image.alpha_composite(result, shade.resize((width, height)))
    text = re.sub(r',(?=\S)', ', ', asset['display_text'])
    assert re.sub(r'\s+', '', text) == re.sub(r'\s+', '', asset['display_text'])
    face = font(58)
    lines = asset.get('display_lines') or wrap(text, face, 920)
    assert re.sub(r'\s+', '', ''.join(lines)) == re.sub(r'\s+', '', text)
    assert all(face.getlength(line) <= 920 for line in lines)
    if len(lines) > 3:
        raise ValueError('Aperçu : plus de trois lignes')
    letters, glow = Image.new('RGBA', result.size), Image.new('RGBA', result.size)
    draw, soft = ImageDraw.Draw(letters), ImageDraw.Draw(glow)
    for index, line in enumerate(lines):
        position = (width // 2, height - 300 + index * 80)
        soft.text(position, line, font=face, anchor='mt', fill=(255, 183, 75, 105), stroke_width=3)
        draw.text(position, line, font=face, anchor='mt', fill=(255, 247, 230, 255),
                  stroke_width=2, stroke_fill=(17, 14, 13, 230))
    result = Image.alpha_composite(result, glow.filter(ImageFilter.GaussianBlur(7)))
    result = Image.alpha_composite(result, letters)
    result.alpha_composite(make_badge(), (36, 36))
    destination.parent.mkdir(parents=True, exist_ok=True)
    result.convert('RGB').save(destination, quality=92, subsampling=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    batch = json.loads(args.manifest.read_text(encoding='utf-8'))
    assets = batch['assets']
    if not 1 <= len(assets) <= 10:
        raise ValueError('Une salve contient 1 à 10 images')
    if len({a['sha256'] for a in assets}) != len(assets):
        raise ValueError('Une même image ne peut pas servir deux slots')
    if batch['text_advance_seconds'] != 0:
        raise ValueError('Ce morceau impose zéro avance')
    columns = 5
    margin, gap, card_width, thumb_height, caption_height = 24, 18, 276, 491, 140
    rows = (len(assets) + columns - 1) // columns
    top, footer = 172, 74
    width = margin * 2 + columns * card_width + (columns - 1) * gap
    height = top + rows * (thumb_height + caption_height) + (rows - 1) * gap + footer
    sheet = Image.new('RGBA', (width, height), (9, 15, 18, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((400, 36), "Je m'aime tellement", font=font(43, True), fill='#fff3dd')
    counts = {style: sum(a['style'] == style for a in assets) for style in ('cinema', 'anime')}
    subtitle = f"Salve {batch['batch_number']:02d} · {counts['cinema']} cinéma / {counts['anime']} animé · Portrait 9:16"
    draw.text((400, 96), subtitle, font=font(24), fill='#9cdce1')
    draw.text((400, 131), 'Silhouette généreuse · Une image propre à chaque slot', font=font(19), fill='#d6c5ad')
    prepared_images = {}
    caption_font = font(17)
    for index, asset in enumerate(assets):
        image = prepare(asset)
        prepared_images[asset['slot']] = image
        x = margin + (index % columns) * (card_width + gap)
        y = top + (index // columns) * (thumb_height + caption_height + gap)
        thumb = ImageOps.fit(image, (card_width, thumb_height), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y + thumb_height, x + card_width - 1, y + thumb_height + caption_height - 1), fill='#101c21')
        draw.text((x + 12, y + thumb_height + 12), f"S{asset['slot']:02d}  ·  {asset['timestamp']}", font=font(17, True), fill='#fff1d4')
        style = 'ANIMÉ' if asset['style'] == 'anime' else 'CINÉMA'
        draw.text((x + 12, y + thumb_height + 37), style, font=font(14, True), fill='#f4bc78' if asset['style'] == 'anime' else '#80ccd5')
        text = re.sub(r',(?=\S)', ', ', asset['source_lyric'])
        lines = wrap(text, caption_font, card_width - 24)
        if len(lines) > 4:
            raise ValueError(f"Légende trop longue au slot {asset['slot']}")
        for row, line in enumerate(lines):
            draw.text((x + 12, y + thumb_height + 59 + row * 19), line, font=caption_font, fill='#e4e5de')
        draw.rectangle((x, y, x + card_width - 1, y + thumb_height + caption_height - 1), outline='#294047', width=1)
    draw.text((width / 2, height - 53), f"Paroles et minutage conservés · {batch['cumulative_generated']} / {batch['total_images_per_format']} fonds portrait · Validation avant la salve suivante",
              font=font(20), anchor='mt', fill='#b6c8c7')
    sheet.alpha_composite(make_badge(), (36, 36))
    destination = ROOT / batch['contact_sheet']
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert('RGB').save(destination, quality=92, subsampling=0)
    preview = next(asset for asset in assets if asset['slot'] == batch['preview_slot'])
    proof(preview, prepared_images[preview['slot']], ROOT / batch['preview_file'])
    print(destination.relative_to(ROOT))
    print(batch['preview_file'])
    print('Sources IA originales intactes ; préparation du ciel S01 enregistrée séparément.')


if __name__ == '__main__':
    main()
