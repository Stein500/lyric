#!/usr/bin/env python3
"""Cover TikTok 9:16 (1080×1920), tout en cursive, à partir d'un fond existant.

Aucune nouvelle génération d'image : réutilisation autorisée des fonds.
Zones sûres TikTok respectées : texte centré, rien d'important sur les bords
droit (icônes) et bas (légende).
"""
from __future__ import annotations
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from je_maime_common import *
from maquette_je_maime import make_badge

OUT = DELIVER / 'cover_tiktok_Je_maime_tellement_9x16.jpg'
SOURCE_SLOT = 21  # même héroïne que la cover MP3 : câlin à soi, doré, charte A


def cursive_line(image, y, text, size, color, max_width=880, glow_alpha=0):
    while font(size, cursive=True).getlength(text) > max_width:
        size -= 2
    face = font(size, cursive=True)
    halo = Image.new('RGBA', image.size)
    ImageDraw.Draw(halo).text((540, y), text, font=face, anchor='mm', fill=(12, 17, 22, 215))
    image = Image.alpha_composite(image, halo.filter(ImageFilter.GaussianBlur(6)))
    if glow_alpha:
        glow = Image.new('RGBA', image.size)
        ImageDraw.Draw(glow).text((540, y), text, font=face, anchor='mm',
                                  fill=(255, 196, 105, glow_alpha), stroke_width=2)
        image = Image.alpha_composite(image, glow.filter(ImageFilter.GaussianBlur(9)))
    ImageDraw.Draw(image).text((540, y), text, font=face, anchor='mm', fill=color)
    return image


def main():
    config, audit = assert_sources_unchanged()
    asset = assets_by_slot()[SOURCE_SLOT]
    source = resolve_asset(asset['render_source'])
    image = ImageOps.fit(Image.open(source).convert('RGB'), (1080, 1920),
                         Image.Resampling.LANCZOS, centering=(.5, .32)).convert('RGBA')
    # Voile sombre progressif en bas pour asseoir le bloc titre.
    shade = Image.new('RGBA', (1, 1920))
    for y in range(1920):
        alpha = int(215 * max(0.0, min(1.0, (y - 1150) / 560)))
        shade.putpixel((0, y), (5, 11, 16, alpha))
    image = Image.alpha_composite(image, shade.resize((1080, 1920)))
    # Léger voile en haut, sous le badge, pour l'équilibre.
    top = Image.new('RGBA', (1, 1920))
    for y in range(1920):
        alpha = int(110 * max(0.0, min(1.0, (260 - y) / 260)))
        top.putpixel((0, y), (5, 11, 16, alpha))
    image = Image.alpha_composite(image, top.resize((1080, 1920)))

    title = config['approved']['title']
    image = cursive_line(image, 1462, title, 150, '#ffefd0', max_width=960, glow_alpha=130)
    # Filet doré discret de part et d'autre du bloc artiste.
    draw = ImageDraw.Draw(image)
    draw.line((330, 1568, 750, 1568), fill=(229, 177, 103, 210), width=2)
    image = cursive_line(image, 1650, 'Daïsky Pro · Success', 78, '#fff4dd')
    image = cursive_line(image, 1756, 'Daïsky Prod / TechStein · Rap · 2026', 54, '#dcE8e6')
    image.alpha_composite(make_badge(), (36, 36))
    image.convert('RGB').save(OUT, quality=92, subsampling=0)
    with Image.open(OUT) as check:
        assert check.size == (1080, 1920)
    print('Cover TikTok :', OUT.relative_to(ROOT), OUT.stat().st_size, 'octets ; SHA-256', sha256(OUT))


if __name__ == '__main__':
    main()
