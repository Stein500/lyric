#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_ass.py — Génère lyrics.ass (sous-titres synchronisés) depuis manifest.json."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as fp:
    M = json.load(fp)

def ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def ass_escape(txt):
    return txt.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")

# Couleurs ASS = &HAABBGGRR
IVOIRE = "&H00DFEFF5"   # F5EFDF
OR     = "&H003DB3F2"   # F2B33D
NOIR   = "&H96000000"

header = f"""[Script Info]
Title: Heritage de mes parents - Daisky (lyrics)
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Parole,DejaVu Sans,52,{IVOIRE},{IVOIRE},{OR},{NOIR},1,0,0,0,100,100,0.6,0,1,3.2,1.6,2,80,80,430,1
Style: Hook,DejaVu Sans,60,{OR},{OR},{NOIR},{NOIR},1,0,0,0,100,100,1.0,0,1,3.4,1.8,2,80,80,430,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

lines = [header]
for p in M["paroles"]:
    texte = ass_escape(p["texte"])
    lines.append(
        f"Dialogue: 0,{ts(p['debut'])},{ts(p['fin'])},{p['style']},,0,0,0,,"
        f"{{\\fad(140,140)}}{texte}\n"
    )

with open(os.path.join(ROOT, "lyrics.ass"), "w", encoding="utf-8") as fp:
    fp.writelines(lines)
print("lyrics.ass généré :", len(M["paroles"]), "lignes")
