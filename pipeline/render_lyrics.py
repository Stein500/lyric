# RENDU LYRICS 9:16 cursive — SOLUTION A (flux continu), v4.9.2
import sys, math, io
sys.path.insert(0,'pipeline')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from render_common import *
from timeline_yafoy import LINES, background_at, ADVANCE, DUR, ENDCARD_T, TOTAL

OUT = 'livrables/Yafoy_9x16_cursive_v1.mp4'
AUDIO = "livrables/Yafoy t'es encore là - Daïsky (Master).mp3"

# --- précalcul fonds (canvas KB) ---
slots = sorted(set([l[3] for l in LINES] + ['s00','s31','s32','s33','s34']))
canvases = {s: load_canvas(slot_path(s)) for s in slots}
seeds = {s:i for i,s in enumerate(slots)}
# segments continus de fond (anti-freeze : u progresse sur TOUTE la durée du segment)
SEGS = []
_t = 0.0
_cur = background_at(0.0)
_start = 0.0
while _t < TOTAL:
    _t += 1.0/FPS
    b = background_at(min(_t, TOTAL-0.01))
    if b != _cur:
        SEGS.append((_start, _t, _cur)); _cur=b; _start=_t
SEGS.append((_start, TOTAL, _cur))
def bg_window(t):
    for a,b,s in SEGS:
        if a <= t < b:
            return s, (t-a)/max(0.5, b-a)
    return SEGS[-1][2], 1.0

def _unused(t):
    s = background_at(t)
    # bornes approx du slot courant
    t0,t1 = 0.0, TOTAL
    if s=='s00': t0,t1=0,4
    elif s=='s31': t0,t1=168.5,182.5
    elif s=='s32': t0,t1=182.5,196.5
    elif s=='s33': t0,t1=196.5,210
    elif s=='s34': t0,t1=ENDCARD_T,TOTAL
    else:
        for txt,a,b,sl,g in LINES:
            if sl==s and a<=t<b+14: t0,t1=a,max(b,a+3); break
        else:
            for txt,a,b,sl,g in LINES:
                if sl==s: t0,t1=a,max(b,a+3)
    u = (t-t0)/max(0.5,(t1-t0))
    return s, min(1.0,max(0.0,u))

# --- sprites paroles (cache) + luminance fond sous texte ---
sprites = {}
for i,(txt,t0,t1,slot,gold) in enumerate(LINES):
    fill = GOLD if gold else WHITE
    spr, inner = make_lyric_sprite(txt, size=88, fill=fill)
    # luminance locale sur le fond du slot (zone bas d'écran)
    bg = kenburns(canvases[slot], 0.5, seeds[slot])
    x = (W-spr.width)//2; y = H-300-spr.height
    zone = np.array(bg.crop((max(0,x), max(0,y), min(W,x+spr.width), min(H,y+spr.height))).convert('L'))
    lum = float(zone.mean())
    ban, pad = banner_for(inner, lum)
    sprites[i] = (spr, ban, pad, inner)

# --- titre intro + endcard (sprites) ---
def title_sprite():
    f = ImageFont.truetype(F_GV, 120)
    tmp=Image.new('RGBA',(10,10)); dt=ImageDraw.Draw(tmp)
    t1_="Yafoy t'es encore là"; t2_="Daïsky"
    f2 = ImageFont.truetype(F_GV, 76)
    b1=dt.textbbox((0,0),t1_,font=f); b2=dt.textbbox((0,0),t2_,font=f2)
    w = max(b1[2]-b1[0], b2[2]-b2[0])+160
    if w-160 > 980:
        f = ImageFont.truetype(F_GV, int(120*980/(b1[2]-b1[0]))); b1=dt.textbbox((0,0),t1_,font=f)
        w = max(b1[2]-b1[0], b2[2]-b2[0])+160
    h = (b1[3]-b1[1])+(b2[3]-b2[1])+200
    spr=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(spr)
    x1=(w-(b1[2]-b1[0]))//2-b1[0]; y1=60-b1[1]
    x2=(w-(b2[2]-b2[0]))//2-b2[0]; y2=60+(b1[3]-b1[1])+50-b2[1]
    for (x,y,t_,fo) in [(x1,y1,t1_,f),(x2,y2,t2_,f2)]:
        d.text((x+4,y+4),t_,font=fo,fill=(0,0,0,190))
        for dx,dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            d.text((x+dx,y+dy),t_,font=fo,fill=(30,20,5,230))
        d.text((x,y),t_,font=fo,fill=GOLD)
    return spr
TITLE = title_sprite()

def endcard_sprite():
    fb  = ImageFont.truetype(F_BOLD, 44)
    fs  = ImageFont.truetype(F_BOLD, 34)
    fgv = ImageFont.truetype(F_GV, 100)
    lines = [
        ("Yafoy t'es encore là", fgv, GOLD),
        ("Daïsky", fb, WHITE),
        ("Daïsky Prod / TechStein · Rock · 2026", fs, WHITE),
        ("229 01 61 16 24 08 · 229 01 49 11 49 51", fs, WHITE),
        ("daiskypro@proton.me", fs, WHITE),
        ("@daiskypro", fs, CYAN),
        ("⚡ DAÏSKY PROD — Wolof TechStein beat wê !", fs, AMBER),
    ]
    tmp=Image.new('RGBA',(10,10)); dt=ImageDraw.Draw(tmp)
    pad=60; wmax=0; hh=pad
    meas=[]
    for t_,fo,c in lines:
        b=dt.textbbox((0,0),t_,font=fo); meas.append(b)
        wmax=max(wmax,b[2]-b[0]); hh+=(b[3]-b[1])+34
    spr=Image.new('RGBA',(wmax+pad*2,hh+pad),(0,0,0,0)); d=ImageDraw.Draw(spr)
    y=pad
    for (t_,fo,c),b in zip(lines,meas):
        x=(spr.width-(b[2]-b[0]))//2-b[0]
        d.text((x+3,y+3-b[1]),t_,font=fo,fill=(0,0,0,190))
        d.text((x,y-b[1]),t_,font=fo,fill=c)
        y+=(b[3]-b[1])+34
    return spr
