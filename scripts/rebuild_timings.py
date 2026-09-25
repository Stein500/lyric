#!/usr/bin/env python3
"""Timings + mapping lock10 (visage intact) — Le goût bon de la vie."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SONG = 204.36
HOOK = 6.0
APAD = 5.0
FPS = 24
HOOK_SRC = 15.93

# close = l02/l04/l06/l08/l10 · medium = l01/l03/l05/l07
RAW = [
    (6.08, "Wolof TechStein beat wê...", "sig", "l01"),
    (9.95, "Yeah... Vivi oor...", "verse", "l02"),
    (13.28, "Le goût bon de la vie...", "hook", "l03"),
    (15.93, "Vivi oor, vivi oor, le goût bon de la vie", "hook", "l03"),
    (18.79, "Wadjaya, viens t'enjailler, la nuit est à nous", "hook", "l07"),
    (22.26, "Kissi noumi, embrasse-moi, ton goût est si doux", "hook", "l04"),
    (25.77, "Vivi oor, vivi oor, je savoure chaque instant", "hook", "l06"),
    (29.59, "Wolof TechStein beat wê!", "sig", "l07"),
    (46.08, "J'ai le sourire collé au visage", "verse", "l01"),
    (47.99, "Chaque jour est un nouveau voyage", "verse", "l05"),
    (49.71, "Le soleil se lève, je sens le bon goût", "verse", "l03"),
    (51.45, "Wadjaya, viens danser, on s'en fout", "verse", "l07"),
    (53.24, "Kissi noumi, ta bouche a le goût du miel", "verse", "l04"),
    (55.10, "Chaque baiser est une étincelle", "verse", "l08"),
    (57.26, "Vivi oor, c'est ma philosophie", "verse", "l05"),
    (59.34, "Savoure la vie, savoure chaque nuit", "verse", "l06"),
    (61.29, "Wadjaya, viens, on va s'enjailler", "verse", "l07"),
    (62.63, "Wadjaya, viens, on va célébrer", "verse", "l07"),
    (64.25, "Vivi oor dans nos cœurs, vivi oor dans nos rires", "verse", "l08"),
    (66.45, "La vie est belle, on va la savourer", "verse", "l03"),
    (68.12, "Vivi oor, vivi oor, le goût bon de la vie", "hook", "l03"),
    (71.05, "Wadjaya, viens t'enjailler, la nuit est à nous", "hook", "l07"),
    (74.68, "Kissi noumi, embrasse-moi, ton goût est si doux", "hook", "l04"),
    (77.93, "Vivi oor, vivi oor, je savoure chaque instant", "hook", "l06"),
    (81.55, "Wolof TechStein beat wê!", "sig", "l01"),
    (84.49, "Je marche dans la rue, je sens le bon air", "verse", "l05"),
    (87.07, "Chaque pas est une danse, chaque souffle est un éclair", "verse", "l07"),
    (90.48, "Wadjaya, mes amis, on va faire la fête", "verse", "l07"),
    (92.49, "Vivi oor dans nos veines, la joie dans nos têtes", "verse", "l08"),
    (96.09, "Kissi noumi, mon amour, donne-moi ton goût", "verse", "l04"),
    (97.99, "Ce soir on savoure tout, ce soir on vit debout", "verse", "l05"),
    (99.87, "Vivi oor, c'est le cri de mon cœur", "verse", "l08"),
    (101.84, "La vie est un festin, je suis le mangeur", "verse", "l03"),
    (105.22, "Wadjaya, viens, on va s'enjailler", "verse", "l07"),
    (107.83, "Wadjaya, viens, on va célébrer", "verse", "l07"),
    (109.69, "Vivi oor dans nos cœurs, vivi oor dans nos rires", "verse", "l08"),
    (111.38, "La vie est belle, on va la savourer", "verse", "l03"),
    (116.46, "Kissi noumi, ton goût reste sur mes lèvres", "verse", "l04"),
    (121.65, "Vivi oor, chaque instant est une trêve", "verse", "l06"),
    (125.24, "Wadjaya, dansons jusqu'au matin", "verse", "l07"),
    (128.62, "Vivi oor, le bon goût, c'est mon destin", "verse", "l03"),
    (140.27, "Vivi oor, vivi oor, le goût bon de la vie", "hook", "l03"),
    (144.01, "Wadjaya, viens t'enjailler, la nuit est à nous", "hook", "l07"),
    (147.50, "Kissi noumi, embrasse-moi, ton goût est si doux", "hook", "l04"),
    (151.11, "Vivi oor, vivi oor, je savoure chaque instant", "hook", "l06"),
    (155.69, "Wolof TechStein beat wê!", "sig", "l01"),
    (161.44, "Wolof TechStein beat wê...", "sig", "l01"),
    (164.38, "Vivi oor...", "verse", "l02"),
    (189.62, "Wadjaya... Kissi noumi...", "verse", "l07"),
    (192.33, "(Le goût bon... toujours...)", "outro", "l10"),
]


def verse_end(i: int) -> float:
    start = RAW[i][0]
    nxt = RAW[i + 1][0] if i + 1 < len(RAW) else SONG
    gap = nxt - start
    text = RAW[i][1]
    natural = max(2.2, min(4.2, 1.6 + 0.055 * len(text)))
    if gap <= 4.6:
        return max(start + 1.2, nxt - 0.04)
    return min(start + natural, nxt - 0.2)


def main() -> None:
    verses = []
    prev = -999.0
    for i, (start, text, kind, photo) in enumerate(RAW):
        end = verse_end(i)
        if start <= prev:
            start = prev + 1.2
        if end <= start:
            end = start + 1.2
        prev = start
        verses.append(
            {
                "i": i,
                "start": round(start, 3),
                "end": round(end, 3),
                "text": text,
                "kind": kind,
                "photo": photo,
                "words": text.replace("...", " …").split(),
            }
        )
    hook_lines = [
        {
            "start": 0.00,
            "end": 2.80,
            "text": "Vivi oor, vivi oor, le goût bon de la vie",
            "kind": "hook",
            "photo": "l03",
            "words": "Vivi oor, vivi oor, le goût bon de la vie".split(),
        },
        {
            "start": 2.80,
            "end": 6.00,
            "text": "Wadjaya, viens t'enjailler, la nuit est à nous",
            "kind": "hook",
            "photo": "l07",
            "words": "Wadjaya, viens t'enjailler, la nuit est à nous".split(),
        },
    ]
    total = HOOK + SONG + APAD
    nframes = int(-(-total * FPS // 1))
    data = {
        "title": "Le goût bon de la vie",
        "artist": "Daïsky",
        "badge": "DSKY✓",
        "song_duration": SONG,
        "hook": HOOK,
        "hook_src_start": HOOK_SRC,
        "apad": APAD,
        "fps": FPS,
        "total": round(total, 3),
        "nframes": nframes,
        "contacts": {
            "email": "daiskyproduction@gmail.com",
            "whatsapp": ["+229 01 61 16 24 08", "+229 01 49 11 49 51"],
        },
        "verses": verses,
        "hook_lines": hook_lines,
        "instrumentals": [
            {"start": 0.00, "end": 6.08, "photo": "l01"},
            {"start": 32.4, "end": 46.08, "photo": "l03"},
            {"start": 132.5, "end": 140.27, "photo": "l05"},
            {"start": 167.5, "end": 189.62, "photo": "l10"},
        ],
    }
    work = ROOT / "work"
    work.mkdir(exist_ok=True)
    (work / "timings_validated.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lrc = ["[ar:Daïsky]", "[ti:Le goût bon de la vie]", "[length:03:24.36]", ""]
    for v in verses:
        m = int(v["start"] // 60)
        s = v["start"] - 60 * m
        lrc.append(f"[{m:02d}:{s:05.2f}]{v['text']}")
    (ROOT / "Le goût bon de la vie.lrc").write_text("\n".join(lrc) + "\n", encoding="utf-8")
    print("verses", len(verses), "nframes", nframes, "total", total)


if __name__ == "__main__":
    main()
