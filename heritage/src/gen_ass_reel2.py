#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_ass_reel2.py — Sous-titres REEL 2 (extrait 1:40 → 2:14). Même style viral."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LIGNES = [
    (0.0,  3.0,  "Maman a arrêté ses études pour que je commence", "Reel"),
    (3.0,  5.0,  "Papa a quitté son pays pour que je me sente chez moi", "Reel"),
    (5.0,  8.0,  "Ils m'ont donné leur âge, leur jeunesse, leur silence", "Reel"),
    (8.0,  10.8, "Pour que je grandisse sans porter leurs souffrances", "Reel"),
    (10.8, 13.0, "Aujourd'hui je suis debout, je suis leur victoire", "Reel"),
    (13.0, 16.0, "Chaque pas que je fais est une page de leur histoire", "Reel"),
    (16.0, 19.0, "Je ne les oublierai pas, jamais, jamais", "Reel"),
    (19.0, 21.0, "Ils sont mon héritage, ma raison de briller", "Reel"),
    (21.0, 24.0, "I owe them everything, my breath, my soul", "Reel"),
    (24.0, 26.0, "They carried me when I lost control", "Reel"),
    (26.0, 30.0, "Now I'm running, I'm flying so high", "Reel"),
    (30.0, 33.6, "For them, I'll touch the sky", "Final"),
]

def ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

BLANC = "&H00FFFFFF"; OR = "&H003DB3F2"; NOIR = "&H00000000"

header = f"""[Script Info]
Title: Reel viral 2 - Heritage (extrait couplet2)
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Reel,DejaVu Sans,72,{BLANC},{BLANC},{NOIR},{NOIR},1,0,0,0,100,100,0.5,0,1,4.5,0,2,90,90,470,1
Style: Final,DejaVu Sans,80,{OR},{OR},{NOIR},{NOIR},1,0,0,0,100,100,1.0,0,1,4.5,0,2,90,90,470,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

out = [header]
for d, f, txt, st in LIGNES:
    out.append(f"Dialogue: 0,{ts(d)},{ts(f)},{st},,0,0,0,,{{\\fad(90,90)}}{txt}\n")

with open(os.path.join(ROOT, "reel2.ass"), "w", encoding="utf-8") as fp:
    fp.writelines(out)
print("reel2.ass :", len(LIGNES), "lignes")
