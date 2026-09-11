#!/usr/bin/env python3
"""Guerrier — rendu lyrics SOLUTION A (flux continu frame-accurate, §0/§9)."""
import json, math, re, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FMT = sys.argv[1]          # portrait | landscape
STYLE = sys.argv[2]        # v2 | cursive
FF = "work/bin/ffmpeg"
FPS = 30
SONG = 206.40
TOTAL = 211.40
ES = 205.9                 # endcard start
ADV = 0.03
W, H = (1080, 1920) if FMT == "portrait" else (1920, 1080)
CW, CH = int(W*1.1), int(H*1.1)
FONT_B = "assets/fonts/DejaVuSans-Bold.ttf"
FONT_S = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
GOLD = (255, 235, 190); WHITE = (245, 248, 250)

def font(sz): return ImageFont.truetype(FONT_B, sz)

# ---------------- paroles ----------------
raw = [l for l in open("guerrier.txt", encoding="utf-8") if l.strip()]
lines = []
for ln in raw:
    m = re.match(r"\[(\d+):(\d+\.\d+)\](.*)", ln)
    t = int(m.group(1))*60 + float(m.group(2))
    txt = m.group(3).strip()
    for p in ("(fort)", "(cri de guerre)", "(crié)"):
        txt = txt.replace(p, "")
    txt = re.sub(r",\s*", ", ", txt.strip())
    lines.append([t, txt])
GOLD_SET = {"Wolof TechStein beat wê!", "On est africains oui oui, que tu veuilles ou non!",
            "Blanc de cœur, noir de peau, accepte-toi!", "On avance, plus peur, finis les combats!"}
windows = []
for i, (t, txt) in enumerate(lines):
    d0 = t - ADV
    d1 = min(lines[i+1][0], t + 5.0) if i + 1 < len(lines) else t + 6.0
    windows.append((d0, d1, txt))

slotmap = json.load(open("pipeline/slots_guerrier.json"))
SLOTS = ["s00_intro","s01_tag_intro","s02_africains","s03_blanc_coeur","s04_on_avance","s05_tag_cri1",
 "s06_epoque","s07_envahisseurs","s08_pleure","s09_renaitre","s10_oublions","s11_debout","s12_reines",
 "s13_ancetres","s14_tag_cri2","s15_arretons","s16_racines","s17_bamako","s18_accepte_toi","s19_traverse","s20_endcard"]
TXT2SLOT = {}
for ln in raw:
    m = re.match(r"\[(\d+):(\d+\.\d+)\](.*)", ln)
    t = round(int(m.group(1))*60 + float(m.group(2)), 2)
    for tt, s in slotmap["vers"]:
        if abs(tt - t) < 0.01:
            txt = m.group(3).strip()
            for p in ("(fort)", "(cri de guerre)", "(crié)"):
                txt = txt.replace(p, "")
            TXT2SLOT[re.sub(r",\s*", ", ", txt.strip())] = s
def bg_index(txt):
    if txt in TXT2SLOT:
        return SLOTS.index(TXT2SLOT[txt])
    return SLOTS.index("s19_traverse")

# ---------------- fonds ----------------
fonds = {}
def fond(i):
    if i not in fonds:
        fonds[i] = Image.open(f"work/fonds_{FMT}/f{i:02d}.jpg").convert("RGB")
    return fonds[i]

def kenburns(i, t, t0, t1, span_id):
    cv = fond(i)
    dur = max(t1 - t0, 0.5)
    u = min(max((t - t0) / dur, 0), 1)
    z = 1.02 + 0.06 * (u if span_id % 2 == 0 else 1 - u)
    cw, ch = CW / z, CH / z
    px = 8 * math.sin(2*math.pi*t/13.0) + (CW - cw)/2
    py = 6 * math.sin(2*math.pi*t/17.0) + (CH - ch)/2
    px = min(max(px, 0), CW - cw); py = min(max(py, 0), CH - ch)
    return cv.crop((int(px), int(py), int(px)+int(cw), int(py)+int(ch))).resize((W, H), Image.LANCZOS)

# ---------------- sprites texte ----------------
def sheared(im, sh=0.22):
    return im.transform((im.width + int(im.height*sh), im.height), Image.AFFINE,
                        (1, sh, 0, 0, 1, 0), resample=Image.BICUBIC)

