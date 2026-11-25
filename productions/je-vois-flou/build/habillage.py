# -*- coding: utf-8 -*-
"""Habillage WTBW : titre, filet orange, bandeau defilant, stickers, clochette, voile."""
import pathlib
from PIL import Image, ImageDraw, ImageFont
A = pathlib.Path(__file__).resolve().parents[1]/"assets"; A.mkdir(exist_ok=True)
W,H = 1080,1920
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CYAN=(0,229,255,255); ORANGE=(255,106,0,255); YELLOW=(255,212,0,255)
WHITE=(255,255,255,255); INK=(10,12,18,225)
def F(s): return ImageFont.truetype(B,s)

img=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
d.rectangle([0,0,W,9],fill=CYAN)
f1=F(70); t="JE VOIS FLOU"; tw=d.textlength(t,font=f1)
d.text(((W-tw)/2,268),t,font=f1,fill=WHITE,stroke_width=7,stroke_fill=(0,0,0,230))
d.rectangle([(W-tw)/2,352,(W+tw)/2,362],fill=ORANGE)
f3=F(40); a="WTBW"; aw=d.textlength(a,font=f3)
d.text(((W-aw)/2,372),a,font=f3,fill=YELLOW,stroke_width=5,stroke_fill=(0,0,0,230))
img.save(A/"hab-top.png")

txt="JE VOIS FLOU   •   WTBW   •   J'AVANCE DANS LA BOUE   •   "
ft=F(33); tmp=ImageDraw.Draw(Image.new("RGBA",(8,8)))
twd=int(tmp.textlength(txt,font=ft))+44
st=Image.new("RGBA",(twd,66),(0,0,0,0)); sd=ImageDraw.Draw(st)
sd.rounded_rectangle([0,0,twd-1,65],radius=14,fill=(0,0,0,160),outline=CYAN,width=3)
sd.text((22,15),txt,font=ft,fill=WHITE)
st.save(A/"hab-ticker.png")

img=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
items=[("LIKE LA VIDÉO",CYAN),("+ S'ABONNER",ORANGE),("COMMENTE",YELLOW)]
fs=F(30); ws=[int(d.textlength(t,font=fs))+50 for t,_ in items]
tot=sum(ws)+14*len(ws)+66; x=int((W-tot)/2); y=1452
for (t,c),wd in zip(items,ws):
    d.rounded_rectangle([x,y,x+wd,y+74],radius=37,fill=INK,outline=c,width=3)
    d.text((x+25,y+21),t,font=fs,fill=c); x+=wd+14
d.rounded_rectangle([x,y,x+66,y+74],radius=33,fill=INK,outline=YELLOW,width=3)
cx=x+33
d.arc([cx-15,y+17,cx+15,y+45],180,360,fill=YELLOW,width=4)
d.line([cx-15,y+31,cx-15,y+44],fill=YELLOW,width=4); d.line([cx+15,y+31,cx+15,y+44],fill=YELLOW,width=4)
d.line([cx-18,y+44,cx+18,y+44],fill=YELLOW,width=4); d.ellipse([cx-4,y+49,cx+4,y+56],fill=YELLOW)
img.save(A/"hab-stickers.png")

img=Image.new("RGBA",(W,H),(0,0,0,0)); px=img.load()
for y in range(560,1574):
    a = int(150*(y-560)/60) if y<620 else (150 if y<1300 else int(150*(1574-y)/274))
    a = max(0,min(150,a))
    for x in range(W): px[x,y]=(4,6,12,a)
img.save(A/"hab-scrim.png")
print("habillage: top, ticker, stickers, scrim")
