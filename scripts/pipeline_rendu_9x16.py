#!/usr/bin/env python3
"""PIPELINE RENDU 9:16 — v4.9 (cold-open 6 s = MOMENT FORT en tête, DSKY✓ milieu haut,
CTA 2 s bas centré, icône partage milieu, cursive GreatVibes + vague eau, SOLUTION A
frame-accurate). VERSION VERSIONNÉE (règle v4.9 §4 : scripts dans scripts/, work/ = cache).
Usage (depuis la racine repo):
  python scripts/pipeline_rendu_9x16.py fonds            # pré-calcul fonds Ken Burns
  python scripts/pipeline_rendu_9x16.py audio            # work/audio_video.wav (hook+song, loudnorm 2p)
  python scripts/pipeline_rendu_9x16.py render <f0> <f1> <out.mp4>
  python scripts/pipeline_rendu_9x16.py mux <video> <out> # mux audio + fades (ré-encode crf21)
Constantes: FPS=30, HOOK=6.0, ADVANCE=0.03, TOTAL=HOOK+210.02+5=221.02, NF=6631.
"""
import json, math, os, subprocess, sys, io
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

FF = "work/ffmpeg"
FPS = 30
W, H = 1080, 1920
CW, CH = 1188, 2112                      # canvas Ken Burns 1,1x
HOOK = 6.0                               # cold-open = moment fort (refrain explosif)
ADV = 0.03
SONG = 210.02
SONG_END = HOOK + SONG
TOTAL = SONG_END + 5.0
NF = math.ceil(TOTAL * FPS)
GV = "assets/fonts/GreatVibes-Regular.ttf"
DV = "assets/fonts/DejaVuSans-Bold.ttf"
CYAN = (0, 225, 255)

# ---------------------------------------------------------------- données
def load():
    d = json.load(open("work/timings_validated.json"))
    vers = d["verses"]
    slot_of, order = {}, []
    for v in vers:
        k = v["text"].lower()
        if k not in slot_of:
            slot_of[k] = len(order) + 1
            order.append(v["text"])
    occ = []
    for i, v in enumerate(vers):
        t0 = v["t0"] + HOOK
        t1 = (vers[i + 1]["t0"] + HOOK) if i + 1 < len(vers) else SONG_END
        occ.append({"text": v["text"], "slot": slot_of[v["text"].lower()],
                    "t0": t0, "t1": t1})
    return occ, order

OCC, ORDER = load()
NUNI = len(ORDER)                          # 38
SLOT_ENDCARD = NUNI + 1                    # s39

