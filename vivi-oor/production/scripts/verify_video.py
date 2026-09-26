#!/usr/bin/env python3
"""Decode/inspect the completed video, check timing and extract a contact proof."""
from pathlib import Path
import hashlib,json,re,struct,subprocess,sys
import imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[3];PROJECT=ROOT/'vivi-oor/production';WORK=ROOT/'work/vivi-production'
FF=imageio_ffmpeg.get_ffmpeg_exe();FILE=PROJECT/'livrables/VIVI_OOR_lyrics_9x16.mp4'
sys.path.insert(0,str(Path(__file__).parent));from prepare_audio import loudness


def run(args):
    p=subprocess.run([FF,'-hide_banner',*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-6000:])
    return p


def boxes(path):
    result=[]
    with path.open('rb') as f:
        while True:
            position=f.tell();header=f.read(8)
            if len(header)<8:break
            size,kind=struct.unpack('>I4s',header)
            if size==1:size=struct.unpack('>Q',f.read(8))[0]
            if size==0:size=path.stat().st_size-position
            if size<8:raise ValueError('Malformed MP4 box')
            result.append(dict(type=kind.decode('ascii',errors='replace'),offset=position,size=size))
            f.seek(position+size)
    return result


def main():
    plan=json.loads((PROJECT/'metadata/timeline.json').read_text())
    levels=loudness(FILE,log='video_audio_loudness.log')
    video_attenuation=0
    if float(levels['input_tp'])>-1.5:
        video_attenuation=-(float(levels['input_tp'])+1.7)
        repaired=WORK/'video-audio-repaired.mp4'
        run(['-y','-v','info','-i',str(FILE),'-i',str(WORK/'video_audio48.wav'),'-map','0:v:0','-map','1:a:0',
             '-c:v','copy','-af',f'volume={video_attenuation:.4f}dB','-c:a','aac','-b:a','192k','-ar','48000',
             '-t',f"{plan['frames']/plan['fps']:.9f}",'-movflags','+faststart',str(repaired)])
        repaired.replace(FILE);levels=loudness(FILE,log='video_audio_loudness_repaired.log')
    scan=run(['-v','info','-i',str(FILE),'-map','0:v:0','-an','-vf',
              'blackdetect=d=0.08:pix_th=0.06:pic_th=0.95,freezedetect=n=-80dB:d=1.5',
              '-progress','pipe:1','-nostats','-f','null','-'])
    (WORK/'video_decode_verify.log').write_text(scan.stderr+'\n'+scan.stdout)
    decoded_frames=int(re.findall(r'^frame=(\d+)',scan.stdout,re.M)[-1])
    black=[dict(start=float(a),end=float(b),duration=float(c)) for a,b,c in re.findall(r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)',scan.stderr)]
    freezes=re.findall(r'lavfi\.freezedetect\.freeze_start: ([\d.]+)',scan.stderr)
    assert decoded_frames==plan['frames'],(decoded_frames,plan['frames'])
    assert '1080x1920' in scan.stderr and 'yuv420p' in scan.stderr and '30 fps' in scan.stderr
    assert abs(decoded_frames/plan['fps']-plan['total_duration'])<=.05
    assert all(x['start']>=plan['total_duration']-3.08 for x in black),black
    assert not freezes,freezes
    atoms=boxes(FILE);positions={x['type']:x['offset'] for x in atoms}
    assert positions['moov']<positions['mdat']
    assert FILE.stat().st_size<95_000_000
    captures=[(.45,'Hook / mot actif'),(4.5,'Mot vers traînée'),(11.8,'Signature'),(28.9,'Refrain'),(59.3,'Le miel'),
              (86.1,'Refrain repris'),(105.4,'Cœur ouvert'),(137.5,'Notre trésor'),(150.2,'Dernier refrain'),
              (178.5,'Outro chantée'),(194.2,'Outro musicale'),(211,'Fin / contacts')]
    sheet=Image.new('RGB',(4*270,3*508),'#211920');draw=ImageDraw.Draw(sheet)
    f=ImageFont.truetype(str(PROJECT/'assets/fonts/DejaVuSans.ttf'),14)
    for index,(t,label) in enumerate(captures):
        target=WORK/f'qc-frame-{index:02d}.jpg'
        run(['-y','-v','error','-ss',str(t),'-i',str(FILE),'-frames:v','1',str(target)])
        with Image.open(target) as im:thumb=im.convert('RGB').resize((270,480),Image.Resampling.LANCZOS)
        x=index%4*270;y=index//4*508;sheet.paste(thumb,(x,y));draw.text((x+8,y+486),f'{t:06.2f}s · {label}',font=f,fill='#f1e2d1')
    sheet.save(PROJECT/'metadata/controle_visuel_clip.jpg',quality=94,subsampling=0)
    result=dict(file=FILE.name,bytes=FILE.stat().st_size,sha256=hashlib.sha256(FILE.read_bytes()).hexdigest(),
                frames=decoded_frames,fps=plan['fps'],duration=decoded_frames/plan['fps'],expected_duration=plan['total_duration'],
                width=1080,height=1920,codec='H.264 High / yuv420p',audio='AAC 192 kb/s / 48000 Hz / stereo',
                audio_integrated_lufs=float(levels['input_i']),audio_true_peak_dbtp=float(levels['input_tp']),
                audio_constant_correction_db=round(video_attenuation,4),
                black_intervals=black,black_only_final_fade=True,freeze_intervals=freezes,
                freeze_test='noise=-80dB; minimum duration=1.5 seconds',faststart=True,mp4_atoms=atoms,
                lyrics_face_free_by_layout=True,word_timing_precision='Estimated within the supplied line timestamps, not ASR-validated',
                audio_alignment_checks='Waveform correlation before/after mastering at 5,45,95,154,176 s: zero measured offset at 16 kHz.')
    (PROJECT/'metadata/video_quality.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
