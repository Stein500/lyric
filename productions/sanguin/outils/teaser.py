#!/usr/bin/env python3
"""15-second teaser from artist audio and lyric scenes, with independent vector motion."""
from pathlib import Path
from PIL import Image,ImageDraw
import imageio_ffmpeg,math,subprocess
root=Path(__file__).resolve().parent.parent
work=root.parent.parent/'.cache/sanguin-teaser';work.mkdir(parents=True,exist_ok=True)
ff=imageio_ffmpeg.get_ffmpeg_exe(); overlay=work/'overlay.mov'
p=subprocess.Popen([ff,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgba','-s','1080x130','-r','30','-i','-','-an','-c:v','qtrle',str(overlay)],stdin=subprocess.PIPE)
try:
 for i in range(450):
  t=i/30; im=Image.new('RGBA',(1080,130));d=ImageDraw.Draw(im)
  for k,cx in enumerate((200,880)):
   points=[];phase=(t+k*.6)%2.8; length=max(2,min(181,int(181*min(1,phase/1.15))))
   for j in range(length):
    a=2*math.pi*j/180; x=16*math.sin(a)**3; y=13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a)
    points.append((cx+x*.95,65-y*.95))
   d.line(points,fill=(255,255,255,180),width=3,joint='curve')
   for j in range(3):
    dx=(j-1)*28;dy=-26+int(4*math.sin(t*2+j+k));opacity=int(80+60*(.5+.5*math.sin(t*2.5+j)))
    d.ellipse((cx+dx-1,65+dy-1,cx+dx+1,65+dy+1),fill=(255,255,255,opacity))
  p.stdin.write(im.tobytes())
finally:p.stdin.close()
if p.wait(): raise RuntimeError('overlay failed')
out=root/'livrables/SANGUIN-DSKY-TEASER-15s.mp4'
source=root/'livrables/SANGUIN-DSKY-WTBW-9x16-V1.mp4'
subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-ss','24.166667','-i',str(source),'-i',str(overlay),'-filter_complex','[0:v][1:v]overlay=0:145:shortest=1,setsar=1,format=yuv420p[v]','-map','[v]','-map','0:a:0','-t','15','-r','30','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:v','libx264','-preset','veryfast','-crf','22','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(out)],check=True)
print(out)
