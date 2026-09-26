#!/usr/bin/env python3
"""Export and verify a full-length 320k MP3, then add artwork and lyrics safely."""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
import sys

import imageio_ffmpeg
from mutagen.mp3 import MP3
from mutagen.id3 import (ID3, TIT2, TPE1, TALB, TPE2, TPUB, TCON, TDRC,
                         TXXX, USLT, APIC, COMM, WOAS, GEOB, SYLT)

ROOT=Path(__file__).resolve().parents[3]
PROJECT=ROOT/'vivi-oor/production';WORK=ROOT/'work/vivi-production'
FF=imageio_ffmpeg.get_ffmpeg_exe()
sys.path.insert(0,str(Path(__file__).parent))
from prepare_audio import loudness


def run(args):
    result=subprocess.run([FF,'-hide_banner','-y',*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if result.returncode:raise RuntimeError(result.stderr[-6000:])
    return result


def main():
    analysis=json.loads((PROJECT/'metadata/audio_analysis.json').read_text())
    duration=analysis['decoded_duration']
    gain=-14-float(analysis['normalized_wav']['input_i'])
    mp3=PROJECT/'livrables/VIVI_OOR_master_320k.mp3'
    # Align the integrated level after the two-pass normalization; if the lossy
    # encoder introduces a true-peak overshoot, reduce only constant gain.
    for attempt in range(3):
        run(['-v','error','-i',str(WORK/'master48.wav'),'-map','0:a:0','-vn',
             '-af',f'volume={gain:.4f}dB','-ar','48000','-ac','2','-c:a','pcm_f32le',
             '-t',f'{duration:.9f}',str(WORK/'processed48.wav')])
        run(['-v','error','-i',str(WORK/'processed48.wav'),'-map','0:a:0','-vn','-map_metadata','-1',
             '-c:a','libmp3lame','-b:a','320k','-ar','48000','-ac','2','-id3v2_version','4',
             '-t',f'{duration:.9f}',str(mp3)])
        measured=loudness(mp3,log=f'mp3_verification_{attempt}.log')
        print('MP3 verification',measured['input_i'],measured['input_tp'],flush=True)
        peak=float(measured['input_tp'])
        if peak<=-1.5:break
        gain-=peak-(-1.7)
    else:raise RuntimeError('MP3 true peak did not meet the safe limit.')
    assert abs(float(measured['input_i'])-(-14))<=1.0
    original=MP3(ROOT/'VIVI OOR.mp3')
    source_text=(ROOT/'Vivi O O R.txt').read_text(encoding='utf-8-sig').replace('\u200e','')
    lines=[]
    for row in source_text.splitlines():
        match=re.match(r'\[(\d+):(\d+(?:\.\d+)?)\](.*)',row)
        if match:lines.append((match.group(3).strip(),round((int(match.group(1))*60+float(match.group(2)))*1000)))
    tags=ID3()
    for frame in [TIT2(encoding=3,text=['Vivi OOR']),TPE1(encoding=3,text=['Daïsky']),
                  TALB(encoding=3,text=['Vivi OOR — Single']),TPE2(encoding=3,text=['Daïsky']),
                  TPUB(encoding=3,text=['Daïsky Production']),TCON(encoding=3,text=['Afro-pop']),
                  TDRC(encoding=3,text=['2026'])]:tags.add(frame)
    for desc,text in [('contact','WhatsApp +229 01 61 16 24 08 / +229 01 49 11 49 51'),
                      ('email','daiskyproduction@gmail.com'),('producer','Wolof TechStein'),
                      ('label','Daïsky Production'),
                      ('master_process','EQ 30 Hz–18 kHz; two-pass EBU R128 normalization; 320 kb/s export. Source remains available unchanged.'),
                      ('source_sha256',analysis['source_sha256']),
                      ('provenance','Source made with Suno; original source metadata and C2PA manifest archived in this file. The original C2PA signature does not attest this re-encoded export.')]:
        tags.add(TXXX(encoding=3,desc=desc,text=[text]))
    # Do not invent an unconfirmed composer credit. Preserve known source origin.
    for frame in original.tags.getall('COMM')+original.tags.getall('WOAS'):
        tags.add(copy.deepcopy(frame))
    source_comments=[str(x) for x in original.tags.getall('TXXX') if x.desc=='comment']
    if source_comments:tags.add(TXXX(encoding=3,desc='source_comment',text=source_comments))
    c2pa=[]
    for index,frame in enumerate(original.tags.getall('GEOB')):
        tags.add(GEOB(encoding=3,mime=frame.mime,filename=f'original-source-{index}.c2pa',
                      desc='Original source provenance manifest; not a signature of this edited export',data=frame.data))
        c2pa.append(dict(mime=frame.mime,bytes=len(frame.data),sha256=hashlib.sha256(frame.data).hexdigest()))
    tags.add(USLT(encoding=3,lang='fra',desc='Paroles fournies par l’artiste',text='\n'.join(text for text,_ in lines)))
    tags.add(SYLT(encoding=3,lang='fra',format=2,type=1,desc='Vers — timecodes du fichier fourni',text=lines))
    cover=PROJECT/'livrables/cover_vivi_oor_1080x1080.jpg'
    tags.add(APIC(encoding=3,mime='image/jpeg',type=3,desc='Vivi OOR — Daïsky',data=cover.read_bytes()))
    tags.save(mp3,v2_version=4)
    tagged=MP3(mp3)
    assert tagged.info.sample_rate==48000 and tagged.info.channels==2 and tagged.info.bitrate==320000
    assert abs(tagged.info.length-duration)<.1
    assert tagged.tags.getall('USLT') and tagged.tags.getall('APIC') and tagged.tags.getall('SYLT')
    assert len(tagged.tags.getall('GEOB'))==len(c2pa)
    # Decode only the audio to verify that an APIC image cannot truncate playback.
    decoded=subprocess.run([FF,'-v','error','-i',str(mp3),'-map','0:a:0','-vn','-ar','48000','-ac','2','-f','s16le','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    decoded_duration=len(decoded.stdout)/(48000*2*2)
    assert abs(decoded_duration-duration)<.001,(decoded_duration,duration)
    report=dict(file=mp3.name,bytes=mp3.stat().st_size,sha256=hashlib.sha256(mp3.read_bytes()).hexdigest(),
                sample_rate=48000,channels=2,bitrate=320000,decoded_duration=decoded_duration,
                integrated_lufs=float(measured['input_i']),true_peak_dbtp=float(measured['input_tp']),
                loudness_range_lu=float(measured['input_lra']),constant_gain_after_pass2_db=round(gain,4),
                id3_version=list(tagged.tags.version),lyrics_entries=len(lines),cover='cover_vivi_oor_1080x1080.jpg',
                source_origin_preserved=True,source_manifests=c2pa,
                metadata_note='Daïsky and default contact/label metadata follow the artist prompt. Afro-pop is an editorial genre label; no unconfirmed composer is invented.',
                quality_note='320 kb/s is the output encoding, not a recovery of information missing from the original ~184 kb/s MP3.')
    (PROJECT/'metadata/mp3_quality.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
