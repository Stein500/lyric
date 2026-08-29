#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MP3 nettoye + cover dediee + tags ID3 propres (charte Daïsky Prod / TechStein)."""
import os, subprocess, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

BASE=os.path.dirname(os.path.abspath(__file__))
RAW=os.path.join(BASE,"assets","raw","portrait")
GEN=os.path.join(BASE,"assets","gen")
LIVR=os.path.join(BASE,"livrables"); os.makedirs(LIVR,exist_ok=True)
WORK=os.path.join(BASE,"work"); os.makedirs(WORK,exist_ok=True)
AUDIO_IN=os.path.join(BASE,"..","Joyeux anniversaire Klo.mp3")
COVER=os.path.join(WORK,"cover.jpg")
FD="/usr/share/fonts/truetype/dejavu"
import imageio_ffmpeg; FF=imageio_ffmpeg.get_ffmpeg_exe()

def F(sz,bold=True):
    return ImageFont.truetype(os.path.join(FD,"DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),sz)

def enhance(im):
    im=ImageOps.exif_transpose(im).convert("RGB")
    im=ImageEnhance.Brightness(im).enhance(1.06)
    im=ImageEnhance.Contrast(im).enhance(1.09)
    im=ImageEnhance.Color(im).enhance(1.20)
    im=ImageEnhance.Sharpness(im).enhance(1.5)
    return im

def square_crop(im,s,vy=0.5):
    w,h=im.size; nh=int(s*h/w); im=im.resize((s,nh),Image.LANCZOS)
    y=int((nh-s)*vy); return im.crop((0,y,s,y+s))

def scrim(im,top_h=190,bot_h=300):
    w,h=im.size; ov=Image.new("L",(w,h),0); d=ImageDraw.Draw(ov)
    for i in range(top_h): d.line([(0,i),(w,i)],fill=int((1-i/top_h)*160))
    for i in range(bot_h): d.line([(0,h-bot_h+i),(w,h-bot_h+i)],fill=int((i/bot_h)**1.5*205))
    return Image.composite(Image.new("RGB",(w,h),(0,0,0)), im, ov)

def center(d,cx,y,txt,font,fill,stroke=(0,0,0),sw=0,ls=0):
    if ls:
        ws=[d.textlength(c,font=font) for c in txt]; tot=sum(ws)+ls*(len(txt)-1); x=cx-tot/2
        for c,wd in zip(txt,ws):
            d.text((x,y),c,font=font,fill=fill,stroke_width=sw,stroke_fill=stroke); x+=wd+ls
    else:
        bb=d.textbbox((0,0),txt,font=font,stroke_width=sw)
        d.text((cx-(bb[2]-bb[0])/2,y),txt,font=font,fill=fill,stroke_width=sw,stroke_fill=stroke)

# ------------------------------ COVER DEDIE 1080x1080 ------------------------------
def build_cover():
    S=1080
    bg=square_crop(Image.open(os.path.join(GEN,"gold_balloons.jpg")).convert("RGB"),S,0.40)
    bg=ImageEnhance.Brightness(bg).enhance(0.98)
    bg=scrim(bg,190,300).convert("RGBA")
    d=ImageDraw.Draw(bg)
    gold=(255,214,140); white=(255,255,255)
    # portrait cercle
    ph=enhance(Image.open(os.path.join(RAW,"IMG-20260827-WA0010.jpg")))
    D=560; cx,cy=S//2,430
    circ=square_crop(ph,D,0.18).convert("RGBA")
    mask=Image.new("L",(D,D),0); ImageDraw.Draw(mask).ellipse([0,0,D-1,D-1],fill=255)
    halo=Image.new("RGBA",(S,S),(0,0,0,0)); hd=ImageDraw.Draw(halo)
    for rr,al,wd in [(30,55,12),(17,110,9),(8,190,6)]:
        hd.ellipse([cx-D//2-rr,cy-D//2-rr,cx+D//2+rr,cy+D//2+rr],outline=(232,163,61,al),width=wd)
    bg.alpha_composite(halo.filter(ImageFilter.GaussianBlur(13)))
    bg.paste(circ,(cx-D//2,cy-D//2),mask)
    d.ellipse([cx-D//2,cy-D//2,cx+D//2,cy+D//2],outline=(255,228,175,255),width=9)
    # textes (aucun chevauchement)
    center(d,S//2,64,"JOYEUX ANNIVERSAIRE",F(50),gold,stroke=(70,38,0),sw=3,ls=10)
    center(d,S//2,738,"KLO",F(150),white,stroke=(0,0,0),sw=7)
    center(d,S//2,906,"Confiance ♥   •   30 août",F(46),gold,stroke=(60,32,0),sw=3)
    # badge en bas a gauche (zone libre)
    b=Image.new("RGBA",(S,S),(0,0,0,0)); bd=ImageDraw.Draw(b)
    t="DAÏSKY PROD"; f=F(30); bf=F(34)
    tb=bd.textbbox((0,0),t,font=f); bb=bd.textbbox((0,0),"⚡",font=bf)
    tw=tb[2]-tb[0]; bw=bb[2]-bb[0]; th=tb[3]-tb[1]; px,py,g=22,13,12
    pw=px*2+bw+g+tw; phh=max(th,bb[3]-bb[1])+py*2
    x0,y0=44,S-44-phh
    bd.rounded_rectangle([x0,y0,x0+pw,y0+phh],radius=phh//2,fill=(5,8,16,220),outline=(77,210,255,255),width=3)
    bd.text((x0+px,y0+(phh-(bb[3]-bb[1]))//2-bb[1]),"⚡",font=bf,fill=(77,210,255,255))
    bd.text((x0+px+bw+g,y0+(phh-th)//2-tb[1]),t,font=f,fill=white)
    bg.alpha_composite(b)
    bg.convert("RGB").save(COVER,quality=93)
    print("cover ->",COVER)

def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode!=0:
        print(r.stderr[-2000:]); raise SystemExit("ffmpeg erreur")
    return r

# ------------------------------ AUDIO NETTOYE --------------------------------
def clean_audio(out):
    p1=run([FF,"-hide_banner","-i",AUDIO_IN,"-af","loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-f","null","-"])
    m=json.loads("{"+p1.stderr.split("{")[-1].split("}")[0]+"}")
    print("loudness entree:",m["input_i"],"LUFS | TP",m["input_tp"])
    af=(f"loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:"
        f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
        f"measured_thresh={m['input_thresh']}:offset={m['target_offset']},"
        f"afade=t=in:st=0:d=0.35,afade=t=out:st=101.8:d=3.2,aresample=44100")
    run([FF,"-y","-i",AUDIO_IN,"-af",af,"-c:a","libmp3lame","-b:a","320k","-ar","44100","-ac","2",out])
    print("audio nettoye ->",out)

# ------------------------------ TAGS PROPRES ---------------------------------
def tag(path):
    from mutagen.id3 import (ID3, TIT2, TPE1, TPE2, TALB, TDRC, TCON, TRCK, TPOS,
                             TCOM, TENC, TCOP, TPUB, TLAN, COMM, APIC)
    tags=ID3(path)
    tags.clear()   # retire tout (dont les metadonnees Suno et l'ancienne cover)
    tags.add(TIT2(encoding=3,text="Joyeux Anniversaire Klo"))
    tags.add(TPE1(encoding=3,text="Daïsky"))
    tags.add(TPE2(encoding=3,text="Daïsky Prod · TechStein"))
    tags.add(TALB(encoding=3,text="Joyeux Anniversaire Klo (Single)"))
    tags.add(TDRC(encoding=3,text="2026-08-30"))
    tags.add(TCON(encoding=3,text="Afro-Pop"))
    tags.add(TRCK(encoding=3,text="1"))
    tags.add(TPOS(encoding=3,text="1"))
    tags.add(TLAN(encoding=3,text="fra"))
    tags.add(TCOM(encoding=3,text="TechStein"))
    tags.add(TPUB(encoding=3,text="Daïsky Prod / TechStein"))
    tags.add(TENC(encoding=3,text="Daïsky Prod"))
    tags.add(TCOP(encoding=3,text="© 2026 Daïsky Prod / TechStein"))
    tags.add(COMM(encoding=3,lang="fra",desc="",
        text="Joyeux anniversaire Klo / Confiance — 30 août. Wolof TechStein beat wê ! ⚡ Production Daïsky Prod / TechStein."))
    with open(COVER,"rb") as fp:
        tags.add(APIC(encoding=3,mime="image/jpeg",type=3,desc="Cover",data=fp.read()))
    tags.save(path,v2_version=3,v1=2)
    print("tags + cover ecrits")

if __name__=="__main__":
    build_cover()
    out=os.path.join(LIVR,"Klo_Joyeux_Anniversaire_CLEAN.mp3")
    clean_audio(out)
    tag(out)
    from mutagen.mp3 import MP3; from mutagen.id3 import ID3
    a=MP3(out); print("duree:",round(a.info.length,2),"s |",a.info.bitrate//1000,"kbps |",a.info.sample_rate,"Hz")
    t=ID3(out)
    for k in ("TIT2","TPE1","TPE2","TALB","TDRC","TCON","TRCK","TLAN","TCOM","TPUB","TCOP"):
        fr=t.get(k); print("  ",k,"=",fr.text[0] if fr is not None else None)
    ap=t.getall("APIC"); print("  APIC:", (f"{ap[0].mime} type={ap[0].type} {len(ap[0].data)//1024} Ko") if ap else "ABSENT")
    print("  COMM Suno restant:", [k for k in t.keys() if "TXXX" in k or (k=="COMM" and "suno" in str(t[k]))])
    print("TAILLE:",os.path.getsize(out)//1024,"Ko")
