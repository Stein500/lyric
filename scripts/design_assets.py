#!/usr/bin/env python3
"""Titres et covers composés en post sur les fonds approuvés, aucune nouvelle IA."""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from render_ancre import ROOT, draw_flag, badge_sprite

FONT_TITLE = ROOT/'assets/fonts/GreatVibes-Regular.ttf'
FONT_UI = ROOT/'assets/fonts/DejaVuSans-Bold.ttf'
COLOR = (251, 231, 189, 255)
PAD = 18


def title_sprite(max_width=880, size=182):
    lines = ['Concentré', 'sur le chemin']
    while size >= 72:
        font = ImageFont.truetype(str(FONT_TITLE), size)
        bboxes = [font.getbbox(line, stroke_width=2) for line in lines]
        if max(b[2]-b[0] for b in bboxes)+2*PAD <= max_width:
            break
        size -= 2
    widths = [b[2]-b[0] for b in bboxes]
    heights = [b[3]-b[1] for b in bboxes]
    gap = max(18, round(size*.13))
    width = max(widths)+2*PAD
    height = sum(heights)+gap+2*PAD
    mask = Image.new('L', (width, height))
    d = ImageDraw.Draw(mask)
    top = PAD
    for line, bbox, tw, th in zip(lines, bboxes, widths, heights):
        d.text(((width-tw)/2-bbox[0], top-bbox[1]), line, font=font, fill=255,
               stroke_width=1, stroke_fill=255)
        top += th+gap
    shadow = mask.filter(ImageFilter.GaussianBlur(5))
    result = Image.new('RGBA', (width, height))
    dark = Image.new('RGBA', result.size, (2, 5, 10, 0)); dark.putalpha(shadow.point(lambda a: round(a*.95)))
    result.alpha_composite(dark)
    outline = mask.filter(ImageFilter.MaxFilter(5))
    ink = Image.new('RGBA', result.size, (15, 11, 10, 0)); ink.putalpha(outline.point(lambda a: round(a*.9)))
    result.alpha_composite(ink)
    gold = Image.new('RGBA', result.size, COLOR); gold.putalpha(mask)
    result.alpha_composite(gold)
    return result


def ui_sprite(text, size=40, max_width=880, fill=(243, 237, 224, 255)):
    while size >= 18:
        font = ImageFont.truetype(str(FONT_UI), size)
        box = font.getbbox(text, stroke_width=1)
        if box[2]-box[0]+16 <= max_width:
            break
        size -= 1
    result = Image.new('RGBA', (box[2]-box[0]+16, box[3]-box[1]+16))
    ImageDraw.Draw(result).text((8-box[0], 8-box[1]), text, font=font, fill=fill,
                                stroke_width=1, stroke_fill=(4, 8, 14, 235))
    return result


def centered(image, sprite, cx, cy):
    x, y = round(cx-sprite.width/2), round(cy-sprite.height/2)
    image.alpha_composite(sprite, (x, y))
    return [x, y, x+sprite.width, y+sprite.height]


def add_badge(image, y=156, opacity=0.75):
    sprite = badge_sprite().copy()
    sprite.putalpha(sprite.getchannel('A').point(lambda a: round(a*opacity)))
    image.alpha_composite(sprite, ((image.width-sprite.width)//2, y))


def soft_scrim(image, center, sigma, start_y=0, strength=110):
    w, h = image.size
    rows = np.arange(h, dtype=float)
    alpha = strength*np.exp(-0.5*((rows-center)/sigma)**2)
    if start_y:
        alpha *= np.clip((rows-start_y)/70, 0, 1)
    pixels = np.zeros((h, w, 4), dtype=np.uint8)
    pixels[:, :, 3] = alpha[:, None].astype(np.uint8)
    image.alpha_composite(Image.fromarray(pixels))


def make_covers():
    records = json.loads((ROOT/'productions/concentre_sur_le_chemin/backgrounds_manifest.json').read_text())
    def load(fmt, slot):
        entry = next(r for r in records if r['format']==fmt and r['slot']==slot)
        return Image.open(ROOT/entry['background_cache']).convert('RGBA')
    portrait = load('portrait', 's01')
    specs = [
        ('1080x1080', portrait.crop((0, 120, 1080, 1200)), 540, 754, 966, 154, 86),
        ('9x16', portrait.copy(), 540, 993, 1264, 188, 156),
        ('16x9', load('landscape', 's05'), 1220, 528, 780, 206, 144),
    ]
    reports = []
    for suffix, image, cx, cy, artist_y, size, badge_y in specs:
        max_w = 870 if image.width==1080 else 1000
        soft_scrim(image, cy+60, 225 if image.height>1080 else 180,
                   615 if suffix=='1080x1080' else (715 if suffix=='9x16' else 360), 125)
        title = title_sprite(max_w, size)
        title_box = centered(image, title, cx, cy)
        artist = ui_sprite('Daïsky', 44 if image.width==1080 else 56)
        artist_box = centered(image, artist, cx, artist_y)
        add_badge(image, badge_y)
        flag_h = 54 if image.height==1920 else 30
        draw_flag(image, (0, image.height-flag_h, image.width, flag_h))
        destination = ROOT/f'livrables/cover_concentre_sur_le_chemin_{suffix}.jpg'
        image.convert('RGB').save(destination, quality=96, subsampling=0)
        reports.append({'file': str(destination.relative_to(ROOT)), 'size': list(image.size),
                        'title': 'Concentré sur le chemin', 'artist': 'Daïsky',
                        'title_bbox': title_box, 'artist_bbox': artist_box,
                        'flag_height': flag_h, 'new_ai_generations': 0})
    (ROOT/'productions/concentre_sur_le_chemin/covers_report.json').write_text(
        json.dumps(reports, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(reports, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    make_covers()
