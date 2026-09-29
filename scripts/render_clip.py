#!/usr/bin/env python3
"""Rendu mono-horloge du clip entier, portrait OU paysage, sans concat vidéo.

Les mêmes cinq scènes approuvées sont réutilisées ; badge et drapeau sont
composés après mouvement. Les calques de mots sont mis en cache avant la vague.
"""
from __future__ import annotations
import argparse
from collections import OrderedDict
import io
import json
import math
from pathlib import Path
import subprocess
import time

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from render_ancre import ROOT, balanced_lines, badge_alpha, badge_sprite, draw_flag
from design_assets import title_sprite, ui_sprite, centered, soft_scrim

cv2.setNumThreads(1)
FONT = ROOT/'assets/fonts/BarlowCondensed-Bold.ttf'
WORK = ROOT/'work/concentre_sur_le_chemin'
STATE = ROOT/'productions/concentre_sur_le_chemin'


class LyricLayout:
    def __init__(self, text, fmt):
        self.text = text
        self.tokens = text.split()
        self.width = 720 if fmt=='portrait' else 1640
        max_width = self.width-28
        max_lines = 4 if fmt=='portrait' else 2
        sizes = range(112, 87, -4) if fmt=='portrait' else range(128, 99, -4)
        for size in sizes:
            font = ImageFont.truetype(str(FONT), size)
            try:
                lines = balanced_lines(self.tokens, font, max_width)
            except ValueError:
                continue
            if len(lines) <= max_lines:
                break
        else:
            raise ValueError(f'Vers entier impossible dans la zone sûre : {text}')
        self.font_size, self.lines = size, lines
        top = min(font.getbbox(w)[1] for w in self.tokens)
        bottom = max(font.getbbox(w)[3] for w in self.tokens)
        pitch = round(size*1.09)
        self.pad = 16
        self.height = bottom-top+(len(lines)-1)*pitch+2*self.pad
        w, h = (1080, 1920) if fmt=='portrait' else (1920, 1080)
        self.x, self.y = (w-self.width)//2, round((h-self.height)/2)
        self.bounds = (self.x, self.y, self.x+self.width, self.y+self.height)
        self.words = []
        for line_index, line in enumerate(lines):
            space = font.getlength(' ')
            width = sum(font.getlength(word) for word in line)+space*(len(line)-1)
            x = (self.width-width)/2
            for word in line:
                length = font.getlength(word)
                bbox = font.getbbox(word)
                mask = Image.new('L', (math.ceil(max(length, bbox[2]))+2*self.pad, bottom-top+2*self.pad))
                ImageDraw.Draw(mask).text((self.pad, self.pad-top), word, font=font, fill=255)
                self.words.append((round(x)-self.pad, line_index*pitch, mask, word))
                x += length+space
        assert [word[3] for word in self.words] == self.tokens
        self.xx, self.yy = np.meshgrid(np.arange(self.width, dtype=np.float32),
                                      np.arange(self.height, dtype=np.float32))
        self.phase = np.arange(self.width, dtype=np.float32)*np.float32(2*np.pi/320)
        self.layers = OrderedDict()

    def flat(self, index):
        index = min(len(self.words)-1, max(0, index))
        if index in self.layers:
            self.layers.move_to_end(index)
            return self.layers[index]
        past = Image.new('L', (self.width, self.height))
        active = Image.new('L', past.size)
        whole = Image.new('L', past.size)
        for i, (x, y, mask, _) in enumerate(self.words):
            if i > index: break
            (past if i<index else active).paste(mask, (x, y))
            whole.paste(mask, (x, y))
        stroke = whole.filter(ImageFilter.MaxFilter(7))
        layer = Image.new('RGBA', whole.size)
        shade = Image.new('RGBA', whole.size, (3, 7, 13, 0))
        shade.putalpha(stroke.filter(ImageFilter.GaussianBlur(3)).point(lambda a: round(a*.9)))
        layer.alpha_composite(shade)
        ink = Image.new('RGBA', whole.size, (3, 7, 13, 0)); ink.putalpha(stroke)
        layer.alpha_composite(ink)
        glow = Image.new('RGBA', whole.size, (255, 197, 100, 0))
        glow.putalpha(active.filter(ImageFilter.GaussianBlur(4)).point(lambda a: round(a*.36)))
        layer.alpha_composite(glow)
        old = Image.new('RGBA', whole.size, (223, 218, 208, 0)); old.putalpha(past.point(lambda a: round(a*.87)))
        layer.alpha_composite(old)
        gold = Image.new('RGBA', whole.size, (255, 224, 164, 0)); gold.putalpha(active)
        layer.alpha_composite(gold)
        self.layers[index] = np.array(layer)
        # Only a few word states per unique line need reside in RAM at a time.
        if len(self.layers)>3:
            self.layers.popitem(last=False)
        return self.layers[index]

    def layer(self, index, t, opacity=1):
        pixels = self.flat(index)
        shift = 4.5*np.sin(2*np.pi*.9*t+self.phase)
        warped = cv2.remap(pixels, self.xx, self.yy-shift[None, :],
                           interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        if opacity < 1:
            warped[:, :, 3] = np.rint(warped[:, :, 3]*opacity).astype(np.uint8)
        return Image.fromarray(warped)


class ClipRenderer:
    def __init__(self, fmt):
        if fmt not in ('portrait','landscape'): raise ValueError(fmt)
        self.fmt = fmt
        self.w, self.h = (1080, 1920) if fmt=='portrait' else (1920, 1080)
        self.timeline = json.loads((STATE/'timings_render.json').read_text())
        self.config = json.loads((STATE/'production.json').read_text())
        if not self.config['approvals'].get('image_series'):
            raise RuntimeError('La série doit être approuvée avant un rendu complet.')
        self.verses = self.timeline['verses']
        self.hook = self.timeline['hook_duration']
        self.total = self.timeline['total']
        self.frames = self.timeline['frames']
        self.fps = self.timeline['fps']
        self.layouts = {v['text']: LyricLayout(v['text'], fmt) for v in self.verses}
        self.bases = {}
        manifest = json.loads((STATE/'backgrounds_manifest.json').read_text())
        for entry in manifest:
            if entry['format'] != fmt: continue
            if not entry['artist_approved']: raise RuntimeError('Fond non approuvé.')
            image = Image.open(ROOT/entry['background_cache']).convert('RGB')
            if fmt=='portrait' and entry['slot']=='s04':
                # Reserve the approved upper badge zone above the head.
                shifted = Image.new('RGB', image.size)
                shifted.paste(image, (0, 55))
                ceiling = image.crop((0,0,self.w,8)).resize((self.w,55),Image.Resampling.BICUBIC)
                shifted.paste(ceiling,(0,0)); image = shifted
            canvas = image.resize((round(self.w*1.1),round(self.h*1.1)),Image.Resampling.LANCZOS)
            self.bases[entry['slot']] = np.array(canvas)
        rows = np.arange(self.h, dtype=float)
        sigma, protected = (230, 725) if fmt=='portrait' else (130, 355)
        alpha = 95*np.exp(-.5*((rows-self.h/2)/sigma)**2)*np.clip((rows-protected)/65,0,1)
        pixels = np.zeros((self.h,self.w,4),dtype=np.uint8)
        pixels[:,:,3] = alpha[:,None].astype(np.uint8)
        self.scrim = Image.fromarray(pixels)
        self.title = title_sprite(880 if fmt=='portrait' else 1100,182 if fmt=='portrait' else 172)
        self.artist = ui_sprite('Daïsky',42 if fmt=='portrait' else 48,max_width=700)
        self.whatsapp = ui_sprite('WhatsApp',30,max_width=700,fill=(209,191,153,255))
        self.phone1 = ui_sprite('+229 01 61 16 24 08',39,max_width=700)
        self.phone2 = ui_sprite('+229 01 49 11 49 51',39,max_width=700)
        self.email = ui_sprite('daiskyproduction@gmail.com',38,max_width=710)
        self.badge = badge_sprite()

    def music_time(self,t):
        return self.timeline['hook_start']+t if t < self.hook else t-self.hook

    def verse_at(self,t):
        source = self.music_time(t)
        for v in self.verses:
            if t<self.hook and not (self.timeline['hook_start']<=v['start']<self.timeline['hook_end']):
                continue
            if v['start']-.03<=source<v['end']-.03:
                return v
        return None

    def motion(self,slot,t,age,duration):
        canvas = self.bases[slot]
        phase = min(1,max(0,age/max(1,duration)))
        max_zoom = 1.055
        if self.fmt=='landscape' and slot=='s03': max_zoom=1.035
        if self.fmt=='portrait' and slot=='s04': max_zoom=1.025
        low = 1.015 if slot=='s04' else 1.02
        if int(slot[-1])%2: phase=1-phase
        zoom = low+(max_zoom-low)*phase
        ch,cw=canvas.shape[:2]
        crop_w,crop_h=cw/zoom,ch/zoom
        mx,my=(cw-crop_w)/2,(ch-crop_h)/2
        strength=0 if self.fmt=='landscape' and slot=='s03' else .14
        dx=mx*(1+strength*math.sin(t*2*math.pi/13))
        dy=my*(1+.10*math.sin(t*2*math.pi/17))
        scale=self.w/crop_w
        matrix=np.array([[scale,0,-dx*scale],[0,self.h/crop_h,-dy*self.h/crop_h]],dtype=np.float32)
        return cv2.warpAffine(canvas,matrix,(self.w,self.h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)

    def background(self,t):
        if t<self.hook:
            return self.motion('s03',t,t,self.hook)
        source=t-self.hook
        sections=self.timeline['sections']
        index=max(i for i,s in enumerate(sections) if source>=s['start'])
        scene=sections[index]
        age=source-scene['start']
        current=self.motion(scene['slot'],t,age,scene['end']-scene['start'])
        if age<.4:
            previous=sections[index-1]['slot'] if index else 's03'
            if previous!=scene['slot']:
                old=self.motion(previous,t,1,1)
                factor=max(0,min(1,age/.4)); factor=factor*factor*(3-2*factor)
                current=cv2.addWeighted(old,1-factor,current,factor,0)
        return current

    def put_badge(self,image,alpha):
        if alpha<=0:return
        badge=self.badge.copy()
        badge.putalpha(badge.getchannel('A').point(lambda a: round(a*alpha)))
        image.alpha_composite(badge,((self.w-badge.width)//2,156 if self.fmt=='portrait' else 145))

    def frame(self,t):
        image=Image.fromarray(self.background(t)).convert('RGBA')
        source=self.music_time(t)
        verse=self.verse_at(t)
        if t>=self.timeline['endcard_start']:
            if self.fmt=='portrait':
                soft_scrim(image,1130,270,715,145)
                cx=self.w/2
                centered(image,self.title,cx,930)
                centered(image,self.whatsapp,cx,1150)
                centered(image,self.phone1,cx,1210)
                centered(image,self.phone2,cx,1270)
                centered(image,self.email,cx,1370)
            else:
                soft_scrim(image,620,210,365,130)
                cx=1220
                centered(image,self.title,cx,410)
                centered(image,self.whatsapp,cx,622)
                centered(image,self.phone1,cx,680)
                centered(image,self.phone2,cx,735)
                centered(image,self.email,cx,830)
            self.put_badge(image,badge_alpha(t,self.timeline['endcard_start'],self.total))
        elif t>=self.hook and source<4.31:
            image.alpha_composite(self.scrim)
            alpha=min(1,max(0,source/.3),max(0,(4.31-source)/.3))
            title=self.title.copy();title.putalpha(title.getchannel('A').point(lambda a:round(a*alpha)))
            artist=self.artist.copy();artist.putalpha(artist.getchannel('A').point(lambda a:round(a*alpha)))
            if self.fmt=='portrait':
                centered(image,title,540,1000);centered(image,artist,540,1264)
            else:
                centered(image,title,1220,500);centered(image,artist,1220,740)
            self.put_badge(image,badge_alpha(source,0,4.31))
        elif verse:
            image.alpha_composite(self.scrim)
            # Source timestamps and complete layout remain fixed throughout reveal.
            starts=[w['start']-.03 for w in verse['words']]
            index=max(0,min(len(starts)-1,int(np.searchsorted(starts,source,side='right'))-1))
            remaining=verse['end']-.03-source
            opacity=min(1,max(0,remaining/.15))
            layout=self.layouts[verse['text']]
            image.alpha_composite(layout.layer(index,t,opacity),(layout.x,layout.y))
            self.put_badge(image,badge_alpha(source,verse['start']-.03,verse['end']-.03))
        height=54 if self.fmt=='portrait' else 30
        draw_flag(image,(0,self.h-height,self.w,height))
        result=np.array(image.convert('RGB'))
        if t>self.total-3:
            fade=max(0,min(1,(self.total-t)/3))
            result=cv2.convertScaleAbs(result,alpha=fade)
        return result

    def layout_report(self):
        return [{'text':text,'font_size':layout.font_size,'bbox':list(layout.bounds),
                 'lines':[' '.join(line) for line in layout.lines], 'word_count':len(layout.words)}
                for text,layout in self.layouts.items()]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--format',choices=['portrait','landscape'],required=True)
    p.add_argument('--stills-only',action='store_true')
    p.add_argument('--limit-frames',type=int,default=0,help='Essai local, hors livrables finaux')
    args=p.parse_args()
    renderer=ClipRenderer(args.format)
    label='9x16' if args.format=='portrait' else '16x9_YT'
    destination=ROOT/f'livrables/Concentre_sur_le_chemin_{label}_v1.mp4'
    checks=WORK/f'checks_{args.format}'
    checks.mkdir(parents=True,exist_ok=True)
    samples=[0.7,3.1,renderer.hook+1.8,renderer.hook+26.9,renderer.hook+86.8,
             renderer.hook+144.3,renderer.hook+158.4,renderer.hook+184.8,218.6,220.5]
    for i,t in enumerate(samples):
        Image.fromarray(renderer.frame(t)).save(checks/f'sample_{i:02}_{t:.2f}.jpg',quality=94)
    (STATE/f'layout_{args.format}.json').write_text(json.dumps(renderer.layout_report(),ensure_ascii=False,indent=2)+'\n')
    if args.stills_only:return
    frame_count=renderer.frames if not args.limit_frames else min(args.limit_frames,renderer.frames)
    if args.limit_frames: destination=WORK/f'encoding_test_{label}.mp4'
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    command=[ffmpeg,'-hide_banner','-nostdin','-y','-thread_queue_size','64',
             '-f','image2pipe','-vcodec','mjpeg','-framerate',str(renderer.fps),'-i','pipe:0',
             '-i',str(WORK/'video_audio.wav'),'-map','0:v:0','-map','1:a:0',
             '-frames:v',str(frame_count),'-t',str(frame_count/renderer.fps),
             '-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709',
             '-c:v','libx264','-preset','fast','-tune','animation','-threads','2','-crf','21',
             '-maxrate','950k','-bufsize','1900k','-pix_fmt','yuv420p',
             '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',
             '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',
             '-metadata','title=Concentré sur le chemin — Daïsky',str(destination)]
    started=time.monotonic()
    log_path=WORK/f'render_{args.format}.log'
    with log_path.open('w') as log:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=log,stderr=log)
        try:
            for i in range(frame_count):
                rgb=renderer.frame(i/renderer.fps)
                bgr=cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
                ok,encoded=cv2.imencode('.jpg',bgr,[cv2.IMWRITE_JPEG_QUALITY,94,
                    cv2.IMWRITE_JPEG_SAMPLING_FACTOR,cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444])
                if not ok:raise RuntimeError('Encodage image intermédiaire impossible.')
                process.stdin.write(encoded.tobytes())
                if i%150==0:
                    elapsed=time.monotonic()-started
                    print(f'{args.format}: {i}/{frame_count} frames, {i/renderer.fps:.1f}s, {i/max(1,elapsed):.1f} fps de calcul',flush=True)
            process.stdin.close()
            code=process.wait(timeout=180)
        except BaseException:
            process.kill();process.wait();raise
    if code:raise RuntimeError(log_path.read_text()[-5000:])
    report={'file':str(destination.relative_to(ROOT)),'format':args.format,
            'frames':frame_count,'fps':renderer.fps,'duration':frame_count/renderer.fps,
            'render_seconds':round(time.monotonic()-started,2),'size_bytes':destination.stat().st_size,
            'codec':'H.264','crf':21,'vbv_maxrate_kbps':950,'audio':'AAC 192 kb/s 48 kHz stereo',
            'word_alignment':'estimated from artist LRC, not forced vocal alignment',
            'single_frame_clock':True,'new_ai_images':0}
    if not args.limit_frames:
        (STATE/f'render_{args.format}_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    main()
