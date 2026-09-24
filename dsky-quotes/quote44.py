#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSKY QUOTES — Citation 44 « Le partage » : stickers adaptés (pièce d'or, partage)."""
import os, re
from PIL import Image, ImageDraw
from compose import (ROOT, playfair, montserrat, draw_tracking, tracking_w,
                     draw_badge, draw_flag, scrim, grain, fit_text, STYLES)

TXT = ("Comment vois-tu le partage ? Je te réveille. Toi seul crois ou penses que "
       "partager signifie donner 50 % de ce que tu as, ou tout donner. Donner "
       "0,00009 % de ce que tu as suffit pour dire que « je partage toujours ce "
       "que j'ai »… Tu t'étonnes d'être toujours vidé et les autres non, après un "
       "partage ? Bah, le souci est que tu en donnes plus que tu ne supporterais.")

def sticker_coin(img, cx, cy, r, label):
    """Pièce d'or + étiquette « 0,00009 %» — dessinée, pas générée."""
    ov = Image.new("RGBA", (int(r*4), int(r*6)), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    ccx, ccy = int(r*2), int(r*2)
    d.ellipse([ccx-r, ccy-r, ccx+r, ccy+r], fill=(20,14,4,140))          # ombre
    d.ellipse([ccx-r, ccy-r-3, ccx+r, ccy-r-3+2*r], fill=(146,109,21,255))  # bord sombre
    d.ellipse([ccx-r+4, ccy-r-3+4, ccx+r-4, ccy+r-7], fill=(233,183,54,255))  # or
    d.ellipse([ccx-int(r*.72), ccy-int(r*.72)-3, ccx+int(r*.72), ccy+int(r*.72)-3],
              outline=(255,226,140,255), width=3)
    f = montserrat(int(r*0.62), 800)
    # étoile à 5 branches dessinée (glyphe ✦ indisponible dans la police)
    import math
    pts = []
    for k in range(10):
        ang = -math.pi/2 + k*math.pi/5
        rr = r*0.55 if k % 2 == 0 else r*0.24
        pts.append((ccx + rr*math.cos(ang), ccy - 3 + rr*math.sin(ang)))
    d.polygon(pts, fill=(255,240,200,255))
    # étiquette
    fl = montserrat(int(r*0.46), 700)
    tw = tracking_w(d, label, fl, 1)
    bw, bh = int(tw + r*0.7), int(fl.size*1.8)
    bx, by = ccx - bw//2, ccy + r + int(r*0.35)
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=bh//2, fill=(8,8,12,200),
                        outline=(233,183,54,235), width=2)
    draw_tracking(d, (bx + (bw-tw)//2, by + bh//2 - fl.size//2 - 2), label, fl,
                  (240,220,150,255), tr=1)
    img.alpha_composite(ov, (int(cx - r*2), int(cy - r*2)))

def sticker_share(img, cx, cy, s):
    """Icône « partage » (3 nœuds reliés)."""
    ov = Image.new("RGBA", (int(s*3), int(s*3)), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    ax, ay = s*0.5, s*0.7
    bx, by = s*2.0, s*0.35
    cxx, cyy = s*2.0, s*1.9
    r = s*0.42
    for (px, py) in ((ax,ay),(bx,by),(cxx,cyy)):
        d.ellipse([px-r-3, py-r-3, px+r+3, py+r+3], fill=(15,12,6,150))
    d.line([ax, ay, bx, by], fill=(247,242,231,235), width=int(s*0.16))
    d.line([ax, ay, cxx, cyy], fill=(247,242,231,235), width=int(s*0.16))
    d.line([bx, by, cxx, cyy], fill=(247,242,231,235), width=int(s*0.16))
    for (px, py) in ((ax,ay),(bx,by),(cxx,cyy)):
        d.ellipse([px-r, py-r, px+r, py+r], fill=(233,183,54,255))
        d.ellipse([px-r*0.45, py-r*0.45, px+r*0.45, py+r*0.45], fill=(255,235,170,255))
    img.alpha_composite(ov, (int(cx - s*1.2), int(cy - s*1.2)))

def quote44():
    base = Image.open(os.path.join(ROOT, "assets/bases/base-44.jpg")).convert("RGB")
    pal = STYLES["LUXE"]
    for (W, H, zone, out) in (
        (1080, 1350, (0.10, 0.105, 0.535), "salve-05/post/quote-44-post.jpg"),
        (1080, 1920, (0.085, 0.100, 0.465), "salve-05/story/quote-44-story.jpg"),
    ):
        img = base.copy()
        r = max(W/img.width, H/img.height)
        img = img.resize((int(img.width*r)+1, int(img.height*r)+1), Image.LANCZOS)
        x0 = (img.width - W)//2
        y0 = max(0, min(int((img.height-H)*0.42), img.height-H))
        img = img.crop((x0, y0, x0+W, y0+H)).convert("RGBA")
        scrim(img, "LUXE", W, H)
        d = ImageDraw.Draw(img)
        m = int(W*0.075)
        draw_badge(img, m, m, pal["accent"])
        fnum = montserrat(26, 700)
        t = f"N° 44"
        tw_ = tracking_w(d, t, fnum, 3)
        draw_tracking(d, (W-m-tw_, m+14), t, fnum, pal["accent"]+(255,), tr=3,
                      shadow=(0,0,0,160))

        # stickers — sur le mur, à côté de la tête, JAMAIS dans la zone de texte
        if H > 1400:
            sticker_coin(img,  W*0.855, H*0.520, 46, "0,00009 %")
            sticker_share(img, W*0.135, H*0.500, 26)
        else:
            sticker_coin(img,  W*0.850, H*0.560, 42, "0,00009 %")
            sticker_share(img, W*0.135, H*0.535, 24)

        zx0, zy0f, zy1f = zone
        f, lines, lh = fit_text(d, TXT, W*(1-2*zx0), H*(zy1f-zy0f),
                                lambda s: playfair(s, 600), 64 if H > 1400 else 58, 34)
        total = len(lines)*lh
        y = H*zy0f + (H*(zy1f-zy0f) - total)/2
        for ln in lines:
            draw_tracking(d, (0, y), ln, f, pal["text"]+(255,), tr=0.4,
                          anchor_center_x=W/2, shadow=(0,0,0,120))
            y += lh

        fy = H - int(H*0.052)
        d.rectangle([W/2-28, fy-34, W/2+28, fy-31], fill=pal["accent"]+(255,))
        fsig = montserrat(25, 700)
        draw_tracking(d, (0, fy-8), "C. JÉSUTONDJI SAMUEL STEIN", fsig,
                      pal["text"]+(235,), tr=3.2, anchor_center_x=W/2, shadow=(0,0,0,150))
        fsub = montserrat(15, 500)
        sub = "LYRICISTE  ·  BÉNIN"
        subw = tracking_w(d, sub, fsub, 3.6)
        draw_tracking(d, (0, fy+26), sub, fsub, pal["accent"]+(220,), tr=3.6,
                      anchor_center_x=W/2, shadow=(0,0,0,150))
        fw2, fh2, gap = 27, 18, 16
        for fx in (W/2-subw/2-gap-fw2, W/2+subw/2+gap):
            mflag = Image.new("L", (fw2, fh2), 0)
            ImageDraw.Draw(mflag).rounded_rectangle([0,0,fw2,fh2], radius=3, fill=255)
            fl = Image.new("RGBA", (fw2, fh2))
            draw_flag(ImageDraw.Draw(fl), 0, 0, fw2, fh2)
            img.paste(fl, (int(fx), fy+27), mflag)
        sh_ = max(6, int(H*0.0065)); third = int(W/3)
        d.rectangle([0, H-sh_, third, H], fill=(0,135,81))
        d.rectangle([third, H-sh_, W, H-sh_//2], fill=(252,209,22))
        d.rectangle([third, H-sh_//2, W, H], fill=(232,17,45))
        grain(img)
        img.convert("RGB").save(os.path.join(ROOT, out), quality=92, subsampling=0, optimize=True)
        print("✔", out)

if __name__ == "__main__":
    quote44()
