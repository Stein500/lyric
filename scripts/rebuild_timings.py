#!/usr/bin/env python3
"""v4.9 — reconstruit work/timings_validated.json depuis le .lrc committé
(65 occurrences horodatées = ordre chanté). Usage: python scripts/rebuild_timings.py"""
import json, re
lrc = open("Je crache mes démons.lrc", encoding="utf-8").read()
verses = []
for line in lrc.splitlines():
    m = re.match(r"\[(\d+):(\d+\.\d+)\](.*)$", line.strip())
    if not m:
        continue
    verses.append({"section": "LRC", "text": m.group(3).strip(),
                   "t0": int(m.group(1)) * 60 + float(m.group(2)),
                   "onset_ok": True, "t_corr": int(m.group(1)) * 60 + float(m.group(2))})
seen, uniq = set(), []
for v in verses:
    if v["text"].lower() not in seen:
        seen.add(v["text"].lower())
        uniq.append(v["text"])
out = {"duration_s": 210.02, "verses": verses, "unique_lines": uniq,
       "n_unique": len(uniq), "budget_par_format": len(uniq) + 2,
       "corrections": [{"text": "Je me relève, je me relève, même quand tout est fini", "old": 36.5, "new": 27.0},
                       {"text": "J'ai survécu, j'ai survécu, personne ne m'a trahi", "old": 40.0, "new": 39.5},
                       {"text": "J'ai perdu, j'ai gagné, j'ai traversé la nuit", "old": 148.5, "new": 146.5}]}
json.dump(out, open("work/timings_validated.json", "w"), ensure_ascii=False, indent=1)
print(f"timings reconstruits: {len(verses)} occurrences, {len(uniq)} uniques")
