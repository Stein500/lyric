#!/usr/bin/env python3
"""Production reproductible de Je plane. Dépendances : Pillow, mutagen, imageio-ffmpeg.
Le calage mot à mot et les bornes des teasers sont des estimations, à vérifier à l'écoute.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from mutagen.id3 import ID3, TIT2, TPE1, TPE2, TALB, APIC, USLT, TXXX
import imageio_ffmpeg
import json, math, re, subprocess, sys

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
WORK = P/'travail'; OUT = P/'livrables'; WORK.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()
DURATION = 173.4399791667
END = DURATION + 5.0
FPS=30
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def run(cmd, **kw):
    print('RUN', ' '.join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], check=True, **kw)

def fmt(s):
    cs=max(0,round(s*100)); h,cs=divmod(cs,360000); m,cs=divmod(cs,6000); sec,cs=divmod(cs,100)
    return f'{h}:{m:02}:{sec:02}.{cs:02}'

def center(draw, text, y, font, fill, stroke=0):
    box=draw.textbbox((0,0),text,font=font,stroke_width=stroke); w=box[2]-box[0]
    draw.text(((draw.im.size[0]-w)/2,y),text,font=font,fill=fill,stroke_width=stroke,stroke_fill='#080d20')

def covers():
    # Le choix de l'artiste est carré ; l'image entière est conservée dans un fond vertical cohérent.
    src=Image.open(P/'fonds/cover-selection.png').convert('RGB')
    def vertical(im):
        bg=ImageOps.fit(im,(1080,1920),method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(38)).point(lambda p: int(p*.36))
        fg=ImageOps.contain(im,(1080,1080),method=Image.Resampling.LANCZOS)
        mask=Image.new('L',fg.size,255)
        pixels=mask.load()
        for y in range(fg.height):
            opacity=min(255, round(255*y/100), round(255*(fg.height-1-y)/100))
            for x in range(fg.width): pixels[x,y]=opacity
        bg.paste(fg,((1080-fg.width)//2,230),mask)
        return bg
    for name, raw in [('COVER-CHOISIE', src), ('COVER-ALTERNATIVE', Image.open(P/'fonds/scene-01-ancre.png').convert('RGB'))]:
        if name=='COVER-CHOISIE':
            im=vertical(raw)
        else:
            im=ImageOps.fit(raw,(1080,1920),method=Image.Resampling.LANCZOS,centering=(.5,0))
        layer=Image.new('RGBA',im.size); d=ImageDraw.Draw(layer)
        d.rounded_rectangle((125,1270,955,1515),radius=26,fill=(4,8,20,205))
        im=Image.alpha_composite(im.convert('RGBA'),layer); d=ImageDraw.Draw(im)
        center(d,'JE PLANE',1290,ImageFont.truetype(FONT,96),'#ffe1a1',3)
        center(d,'DSKY  ·  WTBW',1420,ImageFont.truetype(FONT,42),'#ffffff',2)
        im.convert('RGB').save(OUT/f'{name}-1080x1920.jpg',quality=95,subsampling=0)
    # Carré : réduction de l'image complète, sans rogner le visage.
    im=src.resize((1080,1080),Image.Resampling.LANCZOS).convert('RGBA'); lay=Image.new('RGBA',im.size); d=ImageDraw.Draw(lay)
    d.rounded_rectangle((115,775,965,1040),radius=25,fill=(4,8,20,210)); im=Image.alpha_composite(im,lay); d=ImageDraw.Draw(im)
    center(d,'JE PLANE',792,ImageFont.truetype(FONT,93),'#ffe1a1',2)
    center(d,'DSKY  ·  WTBW',930,ImageFont.truetype(FONT,38),'white',1)
    im.convert('RGB').save(OUT/'COVER-CHOISIE-1080x1080.jpg',quality=95,subsampling=0)

def normalize_assets(rows):
    for rel in sorted({r['image'] for r in rows}):
        src=P/rel; dst=WORK/Path(rel).name
        im=Image.open(src).convert('RGB')
        # Mêmes dimensions pour le démultiplexeur concat, sans déformer.
        if im.size != (768,1376):
            bg=ImageOps.fit(im,(768,1376),method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(24)).point(lambda p:int(p*.5))
            fg=ImageOps.contain(im,(768,1376),method=Image.Resampling.LANCZOS)
            bg.paste(fg,((768-fg.width)//2,0)); im=bg
        im.save(dst)
    parts=['ffconcat version 1.0']
    for i,r in enumerate(rows):
        start=0 if i==0 else r['debut_source']
        end=rows[i+1]['debut_source'] if i+1<len(rows) else END
        path=(WORK/Path(r['image']).name).as_posix().replace("'", "'\\''")
        parts += [f"file '{path}'",f'duration {end-start:.6f}']
    parts.append(f"file '{(WORK/Path(rows[-1]['image']).name).as_posix()}'")
    (WORK/'images.ffconcat').write_text('\n'.join(parts)+'\n')

def wrap_words(text):
    f=ImageFont.truetype(FONT,50); lines=[]; line=[]
    for word in text.split():
        if line and f.getlength(' '.join(line+[word]))>680:
            lines.append(line); line=[]
        line.append(word)
    if line: lines.append(line)
    return lines

def ass(rows):
    headers='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,DejaVu Sans,50,&H00FFFFFF,&H00D3E3FF,&H00101220,&H66000000,-1,0,0,0,100,100,0,0,1,3,1,5,170,170,0,1
Style: Badge,DejaVu Sans,32,&H00D5E7FF,&H00D5E7FF,&H00101220,&H66000000,-1,0,0,0,100,100,2,0,1,2,1,8,0,0,0,1
Style: Card,DejaVu Sans,70,&H00D5E7FF,&H00D5E7FF,&H00101220,&H66000000,-1,0,0,0,100,100,0,0,1,3,1,5,0,0,0,1
Style: Bar,DejaVu Sans,20,&H00C8DFFF,&H00C8DFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    events=[]
    def ev(a,b,sty,txt,layer=0): events.append(f'Dialogue: {layer},{fmt(a)},{fmt(b)},{sty},,0,0,0,,{txt}')
    ev(0,rows[0]['debut_source'],'Card',r'{\an5\pos(540,1150)\fad(200,200)}JE PLANE\N{\fs35}DSKY · WTBW',2)
    for i,r in enumerate(rows):
        start=r['debut_source']; end=rows[i+1]['debut_source'] if i+1<len(rows) else DURATION
        # Les fins et la répartition mot à mot sont indicatives : à contrôler à l'écoute.
        lines=wrap_words(r['texte_affiche']); words=sum((len(l) for l in lines)); duration=int((end-start)*100)
        per=max(1,duration//words); seg=[]
        for line in lines:
            seg.append(' '.join(r'{\kf%d}%s'%(per,w.replace('{','').replace('}','').replace('\\','')) for w in line))
        ev(start,end,'Lyric',r'{\an5\pos(540,1190)\q2}'+r'\N'.join(seg),3)
    # Badge discret, lecture alternative lente, hors cartes.
    t=rows[0]['debut_source']; k=0
    while t<DURATION:
        end=min(t+2.4,DURATION); text='DSKY' if k%2==0 else 'WTBW'
        ev(t,end,'Badge',r'{\an8\pos(540,165)\fad(300,200)}'+text,2); t=end; k+=1
    # Rubans/vagues fins et animés dans une bande dédiée, sous les paroles et au-dessus du filet.
    # Animation sur un plan séparé : jamais de filtre ni de transparence sur les mots.
    ribbon = 'm 0 18 b 110 2 235 2 360 18 b 485 34 610 34 720 18 l 720 21 b 610 37 485 37 360 21 b 235 5 110 5 0 21'
    t=rows[0]['debut_source']; wave_index=0
    while t<DURATION:
        e=min(t+3.6,DURATION)
        color='&HF2D89E&' if wave_index%2==0 else '&HFFCFAB&'
        ev(t,e,'Bar',r'{\an7\move(155,1406,170,1418)\fad(400,400)\alpha&H55&\c'+color+r'\p1}'+ribbon,1)
        ev(t,e,'Bar',r'{\an7\move(170,1445,155,1433)\fad(500,500)\alpha&H88&\c&HFFE8BD&\p1}'+ribbon,1)
        # Étincelle brève dessinée, hors visage et bande des paroles.
        ev(t,e,'Bar',r'{\an5\pos(194,1468)\fad(600,600)\fscx80\fscy80\t(0,900,\fscx125\fscy125)\c&H9CE6FF&\p1}m 0 -8 l 3 -3 8 0 3 3 0 8 -3 3 -8 0 -3 -3',1)
        t=e; wave_index+=1
    # Filet de progression : piste + progression par pas d'une seconde.
    ev(rows[0]['debut_source'],DURATION,'Bar',r'{\an7\pos(170,1554)\alpha&H99&\p1}m 0 0 l 740 0 740 4 0 4',1)
    t=rows[0]['debut_source']
    while t<DURATION:
        end=min(t+1,DURATION); width=max(1,round(740*(end-rows[0]['debut_source'])/(DURATION-rows[0]['debut_source'])))
        ev(t,end,'Bar',r'{\an7\pos(170,1552)\p1}m 0 0 l '+str(width)+' 0 '+str(width)+' 8 0 8',2); t=end
    ev(DURATION,END,'Card',r'{\an5\pos(540,1010)\fad(400,300)}MERCI · WTBW\N{\fs38}JE PLANE · DSKY\N{\fs30}Merci d’avoir écouté',4)
    # Clochette visuelle courte sur la carte finale après l'audio, sans bruit ajouté.
    # L'artiste la demande explicitement ; cette position évite toute syllabe ou parole.
    bell='m 0 2 b 20 2 29 18 29 40 l 29 50 39 59 39 65 l -39 65 -39 59 -29 50 -29 40 b -29 18 -20 2 0 2 m -8 69 b -7 78 7 78 8 69'
    ev(DURATION+.35,DURATION+2.35,'Bar',r'{\an5\pos(300,1300)\fad(180,220)\c&H9CE6FF&\frz-8\t(0,500,\frz8)\t(500,1000,\frz-4)\t(1000,1500,\frz0)\p1}'+bell,5)
    ev(DURATION+.35,DURATION+2.35,'Badge',r'{\an5\pos(585,1305)\fad(180,220)\fs42}CLIQUE SUR +',5)
    ev(DURATION+2.2,END-.2,'Badge',r'{\an5\pos(540,1310)\fad(250,300)\fs35}LIKE  ·  PARTAGE  ·  COMMENTE',5)
    (WORK/'paroles.ass').write_text(headers+'\n'.join(events)+'\n',encoding='utf-8')

def mp3():
    src=ROOT/'Je plane.mp3'
    cmd=[FF,'-hide_banner','-i',src,'-map','0:a:0','-vn','-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-']
    p=subprocess.run([str(c) for c in cmd],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    matches=re.findall(r'\{\s*"input_i".*?\}',p.stderr,re.S)
    if not matches: raise RuntimeError('Mesure loudnorm absente')
    stats=json.loads(matches[-1]); (WORK/'loudnorm-passe1.json').write_text(json.dumps(stats,indent=2))
    af=('loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:print_format=json:'+
        ':'.join(f'{k}={stats[v]}' for k,v in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')]))
    path=OUT/'JE-PLANE-DSKY.mp3'
    p=subprocess.run([str(x) for x in [FF,'-y','-hide_banner','-i',src,'-map','0:a:0','-map_metadata','-1','-vn','-af',af,'-ar','48000','-ac','2','-c:a','libmp3lame','-b:a','320k',path]],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    (WORK/'loudnorm-passe2.log').write_text(p.stderr)
    # Reconstruire les tags de zéro : ne pas propager les métadonnées du fichier source.
    tags=ID3()
    tags.add(TIT2(encoding=3,text='Je plane')); tags.add(TPE1(encoding=3,text='DSKY')); tags.add(TPE2(encoding=3,text='DSKY')); tags.add(TALB(encoding=3,text='Je plane'))
    tags.add(TXXX(encoding=3,desc='SERIE',text='WTBW'))
    tags.add(APIC(encoding=3,mime='image/jpeg',type=3,desc='Cover',data=(OUT/'COVER-CHOISIE-1080x1080.jpg').read_bytes()))
    rows=json.loads((P/'verses_map.json').read_text()); tags.add(USLT(encoding=3,lang='fra',desc='',text='\n'.join(re.sub(r'\[reference:\d+\]', '',x['texte_source']) for x in rows)))
    tags.save(path,v2_version=4)

def render(preview=False):
    dest=WORK/'preview-animations.mp4' if preview else OUT/'JE-PLANE-DSKY-LYRICS-9x16.mp4'
    rows=json.loads((P/'verses_map.json').read_text())
    # Fondu très court de la scène précédente vers la suivante, AVANT les sous-titres.
    # Aucun dédoublement ou voile n'est appliqué aux paroles.
    times=[r['debut_source'] for r in rows[1:]]
    phases=['+'.join(f'between(t,{t+offset:.3f},{t+offset+.079:.3f})' for t in times) for offset in (0,.08,.16)]
    scene="fps=30,scale=1080:1935:flags=bicubic,crop=1080:1920:0:0,zoompan=z='1.055+0.022*sin(on/55)':x='iw/2-(iw/zoom/2)+13*sin(on/47)':y='ih/2-(ih/zoom/2)+9*sin(on/61)':d=1:s=1080x1920:fps=30,noise=alls=3:allf=t"
    graph=(f"[0:v]{scene},split=2[direct][delayed];"
           f"[delayed]tpad=start_mode=clone:start_duration=0.24,setpts=PTS-STARTPTS,split=3[l1][l2][l3];"
           f"[direct][l1]blend=all_mode=normal:all_opacity=0.25:enable='{phases[0]}'[b1];"
           f"[b1][l2]blend=all_mode=normal:all_opacity=0.50:enable='{phases[1]}'[b2];"
           f"[b2][l3]blend=all_mode=normal:all_opacity=0.75:enable='{phases[2]}',ass={WORK/'paroles.ass'}[v];"
           f"[1:a:0]apad=pad_dur=5.1[a]")
    run([FF,'-y','-hide_banner','-loglevel','warning','-f','concat','-safe','0','-i',WORK/'images.ffconcat','-i',ROOT/'Je plane.mp3',
        '-filter_complex',graph, '-map','[v]','-map','[a]', '-t',str(20 if preview else END),
        '-r','30','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
        '-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',dest])

def teasers():
    source=OUT/'JE-PLANE-DSKY-LYRICS-9x16.mp4'
    # Deux reprises du refrain ; coupes à vérifier à l'écoute.
    for number,start in [(1,10.41),(2,133.54)]:
        dest=OUT/f'JE-PLANE-DSKY-TEASER-{number}.mp4'
        run([FF,'-y','-hide_banner','-loglevel','warning','-ss',str(start),'-i',source,'-t','15',
             '-map','0:v:0','-map','0:a:0','-vf','fps=30:start_time=0','-frames:v','450','-c:v','libx264','-preset','ultrafast','-crf','25',
             '-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',dest])

if __name__=='__main__':
    action=sys.argv[1] if len(sys.argv)>1 else 'prepare'
    if action=='prepare':
        subprocess.run([sys.executable,str(P/'build_map.py')],check=True)
        rows=json.loads((P/'verses_map.json').read_text()); assert all(x['disponible'] and x['texte_affiche'] for x in rows)
        covers(); normalize_assets(rows); ass(rows); mp3()
    elif action=='render': render()
    elif action=='preview': render(preview=True)
    elif action=='teasers': teasers()
    else: raise SystemExit('prepare | preview | render | teasers')
