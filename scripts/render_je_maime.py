#!/usr/bin/env python3
"""Rendu continu frame-accurate : UN flux MJPEG, Ken Burns, lettres et badge.

Aucun clip intermédiaire ni concaténation. Toute frame i représente t=i/30.
Usage : .venv/bin/python scripts/render_je_maime.py [--proofs] [--benchmark 60]
"""
from __future__ import annotations
import argparse
import bisect
import io
import math
import subprocess
import time
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

cv2.setNumThreads(1)

from je_maime_common import *
from maquette_je_maime import make_badge


class Renderer:
    def __init__(self, plan_path=PROJECT / 'montage_v1.json'):
        self.plan = load(plan_path)
        assert (self.plan['width'], self.plan['height'], self.plan['fps']) == (1080, 1920, 30)
        assert self.plan['text_advance_seconds'] == 0
        self.segments = self.plan['segments']
        self.starts = [s['first_frame'] for s in self.segments]
        self.font = font(58)
        self.badge = make_badge()
        self.backgrounds = {}
        self.glyphs = {}
        self.alpha_glyphs = {}
        self.layouts = {}
        self.prepare_backgrounds()
        for segment in self.segments:
            if segment['kind'] == 'lyric':
                self.layouts[segment['slot']] = self.layout(segment['display_lines'])
        self.intro_title = self.title_sprite(self.plan['title'], 106)
        self.intro_subtitle = self.simple_sprite(self.plan['artist'] + ' · ' + self.plan['album'], 34, '#fff0d5')
        self.intro_label = self.simple_sprite('Daïsky Prod / TechStein', 25, '#b9d9db')
        self.card_title = self.title_sprite(self.plan['title'], 86)
        self.card_panel = self.make_endcard_panel()

    def prepare_backgrounds(self):
        directory = WORK / 'fonds_portrait'
        directory.mkdir(parents=True, exist_ok=True)
        for key, spec in self.plan['backgrounds'].items():
            slot = int(key)
            cached = directory / f'f{slot:02d}.jpg'
            stamp = directory / f'f{slot:02d}.json'
            signature = {'source_sha256':spec['sha256'], 'canvas':[1188,2112], 'jpeg_quality':92, 'version':1}
            if not cached.is_file() or not stamp.is_file() or load(stamp) != signature:
                original = resolve_asset(spec['path'], spec['sha256'])
                with Image.open(original) as im:
                    canvas = ImageOps.fit(im.convert('RGB'), (1188,2112), Image.Resampling.LANCZOS)
                canvas.save(cached, quality=92, subsampling=0)
                dump(stamp, signature)
            with Image.open(cached) as im:
                self.backgrounds[slot] = im.convert('RGB')
        self.card_background = ImageEnhance.Brightness(self.backgrounds[0].filter(ImageFilter.GaussianBlur(5))).enhance(.34)
        self.backgrounds = {slot: np.asarray(image) for slot, image in self.backgrounds.items()}
        self.card_background = np.asarray(self.card_background)

    def glyph(self, char):
        if char in self.glyphs:
            return self.glyphs[char]
        bbox = self.font.getbbox(char, anchor='ls', stroke_width=2)
        pad = 16
        size = (max(1,bbox[2]-bbox[0])+2*pad, max(1,bbox[3]-bbox[1])+2*pad)
        position = (pad-bbox[0], pad-bbox[1])
        glow = Image.new('RGBA', size)
        ImageDraw.Draw(glow).text(position, char, font=self.font, anchor='ls', fill=(255,181,81,95), stroke_width=3)
        image = glow.filter(ImageFilter.GaussianBlur(6))
        ImageDraw.Draw(image).text(position, char, font=self.font, anchor='ls', fill=(255,247,230,255), stroke_width=2, stroke_fill=(13,14,15,235))
        result = (image, bbox[0]-pad, bbox[1]-pad)
        self.glyphs[char] = result
        return result

    def layout(self, lines):
        result = []
        for line_index, line in enumerate(lines):
            width = self.font.getlength(line)
            assert width <= 920
            x0 = (WIDTH-width)/2
            top = HEIGHT-300 + line_index*80
            baseline = top-self.font.getbbox(line, anchor='ls')[1]
            for j, char in enumerate(line):
                if char.isspace():
                    continue
                sprite, dx, dy = self.glyph(char)
                x = x0 + self.font.getlength(line[:j+1]) - self.font.getlength(char)
                result.append((char, sprite, x+dx, baseline+dy))
        return result

    def alpha_sprite(self, char, sprite, level):
        if level >= 16:
            return sprite
        key = (char, level)
        if key not in self.alpha_glyphs:
            result = sprite.copy()
            result.putalpha(sprite.getchannel('A').point(lambda v: round(v*level/16)))
            self.alpha_glyphs[key] = result
        return self.alpha_glyphs[key]

    @staticmethod
    def ease(value):
        value = max(0.0, min(1.0, value))
        return value*value*(3-2*value)

    def draw_lyric(self, image, segment, t):
        layout = self.layouts[segment['slot']]
        duration = (segment['end_centiseconds']-segment['start_centiseconds'])/100
        age = t-segment['start_centiseconds']/100
        enter = min(.9, duration*.25)
        rise = min(.16, enter*.4)
        exit_span = min(.45, duration*.15)
        fall = min(.16, exit_span*.6)
        count = max(1,len(layout)-1)
        for index, (char, sprite, x, y) in enumerate(layout):
            phase = index/count
            entry_start = phase*max(0, enter-rise)
            if age+1e-8 < entry_start:
                continue
            # Le premier caractère est déjà visible à la première frame du vers.
            entering = self.ease((age-entry_start+1/FPS)/max(.001,rise))
            exit_start = duration-exit_span+(1-phase)*max(0,exit_span-fall)
            leaving = self.ease((age-exit_start)/max(.001,fall))
            opacity = entering*(1-leaving)
            level = round(opacity*16)
            if level <= 0:
                continue
            wave = 6*math.sin(2*math.pi*.9*t+index*.42)
            vertical = wave+24*(1-entering)-18*leaving
            glyph = self.alpha_sprite(char, sprite, level)
            image.paste(glyph, (round(x),round(y+vertical)), glyph)

    @staticmethod
    def simple_sprite(text, size, color, bold=False):
        face = font(size,bold=bold)
        bbox = face.getbbox(text,stroke_width=1)
        image = Image.new('RGBA',(bbox[2]-bbox[0]+20,bbox[3]-bbox[1]+20))
        ImageDraw.Draw(image).text((10-bbox[0],10-bbox[1]),text,font=face,fill=color,stroke_width=1,stroke_fill='#10191d')
        return image

    @staticmethod
    def title_sprite(text,size):
        face = font(size,cursive=True)
        while face.getlength(text)>990:
            size-=2
            face=font(size,cursive=True)
        bbox=face.getbbox(text,stroke_width=1)
        dimensions=(bbox[2]-bbox[0]+48,bbox[3]-bbox[1]+48)
        position=(24-bbox[0],24-bbox[1])
        glow=Image.new('RGBA',dimensions)
        ImageDraw.Draw(glow).text(position,text,font=face,fill=(255,189,94,135),stroke_width=2)
        image=glow.filter(ImageFilter.GaussianBlur(8))
        ImageDraw.Draw(image).text(position,text,font=face,fill='#ffefd0',stroke_width=1,stroke_fill=(65,41,23,170))
        return image

    @staticmethod
    def paste_center(image,sprite,y):
        image.paste(sprite,(round((WIDTH-sprite.width)/2),round(y)),sprite)

    def make_endcard_panel(self):
        panel=Image.new('RGBA',(940,1090))
        draw=ImageDraw.Draw(panel)
        draw.rounded_rectangle((0,0,939,1089),radius=34,fill=(6,15,21,204),outline=(61,161,166,200),width=2)
        def line(y,text,size=30,color='#f3ecd9',bold=False):
            face=font(size,bold=bold)
            assert face.getlength(text)<870
            draw.text((470,y),text,font=face,anchor='mt',fill=color)
        # Le titre est ajouté séparément, avec une oscillation légère et continue.
        line(190,self.plan['artist'],44,bold=True)
        line(255,self.plan['album']+' · '+self.plan['genre']+' · '+self.plan['year'],28,color='#c4d6d5')
        line(326,'Daïsky Prod / TechStein',34,bold=True)
        line(395,'@daiskypro',32,color='#86d9e1')
        draw.line((96,459,844,459),fill=(229,177,103,220),width=2)
        line(500,'CONTACTS',23,color='#efc890',bold=True)
        line(548,'229 01 61 16 24 08',31)
        line(598,'229 01 49 11 49 51',31)
        line(681,'daiskypro@proton.me',30,color='#c7e7e6')
        line(733,'daiskyproduction@gmail.com',28)
        line(781,'techsteinsecureway@gmail.com',28)
        draw.line((188,857,752,857),fill=(62,137,144,180),width=1)
        line(904,'Wolof TechStein beat wê !',31,color='#ffe0a7')
        return panel

    def frame(self,index):
        if not 0 <= index < self.plan['total_frames']:
            raise IndexError(index)
        segment=self.segments[bisect.bisect_right(self.starts,index)-1]
        t=index/FPS
        duration=(segment['end_centiseconds']-segment['start_centiseconds'])/100
        u=max(0,min(1,(t-segment['start_centiseconds']/100)/duration))
        z=1.02+.06*(u if segment['slot']%2==0 else 1-u)
        background=self.card_background if segment['kind']=='endcard' else self.backgrounds[segment['asset_slot']]
        ch,cw=background.shape[:2]
        w,h=WIDTH/z,HEIGHT/z
        phase=segment['slot']*.61
        cx=cw/2+math.sin(t*.19+phase)*(cw-w)*.18
        cy=ch/2+math.cos(t*.13+phase)*(ch-h)*.15
        matrix=np.array([[1/z,0,cx-w/2],[0,1/z,cy-h/2]],dtype=np.float64)
        warped=cv2.warpAffine(background,matrix,(WIDTH,HEIGHT),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)
        image=Image.fromarray(warped)
        if segment['kind']=='intro':
            self.paste_center(image,self.intro_title,1490+4*math.sin(2*math.pi*.9*t))
            self.paste_center(image,self.intro_subtitle,1668)
            self.paste_center(image,self.intro_label,1740)
        elif segment['kind']=='endcard':
            image.paste(self.card_panel,(70,434),self.card_panel)
            self.paste_center(image,self.card_title,478+4*math.sin(2*math.pi*.9*t))
        else:
            if segment['slot']==49:
                image=ImageEnhance.Brightness(image).enhance(1-.35*u)
            self.draw_lyric(image,segment,t)
        image.paste(self.badge,(36,36),self.badge)  # TOUJOURS EN DERNIER.
        return image


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark',type=int,default=0)
    parser.add_argument('--start-frame',type=int,default=2260)
    parser.add_argument('--proofs',action='store_true')
    args=parser.parse_args()
    assert_sources_unchanged()
    start=time.monotonic()
    renderer=Renderer()
    plan=renderer.plan
    print(f"Fonds prêts en {time.monotonic()-start:.1f}s ; {plan['total_frames']} frames à rendre.",flush=True)
    if args.proofs:
        directory=WORK/'proofs'
        directory.mkdir(parents=True,exist_ok=True)
        for index in (90,198,1118,2265,3930,4500,5700):
            renderer.frame(index).save(directory/f'frame_{index:05d}.jpg',quality=92)
        print('Maquettes de contrôle : '+str(directory),flush=True)
        return
    if args.benchmark:
        start=time.monotonic()
        for i in range(args.benchmark):
            image=renderer.frame(args.start_frame+i)
            buffer=io.BytesIO()
            image.save(buffer,format='JPEG',quality=92,subsampling=0)
        elapsed=time.monotonic()-start
        print(f'Benchmark rendu + JPEG : {args.benchmark/elapsed:.2f} fps ({elapsed:.2f}s).',flush=True)
        return
    pcm=WORK/'master_48k_f32.wav'
    if not pcm.is_file():
        raise FileNotFoundError('Lancer master_je_maime.py avant le rendu')
    output=ROOT/plan['video_output']
    output.parent.mkdir(parents=True,exist_ok=True)
    total=plan['total_duration_seconds']
    fade_start=plan['fade_out_first_frame']/FPS
    e=plan['encoding']
    filters=(f'[0:v]fade=t=out:st={fade_start:.9f}:d=3[v];'
             f'[1:a]apad=whole_dur={total:.9f},afade=t=out:st={fade_start:.9f}:d=3[a]')
    cmd=[FFMPEG,'-hide_banner','-nostdin','-y','-f','image2pipe','-framerate','30','-vcodec','mjpeg','-i','-',
         '-i',str(pcm),'-filter_complex',filters,'-map','[v]','-map','[a]',
         '-c:v','libx264','-preset',e['preset'],'-crf',str(e['crf']),'-pix_fmt','yuv420p',
         '-maxrate',e['maxrate'],'-bufsize',e['bufsize'],'-threads','2',
         '-c:a','aac','-b:a',e['aac_bitrate'],'-ar','48000','-ac','2',
         '-frames:v',str(plan['total_frames']),'-t',f'{total:.9f}',
         '-movflags','+faststart','-metadata','title='+plan['title'],
         '-metadata','artist='+plan['artist'],str(output)]
    dump(WORK/'render_command.json',{'command':cmd,'total_frames':plan['total_frames']})
    start=time.monotonic()
    with (WORK/'render_ffmpeg.log').open('wb') as log:
        process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
        try:
            for index in range(plan['total_frames']):
                image=renderer.frame(index)
                image.save(process.stdin,format='JPEG',quality=92,subsampling=0)
                if index%300==0 or index==plan['total_frames']-1:
                    elapsed=time.monotonic()-start
                    print(f'Frame {index+1}/{plan["total_frames"]} — t={index/FPS:.2f}s — {(index+1)/max(.001,elapsed):.1f} fps',flush=True)
            process.stdin.close()
            result=process.wait()
        except BaseException:
            process.kill()
            process.wait()
            raise
    if result:
        raise RuntimeError('FFmpeg a échoué ; consulter work/out/je_maime_tellement/render_ffmpeg.log')
    elapsed=time.monotonic()-start
    dump(PROJECT/'rendu_v1.json',{'output':plan['video_output'],'frames_sent':plan['total_frames'],'elapsed_seconds':elapsed,'file_bytes':output.stat().st_size,'sha256':sha256(output),'continuous_stream':True,'frame_time_formula':'t=i/30','text_advance_seconds':0.0,'encoder':e})
    print(f'RENDU TERMINÉ : {output.name}, {output.stat().st_size/1e6:.1f} Mo en {elapsed:.1f}s.',flush=True)


if __name__=='__main__':
    main()
