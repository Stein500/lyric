#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_ass_reel.py — Sous-titres REEL : gros style viral, blanc + contour noir épais, zénith doré pour la chute."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LIGNES = [
    (0.0,  3.0,  "J'ai vu mon père rentrer à 2h du matin", "Reel"),
    (3.0,  5.0,  "Le dos courbé, les mains usées, le regard éteint", "Reel"),
    (5.0,  7.8,  "J'ai vu ma mère sourire quand le frigo est vide", "Reel"),
    (7.8,  10.0, "Elle mettait du sel dans l'eau…", "Reel"),
    (10.0, 13.0, "Ils ont vendu leurs rêves pour que je fasse les miens", "Reel"),
    (13.0, 16.0, "Ils ont marché sur leurs fiertés, ils ont serré les poings", "Reel"),
    (16.0, 18.0, "Pour que j'aie une chance, pour que j'aie un nom", "Reel"),
    (18.0, 21.0, "Pour que je dise « je suis fier » sans honte", "Reel"),
    (21.0, 24.0, "I owe them everything, my breath, my soul", "Reel"),
    (24.0, 27.0, "They carried me when I lost control", "Reel"),
    (27.0, 30.0, "Now I'm running, I'm flying so high", "Reel"),
    (30.0, 33.6, "For them, I'll touch the sky", "Final"),
]

def ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

BLANC = "&H00FFFFFF"; OR = "&H003DB3F2"; NOIR = "&H00000000"

header = f"""[Script Info]
Title: Reel viral - Heritage (extrait couplet1)
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

with open(os.path.join(ROOT, "reel.ass"), "w", encoding="utf-8") as fp:
    fp.writelines(out)
print("reel.ass :", len(LIGNES), "lignes")
