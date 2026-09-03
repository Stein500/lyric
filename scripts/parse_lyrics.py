#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse le fichier de paroles minuté de l'artiste -> work/timing.csv
Règles v4.7 §3 / v4.2 :
  - "-M:SS" en fin de ligne  => FIN du vers (début = fin du vers précédent)
  - "M:SS-M:SS"             => plage EXPLICITE
Script TRACKÉ (scripts/) : survit aux resets sandbox.
"""
import csv
import os
import re
import sys

SRC = "Je suis Pauvre et riche.txt"
OUT = "work/timing.csv"

STYLE = {
    "INTRO": "intro",
    "REFRAIN": "hook",
    "REFRAIN FINAL": "hook_final",
    "COUPLET": "verse",
    "PRÉ-REFRAIN": "pre",
    "PONT": "bridge",
    "OUTRO": "outro",
}

RANGE = re.compile(r"^(?P<txt>.*?)\s*(?P<a>\d+):(?P<am>\d+(?:\.\d+)?)\s*-\s*(?P<b>\d+):(?P<bm>\d+(?:\.\d+)?)\s*$")
END = re.compile(r"^(?P<txt>.*?)\s*-?\s*(?P<a>\d+):(?P<am>\d+(?:\.\d+)?)\s*$")
SECTION = re.compile(r"^\[(?P<sec>.+?)\]\s*$")


def style_of(sec: str) -> str:
    head = (sec or "").split(" - ")[0].strip().upper()
    return STYLE.get(head, "verse")


def main() -> int:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    lines = []
    sec = ""
    for raw in open(SRC, encoding="utf-8"):
        s = raw.strip()
        if not s:
            continue
        m = SECTION.match(s)
        if m:
            sec = m.group(1)
            continue
        m = RANGE.match(s)
        if m:
            lines.append((sec, m.group("txt").strip(),
                          int(m.group("a")) * 60 + float(m.group("am")),
                          int(m.group("b")) * 60 + float(m.group("bm")), "range"))
            continue
        m = END.match(s)
        if m:
            lines.append((sec, m.group("txt").strip(), None,
                          int(m.group("a")) * 60 + float(m.group("am")), "end"))
            continue
        print("ERREUR: ligne non parsée -> %r" % s, file=sys.stderr)
        return 1

    rows = []
    prev_end = 0.0
    for i, (sec, txt, st, en, kind) in enumerate(lines, start=1):
        if kind == "range":
            note = "plage explicite artiste"
        else:
            st = prev_end
            note = "début = fin du vers précédent"
        if en <= st:
            print("ERREUR: vers %d : fin %.2f <= début %.2f" % (i, en, st), file=sys.stderr)
            return 1
        rows.append(dict(slot=i, start=round(st, 2), end=round(en, 2),
                         dur=round(en - st, 2), section=sec.split(" - ")[0].strip(),
                         style=style_of(sec), text=txt, note=note))
        prev_end = en

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("vers parsés : %d -> %s (dernière fin %.2f s)" % (len(rows), OUT, rows[-1]["end"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
