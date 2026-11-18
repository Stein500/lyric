#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lettrage MOTEUR (v7.0 §6 B) — cuit le vers exact dans l'image, avant montage.

- le generateur a recu NO TEXT AT ALL : aucune parole deja peinte par le modele
- contour par DILATATION DU MASQUE place DERRIERE les glyphes (pas de remplissage
  des contre-formes), halo serre, glyphes espaces et tournes individuellement
- largeur <= 526 px, bande y 441 -> 953 en natif 768x1376 (§4), sous la limite
  visage 398, jamais sur le visage, aucun voile/plaque sur les mots
"""
import json, math, os, random, sys
import outils  # amorce Pillow (hors Git, réinstallé si purgé)
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CONTRACT = json.load(open(os.path.join(HERE, "verses_map.json"), encoding="utf-8"))
OUT_DIR = os.path.join(HERE, "assets", "cuits")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 768, 1376
MAX_W = 500                  # marge de securite sous les 526 px du §4
BAND_TOP, BAND_BOTTOM = 441, 953
SPACING = 2
# Apostrophes, points, virgules et guillemets restent SOLIDAIRES du mot :
# aucun espacement ajoute autour d'eux, aucune rotation (counter-formes intactes).
TIGHT = set("'’.,\"…")

FONT_CANDIDATES = [
    os.path.join(ROOT, "dsky-quotes", "assets", "fonts", "Montserrat-Bold.ttf"),
    os.path.join(ROOT, "dsky-quotes", "assets", "fonts", "Montserrat-ExtraBold.ttf"),
    os.path.join(ROOT, "dsky-quotes", "assets", "fonts", "Montserrat-SemiBold.ttf"),
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_PATH = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)
if FONT_PATH is None:
    raise SystemExit("aucune police TrueType trouvee")


def measure(s, font):
    return sum(math.ceil(font.getlength(ch)) + 8 + SPACING for ch in s) - SPACING


def wrap(text, font):
    """Découpe en lignes équilibrées (DP : minimise la largeur maximale).

    Évite les lignes orphelines tout en gardant chaque mot exact et l'ordre
    des mots ; aucun mot n'est coupé, aucun retour à la ligne n'invente de texte.
    """
    words = text.split(" ")
    n = len(words)
    widths = [[measure(" ".join(words[i:j + 1]), font) for j in range(n)] for i in range(n)]
    INF = float("inf")
    for L in range(1, min(n, 6) + 1):
        dp = [[INF] * (n + 1) for _ in range(L + 1)]
        parent = [[None] * (n + 1) for _ in range(L + 1)]
        dp[0][0] = 0
        for k in range(1, L + 1):
            for j in range(1, n + 1):
                for i in range(k - 1, j):
                    w = widths[i][j - 1]
                    if dp[k - 1][i] < INF and w <= MAX_W:
                        val = max(dp[k - 1][i], w)
                        if val < dp[k][j]:
                            dp[k][j], parent[k][j] = val, i
        if dp[L][n] < INF:
            lines, j = [], n
            for k in range(L, 0, -1):
                i = parent[k][j]
                lines.append(" ".join(words[i:j]))
                j = i
            lines.reverse()
            return lines
    return [text]


def choose(text):
    for size in range(64, 32, -2):
        font = ImageFont.truetype(FONT_PATH, size)
        lines = wrap(text, font)
        lh = int(font.size * 2.4)
        if all(measure(l, font) <= MAX_W for l in lines) and len(lines) * lh <= BAND_BOTTOM - BAND_TOP:
            return font, lines, size
    return font, lines, size


def render_line(line, font, rng):
    ascent, descent = font.getmetrics()
    pad = 4
    tile_h = ascent + descent + 2 * pad + 20
    baseline = ascent + pad + 12
    tiles = []
    for ch in line:
        tight = ch in TIGHT
        p = 1 if tight else pad
        cw = math.ceil(font.getlength(ch)) + 2 * p
        tile = Image.new("RGBA", (cw, tile_h), (0, 0, 0, 0))
        ImageDraw.Draw(tile).text((p, baseline), ch, font=font,
                                 fill=(255, 255, 255, 255), anchor="ls")
        if not tight:
            tile = tile.rotate(rng.uniform(-1.5, 1.5), resample=Image.BICUBIC,
                               expand=False, fillcolor=(0, 0, 0, 0))
        tiles.append(tile)
    gaps = [0 if (line[j] in TIGHT or line[j + 1] in TIGHT) else SPACING
            for j in range(len(line) - 1)]
    total = sum(t.width for t in tiles) + sum(gaps)
    layer = Image.new("RGBA", (total, tile_h), (0, 0, 0, 0))
    x = 0
    for j, t in enumerate(tiles):
        layer.alpha_composite(t, (x, 0))
        x += t.width + (gaps[j] if j < len(gaps) else 0)
    return layer


def build_block(lines, font, rng):
    layers = [render_line(l, font, rng) for l in lines]
    lh = max(l.height for l in layers)
    bw = max(MAX_W, max(l.width for l in layers))
    block = Image.new("RGBA", (bw, lh * len(layers)), (0, 0, 0, 0))
    for k, l in enumerate(layers):
        block.alpha_composite(l, ((bw - l.width) // 2, k * lh))
    bb = block.getbbox()
    return block.crop(bb) if bb else block


def cook(entry):
    raw = os.path.join(HERE, entry["image"])
    out = os.path.join(HERE, entry["image_cuite"])
    texte = entry["texte_affiche"]
    font, lines, size = choose(texte)
    rng = random.Random(20261115 + entry["i"])
    block = build_block(lines, font, rng)
    px = (W - block.width) // 2
    py = BAND_TOP + (BAND_BOTTOM - BAND_TOP - block.height) // 2
    py = max(BAND_TOP, min(py, BAND_BOTTOM - block.height))
    alpha = block.getchannel("A")
    mask = Image.new("L", (W, H), 0)
    mask.paste(alpha, (px, py))
    dilated = mask.filter(ImageFilter.MaxFilter(7))       # contour derriere les glyphes
    halo = mask.filter(ImageFilter.GaussianBlur(2.5))     # halo serre
    base = Image.open(raw).convert("RGBA")
    halo_layer = Image.new("RGBA", (W, H), (8, 6, 24, 0))
    halo_layer.putalpha(halo.point(lambda a: int(a * 0.50)))
    res = Image.alpha_composite(base, halo_layer)
    outline = Image.new("RGBA", (W, H), (14, 10, 32, 0))
    outline.putalpha(dilated.point(lambda a: int(a * 0.98)))
    res = Image.alpha_composite(res, outline)
    glyphs = Image.new("RGBA", (W, H), (250, 244, 228, 0))
    glyphs.putalpha(mask)
    res = Image.alpha_composite(res, glyphs)
    res.convert("RGB").save(out, "JPEG", quality=96, subsampling=0, optimize=True)
    return {"i": entry["i"], "texte_affiche": texte, "source": entry["image"],
            "sortie": entry["image_cuite"], "police": os.path.basename(FONT_PATH),
            "corps": size, "lignes": lines, "bboite": [px, py, px + block.width, py + block.height],
            "largeur": block.width, "hauteur": block.height}


def main():
    report = []
    for e in CONTRACT["vers"]:
        if e["reprise"]:
            continue
        if os.path.exists(os.path.join(HERE, e["image"])):
            report.append(cook(e))

    with open(os.path.join(HERE, "lettering_report.json"), "w", encoding="utf-8") as fh:
        json.dump({"police": FONT_PATH, "largeur_max": MAX_W, "bande": [BAND_TOP, BAND_BOTTOM],
                   "encodage": "JPEG qualite 96, subsampling=0 (4:4:4), aucun sous-echantillonnage",
               "methode": "dilatation MaxFilter(7) derriere les glyphes + halo serre + rotation faible individuelle ; apostrophes/points/virgules solidaires (correctif 2026-11-15)",
                   "plans": report}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("police:", FONT_PATH)
    print("plans cuits:", len(report))
    print("largeurs:", min(r["largeur"] for r in report), "->", max(r["largeur"] for r in report), "px (max", MAX_W, ")")
    print("bandes y:", min(r["bboite"][1] for r in report), "->", max(r["bboite"][3] for r in report), "(cible", BAND_TOP, BAND_BOTTOM, ")")


if __name__ == "__main__":
    main()
