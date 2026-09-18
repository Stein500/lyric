#!/usr/bin/env python3
"""
rebuild_timings.py - Valide et reconstruit les timings vers par vers
pour 'Nan yi a ga djin wê' selon PROMPT_UNIVERSEL_v5.1.1.
"""
import re
import json

LYRICS_FILE = "Nan yi a ga djin wê.txt"
LRC_OUTPUT = "Nan yi a ga djin wê.lrc"
JSON_OUTPUT = "work/timings_validated.json"

def main():
    with open(LYRICS_FILE, "r", encoding="utf-8") as f:
        raw_lines = [l.strip() for l in f if l.strip()]

    lrc_lines = []
    validated = []

    for l in raw_lines:
        m = re.match(r'^\[(\d+):(\d+\.?\d*)\](.*)$', l)
        if m:
            m_val = int(m.group(1))
            s_val = float(m.group(2))
            t = m_val * 60.0 + s_val
            txt = m.group(3).strip()
            validated.append({"time": t, "text": txt, "formatted": f"{m_val:02d}:{s_val:05.2f}"})
            lrc_lines.append(f"[{m_val:02d}:{s_val:05.2f}]{txt}")

    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(validated, f, indent=2, ensure_ascii=False)

    with open(LRC_OUTPUT, "w", encoding="utf-8") as f:
        f.write("[ti:Nan yi a ga djin wê]\n[ar:Daïsky]\n[al:Nan yi a ga djin wê]\n")
        f.write("\n".join(lrc_lines) + "\n")

    print(f"Rebuilt timings: {len(validated)} vers -> {JSON_OUTPUT} et {LRC_OUTPUT}")

if __name__ == "__main__":
    main()
