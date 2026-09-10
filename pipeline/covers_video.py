# Covers vidéo : teaser TikTok + clip lyrics (1080x1920) — v4.9.2
from PIL import Image, ImageDraw, ImageFont

W,H = 1080,1920
F_BOLD='assets/fonts/DejaVuSans-Bold.ttf'
F_GV='assets/fonts/GreatVibes-Regular.ttf'
WHITE=(245,248,250); GOLD=(255,235,190); CYAN=(0,229,255); AMBER=(255,190,80)

def badge(img):
    d = ImageDraw.Draw(img,'RGBA')
    bt = ImageFont.truetype(F_BOLD, 32)
    tw = d.textbbox((0,0),'DSKY',font=bt)[2]
    pad_x,pad_y,check_w = 22,10,30
    bw,bh = tw+10+check_w+pad_x*2, 32+pad_y*2
    bx,by = (W-bw)//2, 30
    card = Image.new('RGBA',(bw,bh),(0,0,0,0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0,0,bw-1,bh-1],radius=bh//2,fill=(8,14,20,178),outline=(0,229,255,220),width=2)
    img.paste(card,(bx,by),card)
    d.text((bx+pad_x,by+pad_y-2),'DSKY',font=bt,fill=WHITE)
    cx0,cy = bx+pad_x+tw+10, by+bh//2
    d.line([(cx0+2,cy+2),(cx0+10,cy+10),(cx0+26,cy-8)],fill=CYAN,width=6,joint='curve')
    d.line([(cx0+2,cy+2),(cx0+10,cy+10),(cx0+26,cy-8)],fill=(255,215,120),width=2,joint='curve')

def text_block(img, spec, y0, maxw=940):
    d = ImageDraw.Draw(img,'RGBA')
    # mesurer
    meas=[]; fonts=[]; wmax=0; htot=0
    for t_,fp,sz,col in spec:
        f=ImageFont.truetype(fp,sz)
        b=d.textbbox((0,0),t_,font=f)
        if b[2]-b[0]>maxw:
            f=ImageFont.truetype(fp,int(sz*maxw/(b[2]-b[0]))); b=d.textbbox((0,0),t_,font=f)
        meas.append(b); fonts.append(f); wmax=max(wmax,b[2]-b[0]); htot+=(b[3]-b[1])+30
    x0=(W-wmax)//2
    d.rounded_rectangle([x0-50,y0-40,x0+wmax+50,y0+htot+30],radius=30,fill=(8,14,20,150))
    y=y0
    for (t_,fp,sz,col),b,f in zip(spec,meas,fonts):
        x=(W-(b[2]-b[0]))//2-b[0]
        d.text((x+3,y+3-b[1]),t_,font=f,fill=(0,0,0,190))
        for dx,dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            d.text((x+dx,y+dy-b[1]),t_,font=f,fill=(10,16,24,220))
        d.text((x,y-b[1]),t_,font=f,fill=col)
        y+=(b[3]-b[1])+30

# ============ COVER TEASER TIKTOK ============
img = Image.open('assets/raw/teaser/t01_hook.png').convert('RGB').resize((W,H), Image.LANCZOS)
text_block(img, [
    ("Bientôt...", F_GV, 120, GOLD),
    ("Yafoy t'es encore là", F_GV, 92, GOLD),
    ("Daïsky", F_BOLD, 42, WHITE),
], 170)
text_block(img, [
    ("TEASER", F_BOLD, 60, CYAN),
    ("Abonne-toi pour la sortie !", F_BOLD, 38, WHITE),
], H-420)
badge(img)
img.save('livrables/cover_teaser_yafoy_tiktok.jpg', quality=92)
print('cover teaser OK')

# ============ COVER CLIP LYRICS ============
img2 = Image.open('assets/raw/cover_base_9x16.png').convert('RGB').resize((W,H), Image.LANCZOS)
# la base contient déjà le titre IA doré -> ajouter le bandeau LYRICS VIDEO + infos
text_block(img2, [
    ("LYRICS VIDEO", F_BOLD, 58, AMBER),
    ("Rock · 2026 · @daiskypro", F_BOLD, 34, WHITE),
], H-380)
badge(img2)
img2.save('livrables/cover_lyrics_yafoy_9x16.jpg', quality=92)
print('cover lyrics OK')
