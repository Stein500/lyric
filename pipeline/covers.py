from PIL import Image, ImageDraw, ImageFont

F_BOLD = 'assets/fonts/DejaVuSans-Bold.ttf'
CYAN=(0,229,255); WHITE=(245,248,250)

def badge(img):
    W = img.width
    d = ImageDraw.Draw(img,'RGBA')
    bt = ImageFont.truetype(F_BOLD, 32)
    txt='DSKY'
    tw = d.textbbox((0,0),txt,font=bt)[2]
    pad_x,pad_y = 22,10; check_w=30
    bw = tw+10+check_w+pad_x*2; bh = 32+pad_y*2
    bx=(W-bw)//2; by=30
    card = Image.new('RGBA',(bw,bh),(0,0,0,0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0,0,bw-1,bh-1],radius=bh//2,fill=(8,14,20,178),outline=(0,229,255,220),width=2)
    img.paste(card,(bx,by),card)
    d.text((bx+pad_x,by+pad_y-2),txt,font=bt,fill=WHITE)
    cx0=bx+pad_x+tw+10; cy=by+bh//2
    d.line([(cx0+2,cy+2),(cx0+10,cy+10),(cx0+26,cy-8)],fill=CYAN,width=6,joint='curve')
    d.line([(cx0+2,cy+2),(cx0+10,cy+10),(cx0+26,cy-8)],fill=(255,215,120),width=2,joint='curve')

def subtitle(img, y_from_bottom=90):
    W,H = img.size
    d = ImageDraw.Draw(img,'RGBA')
    sf = ImageFont.truetype(F_BOLD, 30)
    line = "Daïsky · Daïsky Prod / TechStein · Rock · 2026 · @daiskypro"
    tw = d.textbbox((0,0),line,font=sf)[2]
    if tw > W-80:
        sf = ImageFont.truetype(F_BOLD, int(30*(W-80)/tw))
        tw = d.textbbox((0,0),line,font=sf)[2]
    x=(W-tw)//2; y=H-y_from_bottom
    d.rounded_rectangle([x-24,y-14,x+tw+24,y+46],radius=18,fill=(8,14,20,150))
    d.text((x+2,y+2),line,font=sf,fill=(0,0,0,160))
    d.text((x,y),line,font=sf,fill=WHITE)

# 9:16
c1 = Image.open('assets/raw/cover_base_9x16.png').convert('RGB').resize((1080,1920), Image.LANCZOS)
badge(c1); subtitle(c1, 110)
c1.save('livrables/cover_yafoy_9x16.jpg', quality=92)
# carré 1080x1080 (APIC + publication)
c2 = Image.open('assets/raw/cover_base_square.png').convert('RGB').resize((1080,1080), Image.LANCZOS)
badge(c2); subtitle(c2, 84)
c2.save('livrables/cover_yafoy_1080.jpg', quality=92)
print('covers OK')
