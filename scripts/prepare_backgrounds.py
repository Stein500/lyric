#!/usr/bin/env python3
"""Préparer exactement 5 portraits + 5 paysages et leur planche de validation.

Révision du 29 septembre 2026 : les paysages ont été recomposés, les anciens
masques d'éclaircissement rectangulaires ne doivent JAMAIS leur être appliqués.
Les originaux restent inchangés ; seul le décor parasite est nettoyé en cache.
Badge absent des fonds pour permettre son fondu indépendant dans le clip.
"""
from pathlib import Path
import hashlib
import json
import zipfile

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from render_ancre import ROOT, draw_flag, reframe_background

RAW = ROOT/'assets/raw/concentre_sur_le_chemin'
WORK = ROOT/'work/concentre_sur_le_chemin/backgrounds'
EXPORT = ROOT/'livrables/images_concentre_sur_le_chemin'
PLAN = ROOT/'productions/concentre_sur_le_chemin/landscape_corrections_v2.json'
NAMES = {'s01': 'Tête lourde', 's02': 'Dans le bruit', 's03': 'Tenir le cap',
         's04': 'Patience', 's05': 'Encore debout'}
PORTRAIT_CAPTION_SHA = '583ad4d95b2cb15635bd8d178caf35dd851524a5bb535e34e54b02d731019d9b'
FOOTER_COLORS = [(0, 135, 81), (252, 209, 22), (232, 17, 45)]


def local_inpaint(rgb, mask, radius=5):
    """Contrôle strict : aucun pixel extérieur au masque local ne change."""
    fixed = cv2.inpaint(rgb, mask, radius, cv2.INPAINT_TELEA)
    if not np.array_equal(fixed[mask == 0], rgb[mask == 0]):
        raise AssertionError('Une correction locale a débordé de son masque.')
    return fixed


def clean_ceiling_caption(rgb):
    """Portrait s02 v1 uniquement : lettrage situé dans le plafond vide."""
    if rgb.shape[:2] != (1376, 768):
        raise ValueError('Le masque du plafond exige le cadrage original inspecté.')
    mask = np.zeros(rgb.shape[:2], dtype=np.uint8)
    region = rgb[94:175, 125:656]
    is_letter = ((region[:, :, 0] > 90) & (region[:, :, 1] > 85) & (region[:, :, 2] > 70))
    mask[94:175, 125:656] = np.where(is_letter, 255, 0).astype(np.uint8)
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    fixed = local_inpaint(rgb, mask)
    if not np.array_equal(fixed[210:], rgb[210:]):
        raise AssertionError('Le héros doit rester strictement intact.')
    return fixed


def clean_reference_stickers(rgb):
    """Paysage s03 v2 : trois autocollants et trois faux libellés d'appareil.

    Masques limités au plafond et au rack à droite. La personne dans le tiers
    gauche, son visage, les mains et les vêtements restent pixel pour pixel
    identiques. Les commandes matérielles de la console sont conservées.
    """
    if rgb.shape[:2] != (768, 1376):
        raise ValueError('Le masque exige le paysage original inspecté.')
    # Isolate the three saturated stickers, not a rectangle touching the beam.
    region = rgb[116:177, 610:770].astype(np.int16)
    r, g, b = region[:, :, 0], region[:, :, 1], region[:, :, 2]
    selected = (((r-g > 45) & (r-b > 45) & (r > 140)) |
                ((g-r > 28) & (g-b > 20) & (g > 110)) |
                ((b-r > 30) & (b-g > 18) & (b > 120))).astype(np.uint8)
    _, labels, stats, _ = cv2.connectedComponentsWithStats(selected)
    local = np.zeros(selected.shape, dtype=np.uint8)
    count = 0
    for label, stat in enumerate(stats[1:], 1):
        if stat[cv2.CC_STAT_AREA] > 400:
            points = cv2.findNonZero((labels == label).astype(np.uint8))
            cv2.fillConvexPoly(local, cv2.convexHull(points), 255)
            count += 1
    if count != 3:
        raise AssertionError('Le masque inspecté doit trouver exactement trois autocollants.')
    mask = np.zeros(rgb.shape[:2], dtype=np.uint8)
    mask[116:177, 610:770] = local
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    mask[:122] = 0  # retain the structural ceiling beam
    # Generated gibberish on three small device labels; keep sockets and dials.
    for x1, y1, x2, y2 in [(948, 469, 1007, 489), (954, 507, 990, 523), (960, 525, 980, 540)]:
        mask[y1:y2, x1:x2] = 255
    fixed = local_inpaint(rgb, mask, radius=7)
    if not np.array_equal(fixed[:, :600], rgb[:, :600]):
        raise AssertionError('Le héros dans le tiers gauche doit rester strictement intact.')
    return fixed


