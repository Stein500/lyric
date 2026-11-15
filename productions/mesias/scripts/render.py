# -*- coding: utf-8 -*-
"""Moteur de composition MESÍAS — image vivante, traduction peinte, espagnol défilant.

Rend :
  - image de base 1080x1920 par plan (recadrage ancré en haut + fond flou)
  - lettrage moteur : traduction FR cuite dans l'image, contour par dilatation
  - bandeau espagnol défilant (4 lignes, > 1 s d'avance)
  - prévisualisation PNG (plan + lettrage + HUD)

Aucune police du générateur : le générateur reçoit « NO TEXT AT ALL ».
"""
import json, os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "work", "frames_base")
FONT_PATH = os.path.join(ASSETS, "fonts", "BebasNeue-Regular.ttf")

W, H = 1080, 1920
SRC_W, SRC_H = 768, 1376

# --- zones de sécurité TikTok (prompt v7 §4) ---
TOP_SAFE = 144
BOTTOM_SAFE = 1574
RIGHT_FORBID_X = 910
TEXT_MAX_W = 740
TEXT_TOP, TEXT_BOT = 620, 1340
PILL = (186, 1444, 894, 1556)  # x0,y0,x1,y1
PILL_MAX_W = 620
SPAN_W = 620                  # largeur utile du bandeau espagnol
SPAN_Y0, SPAN_Y1 = 1252, 1452  # 3 lignes, bas < 1574 (zone UI TikTok)

CREAM = (246, 240, 228)
AMBER = (232, 163, 61)
INDIGO = (10, 14, 30)


# ---------------------------------------------------------------- recadrage
def base_image(path):
    """1080x1920 : ancrage en haut, le bas complété par une version floutée."""
    im = Image.open(path).convert("RGB")
    if im.size != (SRC_W, SRC_H):
        im = im.resize((SRC_W, SRC_H), Image.LANCZOS)
    scale = W / SRC_W                       # 1.40625
    nw, nh = W, int(round(SRC_H * scale))   # 1080 x 1935
    big = im.resize((nw, nh), Image.LANCZOS)
    bg = big.crop((0, nh - H, W, nh))       # 1080x1920 depuis le bas
    bg = bg.filter(ImageFilter.GaussianBlur(48))
    # assombrit légèrement le fond pour que la typo reste lisible
    dark = Image.new("RGB", bg.size, INDIGO)
    bg = Image.blend(bg, dark, 0.35)
    canvas = Image.new("RGB", (W, H))
    canvas.paste(bg, (0, 0))
    canvas.paste(big.crop((0, 0, W, H)), (0, 0))  # ancrage en haut
    return canvas


# ---------------------------------------------------------------- typographie
def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def _split_cost(words, fnt, draw, L, maxw):
    """Meilleure répartition de `words` en L lignes contiguës : minimise la largeur max.
    Renvoie (liste_de_lignes, largeur_max) ou (None, inf) si impossible."""
    n = len(words)
    INF = float("inf")
    width = lambda i, j: draw.textlength(" ".join(words[i:j]), font=fnt)
    best = [[INF] * (L + 1) for _ in range(n + 1)]
    cut = [[0] * (L + 1) for _ in range(n + 1)]
    best[0][0] = 0
    for j in range(1, L + 1):
        for i in range(1, n + 1):
            for k in range(j - 1, i):
                if best[k][j - 1] == INF:
                    continue
                w = width(k, i)
                if w > maxw:
                    continue
                c = max(best[k][j - 1], w)
                if c < best[i][j]:
                    best[i][j] = c
                    cut[i][j] = k
    if best[n][L] == INF:
        return None, INF
    lines, i, j = [], n, L
    while j > 0:
        k = cut[i][j]
        lines.append(" ".join(words[k:i]))
        i, j = k, j - 1
    return list(reversed(lines)), best[n][L]


def wrap_balanced(draw, text, fnt, maxw, maxlines):
    """Découpe équilibrée : évite les lignes orphelines (« Roi » seul)."""
    words = text.split(" ")
    for L in range(1, maxlines + 1):
        lines, wmax = _split_cost(words, fnt, draw, L, maxw)
        if lines:
            return lines
    return [text]


