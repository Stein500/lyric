#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSKY QUOTES — Saison 2 : format STORY uniquement, images 100 % IA (sans photo de l'auteur),
barre CTA (Like · Commente · Partage · Abonne-toi) dessinée proprement sous la signature."""
import json, os, re
from PIL import Image, ImageDraw
from compose import (ROOT, playfair, montserrat, draw_tracking, tracking_w,
                     draw_badge, draw_flag, scrim, grain, fit_text, STYLES)

EMOJI = re.compile(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]+")
ACC = (201, 162, 39)
TXT = (247, 242, 231)

# ---------------------------------------------------------------- icônes CTA
def icon_heart(d, cx, cy, s, col):
    r = s * 0.30
    d.ellipse([cx - s*0.5, cy - s*0.32, cx - s*0.5 + 2*r, cy - s*0.32 + 2*r], fill=col)
    d.ellipse([cx + s*0.5 - 2*r, cy - s*0.32, cx + s*0.5, cy - s*0.32 + 2*r], fill=col)
    d.polygon([(cx - s*0.48, cy + s*0.02), (cx + s*0.48, cy + s*0.02),
               (cx + s*0.10, cy + s*0.50), (cx - s*0.10, cy + s*0.50)], fill=col)

def icon_comment(d, cx, cy, s, col):
    d.rounded_rectangle([cx - s*0.5, cy - s*0.42, cx + s*0.5, cy + s*0.22],
                        radius=int(s*0.22), fill=col)
    d.polygon([(cx - s*0.16, cy + s*0.20), (cx + s*0.06, cy + s*0.20),
               (cx - s*0.24, cy + s*0.50)], fill=col)

def icon_share(d, cx, cy, s, col):
    d.line([cx - s*0.40, cy + s*0.30, cx + s*0.18, cy - s*0.28], fill=col, width=max(3, int(s*0.14)))
    d.polygon([(cx + s*0.42, cy - s*0.44), (cx + s*0.06, cy - s*0.30),
               (cx + s*0.28, cy - s*0.06)], fill=col)
    d.line([cx - s*0.42, cy - s*0.30, cx - s*0.42, cy + s*0.44], fill=col, width=max(3, int(s*0.14)))

def icon_plus(d, cx, cy, s, col):
    w = max(3, int(s*0.16))
    d.line([cx - s*0.36, cy, cx + s*0.36, cy], fill=col, width=w)
    d.line([cx, cy - s*0.36, cx, cy + s*0.36], fill=col, width=w)

# ---------------------------------------------------------------- composition
def compose_s2(item):
    W, H = 1080, 1920
    base = Image.open(os.path.join(ROOT, item["base"])).convert("RGB")
    pal = STYLES[item["style"]]
    img = base.copy()
    r = max(W / img.width, H / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x0 = (img.width - W) // 2
    y0 = max(0, min(int((img.height - H) * 0.42), img.height - H))
    img = img.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
    scrim(img, item["style"], W, H)
    d = ImageDraw.Draw(img)
    acc, txt = pal["accent"], pal["text"]
    m = int(W * 0.075)

    draw_badge(img, m, m, acc)
    fnum = montserrat(26, 700)
    t = f"N° {item['num']}"
    wnum = tracking_w(d, t, fnum, 3)
    draw_tracking(d, (W - m - wnum, m + 14), t, fnum, acc + (255,), tr=3, shadow=(0, 0, 0, 160))

    # citation
    q = EMOJI.sub("", item["text"]).strip()
    f, lines, lh = fit_text(d, q, W - 2 * int(W * 0.085), H * 0.36,
                            lambda s: playfair(s, 600) if item["style"] != "AFRO" else montserrat(s, 600),
                            72, 36)
    total = len(lines) * lh
    y = H * 0.105 + (H * 0.36 - total) / 2
    for ln in lines:
        draw_tracking(d, (0, y), ln, f, txt + (255,), tr=0.4,
                      anchor_center_x=W / 2, shadow=(0, 0, 0, 130))
        y += lh

    # signature
    fy = int(H * 0.908)
    d.rectangle([W/2 - 28, fy - 34, W/2 + 28, fy - 31], fill=acc + (255,))
    fsig = montserrat(25, 700)
    draw_tracking(d, (0, fy - 8), "C. JÉSUTONDJI SAMUEL STEIN", fsig,
                  txt + (235,), tr=3.2, anchor_center_x=W / 2, shadow=(0, 0, 0, 150))
    fsub = montserrat(15, 500)
    sub = "LYRICISTE  ·  BÉNIN"
    subw = tracking_w(d, sub, fsub, 3.6)
    draw_tracking(d, (0, fy + 26), sub, fsub, acc + (220,), tr=3.6,
                  anchor_center_x=W / 2, shadow=(0, 0, 0, 150))
    fw2, fh2, gap = 27, 18, 16
    for fx in (W/2 - subw/2 - gap - fw2, W/2 + subw/2 + gap):
        mflag = Image.new("L", (fw2, fh2), 0)
        ImageDraw.Draw(mflag).rounded_rectangle([0, 0, fw2, fh2], radius=3, fill=255)
        fl = Image.new("RGBA", (fw2, fh2))
        draw_flag(ImageDraw.Draw(fl), 0, 0, fw2, fh2)
        img.paste(fl, (int(fx), fy + 27), mflag)

    # ── barre CTA : Like · Commente · Partage · Abonne-toi ──
    cta = [("LIKE", icon_heart), ("COMMENTE", icon_comment),
           ("PARTAGE", icon_share), ("ABONNE-TOI", icon_plus)]
    fi = montserrat(21, 700)
    tr = 2
    gaps, dotw = 46, 26
    blocks = []
    for word, icon in cta:
        ww = tracking_w(d, word, fi, tr)
        blocks.append((word, icon, ww))
    total_w = sum(24 + 10 + ww for _, _, ww in blocks) + 3 * (dotw + gaps)
    x = W / 2 - total_w / 2
    ycta = H - 128
    for i, (word, icon, ww) in enumerate(blocks):
        icon(d, x + 12, ycta + 12, 24, acc + (255,))
        draw_tracking(d, (x + 24 + 10, ycta), word, fi, txt + (240,), tr=tr,
                      shadow=(0, 0, 0, 140))
        x += 24 + 10 + ww
        if i < 3:
            d.ellipse([x + dotw/2 - 3, ycta + 9, x + dotw/2 + 3, ycta + 15], fill=acc + (255,))
            x += dotw + gaps

    # liseré béninois
    sh_ = max(6, int(H * 0.0065))
    third = int(W / 3)
    d.rectangle([0, H - sh_, third, H], fill=(0, 135, 81))
    d.rectangle([third, H - sh_, W, H - sh_ // 2], fill=(252, 209, 22))
    d.rectangle([third, H - sh_ // 2, W, H], fill=(232, 17, 45))
    grain(img)
    out = os.path.join(ROOT, f"saison-02/story/quote-{item['num']}-story.jpg")
    img.convert("RGB").save(out, quality=92, subsampling=0, optimize=True)
    print("✔", f"quote-{item['num']}-story.jpg", f"[{item['style']}]")

def main():
    os.makedirs(os.path.join(ROOT, "saison-02/story"), exist_ok=True)
    meta = json.load(open(os.path.join(ROOT, "saison-02.json"), encoding="utf-8"))
    for item in meta:
        compose_s2(item)

if __name__ == "__main__":
    main()
