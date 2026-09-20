#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DSKY QUOTES — Moteur de composition
Génère, à partir d'un visuel IA (visage préservé) et d'une citation :
  - Post  1080x1350 (4:5)
  - Story 1080x1920 (9:16)  (statut WhatsApp / story IG)
Badge « DSKKY 🇧🇯 » (drapeau béninois dessiné), nom de l'auteur en bas.
"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(ROOT, "assets", "fonts")

# ------------------------------------------------------------------ styles
STYLES = {
    "LUXE":    {"accent": (201, 162, 39),  "text": (247, 242, 231), "scrim": (5, 5, 10)},
    "MINIMAL": {"accent": (168, 190, 224), "text": (247, 247, 242), "scrim": (14, 20, 38)},
    "AFRO":    {"accent": (232, 178, 58),  "text": (250, 247, 238), "scrim": (18, 34, 24)},
}
BENIN_GREEN  = (0, 135, 81)
BENIN_YELLOW = (252, 209, 22)
BENIN_RED    = (232, 17, 45)

def font(path, size, weight=None, italic=False):
    f = ImageFont.truetype(os.path.join(FONTS, path), size)
    if italic:
        f = ImageFont.truetype(os.path.join(FONTS, path.replace(".ttf", "-Italic.ttf")), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f

def playfair(size, weight=600, italic=False): return font("PlayfairDisplay.ttf", size, weight, italic)
def montserrat(size, weight=500, italic=False): return font("Montserrat.ttf", size, weight, italic)

EMOJI = re.compile(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]+")

def tracking_w(draw, text, f, tr):
    w = 0
    for ch in text:
        w += draw.textlength(ch, font=f) + tr
    return max(0, w - tr)

def draw_tracking(draw, xy, text, f, fill, tr=0, anchor_center_x=None, shadow=None):
    x, y = xy
    if anchor_center_x is not None:
        x = anchor_center_x - tracking_w(draw, text, f, tr) / 2
    for ch in text:
        if shadow:
            draw.text((x + 2, y + 2), ch, font=f, fill=shadow)
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tr
    return x

def wrap(draw, text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=f) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur); cur = word
    if cur: lines.append(cur)
    return lines

def fit_text(draw, text, max_w, max_h, mkfont, size0, size_min, lh=1.32):
    size = size0
    while size >= size_min:
        f = mkfont(size)
        lines = wrap(draw, text, f, max_w)
        if len(lines) * size * lh <= max_h:
            return f, lines, size * lh
        size -= 2
    f = mkfont(size_min)
    return f, wrap(draw, text, f, max_w), size_min * lh