def fit_block(draw, text, maxw, maxlines, size_max=104, size_min=46, leading=0.94):
    """Taille la plus grande tenant en <= maxlines lignes équilibrées."""
    for size in range(size_max, size_min - 1, -2):
        f = font(size)
        ls = wrap_balanced(draw, text, f, maxw, maxlines)
        if len(ls) <= maxlines:
            return f, ls, int(size * leading * 1.18)
    f = font(size_min)
    return f, wrap_balanced(draw, text, f, maxw, maxlines), int(size_min * leading * 1.18)


def bake_text(img, text, maxw=TEXT_MAX_W, maxlines=3, top=None,
              color=CREAM, outline=6, glow=True, anchor="bottom", bottom_limit=1180,
              scrim=True):
    """Peint le texte dans l'image (durée permanente), contour par dilatation."""
    d = ImageDraw.Draw(img)
    f, lines, lh = fit_block(d, text, maxw, maxlines)
    block_h = lh * (len(lines) - 1) + int(f.size * 1.02)
    if top is None:
        if anchor == "bottom":
            top = bottom_limit - block_h
        else:
            top = TEXT_TOP + (TEXT_BOT - TEXT_TOP - block_h) // 2
    top = max(top, TOP_SAFE)
    if top + block_h > BOTTOM_SAFE:
        top = BOTTOM_SAFE - block_h

    # masque des glyphes -> dilatation -> contour (jamais de remplissage des contre-formes)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    for i, ln in enumerate(lines):
        y = top + i * lh
        x = (W - d.textlength(ln, font=f)) / 2
        md.text((x, y), ln, font=f, fill=255)

    # voile doux DERRIÈRE les mots (jamais sur les glyphes) : lisibilité sur fonds chargés
    if scrim:
        top_s, bot_s = max(0, top - 46), min(H, top + block_h + 46)
        lay = Image.new("RGB", (W, bot_s - top_s), (8, 10, 20))
        grad = Image.new("L", (1, bot_s - top_s))
        for i in range(bot_s - top_s):
            y = top_s + i
            a = 78
            if y < top:
                a = int(78 * max(0.0, (y - (top - 46)) / 46.0))
            elif y > top + block_h:
                a = int(78 * max(0.0, 1 - (y - (top + block_h)) / 46.0))
            grad.putpixel((0, i), max(0, min(255, a)))
        img.paste(lay, (0, top_s), grad.resize((W, bot_s - top_s)))

    if glow:
        halo = mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(18))
        shadow = Image.new("RGB", (W, H), INDIGO)
        img.paste(shadow, (0, 0), halo.point(lambda v: int(v * 0.62)))
    ring = mask.filter(ImageFilter.MaxFilter(outline * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2))
    ring = ring.point(lambda v: 255 if v > 30 else 0)
    edge = Image.new("RGB", (W, H), (12, 16, 34))
    img.paste(edge, (0, 0), ring)

    layer = Image.new("RGB", (W, H), color)
    img.paste(layer, (0, 0), mask)
    return {"top": top, "bottom": top + block_h, "size": f.size, "lines": lines}


