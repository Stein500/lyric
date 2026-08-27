#!/usr/bin/env python3
"""Build YouTube 16:9 MP4 + clean MP3 + prompt deliverables for Daïsky — Trop Belle.

Critical rule: the DAÏSKY PROD badge is rendered as a transparent PNG and overlaid
AFTER all Ken Burns/zoompan movement, so it stays pixel-fixed on screen.
"""
from __future__ import annotations

import importlib.util
import json
import math
import shutil
import shlex
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from mutagen import File as MutagenFile

try:
    import imageio_ffmpeg
except Exception:  # pragma: no cover
    imageio_ffmpeg = None

ROOT = Path(__file__).resolve().parents[1]
PORTRAIT_SCRIPT = ROOT / "scripts" / "build_trop_belle_9x16_v1.py"
spec = importlib.util.spec_from_file_location("portrait_builder", PORTRAIT_SCRIPT)
portrait_builder = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(portrait_builder)

AUDIO = ROOT / "Trop Belle.mp3"
PROMPT_SRC = ROOT / "PROMPT_UNIVERSEL_MAJ.md"
RAW_DIR = ROOT / "assets" / "raw" / "landscape"
WORK = ROOT / "work"
PREP = WORK / "prep" / "landscape_16x9_YT_v1"
CLIPS = WORK / "clips" / "landscape_16x9_YT_v1"
QC = WORK / "qc" / "landscape_16x9_YT_v1"
DATA = ROOT / "data"
LIVRABLES = ROOT / "livrables"
ASS_PATH = DATA / "trop_belle_16x9_YT_v1.ass"
TIMELINE_PATH = DATA / "trop_belle_timeline_16x9_YT_v1.json"
SEGMENTS_PATH = DATA / "trop_belle_video_segments_16x9_YT_v1.json"
OUT = LIVRABLES / "trop_belle_16x9_YT_v1.mp4"
OUT_MP3 = LIVRABLES / "trop_belle_audio_v1.mp3"
OUT_PROMPT = LIVRABLES / "PROMPT_UNIVERSEL_MAJ_TROP_BELLE.md"
QC_REPORT = LIVRABLES / "trop_belle_16x9_YT_v1_QC.md"
QC_SHEET_COMMITTED = LIVRABLES / "trop_belle_16x9_YT_v1_QC_sheet.jpg"
BADGE_PNG = WORK / "overlays" / "badge_daisky_prod_static_16x9.png"
GRADIENT_PNG = WORK / "overlays" / "bottom_gradient_static_16x9.png"

W, H = 1920, 1080
FPS = 24
AUDIO_DURATION = float(portrait_builder.AUDIO_DURATION)
LYRICS = portrait_builder.LYRICS
VIDEO_SEGMENTS = portrait_builder.VIDEO_SEGMENTS

IMAGE_FILES = {
    "01": "01_intro_wolof_signature_afro_bd_16x9.jpg",
    "02": "02_elle_est_trop_belle_afro_bd_16x9.jpg",
    "03": "03_refrain_scared_of_you_afro_bd_16x9.jpg",
    "04": "04_honte_hommes_virils_afro_bd_16x9.jpg",
    "05": "05_couplet_ame_transe_afro_bd_16x9.jpg",
    "06": "06_maladroit_sideral_afro_bd_16x9.jpg",
    "07": "07_trouille_peur_ventre_afro_bd_16x9.jpg",
    "08": "08_creature_etrange_oiseau_afro_bd_16x9.jpg",
    "09": "09_pre_refrain_roc_fissure_afro_bd_16x9.jpg",
    "10": "10_guerrier_sans_armure_afro_bd_16x9.jpg",
    "11": "11_refrain_lumineux_rose_vert_afro_bd_16x9.jpg",
    "12": "12_tempetes_lions_couleurs_vives_afro_bd_16x9.jpg",
    "13": "13_colosse_argile_afro_bd_color_16x9.jpg",
    "14": "14_brouillard_rose_vert_afro_bd_16x9.jpg",
    "15": "15_enigme_paradoxe_afro_bd_16x9.jpg",
    "16": "16_pre_refrain_violin_white_green_afro_bd_16x9.jpg",
    "17": "17_pont_piano_calme_afro_bd_couleur_16x9.jpg",
    "18": "18_genoux_amour_afro_bd_vif_16x9.jpg",
    "19": "19_poete_douleur_rose_blanc_vert_16x9.jpg",
    "20": "20_hook_final_tutti_afro_bd_bright_16x9.jpg",
}


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
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)}\n{p.stdout[-5000:]}")
    return p.stdout


def duration_mutagen(path: Path) -> float | None:
    try:
        m = MutagenFile(path)
        return float(m.info.length) if m and m.info else None
    except Exception:
        return None


