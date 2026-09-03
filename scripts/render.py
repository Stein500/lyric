#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOTEUR DE RENDU 9:16 — SOLUTION A (v4.7 §0/§8/§9) + ADDENDUM v4.8.
Flux continu frame-accurate : frame i <=> t = i/FPS, 0 accumulation d'erreur.
- fonds pré-calculés canvas Ken Burns 1,1x -> work/fonds_portrait/
- texte par fenêtres [t0-ADV, t1-ADV) ; fonds sur horloge musique
- vague 6 px / 0,9 Hz + apparition staggered 0,9 s + cascade inversée
- Ken Burns zoom 1,02->1,08 + pan sinus ; badge STATIQUE posé en dernier
- intro titre Great Vibes (0->9 s) · « Merci » 245->253,9 · endcard 254->266
Usage : .venv/bin/python scripts/render.py [smoke|full]
Script TRACKÉ (scripts/) : survit aux resets.
"""
import csv
import glob
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS = 30
W, H = 1080, 1920
CW, CH = 1188, 2112
ADV = 0.03
AUDIO_DUR = 261.04
ENDCARD_AT = 254.0
TOTAL = 266.0
MERCI = (245.0, 253.9)
FIRST_VOICE = 9.0
DEJ = "/usr/share/fonts/truetype/dejavu/"
GREAT = "fonts/GreatVibes-Regular.ttf"
CYAN = (77, 210, 255)
AMBER = (232, 163, 61)
BLANC = (245, 249, 255)
CASSE = (235, 235, 225)
PAD = 14

FR = {
    "Yeah... I'm poor but I'm rich...": "Ouais… je suis pauvre mais je suis riche…",
    "I got no money, but I got soul": "J'ai pas d'argent, mais j'ai une âme",
    "I got no gold, but I got control": "J'ai pas d'or, mais j'ai le contrôle",
    "I'm arrogant, I'm proud, I'm too much": "Je suis arrogant, je suis fier, je suis trop",
    "But I love my people, I love my touch": "Mais j'aime les miens, j'aime ma touche",
    "Nihon go, español, français, fon": "Japonais, espagnol, français, fon",
}

STYLE = {
    "intro": (58, BLANC, True, False),
    "verse": (58, BLANC, True, False),
    "pre": (58, CYAN, True, False),
    "hook": (58, CYAN, True, False),
    "hook_final": (64, AMBER, True, False),
    "bridge": (50, (178, 232, 255), False, True),
    "wolof": (64, AMBER, True, False),
    "outro": (58, AMBER, True, True),
}


def load():
    vers = list(csv.DictReader(open("work/timing.csv", encoding="utf-8")))
    for r in vers:
        r["slot"] = int(r["slot"]); r["start"] = float(r["start"]); r["end"] = float(r["end"])
    mp = {}
    for r in csv.DictReader(open("scripts/slot_map.csv", encoding="utf-8")):
        mp[int(r["slot"])] = r["image"]
    return vers, mp


def img_for_slot(slot):
    g = sorted(glob.glob("assets/raw/portrait/s%02d_*.png" % slot))
    if not g:
        raise SystemExit("IMAGE MANQUANTE slot %d" % slot)
    return g[0]


def make_fonds(mp):
    os.makedirs("work/fonds_portrait", exist_ok=True)
    done = 0
    for slot in range(0, 64):
        out = "work/fonds_portrait/f%02d.jpg" % slot
        if os.path.exists(out):
            continue
        src = img_for_slot(int(mp[slot][1:]))   # v4.8 : slot réutilisé -> image mappée
        im = Image.open(src).convert("RGB").resize((CW, CH), Image.LANCZOS)
        im.save(out, quality=92)
        done += 1
    print("fonds pré-calculés :", done)


def build_badge():
    f_lab = ImageFont.truetype(DEJ + "DejaVuSans-Bold.ttf", 34)
    f_hdl = ImageFont.truetype(DEJ + "DejaVuSans.ttf", 24)
    lab, hdl = "DAÏSKY PROD", "@daiskypro"
    pad_x, pad_y, gap = 22, 16, 42
    tw = max(f_lab.getlength(lab), f_hdl.getlength(hdl))
    bw, bh = int(tw + pad_x * 2 + gap), int(pad_y * 2 + 34 + 24 + 6)
    layer = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=bh // 2,
                        fill=(5, 6, 10, 165), outline=CYAN + (235,), width=3)
    s = 52
    cx, cy = pad_x + gap / 2, bh / 2
    d.polygon([(cx + 0.10 * s, cy - 0.50 * s), (cx - 0.28 * s, cy + 0.06 * s),
               (cx - 0.02 * s, cy + 0.06 * s), (cx - 0.12 * s, cy + 0.50 * s),
               (cx + 0.30 * s, cy - 0.10 * s), (cx + 0.02 * s, cy - 0.10 * s)],
              fill=AMBER + (255,))
    tx = pad_x + gap
    d.text((tx, pad_y - 2), lab, font=f_lab, fill=BLANC + (255,))
    d.text((tx, pad_y + 36), hdl, font=f_hdl, fill=CYAN + (235,))
    return layer


def skew(im):
    return im.transform((int(im.width * 1.18), im.height), Image.AFFINE,
                        (1, 0.18, -0.18 * im.height, 0, 1, 0),
                        resample=Image.BICUBIC)


def wrap(text, font, max_w, d):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def letter_sprites(text, font, color, italic):
    sprites = []
    for ch in text:
        x0, y0, x1, y1 = font.getbbox(ch)
        adv = max(1, x1 - x0)
        if ch == " ":
            adv = int(font.getlength(" "))
        w = adv + 2 * PAD
        h = font.size + 2 * PAD
        sp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sp)
        sd.text((PAD - x0, PAD - y0), ch, font=font, fill=color + (255,))
        glow = sp.filter(ImageFilter.GaussianBlur(6))
        sp = Image.alpha_composite(glow, sp)
        if italic:
            sp = skew(sp)
        sprites.append((ch, sp, adv))
    return sprites


class VerseBlock:
    def __init__(self, text, style, fr=None):
        size, color, bold, italic = STYLE[style]
        path = DEJ + ("DejaVuSans-Bold.ttf" if bold else
                      ("DejaVuSerif.ttf" if italic else "DejaVuSans.ttf"))
        self.font = ImageFont.truetype(path, size)
        d = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
        self.lines = wrap(text, self.font, 920, d)
        self.sprites = [letter_sprites(ln, self.font, color, italic) for ln in self.lines]
        self.line_h = int(size * 1.28)
        self.fr = None
        if fr:
            ff = ImageFont.truetype(DEJ + "DejaVuSerif.ttf", 34)
            self.fr = letter_sprites(fr, ff, CASSE, True)


def draw_block(frame, block, t, t0, t1):
    n_total = sum(len(s) for s in block.sprites)
    stag = 0.9 / max(1, n_total)
    idx = 0
    y = H - 300 - block.line_h * (len(block.sprites) - 1)
    for line in block.sprites:
        lw = sum(adv for _, _, adv in line)
        x = (W - lw) / 2
        for ch, sp, adv in line:
            a_in = min(1.0, max(0.0, (t - (t0 + idx * stag)) / 0.18))
            a_out = min(1.0, max(0.0, ((t1 - 0.05 - (n_total - 1 - idx) * stag * 0.6) - t) / 0.15))
            a = min(a_in, a_out)
            if a > 0.01:
                wave = 6 * math.sin(2 * math.pi * 0.9 * t + idx * 0.35)
                rise = (1 - a_in) * 30
                yy = int(y + wave + rise)
                if 0 < a < 1:
                    sp2 = sp.copy()
                    sp2.putalpha(sp2.getchannel("A").point(lambda v: int(v * a)))
                    frame.paste(sp2, (int(x - PAD), yy - PAD), sp2)
                else:
                    frame.paste(sp, (int(x - PAD), yy - PAD), sp)
            x += adv
            idx += 1
        y += block.line_h
    if block.fr:
        lw = sum(adv for _, _, adv in block.fr)
        x = (W - lw) / 2
        yfr = H - 300 + 24
        for ch, sp, adv in block.fr:
            frame.paste(sp, (int(x - PAD), yfr - PAD), sp)
            x += adv


def kb_crop(slot, t):
    z = 1.02 + 0.06 * (0.5 + 0.5 * math.sin(t * 0.25 + slot))
    cw, chh = W / z, H / z
    px = 20 * math.sin(2 * math.pi * t / 17.0)
    py = 14 * math.cos(2 * math.pi * t / 23.0)
    cx, cy = CW / 2 + px, CH / 2 + py
    x0 = int(max(0, min(CW - cw, cx - cw / 2)))
    y0 = int(max(0, min(CH - chh, cy - chh / 2)))
    return (x0, y0, x0 + int(cw), y0 + int(chh))


def titre_intro(frame, t):
    a = min(1, t / 0.6) * min(1, (FIRST_VOICE - 0.4 - t) / 0.5) if t < FIRST_VOICE else 0
    if a <= 0:
        return
    f = ImageFont.truetype(GREAT, 120)
    txt = "Je suis pauvre mais je kiffe"
    d = ImageDraw.Draw(frame)
    lw = d.textlength(txt, font=f)
    sp = Image.new("RGBA", (int(lw) + 80, 220), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sp)
    sd.text((40, 40), txt, font=f, fill=AMBER + (255,))
    glow = sp.filter(ImageFilter.GaussianBlur(10))
    sp = Image.alpha_composite(glow, sp)
    sp.putalpha(sp.getchannel("A").point(lambda v: int(v * a)))
    frame.paste(sp, ((W - sp.width) // 2, int(H * 0.40)), sp)
    f2 = ImageFont.truetype(DEJ + "DejaVuSans-Bold.ttf", 44)
    d = ImageDraw.Draw(frame)
    d.text((W / 2 - d.textlength("Daïsky", font=f2) / 2, int(H * 0.40) + 190),
           "Daïsky", font=f2, fill=BLANC + (int(255 * a),))


def merci(frame, t):
    a = min(1, (t - MERCI[0]) / 0.5) * min(1, (MERCI[1] - t) / 0.5)
    if a <= 0:
        return
    f = ImageFont.truetype(GREAT, 150)
    sp = Image.new("RGBA", (700, 260), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sp)
    sd.text((40, 40), "Merci", font=f, fill=AMBER + (255,))
    glow = sp.filter(ImageFilter.GaussianBlur(10))
    sp = Image.alpha_composite(glow, sp)
    sp.putalpha(sp.getchannel("A").point(lambda v: int(v * a)))
    frame.paste(sp, ((W - sp.width) // 2, H - 560), sp)
    f2 = ImageFont.truetype(DEJ + "DejaVuSans.ttf", 36)
    d = ImageDraw.Draw(frame)
    line = "@daiskypro · Daïsky Prod"
    d.text((W / 2 - d.textlength(line, font=f2) / 2, H - 320),
           line, font=f2, fill=CYAN + (int(235 * a),))


def endcard(frame, t):
    a = min(1, (t - ENDCARD_AT) / 1.0)
    if a <= 0:
        return
    d = ImageDraw.Draw(frame)
    cx = W / 2
    f1 = ImageFont.truetype(GREAT, 100)
    f2 = ImageFont.truetype(DEJ + "DejaVuSans-Bold.ttf", 46)
    f3 = ImageFont.truetype(DEJ + "DejaVuSans.ttf", 32)
    y = 620
    for txt, f, col in [("Je suis pauvre mais je kiffe", f1, AMBER),
                        ("Daïsky", f2, BLANC),
                        ("Daïsky Prod / TechStein · Afro-Rock / World · 2026", f3, CASSE),
                        ("@daiskypro", f3, CYAN),
                        ("« Wolof TechStein beat wê ! »", f3, AMBER),
                        ("229 01 61 16 24 08 · 229 01 49 11 49 51", f3, CASSE),
                        ("daiskypro@proton.me", f3, CASSE)]:
        d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f,
               fill=col + (int(255 * a),))
        y += f.size + 34


def slot_at(vers, t):
    cur = 0
    for r in vers:
        if t >= r["start"]:
            cur = r["slot"]
        else:
            break
    return cur


def text_window(vers, t):
    for r in vers:
        if r["start"] - ADV <= t < r["end"] - ADV:
            return r
    return None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    vers, mp = load()
    make_fonds(mp)
    badge = build_badge()
    cache = {}

    def fond(slot):
        if slot not in cache:
            cache[slot] = Image.open("work/fonds_portrait/f%02d.jpg" % slot).convert("RGB")
        return cache[slot]

    blocks = {r["slot"]: VerseBlock(r["text"], r["style"], FR.get(r["text"])) for r in vers}

    def frame_at(t):
        if t >= ENDCARD_AT:
            slot = 63
        elif t >= MERCI[0]:
            slot = 62
        else:
            slot = slot_at(vers, t)
        base = fond(slot).crop(kb_crop(slot, t)).resize((W, H), Image.LANCZOS)
        frame = base.convert("RGBA")
        if t < FIRST_VOICE:
            titre_intro(frame, t)
        r = text_window(vers, t)
        if r:
            draw_block(frame, blocks[r["slot"]], t, r["start"] - ADV, r["end"] - ADV)
        if MERCI[0] <= t < MERCI[1]:
            merci(frame, t)
        if t >= ENDCARD_AT:
            endcard(frame, t)
        frame.paste(badge, (36, 36), badge)
        return frame.convert("RGB")

    if mode == "smoke":
        os.makedirs("work/smoke", exist_ok=True)
        for t in (2.0, 20.0, 185.0, 246.5, 264.0):
            frame_at(t).save("work/smoke/f_%06.1f.png" % t)
            print("smoke t=%.1f ok" % t)
        return

    out = "work/video_sans_audio.mp4"
    cmd = ["work/ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
           "-pix_fmt", "yuv420p", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = math.ceil(TOTAL * FPS)
    for i in range(n):
        p.stdin.write(frame_at(i / FPS).tobytes())
        if i % 600 == 0:
            print("frame %d/%d (t=%.1f)" % (i, n, i / FPS), flush=True)
    p.stdin.close()
    p.wait()
    print("RENDU_TERMINE exit=%d -> %s" % (p.returncode, out))


if __name__ == "__main__":
    main()