# ------------------------------------------------------------------ elements
def draw_flag(draw, x, y, w, h):
    """Drapeau du Bénin : bande verte verticale + jaune/rouge horizontaux."""
    third = int(w / 3)
    draw.rectangle([x, y, x + third, y + h], fill=BENIN_GREEN)
    draw.rectangle([x + third, y, x + w, y + h // 2], fill=BENIN_YELLOW)
    draw.rectangle([x + third, y + h // 2, x + w, y + h], fill=BENIN_RED)

def draw_badge(img, x, y, accent, scale=1.0):
    """Pilule semi-transparente : drapeau + DSKY."""
    W, H = int(238 * scale), int(64 * scale)
    overlay = Image.new("RGBA", (W + 40, H + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([20, 20, 20 + W, 20 + H], radius=H // 2, fill=(8, 8, 12, 170),
                        outline=accent + (230,), width=max(2, int(2 * scale)))
    fx, fy, fw, fh = 20 + int(15 * scale), 20 + int(17 * scale), int(38 * scale), int(28 * scale)
    mask = Image.new("L", (fw, fh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, fw, fh], radius=4, fill=255)
    flag = Image.new("RGBA", (fw, fh))
    draw_flag(ImageDraw.Draw(flag), 0, 0, fw, fh)
    overlay.paste(flag, (fx, fy), mask)
    f = montserrat(int(23 * scale), 800)
    db = ImageDraw.Draw(overlay)
    draw_tracking(db, (fx + fw + int(12 * scale), 20 + (H - f.size) // 2 + int(2 * scale)),
                  "DSKY", f, (247, 242, 231, 255), tr=1.5 * scale)
    img.alpha_composite(overlay.resize((W + 40, H + 40)) if False else overlay, (int(x) - 20, int(y) - 20))

def scrim(img, style, W, H):
    """Voiles : assombrissement global léger + dégradé fort en haut (titre)
    + dégradé bas (signature). Garantit la lisibilité sur fonds clairs."""
    s = STYLES[style]["scrim"]
    ov = Image.new("RGBA", (W, H), s + (38,))          # voile global doux
    d = ImageDraw.Draw(ov)
    plateau = int(H * 0.20)                            # zone titre bien assombrie
    top_end = int(H * 0.74)
    for i in range(top_end):
        if i < plateau:
            a = 225
        else:
            t = (i - plateau) / max(1, (top_end - plateau))
            a = int(225 * (1 - t) ** 1.30)
        d.line([(0, i), (W, i)], fill=s + (a,))
    bot_start = int(H * 0.80)
    for i in range(bot_start, H):
        t = (i - bot_start) / max(1, (H - bot_start))
        a = int(185 * t ** 1.15)
        d.line([(0, i), (W, i)], fill=s + (a,))
    img.alpha_composite(ov)

def grain(img, amount=6):
    import random
    px = img.load()
    w, h = img.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    random.seed(7)
    for _ in range(int(w * h * 0.02)):
        x, y = random.randrange(w), random.randrange(h)
        d.point((x, y), fill=(255, 255, 255, random.randint(0, amount)))
    img.alpha_composite(ov)

# ------------------------------------------------------------------ compose
def compose(base_path, quote_text, style, num, out_post, out_story):
    W_POST, H_POST = 1080, 1350
    W_ST, H_ST = 1080, 1920
    base = Image.open(base_path).convert("RGB")
    pal = STYLES[style]

    def make(W, H, zone):
        img = base.copy()
        # cover-fit : on recadre en gardant le BAS de l'image (le sujet) et l'espace au-dessus
        r = max(W / img.width, H / img.height)
        nw, nh = int(img.width * r) + 1, int(img.height * r) + 1
        img = img.resize((nw, nh), Image.LANCZOS)
        x0 = (nw - W) // 2
        y0 = max(0, min(int((nh - H) * 0.42), nh - H))  # légèrement au-dessus du centre
        img = img.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
        scrim(img, style, W, H)
        d = ImageDraw.Draw(img)

        m = int(W * 0.075)
        # badge + numéro (aligné à droite, dessiné une seule fois)
        draw_badge(img, m, m, pal["accent"], scale=1.0)
        fnum = montserrat(26, 700)
        num_txt = f"N° {num:02d}"
        nw_num = tracking_w(d, num_txt, fnum, 3)
        draw_tracking(d, (W - m - nw_num, m + 14), num_txt, fnum, pal["accent"] + (255,), tr=3)

        # citation — zone haute
        zx0, zy0, zx1, zy1 = zone
        f, lines, lh = fit_text(d, quote_text, zx1 - zx0, zy1 - zy0,
                                lambda s: playfair(s, 600) if style != "AFRO" else montserrat(s, 600),
                                64 if H > 1400 else 58, 34)
        total = len(lines) * lh
        y = zy0 + (zy1 - zy0 - total) / 2
        for ln in lines:
            draw_tracking(d, (0, y), ln, f, pal["text"] + (255,), tr=0.4, anchor_center_x=W / 2)
            y += lh

        # signature en bas
        fy = H - int(H * 0.052)
        rule_w = 56
        d.rectangle([W / 2 - rule_w / 2, fy - 34, W / 2 + rule_w / 2, fy - 31], fill=pal["accent"] + (255,))
        fsig = montserrat(25, 700)
        draw_tracking(d, (0, fy - 8), "C. JÉSUTONDJI SAMUEL STEIN", fsig,
                      pal["text"] + (235,), tr=3.2, anchor_center_x=W / 2, shadow=(0, 0, 0, 150))
        fsub = montserrat(15, 500)
        sub = "LYRICISTE  ·  BÉNIN"
        subw = tracking_w(d, sub, fsub, 3.6)
        draw_tracking(d, (0, fy + 26), sub, fsub,
                      pal["accent"] + (220,), tr=3.6, anchor_center_x=W / 2, shadow=(0, 0, 0, 150))
        # mini-drapeaux 🇧🇯 flanquant la ligne de signature
        fw2, fh2, gap = 27, 18, 16
        for fx in (W / 2 - subw / 2 - gap - fw2, W / 2 + subw / 2 + gap):
            mflag = Image.new("L", (fw2, fh2), 0)
            ImageDraw.Draw(mflag).rounded_rectangle([0, 0, fw2, fh2], radius=3, fill=255)
            fl = Image.new("RGBA", (fw2, fh2))
            draw_flag(ImageDraw.Draw(fl), 0, 0, fw2, fh2)
            img.paste(fl, (int(fx), fy + 27), mflag)
        # liseré tricolore béninois sur le bord inférieur
        sh_ = max(6, int(H * 0.0065))
        third = int(W / 3)
        d.rectangle([0, H - sh_, third, H], fill=BENIN_GREEN)
        d.rectangle([third, H - sh_, W, H - sh_ // 2], fill=BENIN_YELLOW)
        d.rectangle([third, H - sh_ // 2, W, H], fill=BENIN_RED)
        grain(img)
        return img.convert("RGB")

    make(W_POST, H_POST, (m := int(W_POST * 0.09), int(H_POST * 0.13), W_POST - m, int(H_POST * 0.50))) \
        .save(out_post, quality=92, subsampling=0, optimize=True)
    m2 = int(W_ST * 0.085)
    make(W_ST, H_ST, (m2, int(H_ST * 0.115), W_ST - m2, int(H_ST * 0.475))) \
        .save(out_story, quality=92, subsampling=0, optimize=True)

# ------------------------------------------------------------------ main
def main(salve="01"):
    meta = json.load(open(os.path.join(ROOT, f"salve-{salve}.json"), encoding="utf-8"))
    for item in meta:
        q = EMOJI.sub("", item["text"]).strip()
        q = re.sub(r"\s{2,}", " ", q)
        n = item["num"]
        compose(os.path.join(ROOT, item["base"]), q, item["style"], n,
                os.path.join(ROOT, f"salve-{salve}", "post", f"quote-{n:02d}-post.jpg"),
                os.path.join(ROOT, f"salve-{salve}", "story", f"quote-{n:02d}-story.jpg"))
        print(f"✔ citation {n:02d} [{item['style']}]")
    print("Done.")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "01")
