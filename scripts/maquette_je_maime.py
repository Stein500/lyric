#!/usr/bin/env python3
"""Maquette d'ancrage 9:16 : image sans texte + typographie et badge en post.

Ce JPEG est une maquette à valider, pas une frame du clip définitif.
Le badge sera identique et posé en dernier sur chaque frame du futur rendu.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
WIDTH, HEIGHT = 1080, 1920


def make_badge():
    badge = Image.new('RGBA', (332, 94))
    draw = ImageDraw.Draw(badge)
    draw.rounded_rectangle((0, 0, 331, 93), radius=16,
                           fill=(7, 18, 21, 205), outline=(74, 213, 224, 230), width=2)
    draw.polygon([(36, 15), (18, 45), (31, 45), (24, 76),
                  (50, 37), (36, 37), (45, 15)], fill=(255, 200, 101, 255))
    draw.text((63, 14), 'DAÏSKY PROD', anchor='lt',
              font=ImageFont.truetype(str(FONT_DIR / 'DejaVuSans-Bold.ttf'), 27),
              fill=(255, 247, 229, 255))
    draw.text((63, 53), '@daiskypro', anchor='lt',
              font=ImageFont.truetype(str(FONT_DIR / 'DejaVuSans.ttf'), 21),
              fill=(155, 222, 227, 255))
    return badge


def main():
    source = ROOT / 'projets/je_maime_tellement/assets/ancrage/charte_A.png'
    destination = ROOT / 'livrables/Je_maime_tellement_ancrage_A_9x16_v1.jpg'
    destination.parent.mkdir(parents=True, exist_ok=True)
    image = ImageOps.fit(Image.open(source).convert('RGB'), (WIDTH, HEIGHT),
                         method=Image.Resampling.LANCZOS).convert('RGBA')
    # Contraste local discret sous les paroles ; aucune modification du portrait.
    shade = Image.new('RGBA', (1, HEIGHT))
    pixels = shade.load()
    for y in range(HEIGHT):
        opacity = int(75 * max(0, min(1, (y - HEIGHT * 0.67) / (HEIGHT * 0.30))))
        pixels[0, y] = (5, 12, 17, opacity)
    image = Image.alpha_composite(image, shade.resize((WIDTH, HEIGHT)))
    text = Image.new('RGBA', image.size)
    glow = Image.new('RGBA', image.size)
    draw, soft = ImageDraw.Draw(text), ImageDraw.Draw(glow)
    font = ImageFont.truetype(str(FONT_DIR / 'DejaVuSans.ttf'), 58)
    # Vers fourni à 00:30.47. Seuls les espaces typographiques et le wrap changent.
    lines = ["Je m'aime tellement,", 'fort, sensationnel, triste']
    for index, line in enumerate(lines):
        assert draw.textlength(line, font=font) <= 920
        position = (WIDTH // 2, HEIGHT - 300 + index * 80)
        soft.text(position, line, font=font, anchor='mt', fill=(255, 183, 75, 110), stroke_width=3)
        draw.text(position, line, font=font, anchor='mt', fill=(255, 247, 230, 255),
                  stroke_width=2, stroke_fill=(17, 14, 13, 230))
    image = Image.alpha_composite(image, glow.filter(ImageFilter.GaussianBlur(7)))
    image = Image.alpha_composite(image, text)
    image.alpha_composite(make_badge(), (36, 36))  # Toujours en dernier, position fixe.
    image.convert('RGB').save(destination, quality=92, subsampling=0)
    print(destination.relative_to(ROOT))


if __name__ == '__main__':
    main()