def fit_landscape(image):
    """Relever le cadrage de 80 px, sans bordure floue ni étirer la personne.

    Le plafond contient de la marge ; le bas est prolongé par un dégradé de sol
    calculé depuis sa dernière rangée, limité aux pixels ajoutés. Ni duplication
    de chaussures, ni bandes latérales de remplissage. Tous les pixels d'image
    conservés sont inchangés après la mise au format proportionnelle.
    """
    frame = ImageOps.fit(image, (1920, 1080), method=Image.Resampling.LANCZOS)
    rgb = np.asarray(frame)
    shift = 80
    result = np.empty_like(rgb)
    result[:-shift] = rgb[shift:]
    row = rgb[-1:].astype(np.float32)
    smooth = cv2.GaussianBlur(row, (0, 0), sigmaX=75, sigmaY=0.1)
    # Fade out fine vertical structures rather than continuing a shoe-shaped line.
    blend = np.minimum(np.arange(shift, dtype=np.float32)/22, 1)[:, None, None]
    floor = row*(1-blend)+smooth*blend
    result[-shift:] = np.clip(floor, 0, 255).astype(np.uint8)
    if not np.array_equal(result[:-shift], rgb[shift:]):
        raise AssertionError('Le recadrage ne doit pas retoucher le héros.')
    return Image.fromarray(result)


def fit_portrait(path, slot):
    frame = reframe_background(path)
    if slot != 's01':
        # Only the floor extension added below the original pixels is softened.
        # Preserve the approved anchor's precise composition unchanged.
        floor = frame.crop((0, 1800, 1080, 1920)).filter(ImageFilter.GaussianBlur(52))
        blend = Image.new('L', (1080, 120))
        alpha = np.minimum(np.arange(120) / 28, 1) * 255
        blend = Image.fromarray(np.broadcast_to(alpha[:, None], (120, 1080)).astype(np.uint8))
        frame.paste(floor, (0, 1800), blend)
    return frame


