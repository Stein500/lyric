#!/usr/bin/env python3
"""§D SOLUUTION A — rendu 9:16 (1080×1920) « Ayon dèkpè » (Daïsky) — S2 Golden Sunset.
Un seul flux de frames → image2pipe → libx264. Ken Burns + vague eau cursive + safe zones §H.
Usage: .venv/bin/python scripts/pipeline_rendu_9x16.py [fps] [out.mp4]
"""
import os, subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
OUT = sys.argv[2] if len(sys.argv) > 2 else "livrables/Ayon dèkpè_9x16_v1.mp4"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FF = os.path.join(ROOT, "bin", "ffmpeg")
ASSET = lambda *p: os.path.join(ROOT, "assets", *p)

HOOK = 6.0
SONG_DUR = 199.80
APAD = 5.0
TOTAL = HOOK + SONG_DUR + APAD          # 210.8
N = round(TOTAL * FPS)                  # 6324

CURSIVE = ASSET("fonts", "GreatVibes-Regular.ttf")
BOLD = ASSET("fonts", "DejaVuSans-Bold.ttf")
REG = ASSET("fonts", "DejaVuSans.ttf")

GOLD = (255, 205, 84)
GOLD_L = (255, 224, 130)
AMBER = (255, 172, 60)
CREAM = (255, 246, 226)
NAVY = (10, 12, 22)

# ----------------------------------------------------------------------------
# LYRICS: (onset_sec, text, slot)
L = [
    (6.35,  "Wolof TechStein beat wê...", "s00"),
    (11.78, "Ayon dèkpè...", "s40"),
    (14.89, "Ovèor gogo tipé...", "s31"),
    (16.52, "Ayon dèkpè, tu es trop jolie", "s01"),
    (18.75, "Ovèor gogo tipé, tu fais danser la nuit", "s32"),
    (23.95, "Ayon dèkpè, tu es trop jolie", "s25"),
    (31.29, "Ovèor gogo tipé, tu fais danser la vie", "s33"),
    (33.58, "Wolof TechStein beat wê!", "s41"),
    (40.23, "Quand tu marches dans la rue, tout s'arrête", "s11"),
    (42.21, "Les gens se retournent, la terre s'arrête", "s42"),
    (44.17, "Tu as ce truc, ce truc qui fait bouger", "s12"),
    (46.18, "Ce truc qui fait danser, ce truc qui fait rêver", "s43"),
    (48.36, "Tes pas sont une mélodie, ton corps une symphonie", "s13"),
    (50.30, "Tu danses comme si le monde était à toi, toute la nuit", "s14"),
    (52.38, "Ayon dèkpè, tu es une œuvre d'art", "s44"),
    (54.47, "Ovèor gogo tipé, tu illumines le noir", "s34"),
    (56.65, "Danse, danse, danse avec moi", "s15"),
    (59.15, "Danse, danse, danse jusqu'au bout de la nuit", "s16"),
    (61.20, "Danse, danse, danse avec moi", "s45"),
    (63.19, "Danse, danse, danse, tu es la vie", "s46"),
    (65.43, "Ayon dèkpè, tu es trop jolie", "s26"),
    (67.95, "Ovèor gogo tipé, tu fais danser la nuit", "s35"),
    (72.85, "Ayon dèkpè, tu es trop jolie", "s47"),
    (76.06, "Ovèor gogo tipé, tu fais danser la vie", "s27"),
    (79.97, "Wolof TechStein beat wê!", "s48"),
    (97.55, "Je danse comme si demain n'existait pas", "s17"),
    (99.33, "Je danse comme si le monde était à moi", "s49"),
    (101.40,"Mes hanches parlent, mes pieds racontent", "s19"),
    (103.69,"Une histoire que seuls les danseurs comprennent", "s19"),
    (105.49,"Ayon dèkpè, c'est ce qu'ils me disent", "s20"),
    (107.58,"Ovèor gogo tipé, c'est ce qu'ils me crient", "s36"),
    (109.66,"Mais moi je danse pour moi, pour la nuit", "s18"),
    (111.67,"Pour la house, le break, pour la vie", "s18"),
    (113.68,"Danse, danse, danse avec moi", "s21"),
    (116.13,"Danse, danse, danse jusqu'au bout de la nuit", "s22"),
    (118.17,"Danse, danse, danse avec moi", "s21"),
    (120.31,"Danse, danse, danse, tu es la vie", "s22"),
    (122.35,"Ayon dèkpè... tu es belle", "s23"),
    (125.26,"Ovèor gogo tipé... tu es celle", "s37"),
    (127.09,"Qui fait bouger les murs, qui fait trembler le sol", "s24"),
    (129.36,"Qui transforme la piste en un champ de bataille", "s24"),
    (132.48,"Ayon dèkpè, tu es trop jolie", "s26"),
    (134.94,"Ovèor gogo tipé, tu fais danser la nuit", "s38"),
    (140.30,"Ayon dèkpè, tu es trop jolie", "s25"),
    (143.07,"Ovèor gogo tipé, tu fais danser la vie", "s27"),
    (147.29,"Wolof TechStein beat wê!", "s00"),
    (155.49,"Wolof TechStein beat wê...", "s29"),
    (173.50,"Ayon dèkpè...", "s29"),
    (181.09,"Ovèor gogo tipé...", "s39"),
    (187.28,"(Danse... danse...)", "s30"),
]
# display window per line: onset -> next onset (or song end), capped at 5.0s
MAX_WIN = 5.0
ADV = 0.03
for i, (t, txt, slot) in enumerate(L):
    nxt = L[i+1][0] if i+1 < len(L) else SONG_DUR
    win = min(nxt - t, MAX_WIN)
    L[i] = (t, txt, slot, win)