def make_letter(ch, size, cursive, fill):
    pad = int(size*0.8)
    f = ImageFont.truetype(FONT_S if cursive else FONT_B, size)
    im = Image.new("RGBA", (int(size*1.4)+pad*2, int(size*1.9)+pad*2), (0,0,0,0))
    d = ImageDraw.Draw(im)
    d.text((pad, pad), ch, font=f, fill=fill,
           stroke_width=2 if cursive else 3, stroke_fill=(8,12,18,255))
    sh = Image.new("RGBA", im.size, (0,0,0,0)); sd = ImageDraw.Draw(sh)
    sd.text((pad+4, pad+4), ch, font=f, fill=(0,0,0,190),
            stroke_width=2 if cursive else 3, stroke_fill=(0,0,0,190))
    im = Image.alpha_composite(sh, im)
    if cursive:
        glow = im.filter(ImageFilter.GaussianBlur(6))
        im = Image.alpha_composite(glow, im)
        im = sheared(im)
    return im, f

def build_line(txt, cursive):
    size = 80 if cursive else (58 if FMT == "portrait" else 62)
    maxw = 920 if FMT == "portrait" else 1640
    fill = GOLD if txt in GOLD_SET else WHITE
    f = ImageFont.truetype(FONT_S if cursive else FONT_B, size)
    seqs = [txt]
    if f.getlength(txt) > maxw:
        words = txt.split(); best = None
        for i in range(1, len(words)):
            l1, l2 = " ".join(words[:i]), " ".join(words[i:])
            s = max(f.getlength(l1), f.getlength(l2))
            if best is None or s < best[0]: best = (s, [l1, l2])
        seqs = best[1]
    out = []
    for seq in seqs:
        letters = []
        for ch in seq:
            if ch == " ":
                letters.append((None, f.getlength(" ")))
                continue
            im, _ = make_letter(ch, size, cursive, fill)
            letters.append((im, f.getlength(ch)))
        out.append(letters)
    return out, size

LINE_CACHE = {}
def line_sprites(txt):
    key = (txt, STYLE)
    if key not in LINE_CACHE:
        LINE_CACHE[key] = build_line(txt, STYLE == "cursive")
    return LINE_CACHE[key]

def line_width(letters): return sum(a for _, a in letters)

LUM_CACHE = {}
def banner_alpha(slot_i):
    if slot_i not in LUM_CACHE:
        g = fond(slot_i).convert("L")
        y0 = int(CH*0.78)
        zone = np.array(g.crop((int(CW*0.1), y0, int(CW*0.9), min(CH, y0+int(CH*0.16)))))
        LUM_CACHE[slot_i] = zone.mean()/255
    return 0.68 if LUM_CACHE[slot_i] > 0.30 else 0.45

# ---------------- overlays ----------------
def badge_sprite():
    bfont = font(30 if FMT == "portrait" else 34)
    txt = "DSKY"
    bb = bfont.getbbox(txt)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    chk, pad = 30, 16
    bw, bh = tw + chk + pad*3 - 8, th + pad*2 - 6
    im = Image.new("RGBA", (bw+8, bh+8), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, 4+bw, 4+bh], radius=14, fill=(5,8,12,178), outline=(77,210,255,200), width=2)
    cx0, cym = 4+pad, 4+bh//2
    d.line([(cx0, cym+1), (cx0+8, cym+9), (cx0+22, cym-9)], fill=(232,163,61,255), width=5)
    d.text((cx0+chk, 4+pad-5), txt, font=bfont, fill=(240,248,252,255))
    return im

