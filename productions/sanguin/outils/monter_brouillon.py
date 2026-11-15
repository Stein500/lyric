#!/usr/bin/env python3
"""Render a provisional full preview using source timings; Pillow + imageio-ffmpeg required.
No modifications to original audio. Review images/word timing before final delivery.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg,json,math,subprocess

ROOT=Path(__file__).resolve().parent.parent
REPO=ROOT.parent.parent
WORK=REPO/'.cache'/'sanguin-render'
WORK.mkdir(parents=True,exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe(); FPS=30; END=172.799979

def run(args): subprocess.run(args,check=True)
def alpha_weights(t):
    # 2.4 seconds per word with a 0.4 second crossfade centred on each switch.
    p=t%4.8
    if p<.2: return .5+p/0.4, .5-p/0.4
    if p<2.2: return 1.,0.
    if p<2.6: return (2.6-p)/.4,(p-2.2)/.4
    if p<4.6: return 0.,1.
    return (p-4.6)/.4,(4.8-p)/.4

def badge():
    path=WORK/'badge.mov'; font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',32)
    cmd=[FF,'-y','-loglevel','error','-f','rawvideo','-pixel_format','rgba','-video_size','1080x220','-framerate','30','-i','-','-an','-c:v','qtrle',str(path)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(144):
            a,b=alpha_weights(i/FPS); im=Image.new('RGBA',(1080,220)); d=ImageDraw.Draw(im)
            for word,weight in [('DSKY',a),('WTBW',b)]:
                if weight<=0: continue
                layer=Image.new('RGBA',im.size); ld=ImageDraw.Draw(layer); opacity=round(184*weight)
                ld.text((540,145),word,anchor='mm',font=font,fill=(255,255,255,opacity),stroke_width=2,stroke_fill=(0,0,0,opacity))
                half=31 if word=='DSKY' else 36; ld.line((540-half,168,540+half,168),fill=(255,255,255,opacity),width=2)
                im=Image.alpha_composite(im,layer)
            p.stdin.write(im.tobytes())
    finally: p.stdin.close()
    if p.wait(): raise RuntimeError('badge rendering failed')
    return path

def frames(t):
    mm,ss=t.split(':'); return round((int(mm)*60+float(ss))*FPS)

def main():
    rows=json.loads((ROOT/'verses_map.json').read_text(encoding='utf-8'))
    if not all((ROOT/r['image']).is_file() for r in rows): raise RuntimeError('Missing images')
    badge_file=badge(); end=round(END*FPS); segments=[]
    for i,r in enumerate(rows):
        start=frames(r['t']); stop=frames(rows[i+1]['t']) if i+1<len(rows) else end
        count=stop-start
        if count<=0: raise ValueError('Non-increasing timestamp')
        dest=WORK/f'{i:03}.mp4'; duration=count/FPS
        # A gentle 2% crop slides in four directions. Inspect all text placement in final QC.
        traj=[('0','iw-1080','0','ih-1920'),('iw-1080','0','0','ih-1920'),('0.18*(iw-1080)','0.82*(iw-1080)','ih-1920','0'),('0.82*(iw-1080)','0.18*(iw-1080)','0','ih-1920')][i%4]
        x0,x1,y0,y1=traj; u=f'min(t/{duration:.6f},1)'
        x=f'({x0})+(({x1})-({x0}))*{u}'; y=f'({y0})+(({y1})-({y0}))*{u}'
        filters=f"[0:v]scale=1102:1958:flags=lanczos,crop=1080:1920:x='{x}':y='{y}'[base];[base][1:v]overlay=0:0:shortest=1:format=auto,format=yuv420p[v]"
        run([FF,'-y','-loglevel','error','-loop','1','-framerate','30','-i',str(ROOT/r['image']),'-stream_loop','-1','-i',str(badge_file),'-filter_complex',filters,'-map','[v]','-an','-frames:v',str(count),'-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-r','30',str(dest)])
        segments.append(dest);print(f'Plan {i+1}/{len(rows)} : {count} images',flush=True)
    paths=[ROOT/'livrables/APERCU-intro-inspire-muet.mp4',*segments,ROOT/'livrables/APERCU-outro-inspire-muet.mp4']
    concat=WORK/'concat.txt';concat.write_text(''.join("file '"+str(p).replace("'", "'\\''")+"'\n" for p in paths))
    video=WORK/'video.mp4'
    run([FF,'-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-map','0:v:0','-an','-c','copy',str(video)])
    final=ROOT/'livrables'/'SANGUIN-DSKY-WTBW-9x16-BROUILLON.mp4'
    run([FF,'-y','-loglevel','error','-i',str(video),'-i',str(REPO/'Sanguin.mp3'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af','apad=pad_dur=5.00','-c:a','aac','-b:a','256k','-ar','48000','-t',str((end+150)/FPS),'-movflags','+faststart',str(final)])
    print('BROUILLON:',final,flush=True)
if __name__=='__main__': main()