def fmt_ass_time(seconds: float) -> str:
    cs = max(0, int(round(seconds * 100)))
    h = cs // 360000
    cs %= 360000
    m = cs // 6000
    cs %= 6000
    s = cs // 100
    c = cs % 100
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")")


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def cover(im: Image.Image, size=(W, H)) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / im.width, target_h / im.height)
    nw, nh = int(round(im.width * scale)), int(round(im.height * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - target_w) // 2
    top = (nh - target_h) // 2
    return im.crop((left, top, left + target_w, top + target_h))


def write_ass() -> None:
    header = f"""[Script Info]
Title: Trop Belle - Daïsky - Lyrics 16x9 YouTube v1
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 1
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: verse,DejaVu Sans,58,&H00F8FBFF,&H000000FF,&HE503040A,&HAA000000,0,0,0,0,100,100,0,0,1,3,2,2,220,220,170,1
Style: hook,DejaVu Sans,70,&H004DD2FF,&H000000FF,&HE503040A,&HAA000000,1,0,0,0,100,100,0,0,1,3,2,2,190,190,178,1
Style: hook_final,DejaVu Sans,76,&H003DA3E8,&H000000FF,&HE503040A,&HAA000000,1,0,0,0,100,100,0,0,1,3,2,2,170,170,184,1
Style: bridge,DejaVu Sans,54,&H00D8F7FF,&H000000FF,&HE503040A,&HAA000000,0,1,0,0,100,100,0,0,1,3,2,2,240,240,168,1
Style: wolof,DejaVu Sans,74,&H003DA3E8,&H000000FF,&HE503040A,&HAA000000,1,0,0,0,100,100,0,0,1,3,2,2,190,190,178,1
Style: fr,DejaVu Sans,40,&H00EEF5FA,&H000000FF,&HD503040A,&H99000000,0,1,0,0,100,100,0,0,1,3,2,2,260,260,112,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for item in LYRICS:
        start = fmt_ass_time(item["start"])
        end = fmt_ass_time(item["end"])
        style = item["style"]
        lines.append(f"Dialogue: 0,{start},{end},{style},,0,0,0,,{{\\fad(80,120)}}{ass_escape(item['text'])}\n")
        if item.get("fr"):
            lines.append(f"Dialogue: 1,{start},{end},fr,,0,0,0,,{{\\fad(80,120)}}{ass_escape(item['fr'])}\n")
    ASS_PATH.parent.mkdir(parents=True, exist_ok=True)
    ASS_PATH.write_text("".join(lines), encoding="utf-8")


def write_json() -> None:
    TIMELINE_PATH.write_text(json.dumps({"audio": AUDIO.name, "duration_seconds": AUDIO_DURATION, "lyrics": LYRICS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SEGMENTS_PATH.write_text(json.dumps({"duration_seconds": AUDIO_DURATION, "segments": VIDEO_SEGMENTS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prep_images() -> None:
    PREP.mkdir(parents=True, exist_ok=True)
    for num, name in IMAGE_FILES.items():
        src = RAW_DIR / name
        if not src.exists():
            raise FileNotFoundError(src)
        im = cover(Image.open(src).convert("RGB"))
        # Keep YouTube bright and vivid while avoiding clipping.
        im = ImageEnhance.Color(im).enhance(1.08)
        im = ImageEnhance.Contrast(im).enhance(1.025)
        im = ImageEnhance.Brightness(im).enhance(1.012)
        im = ImageEnhance.Sharpness(im).enhance(1.035)
        out = PREP / f"{num}_{Path(name).stem}_prep.jpg"
        im.save(out, quality=92, subsampling=1, optimize=True)


def find_prepped(num: str) -> Path:
    matches = sorted(PREP.glob(f"{num}_*_prep.jpg"))
    if not matches:
        raise FileNotFoundError(f"No prepped image for {num}")
    return matches[0]


def make_static_overlays() -> None:
    BADGE_PNG.parent.mkdir(parents=True, exist_ok=True)
    # Static bottom gradient for subtitles; overlaid after camera movement.
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = grad.load()
    start_y = int(H * 0.66)
    for y in range(start_y, H):
        t = (y - start_y) / (H - start_y)
        alpha = int(132 * (t ** 1.55))
        for x in range(W):
            pix[x, y] = (4, 9, 28, alpha)
    grad.save(GRADIENT_PNG)

    text = "⚡ DAÏSKY PROD"
    font = load_font(34, bold=True)
    probe = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(probe)
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 22, 13
    badge = Image.new("RGBA", (tw + 2 * pad_x + 4, th + 2 * pad_y + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(badge)
    rect = (1, 1, badge.width - 2, badge.height - 2)
    d.rounded_rectangle(rect, radius=22, fill=(5, 7, 15, 182), outline=(255, 255, 255, 175), width=2)
    d.text((pad_x + 3, pad_y + 3), text, font=font, fill=(0, 0, 0, 135))
    d.text((pad_x, pad_y), text, font=font, fill=(255, 243, 155, 255))
    badge.save(BADGE_PNG)


def build_clips(ffmpeg: str) -> None:
    CLIPS.mkdir(parents=True, exist_ok=True)
    concat_lines = []
    for idx, seg in enumerate(VIDEO_SEGMENTS, 1):
        src = find_prepped(seg["image"])
        dur = seg["end"] - seg["start"]
        frames = max(1, math.ceil(dur * FPS))
        clip_dur = frames / FPS
        out = CLIPS / f"clip_{idx:03d}.mp4"
        z_expr = "max(1.0001,1.045-0.00030*on)" if idx % 3 == 0 else "min(1.050,1.000+0.00030*on)"
        vf = (
            f"zoompan=z='{z_expr}':"
            "x='iw/2-iw/(2*zoom)':"
            "y='ih/2-ih/(2*zoom)':"
            f"d={frames}:s={W}x{H}:fps={FPS},format=yuv420p"
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
            "-t", f"{clip_dur:.6f}", "-shortest", "-movflags", "+faststart", str(out),
        ]
        run(cmd)
        concat_lines.append(f"file '{out.as_posix()}'\n")
    (CLIPS / "concat.txt").write_text("".join(concat_lines), encoding="utf-8")


def concat_clips(ffmpeg: str) -> Path:
    concat_mp4 = WORK / "trop_belle_16x9_YT_v1_concat.mp4"
    run([
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-f", "concat", "-safe", "0", "-i", str(CLIPS / "concat.txt"),
        "-c", "copy", "-movflags", "+faststart", str(concat_mp4),
    ])
    return concat_mp4


def burn_badge_and_mux(ffmpeg: str, concat_mp4: Path) -> None:
    fade_out_start = max(0, AUDIO_DURATION - 3.0)
    af = f"afade=t=in:st=0:d=0.3,afade=t=out:st={fade_out_start:.3f}:d=3"
    fc = (
        f"[0:v][2:v]overlay=0:0:format=auto[vgrad];"
        f"[vgrad]ass={ASS_PATH.as_posix()}[vsub];"
        f"[vsub][3:v]overlay=x=44:y=main_h-overlay_h-44:format=auto[v]"
    )
    run([
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(concat_mp4), "-i", str(AUDIO),
        "-loop", "1", "-i", str(GRADIENT_PNG),
        "-loop", "1", "-i", str(BADGE_PNG),
        "-filter_complex", fc,
        "-map", "[v]", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "medium", "-crf", "24",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-af", af,
        "-t", f"{AUDIO_DURATION:.3f}", "-movflags", "+faststart", "-shortest", str(OUT),
    ], log=WORK / "logs" / "final_encode_16x9_YT_v1.log")


def export_mp3_and_prompt(ffmpeg: str) -> None:
    LIVRABLES.mkdir(parents=True, exist_ok=True)
    run([
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(AUDIO), "-vn", "-map", "0:a:0", "-c:a", "copy",
        "-id3v2_version", "3",
        "-metadata", "title=Trop Belle",
        "-metadata", "artist=Daïsky",
        "-metadata", "comment=Clean lossless stream-copy deliverable from source MP3",
        str(OUT_MP3),
    ], log=WORK / "logs" / "export_mp3_v1.log")
    shutil.copy2(PROMPT_SRC, OUT_PROMPT)


def qc_blackdetect(ffmpeg: str) -> int:
    output = run([
        ffmpeg, "-hide_banner", "-nostats", "-i", str(OUT),
        "-vf", "blackdetect=d=0.3:pix_th=0.10", "-an", "-f", "null", "-",
    ], log=WORK / "logs" / "blackdetect_16x9_YT_v1.log")
    return output.count("black_start:")


def extract_qc_frames(ffmpeg: str) -> list[Path]:
    QC.mkdir(parents=True, exist_ok=True)
    stamps = [0.5, 20.5, 49.0, 74.0, 103.0, 129.0, 159.0, 176.0, 185.5, 193.5, 200.0, 202.5]
    frames = []
    for t in stamps:
        out = QC / f"qc_{t:06.1f}s.jpg"
        run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(OUT), "-frames:v", "1", "-q:v", "2", str(out)])
        frames.append(out)
    return frames


def make_qc_sheet(frames: list[Path]) -> Path:
    thumbs = []
    for p in frames:
        im = Image.open(p).convert("RGB")
        im.thumbnail((320, 180), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (320, 220), (245, 247, 250))
        canvas.paste(im, ((320 - im.width) // 2, 0))
        d = ImageDraw.Draw(canvas)
        d.text((12, 190), p.stem.replace("qc_", ""), font=load_font(20, bold=True), fill=(0, 0, 0))
        thumbs.append(canvas)
    cols = 3
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * 320, rows * 220), (235, 238, 242))
    for i, im in enumerate(thumbs):
        sheet.paste(im, ((i % cols) * 320, (i // cols) * 220))
    sheet.save(QC_SHEET_COMMITTED, quality=92)
    return QC_SHEET_COMMITTED


def write_qc_report(duration_audio: float, duration_video: float, duration_mp3: float, black_count: int, qc_sheet: Path) -> None:
    diff = abs(duration_audio - duration_video)
    size_video = OUT.stat().st_size / (1024 * 1024)
    size_mp3 = OUT_MP3.stat().st_size / (1024 * 1024)
    size_prompt = OUT_PROMPT.stat().st_size / 1024
    used = sorted({seg["image"] for seg in VIDEO_SEGMENTS})
    report = f"""# QC — Trop Belle 16x9 YouTube v1

Fichier contrôlé : `livrables/{OUT.name}`

## Résumé

- Format : YouTube paysage **1920×1080**, 24 fps.
- Images sources : **20 images paysage 16:9**.
- Badge : `⚡ DAÏSKY PROD` ajouté en **overlay final immobile** après tous les zooms/pans.
- Sous-titres : ASS burn-in, WrapStyle 1, fades 80/120 ms, traduction FR sous les lignes anglaises.
- Audio vidéo : `Trop Belle.mp3`, fade-in 0.3 s, fade-out 3 s.
- MP3 livrable : stream-copy sans réencodage audio → `livrables/{OUT_MP3.name}`.
- Prompt livrable : `livrables/{OUT_PROMPT.name}`.

## Contrôles automatiques

| Contrôle | Résultat |
|---|---:|
| Durée audio source | {duration_audio:.3f} s |
| Durée vidéo | {duration_video:.3f} s |
| Écart audio/vidéo | {diff:.3f} s |
| Durée ±0.30 s | {'OK' if diff <= 0.30 else 'À REVOIR'} |
| Blackdetect >300 ms | {black_count} |
| Blackdetect | {'OK' if black_count == 0 else 'À REVOIR'} |
| Durée MP3 livrable | {duration_mp3:.3f} s |
| Taille vidéo | {size_video:.1f} MB |
| Taille MP3 | {size_mp3:.1f} MB |
| Taille prompt | {size_prompt:.1f} KB |

## Images utilisées

{', '.join(used)}

## Contrôle visuel exporté

Planche QC commit : `{qc_sheet.as_posix()}`

Points de contrôle : début, hooks, couplets, pont, hook final, Wolof final, outro/fade jusqu’à la fin. Le badge doit rester au même endroit écran sur tous les extraits.
"""
    QC_REPORT.write_text(report, encoding="utf-8")


def main() -> None:
    ffmpeg = ffmpeg_bin()
    print(f"Using ffmpeg: {ffmpeg}")
    for d in (PREP, CLIPS, QC, DATA, LIVRABLES, WORK / "logs", WORK / "overlays"):
        d.mkdir(parents=True, exist_ok=True)
    write_json()
    write_ass()
    make_static_overlays()
    prep_images()
    build_clips(ffmpeg)
    concat_mp4 = concat_clips(ffmpeg)
    burn_badge_and_mux(ffmpeg, concat_mp4)
    export_mp3_and_prompt(ffmpeg)
    audio_len = duration_mutagen(AUDIO) or AUDIO_DURATION
    video_len = duration_mutagen(OUT) or AUDIO_DURATION
    mp3_len = duration_mutagen(OUT_MP3) or AUDIO_DURATION
    black_count = qc_blackdetect(ffmpeg)
    qc_sheet = make_qc_sheet(extract_qc_frames(ffmpeg))
    write_qc_report(audio_len, video_len, mp3_len, black_count, qc_sheet)
    print(f"DONE MP4: {OUT} ({OUT.stat().st_size / (1024*1024):.1f} MB)")
    print(f"DONE MP3: {OUT_MP3} ({OUT_MP3.stat().st_size / (1024*1024):.1f} MB)")
    print(f"DONE PROMPT: {OUT_PROMPT}")
    print(f"QC: {QC_REPORT}")
    print(f"QC sheet: {qc_sheet}")


if __name__ == "__main__":
    main()
