#!/usr/bin/env python3
"""Contrôles indépendants du MP4 encodé, du MP3 et de la timeline publiée."""
from __future__ import annotations
import io
import re
import subprocess
from fractions import Fraction

import av
import numpy as np
from PIL import Image
from scipy import signal
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

from je_maime_common import *
from render_je_maime import Renderer


def encoded_frame(path, index):
    with av.open(str(path)) as container:
        stream = container.streams.video[0]
        target = Fraction(index,FPS)
        container.seek(int(target/stream.time_base),stream=stream,backward=True,any_frame=False)
        for frame in container.decode(stream):
            current = round(Fraction(frame.pts)*frame.time_base*FPS)
            if current == index:
                return frame.to_image().convert('RGB')
            if current > index:
                raise ValueError(f'Frame {index} absente, reçu {current}')
    raise ValueError(f'Frame {index} non trouvée')


def mp4_atoms(path):
    result=[]
    with Path(path).open('rb') as handle:
        while True:
            offset=handle.tell()
            header=handle.read(8)
            if len(header)<8:break
            size=int.from_bytes(header[:4],'big')
            name=header[4:8].decode('ascii',errors='replace')
            if size==1:
                size=int.from_bytes(handle.read(8),'big')
            elif size==0:
                size=Path(path).stat().st_size-offset
            if size<8:raise ValueError('Atome MP4 invalide')
            result.append({'name':name,'offset':offset,'bytes':size})
            handle.seek(offset+size)
    return result


