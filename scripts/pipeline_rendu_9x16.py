"""Pipeline rendu 9:16 — 'Nan yi a ga djin wê' (charte S6).
SOLUTION A : flux unique de frames i <-> t=i/FPS ; TOTAL=HOOK+duree+apad(5s).
Ken Burns 1,1x, vague eau cursive, safe zones §H, endcard §D.8, fades 3 s fin.
"""
import json, math, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

FF = "work/ffmpeg"
FPS = 25
W, H = 1080, 1920
CW, CH = 1188, 2112            # canvas 1,1x
HOOK = 6.0
APAD = 5.0
SONG = 162.84
TOTAL = HOOK + SONG + APAD
NB = math.ceil(TOTAL * FPS)

FONT_CUR = "assets/fonts/GreatVibes-latin.ttf"
FONT_UI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ---- timings validés + mapping texte->slot ----
tim = json.load(open("work/timings_validated.json"))
prompts = {e["slot"]: e for e in json.load(open("work/prompts.json"))}
slot_of = {}
n = 1
for e in tim:
    t = e["texte"]
    if t not in slot_of:
        slot_of[t] = f"s{n:02d}"
        n += 1
print(f"{len(slot_of)} textes uniques -> slots s01..s{n-1:02d}")

# fenêtres de vers (horloge vidéo = +HOOK, avance 0,03 s)
vers = []
for i, e in enumerate(tim):
    t0 = e["t_valide"] + HOOK - 0.03
    t1 = (tim[i + 1]["t_valide"] + HOOK - 0.03) if i + 1 < len(tim) else HOOK + SONG - 2.0
    vers.append((t0, t1, e["texte"], slot_of[e["texte"]]))

# ---- assets ----
def load(slot):
    p = f"work/img916/{slot}.jpg" if slot not in ("s00_intro", "s37_endcard") else f"work/img916/{slot}.jpg"
    return Image.open(p).convert("RGB").resize((CW, CH), Image.LANCZOS)

BG = {"s00_intro": load("s00_intro"), "s37_endcard": load("s37_endcard")}
for e in tim:
    s = slot_of[e["texte"]]
    if s not in BG:
        BG[s] = load(s)

fc96 = ImageFont.truetype(FONT_CUR, 96)
fcT = ImageFont.truetype(FONT_CUR, 120)
fui = ImageFont.truetype(FONT_UI, 40)
fuiS = ImageFont.truetype(FONT_UI, 34)

def wavy(txt, font, amp=4.5, glow=(255, 170, 40), core=(255, 240, 200)):
    tl = Image.new("RGBA", (2200, 340), (0, 0, 0, 0))
    d = ImageDraw.Draw(tl)
    d.text((24, 48), txt, font=font, fill=glow + (170,))
    d.text((20, 44), txt, font=font, fill=core + (255,))
    a = np.array(tl)
    out = np.zeros_like(a)
    xs = np.arange(a.shape[1])
    dy = (amp * np.sin(2 * np.pi * 0.9 * xs / (W * 0.5))).astype(int)
    for x in xs:
        out[:, x, :] = np.roll(a[:, x, :], dy[x], axis=0)
    im = Image.fromarray(out)
    return im.crop(im.getbbox())

def fit(img, maxw=W - 120):
    s = min(1.0, maxw / img.width)
    return img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)

def stagger_alpha(prog):
    """apparition staggered 0,9 s : renvoie fraction visible 0..1"""
    return max(0.0, min(1.0, prog))

# ---- scrim précalculé ----
scrim = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(scrim)
for y in range(H - 760, H - 380):
    d.line([(0, y), (W, y)], fill=int(200 * (y - (H - 760)) / 380))
for y in range(H - 380, H):
    d.line([(0, y), (W, y)], fill=200)
SCRIM = np.array(scrim) / 255.0

# ---- badge DSKY✓ ----
badge_lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
db = ImageDraw.Draw(badge_lay)
fb = ImageFont.truetype(FONT_UI, 58)
tw = db.textlength("DSKY✓", font=fb)
db.rounded_rectangle([(W / 2 - tw / 2 - 40, 98), (W / 2 + tw / 2 + 40, 202)], radius=26,
                     fill=(10, 10, 14, 205), outline=(255, 190, 60, 255), width=3)
db.text(((W - tw) / 2, 118), "DSKY✓", font=fb, fill=(255, 205, 90, 255))
BADGE = np.array(badge_lay).astype(np.float32) / 255.0

# ---- titre hook ----
titre = fit(wavy("Nan yi a ga djin wê", fcT))

