#!/usr/bin/env python3
"""Badge et pied de page béninois exacts en post-production sur les images IA.

Usage : python scripts/habiller_image_nonvi.py RAW.png OUTPUT.png [--maquette]
Ne modifie jamais l'image brute. La maquette montre un instant du futur texte animé.
"""
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
BOLD = ROOT/'assets/fonts/DejaVuSans-Bold.ttf'
CURSIVE = ROOT/'assets/fonts/GreatVibes-latin.ttf'
W,H = 1080,1920


def flag(draw, bounds):
    """Drapeau officiel : 1/3 vert vertical ; 2/3 jaune haut et rouge bas."""
    x0,y0,x1,y1 = map(int,bounds)
    split=x0+(x1-x0)//3
    middle=y0+(y1-y0)//2
    draw.rectangle((x0,y0,split-1,y1), fill='#008751')
    draw.rectangle((split,y0,x1,middle-1), fill='#FCD116')
    draw.rectangle((split,middle,x1,y1), fill='#E8112D')


def badge(im):
    layer=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(layer)
    box=(365,160,715,239)  # sous la barre recherche y<144
    d.rounded_rectangle(box,radius=30,fill=(3,18,26,213),outline=(248,218,154,210),width=2)
    font=ImageFont.truetype(BOLD,48)
    d.text((391,167),'Dsky',font=font,fill=(255,250,232,255),stroke_width=1,stroke_fill=(4,10,18,240))
    flag(d,(587,177,666,225))
    # signature lisible « Dsky 🇧🇯 » par texte net + pictogramme drapeau vectoriel
    im.alpha_composite(layer)


def footer(im):
    layer=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(layer)
    start=1776
    d.rectangle((0,start-5,W,start),fill=(236,194,101,255))
    flag(d,(0,start,W,H))
    im.alpha_composite(layer)


def corriger_artefacts_ia(im, source_name):
    """La salve 01 a halluciné des drapeaux bas et trois médaillons hauts.

    La vraie bannière est créée APRÈS correction ; ne pas garder deux drapeaux
    (dont certains tricolores erronés) ni un faux logo sous le vrai badge.
    """
    if not source_name.startswith('s') or '_brute' not in source_name:
        return
    layer=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(layer)
    # Vignette nocturne croissante dans la zone décorative (aucune parole ici).
    for y in range(1500,1776,2):
        a=min(255,round(255*(y-1500)/110))
        d.rectangle((0,y,W,y+1),fill=(5,13,20,a))
    im.alpha_composite(layer)
    if source_name.split('_brute')[0] in {'s06_dokpe','s07_vivi','s09_millions'}:
        top=Image.new('RGBA',(W,H))
        d=ImageDraw.Draw(top)
        d.rectangle((0,0,W,365),fill=(5,14,20,255))
        for y in range(366,531,2):
            alpha=round(251*(531-y)/165)
            d.rectangle((0,y,W,y+1),fill=(5,14,20,alpha))
        im.alpha_composite(top)


def maquette(im):
    # Extrait visuel de l'animation future : vers complet centré sur sa largeur FINALE,
    # mot courant en or, mots précédents adoucis, vague sinusoïdale sur chaque colonne.
    layer=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(layer)
    cy=960
    for y in range(cy-255,cy+256,2):
        alpha=round(112*math.exp(-((y-cy)/160)**2))
        d.rectangle((0,y,W,y+1), fill=(0,6,17,alpha))
    im.alpha_composite(layer)
    words=[['Nonvi','konou,'],['mon','frère','sourit']]
    font=ImageFont.truetype(str(CURSIVE),91)
    display=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(display)
    positions=[]
    for row,line in enumerate(words):
        widths=[int(d.textlength(w,font=font))+24 for w in line]
        width=sum(widths)-24
        x=(W-width)//2
        y=cy-139+row*130
        for word,cell in zip(line,widths):
            positions.append((word,x,y))
            x+=cell
    # Le déplacement horizontal est calculé dès le début sur le vers final.
    for word,x,y in positions:
        active=word=='frère'
        color=(255,214,122,255) if active else (255,247,228,227)
        bbox=font.getbbox(word,stroke_width=2)
        tile=Image.new('RGBA',(bbox[2]-bbox[0]+20,bbox[3]-bbox[1]+24))
        p=ImageDraw.Draw(tile)
        p.text((10-bbox[0],10-bbox[1]),word,font=font,fill=color,stroke_width=1,stroke_fill=(15,27,35,230))
        # onde d'eau ~4,5 px sur le trait du texte; ici phase fixe de la maquette.
        out=Image.new('RGBA',(tile.width,tile.height+16))
        for col in range(tile.width):
            dy=round(4.5*math.sin(col/39+1.2))
            out.paste(tile.crop((col,0,col+1,tile.height)),(col,8+dy))
        sprite=Image.new('RGBA',(W,H))
        sprite.alpha_composite(out,(x-10,y-12))
        if active:
            glow=sprite.filter(ImageFilter.GaussianBlur(13))
            im.alpha_composite(glow)
        im.alpha_composite(sprite)
    d=ImageDraw.Draw(im)
    # Discret sillage de vague, pas de sous-titre inférieur.
    points=[(x,1082+4*math.sin(x/27)) for x in range(344,750)]
    d.line(points,fill=(255,218,149,210),width=3,joint='curve')


def main():
    a=argparse.ArgumentParser()
    a.add_argument('source',type=Path); a.add_argument('output',type=Path)
    a.add_argument('--maquette',action='store_true')
    args=a.parse_args()
    im=Image.open(args.source).convert('RGB')
    # Centre crop léger, pas de recadrage du visage.
    ratio=W/H
    if im.width/im.height > ratio:
        target=round(im.height*ratio); left=(im.width-target)//2
        im=im.crop((left,0,left+target,im.height))
    else:
        target=round(im.width/ratio); top=(im.height-target)//2
        im=im.crop((0,top,im.width,top+target))
    im=im.resize((W,H),Image.Resampling.LANCZOS).convert('RGBA')
    corriger_artefacts_ia(im,args.source.stem)
    badge(im)
    if args.maquette:
        maquette(im)
    footer(im)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    im.convert('RGB').save(args.output,optimize=True)

if __name__ == '__main__':
    main()
