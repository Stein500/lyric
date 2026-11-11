#!/usr/bin/env python3
"""lettering.py — cuit les paroles dans chaque plan (v6.4 §4, 4 correctifs mesurés v6.3).

Entrée  : fonds/plan-XX.png 768x1376 (générateur, NO TEXT AT ALL)
Sortie  : fonds/baked-XX.png 1080x1920 (ancré en HAUT, rognage du bas) avec lettrage cuit :
          - contour par DILATATION du masque du glyphe (jamais stroke_width)
          - une tuile par glyphe à la taille de son encre, interlettrage 0.055*taille, rotation ±1.0°
          - halo = ombre serrée (flou7 60% + flou17 34% + 150 mouchetures masquées autour des glyphes)
          - bloc centré x 211->831 (largeur 620 <= 740), bande y 640->1080 ; dy par plan (typo_offsets.json)
          - palette N&B : ligne 1 blanc pur #FFFFFF, ligne 2 gris-argent #C9D2DC,
            voile d'encre sous le bloc, coulures SOUS le bloc jamais sur les lettres.
Génère aussi livrables/CONTROLE-paroles.jpg (blocs 1:1 de tous les plans cuits).
"""
import json, os, random, zlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
SERIF = os.path.join(ROOT, "fonts", "PlayfairDisplay.ttf")
W, H = 1080, 1920
S = 1080 / 768.0
BOX_X0, BOX_X1 = 211, 831
BOX_Y0, BOX_Y1 = 640, 1080

