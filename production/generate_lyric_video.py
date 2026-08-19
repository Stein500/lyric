#!/usr/bin/env python3
"""
LYRIC VIDEO GENERATOR — Daïsky « I'm Not Afraid »
Timeline unique, traductions EN→FR, effets visuels
"""

import os, sys, math, json, random
from typing import List, Tuple, Optional
from dataclasses import dataclass, field

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    VideoClip, AudioFileClip, ImageClip, TextClip,
    CompositeVideoClip, concatenate_videoclips, vfx
)

# ─── PATHS ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(BASE_DIR, "..", "I'm_not_afraid_Daïsky.mp3")
IMG_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "production", "video")
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1920, 1080
FPS = 30

# ─── COLORS ────────────────────────────────────────────────────────────────
BLACK = (10, 10, 10)
GOLD = (255, 215, 0)
WARM_GOLD = (255, 185, 15)
DARK_RED = (139, 0, 0)
WHITE = (255, 255, 255)
DIM_WHITE = (200, 200, 200)
SILVER = (192, 192, 192)
ORANGE = (255, 140, 0)
DARK_BLUE = (5, 5, 40)
PURPLE = (40, 5, 40)

# ─── FONTS ─────────────────────────────────────────────────────────────────
def get_font(size, bold=True):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

# ─── BACKGROUNDS ────────────────────────────────────────────────────────────
def gradient(w, h, c1, c2, direction="v"):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    steps = h if direction == "v" else w
    for i in range(steps):
        r = i / steps
        cr = tuple(int(c1[j]*(1-r) + c2[j]*r) for j in range(3))
        if direction == "v":
            draw.line([(0,i), (w,i)], fill=cr, width=1)
        else:
            draw.line([(i,0), (i,h)], fill=cr, width=1)
    return img

def glow_overlay(img, cx, cy, radius, color, intensity=50):
    """Add radial glow effect"""
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    for r in range(radius, 0, -20):
        a = int(intensity * (1 - r/radius))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, a))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

