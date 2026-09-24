#!/usr/bin/env python3
"""Build validated timings + LRC for Le goût bon de la vie."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SONG = 204.36
HOOK = 6.0
APAD = 5.0
FPS = 24
HOOK_SRC = 15.93

# LRC start times (music clock) and text
RAW = [
    (6.08, "Wolof TechStein beat wê...", "sig", "s01_tee"),
    (9.95, "Yeah... Vivi oor...", "verse", "s03_seated"),
    (13.28, "Le goût bon de la vie...", "hook", "s01_tee"),
    (15.93, "Vivi oor, vivi oor, le goût bon de la vie", "hook", "s01_tee"),
    (18.79, "Wadjaya, viens t'enjailler, la nuit est à nous", "hook", "s02_vest"),
    (22.26, "Kissi noumi, embrasse-moi, ton goût est si doux", "hook", "s03_seated"),
    (25.77, "Vivi oor, vivi oor, je savoure chaque instant", "hook", "s01_tee"),
    (29.59, "Wolof TechStein beat wê!", "sig", "s02_vest"),
    (46.08, "J'ai le sourire collé au visage", "verse", "s01_tee"),
    (47.99, "Chaque jour est un nouveau voyage", "verse", "s01_tee"),
    (49.71, "Le soleil se lève, je sens le bon goût", "verse", "s01_tee"),
    (51.45, "Wadjaya, viens danser, on s'en fout", "verse", "s02_vest"),
    (53.24, "Kissi noumi, ta bouche a le goût du miel", "verse", "s03_seated"),
    (55.10, "Chaque baiser est une étincelle", "verse", "s03_seated"),
    (57.26, "Vivi oor, c'est ma philosophie", "verse", "s01_tee"),
    (59.34, "Savoure la vie, savoure chaque nuit", "verse", "s03_seated"),
    (61.29, "Wadjaya, viens, on va s'enjailler", "verse", "s02_vest"),
    (62.63, "Wadjaya, viens, on va célébrer", "verse", "s02_vest"),
    (64.25, "Vivi oor dans nos cœurs, vivi oor dans nos rires", "verse", "s01_tee"),
    (66.45, "La vie est belle, on va la savourer", "verse", "s01_tee"),
    (68.12, "Vivi oor, vivi oor, le goût bon de la vie", "hook", "s01_tee"),
    (71.05, "Wadjaya, viens t'enjailler, la nuit est à nous", "hook", "s02_vest"),
    (74.68, "Kissi noumi, embrasse-moi, ton goût est si doux", "hook", "s03_seated"),
    (77.93, "Vivi oor, vivi oor, je savoure chaque instant", "hook", "s01_tee"),
    (81.55, "Wolof TechStein beat wê!", "sig", "s02_vest"),
    (84.49, "Je marche dans la rue, je sens le bon air", "verse", "s01_tee"),
    (87.07, "Chaque pas est une danse, chaque souffle est un éclair", "verse", "s02_vest"),
    (90.48, "Wadjaya, mes amis, on va faire la fête", "verse", "s02_vest"),
    (92.49, "Vivi oor dans nos veines, la joie dans nos têtes", "verse", "s02_vest"),
    (96.09, "Kissi noumi, mon amour, donne-moi ton goût", "verse", "s03_seated"),
    (97.99, "Ce soir on savoure tout, ce soir on vit debout", "verse", "s02_vest"),
    (99.87, "Vivi oor, c'est le cri de mon cœur", "verse", "s03_seated"),
    (101.84, "La vie est un festin, je suis le mangeur", "verse", "s01_tee"),
    (105.22, "Wadjaya, viens, on va s'enjailler", "verse", "s02_vest"),
    (107.83, "Wadjaya, viens, on va célébrer", "verse", "s02_vest"),
    (109.69, "Vivi oor dans nos cœurs, vivi oor dans nos rires", "verse", "s01_tee"),
    (111.38, "La vie est belle, on va la savourer", "verse", "s01_tee"),
    (116.46, "Kissi noumi, ton goût reste sur mes lèvres", "verse", "s03_seated"),
    (121.65, "Vivi oor, chaque instant est une trêve", "verse", "s03_seated"),
    (125.24, "Wadjaya, dansons jusqu'au matin", "verse", "s02_vest"),
    (128.62, "Vivi oor, le bon goût, c'est mon destin", "verse", "s01_tee"),
    (140.27, "Vivi oor, vivi oor, le goût bon de la vie", "hook", "s01_tee"),
    (144.01, "Wadjaya, viens t'enjailler, la nuit est à nous", "hook", "s02_vest"),
    (147.50, "Kissi noumi, embrasse-moi, ton goût est si doux", "hook", "s03_seated"),
    (151.11, "Vivi oor, vivi oor, je savoure chaque instant", "hook", "s01_tee"),
    (155.69, "Wolof TechStein beat wê!", "sig", "s02_vest"),
    (161.44, "Wolof TechStein beat wê...", "sig", "s01_tee"),
    (164.38, "Vivi oor...", "verse", "s03_seated"),
    (189.62, "Wadjaya... Kissi noumi...", "verse", "s02_vest"),
    (192.33, "(Le goût bon... toujours...)", "outro", "s01_tee"),
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
        # 0.03s advance on the video clock (applied later in renderer)
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
            }
        )

    # cold-open lyrics (hook excerpt starting at 15.93)
    hook_lines = [
        {
            "start": 0.00,
            "end": 2.80,
            "text": "Vivi oor, vivi oor, le goût bon de la vie",
            "kind": "hook",
            "photo": "s01_tee",
        },
        {
            "start": 2.80,
            "end": 6.00,
            "text": "Wadjaya, viens t'enjailler, la nuit est à nous",
            "kind": "hook",
            "photo": "s02_vest",
        },
    ]

    total = HOOK + SONG + APAD
    nframes = int(-(-total * FPS // 1))  # ceil
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
            {"start": 0.00, "end": 6.08, "photo": "s00_intro"},
            {"start": 32.4, "end": 46.08, "photo": "s04_lagoon"},
            {"start": 132.5, "end": 140.27, "photo": "s04_lagoon"},
            {"start": 167.5, "end": 189.62, "photo": "s04_lagoon"},
        ],
    }
    work = ROOT / "work"
    work.mkdir(exist_ok=True)
    out = work / "timings_validated.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lrc = ["[ar:Daïsky]", "[ti:Le goût bon de la vie]", "[length:03:24.36]", ""]
    for v in verses:
        m = int(v["start"] // 60)
        s = v["start"] - 60 * m
        lrc.append(f"[{m:02d}:{s:05.2f}]{v['text']}")
    lrc_path = ROOT / "Le goût bon de la vie.lrc"
    lrc_path.write_text("\n".join(lrc) + "\n", encoding="utf-8")
    print("verses", len(verses), "nframes", nframes, "total", total)
    print("wrote", out)
    print("wrote", lrc_path)


if __name__ == "__main__":
    main()
