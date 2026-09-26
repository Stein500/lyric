#!/usr/bin/env python3
"""Build the requested covers from existing approved art; no new face generation."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT=Path(__file__).resolve().parents[3]
PROJECT=ROOT/'vivi-oor/production'
OUT=PROJECT/'livrables'
FONTS=PROJECT/'assets/fonts'
RESAMPLE=Image.Resampling.LANCZOS
TITLE='Vivi OOR'
ARTIST='Daïsky'


def font(size,script=False,bold=False):
    filename='GreatVibes-Regular.ttf' if script else ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')
    return ImageFont.truetype(str(FONTS/filename),round(size))


def centered_text(canvas,text,center,size,script=False,color='#ffedd1',max_width=None,shadow=True,stroke=0):
    f=font(size,script=script,bold=not script)
    while True:
        box=f.getbbox(text,stroke_width=stroke)
        if max_width is None or box[2]-box[0]<=max_width: break
        size-=1;f=font(size,script=script,bold=not script)
    pad=max(8,round(canvas.width*.012))
    w,h=box[2]-box[0],box[3]-box[1]
    sprite=Image.new('RGBA',(w+pad*2,h+pad*2))
    d=ImageDraw.Draw(sprite)
    if shadow:
        sh=Image.new('RGBA',sprite.size);sd=ImageDraw.Draw(sh)
        sd.text((pad-box[0],pad-box[1]+2),text,font=f,fill=(12,7,12,220),stroke_width=max(1,stroke+2))
        sh=sh.filter(ImageFilter.GaussianBlur(max(1,canvas.width/550)))
        sprite.alpha_composite(sh)
    d=ImageDraw.Draw(sprite)
    d.text((pad-box[0],pad-box[1]),text,font=f,fill=color,stroke_width=stroke,stroke_fill=color)
    position=(round(center[0]-sprite.width/2),round(center[1]-sprite.height/2))
    canvas.alpha_composite(sprite,position)
    return [position[0]+pad,position[1]+pad,position[0]+pad+w,position[1]+pad+h]


def tracking(canvas,text,cx,top,size,spacing,color):
    f=font(size)
    widths=[f.getlength(c) for c in text]
    width=sum(widths)+spacing*(len(text)-1)
    d=ImageDraw.Draw(canvas);x=cx-width/2
    for c,tw in zip(text,widths):
        d.text((x,top),c,font=f,fill=color,stroke_width=0);x+=tw+spacing
    return [cx-width/2,top,cx+width/2,top+size*1.25]


def flag(canvas,cx,cy,width):
    w=round(width);h=round(w*.25);x=round(cx-w/2);y=round(cy-h/2)
    d=ImageDraw.Draw(canvas)
    d.rectangle((x,y,x+w/3,y+h),fill='#008751')
    d.rectangle((x+w/3,y,x+w,y+h/2),fill='#fcd116')
    d.rectangle((x+w/3,y+h/2,x+w,y+h),fill='#e8112d')


def shade(im,landscape=False):
    w,h=im.size
    yy=np.linspace(0,1,h)[:,None]
    xx=np.linspace(0,1,w)[None,:]
    # A soft editorial grade, darker where typography sits, never a hard strip.
    a=.20+.25*np.exp(-((yy-.57)/.27)**2)+.16*yy
    a=np.broadcast_to(a,(h,w)).copy()
    if landscape:a+=.22*(1-xx)
    layer=Image.new('RGBA',(w,h),(27,14,24))
    layer.putalpha(Image.fromarray(np.clip(a*255,0,190).astype('uint8')))
    im=im.convert('RGBA');im.alpha_composite(layer)
    return im


def still_cover(size):
    w,h=size
    base=Image.open(ROOT/'vivi-oor/assets/backgrounds/01_invitation.jpg').convert('RGB')
    landscape=w>h
    image=shade(ImageOps.fit(base,size,method=RESAMPLE,centering=(.5,.49 if landscape else .42)),landscape)
    if landscape:
        cx=w*.37
        centered_text(image,TITLE,(cx,h*.44),h*.23,script=True,max_width=w*.60,stroke=0)
        tracking(image,ARTIST.upper(),cx,h*.65,h*.049,h*.012,'#f9e7c8')
        centered_text(image,'DSKY✓',(cx,h*.84),h*.026,color=(255,232,196,190),max_width=w*.3,shadow=False)
        flag(image,cx,h*.905,h*.11)
    elif w==h:
        centered_text(image,TITLE,(w*.5,h*.465),w*.205,script=True,max_width=w*.82,stroke=0)
        tracking(image,ARTIST.upper(),w*.5,h*.645,w*.045,w*.011,'#f9e7c8')
        centered_text(image,'DSKY✓',(w*.5,h*.84),w*.028,color=(255,232,196,190),shadow=False)
        flag(image,w*.5,h*.905,w*.12)
    else:
        centered_text(image,TITLE,(w*.5,h*.435),w*.22,script=True,max_width=w*.82)
        tracking(image,ARTIST.upper(),w*.5,h*.575,w*.050,w*.012,'#f9e7c8')
        centered_text(image,'DSKY✓',(w*.5,h*.765),w*.032,color=(255,232,196,190),shadow=False)
        flag(image,w*.5,h*.81,w*.15)
    return image.convert('RGB')


def portrait_alternative():
    base=Image.open(ROOT/'vivi-oor/v2/livrables/VIVI_OOR_V2_03_etincelles.png').convert('RGB')
    image=base.crop((0,210,1080,1290)).convert('RGBA')
    w,h=image.size
    y=np.linspace(0,1,h)
    alpha=(np.maximum(0,(y-.68)/.32)**.8*.78*255).clip(0,210).astype('uint8')
    layer=Image.new('RGBA',image.size,(22,13,24));layer.putalpha(Image.fromarray(np.repeat(alpha[:,None],w,axis=1)))
    image.alpha_composite(layer)
    centered_text(image,TITLE,(540,885),155,script=True,max_width=830,stroke=0)
    tracking(image,ARTIST.upper(),540,964,30,8,'#fff0d6')
    centered_text(image,'DSKY✓',(852,118),28,color=(255,234,201,195),shadow=True)
    flag(image,158,117,95)
    return image.convert('RGB')


def main():
    OUT.mkdir(exist_ok=True,parents=True)
    outputs=[]
    for name,size in [('cover_vivi_oor_universelle_3000.jpg',(3000,3000)),
                      ('cover_vivi_oor_1080x1080.jpg',(1080,1080)),
                      ('cover_vivi_oor_9x16.jpg',(1080,1920)),
                      ('cover_vivi_oor_16x9.jpg',(1920,1080))]:
        path=OUT/name;still_cover(size).save(path,quality=94,subsampling=0)
        outputs.append(dict(file=name,size=size,type='Official S2 decor cover, no regenerated face'))
        print(name,size,flush=True)
    name='cover_vivi_oor_portrait_alternative_1080.jpg'
    portrait_alternative().save(OUT/name,quality=94,subsampling=0)
    outputs.append(dict(file=name,size=[1080,1080],type='Alternative using the approved V2 portrait 03, no additional generation'))
    (PROJECT/'metadata/covers.json').write_text(json.dumps(outputs,ensure_ascii=False,indent=2)+'\n')
    # A contact proof is a derived review document, not an additional generated scene.
    proof=Image.new('RGB',(1650,1000),'#211920');d=ImageDraw.Draw(proof)
    ui=font(24)
    for i,item in enumerate([outputs[1],outputs[2],outputs[3],outputs[4]]):
        im=Image.open(OUT/item['file']);im.thumbnail((700 if i==2 else 405,810),RESAMPLE)
        positions=[(20,40),(440,40),(865,40),(1100,475)]
        x,y=positions[i]
        if i==3:im.thumbnail((400,400),RESAMPLE)
        proof.paste(im,(x,y))
        d.text((x,y+im.height+12),['Carré / APIC','Vertical','Horizontal','Portrait alternatif'][i],font=ui,fill='#eddfc8')
    proof.save(ROOT/'work/vivi-production/covers-proof.jpg',quality=90)


if __name__=='__main__':main()