def particles_overlay(w, h, count=40, color=GOLD):
    overlay = Image.new("RGBA", (w, h), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    for _ in range(count):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.randint(1, 3)
        a = random.randint(80, 200)
        draw.ellipse([x-s, y-s, x+s, y+s], fill=(*color, a))
    return overlay

# ─── TEXT DRAWING ──────────────────────────────────────────────────────────
def draw_text_centered(draw, text, y, font_size, color, glow=False, outline=True):
    font = get_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (W - tw) // 2
    y_pos = y - th // 2
    
    if glow:
        for o in range(6, 0, -2):
            a = max(5, 30 - o*3)
            draw.text((x+o, y_pos), text, font=font, fill=(*color, a//4))
            draw.text((x-o, y_pos), text, font=font, fill=(*color, a//4))
    if outline:
        for dx,dy in [(-2,-2),(-2,2),(2,-2),(2,2)]:
            draw.text((x+dx, y_pos+dy), text, font=font, fill=(0,0,0))
    draw.text((x, y_pos), text, font=font, fill=color)
    return th

# ─── LYRIC LINE ────────────────────────────────────────────────────────────
@dataclass
class LyricEvent:
    t_start: float
    t_end: float
    text_en: str = ""
    text_fr: str = ""
    size: int = 80
    color: Tuple = WHITE
    bg_action: str = ""   # "flash", "glow", "glitch"

# ─── FULL TIMELINE ─────────────────────────────────────────────────────────
def build_timeline() -> Tuple[List[Tuple[str, Tuple, float, float]], List[LyricEvent]]:
    """
    Returns (background_phases, lyric_events)
    background_phases: (style_name, colors_tuple, start, end)
    """
    
    phases = [
        ("intro",       (BLACK, (20,0,0)),           0.0,   13.0),
        ("emerge",      (BLACK, (30,20,5)),          13.0,  24.0),
        ("chains",      (BLACK, (40,20,0)),          24.0,  34.0),
        ("wolof1",      ((50,50,0), (10,10,10)),      34.0,  50.0),
        ("darkness",    ((10,10,30), (20,0,20)),      50.0,  58.0),
        ("flame",       ((30,10,0), (10,10,20)),      58.0,  66.0),
        ("resolve",     ((20,20,5), (10,5,20)),       66.0,  76.5),
        ("refrain1_en", ((40,30,5), (10,10,20)),      76.5,  94.0),
        ("refrain1_fr", ((50,40,0), (10,10,10)),      94.0,  110.0),
        ("wolof2",      ((60,40,0), (10,10,10)),      110.0, 110.9),
        ("couplet2",    ((30,5,0), (5,5,20)),         110.9, 122.0),
        ("triumph",     ((40,30,5), (10,10,10)),      122.0, 127.8),
        ("refrain2_en", ((50,40,5), (10,10,20)),      127.8, 145.0),
        ("bridge",      ((5,5,40), (5,5,20)),         145.8, 165.0),
        ("finale",      ((60,50,0), (10,10,10)),      165.0, 195.0),
        ("outro1",      ((20,20,20), (50,50,50)),     195.0, 202.0),
        ("outro2",      (BLACK, (20,0,0)),            202.0, 215.0),
    ]
    
    events = [
        # ── Intro CTA ──
        LyricEvent(0.5, 3.0, "🔥 NOUVEAU SON 🔥", "", 70, GOLD, ""),
        LyricEvent(3.5, 5.5, "Daïsky", "", 120, WHITE, "glow"),
        LyricEvent(5.5, 8.0, "I'M NOT AFRAID", "", 100, GOLD, "glow"),
        LyricEvent(8.5, 10.5, "[Prod. TechStein]", "", 50, SILVER, ""),
        LyricEvent(10.5, 13.0, "👆 ABONNE-TOI — LIKE — COMMENTE 👆", "", 55, DARK_RED, "flash"),
        
        # ── Yeah / Emerge ──
        LyricEvent(13.0, 16.0, "Yeah...", "", 140, WHITE, "glow"),
        LyricEvent(16.0, 20.0, "Je n'ai plus peur...", "I'm not afraid anymore", 90, GOLD, "glow"),
        LyricEvent(20.0, 24.0, "To stand up → Se lever", "", 75, WHITE, ""),
        
        # ── Break the chains ──
        LyricEvent(24.0, 28.0, "To stand up → Se lever", "", 85, WHITE, ""),
        LyricEvent(28.0, 34.0, "To break the chains → Briser les chaînes", "", 85, GOLD, "flash"),
        
        # ── Wolof TechStein beat wê! x3 ──
        LyricEvent(34.0, 39.0, "WOLOF TECHSTEIN", "", 110, GOLD, "glow"),
        LyricEvent(39.0, 44.0, "BEAT WÊ! 🔥", "", 120, ORANGE, "flash"),
        LyricEvent(44.0, 50.0, "WOLOF ❖ TECHSTEIN ❖ BEAT ❖ WÊ! ⚡", "", 90, GOLD, "flash"),
        
        # ── Couplet 1 - darkness ──
        LyricEvent(50.0, 52.5, "J'ai touché le fond", "", 85, DIM_WHITE, ""),
        LyricEvent(52.5, 55.0, "J'ai vu le vide en face", "", 85, DIM_WHITE, ""),
        LyricEvent(55.0, 57.0, "Les doutes m'ont bouffé", "", 75, DIM_WHITE, ""),
        LyricEvent(57.0, 58.5, "J'ai perdu ma trace", "", 75, DIM_WHITE, ""),
        
        # ── Flame emerges ──
        LyricEvent(58.5, 61.5, "Mais dans le noir", "", 90, GOLD, "glow"),
        LyricEvent(61.5, 64.0, "j'ai trouvé une ✦ flamme", "", 90, ORANGE, ""),
        LyricEvent(64.0, 66.0, "Petite mais brûlante", "", 80, WARM_GOLD, ""),
        
        # ── Resolve ──
        LyricEvent(66.0, 68.0, "elle a ravivé mon âme", "", 80, GOLD, ""),
        LyricEvent(68.0, 71.0, "On m'a dit \"t'y arriveras pas\"", "They said you won't make it", 70, DARK_RED, ""),
        LyricEvent(71.0, 74.0, "Mais j'ai transformé leurs mots", "", 85, GOLD, "glow"),
        LyricEvent(74.0, 76.5, "en carburant, en vérité", "", 85, GOLD, ""),
        LyricEvent(68.0, 71.0, "Chaque chute m'a forgé", "Fall forged me", 75, SILVER, ""),
        LyricEvent(71.0, 74.0, "Chaque larme m'a lavé", "Tears cleansed me", 75, SILVER, ""),
        LyricEvent(74.0, 76.5, "Je marche sur l'eau", "Now I walk on water", 85, GOLD, "glow"),
        LyricEvent(76.0, 76.5, "J'ai plus peur de me noyer", "Not afraid to drown", 80, GOLD, ""),
        
        # ── Refrain 1 English ──
        LyricEvent(76.5, 80.5, "I've been down, I've been low", "J'ai touché le fond", 85, WHITE, ""),
        LyricEvent(80.5, 84.5, "But I'm ready, I'm ready to go", "Mais je suis prêt à avancer", 85, GOLD, "glow"),
        LyricEvent(84.5, 88.5, "I've been broken, I've been scarred", "J'ai été brisé, marqué", 85, WHITE, ""),
        LyricEvent(88.5, 94.0, "But I'm rising, I'm reaching the stars", "Mais je m'élève, j'atteins les étoiles", 85, GOLD, "glow"),
        
        # ── Refrain 1 French ──
        LyricEvent(94.0, 98.0, "I'M NOT AFRAID", "Je n'ai pas peur", 120, GOLD, "glow"),
        LyricEvent(98.0, 101.0, "To stand up → Me lever", "", 80, WHITE, ""),
        LyricEvent(101.0, 103.5, "To break the chains → Briser les chaînes", "", 80, GOLD, ""),
        LyricEvent(103.5, 107.0, "I'M NOT AFRAID", "Je n'ai pas peur", 120, GOLD, "flash"),
        LyricEvent(107.0, 110.0, "To rise again → Renaître", "Through the pain → À travers la douleur", 75, WHITE, ""),
        
        # ── Wolof TechStein ──
        LyricEvent(110.0, 110.9, "WOLOF TECHSTEIN BEAT WÊ! 🔥⚡", "", 100, GOLD, "glitch"),
        
        # ── Couplet 2 ──
        LyricEvent(110.9, 113.5, "Ils voulaient me voir à genoux", "They wanted me on my knees", 75, DIM_WHITE, ""),
        LyricEvent(113.5, 116.0, "Mendier, supplier...", "", 70, DARK_RED, ""),
        LyricEvent(116.0, 119.0, "MAIS j'ai choisi de me battre", "But I chose to fight", 90, GOLD, "glow"),
        LyricEvent(119.0, 122.0, "J'ai rêvé, j'ai sué, j'ai pleuré", "I dreamed, sweated, cried", 80, WHITE, ""),
        
        # ── Triumph ──
        LyricEvent(122.0, 124.5, "FOI 🔥 FEU 🔥 TEMPS", "Faith Fire Time", 90, GOLD, "glow"),
        LyricEvent(124.5, 127.8, "Je RÉUSSIRAI", "I WILL SUCCEED", 110, GOLD, "flash"),
        LyricEvent(126.0, 127.8, "Ma réussite = ma plus belle cicatrice", "My success = my finest scar", 75, GOLD, ""),
        
        # ── Refrain 2 English ──
        LyricEvent(127.8, 131.5, "I've been down, I've been low", "J'ai été au fond", 85, WHITE, ""),
        LyricEvent(131.5, 135.5, "But I'm ready, I'm ready to go", "Mais je suis prêt", 85, GOLD, "glow"),
        LyricEvent(135.5, 139.5, "I've been broken, I've been scarred", "J'ai été brisé", 85, WHITE, ""),
        LyricEvent(139.5, 145.0, "But I'm rising, I'm reaching the stars", "Mais je m'élève", 85, GOLD, "glow"),
        
        # ── Bridge ──
        LyricEvent(145.8, 149.0, "I'm not afraid of the fall", "Je n'ai pas peur de tomber", 80, WHITE, ""),
        LyricEvent(149.0, 152.5, "I'm not afraid of it all", "Je n'ai peur de rien", 80, WHITE, ""),
        LyricEvent(152.5, 157.0, "I've survived the worst of me", "J'ai survécu au pire de moi-même", 85, GOLD, "glow"),
        LyricEvent(157.0, 165.0, "Now I'm finally free", "Maintenant, je suis enfin libre", 100, GOLD, "glow"),
        
        # ── Finale ──
        LyricEvent(165.0, 169.0, "I'M NOT AFRAID !!!", "Je n'ai pas peur", 120, GOLD, "flash"),
        LyricEvent(169.0, 173.0, "I'M NOT AFRAID !!!", "Je n'ai pas peur", 120, GOLD, "flash"),
        LyricEvent(173.0, 177.0, "To rise again through the pain", "Renaître à travers la douleur", 80, WHITE, ""),
        LyricEvent(177.0, 182.0, "WOLOF ❖ TECHSTEIN ❖ BEAT ❖ WÊ!", "", 95, GOLD, "glitch"),
        LyricEvent(182.0, 187.0, "🔥 ⚡ 🔥 ⚡ 🔥", "", 120, ORANGE, "flash"),
        LyricEvent(187.0, 195.0, "WOLOF TECHSTEIN BEAT WÊ!", "", 100, GOLD, "glitch"),
        
        # ── Outro ──
        LyricEvent(195.0, 198.5, "I'm not afraid...", "Je n'ai plus peur", 90, DIM_WHITE, ""),
        LyricEvent(198.5, 202.0, "✧ ✧ ✧", "", 60, SILVER, ""),
        
        # ── CTA final ──
        LyricEvent(202.0, 206.0, "Daïsky — I'm Not Afraid", "", 90, GOLD, "glow"),
        LyricEvent(206.0, 209.0, "[Prod. TechStein]", "", 55, SILVER, ""),
        LyricEvent(209.0, 212.5, "🔔 ABONNE-TOI  ❤️ LIKE  💬 COMMENTE", "", 60, WHITE, "flash"),
        LyricEvent(212.5, 215.0, "#ImaNotAfraid #Daïsky #TechStein #MboaZick", "", 40, SILVER, ""),
    ]
    
    return phases, events


# ─── FRAME RENDERER ────────────────────────────────────────────────────────
class FrameRenderer:
    def __init__(self, W, H, FPS):
        self.W, self.W = W, H
        self.FPS = FPS
        self.phases, self.events = build_timeline()
    
    def get_bg_at(self, t):
        """Get background colors for a given time"""
        for name, colors, start, end in self.phases:
            if start <= t < end:
                return name, colors
        return "default", (BLACK, BLACK)
    
    def get_active_events(self, t):
        """Get events active at time t"""
        return [e for e in self.events if e.t_start <= t < e.t_end]
    
    def render(self, t):
        """Render one frame at time t"""
        # Get background
        bg_name, (c1, c2) = self.get_bg_at(t)
        
        # Build base background
        img = gradient(W, H, c1, c2)
        
        # Glow on bright phases
        if "glow" in bg_name or bg_name in ("finale", "refrain1_fr", "triumph"):
            img = glow_overlay(img, W//2, H//3, 600, GOLD, 30)
        if bg_name == "bridge":
            img = glow_overlay(img, W//2, H//2, 500, (100, 100, 255), 20)
        
        # Particles
        if random.random() < 0.4:
            p = particles_overlay(W, H, 30, GOLD)
            img = Image.alpha_composite(img.convert("RGBA"), p).convert("RGB")
        
        draw = ImageDraw.Draw(img)
        
        # Get active events
        active = self.get_active_events(t)
        
        # Layout lines vertically
        y_base = H // 2 - (len(active) * 35)
        for ev in active:
            # Fade factor
            fade_in = min(1.0, (t - ev.t_start) / 0.25)
            fade_out = min(1.0, (ev.t_end - t) / 0.25)
            alpha = min(fade_in, fade_out)
            
            has_glow = alpha > 0.85 and (ev.bg_action == "glow" or ev.color == GOLD)
            
            # Main text
            display_text = ev.text_en if ev.text_en else ev.text_fr
            color = tuple(int(c * (0.4 + 0.6*alpha)) for c in ev.color)
            
            h1 = draw_text_centered(draw, display_text, y_base, ev.size, color, glow=has_glow)
            y_base += h1 + 5
            
            # Translation if both exist
            if ev.text_en and ev.text_fr:
                fr_color = tuple(int(c * (0.4 + 0.6*alpha) * 0.8) for c in GOLD)
                h2 = draw_text_centered(draw, f"({ev.text_fr})", y_base, max(ev.size-35, 28), fr_color)
                y_base += h2 + 5
            
            y_base += 15
        
        return np.array(img)


# ─── VIDEO GENERATION ──────────────────────────────────────────────────────
def generate_video(output_path, duration=215.0):
    print(f"🎬 Generating lyric video ({duration:.0f}s)...")
    renderer = FrameRenderer(W, H, FPS)
    
    def make_frame(t):
        return renderer.render(t)
    
    clip = VideoClip(make_frame, duration=duration)
    clip = clip.with_fps(FPS)
    
    # Add audio
    print("  • Loading audio...")
    try:
        if os.path.exists(AUDIO_PATH):
            audio = AudioFileClip(AUDIO_PATH)
            # Trim/pad to match duration
            if audio.duration > duration:
                audio = audio.subclipped(0, duration)
            clip = clip.with_audio(audio)
            print(f"  • Audio: {audio.duration:.1f}s")
        else:
            print(f"  ⚠️ Audio not found at: {AUDIO_PATH}")
    except Exception as e:
        print(f"  ⚠️ Audio error: {e}")
    
    # Export
    print(f"  • Exporting to {output_path}...")
    clip.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium",
        bitrate="4000k",
    )
    clip.close()
    print(f"✅ Done: {os.path.getsize(output_path)/1024/1024:.1f} MB")


# ─── PLATFORM VARIANTS ────────────────────────────────────────────────────
def gen_clip_segment(start, end, output_path):
    """Generate a segment of the full video"""
    print(f"\n📹 Segment {start:.0f}s - {end:.0f}s → {output_path}")
    renderer = FrameRenderer(W, H, FPS)
    dur = end - start
    
    def make_frame(t):
        return renderer.render(start + t)
    
    clip = VideoClip(make_frame, duration=dur).with_fps(FPS)
    
    # Add audio segment
    try:
        if os.path.exists(AUDIO_PATH):
            audio = AudioFileClip(AUDIO_PATH).subclipped(start, min(end, 215.0))
            clip = clip.with_audio(audio)
    except:
        pass
    
    clip.write_videofile(output_path, fps=FPS, codec="libx264", audio_codec="aac", 
                         threads=4, preset="medium", bitrate="4000k")
    clip.close()
    print(f"✅ {output_path}")


def gen_platform_variants():
    """Generate all platform variants"""
    dur = 215.0  # 3:35
    
    # ── YOUTUBE (16:9 full) ──
    generate_video(os.path.join(OUTPUT_DIR, "youtube_full.mp4"), dur)
    
    # ── TIKTOK SHORTS (9:16 cropped from center) ──
    # We'll do segments at 9:16 ratio
    # TikTok short 1: intro + Wolof (0:00-0:50)
    # TikTok short 2: refrain (1:34-2:05)
    # TikTok short 3: final Wolof (2:45-3:15)
    # For now, generate the full video at 9:16 aspect
    
    # ── INSTAGRAM REELS (9:16) ──
    
    # ── FACEBOOK (16:9 same as YouTube) ──
    
    # ── X/TWITTER (16:9, max 2:20) ──
    gen_clip_segment(0, 140, os.path.join(OUTPUT_DIR, "x_twitter_short.mp4"))
    
    # ── SNAPCHAT (9:16 ultra short 0:30) ──
    gen_clip_segment(0, 30, os.path.join(OUTPUT_DIR, "snapchat_ultrashort.mp4"))
    
    # ── WHATSAPP STATUS (9:16, 30s) ──
    gen_clip_segment(76.5, 106.5, os.path.join(OUTPUT_DIR, "whatsapp_status.mp4"))
    
    print("\n✅ Toutes les variantes générées !")

# ─── MAIN ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "youtube"
    
    if mode == "youtube":
        generate_video(os.path.join(OUTPUT_DIR, "youtube_full.mp4"))
    elif mode == "all":
        gen_platform_variants()
    elif mode == "segment" and len(sys.argv) >= 4:
        gen_clip_segment(float(sys.argv[2]), float(sys.argv[3]), 
                         os.path.join(OUTPUT_DIR, f"segment_{sys.argv[2]}_{sys.argv[3]}.mp4"))
    else:
        print(f"Usage: {sys.argv[0]} [youtube|all|segment start end]")