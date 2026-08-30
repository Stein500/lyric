#!/usr/bin/env python3
"""Fill mandatory Daïsky Prod / Techstein ID3 tags and embed cover art.

Usage example:
  python tools/fill_music_tags.py audio.mp3 \
    --title "L'amour est la réponse" --genre "Heavy Metal / Rock" --year 2026 \
    --cover livrables/cover_daïsky_9x16.jpg
"""
from __future__ import annotations

import argparse
from pathlib import Path
from mutagen.id3 import (
    ID3,
    ID3NoHeaderError,
    APIC,
    COMM,
    TALB,
    TCOM,
    TCON,
    TCOP,
    TDRC,
    TENC,
    TIT2,
    TPE1,
    TPE2,
    TPUB,
    TXXX,
    WOAR,
)

DEFAULT_ARTIST = "Daïsky"
DEFAULT_LABEL = "Daïsky Prod"
DEFAULT_PRODUCER = "Techstein"
DEFAULT_PHONES = "+229 01 61 16 24 08 / +229 01 49 11 49 51"
DEFAULT_EMAILS = (
    "daiskypro@proton.me / daiskyproduction@gmail.com / "
    "techsteinsecureway@gmail.com"
)
DEFAULT_HANDLE = "@daiskypro"


def set_text(tags: ID3, frame_id: str, frame) -> None:
    tags.delall(frame_id)
    tags.add(frame)


def set_txxx(tags: ID3, desc: str, value: str) -> None:
    tags.delall(f"TXXX:{desc}")
    tags.add(TXXX(encoding=3, desc=desc, text=[value]))


def mime_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    return "image/jpeg"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--album", default="Single")
    parser.add_argument("--artist", default=DEFAULT_ARTIST)
    parser.add_argument("--label", default=DEFAULT_LABEL)
    parser.add_argument("--producer", default=DEFAULT_PRODUCER)
    parser.add_argument("--genre", required=True)
    parser.add_argument("--year", required=True)
    parser.add_argument("--phones", default=DEFAULT_PHONES)
    parser.add_argument("--emails", default=DEFAULT_EMAILS)
    parser.add_argument("--handle", default=DEFAULT_HANDLE)
    parser.add_argument("--cover", type=Path)
    args = parser.parse_args()

    try:
        tags = ID3(args.audio)
    except ID3NoHeaderError:
        tags = ID3()

    contact = (
        f"Contact / Booking: {args.producer} · {args.label} · {args.artist}\n"
        f"Téléphones: {args.phones}\n"
        f"Emails: {args.emails}\n"
        f"Réseaux: {args.handle}\n"
        f"Genre: {args.genre}\n"
        f"Année: {args.year}"
    )
    copyright_text = f"© {args.year} {args.label} / {args.producer}. Tous droits réservés."

    set_text(tags, "TIT2", TIT2(encoding=3, text=[args.title]))
    set_text(tags, "TPE1", TPE1(encoding=3, text=[args.artist]))
    set_text(tags, "TPE2", TPE2(encoding=3, text=[args.label]))
    set_text(tags, "TALB", TALB(encoding=3, text=[args.album]))
    set_text(tags, "TCOM", TCOM(encoding=3, text=[args.producer]))
    set_text(tags, "TCON", TCON(encoding=3, text=[args.genre]))
    set_text(tags, "TDRC", TDRC(encoding=3, text=[args.year]))
    set_text(tags, "TPUB", TPUB(encoding=3, text=[args.label]))
    set_text(tags, "TCOP", TCOP(encoding=3, text=[copyright_text]))
    set_text(tags, "TENC", TENC(encoding=3, text=[f"{args.producer} / {args.label}"]))

    set_txxx(tags, "PRODUCER", args.producer)
    set_txxx(tags, "LABEL", args.label)
    set_txxx(tags, "ARTIST", args.artist)
    set_txxx(tags, "PHONE", args.phones)
    set_txxx(tags, "EMAIL", args.emails)
    set_txxx(tags, "CONTACT", contact)
    set_txxx(tags, "HANDLE", args.handle)
    set_txxx(tags, "YEAR", args.year)
    set_txxx(tags, "GENRE", args.genre)

    tags.delall("COMM:Contact:fra")
    tags.add(COMM(encoding=3, lang="fra", desc="Contact", text=contact))
    tags.delall("WOAR")
    tags.add(WOAR(url=f"https://instagram.com/{args.handle.lstrip('@')}"))

    if args.cover:
        cover_data = args.cover.read_bytes()
        tags.delall("APIC")
        tags.add(
            APIC(
                encoding=3,
                mime=mime_for(args.cover),
                type=3,
                desc="Cover",
                data=cover_data,
            )
        )

    tags.save(args.audio)
    print(f"Tags complétés: {args.audio}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
