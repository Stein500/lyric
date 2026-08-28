import os, sys, cv2, time, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AUDIO_PATH = '/home/user/lyric/klo/Joyeux anniversaire Klo.mp3'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

os.makedirs('livrables', exist_ok=True)
os.makedirs('work/prep', exist_ok=True)
os.makedirs('assets/subtitles', exist_ok=True)

# 1. WRITE ASS SUBTITLES (CLEAN CHARACTERS)
def write_clean_ass():
    def make_ass(path, W, H, margin_v, fsize):
        header = f"""[Script Info]
Title: Joyeux Anniversaire Klo
ScriptType: v4.00+
WrapStyle: 1
PlayResX: {W}
PlayResY: {H}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,{fsize},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.5,2,2,40,40,{margin_v},1
Style: Hook,DejaVu Sans,{int(fsize*1.15)},&H00FFD24D,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4.0,2.5,2,30,30,{margin_v},1
Style: Gold,DejaVu Sans,{int(fsize*1.22)},&H0000D7FF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4.5,3,2,30,30,{margin_v},1
Style: Verse,DejaVu Sans,{fsize},&H00F5F9FF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.5,2,2,40,40,{margin_v},1
Style: Bridge,DejaVu Sans,{int(fsize*1.08)},&H00B285FF,&H000000FF,&H00000000,&H80000000,-1,1,0,0,100,100,0,0,1,3.5,2,2,40,40,{margin_v},1
Style: Wolof,DejaVu Sans,{int(fsize*1.15)},&H0000D7FF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4.0,2.5,2,30,30,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = [
            ('0:00:04.50', '0:00:08.50', 'Wolof', '{\\fad(100,150)}⚡ Wolof TechStein beat wê... ⚡'),
            ('0:00:08.50', '0:00:11.50', 'Hook', '{\\fad(100,120)}★ Klo... Confiance... ★'),
            ('0:00:11.50', '0:00:17.00', 'Gold', '{\\fad(100,120)}★ JOYEUX ANNIVERSAIRE, KLO ! ★'),
            ('0:00:17.00', '0:00:22.00', 'Hook', '{\\fad(100,120)}★ Joyeux anniversaire, ma lumière ★'),
            ('0:00:22.00', '0:00:27.00', 'Gold', '{\\fad(100,120)}★ 30 août, c\'est ton jour ★'),
            ('0:00:27.00', '0:00:33.00', 'Hook', '{\\fad(100,120)}Le monde est plus beau quand tu es là'),
            ('0:00:33.00', '0:00:35.50', 'Verse', '{\\fad(80,100)}Tu es la joie, tu es la paix'),
            ('0:00:35.50', '0:00:38.00', 'Verse', '{\\fad(80,100)}Chaque jour avec toi est un rêve'),
            ('0:00:38.00', '0:00:40.50', 'Verse', '{\\fad(80,100)}Je te souhaite tout le bonheur'),
            ('0:00:40.50', '0:00:44.00', 'Gold', '{\\fad(100,120)}Ma Confiance, mon cœur ★'),
            ('0:00:44.00', '0:00:46.50', 'Verse', '{\\fad(80,100)}Tu es la joie, tu es la paix'),
            ('0:00:46.50', '0:00:49.00', 'Verse', '{\\fad(80,100)}Chaque jour avec toi est un rêve'),
            ('0:00:49.00', '0:00:51.50', 'Verse', '{\\fad(80,100)}Je te souhaite tout le bonheur'),
            ('0:00:51.50', '0:00:54.00', 'Gold', '{\\fad(100,120)}Ma Confiance, mon cœur ★'),
            ('0:00:54.00', '0:00:57.00', 'Bridge', '{\\fad(100,120)}Que cette année soit belle'),
            ('0:00:57.00', '0:00:59.50', 'Bridge', '{\\fad(100,120)}Que tes rêves deviennent réels'),
            ('0:00:59.50', '0:01:02.00', 'Gold', '{\\fad(100,120)}★ Klo, tu es unique ★'),
            ('0:01:02.00', '0:01:05.50', 'Hook', '{\\fad(100,120)}Confiance, tu es magnifique'),
            ('0:01:05.50', '0:01:11.00', 'Gold', '{\\fad(100,120)}★ Joyeux anniversaire, JésuKlo... ★'),
            ('0:01:11.00', '0:01:16.00', 'Gold', '{\\fad(100,120)}★ Joyeux anniversaire, Confiance... ★'),
            ('0:01:16.00', '0:01:22.00', 'Wolof', '{\\fad(100,150)}⚡ Wolof TechStein beat wê... ⚡'),
            ('0:01:22.00', '0:01:31.00', 'Hook', '{\\fad(100,150)}★ 30 Août • Happy Birthday Queen Klo ★'),
            ('0:01:31.00', '0:01:34.50', 'Wolof', '{\\fad(100,150)}⚡ Wolof TechStein beat wê... ⚡'),
            ('0:01:34.50', '0:01:44.00', 'Gold', '{\\fad(100,300)}★ JOYEUX ANNIVERSAIRE KLO ! ★')
        ]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(header)
            for s, e, st, tx in events:
                f.write(f'Dialogue: 0,{s},{e},{st},,0,0,0,,{tx}\n')

    make_ass('assets/subtitles/subs_9x16.ass', 1080, 1920, 340, 52)
    make_ass('assets/subtitles/subs_16x9.ass', 1920, 1080, 160, 48)

write_clean_ass()

# TIMELINE SEGMENTS (105.024s total)
segments = [
    {"file": "klo/IMG-20260827-WA0002.jpg", "start": 0.0, "end": 11.5, "zoom": "in"},
    {"file": "klo/IMG-20260827-WA0003.jpg", "start": 11.5, "end": 22.0, "zoom": "out"},
    {"file": "klo/IMG-20260827-WA0004.jpg", "start": 22.0, "end": 33.0, "zoom": "in"},
    {"file": "klo/IMG-20260827-WA0005.jpg", "start": 33.0, "end": 44.0, "zoom": "out"},
    {"file": "klo/IMG-20260827-WA0006.jpg", "start": 44.0, "end": 54.0, "zoom": "in"},
    {"file": "klo/IMG-20260827-WA0007.jpg", "start": 54.0, "end": 65.5, "zoom": "out"},
    {"file": "klo/IMG-20260827-WA0008.jpg", "start": 65.5, "end": 76.0, "zoom": "in"},
    {"file": "livrables/Klo_Anime_Cyber_Portrait.png", "start": 76.0, "end": 83.5, "zoom": "out"},
    {"file": "klo/IMG-20260827-WA0009.jpg", "start": 83.5, "end": 91.0, "zoom": "in"},
    {"file": "livrables/Klo_Royal_Gold_Portrait.png", "start": 91.0, "end": 98.0, "zoom": "out"},
    {"file": "klo/IMG-20260827-WA0010.jpg", "start": 98.0, "end": 105.024, "zoom": "in"},
]

TOTAL_DURATION = 105.024

# 2. STATIC BADGE GENERATION (100% STATIC, NEVER MOVES)
def make_static_badge(W, H, is_portrait=True):
    badge_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge_img)
    font_badge = ImageFont.truetype(FONT_BOLD, 26 if is_portrait else 22)
    badge_text = '⚡ DAÏSKY PROD'
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_badge)
    tw_b, th_b = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    bx, by = (50, H - 120) if is_portrait else (60, H - 90)
    pad_x, pad_y = (18, 10) if is_portrait else (16, 8)
    draw.rounded_rectangle([bx, by, bx + tw_b + pad_x * 2, by + th_b + pad_y * 2], radius=12, fill=(11, 16, 36, 235), outline=(77, 210, 255, 255), width=2)
    draw.text((bx + pad_x, by + pad_y - 2), badge_text, font=font_badge, fill=(245, 249, 255, 255))
    return badge_img

badge_9x16 = make_static_badge(1080, 1920, True)
badge_9x16.save('work/prep/badge_9x16.png')

badge_16x9 = make_static_badge(1920, 1080, False)
badge_16x9.save('work/prep/badge_16x9.png')

# 3. HELPER: SAFE PASTE
def safe_paste(bg, fg, x0, y0):
    H, W = bg.shape[:2]
    fh, fw = fg.shape[:2]
    bx1, by1 = max(0, x0), max(0, y0)
    bx2, by2 = min(W, x0 + fw), min(H, y0 + fh)
    fx1, fy1 = bx1 - x0, by1 - y0
    fx2, fy2 = fx1 + (bx2 - bx1), fy1 + (by2 - by1)
    if bx2 > bx1 and by2 > by1:
        bg[by1:by2, bx1:bx2] = fg[fy1:fy2, fx1:fx2]

# 4. BUILD VIDEO 1 (9:16 TIKTOK / REELS)
def build_video_1():
    print("\n🎬 Building Video 1: Klo_HDB_9x16_TikTok_Lyrics.mp4...")
    W, H = 1080, 1920
    seg_dir = 'work/prep/v1_segs'
    os.makedirs(seg_dir, exist_ok=True)
    concat_lines = []
    
    font_hdr = ImageFont.truetype(FONT_BOLD, 24)
    hdr_text = "★ JOYEUX ANNIVERSAIRE KLO • 30 AOÛT ★"
    
    for i, seg in enumerate(segments):
        img_bgr = cv2.imread(seg["file"])
        ih, iw = img_bgr.shape[:2]
        
        # Make background
        scale_bg = max(W / iw, H / ih) * 1.15
        bw, bh = int(iw * scale_bg), int(ih * scale_bg)
        bg_big = cv2.resize(img_bgr, (bw, bh), interpolation=cv2.INTER_LINEAR)
        cx, cy = (bw - W) // 2, (bh - H) // 2
        bg_cropped = bg_big[cy:cy+H, cx:cx+W]
        blurred = cv2.GaussianBlur(bg_cropped, (51, 51), 30)
        darkened = cv2.addWeighted(blurred, 0.55, np.zeros_like(blurred), 0.45, 0)
        
        # Make foreground
        base_scale = min(W / iw, (H - 260) / ih) * 0.90
        nw, nh = int(iw * base_scale), int(ih * base_scale)
        fg_resized = cv2.resize(img_bgr, (nw, nh), interpolation=cv2.INTER_LINEAR)
        x0, y0 = (W - nw) // 2, (H - nh) // 2 - 25
        
        cv2.rectangle(darkened, (max(0, x0 - 4), max(0, y0 - 4)), (min(W, x0 + nw + 4), min(H, y0 + nh + 4)), (10, 15, 30), -1)
        safe_paste(darkened, fg_resized, x0, y0)
        cv2.rectangle(darkened, (max(0, x0), max(0, y0)), (min(W, x0 + nw), min(H, y0 + nh)), (77, 210, 255), 2)
        
        # Header banner
        pil_frame = Image.fromarray(cv2.cvtColor(darkened, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_frame)
        bbox_h = draw.textbbox((0, 0), hdr_text, font=font_hdr)
        tw_h, th_h = bbox_h[2] - bbox_h[0], bbox_h[3] - bbox_h[1]
        hx, hy = (W - tw_h) // 2, 70
        draw.rounded_rectangle([hx - 22, hy - 10, hx + tw_h + 22, hy + th_h + 10], radius=14, fill=(11, 16, 36), outline=(232, 163, 61), width=2)
        draw.text((hx, hy - 2), hdr_text, font=font_hdr, fill=(255, 225, 130))
        
        frame_path = f'{seg_dir}/frame_{i:02d}.jpg'
        pil_frame.save(frame_path, quality=95)
        
        # Zoompan clip
        dur = seg["end"] - seg["start"]
        clip_path = f'{seg_dir}/clip_{i:02d}.mp4'
        frames_num = int(dur * 24)
        
        if seg["zoom"] == "in":
            zp_expr = f"zoompan=z='min(zoom+0.0007,1.08)':d={frames_num}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=24"
        else:
            zp_expr = f"zoompan=z='if(lte(zoom,1.0),1.08,max(1.001,zoom-0.0007))':d={frames_num}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=24"
            
        cmd_clip = [
            'ffmpeg', '-y', '-loop', '1', '-i', frame_path,
            '-t', f'{dur:.3f}',
            '-vf', zp_expr,
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '21', '-pix_fmt', 'yuv420p',
            clip_path
        ]
        subprocess.run(cmd_clip, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        concat_lines.append(f"file '{os.path.abspath(clip_path)}'")
        
    concat_txt = f'{seg_dir}/concat.txt'
    with open(concat_txt, 'w') as f:
        f.write('\n'.join(concat_lines))
        
    concat_mp4 = f'{seg_dir}/concat.mp4'
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_txt, '-c', 'copy', concat_mp4], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Final mux with 100% STATIC BADGE + ASS Subtitles + Audio
    out_file = 'livrables/Klo_HDB_9x16_TikTok_Lyrics.mp4'
    cmd_mux = [
        'ffmpeg', '-y',
        '-i', concat_mp4,
        '-i', 'work/prep/badge_9x16.png',
        '-i', AUDIO_PATH,
        '-filter_complex', '[0:v][1:v]overlay=0:0[v1];[v1]ass=assets/subtitles/subs_9x16.ass[v]',
        '-map', '[v]',
        '-map', '2:a:0',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '256k',
        '-af', f'afade=t=in:st=0:d=0.3,afade=t=out:st={TOTAL_DURATION-3.0:.2f}:d=3.0',
        '-t', f'{TOTAL_DURATION:.3f}',
        '-movflags', '+faststart',
        out_file
    ]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sz = os.path.getsize(out_file) / (1024 * 1024)
    print(f"✅ Video 1 SUCCESS -> {out_file} ({sz:.2f} MB)")

build_video_1()

# 5. BUILD VIDEO 2 (16:9 YOUTUBE CINEMA)
def build_video_2():
    print("\n🎬 Building Video 2: Klo_HDB_16x9_YouTube_Cinema.mp4...")
    W, H = 1920, 1080
    seg_dir = 'work/prep/v2_segs'
    os.makedirs(seg_dir, exist_ok=True)
    concat_lines = []
    
    font_hdr = ImageFont.truetype(FONT_BOLD, 22)
    hdr_text = "★ JOYEUX ANNIVERSAIRE KLO • 30 AOÛT ★"
    
    for i, seg in enumerate(segments):
        img_bgr = cv2.imread(seg["file"])
        ih, iw = img_bgr.shape[:2]
        
        scale_bg = max(W / iw, H / ih) * 1.2
        bw, bh = int(iw * scale_bg), int(ih * scale_bg)
        bg_big = cv2.resize(img_bgr, (bw, bh), interpolation=cv2.INTER_LINEAR)
        cx, cy = (bw - W) // 2, (bh - H) // 2
        bg_cropped = bg_big[cy:cy+H, cx:cx+W]
        blurred = cv2.GaussianBlur(bg_cropped, (61, 61), 40)
        darkened = cv2.addWeighted(blurred, 0.45, np.zeros_like(blurred), 0.55, 0)
        
        base_scale = min(1100 / iw, (H - 220) / ih)
        nw, nh = int(iw * base_scale), int(ih * base_scale)
        fg_resized = cv2.resize(img_bgr, (nw, nh), interpolation=cv2.INTER_LINEAR)
        x0, y0 = (W - nw) // 2, (H - nh) // 2 - 15
        
        cv2.rectangle(darkened, (max(0, x0 - 6), max(0, y0 - 6)), (min(W, x0 + nw + 6), min(H, y0 + nh + 6)), (15, 20, 35), -1)
        safe_paste(darkened, fg_resized, x0, y0)
        cv2.rectangle(darkened, (max(0, x0), max(0, y0)), (min(W, x0 + nw), min(H, y0 + nh)), (61, 163, 232), 3)
        
        pil_frame = Image.fromarray(cv2.cvtColor(darkened, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_frame)
        bbox_h = draw.textbbox((0, 0), hdr_text, font=font_hdr)
        tw_h, th_h = bbox_h[2] - bbox_h[0], bbox_h[3] - bbox_h[1]
        hx, hy = (W - tw_h) // 2, 45
        draw.rounded_rectangle([hx - 20, hy - 8, hx + tw_h + 20, hy + th_h + 8], radius=12, fill=(11, 16, 36), outline=(232, 163, 61), width=2)
        draw.text((hx, hy - 2), hdr_text, font=font_hdr, fill=(255, 225, 130))
        
        frame_path = f'{seg_dir}/frame_{i:02d}.jpg'
        pil_frame.save(frame_path, quality=95)
        
        dur = seg["end"] - seg["start"]
        clip_path = f'{seg_dir}/clip_{i:02d}.mp4'
        frames_num = int(dur * 24)
        
        if seg["zoom"] == "in":
            zp_expr = f"zoompan=z='min(zoom+0.0006,1.07)':d={frames_num}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=24"
        else:
            zp_expr = f"zoompan=z='if(lte(zoom,1.0),1.07,max(1.001,zoom-0.0006))':d={frames_num}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=24"
            
        cmd_clip = [
            'ffmpeg', '-y', '-loop', '1', '-i', frame_path,
            '-t', f'{dur:.3f}',
            '-vf', zp_expr,
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '21', '-pix_fmt', 'yuv420p',
            clip_path
        ]
        subprocess.run(cmd_clip, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        concat_lines.append(f"file '{os.path.abspath(clip_path)}'")
        
    concat_txt = f'{seg_dir}/concat.txt'
    with open(concat_txt, 'w') as f:
        f.write('\n'.join(concat_lines))
        
    concat_mp4 = f'{seg_dir}/concat.mp4'
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_txt, '-c', 'copy', concat_mp4], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    out_file = 'livrables/Klo_HDB_16x9_YouTube_Cinema.mp4'
    cmd_mux = [
        'ffmpeg', '-y',
        '-i', concat_mp4,
        '-i', 'work/prep/badge_16x9.png',
        '-i', AUDIO_PATH,
        '-filter_complex', '[0:v][1:v]overlay=0:0[v1];[v1]ass=assets/subtitles/subs_16x9.ass[v]',
        '-map', '[v]',
        '-map', '2:a:0',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '256k',
        '-af', f'afade=t=in:st=0:d=0.3,afade=t=out:st={TOTAL_DURATION-3.0:.2f}:d=3.0',
        '-t', f'{TOTAL_DURATION:.3f}',
        '-movflags', '+faststart',
        out_file
    ]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sz = os.path.getsize(out_file) / (1024 * 1024)
    print(f"✅ Video 2 SUCCESS -> {out_file} ({sz:.2f} MB)")

build_video_2()

# 6. BUILD VIDEO 3 (9:16 WHATSAPP PRESTIGE VIP WITH GOLD GLOW & AUDIO SPECTRUM)
def build_video_3():
    print("\n🎬 Building Video 3: Klo_HDB_9x16_WhatsApp_Prestige_VIP.mp4...")
    W, H = 1080, 1920
    out_file = 'livrables/Klo_HDB_9x16_WhatsApp_Prestige_VIP.mp4'
    
    # Load raw audio for spectrum
    cmd = ['ffmpeg', '-i', AUDIO_PATH, '-f', 's16le', '-ac', '1', '-ar', '22050', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw, _ = p.communicate()
    audio_samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    sr = 22050
    
    loaded_images = [cv2.imread(s["file"]) for s in segments]
    precomputed_bg = []
    for img_bgr in loaded_images:
        ih, iw = img_bgr.shape[:2]
        scale_bg = max(W / iw, H / ih) * 1.15
        bw, bh = int(iw * scale_bg), int(ih * scale_bg)
        bg_big = cv2.resize(img_bgr, (bw, bh), interpolation=cv2.INTER_LINEAR)
        cx, cy = (bw - W) // 2, (bh - H) // 2
        bg_cropped = bg_big[cy:cy+H, cx:cx+W]
        blurred = cv2.GaussianBlur(bg_cropped, (41, 41), 25)
        gold_tint = np.full_like(blurred, (25, 35, 70))
        darkened = cv2.addWeighted(blurred, 0.55, gold_tint, 0.45, 0)
        precomputed_bg.append(darkened)
        
    font_hdr = ImageFont.truetype(FONT_BOLD, 24)
    hdr_text = "★ JOYEUX ANNIVERSAIRE KLO • 30 AOÛT ★"
    
    # Pre-render top banner
    banner_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(banner_img)
    bbox_h = draw_b.textbbox((0, 0), hdr_text, font=font_hdr)
    tw_h, th_h = bbox_h[2] - bbox_h[0], bbox_h[3] - bbox_h[1]
    hx, hy = (W - tw_h) // 2, 70
    draw_b.rounded_rectangle([hx - 22, hy - 10, hx + tw_h + 22, hy + th_h + 10], radius=14, fill=(11, 16, 36, 230), outline=(232, 163, 61, 255), width=2)
    draw_b.text((hx, hy - 2), hdr_text, font=font_hdr, fill=(255, 225, 130, 255))
    
    banner_np = np.array(banner_img)
    banner_bgr = cv2.cvtColor(banner_np[:, :, :3], cv2.COLOR_RGB2BGR)
    banner_alpha = (banner_np[:, :, 3].astype(np.float32) / 255.0)[:, :, np.newaxis]
    
    # Golden particles
    np.random.seed(42)
    num_particles = 70
    px = np.random.uniform(50, W - 50, num_particles)
    py = np.random.uniform(100, H - 200, num_particles)
    pspeed = np.random.uniform(15, 45, num_particles)
    pradius = np.random.uniform(2, 5, num_particles)
    
    total_frames = int(TOTAL_DURATION * 24)
    num_bars = 28
    
    cmd_stream = [
        'ffmpeg', '-y',
        '-f', 'rawvideo', '-vcodec', 'rawvideo',
        '-s', f'{W}x{H}', '-pix_fmt', 'bgr24', '-r', '24',
        '-i', '-',
        '-i', 'work/prep/badge_9x16.png',
        '-i', AUDIO_PATH,
        '-filter_complex', '[0:v][1:v]overlay=0:0[v1];[v1]ass=assets/subtitles/subs_9x16.ass[v]',
        '-map', '[v]',
        '-map', '2:a:0',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '21', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '256k',
        '-af', f'afade=t=in:st=0:d=0.3,afade=t=out:st={TOTAL_DURATION-3.0:.2f}:d=3.0',
        '-t', f'{TOTAL_DURATION:.3f}',
        '-movflags', '+faststart',
        out_file
    ]
    
    proc = subprocess.Popen(cmd_stream, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    cur_idx = 0
    
    for frame_idx in range(total_frames):
        t = frame_idx / 24.0
        while cur_idx < len(segments) - 1 and t >= segments[cur_idx]["end"]:
            cur_idx += 1
            
        seg = segments[cur_idx]
        img_bgr = loaded_images[cur_idx]
        bg_frame = precomputed_bg[cur_idx].copy()
        
        seg_dur = seg["end"] - seg["start"]
        prog = max(0.0, min(1.0, (t - seg["start"]) / seg_dur))
        zoom = (1.0 + 0.08 * prog) if seg["zoom"] == "in" else (1.08 - 0.08 * prog)
        
        ih, iw = img_bgr.shape[:2]
        base_scale = min(W / iw, (H - 300) / ih) * 0.88
        scale = base_scale * zoom
        nw, nh = int(iw * scale), int(ih * scale)
        fg_resized = cv2.resize(img_bgr, (nw, nh), interpolation=cv2.INTER_LINEAR)
        
        x0 = (W - nw) // 2
        y0 = (H - nh) // 2 - 35
        
        # Double gold luxury border
        cv2.rectangle(bg_frame, (max(0, x0 - 8), max(0, y0 - 8)), (min(W, x0 + nw + 8), min(H, y0 + nh + 8)), (20, 25, 45), -1)
        safe_paste(bg_frame, fg_resized, x0, y0)
        cv2.rectangle(bg_frame, (max(0, x0 - 4), max(0, y0 - 4)), (min(W, x0 + nw + 4), min(H, y0 + nh + 4)), (0, 215, 255), 2)
        cv2.rectangle(bg_frame, (max(0, x0), max(0, y0)), (min(W, x0 + nw), min(H, y0 + nh)), (77, 210, 255), 2)
        
        # Floating sparkles
        for p_i in range(num_particles):
            cur_py = (py[p_i] - pspeed[p_i] * t) % (H - 250) + 100
            cur_px = (px[p_i] + math.sin(t * 2 + p_i) * 15) % (W - 80) + 40
            rad = int(pradius[p_i] + math.sin(t * 5 + p_i) * 1.5)
            if rad > 1:
                cv2.circle(bg_frame, (int(cur_px), int(cur_py)), rad, (0, 215, 255), -1)
                cv2.circle(bg_frame, (int(cur_px), int(cur_py)), max(1, rad // 2), (255, 255, 255), -1)
                
        # Audio visualizer spectrum
        sample_center = int(t * sr)
        window = int(0.05 * sr)
        s_start = max(0, sample_center - window)
        s_end = min(len(audio_samples), sample_center + window)
        if s_end > s_start:
            chunk = audio_samples[s_start:s_end]
            fft_vals = np.abs(np.fft.rfft(chunk * np.hanning(len(chunk))))
            spec = np.interp(np.linspace(0, len(fft_vals)//3, num_bars), np.arange(len(fft_vals)), fft_vals)
            spec_max = np.max(spec) + 1e-6
            norm_spec = np.clip(spec / max(spec_max, 4.0), 0.05, 1.0)
        else:
            norm_spec = np.full(num_bars, 0.1)

        bar_w = 18
        bar_gap = 10
        total_spec_w = num_bars * bar_w + (num_bars - 1) * bar_gap
        start_spec_x = (W - total_spec_w) // 2
        spec_base_y = H - 240
        
        for b_i in range(num_bars):
            bh = int(norm_spec[b_i] * 80)
            bx = start_spec_x + b_i * (bar_w + bar_gap)
            b_col = (int(77 + (0 - 77) * (b_i / num_bars)), int(210 + (215 - 210) * (b_i / num_bars)), 255)
            cv2.rectangle(bg_frame, (bx, spec_base_y - bh), (bx + bar_w, spec_base_y), b_col, -1)
            cv2.circle(bg_frame, (bx + bar_w // 2, spec_base_y - bh), 3, (255, 255, 255), -1)
            
        # Composite top banner
        out_frame = (bg_frame * (1.0 - banner_alpha) + banner_bgr * banner_alpha).astype(np.uint8)
        proc.stdin.write(out_frame.tobytes())
        
    proc.stdin.close()
    proc.wait()
    sz = os.path.getsize(out_file) / (1024 * 1024)
    print(f"✅ Video 3 SUCCESS -> {out_file} ({sz:.2f} MB)")

build_video_3()

# 7. BUILD GIFS
def build_gifs():
    print("\n✨ Building Animated GIFs...")
    
    # GIF 1 : Carte d'anniversaire scintillante (540x960, 48 frames loop)
    gif1_path = 'livrables/Klo_HDB_Carte_Scintillante.gif'
    GW, GH, GFPS, GDUR = 540, 960, 12, 4.0
    gframes_total = int(GFPS * GDUR)
    
    src_royal = cv2.imread('livrables/Klo_Royal_Gold_Portrait.png')
    src_royal = cv2.resize(src_royal, (460, int(460 * src_royal.shape[0] / src_royal.shape[1])))
    
    gif1_frames = []
    bg_base = np.zeros((GH, GW, 3), dtype=np.uint8)
    bg_base[:, :] = (20, 15, 35)
    
    np.random.seed(99)
    n_sp = 50
    sp_x = np.random.uniform(20, GW - 20, n_sp)
    sp_y = np.random.uniform(50, GH - 50, n_sp)
    sp_speed = np.random.uniform(10, 30, n_sp)
    sp_phase = np.random.uniform(0, math.pi * 2, n_sp)
    
    font_g1_hdr = ImageFont.truetype(FONT_BOLD, 22)
    font_g1_sub = ImageFont.truetype(FONT_BOLD, 18)
    font_g1_date = ImageFont.truetype(FONT_BOLD, 20)
    
    for f in range(gframes_total):
        gt = f / GFPS
        f_img = bg_base.copy()
        
        px0 = (GW - src_royal.shape[1]) // 2
        py0 = (GH - src_royal.shape[0]) // 2 - 20
        safe_paste(f_img, src_royal, px0, py0)
        
        pulse = 0.5 + 0.5 * math.sin(gt * math.pi * 2)
        frame_gold = (0, int(180 + 75 * pulse), 255)
        cv2.rectangle(f_img, (px0 - 4, py0 - 4), (px0 + src_royal.shape[1] + 4, py0 + src_royal.shape[0] + 4), frame_gold, 2)
        
        for i in range(n_sp):
            sy = (sp_y[i] - sp_speed[i] * gt) % (GH - 60) + 30
            sx = (sp_x[i] + math.sin(gt * 3 + sp_phase[i]) * 10) % (GW - 40) + 20
            brightness = 0.5 + 0.5 * math.sin(gt * math.pi * 4 + sp_phase[i])
            r = int(1.5 + 2.5 * brightness)
            col = (int(100 * brightness), int(215 * brightness), 255)
            cv2.circle(f_img, (int(sx), int(sy)), r, col, -1)
            
        pil_frame = Image.fromarray(cv2.cvtColor(f_img, cv2.COLOR_BGR2RGB))
        draw_g = ImageDraw.Draw(pil_frame)
        
        t1 = "★ JOYEUX ANNIVERSAIRE ★"
        b1 = draw_g.textbbox((0, 0), t1, font=font_g1_hdr)
        draw_g.text(((GW - (b1[2]-b1[0]))//2, 60), t1, font=font_g1_hdr, fill=(255, 215, 0))
        
        t2 = "👑 QUEEN KLO 👑"
        b2 = draw_g.textbbox((0, 0), t2, font=font_g1_hdr)
        draw_g.text(((GW - (b2[2]-b2[0]))//2, 100), t2, font=font_g1_hdr, fill=(255, 240, 180))
        
        t3 = "★ 30 AOÛT • MA CONFIANCE ★"
        b3 = draw_g.textbbox((0, 0), t3, font=font_g1_date)
        draw_g.rounded_rectangle([(GW - (b3[2]-b3[0]))//2 - 15, GH - 110, (GW + (b3[2]-b3[0]))//2 + 15, GH - 70], radius=10, fill=(11, 16, 36), outline=(232, 163, 61), width=2)
        draw_g.text(((GW - (b3[2]-b3[0]))//2, GH - 100), t3, font=font_g1_date, fill=(255, 215, 0))
        
        gif1_frames.append(pil_frame)
        
    gif1_frames[0].save(
        gif1_path,
        save_all=True,
        append_images=gif1_frames[1:],
        duration=int(1000 / GFPS),
        loop=0,
        optimize=True
    )
    sz1 = os.path.getsize(gif1_path) / (1024 * 1024)
    print(f"✅ GIF 1 SUCCESS -> {gif1_path} ({sz1:.2f} MB)")
    
    # GIF 2 : Sticker carré animé (500x500, 36 frames loop)
    gif2_path = 'livrables/Klo_HDB_Queen_Klo_Sticker.gif'
    SW, SH = 500, 500
    sframes_total = 36
    
    src_crop = cv2.imread('livrables/Klo_Royal_Gold_Portrait.png')
    src_crop = cv2.resize(src_crop, (320, 320))
    
    mask = np.zeros((320, 320), dtype=np.uint8)
    cv2.circle(mask, (160, 160), 155, 255, -1)
    
    gif2_frames = []
    for f in range(sframes_total):
        st = f / 12.0
        frame_s = np.zeros((SH, SW, 3), dtype=np.uint8)
        frame_s[:, :] = (15, 12, 28)
        
        cx, cy = SW // 2, SH // 2 - 10
        f_crop = src_crop.copy()
        
        for y in range(320):
            for x in range(320):
                if mask[y, x] > 0:
                    frame_s[cy - 160 + y, cx - 160 + x] = f_crop[y, x]
                    
        pulse = 0.5 + 0.5 * math.sin(st * math.pi * 2)
        c_gold = (0, int(180 + 75 * pulse), 255)
        cv2.circle(frame_s, (cx, cy), 158, c_gold, 4)
        cv2.circle(frame_s, (cx, cy), 164, (77, 210, 255), 2)
        
        pil_s = Image.fromarray(cv2.cvtColor(frame_s, cv2.COLOR_BGR2RGB))
        draw_s = ImageDraw.Draw(pil_s)
        
        font_s_top = ImageFont.truetype(FONT_BOLD, 22)
        font_s_bot = ImageFont.truetype(FONT_BOLD, 18)
        
        st1 = "👑 QUEEN KLO 👑"
        sb1 = draw_s.textbbox((0, 0), st1, font=font_s_top)
        draw_s.rounded_rectangle([(SW - (sb1[2]-sb1[0]))//2 - 12, 18, (SW + (sb1[2]-sb1[0]))//2 + 12, 54], radius=10, fill=(11, 16, 36), outline=(255, 215, 0), width=2)
        draw_s.text(((SW - (sb1[2]-sb1[0]))//2, 24), st1, font=font_s_top, fill=(255, 225, 120))
        
        st2 = "★ 30 AOÛT • MA CONFIANCE ★"
        sb2 = draw_s.textbbox((0, 0), st2, font=font_s_bot)
        draw_s.rounded_rectangle([(SW - (sb2[2]-sb2[0]))//2 - 12, SH - 55, (SW + (sb2[2]-sb2[0]))//2 + 12, SH - 18], radius=10, fill=(11, 16, 36), outline=(77, 210, 255), width=2)
        draw_s.text(((SW - (sb2[2]-sb2[0]))//2, SH - 48), st2, font=font_s_bot, fill=(255, 255, 255))
        
        gif2_frames.append(pil_s)
        
    gif2_frames[0].save(
        gif2_path,
        save_all=True,
        append_images=gif2_frames[1:],
        duration=int(1000 / 12),
        loop=0,
        optimize=True
    )
    sz2 = os.path.getsize(gif2_path) / (1024 * 1024)
    print(f"✅ GIF 2 SUCCESS -> {gif2_path} ({sz2:.2f} MB)")

build_gifs()

print("\n🎉🎉🎉 ALL DELIVERABLES FULLY GENERATED! 🎉🎉🎉")