# ----------------------------------------------------------------------------
def cover_resize(img, w, h):
    """Resize + center-crop to exactly (w,h)."""
    iw, ih = img.size
    s = max(w/iw, h/ih)
    img = img.resize((round(iw*s), round(ih*s)), Image.LANCZOS)
    l = (img.width-w)//2; t = (img.height-h)//2
    return img.crop((l, t, l+w, t+h))

SLOT_FILE = {
    "s00": "s00_intro.jpg", "s01": "s01_refrain1.jpg", "s02": "s02_danse_nuit.jpg",
    "s03": "s03_marche_rue.jpg", "s04": "s04_pas_symphonie.jpg",
    "s05": "s05_danse_avec_moi.jpg", "s06": "s06_demain.jpg",
    "s07": "s07_hanches.jpg", "s08": "s08_pont_beaute.jpg", "s09": "s09_outro.jpg",
    # Salve 2 (découpage plan par plan)
    "s11": "s11_rue_s_arrete.jpg", "s12": "s12_truc_rever.jpg",
    "s13": "s13_melodie_pieds.jpg", "s14": "s14_oeuvre_dart.jpg",
    "s15": "s15_invitation.jpg", "s16": "s16_bout_de_nuit.jpg",
    "s17": "s17_demain_libre.jpg", "s18": "s18_house_break.jpg",
    "s19": "s19_hanches_raccontent.jpg", "s20": "s20_ils_me_crient.jpg",
    # Salve 3 (refrain variants, pont, 2e bloc danse, outro)
    "s21": "s21_danse_avec_moi_2.jpg", "s22": "s22_bout_nuit_2.jpg",
    "s23": "s23_tu_es_belle.jpg", "s24": "s24_champ_bataille.jpg",
    "s25": "s25_trop_jolie_a.jpg", "s26": "s26_trop_jolie_b.jpg",
    "s27": "s27_danser_la_vie.jpg", "s28": "s28_danser_nuit_2.jpg",
    "s29": "s29_outro_silhouette.jpg", "s30": "s30_danse_danse_fin.jpg",
    # Salve 4 "gogo" (plans fessiers, bon sens — tenue traditionnelle intacte)
    "s31": "s31_gogo_intro.jpg", "s32": "s32_gogo_nuit.jpg",
    "s33": "s33_gogo_vie.jpg", "s34": "s34_gogo_noir.jpg",
    "s35": "s35_gogo_guirlandes.jpg", "s36": "s36_gogo_foule.jpg",
    "s37": "s37_gogo_celle.jpg", "s38": "s38_gogo_bounce.jpg",
    "s39": "s39_gogo_fin.jpg",
    # Salve 5 « sexy » (tenues provocatrices : fitted wax, backless, high slit, sequins)
    "s40": "s40_gogo_sultry_intro.jpg", "s41": "s41_tag_pose.jpg",
    "s42": "s42_rue_slit.jpg", "s43": "s43_truc_fumee.jpg",
    "s44": "s44_oeuvre_backless.jpg", "s45": "s45_invitation_sultry.jpg",
    "s46": "s46_vie_sequins.jpg", "s47": "s47_jolie_twirl.jpg",
    "s48": "s48_tag_nuit.jpg", "s49": "s49_monde_vent.jpg",
}
# fallback si un fichier d'image est absent (ex: s24 en attente de re-gén modération)
SLOT_FALLBACK = {"s24": "s23"}

