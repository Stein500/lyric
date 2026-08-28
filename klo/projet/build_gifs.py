#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GIFs d'anniversaire pour KLO (boucle parfaite, sans son) + portraits ameliores.
- Photos d'origine retouchees (couleur/lumiere/nettete, visage intact).
- Carte photo arrondie sur fond festif genere.
- Animation : zoom doux sinusoidal (boucle) + etincelles qui montent (boucle).
- Texte de voeux en dur (PIL) + badge DAISKY PROD statique.
Sortie 540x960, ~12 fps, GIF 256 couleurs optimise.
"""
import os, math, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops

BASE = os.path.dirname(os.path.abspath(__file__))
RAW  = os.path.join(BASE, "assets", "raw", "portrait")
GEN  = os.path.join(BASE, "assets", "gen")
GIFDIR = os.path.join(BASE, "livrables", "gifs")
ENHDIR = os.path.join(BASE, "livrables", "photos_ameliorees")
os.makedirs(GIFDIR, exist_ok=True); os.makedirs(ENHDIR, exist_ok=True)
FD = "/usr/share/fonts/truetype/dejavu"

W, H = 540, 960
NFR, FPSG = 30, 12          # 30 frames @12fps = 2.5 s, boucle parfaite
DUR = int(1000/FPSG)

def F(sz, bold=True, serif=False):
    n = "DejaVuSerif-Bold.ttf" if serif else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(os.path.join(FD, n), sz)

# ---------------------------------------------------------------------------
def cover(im, w, h):
    im = im.convert("RGB"); ir = im.size[0]/im.size[1]; sr = w/h
    if ir > sr: nh=h; nw=int(h*ir)
    else:       nw=w; nh=int(w/ir)
    im = im.resize((nw,nh), Image.LANCZOS)
    x=(nw-w)//2; y=(nh-h)//2
    return im.crop((x,y,x+w,y+h))

def enhance(im):
    """Retouche globale : couleurs, lumiere, contraste, nettete. Visage intact."""
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.09)
    im = ImageEnhance.Color(im).enhance(1.20)
    im = ImageEnhance.Sharpness(im).enhance(1.45)
    return im

def vignette(im, strength=0.35):
    w,h = im.size
    mask = Image.new("L",(w,h),0); d=ImageDraw.Draw(mask)
    d.ellipse([-w*0.25,-h*0.18,w*1.25,h*1.18], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(w*0.12))
    dark = Image.new("RGB",(w,h),(0,0,0))
    return Image.composite(im, dark, mask.point(lambda p:int(255-(255-p)*strength)))

def rounded_mask(size, rad):
    m=Image.new("L",size,0); d=ImageDraw.Draw(m)
    d.rounded_rectangle([0,0,size[0]-1,size[1]-1],radius=rad,fill=255); return m

def scrim_bottom(im, a0=170, hgt=380):
    ov=Image.new("L",(W,H),0); d=ImageDraw.Draw(ov)
    for i in range(hgt):
        a=int(a0*((i/hgt)**1.7)); d.line([(0,H-hgt+i),(W,H-hgt+i)],fill=a)
    black=Image.new("RGB",(W,H),(0,0,0))
    return Image.composite(black, im, ov)

def glow_dot(r, color):
    """sprite etincelle : coeur vif + halo."""
    s=r*8
    img=Image.new("RGBA",(s,s),(0,0,0,0)); d=ImageDraw.Draw(img)
    cx=cy=s//2
    for rr,al in [(r*3.2,40),(r*2.1,80),(r*1.3,150),(r,255)]:
        c=color+(al,)
        d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr], fill=c)
    return img.filter(ImageFilter.GaussianBlur(r*0.5))

def draw_center(d, cy, text, font, fill, stroke=(0,0,0), sw=3, ls=0):
    if ls:  # letter spacing
        widths=[d.textlength(ch,font=font) for ch in text]
        total=sum(widths)+ls*(len(text)-1)
        x=(W-total)/2
        for ch,wd in zip(text,widths):
            d.text((x,cy),ch,font=font,fill=fill,stroke_width=sw,stroke_fill=stroke)
            x+=wd+ls
    else:
        bb=d.textbbox((0,0),text,font=font,stroke_width=sw)
        d.text(((W-(bb[2]-bb[0]))/2, cy), text, font=font, fill=fill,
               stroke_width=sw, stroke_fill=stroke)
    return d.textbbox((0,0),text,font=font,stroke_width=sw)[3]-d.textbbox((0,0),text,font=font,stroke_width=sw)[1]

def badge_layer():
    img=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
    txt="DAÏSKY PROD"; f=F(19,True); bolt=F(22,True)
    tb=d.textbbox((0,0),txt,font=f); bb=d.textbbox((0,0),"⚡",font=bolt)
    tw=tb[2]-tb[0]; bw=bb[2]-bb[0]; th=tb[3]-tb[1]
    px,py,gap=16,9,8
    pw=px*2+bw+gap+tw; ph=max(th,bb[3]-bb[1])+py*2
    x0,y0=22,H-22-ph
    d.rounded_rectangle([x0,y0,x0+pw,y0+ph],radius=ph//2,fill=(5,8,16,210),outline=(77,210,255,255),width=2)
    d.text((x0+px, y0+(ph-(bb[3]-bb[1]))//2-bb[1]), "⚡", font=bolt, fill=(77,210,255,255))
    d.text((x0+px+bw+gap, y0+(ph-th)//2-tb[1]), txt, font=f, fill=(245,249,255,255))
    return img

# ---------------------------------------------------------------------------
# Sauvegarde des 9 portraits ameliores
# ---------------------------------------------------------------------------
def export_enhanced():
    for f in sorted(glob.glob(os.path.join(RAW,"*.jpg"))):
        im = vignette(enhance(Image.open(f)), 0.18)
        out=os.path.join(ENHDIR, "Klo_"+os.path.basename(f).replace("IMG-20260827-",""))
        im.save(out, quality=92)
    print("portraits ameliores:", len(glob.glob(os.path.join(ENHDIR,"*.jpg"))))

# ---------------------------------------------------------------------------
GIFS = [
 {"out":"Klo_GIF1_FestifOr.gif", "bg":"gold_balloons.jpg", "pho":"WA0010.jpg",
  "particle":(255,209,120), "halo":(232,163,61),
  "lines":[("JOYEUX ANNIVERSAIRE",(255,214,140),26,True,6),("KLO",(255,255,255),64,True,0),("Confiance ♥",(255,190,120),28,False,0)]},
 {"out":"Klo_GIF2_ReineCouronne.gif", "bg":"crown.jpg", "pho":"WA0002.jpg",
  "particle":(255,170,220), "halo":(214,64,170),
  "lines":[("JOYEUX ANNIVERSAIRE",(255,205,130),26,True,6),("KLO",(255,255,255),64,True,0),("Notre reine du jour",(255,170,215),27,False,0)]},
 {"out":"Klo_GIF3_NuitCyan.gif", "bg":"cyan_balloons.jpg", "pho":"WA0004.jpg",
  "particle":(140,225,255), "halo":(77,210,255),
  "lines":[("JOYEUX ANNIVERSAIRE",(140,225,255),26,True,6),("KLO",(255,255,255),64,True,0),("Ma lumière",(170,235,255),28,False,0)]},
 {"out":"Klo_GIF4_Party.gif", "bg":"confetti.jpg", "pho":"WA0009.jpg",
  "particle":(255,120,200), "halo":(245,102,200),
  "lines":[("JOYEUX ANNIVERSAIRE",(120,225,255),26,True,6),("KLO",(255,255,255),64,True,0),("Confiance & bonheur ♥",(255,150,205),26,False,0)]},
]

def build_gif(g):
    bg0 = cover(Image.open(os.path.join(GEN,g["bg"])), W, H)
    ph  = vignette(enhance(Image.open(os.path.join(RAW,"IMG-20260827-"+g["pho"]))), 0.0)
    # carte photo
    cw,ch = 440, 587
    card = cover(ph, cw, ch); rad=34
    cmask = rounded_mask((cw,ch), rad)
    ccy = 372  # centre vertical de la carte (laisse place au texte en bas sur le voile)
    badge = badge_layer()
    # etincelles
    import random; rnd=random.Random(7)
    parts=[]
    sprites={r:glow_dot(r,g["particle"]) for r in (3,5,7)}
    for _ in range(34):
        r=rnd.choice([3,5,7]); k=rnd.choice([1,1,2])
        parts.append({"x":rnd.uniform(0,W),"y0":rnd.uniform(0,H),"r":r,"k":k,
                      "ph":rnd.uniform(0,2*math.pi),"sp":sprites[r]})
    frames=[]
    for fi in range(NFR):
        ph_a = 2*math.pi*fi/NFR
        zoom = 1.0 + 0.045*(1-math.cos(ph_a))/2     # 1.00 -> 1.0225 -> 1.00 (boucle)
        bg = bg0.resize((int(W*zoom), int(H*zoom)), Image.LANCZOS)
        bx=(bg.size[0]-W)//2; by=(bg.size[1]-H)//2
        frame = bg.crop((bx,by,bx+W,by+H)).convert("RGBA")
        # carte avec halo
        cz = 1.0 + 0.02*(1-math.cos(ph_a))/2
        cw2,ch2=int(cw*cz),int(ch*cz)
        cardz = card.resize((cw2,ch2), Image.LANCZOS)
        cmz  = cmask.resize((cw2,ch2), Image.LANCZOS)
        cx0,cy0=(W-cw2)//2, int(ccy-ch2/2)
        glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
        hc=g["halo"]
        for rr,aa in [(26,40),(16,70),(8,120)]:
            gd.rounded_rectangle([cx0-rr,cy0-rr,cx0+cw2+rr,cy0+ch2+rr],radius=rad+rr,
                                 outline=hc+(aa,),width=6)
        frame.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
        frame.paste(cardz,(cx0,cy0),cmz)
        od=ImageDraw.Draw(frame)
        od.rounded_rectangle([cx0,cy0,cx0+cw2,cy0+ch2],radius=rad,outline=(255,255,255,235),width=3)
        # etincelles qui montent (boucle : k tours complets sur N frames)
        for p in parts:
            y = (p["y0"] - (p["k"]*H/NFR)*fi) % H
            tw = 0.55+0.45*math.sin(ph_a*2 + p["ph"])
            sp = p["sp"].copy()
            a = sp.getchannel("A").point(lambda v:int(v*max(0.15,tw)))
            sp.putalpha(a)
            frame.alpha_composite(sp,(int(p["x"]-sp.size[0]/2), int(y-sp.size[1]/2)))
        # voile bas + texte
        frame = scrim_bottom(frame.convert("RGB"), 175, 360).convert("RGBA")
        frame.alpha_composite(badge)
        d=ImageDraw.Draw(frame)
        y=H-272
        for (txt,col,sz,bold,ls) in g["lines"]:
            fnt=F(sz,bold)
            hh=draw_center(d,y,txt,fnt,col+(255,),stroke=(0,0,0,255),sw=3 if sz<40 else 4,ls=ls)
            y += hh + (10 if sz<40 else 6)
        frames.append(frame.convert("RGB"))
    # quantisation partagee
    pal = frames[0].quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
    q = [frames[0].quantize(palette=pal, dither=Image.FLOYDSTEINBERG)]
    for fr in frames[1:]:
        q.append(fr.quantize(palette=pal, dither=Image.FLOYDSTEINBERG))
    out=os.path.join(GIFDIR,g["out"])
    q[0].save(out, save_all=True, append_images=q[1:], loop=0, duration=DUR,
              optimize=True, disposal=2)
    print(f"{g['out']}: {os.path.getsize(out)//1024} Ko")

if __name__=="__main__":
    export_enhanced()
    for g in GIFS: build_gif(g)
    print("GIFs OK ->", GIFDIR)
