# -*- coding: utf-8 -*-
"""Effet VAGUES : paroles ondulantes type brume. Sortie rawvideo RGBA 1080x840 (bande y 560..1400).
Usage: python3 waves.py <debut_s> <duree_s> > flux.raw
"""
import json, math, pathlib, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = pathlib.Path(__file__).resolve().parents[1]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BW, BH, BAND_TOP, FPS = 1080, 840, 560, 30
SIZE, MAXW, Y_FIRST, LINE_GAP = 60, 740, 1010, 78
AMP, WL, SPEED, RISE, MIST = 9.0, 330.0, 2.3, 56.0, 1.1

def wrap(t, f):
    out, cur = [], ""
    for w in t.split():
        c = (cur+" "+w).strip()
        if f.getlength(c) <= MAXW: cur = c
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    if len(out) > 2: out = [out[0], " ".join(out[1:])]
    return out

class S:
    def __init__(self):
        self.f = ImageFont.truetype(FONT, SIZE); self.d = {}
    def get(self, ch):
        s = self.d.get(ch)
        if s is not None: return s
        w = int(self.f.getlength(ch))+32; h = SIZE*2+44
        mk = Image.new("L",(w,h),0)
        ImageDraw.Draw(mk).text((16,20),ch,font=self.f,fill=255,stroke_width=7,stroke_fill=110)
        s = np.array(mk, np.uint8); self.d[ch]=s; return s

def layout(t, f):
    out=[]
    for li,ln in enumerate(wrap(t,f)):
        wt = sum(f.getlength(c) for c in ln); x = 540-wt/2; y = Y_FIRST+li*LINE_GAP
        for c in ln:
            if c != " ": out.append((c,x,y))
            x += f.getlength(c)
    return out

def main():
    start, dur = float(sys.argv[1]), float(sys.argv[2])
    o = sys.stdout.buffer
    m = json.load(open(ROOT/"verses_map.json",encoding="utf-8"))
    sp = S()
    cache = {k:(layout(v["texte_affiche"],sp.f), v["debut_source"], v["fin_mesuree"]-v["debut_source"])
             for k,v in enumerate(m["verses"])}
    for fr in range(int(round(dur*FPS))):
        t = start+fr/FPS
        k = next((i for i,v in enumerate(m["verses"]) if v["debut_source"]<=t<v["fin_mesuree"]), None)
        ga = np.zeros((BH,BW), np.uint8)
        if k is not None:
            pos, ts, d = cache[k]; age = t-ts
            prog = min(1.0, max(0.0, age/max(d,0.30)))
            rise = (0.5-prog)*RISE
            a = 1.0
            if age < 0.16: a = age/0.16
            if d-age < 0.24: a = min(a, max(0.0,(d-age)/0.24))
            for ch,x,y in pos:
                s = sp.get(ch); h,w = s.shape
                ph = (x/WL)*2*math.pi + t*SPEED
                yy = int(round(y + AMP*math.sin(ph) + rise - BAND_TOP - 20))
                xx = int(round(x + 2.0*math.cos(ph*0.7) - 16))
                x0,y0 = max(0,xx), max(0,yy); x1,y1 = min(BW,xx+w), min(BH,yy+h)
                if x1<=x0 or y1<=y0: continue
                ga[y0:y1,x0:x1] = np.maximum(ga[y0:y1,x0:x1], s[y0-yy:y1-yy, x0-xx:x1-xx])
            img = Image.fromarray(ga,"L").filter(ImageFilter.GaussianBlur(MIST))
            if a < 1.0: img = img.point(lambda v: int(v*max(0.0,a)))
            ga = np.asarray(img, np.uint8)
        buf = np.zeros((BH,BW,4), np.uint8)
        buf[...,0]=255; buf[...,1]=246; buf[...,2]=178; buf[...,3]=ga
        o.write(buf.tobytes())
    o.flush()
if __name__=="__main__": main()
