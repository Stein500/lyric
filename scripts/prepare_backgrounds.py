#!/usr/bin/env python3
"""Nettoyage local et planche de validation, sans autre génération IA.

Le lettrage du plafond et les aplats parasites sont corrigés uniquement dans
le décor. Les paysages s03/s04 restent à recadrer (pas de plein pied) et ne sont
PAS exportés comme images prêtes. Les originaux IA sont conservés.
"""
from pathlib import Path
import hashlib
import json
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from render_ancre import ROOT, draw_flag, reframe_background

RAW = ROOT/'assets/raw/concentre_sur_le_chemin'
WORK = ROOT/'work/concentre_sur_le_chemin/backgrounds'
EXPORT = ROOT/'livrables/images_concentre_sur_le_chemin'
NAMES = {'s01': 'Tête lourde', 's02': 'Dans le bruit', 's03': 'Tenir le cap',
         's04': 'Patience', 's05': 'Encore debout'}
NEEDS_REFRAME = {('landscape', 's03'), ('landscape', 's04')}


def clean_ceiling_caption(rgb):
    """Masque des seuls pixels du lettrage, dans le plafond loin du personnage."""
    mask = np.zeros(rgb.shape[:2], dtype=np.uint8)
    region = rgb[94:175, 125:656]
    is_letter = ((region[:, :, 0] > 90) & (region[:, :, 1] > 85) & (region[:, :, 2] > 70))
    mask[94:175, 125:656] = np.where(is_letter, 255, 0).astype(np.uint8)
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    fixed = cv2.inpaint(rgb, mask, 5, cv2.INPAINT_TELEA)
    # The whole face, hands and body are well below this ceiling mask.
    if not np.array_equal(fixed[210:], rgb[210:]):
        raise AssertionError('Nettoyage du plafond hors de sa zone autorisée.')
    return fixed


def remove_background_band(rgb, slot):
    """Corrige l'assombrissement rectangulaire du décor, masqués sur les bords.

    Les zones de transition situées entre le personnage et le bord ont des
    coordonnées propres à chaque image inspectée, car le buste et la lampe
    chevauchent la bande. Ce n'est ni un rééclairage du visage ni une réparation
    générique : le visage, les mains et le corps ne sont jamais modifiés.
    """
    settings = {
        's01': (313, 468, 2.98, 2.98, [(313, 526), (380, 540), (440, 533), (468, 551)], None),
        's02': (275, 502, 2.85, 2.74, [(275, 620), (350, 635), (420, 630), (455, 651), (502, 660)], None),
        's03': (281, 507, 2.30, 2.30, [(281, 572), (350, 594), (450, 620), (507, 626)],
                [(281, 106), (350, 86), (420, 64), (507, 66)])
    }
    if slot not in settings:
        return rgb
    y0, y1, gain_top, gain_bottom, edge, left_edge = settings[slot]
    height, width = rgb.shape[:2]
    xs = np.arange(width)
    mask = np.zeros((height, width), dtype=np.float32)
    gain = np.ones(height, dtype=np.float32)
    for y in range(y0, y1):
        right = np.interp(y, [v[0] for v in edge], [v[1] for v in edge])
        mask[y] = np.clip((xs-right)/3, 0, 1)
        if left_edge:
            left = np.interp(y, [v[0] for v in left_edge], [v[1] for v in left_edge])
            mask[y] = np.maximum(mask[y], np.clip((left-xs)/3, 0, 1))
        gain[y] = gain_top+(gain_bottom-gain_top)*(y-y0)/max(1, y1-y0-1)
    fixed = rgb.astype(np.float32)*(1+mask[:, :, None]*(gain[:, None, None]-1))
    fixed = np.clip(fixed, 0, 255).astype(np.uint8)
    # Two very thin joins in the decor only: remove the hard antialiased edges.
    joins = np.zeros((height, width), dtype=np.uint8)
    right_max = int(max(v[1] for v in edge))+8
    for y in (y0, y1):
        joins[max(0, y-4):min(height, y+4), right_max:] = 255
    fixed = cv2.inpaint(fixed, joins, 3, cv2.INPAINT_TELEA)
    return fixed


def fit_landscape(image):
    """Petit recul non génératif pour conserver le personnage au-dessus du drapeau."""
    frame = ImageOps.fit(image, (1920, 1080), method=Image.Resampling.LANCZOS)
    small = frame.resize((1766, 994), Image.Resampling.LANCZOS)
    # No face/body stretch. Only the empty margins of the physical room extend.
    array = np.asarray(small)
    padded = cv2.copyMakeBorder(array, 5, 81, 77, 77, cv2.BORDER_REPLICATE)
    return Image.fromarray(padded)


