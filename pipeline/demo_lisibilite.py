# Démo v4.9.2 : rendu paroles 4 couches (bandeau adaptatif / ombre / contour / blanc chaud)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W,H = 1080,1920
F_GV = 'assets/fonts/GreatVibes-Regular.ttf'

def render_lyric(bg_path, text, out, size=96):
    img = Image.open(bg_path).convert('RGB').resize((W,H), Image.LANCZOS)
    font = ImageFont.truetype(F_GV, size)
    d = ImageDraw.Draw(img,'RGBA')
    bbox = d.textbbox((0,0), text, font=font)
    tw_, th_ = bbox[2]-bbox[0], bbox[3]-bbox[1]
    if tw_ > 920:
        size2 = int(size*920/tw_)
        size2 = max(size2, 80)
        font = ImageFont.truetype(F_GV, size2)
        bbox = d.textbbox((0,0), text, font=font); tw_, th_ = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (W-tw_)//2 - bbox[0]; y = H-300-th_ - bbox[1]
    # 1) mesurer luminance locale
    zone = np.array(img.crop((max(0,x-30), max(0,y-30), min(W,x+tw_+30), min(H,y+th_+30))).convert('L'))
    lum = zone.mean()
    pad = int(0.38*font.size)
    if lum > 90:   # fond clair/chargé -> bandeau fort
        alpha = 165 if lum > 140 else 130
        d.rounded_rectangle([x-pad, y-pad, x+tw_+pad, y+th_+int(pad*1.2)], radius=28, fill=(8,14,20,alpha))
    else:          # fond sombre -> scrim léger
        d.rounded_rectangle([x-pad, y-pad, x+tw_+pad, y+th_+int(pad*1.2)], radius=28, fill=(8,14,20,70))
    # 2) ombre portée
    d.text((x+4,y+4), text, font=font, fill=(0,0,0,190))
    # 3) contour 2px (cursive fine)
    for dx,dy in [(-2,0),(2,0),(0,-2),(0,2),(-1,-1),(1,1),(-1,1),(1,-1)]:
        d.text((x+dx,y+dy), text, font=font, fill=(10,16,24,230))
    # 4) remplissage blanc chaud
    d.text((x,y), text, font=font, fill=(245,248,250))
    img.save(out, quality=92)
    print(out, '| lum locale =', round(lum,1), '| taille =', font.size)

# pire cas 1 : fond TRES clair (s13 rock, ciel + soleil) + ligne longue
render_lyric('assets/raw/portrait/s13_rock.png',
             "La guitare qui hurle, le son qui t'emballe",
             'livrables/validation/demo_lisibilite_fondclair.jpg')
# cas 2 : refrain en doré pâle sur s03
img = Image.open('assets/raw/portrait/s03_legende.png').convert('RGB').resize((W,H), Image.LANCZOS)
font = ImageFont.truetype(F_GV, 96)
d = ImageDraw.Draw(img,'RGBA')
text = "Yafoy t'es encore une légende"
bbox = d.textbbox((0,0), text, font=font)
tw_, th_ = bbox[2]-bbox[0], bbox[3]-bbox[1]
if tw_ > 920:
    font = ImageFont.truetype(F_GV, max(80,int(96*920/tw_))); bbox = d.textbbox((0,0),text,font=font); tw_,th_=bbox[2]-bbox[0],bbox[3]-bbox[1]
x=(W-tw_)//2-bbox[0]; y=H-300-th_-bbox[1]
zone = np.array(img.crop((x-30,y-30,x+tw_+30,y+th_+30)).convert('L')); lum=zone.mean()
pad=int(0.38*font.size)
d.rounded_rectangle([x-pad,y-pad,x+tw_+pad,y+th_+int(pad*1.2)],radius=28,fill=(8,14,20,150 if lum>90 else 70))
d.text((x+4,y+4),text,font=font,fill=(0,0,0,190))
for dx,dy in [(-2,0),(2,0),(0,-2),(0,2),(-1,-1),(1,1),(-1,1),(1,-1)]:
    d.text((x+dx,y+dy),text,font=font,fill=(30,20,5,230))
d.text((x,y),text,font=font,fill=(255,235,190))  # doré pâle refrain
img.save('livrables/validation/demo_lisibilite_refrain_dore.jpg', quality=92)
print('demo refrain doré OK | lum =', round(lum,1))
