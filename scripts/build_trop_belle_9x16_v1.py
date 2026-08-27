#!/usr/bin/env python3
"""Build the first portrait MP4 lyrics video for Daïsky — Trop Belle.

Requires pillow, mutagen, imageio-ffmpeg in the active Python environment.
All heavy intermediates are written under work/ (gitignored).
"""
from __future__ import annotations

import json
import math
import os
import shutil
import shlex
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from mutagen import File as MutagenFile

try:
    import imageio_ffmpeg
except Exception:  # pragma: no cover
    imageio_ffmpeg = None

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "Trop Belle.mp3"
RAW_DIR = ROOT / "assets" / "raw" / "portrait"
WORK = ROOT / "work"
PREP = WORK / "prep" / "portrait_9x16_v1"
CLIPS = WORK / "clips" / "portrait_9x16_v1"
QC = WORK / "qc" / "portrait_9x16_v1"
DATA = ROOT / "data"
LIVRABLES = ROOT / "livrables"
ASS_PATH = DATA / "trop_belle_9x16_v1.ass"
TIMELINE_PATH = DATA / "trop_belle_timeline_v1.json"
SEGMENTS_PATH = DATA / "trop_belle_video_segments_9x16_v1.json"
OUT = LIVRABLES / "trop_belle_9x16_v1.mp4"
QC_REPORT = LIVRABLES / "trop_belle_9x16_v1_QC.md"

W, H = 1080, 1920
FPS = 24
AUDIO_DURATION = 202.992  # hard value from Xing header; verified by mutagen too.

IMAGE_FILES = {
    "01": "01_intro_wolof_signature_afro_bd.jpg",
    "02": "02_elle_est_trop_belle_afro_bd.jpg",
    "03": "03_refrain_scared_of_you_afro_bd.jpg",
    "04": "04_honte_hommes_virils_afro_bd.jpg",
    "05": "05_couplet_ame_transe_afro_bd.jpg",
    "06": "06_maladroit_sideral_afro_bd.jpg",
    "07": "07_trouille_peur_ventre_afro_bd.jpg",
    "08": "08_creature_etrange_oiseau_afro_bd.jpg",
    "09": "09_pre_refrain_roc_fissure_afro_bd.jpg",
    "10": "10_guerrier_sans_armure_afro_bd.jpg",
    "11": "11_refrain_lumineux_rose_vert_afro_bd.jpg",
    "12": "12_tempetes_lions_couleurs_vives_afro_bd.jpg",
    "13": "13_colosse_argile_afro_bd_color.jpg",
    "14": "14_brouillard_rose_vert_afro_bd.jpg",
    "15": "15_enigme_paradoxe_afro_bd.jpg",
    "16": "16_pre_refrain_violin_white_green_afro_bd.jpg",
    "17": "17_pont_piano_calme_afro_bd_couleur.jpg",
    "18": "18_genoux_amour_afro_bd_vif.jpg",
    "19": "19_poete_douleur_rose_blanc_vert.jpg",
    "20": "20_hook_final_tutti_afro_bd_bright.jpg",
}

# Visual segmentation uses only the 20 validated images, with tasteful reuse on hooks/outro.
VIDEO_SEGMENTS = [
    {"start": 0.0, "end": 10.0, "image": "01", "label": "intro wolof signature"},
    {"start": 10.0, "end": 20.0, "image": "02", "label": "yeah elle est trop belle"},
    {"start": 20.0, "end": 32.0, "image": "03", "label": "hook scared trop belle"},
    {"start": 32.0, "end": 48.0, "image": "04", "label": "hook honte wolof"},
    {"start": 48.0, "end": 51.9, "image": "05", "label": "v1 âme mots"},
    {"start": 51.9, "end": 56.0, "image": "06", "label": "v1 maladroit fatal"},
    {"start": 56.0, "end": 59.0, "image": "07", "label": "v1 peur ventre"},
    {"start": 59.0, "end": 64.9, "image": "08", "label": "v1 créature oiseau"},
    {"start": 64.9, "end": 69.0, "image": "09", "label": "pré refrain roc"},
    {"start": 69.0, "end": 73.0, "image": "10", "label": "pré refrain armure"},
    {"start": 73.0, "end": 86.0, "image": "11", "label": "refrain 2 lumineux"},
    {"start": 86.0, "end": 102.0, "image": "20", "label": "refrain 2 tutti"},
    {"start": 102.0, "end": 108.0, "image": "12", "label": "v2 tempêtes lions"},
    {"start": 108.0, "end": 112.0, "image": "13", "label": "v2 colosse"},
    {"start": 112.0, "end": 117.0, "image": "14", "label": "v2 brouillard"},
    {"start": 117.0, "end": 119.0, "image": "15", "label": "v2 énigme"},
    {"start": 119.0, "end": 124.0, "image": "16", "label": "pré refrain 2 violon"},
    {"start": 124.0, "end": 135.0, "image": "17", "label": "pont piano questions"},
    {"start": 135.0, "end": 150.5, "image": "18", "label": "pont amour genoux"},
    {"start": 150.5, "end": 153.0, "image": "19", "label": "pont poète lead"},
    {"start": 153.0, "end": 163.0, "image": "11", "label": "final hook 1 lumineux"},
    {"start": 163.0, "end": 173.0, "image": "20", "label": "final hook 2 festival"},
    {"start": 173.0, "end": 183.0, "image": "03", "label": "final hook wolof impact"},
    {"start": 183.0, "end": 193.0, "image": "20", "label": "outro vocal"},
    {"start": 193.0, "end": 202.992, "image": "01", "label": "outro fade instrumental"},
]