ENDCARD = endcard_sprite()

BADGE, BPOS = make_badge()
CTA, CPOS = make_cta()
SHARE = load_share()
pf = ImageFont.truetype(F_BOLD, 30)

# fenêtre partage : milieu ~122.5 -> fenêtre 123.2-126.2 (entre s26 fin 123 et PR2 127 : pile entre deux vers)
SH_T0, SH_T1 = 123.2, 126.2

import imageio_ffmpeg, subprocess
total = TOTAL
nfr = math.ceil(total*FPS)
proc = encode(OUT, total, ['-i', AUDIO], total-3)

fade_pix = None
for i in range(nfr):
    t = i/FPS
    s,u = bg_window(t)
    frame = kenburns(canvases[s], u, seeds[s])
    la = None
    # paroles (fenêtre décalée ADVANCE)
    for j,(txt,t0,t1,slot,g) in enumerate(LINES):
        d0,d1 = t0-ADVANCE, t1-ADVANCE
        if d0 <= t < d1:
            spr, ban, pad, inner = sprites[j]
            # vague sinusoïdale douce (ligne connectée)
            wave = int(4*math.sin(2*math.pi*0.9*t))
            # fondu in/out 0.35s
            a = min(1.0,(t-d0)/0.35, max(0.0,(d1-t)/0.35))
            a = max(0.0,min(1.0,a))
            x = (W-spr.width)//2; y = H-300-spr.height+wave
            bx = x+inner[0]-pad- (inner[0]); by=y+inner[1]-pad
            if a<1.0:
                ban2 = ban.copy(); ban2.putalpha(ban2.getchannel('A').point(lambda p:int(p*a)))
                spr2 = spr.copy(); spr2.putalpha(spr2.getchannel('A').point(lambda p:int(p*a)))
            else:
                ban2, spr2 = ban, spr
            frame.paste(ban2,(x+inner[0]-pad, y+inner[1]-pad), ban2)
            frame.paste(spr2,(x,y),spr2)
            break
    # titre intro
    if t < 11.0:
        a = 1.0 if t<9.0 else max(0.0,(11.0-t)/2.0)
        tt = TITLE if a>=1.0 else TITLE.copy()
        if a<1.0: tt.putalpha(tt.getchannel('A').point(lambda p:int(p*a)))
        frame.paste(tt, ((W-TITLE.width)//2, 150), tt)
    # endcard
    if t >= ENDCARD_T:
        a = min(1.0,(t-ENDCARD_T)/1.0)
        ec = ENDCARD if a>=1.0 else ENDCARD.copy()
        if a<1.0: ec.putalpha(ec.getchannel('A').point(lambda p:int(p*a)))
        frame.paste(ec, ((W-ENDCARD.width)//2, (H-ENDCARD.height)//2-60), ec)
    # icône partage mi-vidéo (pulse)
    if SH_T0 <= t < SH_T1:
        prog = (t-SH_T0)/(SH_T1-SH_T0)
        a = min(1.0, prog/0.15, (1.0-prog)/0.15); a=max(0.0,min(1.0,a))
        sc = 1.0+0.06*math.sin(2*math.pi*0.9*(t-SH_T0))
        sw,shh = int(SHARE.width*sc), int(SHARE.height*sc)
        sh2 = SHARE.resize((sw,shh), Image.BILINEAR)
        if a<1.0: sh2.putalpha(sh2.getchannel('A').point(lambda p:int(p*a)))
        sx,sy=(W-sw)//2, 620
        frame.paste(sh2,(sx,sy),sh2)
        d=ImageDraw.Draw(frame,'RGBA')
        pt='PARTAGE'; pw=d.textbbox((0,0),pt,font=pf)[2]
        d.text(((W-pw)//2+2, sy+shh+12+2), pt, font=pf, fill=(0,0,0,int(200*a)))
        d.text(((W-pw)//2, sy+shh+12), pt, font=pf, fill=(255,190,80,int(255*a)))
    # CTA 0-2 s (fade out 2.0->2.4)
    if t < 2.4:
        a = 1.0 if t<2.0 else (2.4-t)/0.4
        c2 = CTA if a>=1.0 else CTA.copy()
        if a<1.0: c2.putalpha(c2.getchannel('A').point(lambda p:int(p*a)))
        frame.paste(c2, CPOS, c2)
    # badge DSKY✓ en DERNIER
    frame.paste(BADGE, BPOS, BADGE)
    buf = io.BytesIO(); frame.save(buf,'JPEG',quality=90)
    proc.stdin.write(buf.getvalue())
    if i % (FPS*30) == 0: print(f'{t:6.1f}s / {total:.1f}', flush=True)

proc.stdin.close(); proc.wait()
print('RENDU OK ->', OUT)
