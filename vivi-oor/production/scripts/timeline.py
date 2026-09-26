#!/usr/bin/env python3
"""LRC-anchored word animation, ASS overlays and a single PCM audio timeline.

Line onsets are the artist's supplied times. Word onsets are estimates (not ASR).
"""
from pathlib import Path
import json, math, re, unicodedata, warnings
from collections import defaultdict

import numpy as np
from PIL import ImageFont
from scipy.io import wavfile

ROOT=Path(__file__).resolve().parents[3]
PROJECT=ROOT/'vivi-oor/production';WORK=ROOT/'work/vivi-production';OUT=PROJECT/'livrables'
FONTS=PROJECT/'assets/fonts';FPS=30;HOOK=6.0;HOOK_START=152.43;LEAD=.03
CX=480;ACTIVE_Y=1228;TRAIL_SIZE=43;TRAIL_Y=[1400,1460];MAX_WIDTH=800


def ass_time(t):
    cs=max(0,round(t*100));return f'{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}'


def srt_time(t):
    ms=max(0,round(t*1000));return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'


def weight(word):
    special={'wanyiyi':3,'wadjaya':3,'techstein':2,'djalé':2,'yiwan':2,'noumi':2,'vivi':2,'oor':1,'gbètché':2,'kissi':2}
    key=word.lower().strip('.,!?…')
    if key in special:return float(special[key])
    if key in {'le','la','de','du','je','te','me','ne','se','ce','tu','et','est','à','en'}:return .62
    total=0
    for part in re.split("[-’']",key):
        if len(part)>3 and part.endswith('e'):part=part[:-1]
        groups=re.findall('[aeiouyàâäéèêëîïôöùûüœ]+',part)
        total+=max(1,len(groups))
    return max(.65,float(total))


def scene_for(text):
    s=text.lower()
    if 'dansons' in s:return 9
    if 'trésor' in s or 'plus fort' in s:return 7
    if 'festin' in s:return 8
    if 'étincelle' in s:return 3
    if 'miel' in s or 'kissi noumi, embrasse' in s:return 2
    if 'ouvre mon cœur' in s or 'cœur' in s:return 6
    if 'reste avec moi' in s or 'attends' in s or 'supplie' in s:return 4
    if 'chaque instant' in s or 'savoure la vie' in s or 'ma vie me plaît' in s:return 5
    if 'nuit' in s:return 9
    if 'wolof' in s:return 7
    return 1


def trail_layout(tokens):
    f=ImageFont.truetype(str(FONTS/'DejaVuSans-Bold.ttf'),TRAIL_SIZE)
    widths=[float(f.getlength(w)) for w in tokens];space=float(f.getlength(' '));rows=[[]]
    for i,width in enumerate(widths):
        used=sum(widths[j] for j in rows[-1])+space*max(0,len(rows[-1])-1)
        if rows[-1] and used+space+width>MAX_WIDTH:rows.append([])
        rows[-1].append(i)
    assert len(rows)<=2,(tokens,rows)
    positions={}
    for row,indices in enumerate(rows):
        total=sum(widths[j] for j in indices)+space*(len(indices)-1);x=CX-total/2
        for j in indices:
            positions[j]=(x+widths[j]/2,TRAIL_Y[row],widths[j]);x+=widths[j]+space
    return positions