# ---------------------------------------------------------------- sprites
_cache = {}
def cursive_sprite(text, size=76, maxw=940):
    key = ("c", text, size)
    if key in _cache:
        return _cache[key]
    font = ImageFont.truetype(GV, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    lines = [text]
    w = tmp.textbbox((0, 0), text, font=font)[2]
    if w > maxw:                             # §14: réduction puis retour à ligne
        words = text.split()
        best, bw = None, 10 ** 9
        for i in range(1, len(words)):
            a, b = " ".join(words[:i]), " ".join(words[i:])
            ww = max(tmp.textbbox((0, 0), a, font=font)[2],
                     tmp.textbbox((0, 0), b, font=font)[2])
            if ww < bw:
                bw, best = ww, (a, b)
        lines = list(best)
    pads = [ImageDraw.Draw(Image.new("RGBA", (8, 8))).textbbox((0, 0), ln, font=font)
            for ln in lines]
    lw = max(p[2] - p[0] for p in pads)
    lh = sum(p[3] - p[1] for p in pads) + 18 * (len(lines) - 1)
    px, pt, pb = int(size * .6), int(size * .7), int(size * .8)
    spr = Image.new("RGBA", (lw + 2 * px, lh + pt + pb), (0, 0, 0, 0))
    d = ImageDraw.Draw(spr)
    y = pt
    for ln, p in zip(lines, pads):
        x = px + (lw - (p[2] - p[0])) // 2 - p[0]
        d.text((x + 3, y + 4), ln, font=font, fill=(0, 0, 0, 170))
        d.text((x, y), ln, font=font, fill=(255, 176, 64, 140))
        d.text((x, y), ln, font=font, fill=(255, 246, 218, 255))
        y += (p[3] - p[1]) + 18
    _cache[key] = spr
    return spr

def badge_sprite():
    if "badge" in _cache:
        return _cache["badge"]
    font = ImageFont.truetype(DV, 34)
    txt = "DSKY✓"
    bb = ImageDraw.Draw(Image.new("RGBA", (8, 8))).textbbox((0, 0), txt, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    Wb, Hb = tw + 60, th + 22
    card = Image.new("RGBA", (Wb, Hb), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, Wb - 1, Hb - 1], radius=10,
                        fill=(8, 10, 14, 235), outline=CYAN + (255,), width=2)
    d.polygon([(14, 4), (24, 4), (19, Hb // 2), (27, Hb // 2), (12, Hb - 4),
               (17, Hb // 2 + 2), (10, Hb // 2)], fill=(255, 196, 40, 255))
    d.text((38 - bb[0], (Hb - th) // 2 - bb[1] - 1), txt, font=font,
           fill=(240, 246, 255, 255))
    _cache["badge"] = card
    return card

def icon_sprite(name, size):
    key = ("i", name, size)
    if key in _cache:
        return _cache[key]
    im = Image.open(f"work/icons/icon_{name}.png").convert("RGB").resize((size, size))
    lum = np.array(im.convert("L"), np.float32) / 255.0
    rgba = im.convert("RGBA")
    rgba.putalpha(Image.fromarray((np.clip(lum * 1.9, 0, 1) * 255).astype(np.uint8)))
    _cache[key] = rgba
    return rgba

def scrim_sprite():
    """Bande dégradée sombre derrière les paroles (lisibilité sur UI plateformes)."""
    if "scrim" in _cache:
        return _cache["scrim"]
    h = 320
    sc = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    a = np.zeros((h, W, 4), np.uint8)
    prof = (np.sin(np.linspace(0, np.pi, h)) * 110).astype(np.uint8)
    a[:, :, 3] = prof[:, None]
    sc = Image.fromarray(a, "RGBA")
    _cache["scrim"] = sc
    return sc

SAFE_TOP = 150          # sous barre de recherche/tabs (0-144 px)
SAFE_CTA = 232          # rangée CTA sous le badge
SAFE_TITLE = 330        # titres hook/intro
SAFE_LYR = H - 520      # top sprite paroles -> glyphs <= 0.80H (au-dessus caption/nav)
SAFE_LYR_SCRIM = 1330

def cta_sprite(size=72, gap=24):
    key = ("cta", size)
    if key in _cache:
        return _cache[key]
    ims = [icon_sprite(k, size) for k in ("like", "sub", "comment")]
    row = Image.new("RGBA", (3 * size + 2 * gap, size), (0, 0, 0, 0))
    for i, im in enumerate(ims):
        row.alpha_composite(im, (i * (size + gap), 0))
    _cache[key] = row
    return row

# ---------------------------------------------------------------- vague eau
def wave(sprite, t, amp=4.5, freq=0.9, lam=170.0, reveal=1.0, out=0.0):
    a = np.array(sprite)
    h, w = a.shape[:2]
    xs = np.arange(w)
    dy = (amp * np.sin(2 * math.pi * freq * t + 2 * math.pi * xs / lam)).round().astype(int)
    if reveal < 1.0:
        delay = xs / w * 0.45
        p = np.clip((reveal * 0.9 - delay) / 0.45, 0, 1)
        dy = dy + ((1 - p) * 46).round().astype(int)
        a = a.copy()
        a[:, :, 3] = (a[:, :, 3] * p[np.newaxis, :]).astype(np.uint8)
    if out > 0.0:
        delay = (w - xs) / w * 0.4
        p = np.clip(1 - (out * 0.8 - delay) / 0.4, 0, 1)
        a = a.copy()
        a[:, :, 3] = (a[:, :, 3] * p[np.newaxis, :]).astype(np.uint8)
        dy = dy + ((1 - p) * -30).round().astype(int)
    sh = a.shape[0]
    outa = np.zeros_like(a)
    for x in range(w):
        s = dy[x]
        if 0 <= s < sh:
            outa[s:, x] = a[:sh - s, x]
        elif s < 0 and -s < sh:
            outa[:sh + s, x] = a[-s:, x]
    return Image.fromarray(outa)

# ---------------------------------------------------------------- fonds
def precompute_fonds():
    import glob
    os.makedirs("work/fonds_portrait", exist_ok=True)
    for slot in range(0, NUNI + 2):
        dst = f"work/fonds_portrait/f{slot:02d}.jpg"
        if os.path.exists(dst):
            continue
        if slot == 0:
            src = "assets/raw/portrait/s00_intro.png"
        elif slot == NUNI + 1:
            src = "assets/raw/portrait/s39_endcard.png"
        else:
            g = glob.glob(f"assets/raw/portrait/s{slot:02d}_*.png")
            src = g[0] if g else None
        if not src or not os.path.exists(src):
            continue
        im = Image.open(src).convert("RGB")
        r = max(CW / im.width, CH / im.height)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        im = ImageOps.fit(im, (CW, CH), Image.LANCZOS)
        im.save(dst, quality=92)
        print("fond", dst)

_fonds = {}
def fond(slot):
    if slot not in _fonds:
        p = f"work/fonds_portrait/f{slot:02d}.jpg"
        if not os.path.exists(p) and slot == SLOT_ENDCARD:
            from PIL import ImageEnhance, ImageFilter
            base = fond(NUNI).copy()
            base = ImageEnhance.Brightness(base).enhance(0.32)
            base = base.filter(ImageFilter.GaussianBlur(6))
            vg = Image.new("L", (CW, CH), 0)
            ImageDraw.Draw(vg).ellipse([-CW // 2, -CH // 2, CW * 1.5, CH * 1.5], fill=255)
            base = Image.composite(base, Image.new("RGB", (CW, CH), (6, 7, 10)),
                                   vg.filter(ImageFilter.GaussianBlur(180)))
            base.save(p, quality=92)
        elif not os.path.exists(p):
            p = "work/fonds_portrait/f00.jpg"
        _fonds[slot] = Image.open(p).convert("RGB")
    return _fonds[slot]

def kenburns(slot, t, t0, t1):
    im = fond(slot)
    dur = max(t1 - t0, 0.5)
    p = min(max((t - t0) / dur, 0), 1)
    z = 1.02 + 0.06 * (p if slot % 2 == 0 else 1 - p)
    cw, ch = min(CW / z, CW), min(CH / z, CH)
    px = (CW - cw) / 2 + 12 * math.sin(2 * math.pi * t / 23.0 + slot)
    py = (CH - ch) / 2 + 8 * math.sin(2 * math.pi * t / 31.0 + slot * 2)
    px = min(max(px, 0), CW - cw); py = min(max(py, 0), CH - ch)
    return im.crop((int(px), int(py), int(px + cw), int(py + ch))).resize((W, H), Image.LANCZOS)

# ---------------------------------------------------------------- frames
def endcard_draw(img, t):
    d = ImageDraw.Draw(img)
    cx = W // 2
    tit = cursive_sprite("Je crache mes démons", 110)
    img.alpha_composite(tit, (cx - tit.width // 2, 260))
    f = lambda s: ImageFont.truetype(DV, s)
    rows = [("DAÏSKY PROD / TECHSTEIN", 44, CYAN),
            ("Artiste : Daïsky", 40, (245, 245, 245)),
            ("Rock / Afro-Rock / World · 2026", 36, (210, 215, 225)),
            ("Tel: 229 01 61 16 24 08 · 229 01 49 11 49 51", 34, (235, 235, 235)),
            ("daiskypro@proton.me", 34, (235, 235, 235)),
            ("daiskyproduction@gmail.com · techsteinsecureway@gmail.com", 28, (200, 205, 215)),
            ("@daiskypro", 40, CYAN),
            ("Wolof TechStein beat wê !", 40, (255, 196, 40))]
    y = 560
    for txt, s, col in rows:
        bb = d.textbbox((0, 0), txt, font=f(s))
        d.text((cx - (bb[2] - bb[0]) // 2, y), txt, font=f(s), fill=col + (255,))
        y += s + 34
    return img

def frame(i):
    t = i / FPS
    if t < HOOK:                              # COLD-OPEN = moment fort
        slot = 3 if t < 3.0 else 4
        img = kenburns(slot, t, 0 if t < 3 else 3.0, 3.0 if t < 3 else HOOK).convert("RGBA")
    elif t < OCC[0]["t0"]:
        img = kenburns(0, t, HOOK, OCC[0]["t0"]).convert("RGBA")
    elif t >= SONG_END - 1.0:
        img = kenburns(SLOT_ENDCARD, t, SONG_END - 1.0, TOTAL).convert("RGBA")
        img = endcard_draw(img, t)
    else:
        oc = next(o for o in OCC if o["t0"] - ADV <= t < o["t1"] - ADV)
        img = kenburns(oc["slot"], t, oc["t0"], oc["t1"]).convert("RGBA")
    if t < HOOK:
        oc = {"text": ORDER[2] if t < 3 else ORDER[3], "t0": 0.0 if t < 3 else 3.0,
              "t1": 3.0 if t < 3 else HOOK}
        spr = cursive_sprite(oc["text"])
        ap = (t - oc["t0"]) / 0.9
        img.alpha_composite(scrim_sprite(), (0, SAFE_LYR_SCRIM))
        img.alpha_composite(wave(spr, t, reveal=min(ap, 1.0)),
                            (W // 2 - spr.width // 2, SAFE_LYR))
        tit = cursive_sprite("Je crache mes démons", 96)
        img.alpha_composite(wave(tit, t, amp=6), (W // 2 - tit.width // 2, SAFE_TITLE))
    elif t < OCC[0]["t0"]:
        tit = cursive_sprite("Je crache mes démons", 118)
        img.alpha_composite(wave(tit, t, amp=6), (W // 2 - tit.width // 2, SAFE_TITLE + 30))
        sub = cursive_sprite("Daïsky", 84)
        img.alpha_composite(wave(sub, t, amp=5), (W // 2 - sub.width // 2, SAFE_TITLE + 30 + tit.height - 40))
    elif t < SONG_END - 1.0:
        oc = next(o for o in OCC if o["t0"] - ADV <= t < o["t1"] - ADV)
        spr = cursive_sprite(oc["text"])
        ap = (t - (oc["t0"] - ADV)) / 0.9
        op = (oc["t1"] - ADV - t) / 0.8
        img.alpha_composite(scrim_sprite(), (0, SAFE_LYR_SCRIM))
        img.alpha_composite(wave(spr, t, reveal=min(ap, 1.0), out=0.0 if op > 1 else max(0.0, 1 - op)),
                            (W // 2 - spr.width // 2, SAFE_LYR))
    if t < 2.0:                               # CTA 2 premières secondes
        row = cta_sprite()
        al = int(255 * min(t / 0.3, (2.0 - t) / 0.4, 1.0))
        r2 = row.copy(); r2.putalpha(r2.getchannel("A").point(lambda v: v * al // 255))
        img.alpha_composite(r2, (W // 2 - row.width // 2, SAFE_CTA))
    mid = TOTAL / 2                           # icône partage au milieu
    if abs(t - mid) < 2.5:
        s = icon_sprite("share", 150)
        pl = 1.0 + 0.08 * math.sin(2 * math.pi * 1.4 * t)
        s2 = s.resize((int(s.width * pl), int(s.height * pl)))
        al = int(255 * min((t - (mid - 2.5)) / 0.4, ((mid + 2.5) - t) / 0.4, 1.0))
        s2.putalpha(s2.getchannel("A").point(lambda v: v * al // 255))
        img.alpha_composite(s2, (W // 2 - s2.width // 2, int(H * 0.40)))
    b = badge_sprite()                        # badge DSKY✓ milieu haut, en dernier
    img.alpha_composite(b, (W // 2 - b.width // 2, SAFE_TOP))
    return img.convert("RGB")

def render(f0, f1, out):
    cmd = [FF, "-y", "-f", "image2pipe", "-vcodec", "mjpeg", "-framerate", str(FPS),
           "-i", "-", "-vcodec", "libx264", "-preset", "veryfast", "-crf", "19",
           "-pix_fmt", "yuv420p", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(f0, f1):
        b = io.BytesIO(); frame(i).save(b, "JPEG", quality=92)
        p.stdin.write(b.getvalue())
    p.stdin.close(); p.wait()
    print("rendu", out, f0, f1)

def mux(video, out):
    cmd = [FF, "-y", "-i", video, "-i", "work/audio_video.wav",
           "-filter_complex",
           f"[1:a]apad=whole_dur={TOTAL:.2f},afade=t=out:st={TOTAL-3:.2f}:d=3[a];"
           f"[0:v]fade=t=out:st={TOTAL-3:.2f}:d=3[v]",
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", "-t", f"{TOTAL:.2f}", out]
    subprocess.run(cmd, check=True)
    print("mux OK", out)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "fonds":
        precompute_fonds()
    elif mode == "render":
        render(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif mode == "mux":
        mux(sys.argv[2], sys.argv[3])
    elif mode == "audio":
        m1 = subprocess.run([FF, "-v", "info", "-i", "work/audio_concat.wav", "-af",
                             "loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
        j = json.loads(m1[m1.index("{"):m1.rindex("}") + 1])
        chain = ("highpass=f=30,lowpass=f=18000,loudnorm=I=-14:TP=-1.8:LRA=11:"
                 f"measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
                 f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
        subprocess.run([FF, "-y", "-v", "error", "-i", "work/audio_concat.wav", "-af", chain,
                        "-ar", "48000", "-ac", "2", "work/audio_video.wav"], check=True)
        print("audio master OK")