def font(size, weight=800):
    f = ImageFont.truetype(SERIF, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f

def glyph_mask(ch, f):
    tmp = Image.new("L", (int(f.size * 2.4), int(f.size * 2.4)), 0)
    d = ImageDraw.Draw(tmp)
    d.text((f.size * 0.7, f.size * 0.7), ch, font=f, fill=255)
    bbox = tmp.getbbox()
    return tmp.crop(bbox)

def draw_line(target, line, cx, cy, size, fill, seed):
    f = font(size, 800)
    spacing = 0.085 * size
    rng = random.Random(seed)
    tiles = []
    total = 0.0
    for ch in line:
        if ch == " ":
            tiles.append((" ", None, spacing * 1.7)); total += spacing * 1.7; continue
        m = glyph_mask(ch, f)
        w = m.width + spacing
        tiles.append((ch, m, w)); total += w
    total -= spacing
    x = cx - total / 2
    ow = max(2, size // 10)
    for ch, m, w in tiles:
        if ch != " ":
            rot = rng.uniform(-1.0, 1.0)
            tile = Image.new("L", (m.width + 2 * ow, m.height + 2 * ow), 0)
            tile.paste(m, (ow, ow))
            contour = tile.filter(ImageFilter.MaxFilter(2 * ow + 1))  # dilatation
            black = Image.new("RGBA", tile.size, (5, 6, 8, 255))
            layer = Image.new("RGBA", tile.size, (0, 0, 0, 0))
            layer.paste(black, (0, 0), contour)
            g = m.rotate(rot, resample=Image.BICUBIC, expand=True)
            col = Image.new("RGBA", g.size, fill + (255,))
            layer.paste(col, (ow + (tile.width - 2 * ow - g.width) // 2,
                              ow + (tile.height - 2 * ow - g.height) // 2), g)
            layer = layer.rotate(rot, resample=Image.BICUBIC, expand=True)
            target.alpha_composite(layer, (int(x - ow), int(cy - tile.height / 2 - ow)))
        x += w

def bake(plan_path, lignes, out_path, dy=0, seed=0):
    im = Image.open(plan_path).convert("L").convert("RGB")  # N&B strict garanti (recette 8.1)
    im = im.resize((W, int(round(im.height * S))), Image.LANCZOS).crop((0, 0, W, H))
    rgba = im.convert("RGBA")
    n = len(lignes)
    size = 46 if n <= 2 else (40 if n == 3 else 34)
    # auto-fit : rétrécit tant que la ligne la plus large dépasse la boîte (620 px)
    def max_line_w(sz):
        f = font(sz, 800); sp = 0.085 * sz; spw = 0.55 * sz
        mx = 0.0
        for line in lignes:
            w = sum((spw if c == " " else glyph_mask(c, f).width + sp) for c in line) - sp
            mx = max(mx, w)
        return mx
    while max_line_w(size) > (BOX_X1 - BOX_X0) - 64 and size > 22:  # marge contour+rotation
        size -= 2
    line_h = int(size * 1.28)
    block_h = line_h * n
    cx = (BOX_X0 + BOX_X1) // 2
    cy0 = (BOX_Y0 + BOX_Y1) // 2 - block_h // 2 + line_h // 2 + dy
    # voile d'encre + halo serré
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pad = 26
    d.rounded_rectangle([BOX_X0 - pad, cy0 - block_h // 2 - pad, BOX_X1 + pad, cy0 + block_h // 2 + pad],
                        radius=30, fill=(4, 5, 7, 235))
    halo = layer.filter(ImageFilter.GaussianBlur(7)).point(lambda a: int(a * 0.60))
    halo2 = layer.filter(ImageFilter.GaussianBlur(17)).point(lambda a: int(a * 0.34))
    out = Image.alpha_composite(rgba, halo2)
    out = Image.alpha_composite(out, halo)
    # mouchetures masquées autour des glyphes
    rng = random.Random(seed)
    dots = Image.new("L", (W, H), 0)
    dd = ImageDraw.Draw(dots)
    for _ in range(150):
        x = rng.randint(BOX_X0 - 40, BOX_X1 + 40)
        y = rng.randint(cy0 - block_h // 2 - 40, cy0 + block_h // 2 + 40)
        r = rng.randint(1, 3)
        dd.ellipse([x, y, x + r, y + r], fill=rng.randint(60, 140))
    mask = dots.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2))
    ink = Image.new("RGBA", (W, H), (4, 5, 7, 255))
    out = Image.composite(Image.alpha_composite(out, ink), out, mask)
    # lettrage
    for li, line in enumerate(lignes):
        fill = (255, 255, 255) if li == 0 else (201, 210, 220)
        draw_line(out, line.upper(), cx, int(cy0 + li * line_h), size, fill, seed + li * 131 + int(cy0))
    # coulures sous le bloc
    d2 = ImageDraw.Draw(out)
    for _ in range(6):
        x = rng.randint(BOX_X0 + 20, BOX_X1 - 20)
        y = cy0 + block_h // 2 + 6
        ln = rng.randint(18, 60)
        d2.line([(x, y), (x + rng.randint(-4, 4), y + ln)], fill=(10, 11, 13, 200), width=rng.randint(2, 4))
    out.convert("RGB").save(out_path)

def main():
    mp = json.load(open(os.path.join(ROOT, "verses_map.json"), encoding="utf-8"))
    plans = {}
    for v in mp["verses"]:
        plans[v["image"]] = v
    offsets = {}
    off_path = os.path.join(ROOT, "typo_offsets.json")
    if os.path.exists(off_path):
        offsets = json.load(open(off_path))
    done = []
    for img, v in sorted(plans.items()):
        src = os.path.join(ROOT, img)
        if not os.path.exists(src):
            print("MANQUANT:", img); continue
        base = os.path.basename(img).replace(".png", "")
        out = os.path.join(ROOT, "fonds", f"baked-{base}.png")
        seed = zlib.crc32("|".join(v["lignes"]).encode())
        bake(src, v["lignes"], out, dy=offsets.get(base, 0), seed=seed)
        done.append((v["i"], out))
        print("cuit:", base, "<- vers", v["i"])
    # planche CONTROLE-paroles.jpg : blocs 1:1
    tiles = []
    for i, out in done:
        im = Image.open(out)
        tiles.append((f"v{i:02d}", im.crop((BOX_X0 - 40, BOX_Y0 - 40, BOX_X1 + 40, BOX_Y1 + 40))))
    cols, tw = 4, 720
    rows = (len(tiles) + cols - 1) // cols
    th = int((BOX_Y1 - BOX_Y0 + 80) * tw / (BOX_X1 - BOX_X0 + 80))
    sheet = Image.new("RGB", (cols * tw, rows * (th + 22)), (20, 20, 24))
    d = ImageDraw.Draw(sheet)
    for idx, (name, crop) in enumerate(tiles):
        crop = crop.resize((tw, th), Image.LANCZOS)
        x = (idx % cols) * tw; y = (idx // cols) * (th + 22)
        sheet.paste(crop, (x, y + 20)); d.text((x + 4, y + 4), name, fill=(255, 232, 168))
    sheet.save(os.path.join(ROOT, "livrables", "CONTROLE-paroles.jpg"), quality=90)
    print("CONTROLE-paroles.jpg:", len(tiles), "blocs")

if __name__ == "__main__":
    main()
