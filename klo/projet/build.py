#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production des 3 videos d'anniversaire pour KLO — format 9:16 (WhatsApp/TikTok).
Pipeline : PIL frames -> ffmpeg zoompan (Ken Burns) -> xfade (fondus) -> overlay badge
statique -> burn ASS paroles -> mux audio (afade in/out).
"""
import os, subprocess, math, json, glob, sys

BASE = os.path.dirname(os.path.abspath(__file__))
RAW  = os.path.join(BASE, "assets", "raw", "portrait")
GEN  = os.path.join(BASE, "assets", "gen")
PREP = os.path.join(BASE, "assets", "prep")
WORK = os.path.join(BASE, "work")
LIVR = os.path.join(BASE, "livrables")
AUDIO = os.path.join(BASE, "..", "Joyeux anniversaire Klo.mp3")
BADGE_PNG = os.path.join(PREP, "badge_1080x1920.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
W, H, FPS = 1080, 1920, 24
DURATION = 105.0
FADE = 0.6  # duree des fondus entre segments

for d in (PREP, WORK, LIVR):
    os.makedirs(d, exist_ok=True)

try:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FF = "ffmpeg"

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("ERREUR:", " ".join(str(c) for c in cmd[:4]), "...")
        print(r.stderr[-2500:])
        sys.exit(1)
    return r

# ---------------------------------------------------------------------------
# Palettes des 3 ambiances — couleurs ASS au format &HBBGGRR
# ---------------------------------------------------------------------------
THEME = {
  "V1": {  # Or / Rose chaud
     "title":"&H00A3E8",        # or  (BGR de E8A300)
     "refrain":"&H00A3E8",      # or
     "male":"&HF5F9FF",         # blanc eclair
     "female":"&HC8A2E8",       # rose/mauve (BGR de E8A2C8)
     "bridge":"&H9AD9FF",       # ambre clair (BGR de FFD99A)
     "wolof":"&H00A3E8",        # or
     "outro":"&H00A3E8",
     "halo":(232,163,61),
  },
  "V2": {  # Nuit Cyan "Ma lumiere"
     "title":"&HFFD24D",        # cyan (BGR de 4DD2FF)
     "refrain":"&HFFD24D",      # cyan
     "male":"&HF5F9FF",         # blanc eclair
     "female":"&HF4B686",       # periwinkle doux (BGR de 86B6F4)
     "bridge":"&HFFD2AA",       # cyan clair italic
     "wolof":"&H3DA3E8",        # ambre (signature)
     "outro":"&HFFD24D",
     "halo":(77,210,255),
  },
  "V3": {  # Party confettis (rose + cyan)
     "title":"&HC866F5",        # rose vif (BGR de F566C8)
     "refrain":"&HFFD24D",      # cyan
     "male":"&HF5F9FF",         # blanc
     "female":"&HC866F5",       # rose
     "bridge":"&H3DA3E8",       # ambre
     "wolof":"&H3DA3E8",        # ambre
     "outro":"&HC866F5",
     "halo":(245,102,200),
  },
}

# ---------------------------------------------------------------------------
# Segments visuels : (cle, source, type 'photo'|'bg', teinte halo optionnelle)
# bornes d'affichage (start) ; la derniere finit a DURATION.
# ---------------------------------------------------------------------------
P = {f: os.path.join(RAW, f) for f in os.listdir(RAW)}
G = {g: os.path.join(GEN, g) for g in os.listdir(GEN)}
def pho(n): return os.path.join(RAW, f"IMG-20260827-WA{n}.jpg")
def gen(n): return os.path.join(GEN, n)

FEST = ["0002","0008","0009","0010"]   # robe rose / tresses perles
COZY = ["0004","0005","0006","0003","0007"]  # t-shirt Stitch

# Chaque version : liste de (start, source, kind)
SEG = {
 "V1": [
   (0.0,  gen("gold_bokeh.jpg"), "bg"),
   (8.0,  pho("0008"), "photo"),
   (12.3, pho("0002"), "photo"),
   (22.0, pho("0010"), "photo"),
   (33.2, pho("0009"), "photo"),
   (44.2, gen("gold_roses.jpg"), "bg"),
   (54.5, gen("cake.jpg"), "bg"),
   (65.2, gen("gold_bokeh.jpg"), "bg"),
   (79.0, gen("fireworks.jpg"), "bg"),
   (95.0, gen("fireworks.jpg"), "bg"),
 ],
 "V2": [
   (0.0,  gen("cyan_stars.jpg"), "bg"),
   (8.0,  pho("0004"), "photo"),
   (12.3, pho("0006"), "photo"),
   (22.0, pho("0003"), "photo"),
   (33.2, pho("0005"), "photo"),
   (44.2, pho("0007"), "photo"),
   (54.5, gen("cyan_party.jpg"), "bg"),
   (65.2, gen("cyan_stars.jpg"), "bg"),
   (79.0, gen("fireworks.jpg"), "bg"),
   (95.0, gen("cyan_stars.jpg"), "bg"),
 ],
 "V3": [
   (0.0,  gen("confetti.jpg"), "bg"),
   (8.0,  pho("0010"), "photo"),
   (12.3, pho("0002"), "photo"),
   (22.0, pho("0004"), "photo"),
   (33.2, pho("0008"), "photo"),
   (40.2, pho("0006"), "photo"),
   (46.2, pho("0003"), "photo"),
   (51.2, pho("0005"), "photo"),
   (57.2, gen("confetti.jpg"), "bg"),
   (65.2, pho("0009"), "photo"),
   (71.2, gen("cyan_party.jpg"), "bg"),
   (79.0, gen("fireworks.jpg"), "bg"),
   (91.0, pho("0007"), "photo"),
   (95.0, gen("fireworks.jpg"), "bg"),
 ],
}

def seg_durations(starts):
    """renvoie les durees brutes de clips ; les n-1 premieres gagnent FADE,
    l'affichage final couvre [start_i, start_{i+1}] et la derniere va a DURATION."""
    spans = [starts[i+1]-starts[i] for i in range(len(starts)-1)] + [DURATION-starts[-1]]
    raw = [spans[i]+(FADE if i < len(spans)-1 else 0.0) for i in range(len(spans))]
    return raw

