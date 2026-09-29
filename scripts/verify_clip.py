#!/usr/bin/env python3
"""Contrôles du MP4 terminé : durée, flux, couleur, horloge et scènes.

La corrélation audio contrôle l'absence de dérive au montage, pas l'exactitude
phonétique de chaque mot ; l'animation des mots reste une estimation déclarée.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scipy.signal import correlate

from render_clip import ROOT, STATE, WORK, ClipRenderer

FF = imageio_ffmpeg.get_ffmpeg_exe()


def run(args, timeout=240):
    result = subprocess.run([FF,'-hide_banner','-nostdin',*args],capture_output=True,timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8',errors='replace')[-5000:])
    return result


def audio_window(path,start,duration=5):
    data=run(['-v','error','-i',str(path),'-ss',str(start),'-t',str(duration),
              '-map','0:a:0','-vn','-ar','12000','-ac','1','-f','f32le','pipe:1']).stdout
    return np.frombuffer(data,dtype='<f4')


def verify(fmt):
    renderer=ClipRenderer(fmt)
    label='9x16' if fmt=='portrait' else '16x9_YT'
    video=ROOT/f'livrables/Concentre_sur_le_chemin_{label}_v1.mp4'
    if not video.is_file():raise RuntimeError('Clip manquant.')
    check=run(['-v','info','-progress','pipe:1','-i',str(video),'-map','0:v:0','-an',
               '-vf','blackdetect=d=0.1:pix_th=0.04:pic_th=0.98,freezedetect=n=-70dB:d=1',
               '-f','null','-'])
    log=check.stderr.decode();progress=check.stdout.decode()
    (WORK/f'qa_{fmt}.log').write_text(log)
    count=int(re.findall(r'^frame=(\d+)$',progress,re.M)[-1])
    duration=int(re.findall(r'^out_time_us=(\d+)$',progress,re.M)[-1])/1e6
    if count!=renderer.frames or abs(duration-renderer.frames/renderer.fps)>.05:
        raise AssertionError(('Durée/frames',count,duration))
    streams=[line.strip() for line in log.splitlines() if 'Stream #0:' in line][:2]
    if not any('h264' in line and '30 fps' in line for line in streams):
        raise AssertionError(streams)
    if not any('aac' in line and '48000 Hz' in line and 'stereo' in line for line in streams):
        raise AssertionError(streams)
    black_starts=[float(t) for t in re.findall(r'black_start:([\d.]+)',log)]
    freezes=[line.strip() for line in log.splitlines() if 'freeze_start:' in line]
    if any(t<renderer.total-3.05 for t in black_starts):
        raise AssertionError(('Noir hors fondu final',black_starts))
    if freezes:
        raise AssertionError(('Gel détecté',freezes))
    # The first verse in three separated sections, hook boundary, five scenes, endcard.
    points=[0,1.0,3.5,6.8666667,6.9,7.3,8.7,32.1666667,32.6666667,34.95,
            46.4,66.8,92.4666667,93.0,119.5,134.4,147.4,151.2,
            159.7,160.2,190.6,200.0,217.05,218.0,220.5]
    indices=sorted({max(0,min(renderer.frames-1,round(t*renderer.fps))) for t in points})
    selection='+'.join(f'eq(n\\,{i})' for i in indices)
    data=run(['-v','error','-i',str(video),'-vf',f'select={selection}',
              '-vsync','0','-pix_fmt','rgb24','-f','rawvideo','pipe:1']).stdout
    frames=np.frombuffer(data,dtype=np.uint8).reshape((-1,renderer.h,renderer.w,3))
    if len(frames)!=len(indices):raise AssertionError('Extraction incomplète.')
    records=[]
    for index,actual in zip(indices,frames):
        t=index/renderer.fps
        expected=renderer.frame(t)
        error=float(np.abs(actual.astype(np.int16)-expected.astype(np.int16)).mean())
        if error>=6:
            raise AssertionError(('Écart reconstruction trop grand',fmt,index,error))
        footer=54 if fmt=='portrait' else 30
        coordinates=[(renderer.w//6,renderer.h-footer//2),
                     (renderer.w*2//3,renderer.h-footer+footer//4),
                     (renderer.w*2//3,renderer.h-max(1,footer//4))]
        colors=[actual[y,x].tolist() for x,y in coordinates]
        for color,ref in zip(colors,[(0,135,81),(252,209,22),(232,17,45)]):
            if max(abs(a-b) for a,b in zip(color,ref))>9:
                raise AssertionError(('Drapeau',index,color,ref))
        v=renderer.verse_at(t)
        records.append({'frame':index,'t':round(t,5),'mean_rgb_error':round(error,4),
                        'verse_id':v['id'] if v else None,'flag_samples':colors})
    # Decode matched musical windows, spanning the song. This catches drift/concat mistakes.
    sync=[]
    for source_time in [25.3,85.64,152.84]:
        a=audio_window(ROOT/'Concentré sur le chemin.mp3',source_time)
        b=audio_window(video,renderer.hook+source_time)
        correlation=correlate(b,a,mode='full',method='fft')
        lag=int(np.argmax(correlation))-(len(a)-1)
        lag_seconds=lag/12000
        if abs(lag_seconds)>.02:
            raise AssertionError(('Dérive audio',source_time,lag_seconds))
        sync.append({'source_start':source_time,'video_start':round(renderer.hook+source_time,5),
                     'measured_lag_seconds':lag_seconds})
    # Visual proof from actual encoded MP4 frames, not only pre-encode reconstructions.
    selected=[min(range(len(indices)),key=lambda j:abs(indices[j]/30-t))
              for t in [3.5,8.7,46.4,93.0,147.4,151.2,190.6,220.5]]
    cell_w,cell_h=(360,686) if fmt=='portrait' else (640,408)
    proof=Image.new('RGB',(cell_w*4,cell_h*2),'#101722')
    draw=ImageDraw.Draw(proof)
    font=ImageFont.truetype(str(ROOT/'assets/fonts/DejaVuSans-Bold.ttf'),18)
    for k,j in enumerate(selected):
        im=Image.fromarray(frames[j])
        thumb=ImageOps.contain(im,(cell_w-20,cell_h-46))
        x,y=(k%4)*cell_w,(k//4)*cell_h
        proof.paste(thumb,(x+(cell_w-thumb.width)//2,y+8))
        draw.text((x+12,y+cell_h-29),f'{indices[j]/30:.2f} s',font=font,fill='white')
    proof_path=ROOT/f'livrables/controle_clip_{label}_v1.jpg'
    proof.save(proof_path,quality=93)
    report={'file':str(video.relative_to(ROOT)),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),
            'size_bytes':video.stat().st_size,'frames':count,'fps':renderer.fps,
            'duration':duration,'streams':streams,'black_starts':black_starts,
            'black_allowed_only_after':round(renderer.total-3,5),'freeze_intervals':freezes,
            'freeze_detector':'noise=-70dB, duration>=1s',
            'frame_checks':records,'audio_sync_checks':sync,
            'word_alignment':'estimated, not forced vocal alignment',
            'proof':str(proof_path.relative_to(ROOT)),'status':'technical_checks_passed'}
    (STATE/f'qa_{fmt}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='frame_checks'},ensure_ascii=False,indent=2))
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--format',choices=['portrait','landscape'],required=True)
    verify(parser.parse_args().format)
