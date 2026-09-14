#!/usr/bin/env python3
"""§D.4/E.5 ID3v2.4 tags: TIT2/TPE1/TALB/TPE2/TPUB/TCOM/TCON/TDRC + TXXX + USLT + APIC.
Usage: .venv/bin/python scripts/tag_mp3.py
"""
import os, re
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TPUB, TCOM, TCON, TDRC, TXXX, USLT, APIC
from mutagen.mp3 import MP3

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MP3P = os.path.join(ROOT, "livrables", "Ayon dèkpè_master_320k.mp3")
COVER = os.path.join(ROOT, "livrables", "cover_Ayon dèkpè_1080x1080.jpg")
LRC = os.path.join(ROOT, "Ayon dèkpè.lrc")

TITLE = "Ayon dèkpè"
ARTIST = "Daïsky"
ALBUM = "Ayon dèkpè"
LABEL = "Wolof TechStein"
PRODUCER = "Wolof TechStein"
GENRE = "Afropop"
YEAR = "2026"
COMPOSER = "Wolof TechStein"

# clean lyrics (no timestamps, no [length:])
lyrics = []
for ln in open(LRC, encoding="utf-8"):
    ln = ln.strip()
    if not ln or ln.startswith("[length"):
        continue
    ln = re.sub(r"^\[\d+:\d+(?:\.\d+)?\]", "", ln).strip()
    if ln:
        lyrics.append(ln)
USLT_TEXT = "\n".join(lyrics)

tags = ID3()
tags.add(TIT2(encoding=3, text=TITLE))
tags.add(TPE1(encoding=3, text=ARTIST))
tags.add(TALB(encoding=3, text=ALBUM))
tags.add(TPE2(encoding=3, text=ARTIST))          # album artist
tags.add(TPUB(encoding=3, text=LABEL))
tags.add(TCOM(encoding=3, text=COMPOSER))
tags.add(TCON(encoding=3, text=GENRE))
tags.add(TDRC(encoding=3, text=YEAR))
tags.add(TXXX(encoding=3, desc="contact", text="+229 00 00 00 00"))
tags.add(TXXX(encoding=3, desc="email", text="contact@daïsky.com"))
tags.add(TXXX(encoding=3, desc="producer", text=PRODUCER))
tags.add(TXXX(encoding=3, desc="label", text=LABEL))
tags.add(USLT(encoding=3, lang="fre", desc="", text=USLT_TEXT))
with open(COVER, "rb") as f:
    tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="cover", data=f.read()))
tags.save(MP3P, v2_version=4)
print("tags written to", MP3P)
print("USLT chars:", len(USLT_TEXT))
