#!/usr/bin/env python3
"""
Master MP3 + 3 covers + tags ID3v2.4 + APIC + USLT — « Ça monte, ça descend » (Daïsky)
- Sans contact/email dans l'endcard (Instructions A point 4)
- Drapeau du Bénin UNIQUEMENT en cover (Instructions A point 7)
- Code 9-7-6-1 sur cover

Sorties :
  - livrables/Ca_monte_ca_descend_master_320k.mp3
  - livrables/cover_Ca_monte_ca_descend_1080x1080.jpg
  - livrables/cover_Ca_monte_ca_descend_9x16.jpg
  - livrables/cover_Ca_monte_ca_descend_16x9.jpg
"""
import json, os, subprocess
from pathlib import Path
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

# ---------- Master MP3 ----------
def make_master():
    audio = "Ça monte_ ça descend.mp3"
    # Réencode propre 320k 48k + tags via Mutagen
    out = "livrables/Ca_monte_ca_descend_master_320k.mp3"
    (ROOT / "livrables").mkdir(exist_ok=True)
    # 1) encode propre (sans tags)
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", audio,
                    "-map", "0:a:0", "-vn",
                    "-ar", "48000", "-ac", "2",
                    "-c:a", "libmp3lame", "-b:a", "320k",
                    "-write_xing", "1", out], check=True)
    # 2) Tags via Mutagen
    from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TPUB, TCOM, TCON, TDRC, USLT, APIC
    from mutagen.mp3 import MP3
    f = MP3(out, ID3=ID3)
    if f.tags is None: f.add_tags()
    f.tags.add(TIT2(encoding=3, text="Ça monte, ça descend"))
    f.tags.add(TPE1(encoding=3, text="Daïsky"))
    f.tags.add(TALB(encoding=3, text="Ça monte, ça descend"))
    f.tags.add(TPE2(encoding=3, text="Daïsky"))
    f.tags.add(TPUB(encoding=3, text="Wolof TechStein"))
    f.tags.add(TCOM(encoding=3, text="Daïsky"))
    f.tags.add(TCON(encoding=3, text="Afro-house"))
    f.tags.add(TDRC(encoding=3, text="2026"))
    # USLT = paroles nettoyées, sans timestamps
    lrc = open("Ça monte, ça descend.lrc", encoding="utf-8").read()
    import re
    lyrics = "\n".join(re.sub(r"^\[[\d:]+\.\d+\]", "", l).strip() for l in lrc.splitlines() if l.strip())
    f.tags.add(USLT(encoding=3, lang="fra", desc="", text=lyrics))
    # 3) APIC = cover carrée (générée juste après)
    cover_square = "livrables/cover_Ca_monte_ca_descend_1080x1080.jpg"
    f.tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="cover",
                    data=open(cover_square, "rb").read()))
    f.save()
    print(f"Master : {out}  taille : {os.path.getsize(out)//1024} ko")

# ---------- Covers ----------
def _font(name, size):
    for cand in [name, "/usr/share/fonts/truetype/dejavu/" + name, name.replace("ttf", "TTF")]:
        try: return ImageFont.truetype(cand, size)
        except: pass
    return ImageFont.load_default()

# Pour 16:9 paysage uniquement : on n'utilise PAS le portrait
def _load_landscape_path(idx, default_name):
    """Retourne le CHEMIN du fond paysage idx (1-6)."""
    base = ROOT / "assets/raw/landscape"
    cand = base / f"s0{idx}_{default_name}.png"
    if cand.exists():
        return cand
    files = sorted(base.glob("s*.png"))
    if 0 <= idx-1 < len(files):
        return files[idx-1]
    raise FileNotFoundError(f"Aucun fond paysage s0{idx}")

