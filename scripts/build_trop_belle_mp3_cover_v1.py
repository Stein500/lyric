#!/usr/bin/env python3
"""Create dedicated cover artwork and embed it into the Trop Belle MP3 deliverable."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from mutagen import File as MutagenFile
from mutagen.id3 import APIC, ID3, TALB, TCON, TIT2, TPE1, TPE2, COMM, TDRC

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MP3 = ROOT / "Trop Belle.mp3"
RAW_COVER = ROOT / "assets" / "raw" / "cover" / "trop_belle_cover_raw_afro_bd.jpg"
LIVRABLES = ROOT / "livrables"
COVER_JPG = LIVRABLES / "trop_belle_cover_v1.jpg"
MP3_OUT = LIVRABLES / "trop_belle_audio_cover_v1.mp3"
QC_JSON = LIVRABLES / "trop_belle_audio_cover_v1_QC.json"
QC_MD = LIVRABLES / "trop_belle_audio_cover_v1_QC.md"
PROMPT_SRC = ROOT / "PROMPT_UNIVERSEL_MAJ.md"
PROMPT_OUT = LIVRABLES / "PROMPT_UNIVERSEL_MAJ_TROP_BELLE.md"

SIZE = 1600


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def cover_crop(im: Image.Image, size: int = SIZE) -> Image.Image:
    scale = max(size / im.width, size / im.height)
    nw, nh = round(im.width * scale), round(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - size) // 2
    top = (nh - size) // 2
    return im.crop((left, top, left + size, top + size))


def draw_centered(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill, stroke_fill, stroke_width=2) -> int:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (SIZE - tw) // 2
    draw.text((x, y), text, font=font, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width)
    return y + th


def build_cover() -> None:
    LIVRABLES.mkdir(parents=True, exist_ok=True)
    im = Image.open(RAW_COVER).convert("RGB")
    im = cover_crop(im)
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = ImageEnhance.Sharpness(im).enhance(1.06)
    rgba = im.convert("RGBA")

    # Top and bottom soft overlays for clean readable post typography.
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    pix = overlay.load()
    for y in range(SIZE):
        top_alpha = max(0, int(150 * (1 - y / 520))) if y < 520 else 0
        bottom_alpha = max(0, int(205 * ((y - 900) / 700) ** 1.35)) if y > 900 else 0
        alpha = max(top_alpha, bottom_alpha)
        if alpha:
            for x in range(SIZE):
                pix[x, y] = (3, 5, 20, alpha)
    rgba = Image.alpha_composite(rgba, overlay)

    # Subtle border and glow, no AI text: all typography is added here.
    d = ImageDraw.Draw(rgba)
    d.rounded_rectangle((38, 38, SIZE - 38, SIZE - 38), radius=48, outline=(255, 255, 255, 170), width=4)
    d.rounded_rectangle((54, 54, SIZE - 54, SIZE - 54), radius=38, outline=(77, 210, 255, 100), width=3)

    artist_font = load_font(92, bold=True)
    title_font = load_font(182, bold=True)
    sub_font = load_font(54, bold=True)
    sig_font = load_font(46, bold=True)

    draw_centered(d, 92, "DAÏSKY", artist_font, (255, 255, 255, 255), (4, 6, 20, 240), 4)

    # Bottom title block with a translucent rounded capsule.
    d.rounded_rectangle((110, 1120, SIZE - 110, 1488), radius=56, fill=(5, 7, 18, 150), outline=(255, 236, 160, 145), width=3)
    draw_centered(d, 1142, "TROP BELLE", title_font, (255, 243, 248, 255), (5, 6, 18, 255), 5)
    draw_centered(d, 1334, "I'M SCARED OF YOU", sub_font, (77, 210, 255, 255), (5, 6, 18, 250), 3)
    draw_centered(d, 1414, "Wolof TechStein beat wê", sig_font, (255, 214, 108, 255), (5, 6, 18, 245), 3)

    rgba.convert("RGB").save(COVER_JPG, quality=92, subsampling=1, optimize=True)


def embed_cover() -> dict:
    shutil.copy2(SOURCE_MP3, MP3_OUT)
    audio = MutagenFile(MP3_OUT)
    duration = float(audio.info.length) if audio and audio.info else None

    try:
        tags = ID3(MP3_OUT)
    except Exception:
        tags = ID3()
    tags.delall("APIC")
    tags.delall("TIT2")
    tags.delall("TPE1")
    tags.delall("TPE2")
    tags.delall("TALB")
    tags.delall("TCON")
    tags.delall("COMM")
    tags.delall("TDRC")
    tags.add(TIT2(encoding=3, text="Trop Belle"))
    tags.add(TPE1(encoding=3, text="Daïsky"))
    tags.add(TPE2(encoding=3, text="Daïsky Prod / TechStein"))
    tags.add(TALB(encoding=3, text="Trop Belle"))
    tags.add(TCON(encoding=3, text="Afro trap / Lyrics"))
    tags.add(TDRC(encoding=3, text="2026"))
    tags.add(COMM(encoding=3, lang="fre", desc="", text="Wolof TechStein beat wê"))
    tags.add(APIC(
        encoding=3,
        mime="image/jpeg",
        type=3,
        desc="Cover Trop Belle",
        data=COVER_JPG.read_bytes(),
    ))
    tags.save(MP3_OUT, v2_version=3)

    checked = ID3(MP3_OUT)
    apics = checked.getall("APIC")
    audio2 = MutagenFile(MP3_OUT)
    return {
        "source_mp3": str(SOURCE_MP3.relative_to(ROOT)),
        "output_mp3": str(MP3_OUT.relative_to(ROOT)),
        "cover": str(COVER_JPG.relative_to(ROOT)),
        "duration_source_seconds": duration,
        "duration_output_seconds": float(audio2.info.length) if audio2 and audio2.info else None,
        "cover_count": len(apics),
        "cover_mime": apics[0].mime if apics else None,
        "cover_bytes": len(apics[0].data) if apics else 0,
        "mp3_bytes": MP3_OUT.stat().st_size,
        "cover_file_bytes": COVER_JPG.stat().st_size,
    }


def write_qc(qc: dict) -> None:
    QC_JSON.write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dur_diff = abs((qc["duration_source_seconds"] or 0) - (qc["duration_output_seconds"] or 0))
    md = f"""# QC — MP3 avec cover — Trop Belle v1

