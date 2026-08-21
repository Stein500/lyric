#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean_mp3.py — DERNIÈRE ÉTAPE. Produit un MP3 « master propre » :
- supprime TOUTES les métadonnées d'origine (dont toute trace Suno :
  TXXX/COMM 'made with suno', WOAS suno.com, GEOB c2pa, TSSE, pochette 360px)
- ré-écrit des tags professionnels Daïsky + pochette 1400x1400
- vérifie par scan binaire qu'il ne reste ni 'suno' ni 'c2pa'.
Sortie : out/Héritage de mes parents - Daïsky (master propre).mp3
"""
import os, subprocess, sys
import imageio_ffmpeg
from mutagen.id3 import ID3, TIT2, TPE1, TPE2, TALB, TCON, TDRC, COMM, APIC, TPUB, TENC
from mutagen.id3 import ID3NoHeaderError

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/user/lyric/Héritage de mes parents-Daïsky.mp3"
TMP = os.path.join(ROOT, "livrables", "_tmp_sans_tags.mp3")
DST = os.path.join(ROOT, "livrables", "Héritage de mes parents - Daïsky (master propre).mp3")
POChette = os.path.join(ROOT, "livrables", "pochette_1400.jpg")

# 1) purge totale : réécriture du binaire audio sans aucun tag (audio copié, 0 ré-encodage)
subprocess.run([FFMPEG, "-y", "-i", SRC,
                "-map", "0:a", "-c:a", "copy",
                "-map_metadata", "-1", "-map_chapters", "-1",
                "-id3v2_version", "3", "-write_id3v1", "0",
                TMP], check=True, capture_output=True)

# 2) tags propres
try:
    tags = ID3(TMP)
    tags.delete()
except ID3NoHeaderError:
    pass
tags = ID3()
tags.add(TIT2(encoding=3, text="Héritage de mes parents"))
tags.add(TPE1(encoding=3, text="Daïsky"))
tags.add(TPE2(encoding=3, text="Daïsky Prod"))
tags.add(TALB(encoding=3, text="Héritage"))
tags.add(TCON(encoding=3, text="Hip-Hop/Rap"))
tags.add(TDRC(encoding=3, text="2026"))
tags.add(TPUB(encoding=3, text="Daïsky Prod"))
tags.add(TENC(encoding=3, text="TechStein"))
tags.add(COMM(encoding=3, lang="fra", desc="",
              text=("Signature : Wolof TechStein beat wê ! — "
                    "Prod : Daïsky Prod • Studio/Technologies : TechStein • "
                    "Contact : +229 01 61 16 24 08 / 01 49 11 49 51 — "
                    "techsteinsecureway@gmail.com / daiskyproduction@gmail.com — "
                    "https://linktr.ee/daiskypro")))
with open(POChette, "rb") as fp:
    tags.add(APIC(encoding=3, mime="image/jpeg", type=3,
                  desc="Cover", data=fp.read()))
tags.save(TMP, v2_version=3)
os.replace(TMP, DST)

# 3) vérification binaire
blob = open(DST, "rb").read().lower()
for mot in (b"suno", b"c2pa"):
    assert mot not in blob, f"TRACE RESTANTE: {mot}"
print("MP3 propre écrit :", DST)
print("Taille:", len(blob), "octets — aucune trace suno/c2pa ✔")