def build_lines(duration):
    text=(ROOT/'Vivi O O R.txt').read_text(encoding='utf-8-sig').replace('\u200e','')
    lines=[]
    for row in text.splitlines():
        m=re.match(r'\[(\d+):(\d+(?:\.\d+)?)\](.*)',row)
        if m:lines.append(dict(start=int(m[1])*60+float(m[2]),text=m[3].strip()))
    assert len(lines)==44
    assert all(b['start']-a['start']>=1.2 for a,b in zip(lines,lines[1:]))
    onsets=json.loads((WORK/'onsets.json').read_text())['onsets']
    pts=np.array([p['t'] for p in onsets]);strengths=np.array([p['strength'] for p in onsets])
    templates={}
    for idx,line in enumerate(lines):
        start=line['start'];tokens=line['text'].split();next_start=lines[idx+1]['start'] if idx+1<len(lines) else duration
        gap=next_start-start
        # Long rests/outro are not held under a single lyric for 10–30 seconds.
        end=next_start-.10
        if gap>7.8:end=min(end,start+min(5.5,1.2+.66*len(tokens)))
        if idx==len(lines)-1:end=min(end,start+4.4)
        end=max(end,start+1.2)
        vocal_span=max(.45,end-start-.35)
        ws=np.array([weight(w) for w in tokens]);fractions=np.concatenate(([0],np.cumsum(ws)[:-1]/sum(ws)))
        if line['text'] in templates:
            fractions=np.array(templates[line['text']])
        else:
            # Bounded musical-onset attraction, never reported as a vocal aligner.
            previous=start
            values=[0.0]
            for j in range(1,len(tokens)):
                ideal=start+float(fractions[j])*vocal_span
                selected=np.where((pts>=ideal-.10)&(pts<=ideal+.10)&(pts>previous+.115))[0]
                chosen=ideal
                if len(selected):
                    best=min(selected,key=lambda k:abs(pts[k]-ideal)-min(strengths[k],3)*.009)
                    chosen=float(pts[best])
                chosen=max(previous+.115,min(chosen,start+vocal_span-(len(tokens)-1-j)*.115))
                values.append((chosen-start)/vocal_span);previous=chosen
            fractions=np.array(values);templates[line['text']]=values
        starts=start+fractions*vocal_span
        assert np.all(np.diff(starts)>.05)
        layout=trail_layout(tokens)
        line.update(end=round(end,4),scene=scene_for(line['text']),tokens=tokens,
                    words=[dict(text=w,start=round(float(starts[j]),4),end=round(float(starts[j+1] if j+1<len(starts) else end-.22),4),
                                trail_x=round(layout[j][0],3),trail_y=layout[j][1],trail_width=round(layout[j][2],3)) for j,w in enumerate(tokens)])
    return lines