# ---------------------------------------------------------------- bandeau espagnol
def scrim(img, y0, y1, strength=104, feather=90):
    """Voile sombre DERRIÈRE le bandeau (jamais sur les glyphes), pour un contraste stable.

    Correctif lisibilité v3 : la rampe verticale était tracée à la main puis étirée,
    ce qui laissait une ARÊTE horizontale visible aux deux extrémités (on voyait la
    ligne où le voile s'arrêtait). Elle est désormais calculée par une courbe en
    smoothstep, donc l'alpha arrive à zéro avec une pente nulle : plus de bord.
    """
    top, bot = max(0, y0 - feather), min(H, y1 + feather // 2)
    h = bot - top
    grad = Image.new("L", (1, h))
    for i in range(h):
        y = top + i
        if y < y0:
            t = (y - (y0 - feather)) / float(feather)
        elif y > y1:
            t = 1.0 - (y - y1) / float(feather // 2)
        else:
            t = 1.0
        t = max(0.0, min(1.0, t))
        smooth = t * t * (3 - 2 * t)          # pente nulle aux extrémités
        grad.putpixel((0, i), max(0, min(255, int(strength * smooth))))
    grad = grad.resize((W, h))
    lay = Image.new("RGB", (W, h), (8, 10, 20))
    img.paste(lay, (0, top), grad)


def span_band(img, lines4, y0=SPAN_Y0):
    """Trois lignes espagnoles défilantes. La ligne du bas est la plus récente."""
    d = ImageDraw.Draw(img)
    alpha_steps = [(0.55, 42), (0.74, 48), (1.00, 56)]
    scrim(img, y0 - 34, y0 + 236)
    y = y0
    for k, ln in enumerate(lines4):          # k=0 ligne la plus ancienne (haut)
        a, size = alpha_steps[k]
        ff = font(size)
        while d.textlength(ln, font=ff) > 700 and size > 30:
            size -= 2
            ff = font(size)
        x = (W - d.textlength(ln, font=ff)) / 2
        if x + d.textlength(ln, font=ff) > RIGHT_FORBID_X - 20:
            x = RIGHT_FORBID_X - 20 - d.textlength(ln, font=ff)
        x = max(24, x)
        # lueur + texte
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).text((x, y), ln, font=ff, fill=255)
        halo = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(7))
        sh = Image.new("RGB", (W, H), (6, 8, 18))
        img.paste(sh, (0, 0), halo.point(lambda v: int(v * (0.45 * a + 0.2))))
        lay = Image.new("RGB", (W, H), (250, 246, 236))
        img.paste(lay, (0, 0), mask.point(lambda v: int(v * a)))
        y += 72
    return y


# ---------------------------------------------------------------- HUD / preview
def load_map():
    return json.load(open(os.path.join(ROOT, "data", "verses_map.json"), encoding="utf8"))


def lines_until(verses, t, n=3):
    """Les n derniers vers dont le début <= t, dans l'ordre chronologique."""
    seen = [v for v in verses if v["debut_source"] <= t]
    out, ids = [], set()
    for v in reversed(seen):
        if v["texte_source"] in ids:
            continue
        ids.add(v["texte_source"])
        out.append(v["texte_source"])
        if len(out) == n:
            break
    return list(reversed(out))


def preview(image_name, vers_index, out_path, show_hud=True):
    m = load_map()
    v = m["verses"][vers_index]
    base = os.path.join(ROOT, "work", "base", image_name)
    if not os.path.exists(base):
        base = base_image(os.path.join(ASSETS, image_name))
    else:
        base = Image.open(base).convert("RGB")
    img = base.copy()
    info = bake_text(img, v["traduction_fr"])
    span_band(img, lines_until(m["verses"], v["debut_source"]))
    if show_hud:
        hud(img, m, v)
    img.save(out_path)
    return info


def hud(img, m, v):
    # badge artiste <-> WTBW (ombre portée pour rester lisible sur ciel clair)
    mk = Image.new("L", (W, 200), 0)
    dm = ImageDraw.Draw(mk)
    dm.text((46, 46), m["artiste"].upper(), font=font(44), fill=255)
    dm.text((46, 100), "WTBW", font=font(34), fill=255)
    sh = mk.filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * 0.85))
    img.paste(Image.new("RGB", (W, 200), (6, 8, 18)), (0, 0), sh)
    d = ImageDraw.Draw(img)
    d.text((46, 46), m["artiste"].upper(), font=font(44), fill=(240, 236, 226))
    d.text((46, 100), "WTBW", font=font(34), fill=AMBER)
    # filet de progression
    t0, t1 = 16.84, 737.22
    p = max(0.0, min(1.0, (v["debut_source"] - t0) / (t1 - t0)))
    x0, x1, y = 170, RIGHT_FORBID_X, 186
    d.line([(x0, y), (x1, y)], fill=(96, 102, 120), width=2)
    d.line([(x0, y), (x0 + (x1 - x0) * p, y)], fill=AMBER, width=5)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(ROOT, "work", "base"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "work", "preview"), exist_ok=True)
    for f in sorted(os.listdir(ASSETS)):
        if f.startswith(("plan_", "ancre_")) and f.endswith(".png"):
            dst = os.path.join(ROOT, "work", "base", f)
            if not os.path.exists(dst):
                base_image(os.path.join(ASSETS, f)).save(dst)
    # planches de contrôle
    for idx in (11, 12, 44, 60, 92):
        preview("plan_04.png", idx - 1, os.path.join(ROOT, "work", "preview", f"p{idx:03d}.png"))
    print("ok")
