from __future__ import annotations

import shutil
from pathlib import Path

from mutagen.id3 import APIC, COMM, ID3, TALB, TCON, TDRC, TENC, TIT2, TPE1, TPE2, TPUB

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "mama-tche"
SRC_MP3 = ROOT / "Mama_tche_Daïsky.mp3"
OUT_MP3 = PROJECT / "livrables" / "Mama_tche_Daïsky_clean.mp3"
COVER = PROJECT / "livrables" / "pochette_Mama_tche_Daïsky_1400.jpg"

TITLE = "Mama tché"
ARTIST = "Daïsky"
PROD = "Daïsky Prod"
STUDIO = "TechStein"
GENRE = "Afro-ballad"
YEAR = "2026"
ALBUM = "Mama tché"
COMMENT = (
    "Signature : Wolof TechStein beat wê ! — "
    "Prod : Daïsky Prod • Studio/Technologies : TechStein • "
    "Contact : +229 01 61 16 24 08 / 01 49 11 49 51 — "
    "techsteinsecureway@gmail.com / daiskyproduction@gmail.com — "
    "https://linktr.ee/daiskypro"
)


def main() -> None:
    OUT_MP3.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC_MP3, OUT_MP3)

    try:
        ID3().delete(OUT_MP3)
    except Exception:
        pass

    tags = ID3()
    tags.add(TIT2(encoding=3, text=TITLE))
    tags.add(TPE1(encoding=3, text=ARTIST))
    tags.add(TPE2(encoding=3, text=PROD))
    tags.add(TPUB(encoding=3, text=PROD))
    tags.add(TENC(encoding=3, text=STUDIO))
    tags.add(TALB(encoding=3, text=ALBUM))
    tags.add(TCON(encoding=3, text=GENRE))
    tags.add(TDRC(encoding=3, text=YEAR))
    tags.add(COMM(encoding=3, lang="fra", desc="comment", text=COMMENT))
    tags.add(
        APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=COVER.read_bytes(),
        )
    )
    tags.save(OUT_MP3, v2_version=3)
    print(f"Retagged: {OUT_MP3}")


if __name__ == "__main__":
    main()
