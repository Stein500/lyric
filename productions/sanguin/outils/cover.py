#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
root=Path(__file__).resolve().parent.parent
im=Image.open(root/'fonds/cover-tiktok.png').convert('RGB')
im=ImageOps.fit(im,(1080,1920),method=Image.Resampling.LANCZOS,centering=(.5,0))
d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
sans='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f=ImageFont.truetype(font,140)
while d.textbbox((0,0),'SANGUIN',font=f,stroke_width=3)[2]>900:
 f=ImageFont.truetype(font,f.size-2)
d.text((540,1280),'SANGUIN',font=f,anchor='mm',fill='white',stroke_width=3,stroke_fill='black')
d.line((250,1430,830,1430),fill=(190,190,190),width=2)
d.text((540,1480),'D S K Y',font=ImageFont.truetype(sans,54),anchor='mm',fill='white',stroke_width=2,stroke_fill='black')
d.line((250,1530,830,1530),fill=(190,190,190),width=2)
d.text((540,1580),'WTBW',font=ImageFont.truetype(sans,32),anchor='mm',fill=(230,230,230),stroke_width=2,stroke_fill='black')
im.save(root/'livrables/COVER-SANGUIN-1080x1920.jpg',quality=95,subsampling=0)