def load_bg(slot):
    p = ASSET("raw", "portrait", SLOT_FILE[slot])
    if not os.path.exists(p):
        fb = SLOT_FALLBACK.get(slot)
        if not fb:
            raise FileNotFoundError(p)
        print(f"[warn] {SLOT_FILE[slot]} absent -> fallback {SLOT_FILE[fb]}", flush=True)
        p = ASSET("raw", "portrait", SLOT_FILE[fb])
    img = Image.open(p).convert("RGB")
    return np.asarray(cover_resize(img, 1188, 2112)).astype(np.float32)  # canvas 1.1x

BG = {s: load_bg(s) for s in SLOT_FILE}

def kb_frame(slot, t):
    """Ken Burns: triangle zoom 1.02<->1.08 (16 s) + pan sinus + dérive continue (mouvement permanent, jamais de gel)."""
    arr = BG[slot]
    CH, CW = arr.shape[0], arr.shape[1]
    slotnum = int(slot[1:]) if slot.startswith("s") and slot[1:].isdigit() else 0
    # triangle zoom
    zz = (t % 16.0)/16.0
    z = 1.02 + 0.06*(zz*2) if zz < 0.5 else 1.08 - 0.06*((zz-0.5)*2)
    cw = min(W/z, CW); ch = min(H/z, CH)
    mx = CW - cw; my = CH - ch
    # drift constant (>=1px/frame) + wobble, wrapped
    cx = (mx/2 + (mx/2)*math.sin(2*math.pi*t/13.0 + slotnum) + 33.0*t) % mx
    cy = (my/2 + (my/2)*math.cos(2*math.pi*t/17.0 + slotnum) + 29.0*t) % my
    x0 = int(np.clip(cx, 0, mx)); y0 = int(np.clip(cy, 0, my))
    crop = arr[y0:y0+int(ch), x0:x0+int(cw)]
    im = Image.fromarray(crop.astype(np.uint8)).resize((W,H), Image.LANCZOS)
    return np.asarray(im).astype(np.float32)

# ----------------------------------------------------------------------------
# text sprite rendering (RGBA)
def wrap_text(text, font, maxw):
    words = text.split()
    lines = []; cur = ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if cur and ImageFont.truetype(font, 100).getlength(trial) > maxw*100/90:
            lines.append(cur); cur = w_
        else:
            cur = trial
    if cur: lines.append(cur)
    return lines