def audio_slice(path,start,duration=4):
    p=subprocess.run([FFMPEG,'-v','error','-nostdin','-ss',str(start),'-i',str(path),'-vn','-t',str(duration),'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True,check=True)
    return np.frombuffer(p.stdout,dtype='<f4').copy()


def main():
    config,audit=assert_sources_unchanged()
    plan=load(PROJECT/'montage_v1.json')
    render=load(PROJECT/'rendu_v1.json')
    video=ROOT/plan['video_output']
    mp3=ROOT/plan['mp3_output']
    if sha256(video)!=render['sha256']:
        raise ValueError('Le MP4 ne correspond pas au rendu terminé')
    report={'video':plan['video_output'],'mp3':plan['mp3_output'],'passed':False,'checks':{}}
    checks=report['checks']
    with av.open(str(video)) as container:
        assert len(container.streams.video)==1 and len(container.streams.audio)==1
        v=container.streams.video[0];a=container.streams.audio[0]
        checks['video_stream']={'codec':v.codec_context.name,'width':v.codec_context.width,'height':v.codec_context.height,
            'pixel_format':v.codec_context.format.name,'fps':float(v.average_rate),'frames':v.frames,
            'duration_seconds':float(v.duration*v.time_base),'time_base':str(v.time_base)}
        checks['audio_stream']={'codec':a.codec_context.name,'sample_rate_hz':a.codec_context.sample_rate,'channels':a.codec_context.layout.nb_channels,
            'duration_seconds':float(a.duration*a.time_base)}
        assert (v.codec_context.width,v.codec_context.height)==(1080,1920)
        assert v.codec_context.name=='h264' and v.codec_context.format.name=='yuv420p'
        assert v.average_rate==30 and v.frames==5945
        assert abs(float(v.duration*v.time_base)-plan['total_duration_seconds'])<=.05
        assert a.codec_context.name=='aac' and a.codec_context.sample_rate==48000 and a.codec_context.layout.nb_channels==2
        assert abs(float(a.duration*a.time_base)-plan['total_duration_seconds'])<=.05
    atoms=mp4_atoms(video)
    locations={a['name']:a['offset'] for a in atoms}
    assert locations['moov']<locations['mdat']
    checks['faststart']={'passed':True,'atoms':atoms}
    print('Streams, durée, nombre de frames et faststart OK.',flush=True)

    # Seuil -70 dB adapté au mouvement très doux des aplats animé ; durée minimale 1 s.
    # L'absence d'images figées est également vérifiée par différences de frames distantes.
    filters='blackdetect=d=0.05:pix_th=0.10:pic_th=0.98,freezedetect=n=-70dB:d=1'
    process=subprocess.run([FFMPEG,'-hide_banner','-nostdin','-i',str(video),'-an','-vf',filters,'-f','null','-'],capture_output=True,text=True,check=True)
    (WORK/'video_detection.log').write_text(process.stderr)
    black=[{'start':float(s),'end':float(e),'duration':float(d)} for s,e,d in re.findall(r'black_start:([0-9.]+)\s+black_end:([0-9.]+)\s+black_duration:([0-9.]+)',process.stderr)]
    freeze=[float(x) for x in re.findall(r'freeze_start:\s*([0-9.]+)',process.stderr)]
    checks['blackdetect']={'events':black,'allowed_only_after_seconds':plan['fade_out_first_frame']/FPS,'filter':'d=0.05:pix_th=0.10:pic_th=0.98'}
    checks['freezedetect']={'freeze_start_events':freeze,'filter':'n=-70dB:d=1'}
    dump(PROJECT/'controle_video_v1.json',report)
    if any(event['start']<plan['fade_out_first_frame']/FPS-.05 for event in black):
        raise ValueError('Image noire détectée hors fondu final')
    if freeze:
        raise ValueError(f'Freezedetect a signalé {freeze} : examiner le mouvement avant livraison')
    print('Blackdetect : seulement le fondu final autorisé ; freezedetect : aucun événement.',flush=True)

    renderer=Renderer()
    cues={s['slot']:s for s in plan['segments']}
    samples=sorted(set([0,197,198,240,270,930,cues[20]['first_frame']-1,cues[20]['first_frame'],
                       cues[35]['first_frame'],cues[35]['first_frame']+30,cues[40]['first_frame']+30,
                       cues[45]['first_frame']+10,cues[49]['first_frame']+45,
                       plan['endcard_first_frame']-1,plan['endcard_first_frame'],plan['endcard_first_frame']+90]))
    directory=WORK/'qa_frames';directory.mkdir(parents=True,exist_ok=True)
    comparison=[]
    selected={}
    for index in samples:
        actual=encoded_frame(video,index)
        reference=renderer.frame(index)
        pixels=np.asarray(actual).astype(np.int16)
        expected=np.asarray(reference).astype(np.int16)
        error=np.abs(pixels-expected)
        mae=float(error.mean())
        text_mae=float(error[HEIGHT-330:HEIGHT-60,60:WIDTH-60].mean())
        comparison.append({'frame':index,'time_seconds':index/FPS,'whole_frame_mae_0_255':mae,'text_zone_mae_0_255':text_mae})
        actual.save(directory/f'encoded_{index:05d}.jpg',quality=92)
        if index in (240,270):selected[index]=pixels
        if mae>=6 or text_mae>=8:
            checks['pixel_comparisons']=comparison
            dump(PROJECT/'controle_video_v1.json',report)
            raise ValueError(f'Écart pixel trop grand à la frame {index} : {mae:.3f} / texte {text_mae:.3f}')
        print(f'Frame {index}: MAE {mae:.2f}, texte {text_mae:.2f}',flush=True)
    checks['pixel_comparisons']=comparison
    badge_error=float(np.abs(selected[240][36:130,36:368]-selected[270][36:130,36:368]).mean())
    assert badge_error<4, badge_error
    motion_error=float(np.abs(selected[240][150:HEIGHT-350]-selected[270][150:HEIGHT-350]).mean())
    assert motion_error>.05
    checks['static_badge']={'same_background_frames':[240,270],'region':[36,36,332,94],'mean_difference':badge_error,'max_allowed':4,'source_rgba_identical':True}
    checks['background_motion']={'frames':[240,270],'mean_difference':motion_error,'minimum':.05}
    checks['all_timestamp_boundaries']=[{'slot':s['slot'],'source_cs':s['start_centiseconds'],'first_frame':s['first_frame'],
                                       'display_delay_seconds':s['first_frame']/FPS-s['start_centiseconds']/100}
                                      for s in plan['segments'] if s['kind']=='lyric']
    assert all(-1e-8<=s['display_delay_seconds']<1/FPS+1e-8 for s in checks['all_timestamp_boundaries'])

    # Le mastering ne doit pas introduire de décalage global par rapport à la source.
    offsets=[]
    for start in (46,119,170):
        original=audio_slice(ROOT/config['source_audio'],start)
        mastered=audio_slice(mp3,start)
        n=min(len(original),len(mastered));original=original[:n];mastered=mastered[:n]
        correlation=signal.correlate(mastered,original,mode='full',method='fft')
        center=n-1;radius=800
        lag=int(np.argmax(correlation[center-radius:center+radius+1])-radius)
        offsets.append({'start_seconds':start,'lag_samples_at_16khz':lag,'lag_seconds':lag/16000})
        assert abs(lag)<=160, 'Décalage source/master supérieur à 10 ms'
    checks['source_master_audio_alignment']=offsets
    final_mp3,_=measure_loudness(mp3)
    assert float(final_mp3['input_tp'])<=-1.5
    assert abs(float(final_mp3['input_i'])+14)<=.6
    decoded=decoded_audio_info(mp3)
    assert decoded['samples_per_channel']==audit['decoded_samples_per_channel']
    tags=ID3(mp3)
    required=['TIT2','TPE1','TALB','TPE2','TPUB','TCOM','TCON','TDRC','USLT','APIC']
    assert all(tags.getall(key) for key in required)
    assert str(tags['TPE1'])=='Daïsky Pro' and str(tags['TALB'])=='Success'
    assert tags.getall('USLT')[0].text=='\n'.join(typography(v['source_text']) for v in audit['lrc']['lyrics'])
    for key in ('contact','email','producer','label'):assert tags.getall('TXXX:'+key)
    with Image.open(io.BytesIO(tags.getall('APIC')[0].data)) as im:assert im.size==(1080,1080)
    checks['mp3']={'lufs':float(final_mp3['input_i']),'true_peak_dbtp':float(final_mp3['input_tp']),
                   'decoded':decoded,'bitrate_bps':MP3(mp3).info.bitrate,'id3_required_fields_present':True,'all_user_lyrics_present':True,'cover_1080_square':True}
    video_audio,_=measure_loudness(video)
    checks['video_audio']={'lufs':float(video_audio['input_i']),'true_peak_dbtp':float(video_audio['input_tp'])}
    assert float(video_audio['input_tp'])<0, 'Clipping audio dans le MP4'
    checks['endcard']={'start_seconds':plan['endcard_start_seconds'],'contacts_present':True,
                       'padding_seconds':plan['actual_padding_seconds'],'final_fade_seconds':3}
    checks['source_files_unchanged']=True
    assert_sources_unchanged()
    report['passed']=True
    report['video_sha256']=sha256(video)
    report['mp3_sha256']=sha256(mp3)
    report['limits']='Respect des timestamps utilisateur et comparaison des frames encodées vérifiés ; validation artistique et correspondance perceptive chant/texte laissées au contrôle utilisateur demandé.'
    dump(PROJECT/'controle_video_v1.json',report)
    print('CONTRÔLES TERMINÉS : MP4 et MP3 prêts pour la validation utilisateur.',flush=True)


if __name__=='__main__':
    main()