def make_ass(events,total,endcard_start):
    headers='''[Script Info]
Title: Vivi OOR — mot grand puis petit
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 1
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Active,DejaVu Sans,86,&H00DFF1FF,&H00DFF1FF,&H00201623,&H90000000,-1,0,0,0,100,100,0,0,1,2.5,0,5,56,180,0,1
Style: Trail,DejaVu Sans,43,&H10EAF1F7,&H10EAF1F7,&H00201623,&H90000000,-1,0,0,0,100,100,0,0,1,1.5,0,5,56,180,0,1
Style: Badge,DejaVu Sans,34,&H50D7E7F7,&H50D7E7F7,&H80302030,&HC0000000,-1,0,0,0,100,100,0,0,1,1,0,8,80,80,150,1
Style: Title,Great Vibes,142,&H00D9EEFF,&H00D9EEFF,&H40301B24,&H90000000,0,0,0,0,100,100,0,0,1,1,1,5,85,85,0,1
Style: Contact,DejaVu Sans,35,&H00E4ECF4,&H00E4ECF4,&H00201623,&H90000000,0,0,0,0,100,100,0,0,1,1.4,0,5,90,90,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    output=[headers];bounds=[]
    def add(layer,start,end,style,text):
        if end-start<.02:return
        output.append(f'Dialogue: {layer},{ass_time(start)},{ass_time(end)},{style},,0,0,0,,{text}\n')
    for event in events:
        st,en=event['start'],event['end']
        add(8,st,en,'Badge',r'{\an8\pos(540,153)\fad(400,400)}DSKY✓')
        for i,word in enumerate(event['words']):
            text=word['text'].replace('{','').replace('}','')
            start=max(st,word['start']);stop=min(word['end'],en-.08)
            if stop<=start:continue
            f=ImageFont.truetype(str(FONTS/'DejaVuSans-Bold.ttf'),86)
            fs=min(86,math.floor(770/(max(f.getlength(text),1)*1.5)*86))
            fs=max(48,fs)
            x,y=word['trail_x'],word['trail_y']
            max_width=ImageFont.truetype(str(FONTS/'DejaVuSans-Bold.ttf'),fs).getlength(text)*1.5+32
            assert CX-max_width/2>=50 and CX+max_width/2<=910,(text,max_width)
            assert x-word['trail_width']/2>=50 and x+word['trail_width']/2<=910
            duration=stop-start
            attack=min(150,max(70,round(duration*420)))
            fadein=min(90,max(45,round(duration*220)))
            anim=f'\\an5\\pos({CX},{ACTIVE_Y})\\fs{fs}\\fscx145\\fscy145\\t(0,{attack},\\fscx120\\fscy120)\\fad({fadein},50)'
            add(3,start,stop,'Active','{'+anim+r'\1a&HFF&\3c&H649BE4&\3a&H9A&\bord7\blur5}'+text)
            add(5,start,stop,'Active','{'+anim+r'\blur0.35}'+text)
            # The previous word settles into its preallocated place. Older words
            # never jump sideways when the following word is introduced.
            transition=min(.14,max(.07,duration*.28))
            land=stop+transition
            if land<en-.04:
                ratio=TRAIL_SIZE/fs*100
                flight=(f'\\an5\\move({CX},{ACTIVE_Y},{x:.2f},{y:.2f},0,{round(transition*1000)})\\fs{fs}'
                        f'\\fscx120\\fscy120\\t(0,{round(transition*1000)},\\fscx{ratio:.2f}\\fscy{ratio:.2f}\\bord1.5)\\blur0.35')
                add(4,stop,land,'Active','{'+flight+'}'+text)
                add(4,land,en,'Trail',f'{{\\an5\\pos({x:.2f},{y:.2f})\\fad(0,160)}}'+text)
            bounds.append(dict(word=text,active=[round(CX-max_width/2,1),1100,round(CX+max_width/2,1),1345],trail=[x-word['trail_width']/2,y-34,x+word['trail_width']/2,y+34]))
    add(9,.12,5.86,'Title',r'{\an5\pos(540,288)\fad(220,250)}Vivi OOR')
    add(9,6.15,10.65,'Title',r'{\an5\pos(540,288)\fad(250,350)}Vivi OOR')
    # Short reprise of the title during the instrumental outro; never over a face.
    add(9,190,197,'Title',r'{\an5\pos(540,278)\fad(500,500)}Vivi OOR')
    add(9,endcard_start,total,'Title',r'{\an5\pos(540,535)\fs170\fad(500,450)}Vivi OOR')
    add(9,endcard_start,total,'Badge',r'{\an8\pos(540,153)\fad(400,400)}DSKY✓')
    add(9,endcard_start+.25,total,'Contact',r'{\an5\pos(540,1030)\fs30\fad(400,450)}WhatsApp')
    add(9,endcard_start+.35,total,'Contact',r'{\an5\pos(540,1100)\fad(400,450)}+229 01 61 16 24 08')
    add(9,endcard_start+.45,total,'Contact',r'{\an5\pos(540,1170)\fad(400,450)}+229 01 49 11 49 51')
    add(9,endcard_start+.55,total,'Contact',r'{\an5\pos(540,1290)\fad(400,450)}daiskyproduction@gmail.com')
    (OUT/'VIVI_OOR_lyrics_mot_a_mot.ass').write_text(''.join(output),encoding='utf-8-sig')
    (PROJECT/'metadata/text_bounds.json').write_text(json.dumps(bounds,ensure_ascii=False,indent=2)+'\n')


def main():
    analysis=json.loads((PROJECT/'metadata/audio_analysis.json').read_text());duration=analysis['decoded_duration']
    lines=build_lines(duration)
    events=[]
    # A full title-bearing refrain line fits inside the six-second cold open.
    line=next(x for x in lines if abs(x['start']-152.68)<.001)
    def shifted(line,offset,limit=None):
        e={k:v for k,v in line.items() if k not in ['words','start','end']}
        e['start']=max(0,line['start']+offset-LEAD);e['end']=line['end']+offset-LEAD
        if limit:e['end']=min(e['end'],limit)
        e['words']=[{**w,'start':w['start']+offset-LEAD,'end':min(w['end']+offset-LEAD,e['end']-.12)} for w in line['words']]
        return e
    events.append(shifted(line,-HOOK_START,5.98))
    events.extend(shifted(line,HOOK) for line in lines)
    total=HOOK+duration+5;endcard_start=HOOK+duration-3
    # Background choices share the same absolute frame clock as the words.
    changes=[(0,3),(HOOK,1)]
    changes.extend((max(HOOK,line['start']+HOOK),line['scene']) for line in lines)
    changes.extend([(186,9),(192,5),(199,10),(endcard_start,0)])
    changes=sorted(changes)
    compact=[]
    for t,scene in changes:
        if compact and abs(t-compact[-1][0])<.001:compact[-1]=(t,scene)
        elif not compact or scene!=compact[-1][1]:compact.append((t,scene))
    segments=[dict(start=t,end=compact[i+1][0] if i+1<len(compact) else total,scene=scene) for i,(t,scene) in enumerate(compact)]
    plan=dict(title='Vivi OOR',artist='Daïsky',fps=FPS,width=1080,height=1920,source_duration=duration,
              hook_duration=HOOK,hook_source_start=HOOK_START,hook_source_end=HOOK_START+HOOK,
              total_duration=total,frames=math.ceil(total*FPS),endcard_start=endcard_start,lead_seconds=LEAD,
              line_timing_method='Artist supplied LRC timestamps, no unverified line-time correction',
              word_timing_method='Estimated from syllables, mirrored repeated lines and musical onset attraction ±0.10 s. Not forced-aligned vocals.',
              lyric_mode='Active word 1.45→1.20 scale, settles into fixed small-word trail; soft entrance, discreet glow; face-free safe zone.',
              events=events,segments=segments)
    (PROJECT/'metadata/timeline.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    header=f'[ti:Vivi OOR]\n[ar:Daïsky]\n[length:03:24.96]\n'
    lrc=header+'\n'.join(f"[{int(l['start']//60):02d}:{l['start']%60:05.2f}]{l['text']}" for l in lines)+'\n'
    (OUT/'Vivi_OOR.lrc').write_text(lrc)
    (OUT/'Vivi_OOR_paroles.txt').write_text('\n'.join(l['text'] for l in lines)+'\n')
    for name,seq in [('Vivi_OOR_chanson.srt',lines),('Vivi_OOR_clip.srt',events)]:
        (OUT/name).write_text('\n'.join(f"{i+1}\n{srt_time(e['start'])} --> {srt_time(e['end'])}\n{e['text']}\n" for i,e in enumerate(seq)),encoding='utf-8')
    make_ass(events,total,endcard_start)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore');sr,song=wavfile.read(WORK/'processed48.wav')
    assert sr==48000 and len(song)==round(duration*sr)
    hook=song[round(HOOK_START*sr):round((HOOK_START+HOOK)*sr)].copy()
    edge=round(.035*sr);hook[:edge]*=np.linspace(0,1,edge)[:,None];hook[-edge:]*=np.linspace(1,0,edge)[:,None]
    song=song.copy();fade=round(3*sr);song[-fade:]*=np.linspace(1,0,fade)[:,None]
    track=np.concatenate([hook,song,np.zeros((5*sr,2),np.float32)]).astype(np.float32)
    assert len(track)==round(total*sr)
    wavfile.write(WORK/'video_audio48.wav',sr,track)
    print(f'Timeline: {len(lines)} original lines, {len(events)} video lyric events, {len(segments)} image segments, {total:.2f}s / {plan["frames"]} frames.',flush=True)


if __name__=='__main__':main()