def cta_sprite():
    lw = font(30)
    stickers = [("like_hearts","Like"), ("subscribe_cute","Abonne-toi"), ("comment_cute","Commente")]
    cols = []
    for f_, l in stickers:
        im = Image.open(f"assets/icons/stickers/{f_}.png")
        im.thumbnail((130,130), Image.LANCZOS)
        b = lw.getbbox(l)
        cols.append((im, l, max(im.size[0], b[2]-b[0]), b))
    gap = 46
    total = sum(c[2] for c in cols) + gap*2
    im = Image.new("RGBA", (total, 240), (0,0,0,0)); d = ImageDraw.Draw(im)
    x = 0
    for st, l, cw2, b in cols:
        im.paste(st, (x + (cw2-st.size[0])//2, 0), st)
        d.text((x + (cw2-(b[2]-b[0]))//2, 140), l, font=lw, fill=(245,248,250,255),
               stroke_width=3, stroke_fill=(5,8,12,230))
        x += cw2 + gap
    return im

def share_sprite():
    st = Image.open("assets/icons/stickers/share_cute.png")
    st.thumbnail((190,190), Image.LANCZOS)
    f2 = font(34)
    lab = "Partage"
    b = f2.getbbox(lab)
    aw = 40
    wtot = max(st.size[0], b[2]-b[0]+aw)
    im = Image.new("RGBA", (wtot+20, st.size[1]+80), (0,0,0,0)); d = ImageDraw.Draw(im)
    im.paste(st, ((wtot-st.size[0])//2, 0), st)
    y = st.size[1]+8
    d.text(((wtot-(b[2]-b[0]))//2, y), lab, font=f2, fill=(245,248,250,255), stroke_width=3, stroke_fill=(5,8,12,230))
    ax = (wtot+(b[2]-b[0]))//2 + 8
    d.line([(ax, y+30), (ax+22, y+8), (ax+22, y+20)], fill=(232,163,61,255), width=5)
    d.line([(ax+22, y+8), (ax+10, y+20)], fill=(232,163,61,255), width=5)
    return im

def intro_sprite(cursive):
    f1 = ImageFont.truetype(FONT_S if cursive else FONT_B, 120)
    f2 = font(58)
    t1, t2 = "GUERRIER", "Daïsky"
    w1, w2 = f1.getlength(t1), f2.getlength(t2)
    wtot = max(w1, w2)
    im = Image.new("RGBA", (int(wtot)+160, 300), (0,0,0,0)); d = ImageDraw.Draw(im)
    if cursive:
        tmp = Image.new("RGBA", (int(w1)+160, 200), (0,0,0,0)); td = ImageDraw.Draw(tmp)
        td.text((80, 20), t1, font=f1, fill=GOLD, stroke_width=2, stroke_fill=(8,12,18,255))
        tmp = sheared(tmp, 0.18)
        im.paste(tmp, (0, 0), tmp)
    else:
        d.text(((int(wtot)-int(w1))//2, 20), t1, font=f1, fill=GOLD, stroke_width=3, stroke_fill=(8,12,18,255))
    d.text(((int(wtot)-int(w2))//2, 190), t2, font=f2, fill=WHITE, stroke_width=3, stroke_fill=(8,12,18,255))
    return im

def endcard_sprite(cursive):
    ft = ImageFont.truetype(FONT_S if cursive else FONT_B, 110)
    f3, f4 = font(44), font(34)
    rows = [("GUERRIER", ft, GOLD), ("Daïsky", f3, WHITE),
            ("Daïsky Prod / TechStein · Afro-Rock / World · 2026", f4, WHITE),
            ("@daiskypro", f4, (120,220,255,255)),
            ("Tel: 229 01 61 16 24 08 · 229 01 49 11 49 51", f4, WHITE),
            ("daiskypro@proton.me", f4, WHITE),
            ("« Wolof TechStein beat wê ! »", f4, GOLD)]
    wtot = max(f.getlength(t) for t, f, _ in rows)
    htot = sum(f.size for _, f, _ in rows) + 40*len(rows)
    im = Image.new("RGBA", (int(wtot)+160, int(htot)+80), (0,0,0,0)); d = ImageDraw.Draw(im)
    y = 20
    for t, f, c in rows:
        wl = f.getlength(t)
        if cursive and t == "GUERRIER":
            tmp = Image.new("RGBA", (int(wl)+160, 200), (0,0,0,0)); td = ImageDraw.Draw(tmp)
            td.text((80, 20), t, font=f, fill=c, stroke_width=2, stroke_fill=(8,12,18,255))
            tmp = sheared(tmp, 0.18)
            im.paste(tmp, ((im.width-tmp.size[0])//2, y-20), tmp)
        else:
            d.text(((int(wtot)-int(wl))//2, y), t, font=f, fill=c, stroke_width=3, stroke_fill=(5,8,12,230))
        y += f.size + 40
    return im

BADGE = badge_sprite(); CTA = cta_sprite(); SHARE = share_sprite()
INTRO = intro_sprite(STYLE == "cursive"); ENDC = endcard_sprite(STYLE == "cursive")

# ---------------- boucle frames ----------------
NB = math.ceil(TOTAL * FPS)
out_video = f"work/video_{FMT}_{STYLE}.mp4"
enc = subprocess.Popen([FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-vf", f"fade=t=out:st={TOTAL-3}:d=3",
    "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", out_video],
    stdin=subprocess.PIPE)

def alpha_ramp(t, a, b):
    return min(max((t - a) / (b - a), 0.0), 1.0)

for i in range(NB):
    t = i / FPS
    if t < ES:
        if t < windows[0][0]:
            si, t0, t1 = 0, 0.0, windows[0][0]
        else:
            si = t0 = t1 = None
            for (d0, d1, txt) in windows:
                if d0 <= t < d1:
                    si, t0, t1 = bg_index(txt), d0, d1
                    break
            if si is None:
                prev = [w for w in windows if w[0] <= t]
                d0, d1, txt = prev[-1]
                nxt = [w for w in windows if w[0] > t]
                si, t0, t1 = bg_index(txt), d0, (nxt[0][0] if nxt else ES)
        frame = kenburns(si, t, t0, t1, si)
    else:
        frame = kenburns(SLOTS.index("s20_endcard"), t, ES, TOTAL, 1)
    img = frame.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(ov)

    active = None
    for (d0, d1, txt) in windows:
        if d0 <= t < d1 and t < ES:
            active = (d0, d1, txt); break
    if active:
        d0, d1, txt = active
        letters, size = line_sprites(txt)
        lh = int(size * 1.35)
        heights = len(letters)*lh
        ybase = (H - 300) if FMT == "portrait" else (H - 150)
        ytop = ybase - heights
        bw = max(line_width(L) for L in letters)
        a = banner_alpha(bg_index(txt))
        padb = int(size*0.4)
        d.rounded_rectangle([(W-bw)//2 - padb, ytop - 24, (W+bw)//2 + padb, ybase + 20],
                            radius=26, fill=(8,14,20,int(255*a)))
        n_tot = sum(len(L) for L in letters)
        idx = 0
        for li, L in enumerate(letters):
            lw2 = line_width(L)
            x = (W - lw2)/2
            for (sp, adv) in L:
                ta = d0 + 0.9 * idx / max(n_tot-1, 1)
                tb = d1 - 0.6 * (n_tot-1-idx) / max(n_tot-1, 1)
                al = alpha_ramp(t, ta, ta+0.25) * (1 - alpha_ramp(t, tb, tb+0.25))
                if sp is not None and al > 0.01:
                    yo = 6*math.sin(2*math.pi*0.9*t + idx*0.55) + (1-al)*30
                    sp2 = sp.copy()
                    if al < 0.99:
                        r, g, b, aa = sp2.split()
                        aa = aa.point(lambda v: int(v*al))
                        sp2 = Image.merge("RGBA", (r, g, b, aa))
                    ov.paste(sp2, (int(x - sp2.width*0.18), int(ytop + li*lh - sp2.height*0.28 + yo)), sp2)
                x += adv
                idx += 1

    if t < 2.71:
        al = alpha_ramp(t, 0.1, 0.5) * (1 - alpha_ramp(t, 2.31, 2.71))
        r, g, b, aa = INTRO.split(); aa = aa.point(lambda v: int(v*al))
        im2 = Image.merge("RGBA", (r, g, b, aa))
        y = int(H*0.40) if FMT == "portrait" else int(H*0.30)
        ov.paste(im2, ((W-im2.size[0])//2, y), im2)

    if t >= ES:
        al = alpha_ramp(t, ES, ES+0.8)
        d.rectangle([0, 0, W, H], fill=(4,6,10,int(140*al)))
        r, g, b, aa = ENDC.split(); aa = aa.point(lambda v: int(v*al))
        im2 = Image.merge("RGBA", (r, g, b, aa))
        cx = W//2 if FMT == "portrait" else int(W*0.38)
        y = (H - im2.size[1])//2
        ov.paste(im2, (cx - im2.size[0]//2, y), im2)

    if t < 2.4:
        al = alpha_ramp(t, 0.0, 0.3) * (1 - alpha_ramp(t, 2.0, 2.4))
        r, g, b, aa = CTA.split(); aa = aa.point(lambda v: int(v*al))
        im2 = Image.merge("RGBA", (r, g, b, aa))
        y = int(H*0.335) if FMT == "portrait" else H - 300
        ov.paste(im2, ((W-im2.size[0])//2, y), im2)

    if 101.7 <= t <= 104.7:
        al = alpha_ramp(t, 101.7, 102.1) * (1 - alpha_ramp(t, 104.3, 104.7))
        sc = 1 + 0.06*math.sin(2*math.pi*0.9*t)
        st = SHARE.resize((int(SHARE.width*sc), int(SHARE.height*sc)), Image.LANCZOS)
        r, g, b, aa = st.split(); aa = aa.point(lambda v: int(v*al))
        im2 = Image.merge("RGBA", (r, g, b, aa))
        y = int(H*0.42) if FMT == "portrait" else int(H*0.30)
        ov.paste(im2, ((W-im2.size[0])//2, y), im2)

    ov.paste(BADGE, ((W-BADGE.size[0])//2, 30), BADGE)

    img = Image.alpha_composite(img, ov)
    enc.stdin.write(img.convert("RGB").tobytes())
    if i % 600 == 0:
        print(f"frame {i}/{NB} t={t:.1f}", flush=True)

enc.stdin.close(); enc.wait()
print("video muette OK ->", out_video)

out_final = f"livrables/Guerrier_9x16_{STYLE}.mp4" if FMT == "portrait" else f"livrables/Guerrier_16x9_YT_{STYLE}.mp4"
os.makedirs("livrables", exist_ok=True)
subprocess.run([FF, "-y", "-v", "error", "-i", out_video, "-i", "work/master_guerrier.mp3",
    "-map", "0:v:0", "-map", "1:a:0",
    "-af", f"apad=whole_dur={TOTAL},afade=t=out:st={TOTAL-3}:d=3",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(TOTAL),
    "-movflags", "+faststart", out_final], check=True)
print("FINAL ->", out_final)