# ---------------------------------------------------------------------------
# Construction des frames PIL
# ---------------------------------------------------------------------------
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps, ImageEnhance

def font(size, bold=True, serif=False):
    name = "DejaVuSerif-Bold.ttf" if serif else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def cover(im, w, h):
    im = im.convert("RGB")
    sr = w/h; ir = im.size[0]/im.size[1]
    if ir > sr:
        nh = h; nw = int(h*ir)
    else:
        nw = w; nh = int(w/ir)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw-w)//2; y = (nh-h)//2
    return im.crop((x, y, x+w, y+h))

def bottom_scrim(im, strength=150):
    ov = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(ov)
    for i in range(420):
        a = int(strength * (i/420)**1.6)
        d.line([(0, H-420+i), (W, H-420+i)], fill=a)
    black = Image.new("RGB", (W,H), (0,0,0))
    im = im.convert("RGB")
    im.paste(black, (0,0), ov)
    return im

def top_scrim(im, strength=110):
    ov = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(ov)
    for i in range(360):
        a = int(strength * (1 - i/360)**1.6)
        d.line([(0, i), (W, i)], fill=a)
    black = Image.new("RGB", (W,H), (0,0,0))
    im = im.convert("RGB")
    im.paste(black, (0,0), ov)
    return im

def rounded_mask(size, rad):
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0,0,size[0]-1,size[1]-1], radius=rad, fill=255)
    return m