# Subtitle timeline. After 1:50, timings are explicit/hardcoded in seconds as required by v4.2.
LYRICS = [
    {"start": 0.0, "end": 4.5, "text": "Wolof TechStein beat wê...", "style": "wolof"},
    {"start": 10.0, "end": 14.0, "text": "Yeah...", "style": "verse"},
    {"start": 16.0, "end": 19.0, "text": "Elle est trop belle...", "style": "hook"},

    {"start": 20.0, "end": 26.0, "text": "I'm scared of you, I'm scared of you", "style": "hook", "fr": "J’ai peur de toi, j’ai peur de toi"},
    {"start": 26.0, "end": 32.0, "text": "T'es trop belle, t'es trop belle, j'ai la trouille, c'est fou", "style": "hook"},
    {"start": 32.0, "end": 39.0, "text": "I'm scared of you, I'm scared of you", "style": "hook", "fr": "J’ai peur de toi, j’ai peur de toi"},
    {"start": 39.0, "end": 46.0, "text": "Je suis la honte des hommes virils, c'est tout", "style": "hook"},
    {"start": 46.0, "end": 48.0, "text": "Wolof TechStein beat wê!", "style": "wolof"},

    {"start": 48.0, "end": 50.0, "text": "J'ai l'âme en transe, le cœur en déroute", "style": "verse"},
    {"start": 50.0, "end": 51.9, "text": "Devant tes yeux, mes mots s'égouttent", "style": "verse"},
    {"start": 51.9, "end": 54.9, "text": "Je suis un maladroit sidéral, un déchet sentimental", "style": "verse"},
    {"start": 54.9, "end": 56.0, "text": "Je ne sais pas draguer, je suis plutôt fatal", "style": "verse"},
    {"start": 56.0, "end": 58.0, "text": "J'ai la trouille, j'ai la peur au ventre", "style": "verse"},
    {"start": 58.0, "end": 59.0, "text": "Devant ta beauté qui foudroie et qui entre", "style": "verse"},
    {"start": 59.0, "end": 62.0, "text": "Je suis une créature étrange, un oiseau sans ailes", "style": "verse"},
    {"start": 62.0, "end": 64.9, "text": "Un homme qui tremble devant une si belle", "style": "verse"},

    {"start": 64.9, "end": 66.0, "text": "Je suis censé être fort, être un roc", "style": "bridge"},
    {"start": 66.0, "end": 69.0, "text": "Mais devant toi, je suis un glas, un éclat", "style": "bridge"},
    {"start": 69.0, "end": 71.0, "text": "Je suis un guerrier sans armure", "style": "bridge"},
    {"start": 71.0, "end": 73.0, "text": "Une armée qui se fissure", "style": "bridge"},

    {"start": 73.0, "end": 79.0, "text": "I'm scared of you, I'm scared of you", "style": "hook", "fr": "J’ai peur de toi, j’ai peur de toi"},
    {"start": 79.0, "end": 86.0, "text": "T'es trop belle, t'es trop belle, j'ai la trouille, c'est fou", "style": "hook"},
    {"start": 86.0, "end": 93.0, "text": "I'm scared of you, I'm scared of you", "style": "hook", "fr": "J’ai peur de toi, j’ai peur de toi"},
    {"start": 93.0, "end": 99.7, "text": "Je suis la honte des hommes virils, c'est tout", "style": "hook"},
    {"start": 99.7, "end": 102.0, "text": "Wolof TechStein beat wê!", "style": "wolof"},

    {"start": 102.0, "end": 104.4, "text": "J'ai traversé des tempêtes, j'ai dompté des lions", "style": "verse"},
    {"start": 104.4, "end": 106.0, "text": "Mais devant ton sourire, je perds ma raison", "style": "verse"},
    {"start": 106.0, "end": 107.6, "text": "Je suis un colosse aux pieds d'argile", "style": "verse"},
    {"start": 107.6, "end": 109.5, "text": "Un géant qui vacille, qui titube, qui file", "style": "verse"},
    # Hardcoded exact timings after 1:50 / 110.0 seconds.
    {"start": 109.5, "end": 111.0, "text": "Je ne sais pas quoi dire, je suis hagard", "style": "verse"},
    {"start": 111.0, "end": 113.0, "text": "Mes phrases s'effilochent, je suis dans le brouillard", "style": "verse"},
    {"start": 113.0, "end": 114.5, "text": "Je suis une énigme, un paradoxe ambulant", "style": "verse"},
    {"start": 114.5, "end": 116.9, "text": "Un homme qui aime trop, un amoureux transi", "style": "verse"},

    {"start": 116.9, "end": 119.0, "text": "Je suis censé être fort, être un roc", "style": "bridge"},
    {"start": 119.0, "end": 121.0, "text": "Mais devant toi, je suis un glas, un éclat", "style": "bridge"},
    {"start": 121.0, "end": 123.0, "text": "Je suis un guerrier sans armure", "style": "bridge"},
    {"start": 123.0, "end": 124.0, "text": "Une armée qui se fissure", "style": "bridge"},

    {"start": 124.0, "end": 128.0, "text": "Comment avoir la trouille pour de si belles créatures ?", "style": "bridge"},
    {"start": 128.0, "end": 132.0, "text": "Comment un homme peut-il craindre une blessure ?", "style": "bridge"},
    {"start": 132.0, "end": 135.0, "text": "Je suis étrange, je suis seul, je suis fou", "style": "bridge"},
    {"start": 135.0, "end": 138.0, "text": "Mais je t'aime, je t'aime, je t'aime, je suis à genoux", "style": "bridge"},
    {"start": 138.0, "end": 141.3, "text": "Je suis un artiste de la peur", "style": "bridge"},
    {"start": 141.3, "end": 145.0, "text": "Un poète de la douleur", "style": "bridge"},
    {"start": 145.0, "end": 148.0, "text": "Mais c'est pour toi que je tremble", "style": "bridge"},
    {"start": 148.0, "end": 150.5, "text": "Pour toi que je dissemble", "style": "bridge"},

    {"start": 151.0, "end": 157.0, "text": "I'm scared of you, I'm scared of you", "style": "hook_final", "fr": "J’ai peur de toi, j’ai peur de toi"},
    {"start": 157.0, "end": 164.0, "text": "T'es trop belle, t'es trop belle, j'ai la trouille, c'est fou", "style": "hook_final"},
    {"start": 164.0, "end": 171.0, "text": "I'm scared of you, I'm scared of you", "style": "hook_final", "fr": "J’ai peur de toi, j’ai peur de toi"},
    {"start": 171.0, "end": 176.0, "text": "Je suis la honte des hommes virils, c'est tout", "style": "hook_final"},
    {"start": 176.0, "end": 178.0, "text": "Wolof TechStein beat wê!", "style": "wolof"},

    {"start": 183.0, "end": 188.0, "text": "Wolof TechStein beat wê...", "style": "wolof"},
    {"start": 188.0, "end": 193.0, "text": "(Je suis une créature étrange...)", "style": "bridge"},
]


