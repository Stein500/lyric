#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSKY QUOTES — Couverture de la collection (post + story)."""
import os
from PIL import Image, ImageDraw
from compose import (ROOT, playfair, montserrat, draw_tracking, tracking_w,
                     draw_badge, draw_flag, scrim, grain, STYLES)

def cover(base_path, out_post, out_story):
    base = Image.open(base_path).convert("RGB")
    for (W, H, out) in ((1080, 1350, out_post), (1080, 1920, out_story)):
        img = base.copy()
        r = max(W / img.width, H / img.height)
        img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
        x0 = (img.width - W) // 2
        y0 = max(0, min(int((img.height - H) * 0.42), img.height - H))
        img = img.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
        scrim(img, "LUXE", W, H)
        d = ImageDraw.Draw(img)
        m = int(W * 0.075)
        pal = STYLES["LUXE"]

        draw_badge(img, m, m, pal["accent"])
        fnum = montserrat(24, 700)
        t = "ÉDITION 2026"
        w = tracking_w(d, t, fnum, 3)
        draw_tracking(d, (W - m - w, m + 14), t, fnum, pal["accent"] + (255,), tr=3,
                      shadow=(0, 0, 0, 160))

        # bloc titre centré dans la zone libre
        cy = int(H * (0.20 if H > 1400 else 0.215))
        over = "C. JÉSUTONDJI SAMUEL STEIN"
        fo = montserrat(int(W * 0.026), 700)
        draw_tracking(d, (0, cy), over, fo, pal["text"] + (240,), tr=int(W*0.004),
                      anchor_center_x=W/2, shadow=(0, 0, 0, 160))
        fti = playfair(int(W * 0.155), 700)
        draw_tracking(d, (0, cy + int(W * 0.055)), "PENSÉES", fti, pal["accent"] + (255,),
                      tr=int(W*0.006), anchor_center_x=W/2, shadow=(0, 0, 0, 190))
        ry = cy + int(W * 0.055) + int(W * 0.185)
        d.rectangle([W/2 - 70, ry, W/2 + 70, ry + 4], fill=pal["accent"] + (255,))
        fsub = playfair(int(W * 0.052), 500, italic=True)
        draw_tracking(d, (0, ry + int(W * 0.035)), "d'un Lyriciste béninois", fsub,
                      pal["text"] + (250,), tr=1, anchor_center_x=W/2, shadow=(0, 0, 0, 160))
        f41 = montserrat(int(W * 0.020), 700)
        t41 = "41 CITATIONS  ·  2019 — 2026"
        w41 = tracking_w(d, t41, f41, 3)
        draw_tracking(d, (0, ry + int(W * 0.115)), t41, f41, pal["accent"] + (230,), tr=3,
                      anchor_center_x=W/2, shadow=(0, 0, 0, 160))

        # signature bas de page + drapeaux + liseré (identique aux quotes)
        fy = H - int(H * 0.052)
        fsig = montserrat(25, 700)
        draw_tracking(d, (0, fy - 8), "C. JÉSUTONDJI SAMUEL STEIN", fsig,
                      pal["text"] + (235,), tr=3.2, anchor_center_x=W/2, shadow=(0, 0, 0, 150))
        fsub2 = montserrat(15, 500)
        sub = "LYRICISTE  ·  BÉNIN"
        subw = tracking_w(d, sub, fsub2, 3.6)
        draw_tracking(d, (0, fy + 26), sub, fsub2, pal["accent"] + (220,), tr=3.6,
                      anchor_center_x=W/2, shadow=(0, 0, 0, 150))
        fw2, fh2, gap = 27, 18, 16
        for fx in (W/2 - subw/2 - gap - fw2, W/2 + subw/2 + gap):
            mflag = Image.new("L", (fw2, fh2), 0)
            ImageDraw.Draw(mflag).rounded_rectangle([0, 0, fw2, fh2], radius=3, fill=255)
            fl = Image.new("RGBA", (fw2, fh2))
            draw_flag(ImageDraw.Draw(fl), 0, 0, fw2, fh2)
            img.paste(fl, (int(fx), fy + 27), mflag)
        sh_ = max(6, int(H * 0.0065))
        third = int(W / 3)
        d.rectangle([0, H - sh_, third, H], fill=(0, 135, 81))
        d.rectangle([third, H - sh_, W, H - sh_ // 2], fill=(252, 209, 22))
        d.rectangle([third, H - sh_ // 2, W, H], fill=(232, 17, 45))
        grain(img)
        img.convert("RGB").save(out, quality=92, subsampling=0, optimize=True)
        print("✔", out)

if __name__ == "__main__":
    cover(os.path.join(ROOT, "assets/bases/base-cover.jpg"),
          os.path.join(ROOT, "salve-05/cover-post.jpg"),
          os.path.join(ROOT, "salve-05/cover-story.jpg"))
