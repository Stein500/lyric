#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSKY QUOTES — Série ART (65+) : citations typographiées PAR L'IA dans l'œuvre.
Branding discret ajouté par code : badge, numéro, signature + CTA dans la bande basse."""
import os
from PIL import Image, ImageDraw
from compose import (ROOT, montserrat, draw_tracking, tracking_w, draw_badge,
                     draw_flag, grain, STYLES)
from compose_s2 import icon_heart, icon_comment, icon_share, icon_plus

ART = {  # num -> style d'accent
    65: "LUXE", 66: "LUXE", 67: "AFRO", 68: "MINIMAL", 69: "MINIMAL", 70: "LUXE",
    71: "LUXE", 72: "LUXE", 73: "MINIMAL", 74: "LUXE", 75: "MINIMAL",
    76: "LUXE", 77: "AFRO", 78: "LUXE", 79: "AFRO", 80: "AFRO",
    81: "LUXE", 82: "LUXE", 83: "MINIMAL", 84: "AFRO", 85: "AFRO",
    86: "LUXE", 87: "MINIMAL", 88: "MINIMAL", 89: "LUXE", 90: "AFRO",
    91: "LUXE", 92: "MINIMAL", 93: "MINIMAL", 94: "LUXE", 95: "AFRO",
    96: "MINIMAL", 97: "AFRO", 98: "AFRO", 99: "MINIMAL", 100: "LUXE",
    101: "MINIMAL", 102: "LUXE", 103: "MINIMAL", 104: "MINIMAL", 105: "AFRO",
    106: "MINIMAL", 107: "AFRO", 108: "LUXE", 109: "LUXE", 110: "AFRO",
    111: "LUXE", 112: "LUXE", 113: "MINIMAL", 114: "MINIMAL", 115: "LUXE",
    116: "MINIMAL", 117: "MINIMAL", 118: "AFRO", 119: "LUXE", 120: "LUXE",
    121: "AFRO", 122: "LUXE", 123: "AFRO", 124: "AFRO", 125: "LUXE",
    126: "MINIMAL", 127: "LUXE", 128: "AFRO", 129: "AFRO", 130: "LUXE",
    131: "LUXE", 132: "LUXE", 133: "MINIMAL", 134: "LUXE", 135: "LUXE",
    136: "LUXE", 137: "MINIMAL", 138: "MINIMAL", 139: "MINIMAL", 140: "MINIMAL",
    141: "LUXE", 142: "LUXE", 143: "MINIMAL", 144: "AFRO", 145: "LUXE",
    146: "MINIMAL", 147: "MINIMAL", 148: "AFRO", 149: "LUXE", 150: "LUXE",
    151: "AFRO", 152: "LUXE", 153: "AFRO", 154: "AFRO", 155: "LUXE",
    156: "AFRO", 157: "MINIMAL", 158: "LUXE", 159: "MINIMAL", 160: "LUXE",
    161: "LUXE", 162: "AFRO", 163: "MINIMAL", 164: "LUXE", 165: "AFRO",
    166: "MINIMAL", 167: "LUXE", 168: "AFRO", 169: "LUXE", 170: "MINIMAL",
    171: "LUXE", 172: "AFRO", 173: "LUXE", 174: "MINIMAL", 175: "LUXE",
    176: "AFRO", 177: "LUXE", 178: "MINIMAL", 179: "AFRO", 180: "LUXE",
}

def brand(num):
    W, H = 1080, 1920
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

    # léger dégradé bas pour asseoir le branding
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    od = ImageDraw.Draw(ov)
    bs = int(H*0.86)
    for i in range(bs, H):
        t = (i-bs)/(H-bs)
        od.line([(0,i),(W,i)], fill=(8,8,10,int(200*t*t)))
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)

    draw_badge(img, m, m, acc)
    fnum = montserrat(26, 700)
    t = f"N° {num}"
    wnum = tracking_w(d, t, fnum, 3)
    draw_tracking(d, (W-m-wnum, m+14), t, fnum, acc+(255,), tr=3, shadow=(0,0,0,160))

    fy = H - 235
    d.rectangle([W/2-28, fy-36, W/2+28, fy-33], fill=acc+(255,))
    fsig = montserrat(25, 700)
    draw_tracking(d, (0, fy-10), "C. JÉSUTONDJI SAMUEL STEIN", fsig,
                  txt+(240,), tr=3.2, anchor_center_x=W/2, shadow=(0,0,0,150))
    fsub = montserrat(14, 500)
    sub = "LYRICISTE  ·  BÉNIN"
    subw = tracking_w(d, sub, fsub, 3.6)
    draw_tracking(d, (0, fy+22), sub, fsub, acc+(220,), tr=3.6,
                  anchor_center_x=W/2, shadow=(0,0,0,150))
    fw2, fh2, gap = 25, 17, 15
    for fx in (W/2-subw/2-gap-fw2, W/2+subw/2+gap):
        mflag = Image.new("L", (fw2, fh2), 0)
        ImageDraw.Draw(mflag).rounded_rectangle([0,0,fw2,fh2], radius=3, fill=255)
        fl = Image.new("RGBA", (fw2, fh2))
        draw_flag(ImageDraw.Draw(fl), 0, 0, fw2, fh2)
        img.paste(fl, (int(fx), fy+23), mflag)

    # CTA compacte sous la signature
    cta = [("LIKE", icon_heart), ("COMMENTE", icon_comment),
           ("PARTAGE", icon_share), ("ABONNE-TOI", icon_plus)]
    fi = montserrat(19, 700); tr = 2; dotw, gaps = 22, 40
    blocks = [(w_, ic, tracking_w(d, w_, fi, tr)) for w_, ic in cta]
    total = sum(22+9+ww for _,_,ww in blocks) + 3*(dotw+gaps)
    x = W/2 - total/2; ycta = H - 92
    for i, (word, icon, ww) in enumerate(blocks):
        icon(d, x+11, ycta+11, 22, acc+(255,))
        draw_tracking(d, (x+22+9, ycta), word, fi, txt+(235,), tr=tr, shadow=(0,0,0,140))
        x += 22+9+ww
        if i < 3:
            d.ellipse([x+dotw/2-3, ycta+8, x+dotw/2+3, ycta+14], fill=acc+(255,))
            x += dotw+gaps
    grain(img, amount=4)
    out = os.path.join(ROOT, f"saison-02/story/quote-{num}-story.jpg")
    img.convert("RGB").save(out, quality=92, subsampling=0, optimize=True)
    print("✔", f"quote-{num}-story.jpg  [ART · {ART[num]}]")

if __name__ == "__main__":
    for n in tuple(ART):
        brand(n)
