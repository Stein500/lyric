#!/usr/bin/env python3
"""
🎧 BUILD MP3 PROPRE — Lightning Is My Name (Daïsky)
- Conversion m4a → MP3 320kbps CBR
- Suppression totale des métadonnées Suno / C2PA
- Tags ID3v2.4 propres + cover pro embarquée
- Export: livrables/Daïsky - Lightning Is My Name.mp3
"""
import subprocess, os
from pathlib import Path
from PIL import Image
import tempfile

ROOT = Path("/home/user/lyric")
try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    import shutil as _sh
    FFMPEG = _sh.which("ffmpeg") or "ffmpeg"
SRC = ROOT/"Lightning_is_my_name_Daïsky.m4a"
COVER = ROOT/"assets/cover/cover_Lightning_pro.jpg"
OUT = ROOT/"livrables"
OUT.mkdir(parents=True, exist_ok=True)
FINAL = OUT/"Daïsky - Lightning Is My Name.mp3"

DURATION = 169.486

# Étape 1 : convertir en MP3 320kbps, sans métadonnées
tmp_mp3 = ROOT/"work"/"_clean_raw.mp3"
tmp_mp3.parent.mkdir(parents=True, exist_ok=True)
cmd = [
    FFMPEG, "-y", "-loglevel", "error",
    "-i", str(SRC),
    "-vn",                    # no video stream from source
    "-c:a", "libmp3lame",
    "-b:a", "320k",
    "-ar", "44100",
    "-ac", "2",
    "-af", f"afade=t=in:st=0:d=0.3,afade=t=out:st={DURATION-3}:d=3",
    "-map_metadata", "-1",    # ⚠️ SUPPRIME TOUTES LES MÉTADONNÉES (suno / c2pa)
    "-id3v2_version", "3",
    "-write_id3v1", "1",
    "-t", str(DURATION),
    str(tmp_mp3)
]
print("🔊 Encodage MP3 320kbps, suppression métadonnées Suno...")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("ERREUR:", r.stderr[-1000:]); raise SystemExit(1)
print(f"  ✅ {tmp_mp3.stat().st_size/1e6:.1f} MB")

# Étape 2 : tags ID3 propres + cover embarquée avec mutagen
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, TPUB, TPE2, COMM, APIC, TRCK, TPOS, TSSE, TXXX
from mutagen.mp3 import MP3

audio = MP3(str(tmp_mp3), ID3=ID3)
audio.delete()  # reset tags

# Tags de base
audio["TIT2"] = TIT2(encoding=3, text="Lightning Is My Name")
audio["TPE1"] = TPE1(encoding=3, text="Daïsky")
audio["TPE2"] = TPE2(encoding=3, text="Daïsky")          # Album Artist
audio["TALB"] = TALB(encoding=3, text="Lightning Is My Name — Single")
audio["TDRC"] = TDRC(encoding=3, text="2026")
audio["TCON"] = TCON(encoding=3, text="Hip-Hop / Rap / Trap")
audio["TRCK"] = TRCK(encoding=3, text="1")
audio["TPOS"] = TPOS(encoding=3, text="1")
audio["TPUB"] = TPUB(encoding=3, text="Daïsky Prod")
audio["COMM"] = COMM(encoding=3, lang="eng", desc="Comment",
                     text="Daïsky Prod / TechStein. Wolof TechStein beat wê !")
# Custom tags (TXXX) — assignation directe par clé
audio["TXXX:PRODUCER"] = TXXX(encoding=3, desc="PRODUCER", text="Daïsky Prod")
audio["TXXX:STUDIO"] = TXXX(encoding=3, desc="STUDIO", text="TechStein")
audio["TXXX:CONTACT"] = TXXX(encoding=3, desc="CONTACT", text="techsteinsecureway@gmail.com")
audio["TXXX:LINKTREE"] = TXXX(encoding=3, desc="LINKTREE", text="https://linktr.ee/daiskypro")

# Cover
with open(COVER, "rb") as f:
    cover_data = f.read()
audio["APIC"] = APIC(
    encoding=3,
    mime="image/jpeg",
    type=3,  # Cover (front)
    desc="Cover",
    data=cover_data,
)
# Forcer TSSE (encoder) neutre (on enlève toute empreinte LAME/suno)
audio["TSSE"] = TSSE(encoding=3, text="LAME399.5+")

audio.save(v2_version=3, v1=2)
print(f"  ✅ Tags ID3 + cover ajoutés")

# Étape 3 : déplacer au nom final
import shutil
shutil.move(str(tmp_mp3), str(FINAL))
print(f"\n✅ MP3 FINAL : {FINAL}")
print(f"   Taille : {FINAL.stat().st_size/1e6:.1f} MB")
print(f"   Bitrate attendu : 320 kbps CBR")
print(f"   Durée attendue  : ~{DURATION:.2f}s (avec fades)")

# Vérification
v = MP3(str(FINAL), ID3=ID3)
print(f"\n🔍 Vérification tags:")
for k in ["TIT2","TPE1","TALB","TCON","TPUB"]:
    if k in v: print(f"  {k}: {v[k].text[0]}")
apic_keys = [k for k in v.tags.keys() if k.startswith("APIC")]
for ak in apic_keys:
    print(f"  {ak} (cover): {len(v[ak].data)/1e3:.0f} KB")
print(f"  Durée: {v.info.length:.2f}s  |  Bitrate: {v.info.bitrate//1000} kbps")
print(f"  Taille fichier: {FINAL.stat().st_size/1e6:.2f} MB")
