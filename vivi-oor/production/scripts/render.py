#!/usr/bin/env python3
"""One continuous, frame-clocked MJPEG -> H.264 render, with ASS word motion.

No video concatenation and no face regeneration. Images are the approved V2 set.
"""
from pathlib import Path
import argparse,bisect,io,json,math,subprocess,time
import imageio_ffmpeg
import cv2
import numpy as np
cv2.setNumThreads(1)
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[3]
PROJECT=ROOT/'vivi-oor/production';WORK=ROOT/'work/vivi-production'
FF=imageio_ffmpeg.get_ffmpeg_exe();SIZE=(1080,1920)


def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)


class Renderer:
    def __init__(self):
        self.plan=json.loads((PROJECT/'metadata/timeline.json').read_text())
        self.segments=self.plan['segments'];self.segment_starts=[s['start'] for s in self.segments]
        self.events=self.plan['events'];self.event_starts=[e['start'] for e in self.events]
        images=json.loads((ROOT/'vivi-oor/v2/manifest.json').read_text())['scenes']
        self.images={x['slot']:Image.open(ROOT/'vivi-oor/v2'/x['output']).convert('RGB').resize((1188,2112),Image.Resampling.LANCZOS) for x in images}
        end=Image.open(ROOT/'vivi-oor/assets/backgrounds/07_tresor.jpg').convert('RGB')
        end=ImageOps.fit(end,(1188,2112),method=Image.Resampling.LANCZOS)
        end=Image.blend(end,Image.new('RGB',end.size,'#110b16'),.37)
        self.images[0]=end
        self.images={k:cv2.cvtColor(np.asarray(v),cv2.COLOR_RGB2BGR) for k,v in self.images.items()}
        yy=np.arange(560)[:,None]+1040;xx=np.arange(1080)[None,:]
        shape=np.exp(-((yy-1340)/205)**4)*(.92+.08*np.cos((xx-480)/1080*math.pi))
        self.scrim_alpha=np.clip(shape*.59*255,0,175).astype('uint8')
        self.scrim=np.full((560,1080,3),(25,13,22),dtype=np.uint8)
        self.started=time.monotonic()

    def background(self,index,t):
        segment=self.segments[index];start,end=segment['start'],segment['end']
        duration=max(1.2,end-start);u=max(0,min(1,(t-start)/duration))
        if index%2:zoom=1.076-.052*u
        else:zoom=1.024+.052*u
        # The 1.1x overscan is sampled back to the intended 1.024–1.076 zoom;
        # it is not accidentally multiplied into an 18% face crop.
        sx=1.1/zoom;vw=1080*sx;vh=1920*sx
        wiggle_x=7*math.sin(2*math.pi*u+.7*index)
        wiggle_y=5*math.sin(2*math.pi*u*.8+index)
        left=(1188-vw)/2+wiggle_x;top=(2112-vh)/2+wiggle_y
        left=max(0,min(1188-vw,left));top=max(0,min(2112-vh,top))
        matrix=np.array([[sx,0,left],[0,sx,top]],dtype=np.float64)
        return cv2.warpAffine(self.images[segment['scene']],matrix,SIZE,flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)

    def frame(self,i):
        t=i/self.plan['fps']
        index=max(0,bisect.bisect_right(self.segment_starts,t)-1)
        frame=self.background(index,t)
        dt=t-self.segments[index]['start']
        if index>0 and dt<.36:
            old=self.background(index-1,min(t,self.segments[index-1]['end']))
            mix=ease(dt/.36);frame=cv2.addWeighted(old,1-mix,frame,mix,0)
        e_index=bisect.bisect_right(self.event_starts,t)-1
        if e_index>=0:
            event=self.events[e_index]
            if event['start']<=t<event['end']:
                opacity=min(ease((t-event['start'])/.16),ease((event['end']-t)/.20))
                alpha=(self.scrim_alpha.astype(np.float32)*(opacity/255))
                frame[1040:1600]=cv2.blendLinear(frame[1040:1600],self.scrim,1-alpha,alpha)
        return frame


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',type=float,default=0);parser.add_argument('--output');args=parser.parse_args()
    r=Renderer();p=r.plan
    frames=math.ceil(args.preview*p['fps']) if args.preview else p['frames']
    output=Path(args.output) if args.output else PROJECT/'livrables/VIVI_OOR_lyrics_9x16.mp4'
    output.parent.mkdir(parents=True,exist_ok=True)
    ass=PROJECT/'livrables/VIVI_OOR_lyrics_mot_a_mot.ass';fonts=PROJECT/'assets/fonts'
    vf=(f"scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p,"
        f"ass=filename='{ass}':fontsdir='{fonts}'")
    if not args.preview:vf+=f",fade=t=out:st={p['total_duration']-3:.6f}:d=3"
    cmd=[FF,'-hide_banner','-y','-loglevel','info','-f','image2pipe','-vcodec','mjpeg','-framerate',str(p['fps']),'-i','pipe:0',
         '-i',str(WORK/'video_audio48.wav'),'-map','0:v:0','-map','1:a:0','-vf',vf,
         '-c:v','libx264','-preset','fast','-crf','21','-maxrate','1500k','-bufsize','3000k',
         '-pix_fmt','yuv420p','-profile:v','high','-level','4.1','-g','60','-bf','3','-threads','2','-filter_threads','1',
         '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',
         '-frames:v',str(frames),'-t',f'{frames/p["fps"]:.9f}','-movflags','+faststart',
         '-metadata','title=Vivi OOR — Daïsky — Lyrics','-metadata','artist=Daïsky',str(output)]
    logpath=WORK/('encode-preview.log' if args.preview else 'encode-final.log')
    begin=time.monotonic()
    with logpath.open('w') as log:
        encoder=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
        try:
            for i in range(frames):
                frame=r.frame(i)
                ok,buffer=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,91,cv2.IMWRITE_JPEG_SAMPLING_FACTOR,cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444])
                assert ok
                encoder.stdin.write(buffer.data)
                if i%300==0:
                    elapsed=time.monotonic()-begin
                    print(f'RENDER {i}/{frames} ({i/frames*100:.1f}%) elapsed={elapsed:.1f}s rate={i/max(elapsed,.01):.1f} fps',flush=True)
            encoder.stdin.close();code=encoder.wait()
        except Exception:
            encoder.kill();encoder.wait();raise
    if code:raise RuntimeError(logpath.read_text()[-7000:])
    print(f'RENDER_DONE {output} frames={frames} duration={frames/p["fps"]:.6f} bytes={output.stat().st_size} seconds={time.monotonic()-begin:.1f}',flush=True)
    (PROJECT/'metadata/render_settings.json').write_text(json.dumps(dict(frames=frames,fps=p['fps'],size=SIZE,crf=21,
        maxrate_kbps=1500,preset='fast',video_codec='H.264 high / yuv420p',audio_codec='AAC 192k 48k stereo',
        single_frame_clock=True,video_input_concatenation=False,source_images='approved Vivi OOR V2',
        opacity_badge_max=.69,lyrics_safe_bounds=[50,1100,910,1494],final_fade_seconds=3),indent=2)+'\n')


if __name__=='__main__':main()
