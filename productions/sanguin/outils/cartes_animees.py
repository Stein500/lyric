#!/usr/bin/env python3
"""Prototypes muets des cartes Sanguin. Pillow et imageio-ffmpeg requis."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import imageio_ffmpeg, math, subprocess

ROOT = Path(__file__).resolve().parent.parent
W,H,FPS=540,960,30
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)
def centered(d, y, text, size, color='white', bold=False):
    f=font(size,bold); d.text((W//2,y),text,font=f,fill=color,anchor='mt',stroke_width=0)
def heart(d,cx,cy,size,phase):
    # Animated hand-drawn heart outline, starts at top and is traced progressively.
    pts=[]
    for i in range(181):
        a=2*math.pi*i/180
        x=16*math.sin(a)**3
        y=13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a)
        pts.append((cx+x*size/34,cy-y*size/34))
    n=max(2,min(len(pts),int(len(pts)*min(1,max(0,phase)))))
    d.line(pts[:n], fill=(245,245,245), width=3, joint='curve')

def background(path):
    im=Image.open(path).convert('RGB').resize((600,1067),Image.Resampling.LANCZOS)
    im=ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(6))).enhance(.23)
    return im

def draw_card(bg,t,duration,kind):
    x=round(30+8*math.sin(t*.5)); y=round(53+8*math.cos(t*.48))
    im=bg.crop((x,y,x+W,y+H)); d=ImageDraw.Draw(im)
    d.line((85,155,455,155), fill=(120,120,120),width=1)
    d.line((85,735,455,735), fill=(120,120,120),width=1)
    centered(d,105,'WTBW',17,bold=True)
    if kind=='intro':
        # Soft 0.35-second crossfade between the two greetings.
        midpoint=duration/2
        a=max(0.0,min(1.0,(t-(midpoint-.175))/.35))
        ytitle=190+int(3*math.sin(t*1.1))
        for title,size,alpha in [('SALUT · WTBW',30,1-a),('BIENVENUE SUR WTBW',25,a)]:
            layer=Image.new('RGBA',(W,H)); ld=ImageDraw.Draw(layer)
            ld.text((W//2,ytitle),title,font=font(size,True),fill=(255,255,255,round(255*alpha)),anchor='mt')
            im.paste(layer,(0,0),layer)
        centered(d,244,'SANGUIN · DSKY',22,bold=True)
        centered(d,282,'Soutiens le son en douceur',14)
    else:
        centered(d,190+int(3*math.sin(t*1.1)),'MERCI · WTBW',34,bold=True)
        centered(d,245,"Merci d'avoir écouté",17)
        centered(d,282,'SANGUIN · DSKY',22,bold=True)
    labels=[('LIKE LA VIDÉO','Laisse un cœur si tu valides'),("CLIQUE SUR + POUR T’ABONNER",'Rejoins WTBW'),('COMMENTE SI TU AIMES !','Dis-nous ton vers préféré')]
    for i,(title,sub) in enumerate(labels):
        cy=420+i*105+round(4*math.sin(t*2.3+i)); cx=270+round(2*math.sin(t*1.8+i))
        d.rounded_rectangle((cx-195,cy-39,cx+195,cy+39),radius=21,fill=(17,19,22),outline=(112,112,112),width=1)
        ix=cx-158
        if i==0: heart(d,ix,cy,30,(t%2.8)/1.45)
        elif i==1:
            d.ellipse((ix-14,cy-14,ix+14,cy+14),outline='white',width=2)
            d.line((ix-8,cy,ix+8,cy),fill='white',width=3); d.line((ix,cy-8,ix,cy+8),fill='white',width=3)
        else:
            d.rounded_rectangle((ix-14,cy-11,ix+14,cy+9),radius=6,outline='white',width=2)
            d.line((ix-6,cy+9,ix-9,cy+15,ix+1,cy+9),fill='white',width=2)
        d.text((cx-124,cy-19),title,font=font(13,True),fill='white')
        d.text((cx-124,cy+4),sub,font=font(11),fill=(194,194,194))
    return im

def render(kind,source,frames):
    output=ROOT/'livrables'/f'APERCU-{kind}-muet.mp4'; bg=background(source); duration=frames/FPS
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    args=[ff,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-', '-an','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
    p=subprocess.Popen(args,stdin=subprocess.PIPE)
    try:
        for i in range(frames): p.stdin.write(draw_card(bg,i/FPS,duration,kind).tobytes())
    finally: p.stdin.close()
    if p.wait()!=0: raise RuntimeError('Échec encodage '+kind)
    print(output,frames,'frames')

if __name__=='__main__':
    render('intro',ROOT/'fonds/scene-01-ancre.png',148)
    render('outro',ROOT/'fonds/scene-35-aube.png',150)