def build_frame(src, kind, halo, outpath):
    if kind == "photo":
        photo = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        # fond : meme photo tres floutee + assombrie, teintee du halo
        bg = cover(photo, W, H).filter(ImageFilter.GaussianBlur(46))
        bg = ImageEnhance.Brightness(bg).enhance(0.45)
        tint = Image.new("RGB", (W,H), halo)
        bg = Image.blend(bg, tint, 0.22)
        bg = bottom_scrim(bg, 170)
        bg = top_scrim(bg, 90)
        # carte photo
        cw, ch = 864, 1152  # ratio 3:4
        card = cover(photo, cw, ch)
        rad = 46
        mask = rounded_mask((cw, ch), rad)
        # halo derriere la carte
        glow = Image.new("RGBA", (W,H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        cx, cy = W//2, 800
        for rr, aa in [(54,30),(40,46),(28,66)]:
            gd.rounded_rectangle([cx-cw//2-rr, cy-ch//2-rr, cx+cw//2+rr, cy+ch//2+rr],
                                 radius=rad+rr, outline=halo+(aa,), width=10)
        glow = glow.filter(ImageFilter.GaussianBlur(16))
        bg = bg.convert("RGBA"); bg.alpha_composite(glow)
        bg.paste(card, (cx-cw//2, cy-ch//2), mask)
        # liseré net
        od = ImageDraw.Draw(bg)
        od.rounded_rectangle([cx-cw//2, cy-ch//2, cx+cw//2, cy+ch//2],
                             radius=rad, outline=(255,255,255,235), width=4)
        frame = bg.convert("RGB")
    else:
        im = cover(ImageOps.exif_transpose(Image.open(src)).convert("RGB"), W, H)
        im = ImageEnhance.Brightness(im).enhance(0.96)
        frame = bottom_scrim(im, 150)
        frame = top_scrim(frame, 70)
    frame.save(outpath, quality=92)
    return outpath

def build_badge():
    if os.path.exists(BADGE_PNG):
        return BADGE_PNG
    canvas = Image.new("RGBA", (W,H), (0,0,0,0))
    d = ImageDraw.Draw(canvas)
    txt = "DAÏSKY PROD"
    f = font(34, bold=True)
    bolt = font(40, bold=True)
    tb = d.textbbox((0,0), txt, font=f)
    bb = d.textbbox((0,0), "⚡", font=bolt)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    bw_, bh_ = d.textbbox((0,0),"⚡",font=bolt)[:3][2], 0
    bolt_w = bb[2]-bb[0]
    pad_x, pad_y = 30, 18
    gap = 14
    pill_w = pad_x*2 + bolt_w + gap + tw
    pill_h = max(th, bb[3]-bb[1]) + pad_y*2
    x0, y0 = 40, H-40-pill_h
    # pill
    d.rounded_rectangle([x0,y0,x0+pill_w,y0+pill_h], radius=pill_h//2,
                        fill=(5,8,16,205), outline=(77,210,255,255), width=3)
    tx = x0+pad_x
    ty = y0 + (pill_h-(bb[3]-bb[1]))//2 - bb[1]
    d.text((tx, ty), "⚡", font=bolt, fill=(77,210,255,255))
    tx += bolt_w + gap
    ty = y0 + (pill_h-th)//2 - tb[1]
    d.text((tx, ty), txt, font=f, fill=(245,249,255,255))
    canvas.save(BADGE_PNG)
    return BADGE_PNG

# ---------------------------------------------------------------------------
# Sous-titres ASS
# ---------------------------------------------------------------------------
# Cues partages : (start, end, texte, style)
CUES = [
  (1.0,  8.4,  "Joyeux Anniversaire", "title2"),
  (1.0,  8.4,  "KLO  •  CONFIANCE", "title"),
  (1.0,  8.4,  "30 août", "titlesub"),
  (8.8, 11.8,  "Wolof TechStein beat wê…", "wolof"),
  (12.3,17.0,  "Joyeux anniversaire, Klo", "refrain"),
  (17.0,22.0,  "Joyeux anniversaire, ma lumière", "refrain"),
  (22.0,27.0,  "30 août, c'est ton jour", "refrain"),
  (27.0,33.2,  "Le monde est plus beau quand tu es là", "refrain"),
  (33.2,35.2,  "Tu es la joie, tu es la paix", "male"),
  (35.2,38.0,  "Chaque jour avec toi est un rêve", "male"),
  (38.0,40.2,  "Je te souhaite tout le bonheur", "male"),
  (40.2,44.2,  "Ma Confiance, mon cœur", "male"),
  (44.2,46.2,  "Tu es la joie, tu es la paix", "female"),
  (46.2,49.0,  "Chaque jour avec toi est un rêve", "female"),
  (49.0,51.2,  "Je te souhaite tout le bonheur", "female"),
  (51.2,54.5,  "Ma Confiance, mon cœur", "female"),
  (54.5,57.2,  "Que cette année soit belle", "bridge"),
  (57.2,59.5,  "Que tes rêves deviennent réels", "bridge"),
  (59.5,62.3,  "Klo, tu es unique", "bridge"),
  (62.3,65.2,  "Confiance, tu es magnifique", "bridge"),
  (65.2,71.2,  "Joyeux anniversaire, JésuKlo…", "outro"),
  (71.2,78.8,  "Joyeux anniversaire, Confiance…", "outro"),
  (79.0,82.5,  "Wolof TechStein beat wê…", "wolof"),
  (91.0,94.5,  "Wolof TechStein beat wê…", "wolof"),
  (95.0,103.5, "Joyeux Anniversaire", "title2"),
  (95.0,103.5, "KLO  •  CONFIANCE", "title"),
  (95.0,103.5, "30 août — Merci d'être toi ♥", "titlesub"),
]

def ass_time(t):
    h=int(t//3600); m=int((t%3600)//60); s=t%60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def esc(t):
    return t.replace("\\","\\\\").replace("{","(").replace("}",")")

def build_ass(ver, outpath):
    c = THEME[ver]
    def st(name, size, color, bold=1, italic=0, align=2, margin_v=340, outline=3, fontn="DejaVu Sans"):
        # champs: Name,Fontname,Fontsize,Primary,Secondary,Outline,Back,Bold,Italic,
        #        Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,
        #        Shadow,Alignment,MarginL,MarginR,MarginV,Encoding  (23 champs)
        return (f"Style: {name},{fontn},{size},{color},&H000000FF,&H00000000,&H96000000,"
                f"{bold},{italic},0,0,100,100,0,0,1,{outline},2,{align},40,40,{margin_v},1")
    styles = [
      st("Default",  64, "&HF5F9FF",   bold=1, align=2, margin_v=340, outline=3),
      st("title",    78, c["title"],   bold=1, align=2, margin_v=760, outline=4),
      st("title2",  104, c["title"],   bold=1, align=2, margin_v=900, outline=5),
      st("titlesub", 56, "&HF5F9FF",   bold=0, italic=1, align=2, margin_v=650, outline=3),
      st("refrain",  70, c["refrain"], bold=1, align=2, margin_v=340, outline=4),
      st("male",     64, c["male"],    bold=1, align=2, margin_v=340, outline=3),
      st("female",   64, c["female"],  bold=1, align=2, margin_v=340, outline=3),
      st("bridge",   60, c["bridge"],  bold=0, italic=1, align=2, margin_v=340, outline=3),
      st("outro",    72, c["outro"],   bold=1, align=2, margin_v=360, outline=4),
      st("wolof",    64, c["wolof"],   bold=1, align=2, margin_v=340, outline=4),
    ]
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 1
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
""" + "\n".join(styles) + "\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    lines=[]
    for (s,e,txt,style) in CUES:
        lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},{style},,0,0,0,,{{\\fad(90,140)}}{esc(txt)}")
    with open(outpath,"w",encoding="utf-8") as f:
        f.write(head + "\n".join(lines) + "\n")
    return outpath

# ---------------------------------------------------------------------------
# Montage video
# ---------------------------------------------------------------------------
def build_video(ver):
    print(f"\n=== Construction {ver} ===")
    segs = SEG[ver]
    starts = [s for s,_,_ in segs]
    durs = seg_durations(starts)
    halo = THEME[ver]["halo"]
    vdir = os.path.join(WORK, ver)
    os.makedirs(vdir, exist_ok=True)

    clips=[]
    for i,(stt, src, kind) in enumerate(segs):
        fr = os.path.join(vdir, f"frame_{i:02d}.jpg")
        build_frame(src, kind, halo, fr)
        cl = os.path.join(vdir, f"clip_{i:02d}.mp4")
        frames = max(1, round(durs[i]*FPS))
        # Ken Burns : zoom avant / arriere alternes (base sur le numero de frame 'on')
        if i % 2 == 0:
            z = "min(1.12,1.0+0.00045*on)"
        else:
            z = "max(1.0,1.12-0.00045*on)"
        x = "iw/2-(iw/zoom/2)"; y = "ih/2-(ih/zoom/2)"
        vf = (f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s=1080x1920:fps={FPS},"
              f"format=yuv420p")
        run([FF,"-y","-loop","1","-i",fr,"-t",f"{durs[i]:.3f}","-vf",vf,
             "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",
             "-r",str(FPS),"-an", cl])
        clips.append(cl)
        print(f"  clip {i:02d} {kind:5s} {durs[i]:.2f}s  {os.path.basename(src)}")

    # chaine xfade
    inputs=[]
    for c in clips: inputs += ["-i", c]
    fc=[]; last="[0:v]"; cur_off=0.0
    n=len(clips)
    for i in range(1,n):
        cur_off += durs[i-1] - FADE
        out = f"[vx{i}]"
        trans = "fade" if i not in (4,9) else "dissolve"
        fc.append(f"{last}[{i}:v]xfade=transition={trans}:duration={FADE}:offset={cur_off:.3f}{out}")
        last = out
    total = sum(durs) - FADE*(n-1)
    fc.append(f"{last}format=yuv420p[vout]")
    joined = os.path.join(vdir, "joined.mp4")
    run([FF,"-y",*inputs,"-filter_complex",";".join(fc),"-map","[vout]",
         "-c:v","libx264","-preset","veryfast","-crf","20","-r",str(FPS), joined])
    print(f"  joined: {total:.2f}s (attendu {DURATION:.2f})")

    # badge + ASS + audio
    badge = build_badge()
    ass = os.path.join(vdir, "subs.ass")
    build_ass(ver, ass)
    names = {"V1":"Klo_Anniversaire_V1_FestifOr_9x16.mp4",
             "V2":"Klo_Anniversaire_V2_NuitCyan_9x16.mp4",
             "V3":"Klo_Anniversaire_V3_PartyConfettis_9x16.mp4"}
    out = os.path.join(LIVR, names[ver])
    vf = (f"[0:v][2:v]overlay=0:0:format=auto[bv];"
          f"[bv]ass='{ass}':fontsdir='{FONT_DIR}'[v]")
    run([FF,"-y","-i",joined,"-i",AUDIO,"-i",badge,
         "-filter_complex",vf,"-map","[v]","-map","1:a",
         "-c:v","libx264","-preset","medium","-crf","21","-pix_fmt","yuv420p","-r",str(FPS),
         "-c:a","aac","-b:a","192k","-ar","44100","-ac","2",
         "-af", f"afade=t=in:st=0:d=0.3,afade=t=out:st={DURATION-3:.1f}:d=3",
         "-t", f"{DURATION}", "-movflags","+faststart","-shortest", out])
    print(f"  LIVRABLE -> {out}")
    return out

def qa(path):
    pr = subprocess.run([FF,"-i",path],capture_output=True,text=True)
    dur = [l for l in pr.stderr.splitlines() if "Duration" in l]
    print("  QA", os.path.basename(path), dur[0].strip() if dur else "?")
    bd = subprocess.run([FF,"-i",path,"-vf","blackdetect=d=0.3:pix_th=0.10","-an","-f","null","-"],
                        capture_output=True,text=True)
    blacks = [l for l in bd.stderr.splitlines() if "blackdetect" in l]
    print("  trous noirs:", len(blacks))
    for b in blacks[:5]: print("   ", b.strip())

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv)>1 else "ALL"
    vers = ["V1","V2","V3"] if which=="ALL" else [which]
    outs=[]
    for v in vers:
        outs.append(build_video(v))
    for o in outs:
        qa(o)
    print("\nTERMINE.")
