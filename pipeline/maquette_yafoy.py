# Maquette v4.9 : badge DSKY✓ haut-centre + CTA 0-2s + vers cursive + icône partage
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W,H = 1080,1920
bg = Image.open('assets/raw/portrait/anchor_charteP.png').convert('RGB').resize((W,H), Image.LANCZOS)
img = bg.copy()
d = ImageDraw.Draw(img, 'RGBA')

F_BOLD = 'assets/fonts/DejaVuSans-Bold.ttf'
F_GV   = 'assets/fonts/GreatVibes-Regular.ttf'
CYAN=(0,229,255); AMBER=(255,190,80); WHITE=(245,248,250)

# ---------- BADGE DSKY✓ — haut-centre, discret+visible (§5.1) ----------
bt_font = ImageFont.truetype(F_BOLD, 32)
txt='DSKY'
tw = d.textbbox((0,0),txt,font=bt_font)[2]
check_w = 30
pad_x, pad_y = 22, 10
bw = tw + 10 + check_w + pad_x*2; bh = 32 + pad_y*2
bx = (W-bw)//2; by = 36
# carte semi-opaque
card = Image.new('RGBA',(bw,bh),(0,0,0,0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle([0,0,bw-1,bh-1], radius=bh//2, fill=(8,14,20,178), outline=(0,229,255,220), width=2)
img.paste(card,(bx,by),card)
d.text((bx+pad_x, by+pad_y-2), txt, font=bt_font, fill=WHITE)
# coche polygonale cyan/dorée
cx0 = bx+pad_x+tw+10; cy = by+bh//2
d.line([(cx0+2,cy+2),(cx0+10,cy+10),(cx0+26,cy-8)], fill=CYAN, width=6, joint='curve')
d.line([(cx0+2,cy+2),(cx0+10,cy+10),(cx0+26,cy-8)], fill=(255,215,120), width=2, joint='curve')

# ---------- CTA like/sub/comment (0-2 s) — bandeau discret (§5.2) ----------
def rounded_card(w,h,alpha=165):
    c = Image.new('RGBA',(w,h),(0,0,0,0))
    ImageDraw.Draw(c).rounded_rectangle([0,0,w-1,h-1], radius=18, fill=(8,14,20,alpha), outline=(0,229,255,150), width=2)
    return c
cta_y = 210
icons_w, icons_h = 118, 96
gap = 26
labels = ['LIKE','ABONNE-TOI','COMMENTE']
lf = ImageFont.truetype(F_BOLD, 17)
widths=[]
for lab in labels:
    lw = d.textbbox((0,0),lab,font=lf)[2]
    widths.append(max(icons_w, lw+24))
total = sum(widths)+gap*2
x = (W-total)//2
def draw_thumb(dr, cx, cy, s, col):
    # pouce like vectoriel
    dr.rounded_rectangle([cx-s*0.55, cy-s*0.05, cx-s*0.3, cy+s*0.5], radius=4, fill=col)
    dr.polygon([(cx-s*0.28,cy+0.02*s),(cx-0.05*s,cy+0.02*s),(cx+0.02*s,cy-0.45*s),(cx+0.14*s,cy-0.4*s),(cx+0.12*s,cy-0.02*s),(cx+0.5*s,cy-0.02*s),(cx+0.45*s,cy+0.5*s),(cx-0.28*s,cy+0.5*s)], fill=col)
def draw_bell(dr, cx, cy, s, col):
    dr.pieslice([cx-0.4*s,cy-0.45*s,cx+0.4*s,cy+0.35*s], 180, 360, fill=col)
    dr.rectangle([cx-0.4*s,cy-0.05*s,cx+0.4*s,cy+0.28*s], fill=col)
    dr.rectangle([cx-0.5*s,cy+0.28*s,cx+0.5*s,cy+0.38*s], fill=col)
    dr.ellipse([cx-0.1*s,cy+0.4*s,cx+0.1*s,cy+0.55*s], fill=col)
def draw_bubble(dr, cx, cy, s, col):
    dr.rounded_rectangle([cx-0.5*s,cy-0.4*s,cx+0.5*s,cy+0.25*s], radius=int(0.2*s), fill=col)
    dr.polygon([(cx-0.2*s,cy+0.22*s),(cx+0.05*s,cy+0.22*s),(cx-0.15*s,cy+0.5*s)], fill=col)
draws=[draw_thumb, draw_bell, draw_bubble]
cols=[CYAN, AMBER, CYAN]
for i,(lab,wd) in enumerate(zip(labels,widths)):
    c = rounded_card(wd, icons_h)
    cd = ImageDraw.Draw(c)
    draws[i](cd, wd//2, 36, 34, cols[i]+ (255,))
    lw = cd.textbbox((0,0),lab,font=lf)[2]
    cd.text(((wd-lw)//2, icons_h-24), lab, font=lf, fill=WHITE)
    img.paste(c,(x,cta_y),c)
    x += wd+gap

# ---------- VERS en GreatVibes (cursive, ligne connectée §14) ----------
verse = "Yafoy t'es encore une légende"
vf = ImageFont.truetype(F_GV, 88)
bbox = d.textbbox((0,0),verse,font=vf)
vw = bbox[2]-bbox[0]
if vw > 940:
    vf = ImageFont.truetype(F_GV, int(88*940/vw)); bbox = d.textbbox((0,0),verse,font=vf); vw=bbox[2]-bbox[0]
vx = (W-vw)//2 - bbox[0]; vy = H-300-(bbox[3]-bbox[1])
# glow
glow = Image.new('RGBA',(W,H),(0,0,0,0))
gd = ImageDraw.Draw(glow)
gd.text((vx,vy),verse,font=vf,fill=(0,229,255,200))
glow = glow.filter(ImageFilter.GaussianBlur(10))
img.paste(Image.alpha_composite(img.convert('RGBA'),glow).convert('RGB'),(0,0))
d = ImageDraw.Draw(img,'RGBA')
d.text((vx+3,vy+4),verse,font=vf,fill=(0,0,0,190))
d.text((vx,vy),verse,font=vf,fill=WHITE)

# ---------- ICÔNE PARTAGE mi-vidéo (aperçu, §5.3) ----------
share = Image.open('assets/icons/share_daisky_raw.png').convert('RGB')
arr = np.array(share).astype(np.float32)
lum = arr.max(axis=2)
alpha = np.clip((lum-18)/60.0,0,1)*255
sh = np.dstack([arr, alpha]).astype(np.uint8)
share_rgba = Image.fromarray(sh,'RGBA')
# crop au contenu
a = np.array(share_rgba)[:,:,3]
ys,xs = np.where(a>30)
share_rgba = share_rgba.crop((xs.min(),ys.min(),xs.max(),ys.max()))
share_rgba.save('assets/icons/share_daisky.png')
s2 = share_rgba.copy(); s2.thumbnail((260,260), Image.LANCZOS)
sx,sy = (W-s2.width)//2, 640
img.paste(s2,(sx,sy),s2)
pf = ImageFont.truetype(F_BOLD, 30)
pt = 'PARTAGE'
pw = d.textbbox((0,0),pt,font=pf)[2]
d.text(((W-pw)//2+2, sy+s2.height+10+2), pt, font=pf, fill=(0,0,0,200))
d.text(((W-pw)//2, sy+s2.height+10), pt, font=pf, fill=AMBER)

img.save('work/maquette_yafoy_v1.jpg', quality=92)
print('maquette OK ->', 'work/maquette_yafoy_v1.jpg')
