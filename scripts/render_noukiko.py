"""Render the supplied timed lyrics without ffprobe or external binary downloads.
Setup: python -m venv .venv && .venv/bin/pip install imageio-ffmpeg pillow
Run: .venv/bin/python scripts/render_noukiko.py
"""
from pathlib import Path
import re
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'renders'
OUT.mkdir(exist_ok=True)
SLIDES = OUT / 'slides'
SLIDES.mkdir(exist_ok=True)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
audio = ROOT / 'Noukiko tché wê.mp3'
info = subprocess.run([ffmpeg, '-hide_banner', '-i', str(audio)], capture_output=True, text=True).stderr
m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', info)
if not m:
    raise RuntimeError('Cannot determine audio duration: ' + info)
duration = int(m[1])*3600 + int(m[2])*60 + float(m[3])
entries = [(0., 'Noukiko tché wê', 'C’est mon sourire à moi')]
for line in (ROOT / 'Noukiko.txt').read_text().splitlines():
    match = re.match(r'\[(\d+):(\d+\.\d+)\](.+)', line)
    if match:
        entries.append((int(match[1])*60 + float(match[2]), match[3], ''))
assert all(a[0] < b[0] for a,b in zip(entries,entries[1:]))
assert entries[-1][0] < duration
fontpath = ROOT / 'dsky-quotes/assets/fonts/Montserrat.ttf'
def font(size):
    return ImageFont.truetype(str(fontpath), size)
base = Image.new('RGB', (1280,720))
d = ImageDraw.Draw(base)
for y in range(720):
    t=y/720
    d.line((0,y,1280,y), fill=(int(12+9*t),int(23+15*t),int(34+13*t)))
d.ellipse((920,-320,1580,340), outline=(47,65,69), width=2)
d.ellipse((-380,430,290,1100), outline=(47,65,69), width=2)
d.line((90,105,1190,105), fill=(61,77,80), width=1)
d.text((90,65), 'Wolof TechStein', font=font(22), fill=(224,180,95))
d.text((1190,65), 'NOUKIKO TCHÉ WÊ', font=font(20), fill=(186,196,199), anchor='ra')
d.text((640,635), 'C’EST MON SOURIRE À MOI', font=font(17), fill=(160,177,180), anchor='mm')
concat=[]
for i,(start,text,subtitle) in enumerate(entries):
    im=base.copy(); d=ImageDraw.Draw(im)
    f=font(58 if i==0 else 48)
    lines=[]; current=''
    for word in text.split():
        candidate=(current+' '+word).strip()
        if current and d.textlength(candidate,font=f)>1050:
            lines.append(current); current=word
        else:
            current=candidate
    lines.append(current)
    top=340-(len(lines)-1)*36
    for j,line in enumerate(lines):
        d.text((640,top+j*72),line,font=f,fill=(249,238,211),anchor='mm')
    d.rounded_rectangle((600,top+len(lines)*72-24,680,top+len(lines)*72-20),radius=2,fill=(224,180,95))
    if subtitle:
        d.text((640,460),subtitle,font=font(25),fill=(181,196,200),anchor='mm')
    path=SLIDES/f'{i:03d}.png'; im.save(path)
    end=entries[i+1][0] if i+1<len(entries) else duration
    concat.extend([f"file 'slides/{path.name}'", f'duration {end-start:.6f}'])
concat.append(f"file 'slides/{path.name}'")
manifest=OUT/'slides.ffconcat'
manifest.write_text('\n'.join(concat)+'\n')
output=OUT/'Noukiko-tche-we-lyrics.mp4'
cmd=[ffmpeg,'-y','-hide_banner','-loglevel','warning','-f','concat','-safe','0','-i',str(manifest),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-map_metadata','-1','-c:v','libx264','-preset','veryfast','-crf','22','-r','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(duration),'-movflags','+faststart',str(output)]
subprocess.run(cmd,check=True)
# Decode the actual output to catch corrupt video/audio, not just a dry run.
subprocess.run([ffmpeg,'-v','error','-i',str(output),'-map','0:v','-map','0:a','-f','null','-'],check=True)
print(f'Validated: {output} ({duration:.2f}s, {output.stat().st_size} bytes)',flush=True)