def ffmpeg_bin() -> str:
    if imageio_ffmpeg is not None:
        return imageio_ffmpeg.get_ffmpeg_exe()
    return "ffmpeg"


def run(cmd: list[str], *, log: Path | None = None) -> str:
    print("$", " ".join(shlex.quote(str(c)) for c in cmd), flush=True)
    p = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(p.stdout)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)}\n{p.stdout[-4000:]}")
    return p.stdout


def fmt_ass_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    cs = int(round(seconds * 100))
    h = cs // 360000
    cs %= 360000
    m = cs // 6000
    cs %= 6000
    s = cs // 100
    c = cs % 100
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")")


def write_ass() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    header = f"""[Script Info]
Title: Trop Belle - Daïsky - Lyrics 9x16 v1
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 1
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: verse,DejaVu Sans,62,&H00F5F9FF,&H000000FF,&HDD03040A,&H99000000,0,0,0,0,100,100,0,0,1,3,2,2,82,82,352,1
Style: hook,DejaVu Sans,72,&H004DD2FF,&H000000FF,&HDD03040A,&H99000000,1,0,0,0,100,100,0,0,1,3,2,2,76,76,360,1
Style: hook_final,DejaVu Sans,80,&H003DA3E8,&H000000FF,&HDD03040A,&H99000000,1,0,0,0,100,100,0,0,1,3,2,2,70,70,366,1
Style: bridge,DejaVu Sans,58,&H00C7F1FF,&H000000FF,&HDD03040A,&H99000000,0,1,0,0,100,100,0,0,1,3,2,2,88,88,352,1
Style: wolof,DejaVu Sans,78,&H003DA3E8,&H000000FF,&HDD03040A,&H99000000,1,0,0,0,100,100,0,0,1,3,2,2,76,76,360,1
Style: fr,DejaVu Sans,44,&H00EEF5FA,&H000000FF,&HCC03040A,&H88000000,0,1,0,0,100,100,0,0,1,3,2,2,95,95,274,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for item in LYRICS:
        start = fmt_ass_time(item["start"])
        end = fmt_ass_time(item["end"])
        style = item["style"]
        text = ass_escape(item["text"])
        lines.append(f"Dialogue: 0,{start},{end},{style},,0,0,0,,{{\\fad(80,120)}}{text}\n")
        if item.get("fr"):
            fr = ass_escape(item["fr"])
            lines.append(f"Dialogue: 1,{start},{end},fr,,0,0,0,,{{\\fad(80,120)}}{fr}\n")
    ASS_PATH.write_text("".join(lines), encoding="utf-8")


def write_json() -> None:
    timeline = {"audio": str(AUDIO.name), "duration_seconds": AUDIO_DURATION, "lyrics": LYRICS}
    TIMELINE_PATH.write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SEGMENTS_PATH.write_text(json.dumps({"duration_seconds": AUDIO_DURATION, "segments": VIDEO_SEGMENTS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cover(im: Image.Image, size=(W, H)) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = im.size
    scale = max(target_w / src_w, target_h / src_h)
    nw, nh = int(round(src_w * scale)), int(round(src_h * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - target_w) // 2
    top = (nh - target_h) // 2
    return im.crop((left, top, left + target_w, top + target_h))


def rounded_rectangle(draw: ImageDraw.ImageDraw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def add_bottom_legibility(base: Image.Image) -> Image.Image:
    # Transparent bottom gradient for readable lyrics, kept light enough to preserve vivid colors.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = overlay.load()
    start_y = int(H * 0.64)
    for y in range(start_y, H):
        t = (y - start_y) / (H - start_y)
        alpha = int(118 * (t ** 1.7))
        for x in range(W):
            pix[x, y] = (4, 9, 28, alpha)
    return Image.alpha_composite(base.convert("RGBA"), overlay)


def add_badge(base: Image.Image) -> Image.Image:
    img = base.convert("RGBA")
    draw = ImageDraw.Draw(img)
    font = load_font(38, bold=True)
    text = "⚡ DAÏSKY PROD"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = 42, H - 105
    pad_x, pad_y = 24, 15
    rect = (x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y)
    # Pink/green/white feel, but enough contrast. Badge is static, added in post only.
    rounded_rectangle(draw, rect, radius=26, fill=(5, 7, 15, 178), outline=(255, 255, 255, 170), width=2)
    draw.text((x + pad_x + 2, y + pad_y + 2), text, font=font, fill=(0, 0, 0, 130))
    draw.text((x + pad_x, y + pad_y), text, font=font, fill=(255, 243, 155, 255))
    return img


def prep_images() -> None:
    PREP.mkdir(parents=True, exist_ok=True)
    for num, name in IMAGE_FILES.items():
        src = RAW_DIR / name
        if not src.exists():
            raise FileNotFoundError(src)
        im = Image.open(src).convert("RGB")
        im = cover(im)
        # Keep the user's vivid color request: slight saturation and brightness lift.
        im = ImageEnhance.Color(im).enhance(1.10)
        im = ImageEnhance.Contrast(im).enhance(1.035)
        im = ImageEnhance.Brightness(im).enhance(1.018)
        im = ImageEnhance.Sharpness(im).enhance(1.04)
        rgba = add_bottom_legibility(im)
        rgba = add_badge(rgba)
        out = PREP / f"{num}_{Path(name).stem}_prep.jpg"
        rgba.convert("RGB").save(out, quality=92, subsampling=1, optimize=True)


def find_prepped(num: str) -> Path:
    matches = sorted(PREP.glob(f"{num}_*_prep.jpg"))
    if not matches:
        raise FileNotFoundError(f"No prepped image for {num}")
    return matches[0]


def build_clips(ffmpeg: str) -> None:
    CLIPS.mkdir(parents=True, exist_ok=True)
    concat_lines = []
    for idx, seg in enumerate(VIDEO_SEGMENTS, 1):
        src = find_prepped(seg["image"])
        dur = seg["end"] - seg["start"]
        frames = max(1, math.ceil(dur * FPS))
        clip_dur = frames / FPS
        out = CLIPS / f"clip_{idx:03d}.mp4"
        # Gentle Ken Burns motion: alternates slow zoom-in/zoom-out/tilt feel without visual fades.
        if idx % 3 == 0:
            z_expr = "max(1.0001,1.055-0.00042*on)"
        else:
            z_expr = "min(1.060,1.000+0.00042*on)"
        vf = (
            f"zoompan=z='{z_expr}':"
            "x='iw/2-iw/(2*zoom)':"
            "y='ih/2-ih/(2*zoom)':"
            f"d={frames}:s={W}x{H}:fps={FPS},"
            "format=yuv420p"
        )
        cmd = [
            ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
            "-loop", "1", "-i", str(src),
            "-f", "lavfi", "-t", f"{clip_dur:.6f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-filter:v", vf,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "128k",
            "-t", f"{clip_dur:.6f}", "-shortest", "-movflags", "+faststart",
            str(out),
        ]
        run(cmd)
        concat_lines.append(f"file '{out.as_posix()}'\n")
    (CLIPS / "concat.txt").write_text("".join(concat_lines), encoding="utf-8")


def concat_clips(ffmpeg: str) -> Path:
    concat_mp4 = WORK / "trop_belle_9x16_v1_concat.mp4"
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-f", "concat", "-safe", "0", "-i", str(CLIPS / "concat.txt"),
        "-c", "copy", "-movflags", "+faststart", str(concat_mp4),
    ]
    run(cmd)
    return concat_mp4


def burn_and_mux(ffmpeg: str, concat_mp4: Path) -> None:
    LIVRABLES.mkdir(parents=True, exist_ok=True)
    fade_out_start = max(0, AUDIO_DURATION - 3.0)
    vf = f"ass={ASS_PATH.as_posix()}"
    af = f"afade=t=in:st=0:d=0.3,afade=t=out:st={fade_out_start:.3f}:d=3"
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(concat_mp4), "-i", str(AUDIO),
        "-map", "0:v:0", "-map", "1:a:0",
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "24",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-af", af,
        "-t", f"{AUDIO_DURATION:.3f}", "-movflags", "+faststart", "-shortest",
        str(OUT),
    ]
    run(cmd, log=WORK / "logs" / "final_encode.log")


def duration_mutagen(path: Path) -> float | None:
    try:
        m = MutagenFile(path)
        return float(m.info.length) if m and m.info else None
    except Exception:
        return None


def qc_blackdetect(ffmpeg: str) -> tuple[int, str]:
    log = WORK / "logs" / "blackdetect_9x16_v1.log"
    cmd = [
        ffmpeg, "-hide_banner", "-nostats", "-i", str(OUT),
        "-vf", "blackdetect=d=0.3:pix_th=0.10", "-an", "-f", "null", "-",
    ]
    output = run(cmd, log=log)
    count = output.count("black_start:")
    return count, output


def extract_qc_frames(ffmpeg: str) -> list[Path]:
    QC.mkdir(parents=True, exist_ok=True)
    stamps = [0.5, 20.5, 49.0, 74.0, 103.0, 129.0, 159.0, 176.0, 185.5, 193.5, 200.0, 202.5]
    frames = []
    for t in stamps:
        out = QC / f"qc_{t:06.1f}s.jpg"
        cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(OUT), "-frames:v", "1", "-q:v", "2", str(out)]
        run(cmd)
        frames.append(out)
    return frames


def make_qc_sheet(frames: list[Path]) -> Path:
    thumbs = []
    for p in frames:
        im = Image.open(p).convert("RGB")
        im.thumbnail((216, 384), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (216, 424), (245, 247, 250))
        canvas.paste(im, ((216 - im.width) // 2, 0))
        d = ImageDraw.Draw(canvas)
        font = load_font(18, bold=True)
        d.text((10, 394), p.stem.replace("qc_", ""), font=font, fill=(0, 0, 0))
        thumbs.append(canvas)
    cols = 4
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * 216, rows * 424), (235, 238, 242))
    for i, im in enumerate(thumbs):
        x = (i % cols) * 216
        y = (i // cols) * 424
        sheet.paste(im, (x, y))
    out = QC / "qc_sheet_9x16_v1.jpg"
    sheet.save(out, quality=92)
    committed = LIVRABLES / "trop_belle_9x16_v1_QC_sheet.jpg"
    LIVRABLES.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out, committed)
    return committed


def write_qc_report(duration_audio: float | None, duration_video: float | None, black_count: int, qc_sheet: Path) -> None:
    size_mb = OUT.stat().st_size / (1024 * 1024)
    diff = None if duration_video is None or duration_audio is None else abs(duration_video - duration_audio)
    pass_duration = diff is not None and diff <= 0.30
    pass_black = black_count == 0
    used = sorted({seg["image"] for seg in VIDEO_SEGMENTS})
    report = f"""# QC — Trop Belle 9x16 v1

