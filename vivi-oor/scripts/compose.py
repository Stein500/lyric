#!/usr/bin/env python3
"""Recompose ten 9:16 PNGs with the real, unretouched portrait.

Requires Pillow and NumPy only; the alpha matte and backgrounds are versioned.
Run from any cwd: python vivi-oor/scripts/compose.py
"""
from pathlib import Path
import hashlib
import json
import zipfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, PngImagePlugin

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parent
SIZE = (1080, 1920)
LANCZOS = Image.Resampling.LANCZOS
# Interior face rectangle in the original 720x1280 photo.
FACE_BOX = (235, 380, 420, 580)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size, display=False):
    name = 'PlayfairDisplay.ttf' if display else 'Montserrat.ttf'
    loaded = ImageFont.truetype(str(ROOT / 'dsky-quotes/assets/fonts' / name), size)
    loaded.set_variation_by_axes([400 if display else 500])
    return loaded


def contact_sheet(scenes):
    """Labels are outside the thumbnails. Individual PNGs have NO text."""
    margin, gap, tw, th = 42, 20, 324, 576
    header, label_h, row_gap, footer = 174, 44, 24, 76
    width = margin * 2 + tw * 5 + gap * 4
    height = header + 2 * (th + label_h) + row_gap + footer
    sheet = Image.new('RGB', (width, height), '#20191f')
    d = ImageDraw.Draw(sheet)
    d.text((margin, 28), 'VIVI OOR', font=font(62, True), fill='#f7eddf')
    right = 'DAÏSKY / SÉRIE VISUELLE'
    rf = font(18)
    d.text((width-margin-d.textlength(right,font=rf), 52), right, font=rf, fill='#d1ac77')
    d.text((margin, 108), '10 décors · 1 portrait d’origine · 1080 × 1920 · sans texte',
           font=font(22), fill='#c8bfc3')
    d.line((margin, 149, width-margin, 149), fill='#59444a', width=1)
    labels = ['Invitation dorée', 'Le goût du miel', 'Les étincelles', 'Reste avec moi',
              'Chaque instant', 'Le cœur ouvert', 'Notre trésor', 'Le festin',
              'Jusqu’au matin', 'L’aube douce']
    for index, scene in enumerate(scenes):
        x = margin + (index % 5) * (tw + gap)
        y = header + (index // 5) * (th + label_h + row_gap)
        with Image.open(PROJECT / scene['output']) as im:
            thumb = im.convert('RGB').resize((tw, th), LANCZOS)
        sheet.paste(thumb, (x, y))
        d.text((x, y + th + 12), f'{index+1:02d}  {labels[index]}', font=font(18), fill='#eee3d7')
    d.text((margin, height-45), 'Portrait photographique conservé · Décors générés par IA',
           font=font(18), fill='#b6a8ad')
    path = PROJECT / 'VIVI_OOR_apercu_10_images.jpg'
    sheet.save(path, quality=93, subsampling=0)
    return path


def main():
    manifest = json.loads((PROJECT / 'manifest.json').read_text())
    scenes = manifest['scenes']
    assert len(scenes) == 10, 'Exactly ten final variants are permitted.'
    assert len({s['output'] for s in scenes}) == 10
    assert all(s['reference_image'] == manifest['source'] for s in scenes)
    source_path = ROOT / manifest['source']
    assert sha256(source_path) == manifest['source_sha256'], 'The original source changed.'
    source = ImageOps.exif_transpose(Image.open(source_path)).convert('RGB')
    assert source.size == (720,1280)
    source = source.resize(SIZE, LANCZOS)
    alpha = Image.open(PROJECT / manifest['alpha']).convert('L')
    assert alpha.size == (720,1280)
    assert np.max(np.asarray(alpha)[165:245,525:684]) == 0, 'Snapchat stickers must be fully removed.'
    alpha = alpha.resize(SIZE, LANCZOS)
    # Keep interpolation ringing from creating almost-transparent stray pixels.
    av = np.asarray(alpha).copy()
    av[av <= 2] = 0
    av[av >= 253] = 255
    alpha = Image.fromarray(av)
    opaque = av == 255
    original_pixels = np.asarray(source)
    left, top, right, bottom = [round(v * 1.5) for v in FACE_BOX]
    assert np.all(av[top:bottom, left:right] == 255), 'Face interior must be fully opaque.'
    report = dict(
        source=manifest['source'], source_sha256=sha256(source_path),
        original_unchanged=True, snapchat_stickers_removed_from_mask=True,
        generated_background_count=len(scenes), final_image_count=10,
        size=list(SIZE), format='PNG RGB', text_in_individual_images=False,
        face_core_box_at_delivery_size=[left,top,right,bottom],
        method='Original RGB, uniform Lanczos resize 1.5x, shared alpha matte; no AI face, body or clothing generation.',
        boundary_note='Only the 1–3 pixel feathered silhouette is blended with the new environment. All fully opaque subject pixels are identical to the uniformly resized source.',
        background_processing='Center-fit without distortion to 9:16, Gaussian blur 1.8 px for portrait depth of field. No global grade over the original portrait.',
        files=[],
    )
    for scene in scenes:
        bg_path = PROJECT / scene['background']
        with Image.open(bg_path) as raw:
            bg_size = raw.size
            background = ImageOps.fit(raw.convert('RGB'), SIZE, method=LANCZOS,
                                      centering=(0.5,0.5))
        background = background.filter(ImageFilter.GaussianBlur(1.8))
        result = Image.composite(source, background, alpha)
        path = PROJECT / scene['output']
        path.parent.mkdir(parents=True, exist_ok=True)
        meta = PngImagePlugin.PngInfo()
        meta.add_text('Title', f"Vivi OOR - {scene['title']}")
        meta.add_text('Description', 'AI-generated environment composited with the unchanged photographic portrait. No AI-generated face.')
        result.save(path, pnginfo=meta, compress_level=6)
        with Image.open(path) as verify:
            assert verify.size == SIZE and verify.mode == 'RGB'
            pixels = np.asarray(verify)
            assert np.array_equal(pixels[opaque], original_pixels[opaque]), path.name
            assert np.array_equal(pixels[top:bottom,left:right],
                                  original_pixels[top:bottom,left:right]), path.name
        report['files'].append(dict(
            file=scene['output'], sha256=sha256(path), bytes=path.stat().st_size,
            background_size=list(bg_size),
            background_sha256=sha256(bg_path),
            opaque_portrait_max_pixel_error=0, face_core_max_pixel_error=0,
        ))
        print(f"OK {path.name}: 1080x1920 / portrait pixel error = 0 / {path.stat().st_size / 1024**2:.2f} MiB")
    expected = {Path(s['output']).name for s in scenes}
    actual = {p.name for p in (PROJECT / 'livrables').iterdir() if p.is_file()}
    assert actual == expected, 'The delivery directory must contain exactly the ten PNGs.'
    assert len({r['sha256'] for r in report['files']}) == 10, 'No duplicate final images.'
    contact_sheet(scenes)
    (PROJECT / 'controle_qualite.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    # Exactly the ten PNGs in the artist's download: no raw plates or proof sheets.
    archive_path = PROJECT / 'VIVI_OOR_10_images_9x16.zip'
    with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_STORED) as archive:
        for scene in scenes:
            p = PROJECT / scene['output']
            info = zipfile.ZipInfo(p.name, date_time=(2026,9,26,0,0,0))
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            archive.writestr(info, p.read_bytes())
    with zipfile.ZipFile(archive_path) as archive:
        assert len(archive.namelist()) == 10
        assert set(archive.namelist()) == expected
        assert archive.testzip() is None
    print(f'Archive verified: exactly 10 PNGs, {archive_path.stat().st_size / 1024**2:.2f} MiB')


if __name__ == '__main__':
    main()
