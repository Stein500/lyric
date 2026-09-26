#!/usr/bin/env python3
"""Show the existing ten AI edits without remote URLs or relative image assets.

Creates a self-contained HTML gallery and a ten-page PDF. Does not regenerate,
retouch or overwrite the delivered PNGs. Dependencies: Pillow, pypdf.
"""
from pathlib import Path
from io import BytesIO
import base64
import hashlib
import html
import json

from PIL import Image
from pypdf import PdfReader

PROJECT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((PROJECT / 'manifest.json').read_text())
    report = json.loads((PROJECT / 'controle_qualite.json').read_text())
    assert len(manifest['scenes']) == len(report['files']) == 10
    hashes = {entry['file']: entry['sha256'] for entry in report['files']}
    pages, cards = [], []
    for scene in manifest['scenes']:
        path = PROJECT / scene['output']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == hashes[scene['output']]
        with Image.open(path) as file:
            image = file.convert('RGB')
        assert image.size == (1080, 1920)
        pages.append(image)
        preview = image.resize((768, 1365), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        preview.save(buffer, 'JPEG', quality=94, subsampling=0)
        encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
        title = html.escape(scene['title'])
        number = scene['slot']
        cards.append(f'<figure id="image-{number:02d}"><figcaption><b>{number:02d} / 10</b><span>{title}</span></figcaption><img src="data:image/jpeg;base64,{encoded}" width="768" height="1365" alt="Vivi OOR : image {number}, {title}, retouche IA" loading="lazy" decoding="async"></figure>')
    pdf = PROJECT / 'VIVI_OOR_10_images_a_feuilleter.pdf'
    pages[0].save(pdf, 'PDF', save_all=True, append_images=pages[1:],
                  resolution=144.0, quality=96, subsampling=0,
                  title='Vivi OOR — Les 10 retouches IA', author='Daïsky',
                  subject='10 portraits retouchés avec IA à partir de la même photo de référence. Une image par page.',
                  creator='Vivi OOR — présentation locale')
    reader = PdfReader(pdf)
    assert len(reader.pages) == 10
    assert all(abs(float(p.mediabox.width) / float(p.mediabox.height) - 9/16) < 0.0001 for p in reader.pages)
    document = '''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vivi OOR — les 10 images directement ici</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f2ebe4;color:#31252b;font-family:system-ui,-apple-system,sans-serif}main{max-width:1250px;margin:auto;padding:32px 24px 48px}header{padding-bottom:26px;margin-bottom:24px;border-bottom:1px solid #d6c6ba}.eyebrow{color:#8d583e;font-size:11px;letter-spacing:.2em;font-weight:700}h1{font:normal clamp(48px,7vw,80px)/1 Georgia,serif;letter-spacing:-.04em;margin:15px 0}p{color:#725e65;font-size:14px;line-height:1.6;max-width:690px;margin:0}.gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:30px 24px}figure{margin:0;min-width:0}figcaption{display:flex;align-items:baseline;gap:12px;padding:0 0 11px;font-size:14px}figcaption b{font-size:11px;letter-spacing:.06em;color:#8d583e;white-space:nowrap}img{display:block;width:100%;height:auto;border-radius:4px;background:#d8cac0}footer{border-top:1px solid #d6c6ba;margin-top:35px;padding-top:22px;color:#725e65;font-size:12px;line-height:1.6}@media(max-width:720px){main{padding:25px 14px 35px}.gallery{grid-template-columns:1fr;gap:30px}figcaption{font-size:14px}}
</style></head><body><main><header><div class="eyebrow">DAÏSKY · FINITION IA</div><h1>Vivi OOR</h1><p><strong>Les 10 images, directement ici.</strong><br>Fais défiler pour les voir séparément. Les photos sont intégrées à ce document : aucun lien externe ni serveur à ouvrir.</p></header><section class="gallery" aria-label="Les dix retouches IA">'''
    document += '\n'.join(cards)
    document += '''</section><footer>Une seule photo de référence · Dix ambiances · 9:16 · Aucun texte dans les images.<br>Ce sont les retouches IA de la version 02 ; les PNG livrés et la photo d’origine restent inchangés. Les numéros et légendes appartiennent uniquement à cette présentation.</footer></main></body></html>'''
    gallery = PROJECT / 'VIVI_OOR_10_images_directement_ici.html'
    gallery.write_text(document)
    assert document.count('src="data:image/jpeg;base64,') == 10
    assert 'http://' not in document and 'https://' not in document
    # Recheck: no image has been modified by presentation packaging.
    for file, checksum in hashes.items():
        assert hashlib.sha256((PROJECT / file).read_bytes()).hexdigest() == checksum
    print(f'PDF: 10 pages, {pdf.stat().st_size/1e6:.2f} MB')
    print(f'HTML: 10 embedded images, no external resources, {gallery.stat().st_size/1e6:.2f} MB')


if __name__ == '__main__':
    main()
