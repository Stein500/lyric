#!/usr/bin/env python3
"""Habille les 10 fonds YouTube 16:9 : recadrage 1920×1080 + bandeau fin.

Le badge n'est volontairement pas fixé dans les images paysage : la correction
artiste demande qu'il apparaisse et disparaisse avec chaque vers au montage.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'work/nonvi_youtube_salve_01'
OUT = ROOT / 'assets/nonvi_konou/youtube_16x9'
W, H = 1920, 1080
FOOTER_H = 30  # même proportion 2,8 % que 54 px sur 1920 vertical
DATA = [
    ('y00_intro', 's00_intro', 'INTRO INSTRUMENTALE'),
    ('y01_wolof', 's01_wolof', 'Wolof TechStein beat wê...'),
    ('y02_yeah', 's02_yeah', 'Yeah... Nonvi konou...'),
    ('y03_on_est_la', 's03_on_est_la', 'On est là, on brille, on remercie...'),
    ('y04_nonvi_sourit', 'ancre_01', 'Nonvi konou, mon frère sourit'),
    ('y05_misere', 's05_misere', 'Gbè manfo do ohin min, la vie ne finit pas dans la misère'),
    ('y06_dokpe', 's06_dokpe', 'Dokpè nou mahou nou kpèè or, remercie Dieu pour le peu'),
    ('y07_vivi', 's07_vivi', 'Gbètché vivi, ma vie me plaît, je suis heureux'),
    ('y08_beat', 's08_beat', 'Wolof TechStein beat wê!'),
    ('y09_millions', 's09_millions', "J'ai pas besoin de millions pour sourire"),
]

def flag(draw, bounds):
    x0, y0, x1, y1 = map(int, bounds)
    split = x0 + (x1 - x0) // 3
    mid = y0 + (y1 - y0) // 2
    draw.rectangle((x0, y0, split - 1, y1), fill='#008751')
    draw.rectangle((split, y0, x1, mid - 1), fill='#FCD116')
    draw.rectangle((split, mid, x1, y1), fill='#E8112D')

def fit_16x9(im):
    im = im.convert('RGB')
    ratio = W / H
    if im.width / im.height > ratio:
        width = round(im.height * ratio)
        left = (im.width - width) // 2
        im = im.crop((left, 0, left + width, im.height))
    else:
        height = round(im.width / ratio)
        top = (im.height - height) // 2
        im = im.crop((0, top, im.width, top + height))
    return im.resize((W, H), Image.Resampling.LANCZOS)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for slot, source_slot, lyric in DATA:
        source = RAW / f'{slot}_brute.png'
        target = OUT / f'{slot}_paysage.png'
        im = fit_16x9(Image.open(source))
        d = ImageDraw.Draw(im)
        d.rectangle((0, H - FOOTER_H - 2, W, H - FOOTER_H - 1), fill='#ECC265')
        flag(d, (0, H - FOOTER_H, W, H))
        im.save(target, optimize=True)
        manifest.append({'index': len(manifest), 'slot': slot, 'source_slot': source_slot,
                         'lyric': lyric, 'image': target.name, 'status': 'created'})
    (OUT / 'plan_images_youtube_16x9.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

    # Planche 5×2 facile à lire, sans simuler de paroles ni badge fixe.
    slot_font = ImageFont.truetype(ROOT / 'assets/fonts/DejaVuSans-Bold.ttf', 22)
    label_font = ImageFont.truetype(ROOT / 'assets/fonts/DejaVuSans-Bold.ttf', 17)
    cols, cw, ch, pad = 5, 382, 294, 14
    board = Image.new('RGB', (cols * cw + pad, 2 * ch + pad), (9, 22, 30))
    bd = ImageDraw.Draw(board)
    for i, item in enumerate(manifest):
        im = Image.open(OUT / item['image']).convert('RGB').resize((360, 203), Image.Resampling.LANCZOS)
        x = pad + (i % cols) * cw
        y = pad + (i // cols) * ch
        board.paste(im, (x, y))
        bd.text((x, y + 210), item['slot'], font=slot_font, fill=(252, 213, 130))
        words = item['lyric'].split()
        rows, current = [], []
        for word in words:
            candidate = ' '.join(current + [word])
            if current and bd.textlength(candidate, font=label_font) > 354:
                rows.append(' '.join(current)); current = [word]
            else:
                current.append(word)
        if current: rows.append(' '.join(current))
        for row, label in enumerate(rows[:2]):
            bd.text((x, y + 240 + row * 21), label, font=label_font, fill=(245, 245, 238))
    board.save(OUT / 'planche_youtube_16x9_salve_01.jpg', quality=91, optimize=True)
    print('10 paysages habillés, manifeste et planche :', OUT)

if __name__ == '__main__':
    main()