def prepare():
    records = []
    for fmt in ('portrait', 'landscape'):
        for source in sorted((RAW/fmt).glob('s*.png')):
            slot = source.name.split('_')[0]
            image = Image.open(source).convert('RGB')
            rgb = np.asarray(image).copy()
            corrections = []
            if fmt == 'portrait' and slot == 's02':
                rgb = clean_ceiling_caption(rgb)
                corrections.append('retrait local du lettrage parasite dans le plafond, hors personnage')
            if fmt == 'landscape' and slot in ('s01', 's02', 's03'):
                rgb = remove_background_band(rgb, slot)
                corrections.append('correction du seul assombrissement rectangulaire du décor, frontières masquées image par image autour du personnage')
            native = WORK/fmt/source.name
            native.parent.mkdir(parents=True, exist_ok=True)
            Image.fromarray(rgb).save(native)
            if fmt == 'portrait':
                final = reframe_background(native)
                corrections.append('reprise du cadrage de l’ancre : plafond −120 px, prolongement du sol vide')
            else:
                final = fit_landscape(Image.fromarray(rgb))
                corrections.append('recul proportionnel 92 %, marges du décor prolongées ; aucun étirement du héros')
            base = native.with_name(source.stem+'_frame.png')
            final.save(base)
            flag_height = 54 if fmt == 'portrait' else 30
            draw_flag(final, (0, final.height-flag_height, final.width, flag_height))
            proof = native.with_name(source.stem+'_flag.png')
            final.save(proof)
            ready = (fmt, slot) not in NEEDS_REFRAME
            destination = EXPORT/fmt/(source.stem+'.jpg')
            if ready:
                destination.parent.mkdir(parents=True, exist_ok=True)
                final.save(destination, quality=95, subsampling=0)
            records.append({'slot': slot, 'name': NAMES[slot], 'format': fmt,
                            'raw': str(source.relative_to(ROOT)), 'raw_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                            'raw_size': list(image.size), 'size': list(final.size),
                            'background_cache': str(base.relative_to(ROOT)), 'flag_proof': str(proof.relative_to(ROOT)),
                            'export': str(destination.relative_to(ROOT)) if ready else None,
                            'technical_status': 'ready_for_artist_review' if ready else 'needs_full_figure_reframe',
                            'artist_approved': fmt == 'portrait' and slot == 's01',
                            'corrections': corrections, 'flag_height': flag_height})
    if len(records) != 10:
        raise AssertionError('Il faut exactement cinq scènes dans chaque format.')
    (ROOT/'productions/concentre_sur_le_chemin/backgrounds_manifest.json').write_text(
        json.dumps(records, ensure_ascii=False, indent=2)+'\n')
    return records


def contact_sheet(records):
    width, height = 1600, 3820
    sheet = Image.new('RGB', (width, height), '#0d1420')
    draw = ImageDraw.Draw(sheet)
    title_font = ImageFont.truetype(str(ROOT/'assets/fonts/BarlowCondensed-Bold.ttf'), 68)
    subtitle_font = ImageFont.truetype(str(ROOT/'assets/fonts/DejaVuSans-Bold.ttf'), 25)
    caption_font = ImageFont.truetype(str(ROOT/'assets/fonts/DejaVuSans-Bold.ttf'), 24)
    draw.text((48, 32), 'CONCENTRÉ SUR LE CHEMIN', font=title_font, fill='#f8e6ba')
    draw.text((50, 116), '5 SCÈNES · PORTRAIT + PAYSAGE · PLANCHE DE CONTRÔLE', font=subtitle_font, fill='#a7b6c8')
    draw.text((50, 155), '8 cadrages prêts à valider · 2 paysages signalés à reprendre', font=caption_font, fill='#f3c474')
    for row, slot in enumerate(NAMES):
        y = 222+row*710
        draw.text((50, y), f'{row+1:02}  {NAMES[slot]}', font=subtitle_font, fill='#f2ede5')
        draw.text((50, y+40), '9:16', font=caption_font, fill='#a7b6c8')
        draw.text((430, y+40), '16:9', font=caption_font, fill='#a7b6c8')
        for fmt, x, box in [('portrait', 50, (304, 540)), ('landscape', 430, (1120, 630))]:
            entry = next(e for e in records if e['slot'] == slot and e['format'] == fmt)
            image = Image.open(ROOT/entry['flag_proof']).convert('RGB')
            if fmt == 'landscape':
                box = (1066, 600)
            thumb = ImageOps.contain(image, box)
            sheet.paste(thumb, (x, y+78))
            if entry['technical_status'] != 'ready_for_artist_review':
                # Review label is on the sheet, never on the actual background.
                draw.rounded_rectangle((x+16, y+94, x+710, y+137), radius=7, fill='#6b3e1d')
                draw.text((x+29, y+99), 'À REPRENDRE : CADRAGE PAS PLEIN PIED',
                          font=caption_font, fill='#fff1cd')
        if row < 4:
            draw.line((50, y+690, 1550, y+690), fill='#293446', width=1)
    destination = ROOT/'livrables/Concentre_sur_le_chemin_planche_10_fonds_v1.jpg'
    sheet.save(destination, quality=93, subsampling=0)
    return destination


def main():
    records = prepare()
    path = contact_sheet(records)
    print(path)
    print('Prêts techniquement :', sum(r['technical_status']=='ready_for_artist_review' for r in records), '/ 10')


if __name__ == '__main__':
    main()