def render_cursive(text, target_h=150, maxw=880):
    """Render cursive line(s) with auto-size to fit target height & width."""
    fontsize = 150
    f = ImageFont.truetype(CURSIVE, fontsize)
    lines = wrap_text(text, CURSIVE, maxw)
    # shrink if too wide
    while fontsize > 60 and any(ImageFont.truetype(CURSIVE, fontsize).getlength(ln) > maxw for ln in lines):
        fontsize -= 4
    f = ImageFont.truetype(CURSIVE, fontsize)
    asc, desc = f.getmetrics()
    lh = asc + desc + 14
    total_h = lh*len(lines)
    while total_h > target_h and fontsize > 50:
        fontsize -= 4
        f = ImageFont.truetype(CURSIVE, fontsize)
        asc, desc = f.getmetrics(); lh = asc+desc+14
        total_h = lh*len(lines)
    widths = [f.getlength(ln) for ln in lines]
    w = int(max(widths))+40
    h = int(total_h)+20
    sprite = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(sprite)
    y = 10
    for ln, lw in zip(lines, widths):
        x = (w - lw)/2
        # gold with warm shadow
        d.text((x+3, y+3), ln, font=f, fill=(60,20,0,255))
        d.text((x, y), ln, font=f, fill=GOLD+(255,))
        y += lh
    return np.asarray(sprite).astype(np.float32)

def render_ui(text, font_path, size, fill):
    f = ImageFont.truetype(font_path, size)
    asc, desc = f.getmetrics()
    w = int(f.getlength(text))+20; h = asc+desc+20
    sp = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(sp)
    d.text((10, 10), text, font=f, fill=fill)
    return np.asarray(sp).astype(np.float32)

def wave_shift(sprite, t, amp=4.5, freq=0.9):
    """Column-wise sinusoidal vertical shift = 'vague eau'."""
    h, w, c = sprite.shape
    y = np.arange(h, dtype=np.float32)[:, None]
    xs = np.arange(w, dtype=np.float32)[None, :]
    dy = amp * np.sin(2*np.pi*freq*t + 2*np.pi*(xs/w)*2.0)
    ys = np.clip(y + dy, 0, h-1).astype(np.int32)
    return sprite[ys, np.arange(w)[None, :]]

def blend(bg, sprite, x0, y0, alpha=1.0):
    h, w = sprite.shape[:2]
    x0=int(x0); y0=int(y0)
    x1=min(x0+w, bg.shape[1]); y1=min(y0+h, bg.shape[0])
    sx = x1-x0; sy = y1-y0
    a = (sprite[:sy, :sx, 3:4]/255.0) * alpha
    rgb = sprite[:sy, :sx, :3]
    region = bg[y0:y1, x0:x1]
    bg[y0:y1, x0:x1] = rgb*a + region*(1-a)
    return bg

# ----------------------------------------------------------------------------
# pre-render lyric sprites
LYR = {}
for t, txt, slot, win in L:
    if txt not in LYR:
        LYR[txt] = render_cursive(txt)

# UI sprites
BADGE = render_ui("DSKY✓", BOLD, 52, CREAM+(255,))
CTA = render_ui("♥  AIME     ▶  ABONNE-TOI     ●  COMMENTE", BOLD, 40, CREAM+(255,))
TITLE = render_cursive("Ayon dèkpè", target_h=260, maxw=900)
SUBTITLE = render_ui("Daïsky  ·  Wolof TechStein", BOLD, 48, AMBER+(255,))

# endcard (rendered at canvas size 1188x2112 so Ken Burns keeps moving on it too)
def build_endcard(CW=1188, CH=2112):
    im = Image.new("RGB", (CW, CH), NAVY)
    d = ImageDraw.Draw(im)
    for y in range(CH):
        k = y/CH
        d.line([(0,y),(CW,y)], fill=(int(10+8*k), int(12+6*k), int(22+10*k)))
    sx = CW/W  # scale factor
    f = ImageFont.truetype(CURSIVE, int(200*sx))
    t = "Ayon dèkpè"
    d.text(((CW-f.getlength(t))/2, int(240*sx)), t, font=f, fill=GOLD)
    fb = ImageFont.truetype(BOLD, int(40*sx))
    lines = [
        "Daïsky  ·  Wolof TechStein",
        "Afropop · 2026",
        "+229 00 00 00 00  ·  contact@daïsky.com",
        "@Daïsky",
    ]
    y = int(560*sx)
    for ln in lines:
        d.text(((CW-fb.getlength(ln))/2, y), ln, font=fb, fill=CREAM)
        y += int(64*sx)
    sig = "« Wolof TechStein beat wê ! »"
    fs = ImageFont.truetype(CURSIVE, int(64*sx))
    d.text(((CW-fs.getlength(sig))/2, int(880*sx)), sig, font=fs, fill=AMBER)
    return np.asarray(im).astype(np.float32)