def make_cover_square():
    """Cover universelle 1080x1080 — depuis paysage s03 danse, recadré carré."""
    src = _load_landscape_path(3, "danse")
    img = Image.open(src).convert("RGB")
    W = 1080
    sw, sh = img.size
    s = min(sw, sh)
    img = img.crop(((sw-s)//2, (sh-s)//2, (sw+s)//2, (sh+s)//2)).resize((W, W), Image.LANCZOS)
    # scrim sombre
    scrim = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for y in range(0, W, 4):
        dy = abs(y - W//2)
        a = max(0, min(160, int(160 * (1 - dy / 540))))
        sd.rectangle((0, y, W, y + 4), fill=(0, 0, 0, a))
    img = Image.alpha_composite(img.convert("RGBA"), scrim)
    d = ImageDraw.Draw(img)
    # titre
    fti = _font("GreatVibes-Regular.ttf", 130) or _font("DejaVuSans-Bold.ttf", 80)
    titre = "Ça monte, ça descend"
    wt = d.textlength(titre, font=fti)
    d.text((W//2 - int(wt)//2, 380), titre, font=fti, fill=(255, 230, 180, 255))
    # artiste
    fa = _font("DejaVuSans-Bold.ttf", 48)
    artiste = "Daïsky"
    wa = d.textlength(artiste, font=fa)
    d.text((W//2 - int(wa)//2, 540), artiste, font=fa, fill=(255, 255, 255, 255))
    # code
    fc = _font("DejaVuSans-Bold.ttf", 70)
    code = "9 - 7 - 6 - 1"
    wc = d.textlength(code, font=fc)
    d.text((W//2 - int(wc)//2, 620), code, font=fc, fill=(0, 230, 255, 255))
    # badge Dsky top-left
    badge = Image.open(ROOT / "assets/overlays/badge_dsky.png").convert("RGBA")
    img.paste(badge, (40, 40), badge)
    # bandeau Bénin en bas (UNIQUEMENT en cover)
    bandeau = Image.open(ROOT / "assets/overlays/bandeau_benin.png").convert("RGBA")
    # 30 px sur 1080 de hauteur
    bandeau = bandeau.resize((W, 30), Image.LANCZOS)
    img.paste(bandeau, (0, W - 30), bandeau)
    out = "livrables/cover_Ca_monte_ca_descend_1080x1080.jpg"
    img.convert("RGB").save(out, quality=92)
    print(f"Cover carrée : {out}")
    return out

def make_cover_9x16():
    """Cover 9:16 1080x1920 — depuis s06 drop recadré verticalement."""
    src = _load_landscape_path(6, "drop")
    img = Image.open(src).convert("RGB")
    sw, sh = img.size
    # crop centre pour format vertical
    target_ratio = 1080 / 1920
    src_ratio = sw / sh
    if src_ratio > target_ratio:
        new_w = int(sh * target_ratio)
        img = img.crop(((sw - new_w)//2, 0, (sw + new_w)//2, sh))
    else:
        new_h = int(sw / target_ratio)
        img = img.crop((0, (sh - new_h)//2, sw, (sh + new_h)//2))
    img = img.resize((1080, 1920), Image.LANCZOS)
    scrim = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for y in range(0, 1920, 4):
        dy = abs(y - 960)
        a = max(0, min(160, int(160 * (1 - dy / 960))))
        sd.rectangle((0, y, 1080, y + 4), fill=(0, 0, 0, a))
    img = Image.alpha_composite(img.convert("RGBA"), scrim)
    d = ImageDraw.Draw(img)
    fti = _font("GreatVibes-Regular.ttf", 200) or _font("DejaVuSans-Bold.ttf", 130)
    titre = "Ça monte, ça descend"
    wt = d.textlength(titre, font=fti)
    d.text((540 - int(wt)//2, 700), titre, font=fti, fill=(255, 230, 180, 255))
    fa = _font("DejaVuSans-Bold.ttf", 64)
    artiste = "Daïsky"
    wa = d.textlength(artiste, font=fa)
    d.text((540 - int(wa)//2, 940), artiste, font=fa, fill=(255, 255, 255, 255))
    fc = _font("DejaVuSans-Bold.ttf", 100)
    code = "9 - 7 - 6 - 1"
    wc = d.textlength(code, font=fc)
    d.text((540 - int(wc)//2, 1060), code, font=fc, fill=(0, 230, 255, 255))
    badge = Image.open(ROOT / "assets/overlays/badge_dsky.png").convert("RGBA")
    img.paste(badge, (40, 40), badge)
    bandeau = Image.open(ROOT / "assets/overlays/bandeau_benin.png").convert("RGBA")
    bandeau = bandeau.resize((1080, 54), Image.LANCZOS)
    img.paste(bandeau, (0, 1920 - 54), bandeau)
    out = "livrables/cover_Ca_monte_ca_descend_9x16.jpg"
    img.convert("RGB").save(out, quality=92)
    print(f"Cover 9:16 : {out}")

def make_cover_16x9():
    """Cover 16:9 1920x1080 — depuis s06 drop, format paysage direct."""
    src = _load_landscape_path(6, "drop")
    img = Image.open(src).convert("RGB").resize((1920, 1080), Image.LANCZOS)
    scrim = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for y in range(0, 1080, 4):
        dy = abs(y - 540)
        a = max(0, min(160, int(160 * (1 - dy / 540))))
        sd.rectangle((0, y, 1920, y + 4), fill=(0, 0, 0, a))
    img = Image.alpha_composite(img.convert("RGBA"), scrim)
    d = ImageDraw.Draw(img)
    fti = _font("GreatVibes-Regular.ttf", 200) or _font("DejaVuSans-Bold.ttf", 130)
    titre = "Ça monte, ça descend"
    wt = d.textlength(titre, font=fti)
    d.text((960 - int(wt)//2, 300), titre, font=fti, fill=(255, 230, 180, 255))
    fa = _font("DejaVuSans-Bold.ttf", 60)
    artiste = "Daïsky"
    wa = d.textlength(artiste, font=fa)
    d.text((960 - int(wa)//2, 540), artiste, font=fa, fill=(255, 255, 255, 255))
    fc = _font("DejaVuSans-Bold.ttf", 90)
    code = "9 - 7 - 6 - 1"
    wc = d.textlength(code, font=fc)
    d.text((960 - int(wc)//2, 640), code, font=fc, fill=(0, 230, 255, 255))
    badge = Image.open(ROOT / "assets/overlays/badge_dsky.png").convert("RGBA")
    img.paste(badge, (40, 40), badge)
    bandeau = Image.open(ROOT / "assets/overlays/bandeau_benin.png").convert("RGBA")
    bandeau = bandeau.resize((1920, 30), Image.LANCZOS)
    img.paste(bandeau, (0, 1080 - 30), bandeau)
    out = "livrables/cover_Ca_monte_ca_descend_16x9.jpg"
    img.convert("RGB").save(out, quality=92)
    print(f"Cover 16:9 : {out}")

if __name__ == "__main__":
    make_cover_square()      # nécessaire d'abord (APIC du master en a besoin)
    make_cover_9x16()
    make_cover_16x9()
    make_master()
    print("\n=== Livrables ===")
    for f in sorted((ROOT / "livrables").glob("*")):
        print(f"  {f.name}  ({f.stat().st_size//1024} ko)")
