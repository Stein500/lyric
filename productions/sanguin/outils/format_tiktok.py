#!/usr/bin/env python3
"""Generate draft TikTok frames without cropping lyrics or source artwork."""
from pathlib import Path
from PIL import Image, ImageOps

root = Path(__file__).resolve().parent.parent
out = root / 'portrait-1080x1920'
out.mkdir(exist_ok=True)
for path in sorted((root / 'fonds').glob('scene-*.png')):
    with Image.open(path) as source:
        img = ImageOps.contain(source.convert('RGB'), (1080, 1920), Image.Resampling.LANCZOS)
        frame = Image.new('RGB', (1080, 1920), 'black')
        frame.paste(img, ((1080 - img.width) // 2, (1920 - img.height) // 2))
        frame.save(out / (path.stem + '.jpg'), quality=95, subsampling=0)
        print(f'{path.name}: {source.size} -> {img.size} in 1080x1920')