BG["s10"] = build_endcard()

# ----------------------------------------------------------------------------
# frame pipeline
def build_frame(i):
    t = i/FPS
    # background slot
    if t < HOOK:
        slot = "s01"
    else:
        st = t - HOOK + ADV
        slot = "s00"
        for onset, txt, sl, win in L:
            if st >= onset - 0.02 and st < onset + win:
                slot = sl; break
    frame = kb_frame(slot, t)

    # scrim behind lyrics (band 1330..1650)
    scrim = np.zeros((H, W, 1), np.float32)
    for yy in range(1330, 1650):
        scrim[yy, :, 0] = min(0.43, (yy-1330)/320*0.43 + 0.05)
    frame = frame*(1-scrim) + (frame*0.15)*scrim  # darken behind text

    # badge (always, y=150 centered)
    blend(frame, BADGE, (W-BADGE.shape[1])/2, 150)

    # CTA row (first 2s)
    if t < 2.0:
        blend(frame, CTA, (W-CTA.shape[1])/2, 232)

    # cold-open title
    if t < HOOK:
        a = min(1.0, t/0.8)
        blend(frame, TITLE, (W-TITLE.shape[1])/2, 330, alpha=a)
        blend(frame, SUBTITLE, (W-SUBTITLE.shape[1])/2, 620, alpha=a)
    elif t < HOOK + SONG_DUR:
        st = t - HOOK + ADV
        cur = None
        for onset, txt, sl, win in L:
            if st >= onset - 0.02 and st < onset + win:
                cur = (txt, st - onset); break
        if cur:
            txt, el = cur
            sp = wave_shift(LYR[txt], t)
            a = min(1.0, el/0.9)
            th = sp.shape[0]
            y0 = 1400 + max(0, (150 - th)//2)   # top sprite H-520=1400, keep <=1560
            x0 = (W - sp.shape[1])/2
            blend(frame, sp, x0, y0, alpha=a)
    else:
        # endcard (slot s10) with Ken Burns + 0.5s fade-in
        a = min(1.0, (t - (HOOK+SONG_DUR))/0.5)
        ec = kb_frame("s10", t)
        frame = ec*a + frame*(1-a)

    # global fade-out last 3s
    if t > TOTAL - 3.0:
        k = (t - (TOTAL-3.0))/3.0
        frame = frame*(1-k)

    return np.clip(frame, 0, 255).astype(np.uint8)

# ----------------------------------------------------------------------------
def run():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cmd = [FF, "-y", "-loglevel", "error",
           "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
           "-i", os.path.join(ROOT, "work", "master_audio.wav"),
           "-c:v", "libx264", "-preset", "medium", "-crf", "21",
           "-pix_fmt", "yuv420p", "-tune", "film",
           "-c:a", "aac", "-b:a", "192k",
           "-af", f"afade=t=out:st={TOTAL-3.0:.2f}:d=3",
           "-movflags", "+faststart", "-shortest", OUT]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    buf = bytearray()
    for i in range(N):
        fr = Image.fromarray(build_frame(i))
        fr.save(p.stdin, "JPEG", quality=92)
        buf.clear()
        if i % 300 == 0:
            print(f"frame {i}/{N}  ({i/N*100:.0f}%)", flush=True)
    p.stdin.close()
    p.wait()
    print("DONE", OUT, "rc=", p.returncode)

if __name__ == "__main__":
    run()