def verify_flag(image, height, tolerance=0):
    w, h = image.size
    points = [(w//6, h-height//2), (2*w//3, h-height+height//4),
              (2*w//3, h-max(1, height//4))]
    for point, expected in zip(points, FOOTER_COLORS):
        actual = image.getpixel(point)[:3]
        if max(abs(a-b) for a, b in zip(actual, expected)) > tolerance:
            raise AssertionError(('Drapeau incorrect', point, actual, expected))


def prepare():
    plan = json.loads(PLAN.read_text())
    jobs = {job['slot']: job for job in plan}
    records = []
    for fmt in ('portrait', 'landscape'):
        sources = sorted((RAW/fmt).glob('s*.png'))
        if len(sources) != 5 or {p.stem.split('_')[0] for p in sources} != set(NAMES):
            raise AssertionError(f'{fmt} exige exactement les slots s01 à s05, sans doublon.')
        for source in sources:
            slot = source.stem.split('_')[0]
            sha = hashlib.sha256(source.read_bytes()).hexdigest()
            image = Image.open(source).convert('RGB')
            rgb = np.asarray(image).copy()
            corrections = []
            if fmt == 'portrait' and slot == 's02':
                if sha != PORTRAIT_CAPTION_SHA:
                    raise ValueError('Portrait modifié : revoir le masque avant de le réutiliser.')
                rgb = clean_ceiling_caption(rgb)
                corrections.append('lettrage parasite retiré localement du plafond ; personnage intact')
            if fmt == 'landscape':
                job = jobs[slot]
                if sha != job.get('generated_sha256'):
                    raise ValueError(f'{slot} ne correspond pas au paysage révision 2 inspecté.')
                if slot == 's03':
                    rgb = clean_reference_stickers(rgb)
                    corrections.append('trois autocollants au plafond et trois faux libellés du rack retirés localement ; héros intact')
            native = WORK/fmt/source.name
            native.parent.mkdir(parents=True, exist_ok=True)
            Image.fromarray(rgb).save(native)
            if fmt == 'portrait':
                final = fit_portrait(native, slot)
                corrections.append('cadrage au-dessus des paroles, plafond −120 px, sol vide prolongé')
                if slot != 's01':
                    corrections.append('adoucissement du sol ajouté uniquement, aucun pixel original du héros modifié')
            else:
                final = fit_landscape(Image.fromarray(rgb))
                corrections.append('cadrage relevé de 80 px ; dégradé de sol ajouté uniquement en bas, sans bordures latérales ni étirement du héros')
            base = native.with_name(source.stem+'_frame.png')
            final.save(base)
            flag_height = 54 if fmt == 'portrait' else 30
            draw_flag(final, (0, final.height-flag_height, final.width, flag_height))
            verify_flag(final, flag_height)
            proof = native.with_name(source.stem+'_flag.png')
            final.save(proof)
            destination = EXPORT/fmt/(source.stem+'.jpg')
            destination.parent.mkdir(parents=True, exist_ok=True)
            final.save(destination, quality=95, subsampling=0)
            verify_flag(Image.open(destination).convert('RGB'), flag_height, tolerance=5)
            records.append({
                'slot': slot, 'name': NAMES[slot], 'format': fmt,
                'raw': str(source.relative_to(ROOT)), 'raw_sha256': sha,
                'raw_size': list(image.size), 'size': list(final.size),
                'generation_revision': 2 if fmt == 'landscape' else 1,
                'background_cache': str(base.relative_to(ROOT)), 'flag_proof': str(proof.relative_to(ROOT)),
                'export': str(destination.relative_to(ROOT)),
                'export_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
                'technical_status': 'ready_for_artist_review',
                'artist_approved': fmt == 'portrait' and slot == 's01',
                'corrections': corrections, 'flag_height': flag_height,
                'badge_baked_in': False,
            })
    (ROOT/'productions/concentre_sur_le_chemin/backgrounds_manifest.json').write_text(
        json.dumps(records, ensure_ascii=False, indent=2)+'\n')
    return records


def contact_sheet(records):
    width, height = 1580, 3816
    sheet = Image.new('RGB', (width, height), '#0b1420')
    d = ImageDraw.Draw(sheet)
    title = ImageFont.truetype(str(ROOT/'assets/fonts/BarlowCondensed-Bold.ttf'), 72)
    label = ImageFont.truetype(str(ROOT/'assets/fonts/DejaVuSans-Bold.ttf'), 27)
    small = ImageFont.truetype(str(ROOT/'assets/fonts/DejaVuSans-Bold.ttf'), 23)
    eyebrow = ImageFont.truetype(str(ROOT/'assets/fonts/DejaVuSans-Bold.ttf'), 21)
    d.text((60, 32), 'DAÏSKY   /   DIRECTION VISUELLE', font=eyebrow, fill='#a4b6c5')
    d.text((56, 70), 'CONCENTRÉ SUR LE CHEMIN', font=title, fill='#f4e7cc')
    d.text((60, 164), '5 SCÈNES · 5 PORTRAITS + 5 PAYSAGES', font=label, fill='#c4d0db')
    d.text((60, 210), 'Ancre approuvée  /  Série complète à confirmer avant le rendu des clips', font=small, fill='#a4b6c5')
    d.line((60, 262, width-60, 262), fill='#8f764f', width=2)
    for row, slot in enumerate(NAMES):
        y = 304+row*684
        d.text((60, y), f'0{row+1}', font=label, fill='#d9b67c')
        d.text((118, y), NAMES[slot].upper(), font=label, fill='#eee9df')
        if slot == 's01':
            d.text((width-480, y+2), 'PORTRAIT ANCRE VALIDÉ', font=eyebrow, fill='#8cad9d')
        d.text((60, y+47), 'PORTRAIT  ·  1080 × 1920', font=eyebrow, fill='#92a4b5')
        d.text((500, y+47), 'YOUTUBE  ·  1920 × 1080', font=eyebrow, fill='#92a4b5')
        for fmt, x, box in [('portrait', 60, (320, 570)), ('landscape', 500, (1168, 657))]:
            entry = next(r for r in records if r['slot'] == slot and r['format'] == fmt)
            image = Image.open(ROOT/entry['flag_proof']).convert('RGB')
            # Same displayed height for the two formats, with no cropping.
            if fmt == 'landscape':
                box = (1014, 570)
            thumb = ImageOps.contain(image, box)
            sheet.paste(thumb, (x, y+82))
        d.line((60, y+666, width-60, y+666), fill='#233243', width=1)
    d.text((60, height-66), 'BADGE ANIMÉ AJOUTÉ AU MONTAGE · AUCUN BADGE PERMANENT DANS LES FONDS',
           font=eyebrow, fill='#8fa3b7')
    destination = ROOT/'livrables/Concentre_sur_le_chemin_planche_10_fonds_v2.jpg'
    sheet.save(destination, quality=94, subsampling=0)
    return destination


def bundle_images(records):
    destination = ROOT/'livrables/Concentre_sur_le_chemin_10_images_v2.zip'
    readme = ('CONCENTRÉ SUR LE CHEMIN — 10 FONDS À VALIDER\n\n'
              '5 portraits 1080×1920 et 5 paysages 1920×1080, cinq scènes communes.\n'
              'Bandeau Bénin : 54 px en portrait, 30 px en paysage.\n'
              'Aucun badge gravé : Dsky et son drapeau apparaîtront/disparaîtront\n'
              'à chaque vers dans les clips. La typographie s’ajoute au montage.\n'
              'L’ancre portrait s01 est approuvée ; les autres compositions restent\n'
              'à confirmer par l’artiste. Ce pack ne contient pas les clips finaux.\n')
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
        archive.writestr('LISEZ_MOI.txt', readme)
        for row in records:
            path = ROOT/row['export']
            archive.write(path, f"{row['format']}/{path.name}")
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None or len([n for n in archive.namelist() if n.endswith('.jpg')]) != 10:
            raise AssertionError('Archive incomplète ou corrompue.')
    return destination


def main():
    records = prepare()
    print(contact_sheet(records))
    print(bundle_images(records))
    print('10/10 images exportées, 20 contrôles de drapeau PNG/JPG réussis. Validation artiste en attente.')


if __name__ == '__main__':
    main()