# ---- endcard ----
def endcard():
    im = BG["s37_endcard"].resize((W, H), Image.LANCZOS).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(ov)
    dd.rectangle([(0, int(0.25 * H)), (W, int(0.75 * H))], fill=(5, 5, 8, 190))
    tt = fit(wavy("Nan yi a ga djin wê", fcT, amp=3), W - 160)
    ov.paste(tt, ((W - tt.width) // 2, int(0.27 * H)), tt)
    y = int(0.27 * H) + tt.height + 46
    lines = ["Artiste : Daïsky", "Genre : Hip-Hop Afro motivation", "Label / prod : Wolof TechStein",
             "Année : 2026", "Contact : +229 — à compléter", "Email : à compléter",
             "@daisky_officiel", "Wolof TechStein beat wê !"]
    for i, ln in enumerate(lines):
        f = fui if i < 4 else fuiS
        c = (235, 225, 200, 255) if i < 7 else (255, 205, 90, 255)
        dd.text(((W - dd.textlength(ln, font=f)) / 2, y), ln, font=f, fill=c)
        y += 58
    return im

END = endcard()

# ---- pré-render vers texte (une seule fois par texte unique) ----
VERSW = {t: fit(wavy(t, fc96)) for t in slot_of}

# ---- état Ken Burns par slot ----
kb_state = {}
def kb_params(slot, t_in_slot, dur_slot):
    z0, z1 = (1.02, 1.08) if hash(slot) % 2 == 0 else (1.08, 1.02)
    z = z0 + (z1 - z0) * min(1.0, t_in_slot / max(dur_slot, 0.1))
    return z

def crop_canvas(canvas, z, t):
    cw, ch = int(W / z), int(H / z)
    cx = (CW - cw) / 2 + 18 * math.sin(2 * math.pi * 0.05 * t)
    cy = (CH - ch) / 2 + 12 * math.sin(2 * math.pi * 0.04 * t + 1.3)
    cx = int(max(0, min(CW - cw, cx))); cy = int(max(0, min(CH - ch, cy)))
    return canvas.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.LANCZOS)

def current_slot(t):
    """slot de fond : suit le vers courant (intro s00 avant 1er vers)."""
    tv = t - HOOK
    if tv < vers[0][0] - HOOK + 0.03:
        return "s00_intro", tv
    for t0, t1, txt, s in vers:
        if t0 <= t < t1:
            return s, tv
    return vers[-1][3], tv

# transitions fondu entre slots 0,35 s
def render_frame(i):
    t = i / FPS
    fade_end = max(0.0, min(1.0, (TOTAL - t) / 3.0)) if t > TOTAL - 3 else 1.0
    # fond
    if t >= HOOK + SONG - 3.0:
        base = END.convert("RGB")
        slot = "s37_endcard"
        tin, dur = t - (HOOK + SONG - 3), 8
    else:
        slot, tv = current_slot(t)
        canvas = BG[slot]
        # micro-fondu entre slots
        base = crop_canvas(canvas, kb_params(slot, tv, 4.0), tv)
        tin, dur = tv, 4
    arr = np.array(base).astype(np.float32)
    arr *= (0.4 + 0.6 * SCRIM)[..., None] * 0 + 1.0  # scrim appliqué via overlay ci-dessous
    frame = base.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # scrim bas
    sc = Image.fromarray((SCRIM * 255).astype(np.uint8), "L")
    ov.paste((0, 0, 0, 255), (0, 0, W, H), sc)
    frame = Image.alpha_composite(frame, ov)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # vers courant
    for t0, t1, txt, s in vers:
        if t0 - 0.05 <= t < t1:
            img = VERSW[txt]
            prog = stagger_alpha((t - t0) / 0.9)
            nchars = max(1, int(img.width * prog)) if prog < 1 else img.width
            vis = img.crop((0, 0, nchars, img.height))
            frame.alpha_composite(vis, ((W - img.width) // 2, H - 520 - img.height // 2))
            break
    # badge : apparaît/disparaît avec les paroles du hook + endcard
    alpha = 0.0
    if t < HOOK:
        alpha = min(1.0, t / 0.5) * min(1.0, (HOOK - t) / 0.5)
    if t >= HOOK + SONG - 3.0:
        alpha = min(1.0, (t - (HOOK + SONG - 3)) / 0.5)
    if alpha > 0.01:
        b = (BADGE * np.array([1, 1, 1, alpha])[None, None, :])
        frame = Image.alpha_composite(frame, Image.fromarray((b * 255).astype(np.uint8)))
    # titre hook y=330
    if t < HOOK:
        a = min(1.0, t / 0.6) * min(1.0, (HOOK - t) / 0.6)
        tt = titre.copy()
        tt.putalpha(Image.fromarray((np.array(tt.split()[3]) * a).astype(np.uint8)))
        frame.alpha_composite(tt, ((W - tt.width) // 2, 330))
    rgb = frame.convert("RGB")
    if fade_end < 1.0:
        rgb = rgb.point(lambda v: int(v * fade_end))
    return rgb

def main():
    # audio : hook(6 s ex. 19,04) + master + apad
    subprocess.run([FF, "-v", "error", "-y", "-ss", "19.04", "-t", str(HOOK), "-i", "work/song_master.wav", "-ar", "48000", "-ac", "2", "work/hook.wav"], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo", "-t", str(APAD + 0.2), "work/apad.wav"], check=True)
    lst = open("work/concat.txt", "w"); lst.write("file 'hook.wav'\nfile 'song_master.wav'\nfile 'apad.wav'\n"); lst.close()
    subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "work/concat.txt", "-af", f"afade=t=out:st={TOTAL-3}:d=3", "-ar", "48000", "work/audio_total.wav"], check=True)

    # vidéo : image2pipe mjpeg -> libx264
    cmd = [FF, "-y", "-f", "image2pipe", "-vcodec", "mjpeg", "-framerate", str(FPS), "-i", "-",
           "-i", "work/audio_total.wav", "-c:v", "libx264", "-crf", "21", "-preset", "veryfast",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
           "-t", str(TOTAL), "livrables/Nan yi a ga djin wê - clip 9x16.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for i in range(NB):
        img = render_frame(i)
        buf = __import__("io").BytesIO()
        img.save(buf, "JPEG", quality=92)
        p.stdin.write(buf.getvalue())
        if i % 250 == 0:
            print(f"frame {i}/{NB}", flush=True)
    p.stdin.close()
    p.wait()
    print("rendu terminé", p.returncode)

if __name__ == "__main__":
    main()