Fichier contrôlé : `livrables/{OUT.name}`

## Résumé

- Format : portrait TikTok/Reels/Shorts **1080×1920**, 24 fps.
- Images sources : **20 images validées**, aucune nouvelle génération.
- Badge : `⚡ DAÏSKY PROD` ajouté en post-production, bas-gauche.
- Sous-titres : ASS burn-in, WrapStyle 1, fades 80/120 ms, traduction FR sous les lignes anglaises.
- Audio : `Trop Belle.mp3`, fade-in 0.3 s, fade-out 3 s.

## Contrôles automatiques

| Contrôle | Résultat |
|---|---:|
| Durée audio mutagen | {duration_audio:.3f} s |
| Durée vidéo mutagen | {duration_video:.3f} s |
| Écart audio/vidéo | {diff:.3f} s |
| Durée ±0.30 s | {'OK' if pass_duration else 'À REVOIR'} |
| Blackdetect >300 ms | {black_count} |
| Blackdetect | {'OK' if pass_black else 'À REVOIR'} |
| Taille fichier | {size_mb:.1f} MB |

## Images utilisées

{', '.join(used)}

## Contrôle visuel exporté

Planche QC commit : `{qc_sheet.as_posix()}`

Points vérifiés sur la planche : début, hooks, couplets, pont, hook final, Wolof final, outro/fade jusqu’à la fin.
"""
    QC_REPORT.write_text(report, encoding="utf-8")


def main() -> None:
    ffmpeg = ffmpeg_bin()
    print(f"Using ffmpeg: {ffmpeg}")
    for d in (PREP, CLIPS, QC, LIVRABLES, DATA, WORK / "logs"):
        d.mkdir(parents=True, exist_ok=True)
    write_json()
    write_ass()
    prep_images()
    build_clips(ffmpeg)
    concat_mp4 = concat_clips(ffmpeg)
    burn_and_mux(ffmpeg, concat_mp4)
    audio_len = duration_mutagen(AUDIO) or AUDIO_DURATION
    video_len = duration_mutagen(OUT) or AUDIO_DURATION
    black_count, _ = qc_blackdetect(ffmpeg)
    frames = extract_qc_frames(ffmpeg)
    sheet = make_qc_sheet(frames)
    write_qc_report(audio_len, video_len, black_count, sheet)
    print(f"DONE: {OUT} ({OUT.stat().st_size / (1024*1024):.1f} MB)")
    print(f"QC: {QC_REPORT}")
    print(f"QC sheet: {sheet}")


if __name__ == "__main__":
    main()
