# Moteur commun v4.9.2 — SOLUTION A, paroles 4 couches, badge DSKY✓, CTA, partage
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, subprocess, io, math, glob

W,H = 1080,1920
FPS = 30
CW,CH = 1188,2112   # canvas Ken Burns 1.1x
F_BOLD='assets/fonts/DejaVuSans-Bold.ttf'
F_GV='assets/fonts/GreatVibes-Regular.ttf'
WHITE=(245,248,250); GOLD=(255,235,190); CYAN=(0,229,255); AMBER=(255,190,80)

def slot_path(slot):
    g = glob.glob(f'assets/raw/portrait/{slot}_*.png') + glob.glob(f'assets/raw/teaser/{slot}*.png')
    return g[0]

def load_canvas(path):
    im = Image.open(path).convert('RGB')
    return im.resize((CW,CH), Image.LANCZOS)

def kenburns(canvas, u, seed=0):
    # u in [0,1] progression du slot ; zoom 1.02->1.08 alterné, pan sinusoïdal
    z0,z1 = (1.02,1.08) if seed%2==0 else (1.08,1.02)
    z = z0 + (z1-z0)*u
    cw, ch = int(W*1.1/z), int(H*1.1/z)
    cw, ch = min(cw,CW), min(ch,CH)
    maxx, maxy = CW-cw, CH-ch
    px = 0.5 + 0.35*math.sin(2*math.pi*(0.11*u + 0.13*seed))
    py = 0.5 + 0.35*math.cos(2*math.pi*(0.09*u + 0.07*seed))
    x = int(maxx*px); y = int(maxy*py)
    return canvas.crop((x,y,x+cw,y+ch)).resize((W,H), Image.BILINEAR)

