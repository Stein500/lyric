#!/usr/bin/env python3
"""Measure the original, normalize in two passes, preserve the full song.

Temporary WAVs stay in ignored work/. No voice or musical content is generated.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import warnings

import imageio_ffmpeg
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, find_peaks, sosfilt, stft, correlate

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / 'vivi-oor/production'
WORK = ROOT / 'work/vivi-production'
FF = imageio_ffmpeg.get_ffmpeg_exe()
SOURCE = ROOT / 'VIVI OOR.mp3'


def run(args, logfile):
    p = subprocess.run([FF, '-hide_banner', '-y', *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (WORK / logfile).write_text(p.stderr + '\n' + p.stdout)
    if p.returncode:
        raise RuntimeError(p.stderr[-5000:])
    return p


def loudness(path, filters='', target=-1.8, log='loudness.log'):
    chain = (filters + ',' if filters else '') + f'loudnorm=I=-14:TP={target}:LRA=11:print_format=json'
    p = run(['-v','info','-i',str(path),'-map','0:a:0','-vn','-af',chain,'-f','null','-'],log)
    matches = re.findall(r'\{\s*"input_i".*?\}',p.stderr,re.S)
    assert matches, 'FFmpeg must emit loudnorm JSON at info level.'
    return json.loads(matches[-1])


def main():
    WORK.mkdir(parents=True,exist_ok=True)
    (PROJECT/'metadata').mkdir(exist_ok=True,parents=True)
    run(['-v','info','-i',str(SOURCE),'-map','0:a:0','-vn','-ar','48000','-ac','2','-c:a','pcm_f32le',str(WORK/'source48.wav')],'source_decode.log')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        sr,audio=wavfile.read(WORK/'source48.wav')
    assert sr==48000 and audio.ndim==2 and audio.shape[1]==2
    duration=len(audio)/sr
    source_measure=loudness(SOURCE,log='source_loudness.log')
    filtering='highpass=f=30,lowpass=f=18000'
    measured=loudness(SOURCE,filters=filtering,log='filtered_measure.log')
    normalization=(f"loudnorm=I=-14:TP=-1.8:LRA=11:measured_I={measured['input_i']}:"
                   f"measured_TP={measured['input_tp']}:measured_LRA={measured['input_lra']}:"
                   f"measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}:"
                   'linear=true:print_format=json')
    sample_count=round(duration*sr)
    chain=('asetpts=PTS-STARTPTS,'+filtering+','+normalization+
           f',aresample=48000:first_pts=0,apad=whole_len={sample_count},atrim=end_sample={sample_count}')
    run(['-v','info','-i',str(WORK/'source48.wav'),'-map','0:a:0','-vn','-af',chain,
         '-ar','48000','-ac','2','-c:a','pcm_f32le','-t',f'{duration:.9f}',str(WORK/'master48.wav')],'normalization_pass2.log')
    result=loudness(WORK/'master48.wav',log='normalized_loudness.log')
    # Source timing features are a musical proxy, NOT ASR word recognition.
    mono=audio.mean(axis=1)[::3].astype(np.float64)
    del audio
    sample_rate=sr//3
    band=sosfilt(butter(3,[250,3500],btype='bandpass',fs=sample_rate,output='sos'),mono)
    nperseg,hop=512,160
    frequencies,t,z=stft(band,fs=sample_rate,nperseg=nperseg,noverlap=nperseg-hop,boundary=None,padded=False)
    mag=np.log1p(12*np.abs(z)); flux=np.maximum(np.diff(mag,axis=1),0).sum(axis=0)
    times=t[1:]
    norm=flux/(float(np.std(flux))+1e-12)
    peaks,_=find_peaks(norm,distance=12,prominence=.25)
    ac=correlate(norm-norm.mean(),norm-norm.mean(),mode='full',method='fft')[len(norm)-1:]
    candidates,_=find_peaks(ac)
    choices=sorted([i for i in candidates if 65<=60/(i*hop/sample_rate)<=180],key=lambda i:ac[i],reverse=True)[:5]
    tempo=[dict(bpm=round(60/(i*hop/sample_rate),2),strength=round(float(ac[i]/ac[0]),3)) for i in choices]
    sections=[]
    for name,start,end in [('intro',0,21.13),('refrain1',21.13,41.97),('couplet1',41.97,63.51),
                           ('liaison1',63.51,74.78),('refrain2',74.78,94.79),('couplet2',94.79,116.76),
                           ('liaison2',116.76,128.17),('pont',128.17,138.82),('refrain3',138.82,158.43),('outro',158.43,duration)]:
        x=mono[int(start*sample_rate):int(end*sample_rate)]
        rms=20*np.log10(max(float(np.sqrt(np.mean(x*x))),1e-10))
        sections.append(dict(name=name,start=start,end=end,rms_dbfs_mono=round(rms,2)))
    # Compact feature file: only detected onset candidates, no audio data.
    features=dict(hop_seconds=hop/sample_rate,onsets=[dict(t=round(float(times[i]),4),strength=round(float(norm[i]),4)) for i in peaks])
    (WORK/'onsets.json').write_text(json.dumps(features))
    analysis=dict(
        source='VIVI OOR.mp3',source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        sample_rate=sr,channels=2,decoded_duration=duration,
        original_loudness=source_measure,filtered_pass1=measured,normalized_wav=result,
        tempo_candidates=tempo,sections_estimated_from_lyrics=sections,
        word_alignment_note='No ASR model available over the network. Lyric line times supplied by the artist are authoritative. Word positions will be estimated from syllable weights, repetition templates and bounded musical onset adjustments; they are not independently verified vocal alignments.',
        processing='Full original song; explicit audio mapping; highpass 30 Hz, lowpass 18 kHz, two-pass loudnorm I=-14 / TP=-1.8. No hook or appended silence in the MP3.',
    )
    (PROJECT/'metadata/audio_analysis.json').write_text(json.dumps(analysis,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'duration':duration,'source':source_measure,'normalized':result,'tempo_candidates':tempo},ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    main()
