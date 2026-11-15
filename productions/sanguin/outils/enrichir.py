#!/usr/bin/env python3
"""Add a moving WTBW ticker, drawing hearts and a progress line to V1, without touching lyric artwork."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg,math,subprocess
ROOT=Path(__file__).resolve().parent.parent
REPO=ROOT.parent.parent
WORK=REPO/'.cache'/'sanguin-enrichi';WORK.mkdir(parents=True,exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe(); FPS=30; TOTAL=5334; FIRST=4.93; END=172.8
FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24)
MESSAGE="LIKE LA VIDÉO   ·   CLIQUE SUR + POUR T'ABONNER   ·   COMMENTE SI TU AIMES !   ·   WTBW   ·   "

def encoder(path,w,h):
 return subprocess.Popen([FF,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{w}x{h}','-r','30','-i','-','-an','-c:v','qtrle',str(path)],stdin=subprocess.PIPE)

def make_overlays():
 top=WORK/'top.mov'; bar=WORK/'progress.mov'; a=encoder(top,1080,150); b=encoder(bar,1080,12)
 width=round(FONT.getlength(MESSAGE)); xs=list(range(-1,4))
 try:
  for i in range(TOTAL):
   t=i/FPS; im=Image.new('RGBA',(1080,150));d=ImageDraw.Draw(im)
   # Contours de cœurs tracés progressivement, à côté du badge, sans toucher les paroles.
   for k,cx in enumerate((155,925)):
    pts=[];phase=((t-FIRST)+k*.5)%3.6;count=max(2,min(181,round(181*min(1,phase/1.3))))
    scale=.9*(1+.055*math.sin(t*2.4+k))
    for j in range(count):
     angle=2*math.pi*j/180; xx=16*math.sin(angle)**3;yy=13*math.cos(angle)-5*math.cos(2*angle)-2*math.cos(3*angle)-math.cos(4*angle)
     pts.append((cx+xx*scale,22-yy*scale))
    d.line(pts,fill=(245,245,245,185),width=3,joint='curve')
    for j in range(3):
     px=cx+(j-1)*28; py=42+5*math.sin(t*2+j+k); v=110+round(80*(.5+.5*math.sin(t*2.8+j)))
     d.ellipse((px-1,py-1,px+1,py+1),fill=(255,255,255,v))
   # Bandeau transparent et masqué aux côtés : pas de plaque sur l'image ni sur les paroles.
   strip=Image.new('RGBA',(720,48)); sd=ImageDraw.Draw(strip);offset=int((t-FIRST)*63)%width
   for k in xs:
    sd.text((k*width-offset,9),MESSAGE,font=FONT,fill=(245,245,245,210),stroke_width=2,stroke_fill=(0,0,0,200))
   im.alpha_composite(strip,(180,76));a.stdin.write(im.tobytes())
   # Filet de progression à y=195 : le placement à y=1560 recouvrait des paroles peintes.
   line=Image.new('RGBA',(1080,12));ld=ImageDraw.Draw(line);ld.rectangle((170,4,910,7),fill=(245,245,245,48))
   progress=max(0,min(1,(t-FIRST)/(END-FIRST)))
   ld.rectangle((170,2,170+int(740*progress),9),fill=(245,245,245,210))
   b.stdin.write(line.tobytes())
 finally:
  a.stdin.close();b.stdin.close()
 if a.wait() or b.wait(): raise RuntimeError('Échec des animations')
 return top,bar

def main():
 top,bar=make_overlays();src=ROOT/'livrables/SANGUIN-DSKY-WTBW-9x16-V1.mp4';out=ROOT/'livrables/SANGUIN-DSKY-COMPLET-ENRICHI.mp4'
 f="[0:v][1:v]overlay=0:145:enable='between(t,4.93,172.8)'[a];[a][2:v]overlay=0:195:enable='between(t,4.93,172.8)',setsar=1,format=yuv420p[v]"
 subprocess.run([FF,'-y','-hide_banner','-loglevel','error','-i',str(src),'-i',str(top),'-i',str(bar),'-filter_complex',f,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-movflags','+faststart',str(out)],check=True)
 print('Rendu :',out,flush=True)
if __name__=='__main__': main()
