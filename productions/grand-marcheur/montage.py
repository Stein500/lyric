#!/usr/bin/env python3
"""Montage provisoire, sans altération du maître ; teaser à vérifier à l'écoute."""
from pathlib import Path
import json, subprocess, math
from outils import ffmpeg_exe
from PIL import Image, ImageDraw, ImageFont, ImageOps
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
OUT=P/'livraison'; OUT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def card(source,dest,kind):
    im=ImageOps.fit(Image.open(source).convert('RGB'),(1080,1920),method=Image.Resampling.LANCZOS,centering=(.5,0))
    d=ImageDraw.Draw(im)
    def text(y,s,size):
        font=ImageFont.truetype(FONT,size)
        d.text((540,y),s,font=font,anchor='mt',fill='white',stroke_width=3,stroke_fill='#1c1933')
    if kind=='cover':
        text(175,'GRAND',92); text(285,'MARCHEUR',92); text(1500,'DSKY WTBW',56)
    elif kind=='intro':
        text(640,'GRAND MARCHEUR',66); text(755,'DSKY WTBW',45)
    else:
        text(710,'MERCI · WTBW',68); text(830,'GRAND MARCHEUR',49); text(920,'DSKY WTBW',40)
    im.save(dest,quality=95,subsampling=0)
card(P/'assets/cover-brut.jpg',OUT/'cover-grand-marcheur.jpg','cover')
card(P/'assets/ancre/ancre-gospel.jpg',P/'assets/intro.jpg','intro')
card(P/'assets/cover-brut.jpg',P/'assets/outro.jpg','outro')
data=json.loads((P/'timeline.json').read_text())
# Quantize boundaries once to nearest frame, preserving 30 fps throughout.
items=[(P/'assets/intro.jpg',0,round(1.34*30))]
for v in data['vers']:
    items.append((P/v['image_cuite'],round(v['debut_source']*30),round(v['fin_estimee']*30)))
items.append((P/'assets/outro.jpg',round(220.07*30),round(225.07*30)))
assert all(items[i][2]==items[i+1][1] for i in range(len(items)-1))
# Uniform JPEG geometry avoids filter reinitialization at the intro/outro boundaries.
work=ROOT/'work'/'grand-marcheur-normalises'; work.mkdir(parents=True,exist_ok=True)
cache={}
for path,_,_ in items:
    if path not in cache:
        dst=work/f'{len(cache):02d}.jpg'
        ImageOps.fit(Image.open(path).convert('RGB'),(1100,1956),method=Image.Resampling.LANCZOS,centering=(.5,0)).save(dst,quality=96,subsampling=0)
        cache[path]=dst
items=[(cache[path],a,b) for path,a,b in items]
concat=P/'montage-images.ffconcat' 
with concat.open('w') as f:
    f.write('ffconcat version 1.0\n')
    for path,start,end in items:
        f.write("file '"+str(path).replace("'", "'\\''")+"'\noption framerate 30\nduration %.9f\n"%((end-start)/30))
    f.write("file '"+str(items[-1][0])+"'\noption framerate 30\n")
ff=ffmpeg_exe()[0]
# Gentle movement applies to the entire cooked image, keeping lettering sharp and visible.
font=FONT.replace(':','\\:')
filt=("fps=30,crop=1080:1920:x='10+8*sin(t/5)':y='18+14*sin(t/6)',setsar=1,"
      +f"drawtext=fontfile={font}:text='DSKY WTBW':fontcolor=white:fontsize=32:borderw=2:bordercolor=black@0.6:x=72:y=165:alpha='0.72*min(1,min(mod(t,5.6)/0.4,(2.8-mod(t,5.6))/0.4))':enable='lt(mod(t,5.6),2.8)',"
      +f"drawtext=fontfile={font}:text='WTBW':fontcolor=white:fontsize=32:borderw=2:bordercolor=black@0.6:x=72:y=165:alpha='0.72*min(1,min((mod(t,5.6)-2.8)/0.4,(5.6-mod(t,5.6))/0.4))':enable='gte(mod(t,5.6),2.8)',"
      +f"drawtext=fontfile={font}:text='AVANCE À TON RYTHME':fontcolor=white@0.88:fontsize=25:borderw=2:bordercolor=black@0.6:x=72:y=1470:enable='lt(t,220.07)',"
      "drawbox=x=72:y=1530:w=750:h=4:color=white@0.25:t=fill:enable='lt(t,220.07)',"
      "drawbox=x=72:y=1530:w='750*min(t/220.07,1)':h=4:color=0xffcf77@0.9:t=fill:enable='lt(t,220.07)',format=yuv420p")
# drawbox width cannot depend on time in this filter; progress drawn with moving crop instead below.
filt=filt.replace("drawbox=x=72:y=1530:w='750*min(t/220.07,1)':h=4:color=0xffcf77@0.9:t=fill:enable='lt(t,220.07)',","")
# Dynamic progress line: drawtext underline-like bar via clip/reveal of a pre-rendered transparent image not needed here;
# the moving marker represents song progress.
filt=filt.replace('format=yuv420p',f"drawtext=fontfile={font}:text='●':fontcolor=0xffcf77:fontsize=20:x='72+740*min(t/220.07,1)':y=1518:enable='lt(t,220.07)',format=yuv420p")
cmd=[ff,'-hide_banner','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(ROOT/'Grand marcheur 2.mp3'),'-filter_complex',f'[0:v]{filt}[v];[1:a:0]apad,atrim=duration=225.066667[a]','-map','[v]','-map','[a]','-frames:v','6752','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(OUT/'grand-marcheur-complet.mp4')]
subprocess.run(cmd,check=True)
# Preview teaser: exact frame count and audio independently encoded from master.
subprocess.run([ff,'-hide_banner','-y','-ss','155.96','-i',str(OUT/'grand-marcheur-complet.mp4'),'-ss','155.96','-i',str(ROOT/'Grand marcheur 2.mp3'),'-map','0:v:0','-map','1:a:0','-frames:v','450','-t','15','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(OUT/'grand-marcheur-teaser-PROVISOIRE.mp4')],check=True)
