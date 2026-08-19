#!/usr/bin/env python3
"""
LYRIC VIDEO — PLATFORM VARIANTS GENERATOR
Génère toutes les variantes : TikTok, Instagram Reels, X, Snapchat, WhatsApp, Telegram
Utilise OpenCV + MoviePy + FFmpeg
"""

import os, sys, subprocess, json, glob
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from imageio_ffmpeg import get_ffmpeg_exe

BASE = Path(__file__).resolve().parent.parent
AUDIO = str(BASE / "I'm_not_afraid_Daïsky.mp3")
OUTPUT = str(BASE / "production" / "video")
os.makedirs(OUTPUT, exist_ok=True)

FFMPEG = get_ffmpeg_exe()

FPS = 30

# ── RE-IMPORT the FrameRenderer from the main script ──
sys.path.insert(0, str(BASE / "production"))
from generate_lyric_video import FrameRenderer, build_timeline, W, H, BLACK, GOLD, WHITE

renderer = FrameRenderer(W, H, FPS)

def render_segment(start, end, output_path, width=1920, height=1080, crf=23):
    """Render a segment of the video"""
    dur = end - start
    # If dimensions differ from original, we'll render and then crop
    render_w, render_h = W, H
    
    def make_frame(t):
        return renderer.render(start + t)
    
    from moviepy import VideoClip, AudioFileClip
    
    clip = VideoClip(make_frame, duration=dur).with_fps(FPS)
    
    # Audio
    try:
        if os.path.exists(AUDIO):
            audio = AudioFileClip(AUDIO).subclipped(start, min(end, 215.0))
            clip = clip.with_audio(audio)
    except:
        pass
    
    # If we need 9:16, we'll create it differently
    if width != 1920 or height != 1080:
        # Resize first
        clip = clip.resized((width, height))
    
    print(f"  • Exporting {output_path}...")
    clip.write_videofile(
        output_path, fps=FPS, codec="libx264", audio_codec="aac",
        threads=4, preset="medium", bitrate="4000k",
        ffmpeg_params=["-crf", str(crf)]
    )
    clip.close()
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"  ✅ {size_mb:.1f} MB")
    return output_path


def make_vertical(input_path, output_path, crop_w=1080, crop_h=1920):
    """Convert 16:9 to 9:16 by cropping center"""
    print(f"  • Converting to 9:16 vertical...")
    cmd = [
        FFMPEG, "-i", input_path,
        "-vf", f"crop=ih*9/16:ih,scale={crop_w}:{crop_h}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-y", output_path
    ]
    subprocess.run(cmd, capture_output=True)
    size = os.path.getsize(output_path) / 1024 / 1024
    print(f"  ✅ Vertical: {size:.1f} MB")
    return output_path


def gen_tiktok_variants():
    """Generate TikTok versions (9:16 vertical)"""
    print("\n📱 TIKTOK VERSIONS")
    print("=" * 50)
    
    # TikTok short 1: intro + Wolof (0:00-0:50) - most viral
    seg1 = os.path.join(OUTPUT, "tiktok_short1_temp.mp4")
    out1 = os.path.join(OUTPUT, "tiktok_short1_viral.mp4")
    print("  🎬 Short 1: Intro + Wolof (0:00-0:50)")
    render_segment(0, 50, seg1)
    make_vertical(seg1, out1)
    os.remove(seg1)
    
    # TikTok short 2: Refrain 1 (1:34-2:05) - most energetic
    seg2 = os.path.join(OUTPUT, "tiktok_short2_temp.mp4")
    out2 = os.path.join(OUTPUT, "tiktok_short2_refrain.mp4")
    print("  🎬 Short 2: Refrain (1:34-2:05)")
    render_segment(94, 125, seg2)
    make_vertical(seg2, out2)
    os.remove(seg2)
    
    # TikTok short 3: Final Wolof (2:45-3:15) - beat drop
    seg3 = os.path.join(OUTPUT, "tiktok_short3_temp.mp4")
    out3 = os.path.join(OUTPUT, "tiktok_short3_finale.mp4")
    print("  🎬 Short 3: Final Wolof + beat drop (2:45-3:15)")
    render_segment(165, 195, seg3)
    make_vertical(seg3, out3)
    os.remove(seg3)
    
    print("  ✅ 3 TikTok variants done!")