Fichier contrôlé : `{qc['output_mp3']}`

## Résumé

- Cover dédiée : `{qc['cover']}`
- Cover style : animation conte familial originale + BD africaine, couleurs vives rose/blanc/vert/cyan/or.
- MP3 : copie de la source audio avec tags ID3 propres + pochette APIC intégrée.
- Audio non réencodé : oui, copie du MP3 source puis écriture des tags.
- Prompt livrable mis à jour : `livrables/PROMPT_UNIVERSEL_MAJ_TROP_BELLE.md`

## Contrôles

| Contrôle | Résultat |
|---|---:|
| Durée source | {qc['duration_source_seconds']:.3f} s |
| Durée MP3 cover | {qc['duration_output_seconds']:.3f} s |
| Écart durée | {dur_diff:.3f} s |
| Durée OK ±0.30 s | {'OK' if dur_diff <= 0.30 else 'À REVOIR'} |
| Nombre de covers ID3/APIC | {qc['cover_count']} |
| MIME cover | {qc['cover_mime']} |
| Taille image cover intégrée | {qc['cover_bytes'] / 1024:.1f} KB |
| Taille fichier cover JPG | {qc['cover_file_bytes'] / 1024:.1f} KB |
| Taille MP3 avec cover | {qc['mp3_bytes'] / (1024*1024):.1f} MB |
"""
    QC_MD.write_text(md, encoding="utf-8")


def main() -> None:
    build_cover()
    qc = embed_cover()
    shutil.copy2(PROMPT_SRC, PROMPT_OUT)
    write_qc(qc)
    print(json.dumps(qc, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
