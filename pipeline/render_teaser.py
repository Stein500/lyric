# TEASER 9:16 — vidéo À PART ENTIÈRE (§17 v4.9) : 2 images IA retravaillées, hook 20 s
import sys, math, io
sys.path.insert(0,'pipeline')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from render_common import *
import subprocess, imageio_ffmpeg

OUT = 'livrables/teaser_Yafoy_9x16.mp4'
SRC = "livrables/Yafoy t'es encore là - Daïsky (Master).mp3"
ff = imageio_ffmpeg.get_ffmpeg_exe()
# extrait hook : refrain final explosif 210.0 -> 228.0 (18 s) + fade
T_IN, T_LEN = 210.0, 18.0
TOTAL = T_LEN + 2.0   # 2 s de silence paddé pour la carte finale
subprocess.run([ff,'-y','-ss',str(T_IN),'-t',str(T_LEN),'-i',SRC,'-af','afade=t=in:d=0.8','-c:a','pcm_s16le','work/teaser_audio.wav'],capture_output=True)

c1 = load_canvas('assets/raw/teaser/t01_hook.png')
c2 = load_canvas('assets/raw/teaser/t02_mystere.png')
BADGE,BPOS = make_badge(); CTA,CPOS = make_cta()

def txt_sprite(lines_spec, maxw=940):
    tmp=Image.new('RGBA',(10,10)); dt=ImageDraw.Draw(tmp)
    meas=[]; wmax=0; htot=40
    fonts=[]
    for t_,fp,sz,col in lines_spec:
        f=ImageFont.truetype(fp,sz)
        b=dt.textbbox((0,0),t_,font=f)
        if b[2]-b[0]>maxw:
            f=ImageFont.truetype(fp,int(sz*maxw/(b[2]-b[0])))
            b=dt.textbbox((0,0),t_,font=f)
        meas.append(b); fonts.append(f)
        wmax=max(wmax,b[2]-b[0]); htot+=(b[3]-b[1])+28
    spr=Image.new('RGBA',(wmax+120,htot+40),(0,0,0,0)); d=ImageDraw.Draw(spr)
    ImageDraw.Draw(spr).rounded_rectangle([0,0,spr.width-1,spr.height-1],radius=30,fill=(8,14,20,150))
    y=40
    for (t_,fp,sz,col),b,f in zip(lines_spec,meas,fonts):
        x=(spr.width-(b[2]-b[0]))//2-b[0]
        d.text((x+3,y+3-b[1]),t_,font=f,fill=(0,0,0,190))
        for dx,dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            d.text((x+dx,y+dy-b[1]),t_,font=f,fill=(10,16,24,220))
        d.text((x,y-b[1]),t_,font=f,fill=col)
        y+=(b[3]-b[1])+28
    return spr

S_BIENTOT = txt_sprite([("Bientôt...", F_GV, 110, GOLD)])
S_TITRE   = txt_sprite([("Yafoy t'es encore là", F_GV, 96, GOLD), ("Daïsky", F_BOLD, 40, WHITE)])
S_CLIP    = txt_sprite([("Le clip lyrics arrive", F_BOLD, 52, WHITE), ("Abonne-toi pour ne rien rater", F_BOLD, 38, CYAN)])
S_FINAL   = txt_sprite([("LIKE  ·  ABONNE-TOI  ·  COMMENTE", F_BOLD, 42, AMBER), ("@daiskypro — Wolof TechStein beat wê !", F_BOLD, 34, WHITE)])

proc = encode(OUT, TOTAL, ['-i','work/teaser_audio.wav'], TOTAL-2.5)
nfr = math.ceil(TOTAL*FPS)
for i in range(nfr):
    t = i/FPS
    # alternance dynamique des 2 images : t01 (0-7), t02 (7-13), t01 (13-20) — KB rapide
    if t < 7.0:    cv,seed,u = c1,0,(t)/7.0
    elif t < 13.0: cv,seed,u = c2,1,(t-7)/6.0
    else:          cv,seed,u = c1,2,(t-13)/7.0
    frame = kenburns(cv, u, seed)
    # flash blanc bref aux transitions (0.2 s)
    for tc in (7.0, 13.0):
        dtc = abs(t-tc)
        if dtc < 0.12:
            ov = Image.new('RGB',(W,H),(255,245,225))
            frame = Image.blend(frame, ov, 0.55*(1-dtc/0.12))
    # textes par fenêtres
    def paste_c(spr, y, a=1.0):
        s2 = spr if a>=1.0 else spr.copy()
        if a<1.0: s2.putalpha(s2.getchannel('A').point(lambda p:int(p*a)))
        frame.paste(s2, ((W-spr.width)//2, y), s2)
    if t < 4.0:
        a = min(1.0, t/0.5, max(0.0,(4.0-t)/0.5)); paste_c(S_BIENTOT, 340, max(0,a))
    elif t < 10.0:
        a = min(1.0,(t-4.0)/0.5, max(0.0,(10.0-t)/0.5)); paste_c(S_TITRE, 300, max(0,a))
    elif t < 15.0:
        a = min(1.0,(t-10.0)/0.5, max(0.0,(15.0-t)/0.5)); paste_c(S_CLIP, 340, max(0,a))
    else:
        a = min(1.0,(t-15.0)/0.5); paste_c(S_FINAL, H//2-120, a)
    # CTA 0-2 s (§5.2)
    if t < 2.4:
        a = 1.0 if t<2.0 else (2.4-t)/0.4
        c2c = CTA if a>=1.0 else CTA.copy()
        if a<1.0: c2c.putalpha(c2c.getchannel('A').point(lambda p:int(p*a)))
        frame.paste(c2c, CPOS, c2c)
    frame.paste(BADGE, BPOS, BADGE)
    buf = io.BytesIO(); frame.save(buf,'JPEG',quality=90)
    proc.stdin.write(buf.getvalue())
proc.stdin.close(); proc.wait()
print('TEASER OK ->', OUT)
