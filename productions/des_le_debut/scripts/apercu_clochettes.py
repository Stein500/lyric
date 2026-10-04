#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aperçu — CTA « clochettes animées » (style effets VN / VivaCut / CapCut)
Projet : Dès le début — Daïsky / Wolof TechStein
Rôle   : montrer à l'artiste l'animation prévue pendant les fenêtres
         SANS PAROLES ≥ 5 s (intro, ponts instrumentaux, outro).
Sortie : apercu/CLOCHETTES_apercu.gif (+ .png fixe)
Note   : fond = placeholder de mise en page, pas un fond de production.
"""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 480, 854                     # maquette : design 1080x1920 ramené (÷2.25)
FPS   = 12
NFR   = 36                          # 3,0 s en boucle
OUT   = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apercu"))
os.makedirs(OUT, exist_ok=True)

DEJAVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONT     = "/home/user/lyric/dsky-quotes/assets/fonts/Montserrat.ttf"
f = lambda p, s: ImageFont.truetype(p, s)

GOLD, GOLD2 = (255, 196, 78), (255, 236, 168)
CYAN, WHITE = (86, 226, 255), (255, 255, 255)

TXT_ABO  = f(DEJAVU_B, 31)
TXT_PART = f(DEJAVU_B, 31)
TXT_HINT = f(DEJAVU_B, 18)
TXT_LYR  = f(DEJAVU_B, 21)
TXT_TAG  = f(MONT, 15)

# ------------------------------------------------------------------ fond (provisoire)
def make_bg():
    bg = Image.new("RGB", (W, H), (10, 14, 26))
    d = ImageDraw.Draw(bg, "RGBA")
    for i in range(H):
        t = i / H
        d.line([(0, i), (W, i)], fill=(int(12 + 26 * (1 - t) ** 2),
                                       int(16 + 34 * (1 - t) ** 2),
                                       int(30 + 58 * (1 - t) ** 2)))
    for cx, cy, rad, col in [(80, 180, 90, (255, 176, 64, 26)), (410, 300, 120, (86, 226, 255, 20)),
                             (140, 690, 150, (255, 176, 64, 16)), (390, 640, 80, (86, 226, 255, 16))]:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=col)
        bg = Image.alpha_composite(bg.convert("RGBA"),
                                   lay.filter(ImageFilter.GaussianBlur(28))).convert("RGB")
    return bg

# ------------------------------------------------------------------ cloche vectorielle
def bell_sprite(size=190):
    """Cloche dorée dessinée en vectoriel (aucun emoji système)."""
    S = size * 3
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = S / 2
    y_top, y_lip = S * 0.20, S * 0.76
    half = S * 0.33
    prof = []
    N = 80
    for k in range(N + 1):                      # profil gauche : bas -> haut
        s = k / N                               # 0 = lèvre, 1 = sommet
        w = half * (1 - s ** 3.0) ** 0.5 * (1 + 0.10 * (1 - s) ** 2)
        prof.append((cx - w, y_lip - s * (y_lip - y_top)))
    for k in range(N + 1):                      # profil droit : haut -> bas
        s = 1 - k / N
        w = half * (1 - s ** 3.0) ** 0.5 * (1 + 0.10 * (1 - s) ** 2)
        prof.append((cx + w, y_lip - s * (y_lip - y_top)))
    d.polygon(prof, fill=GOLD)
    d.line(prof + [prof[0]], fill=GOLD2, width=int(S * 0.012), joint="curve")
    # lèvre / rebord inférieur
    d.rounded_rectangle([cx - half * 1.16, y_lip - S * 0.045, cx + half * 1.16, y_lip + S * 0.035],
                        radius=S * 0.028, fill=GOLD, outline=GOLD2, width=int(S * 0.010))
    # anse
    d.arc([cx - S * 0.085, y_top - S * 0.10, cx + S * 0.085, y_top + S * 0.055],
          start=180, end=360, fill=GOLD2, width=int(S * 0.032))
    # battant
    d.ellipse([cx - S * 0.070, y_lip + S * 0.020, cx + S * 0.070, y_lip + S * 0.150],
              fill=GOLD2, outline=(158, 104, 18), width=int(S * 0.008))
    # reflet
    d.ellipse([cx - half * 0.72, y_top + S * 0.05, cx - half * 0.40, y_top + S * 0.22],
              fill=(255, 255, 255, 95))
    halo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    g = im.filter(ImageFilter.GaussianBlur(S * 0.045))
    halo.paste(g, (0, 0), g)
    im = Image.alpha_composite(halo, im)
    return im.resize((size, size), Image.LANCZOS)

def star(d, cx, cy, r, col):
    d.polygon([(cx, cy - r), (cx + r * .28, cy - r * .28), (cx + r, cy), (cx + r * .28, cy + r * .28),
               (cx, cy + r), (cx - r * .28, cy + r * .28), (cx - r, cy), (cx - r * .28, cy - r * .28)],
              fill=col)

def share_sprite(size=38, col=WHITE):
    S = size * 3
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = S * 0.12
    p = [(S * .26, S * .54), (S * .70, S * .28), (S * .70, S * .80)]
    for x, y in p[1:]:
        d.line([p[0], (x, y)], fill=col, width=int(S * .055))
    for x, y in p:
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    d.polygon([(S * .70, S * .04), (S * .99, S * .13), (S * .70, S * .22)], fill=col)
    return im.resize((size, size), Image.LANCZOS)

# ------------------------------------------------------------------ mise en page
BG      = make_bg()
BELL    = bell_sprite(190)
SHARE   = share_sprite(38)
CARD    = (26, 306, W - 26, 700)                 # carte translucide
BELL_CX = W // 2
BELL_TOP = 330
BELL_SZ  = 190
WAVE_CY  = BELL_TOP + 96

def frame(i):
    t  = i / FPS
    ph = 2 * math.pi * t / 1.2
    swing = 15 * math.sin(ph) * math.exp(-0.22 * ((t % 1.2) / 1.2))
    pulse = 1.0 + 0.05 * math.sin(2 * math.pi * t / 0.8)

    im = BG.copy().convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay, "RGBA")

    d.rounded_rectangle(CARD, radius=26, fill=(8, 12, 24, 130),
                        outline=(255, 196, 78, 80), width=2)

    # ondes de sonnerie
    for k in range(2):
        u = ((t / 0.9) + k * 0.5) % 1.0
        rr = 58 + 126 * u
        d.ellipse([BELL_CX - rr, WAVE_CY - rr, BELL_CX + rr, WAVE_CY + rr],
                  outline=(255, 196, 78, int(150 * (1 - u) ** 1.6)), width=3)

    # cloche qui balance (pivot = anse)
    sz = int(BELL_SZ * pulse)
    b = BELL.resize((sz, sz), Image.LANCZOS).rotate(swing, resample=Image.BICUBIC,
                                                    center=(sz / 2, sz * 0.10))
    lay.alpha_composite(b, (BELL_CX - sz // 2, BELL_TOP))

    # étincelles
    for sx, sy, off in [(BELL_CX - 118, BELL_TOP + 58, 0.0), (BELL_CX + 112, BELL_TOP + 78, 0.35),
                        (BELL_CX + 66, BELL_TOP + 12, 0.7)]:
        u = ((t / 0.7) + off) % 1.0
        al = int(235 * (1 - abs(0.5 - u) * 2) ** 0.8)
        if al > 0:
            star(d, sx, sy, 6 + 5 * math.sin(math.pi * u), (255, 240, 190, al))

    # flèche clignotante vers la cloche
    u = (t / 1.0) % 1.0
    if u < 0.72:
        al = int(255 * (1 - u / 0.72))
        yy = BELL_TOP - 34 + u * 20
        d.polygon([(BELL_CX, yy + 22), (BELL_CX - 15, yy), (BELL_CX + 15, yy)], fill=(255, 255, 255, al))

    # ABONNE-TOI
    d.text((BELL_CX, 552), "ABONNE-TOI", font=TXT_ABO, fill=(255, 255, 255, 255), anchor="mm",
           stroke_width=4, stroke_fill=(0, 0, 0, 180))

    # pastille PARTAGE (action prioritaire, contour cyan pulsé)
    box = [BELL_CX - 152, 584, BELL_CX + 152, 632]
    d.rounded_rectangle(box, radius=24, fill=(10, 20, 34, 190),
                        outline=(86, 226, 255, 110 + int(90 * math.sin(2 * math.pi * t / 0.9))), width=3)
    lay.alpha_composite(SHARE, (box[0] + 20, 589))
    d.text((BELL_CX + 20, 608), "PARTAGE", font=TXT_PART, fill=(255, 255, 255, 255), anchor="mm",
           stroke_width=4, stroke_fill=(0, 0, 0, 180))

    d.text((BELL_CX, 668), "Clique sur la cloche — puis PARTAGE", font=TXT_HINT,
           fill=(255, 232, 160, 240), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 170))

    # contexte maquette
    d.text((W // 2, 146), "DÈS LE DÉBUT", font=TXT_TAG, fill=(255, 255, 255, 150), anchor="mm")
    d.text((W // 2, 170), "aperçu d'animation — fond provisoire", font=TXT_TAG,
           fill=(255, 255, 255, 105), anchor="mm")
    d.text((W // 2, 236), "Dès le début, Tu es là, Tu es là", font=TXT_LYR, fill=(255, 250, 235, 240),
           anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 160))
    d.text((W // 2, 730), "exemple : aucune parole pendant 25,2 s", font=TXT_TAG,
           fill=(200, 205, 215, 150), anchor="mm")

    out = Image.alpha_composite(im, lay)
    d2 = ImageDraw.Draw(out, "RGBA")
    yb = H - 12
    d2.rectangle([0, yb, W // 3, H], fill=(0, 135, 81, 255))
    d2.rectangle([W // 3, yb, W, yb + 6], fill=(252, 209, 22, 255))
    d2.rectangle([W // 3, yb + 6, W, H], fill=(232, 17, 45, 255))
    return out.convert("RGB")

frames = [frame(i) for i in range(NFR)]
gif = os.path.join(OUT, "CLOCHETTES_apercu.gif")
frames[0].save(gif, save_all=True, append_images=frames[1:], duration=int(1000 / FPS), loop=0,
               optimize=True, disposal=2)
frames[4].save(os.path.join(OUT, "CLOCHETTES_apercu.png"))
print("OK", gif, os.path.getsize(gif) // 1024, "ko")