def make_badge():
    bt = ImageFont.truetype(F_BOLD, 32)
    tmp = Image.new('RGBA',(10,10)); dt = ImageDraw.Draw(tmp)
    tw = dt.textbbox((0,0),'DSKY',font=bt)[2]
    pad_x,pad_y,check_w = 22,10,30
    bw,bh = tw+10+check_w+pad_x*2, 32+pad_y*2
    card = Image.new('RGBA',(bw,bh),(0,0,0,0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0,0,bw-1,bh-1],radius=bh//2,fill=(8,14,20,178),outline=(0,229,255,220),width=2)
    cd.text((pad_x,pad_y-2),'DSKY',font=bt,fill=WHITE)
    cx0,cy = pad_x+tw+10, bh//2
    cd.line([(cx0+2,cy+2),(cx0+10,cy+10),(cx0+26,cy-8)],fill=CYAN,width=6,joint='curve')
    cd.line([(cx0+2,cy+2),(cx0+10,cy+10),(cx0+26,cy-8)],fill=(255,215,120),width=2,joint='curve')
    return card, ((W-bw)//2, 36)

def _thumb(dr,cx,cy,s,col):
    dr.rounded_rectangle([cx-s*0.55,cy-s*0.05,cx-s*0.3,cy+s*0.5],radius=4,fill=col)
    dr.polygon([(cx-0.28*s,cy+0.02*s),(cx-0.05*s,cy+0.02*s),(cx+0.02*s,cy-0.45*s),(cx+0.14*s,cy-0.4*s),(cx+0.12*s,cy-0.02*s),(cx+0.5*s,cy-0.02*s),(cx+0.45*s,cy+0.5*s),(cx-0.28*s,cy+0.5*s)],fill=col)
def _bell(dr,cx,cy,s,col):
    dr.pieslice([cx-0.4*s,cy-0.45*s,cx+0.4*s,cy+0.35*s],180,360,fill=col)
    dr.rectangle([cx-0.4*s,cy-0.05*s,cx+0.4*s,cy+0.28*s],fill=col)
    dr.rectangle([cx-0.5*s,cy+0.28*s,cx+0.5*s,cy+0.38*s],fill=col)
    dr.ellipse([cx-0.1*s,cy+0.4*s,cx+0.1*s,cy+0.55*s],fill=col)
def _bubble(dr,cx,cy,s,col):
    dr.rounded_rectangle([cx-0.5*s,cy-0.4*s,cx+0.5*s,cy+0.25*s],radius=int(0.2*s),fill=col)
    dr.polygon([(cx-0.2*s,cy+0.22*s),(cx+0.05*s,cy+0.22*s),(cx-0.15*s,cy+0.5*s)],fill=col)

def make_cta():
    lf = ImageFont.truetype(F_BOLD, 17)
    labels=['LIKE','ABONNE-TOI','COMMENTE']; draws=[_thumb,_bell,_bubble]; cols=[CYAN,AMBER,CYAN]
    tmp=Image.new('RGBA',(10,10)); dt=ImageDraw.Draw(tmp)
    widths=[max(118, dt.textbbox((0,0),l,font=lf)[2]+24) for l in labels]
    gap=26; total=sum(widths)+gap*2; ih=96
    strip = Image.new('RGBA',(total,ih),(0,0,0,0))
    x=0
    for i,(lab,wd) in enumerate(zip(labels,widths)):
        c = Image.new('RGBA',(wd,ih),(0,0,0,0))
        cd = ImageDraw.Draw(c)
        cd.rounded_rectangle([0,0,wd-1,ih-1],radius=18,fill=(8,14,20,165),outline=(0,229,255,150),width=2)
        draws[i](cd,wd//2,36,34,cols[i]+(255,))
        lw=cd.textbbox((0,0),lab,font=lf)[2]
        cd.text(((wd-lw)//2,ih-24),lab,font=lf,fill=WHITE)
        strip.paste(c,(x,0),c); x+=wd+gap
    return strip, ((W-total)//2, 210)

def load_share():
    sh = Image.open('assets/icons/share_daisky.png').convert('RGBA')
    sh.thumbnail((240,240), Image.LANCZOS)
    return sh

def fit_font(text, path, size, maxw, minsize=80):
    tmp=Image.new('RGBA',(10,10)); dt=ImageDraw.Draw(tmp)
    f = ImageFont.truetype(path, size)
    wpx = dt.textbbox((0,0),text,font=f)[2]
    if wpx <= maxw: return f, [text]
    ns = max(minsize, int(size*maxw/wpx))
    f = ImageFont.truetype(path, ns)
    wpx = dt.textbbox((0,0),text,font=f)[2]
    if wpx <= maxw: return f, [text]
    # retour à la ligne au plus près du milieu
    words = text.split(' ')
    best,bd = 1,1e9
    for i in range(1,len(words)):
        l1=' '.join(words[:i]); l2=' '.join(words[i:])
        d = abs(dt.textbbox((0,0),l1,font=f)[2]-dt.textbbox((0,0),l2,font=f)[2])
        if d<bd: bd,best=d,i
    return f, [' '.join(words[:best]), ' '.join(words[best:])]

def make_lyric_sprite(text, font_path=F_GV, size=88, fill=WHITE, maxw=920):
    f, lines = fit_font(text, font_path, size, maxw)
    tmp=Image.new('RGBA',(10,10)); dt=ImageDraw.Draw(tmp)
    pads = int(f.size*0.8)
    lws=[]; lhs=[]
    for ln in lines:
        bb = dt.textbbox((0,0),ln,font=f)
        lws.append(bb[2]-bb[0]); lhs.append(bb[3]-bb[1])
    lh = max(lhs)+int(f.size*0.35)
    sw = max(lws)+pads*2; shh = lh*len(lines)+pads*2
    spr = Image.new('RGBA',(sw,shh),(0,0,0,0))
    d = ImageDraw.Draw(spr)
    for i,ln in enumerate(lines):
        bb = dt.textbbox((0,0),ln,font=f)
        x = (sw-(bb[2]-bb[0]))//2 - bb[0]; y = pads + i*lh - bb[1]
        d.text((x+4,y+4),ln,font=f,fill=(0,0,0,190))
        for dx,dy in [(-2,0),(2,0),(0,-2),(0,2),(-1,-1),(1,1),(-1,1),(1,-1)]:
            d.text((x+dx,y+dy),ln,font=f,fill=(10,16,24,230))
        d.text((x,y),ln,font=f,fill=fill)
    inner = (pads, pads-6, sw-pads, shh-pads+6)
    return spr, inner

def banner_for(spr_inner, bg_lum):
    x0,y0,x1,y1 = spr_inner
    w,h = x1-x0, y1-y0
    pad = 30
    alpha = 165 if bg_lum>140 else (130 if bg_lum>90 else 70)
    b = Image.new('RGBA',(w+pad*2,h+pad*2),(0,0,0,0))
    ImageDraw.Draw(b).rounded_rectangle([0,0,b.width-1,b.height-1],radius=28,fill=(8,14,20,alpha))
    return b, pad

def encode(cmd_out, total, audio_args, fade_st):
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff,'-y','-f','image2pipe','-framerate',str(FPS),'-vcodec','mjpeg','-i','-'] + audio_args + [
        '-filter_complex', f'[0:v]fade=t=out:st={fade_st}:d=3[v];[1:a]apad=whole_dur={total},afade=t=out:st={fade_st}:d=3[a]',
        '-map','[v]','-map','[a]','-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','192k','-movflags','+faststart','-t',str(total), cmd_out]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
