#!/usr/bin/env python3
"""Habillage de la salve et planche contact, sans masquer les images originales."""
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'assets/nonvi_konou'
SLOTS=[
 ('s00_intro','INTRO instrumentale'),('s01_wolof','Wolof TechStein beat wê...'),
 ('s02_yeah','Yeah... Nonvi konou...'),('s03_on_est_la','On est là, on brille...'),
 ('ancre_01','Nonvi konou, mon frère sourit'),('s05_misere','Gbè manfo do ohin min...'),
 ('s06_dokpe','Dokpè nou mahou...'),('s07_vivi','Gbètché vivi, ma vie me plaît...'),
 ('s08_beat','Wolof TechStein beat wê!'),('s09_millions','J’ai pas besoin de millions...'),
]
font=ImageFont.truetype(str(ROOT/'assets/fonts/DejaVuSans-Bold.ttf'),19)


def main():
    cells=[]
    for slug,label in SLOTS:
        raw=DIR/f'{slug}_brute.png'
        dressed=DIR/f'{slug}_habillee.png'
        if not dressed.exists():
            subprocess.run([sys.executable,str(ROOT/'scripts/habiller_image_nonvi.py'),str(raw),str(dressed)],check=True)
        im=Image.open(dressed).convert('RGB')
        assert im.size==(1080,1920), (slug,im.size)
        # Bandeau 54 px en pied de page ; trois couleurs exactes sur chaque image.
        assert im.getpixel((80,1880))==(0,135,81),slug
        assert im.getpixel((800,1880))==(252,209,22),slug
        assert im.getpixel((800,1905))==(232,17,45),slug
        cells.append((im,label,slug))
    # Portrait thumbnails 330x587, 3 colonnes pour contrôle facile sur mobile.
    cols=3; cw,ch=346,648; pad=16
    board=Image.new('RGB',(cols*cw+pad,(len(cells)+cols-1)//cols*ch+pad),(13,25,33))
    d=ImageDraw.Draw(board)
    for i,(im,label,slug) in enumerate(cells):
        x=pad+(i%cols)*cw; y=pad+(i//cols)*ch
        preview=im.resize((320,569),Image.Resampling.LANCZOS)
        board.paste(preview,(x,y))
        d.text((x,y+576),slug,font=font,fill=(252,213,130))
        short=label if len(label)<=29 else label[:27]+'…'
        d.text((x,y+603),short,font=font,fill=(246,245,240))
    path=DIR/'planche_salve_01.jpg'
    board.save(path,quality=88,optimize=True)
    print('Planche prête:',path,board.size,'; 10 images : 1 ancre + 9 nouvelles')

if __name__=='__main__':main()
