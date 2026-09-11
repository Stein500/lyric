#!/usr/bin/env python3
"""Teaser autonome 9:16 (~21 s) - PROMPT_UNIVERSEL v4.9.3 §17.
2 images retravaillées IA + Ken Burns + flash cut + cartes annonce/CTA.
Audio: extrait master (refrain 1) avec fade out.
Usage: work/venv/bin/python pipeline/render_teaser.py
"""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
W, H, FPS = 1080, 1920, 30
TOTAL = 21.3
FONT_B = "assets/fonts/DejaVuSans-Bold.ttf"
GOLD = (255, 235, 190); WHITE = (245, 248, 250)
GOLD_SET = {"On est africains oui oui, que tu veuilles ou non!",
            "Blanc de cœur, noir de peau, accepte-toi!"}

def font(sz): return ImageFont.truetype(FONT_B, sz)

def cover(path):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

IMG_A = cover("assets/teaser/t_hook.png")     # 0 -> 9.5
IMG_B = cover("assets/teaser/t_energy.png")   # 9.5 -> end

def kb(img, t, t0, t1, z0, z1, cy=0.52):
    p = min(max((t - t0) / (t1 - t0), 0), 1)
    p = p * p * (3 - 2 * p)
    z = z0 + (z1 - z0) * p
    cw, ch = int(W / z), int(H / z)
    cx = W // 2; cyy = int(H * cy)
    x0 = max(min(cx - cw // 2, W - cw), 0); y0 = max(min(cyy - ch // 2, H - ch), 0)
    return img.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)

def wrap2(txt, f, maxw):
    words = txt.split()
    if f.getlength(txt) <= maxw: return [txt]
    best = None
    for i in range(1, len(words)):
        a = " ".join(words[:i]); b = " ".join(words[i:])
        w = max(f.getlength(a), f.getlength(b))
        if best is None or w < best[0]: best = (w, [a, b])
    return best[1]

# ---- badge ----
def badge_sprite():
    txt = "✓DSKY"; f = font(30); pad = 10
    b = f.getbbox(txt)
    chk = 26
    wtot = chk + 6 + (b[2] - b[0]) + pad * 2
    htot = (b[3] - b[1]) + pad * 2
    im = Image.new("RGBA", (int(wtot) + 4, int(htot) + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=14,
                        fill=(10, 14, 20, 175), outline=(255, 255, 255, 120), width=2)
    cx0, cy0 = pad, (im.height - chk) // 2
    d.rounded_rectangle([cx0, cy0, cx0 + chk, cy0 + chk], radius=6, fill=(250, 200, 60, 255))
    d.text((cx0 + 5, cy0 + 2), "✓", font=font(20), fill=(20, 20, 25, 255))
    d.text((cx0 + chk + 6, 4 + pad - 5), txt, font=f, fill=(240, 248, 252, 255))
    return im
BADGE = badge_sprite()

# ---- stickers CTA (famille coeurs mignons) ----
def cta_sprite():
    lw = font(30)
    stickers = [("like_hearts", "Like"), ("subscribe_cute", "Abonne-toi"), ("comment_cute", "Commente")]
    cells = []
    for f_, l in stickers:
        im = Image.open(f"assets/icons/stickers/{f_}.png").convert("RGBA")
        im = im.resize((120, 120), Image.LANCZOS)
        b = lw.getbbox(l)
        cw2 = max(140, (b[2] - b[0]) + 16)
        cell = Image.new("RGBA", (cw2, 175), (0, 0, 0, 0))
        cell.paste(im, ((cw2 - 120) // 2, 0), im)
        d = ImageDraw.Draw(cell)
        d.text(((cw2 - (b[2] - b[0])) // 2, 140), l, font=lw, fill=(245, 248, 250, 255),
               stroke_width=3, stroke_fill=(5, 8, 12, 230))
        cells.append(cell)
    gap = 34
    wtot = sum(c.width for c in cells) + gap * (len(cells) - 1)
    out = Image.new("RGBA", (wtot, 175), (0, 0, 0, 0))
    x = 0
    for c in cells:
        out.paste(c, (x, 0), c); x += c.width + gap
    return out
CTA = cta_sprite()

# ---- pill BIENTÔT ----
def pill_sprite(txt, fs=46):
    f = font(fs); b = f.getbbox(txt)
    pad_x, pad_y = 46, 18
    im = Image.new("RGBA", (int(b[2] - b[0]) + pad_x * 2, int(b[3] - b[1]) + pad_y * 2 + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=im.height // 2,
                        fill=(255, 196, 60, 235), outline=(255, 255, 255, 200), width=3)
    d.text((pad_x, pad_y - 6), txt, font=f, fill=(25, 18, 5, 255))
    return im
PILL = pill_sprite("BIENTÔT")

def paste_a(base, ov, x, y, a=1.0):
    if a >= 1.0:
        base.paste(ov, (x, y), ov); return
    ov2 = ov.copy()
    ov2.putalpha(ov2.getchannel("A").point(lambda v: int(v * a)))
    base.paste(ov2, (x, y), ov2)

def draw_line(d, txt, y, a=1.0):
    f = font(62)
    rows = wrap2(txt, f, W - 140)
    fill = GOLD if txt in GOLD_SET else WHITE
    for r in rows:
        x = (W - int(f.getlength(r))) // 2
        d.text((x + 5, y + 6), r, font=f, fill=(0, 0, 0, int(200 * a)), stroke_width=4, stroke_fill=(0, 0, 0, int(200 * a)))
        d.text((x, y), r, font=f, fill=(*fill, int(255 * a)), stroke_width=3, stroke_fill=(10, 12, 18, int(230 * a)))
        y += 92

def alpha_ramp(t, a, b):
    if t < a or t >= b: return 0.0
    if t < a + 0.25: return (t - a) / 0.25
    if t > b - 0.3: return max(0.0, (b - t) / 0.3)
    return 1.0

# lignes du refrain 1, offset teaser (t = ts - 35.51)
LINES = [
    (0.00, 6.27, "On est africains oui oui, que tu veuilles ou non!"),
    (6.27, 12.29, "On est africains oui oui, que tu veuilles ou non!"),
    (12.29, 16.32, "Blanc de cœur, noir de peau, accepte-toi!"),
]

def endcard_veil(t):
    return min(max((t - 16.3) / 0.5, 0), 1) * 0.86

def frame(t):
    if t < 9.5:
        im = kb(IMG_A, t, 0, 9.5, 1.02, 1.10).convert("RGBA")
    else:
        im = kb(IMG_B, t, 9.5, TOTAL, 1.12, 1.02).convert("RGBA")
    d = ImageDraw.Draw(im)
    # flash cut à la transition
    if 9.5 <= t < 9.8:
        a = (1 - (t - 9.5) / 0.3) * 0.65
        d.rectangle([0, 0, W, H], fill=(255, 244, 220, int(255 * a)))
    # voile fin lisibilité bas
    g = Image.new("L", (1, H), 0)
    for y in range(int(H * 0.62), H):
        p = (y - H * 0.62) / (H * 0.38)
        g.putpixel((0, y), int(120 * p))
    im.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), g.resize((W, H)))
    d = ImageDraw.Draw(im)
    # lignes synchronisées (jusqu'au voile endcard)
    for a0, b0, txt in LINES:
        al = alpha_ramp(t, a0, b0) * (1 - endcard_veil(t))
        if al > 0:
            draw_line(d, txt, int(H * 0.76), al)
    # pill BIENTÔT sur le hook
    if t < 9.5:
        a = min(t / 0.3, 1) * min((9.5 - t) / 0.3, 1)
        paste_a(im, PILL, (W - PILL.width) // 2, int(H * 0.145), a)
    # endcard: voile + titre + CTA stickers
    ev = endcard_veil(t)
    if ev > 0:
        d.rectangle([0, 0, W, H], fill=(4, 6, 10, int(255 * ev)))
        a = ev
        f1, f2, f3 = font(96), font(56), font(40)
        t1, t2, t3 = "GUERRIER", "Daïsky", "Bientôt disponible"
        for fnt, txt, y, col in ((f1, t1, int(H * 0.36), GOLD),
                                 (f2, t2, int(H * 0.44), WHITE),
                                 (f3, t3, int(H * 0.515), GOLD)):
            x = (W - int(fnt.getlength(txt))) // 2
            d.text((x + 4, y + 5), txt, font=fnt, fill=(0, 0, 0, int(210 * a)))
            d.text((x, y), txt, font=fnt, fill=(*col, int(255 * a)),
                   stroke_width=3, stroke_fill=(10, 12, 18, int(220 * a)))
        paste_a(im, CTA, (W - CTA.width) // 2, int(H * 0.62), a)
    # badge permanent
    paste_a(im, BADGE, (W - BADGE.width) // 2, 24)
    # fade out final
    if t > TOTAL - 0.5:
        a = (t - (TOTAL - 0.5)) / 0.5
        d.rectangle([0, 0, W, H], fill=(0, 0, 0, int(255 * a)))
    return im.convert("RGB")

def main():
    raw = "work/video_teaser_mute.mp4"
    cmd = ["work/bin/ffmpeg", "-y", "-v", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "pipe:0", "-c:v", "libx264", "-preset", "fast", "-crf", "19",
           "-pix_fmt", "yuv420p", raw]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for i in range(n):
        t = i / FPS
        p.stdin.write(frame(t).tobytes())
        if i % 100 == 0: print(f"frame {i}/{n}", flush=True)
    p.stdin.close(); p.wait()
    print("video muette OK ->", raw)
    out = "livrables/Guerrier_teaser_9x16.mp4"
    r = subprocess.run(["work/bin/ffmpeg", "-y", "-v", "error", "-i", raw,
                        "-ss", "35.51", "-i", "work/master_guerrier.mp3",
                        "-af", "afade=t=out:st=19.3:d=1.0",
                        "-map", "0:v", "-map", "1:a", "-t", str(TOTAL),
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out])
    print("FINAL ->", out)
    sys.exit(r.returncode)

if __name__ == "__main__":
    main()