def gen_instagram_variants():
    """Generate Instagram Reels (9:16 vertical)"""
    print("\n📱 INSTAGRAM REELS")
    print("=" * 50)
    
    # Reel 1: Break the chains + Wolof (0:24-0:55) 
    seg1 = os.path.join(OUTPUT, "ig_reel1_temp.mp4")
    out1 = os.path.join(OUTPUT, "instagram_reel1_chains.mp4")
    print("  🎬 Reel 1: Break chains + Wolof (0:24-0:55)")
    render_segment(24, 55, seg1)
    make_vertical(seg1, out1)
    os.remove(seg1)
    
    # Reel 2: Emotional couplet + translation (0:55-1:30)
    seg2 = os.path.join(OUTPUT, "ig_reel2_temp.mp4")
    out2 = os.path.join(OUTPUT, "instagram_reel2_emotion.mp4")
    print("  🎬 Reel 2: Émotion + traduction (0:55-1:30)")
    render_segment(55, 90, seg2)
    make_vertical(seg2, out2)
    os.remove(seg2)
    
    # Reel 3: Bridge + finale (2:25-3:15)
    seg3 = os.path.join(OUTPUT, "ig_reel3_temp.mp4")
    out3 = os.path.join(OUTPUT, "instagram_reel3_bridge.mp4")
    print("  🎬 Reel 3: Pont + Finale (2:25-3:15)")
    render_segment(145, 195, seg3)
    make_vertical(seg3, out3)
    os.remove(seg3)
    
    print("  ✅ 3 Instagram Reels done!")


def gen_x_variant():
    """Generate X/Twitter version (16:9, max 2:20)"""
    print("\n📱 X (TWITTER)")
    print("=" * 50)
    out = os.path.join(OUTPUT, "x_twitter_short.mp4")
    print("  🎬 X: Highlights 0:00-2:20")
    render_segment(0, 140, out)
    print("  ✅ X version done!")


def gen_snapchat_variant():
    """Generate Snapchat (9:16, 0:30)"""
    print("\n📱 SNAPCHAT")
    print("=" * 50)
    seg = os.path.join(OUTPUT, "snapchat_temp.mp4")
    out = os.path.join(OUTPUT, "snapchat_ultrashort.mp4")
    print("  🎬 Snapchat: Intro hit (0:00-0:30)")
    render_segment(0, 30, seg)
    make_vertical(seg, out)
    os.remove(seg)
    print("  ✅ Snapchat done!")


def gen_whatsapp_variant():
    """Generate WhatsApp Status (9:16, 0:30)"""
    print("\n📱 WHATSAPP STATUS")
    print("=" * 50)
    seg = os.path.join(OUTPUT, "whatsapp_temp.mp4")
    out = os.path.join(OUTPUT, "whatsapp_status.mp4")
    print("  🎬 WhatsApp: Refrain hit (1:16-1:46)")
    render_segment(76.5, 106.5, seg)
    make_vertical(seg, out)
    os.remove(seg)
    print("  ✅ WhatsApp Status done!")


def gen_telegram_variant():
    """Generate Telegram version (16:9 full like YouTube)"""
    print("\n📱 TELEGRAM")
    print("=" * 50)
    out = os.path.join(OUTPUT, "telegram_full.mp4")
    print("  🎬 Telegram: Full video (same as YouTube)")
    render_segment(0, 215, out, crf=25)  # Slightly higher compression for Telegram
    print("  ✅ Telegram done!")


def gen_mboazick_variant():
    """Generate MboaZick version (16:9 full)"""
    print("\n📱 MBOAZICK")
    print("=" * 50)
    out = os.path.join(OUTPUT, "mboazick_full.mp4")
    print("  🎬 MboaZick: Full video")
    render_segment(0, 215, out)
    print("  ✅ MboaZick done!")


def gen_facebook_variant():
    """Generate Facebook version (16:9, full)"""
    print("\n📱 FACEBOOK")
    print("=" * 50)
    out = os.path.join(OUTPUT, "facebook_full.mp4")
    print("  🎬 Facebook: Full video")
    render_segment(0, 215, out)
    print("  ✅ Facebook done!")


def cleanup_temp():
    """Clean up temporary files"""
    for f in glob.glob(os.path.join(OUTPUT, "*temp*")):
        os.remove(f)
    for f in glob.glob(os.path.join(OUTPUT, "*TEMP_MPY*")):
        os.remove(f)


if __name__ == "__main__":
    print("=" * 60)
    print("🔥 DAÏSKY — PLATFORM VARIANTS GENERATOR 🔥")
    print("=" * 60)
    
    cleanup_temp()
    
    # Generate all variants
    gen_facebook_variant()
    gen_tiktok_variants()
    gen_instagram_variants()
    gen_x_variant()
    gen_snapchat_variant()
    gen_whatsapp_variant()
    gen_telegram_variant()
    gen_mboazick_variant()
    
    cleanup_temp()
    
    print("\n" + "=" * 60)
    print("✅ TOUTES LES VARIANTES GÉNÉRÉES !")
    print("=" * 60)
    
    # List all generated files
    print("\n📁 Fichiers générés :")
    for f in sorted(glob.glob(os.path.join(OUTPUT, "*.mp4"))):
        name = os.path.basename(f)
        size = os.path.getsize(f) / 1024 / 1024
        print(f"  • {name:40s} {size:6.1f} MB")