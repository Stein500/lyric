#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSKY QUOTES — Variantes TIKTOK de la série ART (65+).
Même œuvre, branding remonté en ZONE SÛRE TikTok :
  · haut : badge + N° descendus à y=150 (sous la nav TikTok)
  · bas  : signature + CTA terminent à ~y=1630 → ~290 px libres en bas
           (pseudo, légende, titre musical, barre de progression TikTok)
  · droite : textes centrés, colonne de boutons (♡ 💬 →) dégagée.
Sortie : saison-02/tiktok/quote-NN-tiktok.jpg
"""
import os
from PIL import Image, ImageDraw
from compose import (ROOT, montserrat, draw_tracking, tracking_w, draw_badge,
                     draw_flag, grain, STYLES)
from compose_s2 import icon_heart, icon_comment, icon_share, icon_plus
from compose_art import ART

W, H = 1080, 1920

def brand_tiktok(num):
    src = os.path.join(ROOT, f"assets/bases/base-{num}.jpg")
    img = Image.open(src).convert("RGB")
    if img.size != (W, H):
        r = max(W/img.width, H/img.height)
        img = img.resize((int(img.width*r)+1, int(img.height*r)+1), Image.LANCZOS)
        x0 = (img.width-W)//2; y0 = (img.height-H)//2
        img = img.crop((x0, y0, x0+W, y0+H))
    img = img.convert("RGBA")
    acc = STYLES[ART[num]]["accent"]
    txt = STYLES[ART[num]]["text"]
    d = ImageDraw.Draw(img)
    m = int(W*0.06)

    # dégradé remonté + un peu plus fort (asseoir le branding en zone sûre)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    bs = int(H*0.677)                      # ~1300 : démarre plus haut que la version story
    for i in range(bs, H):
        t = (i-bs)/(H-bs)
        od.line([(0, i), (W, i)], fill=(8, 8, 10, int(205*t*t)))
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)

    # ---- haut : badge + N° en position story (au-dessus de la citation) ----
    draw_badge(img, m, m, acc)
    fnum = montserrat(26, 700)
    t = f"N° {num}"
    wnum = tracking_w(d, t, fnum, 3)
    draw_tracking(d, (W-m-wnum, m+14), t, fnum, acc+(255,), tr=3, shadow=(0, 0, 0, 160))

    # ---- bas : bloc signature + CTA remonté (finit ~y=1631) ----
    fy = H - 380                           # 1540
    d.rectangle([W/2-28, fy-36, W/2+28, fy-33], fill=acc+(255,))
    fsig = montserrat(25, 700)
    draw_tracking(d, (0, fy-10), "C. JÉSUTONDJI SAMUEL STEIN", fsig,
                  txt+(240,), tr=3.2, anchor_center_x=W/2, shadow=(0, 0, 0, 170))
    fsub = montserrat(14, 500)
    sub = "LYRICISTE  ·  BÉNIN"
    subw = tracking_w(d, sub, fsub, 3.6)
    draw_tracking(d, (0, fy+22), sub, fsub, acc+(220,), tr=3.6,
                  anchor_center_x=W/2, shadow=(0, 0, 0, 170))
    fw2, fh2, gap = 25, 17, 15
    for fx in (W/2-subw/2-gap-fw2, W/2+subw/2+gap):
        mflag = Image.new("L", (fw2, fh2), 0)
        ImageDraw.Draw(mflag).rounded_rectangle([0, 0, fw2, fh2], radius=3, fill=255)
        fl = Image.new("RGBA", (fw2, fh2))
        draw_flag(ImageDraw.Draw(fl), 0, 0, fw2, fh2)
        img.paste(fl, (int(fx), fy+23), mflag)

    cta = [("LIKE", icon_heart), ("COMMENTE", icon_comment),
           ("PARTAGE", icon_share), ("ABONNE-TOI", icon_plus)]
    fi = montserrat(19, 700); tr = 2; dotw, gaps = 22, 40
    blocks = [(w_, ic, tracking_w(d, w_, fi, tr)) for w_, ic in cta]
    total = sum(22+9+ww for _, _, ww in blocks) + 3*(dotw+gaps)
    x = W/2 - total/2; ycta = fy + 58      # 1598 → bloc terminé ~1631
    for i, (word, icon, ww) in enumerate(blocks):
        icon(d, x+11, ycta+11, 22, acc+(255,))
        draw_tracking(d, (x+22+9, ycta), word, fi, txt+(235,), tr=tr, shadow=(0, 0, 0, 160))
        x += 22+9+ww
        if i < 3:
            d.ellipse([x+dotw/2-3, ycta+8, x+dotw/2+3, ycta+14], fill=acc+(255,))
            x += dotw+gaps
    grain(img, amount=4)
    out = os.path.join(ROOT, f"saison-02/tiktok/quote-{num}-tiktok.jpg")
    img.convert("RGB").save(out, quality=92, subsampling=0, optimize=True)
    print("✔", f"quote-{num}-tiktok.jpg  [TIKTOK · {ART[num]}]")

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "saison-02/tiktok"), exist_ok=True)
    for n in tuple(ART):
        brand_tiktok(n)
