#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_ass_yt.py — Sous-titres YouTube 16:9 avec POLICES VARIÉES par section.
PlayRes 1920×1080. Styles :
  IntroOutro → DejaVu Serif (discret)      | Refrain → DejaVu Sans Bold (punchy)
  Couplet    → DejaVu Sans Mono Bold (rap) | PreRefrain → DejaVu Serif Bold (montée)
  Pont       → DejaVu Serif centré écran   | Hook → DejaVu Sans Bold or massif
La zone est déduite du timestamp (manifest.json reste la source de vérité).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as fp:
    M = json.load(fp)

def ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def zone(t):
    if t < 9:        return "IntroOutro"
    if t < 43:       return "Refrain"
    if t < 64:       return "Couplet"
    if t < 76.8:     return "PreRefrain"
    if t < 100:      return "Refrain"
    if t < 121:      return "Couplet"
    if t < 134:      return "PreRefrain"
    if t < 155:      return "Pont"
    if t < 185:      return "Refrain"
    return "IntroOutro"

IVOIRE = "&H00DFEFF5"; OR = "&H003DB3F2"; CUIVRE = "&H2B7AD9"; NOIR = "&H96000000"

header = f"""[Script Info]
Title: Heritage de mes parents - Daisky (lyrics YouTube 16:9)
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Refrain,DejaVu Sans,64,{IVOIRE},{IVOIRE},{OR},{NOIR},1,0,0,0,100,100,0.5,0,1,3.2,1.6,2,90,90,74,1
Style: Hook,DejaVu Sans,72,{OR},{OR},{NOIR},{NOIR},1,0,0,0,100,100,1.2,0,1,3.4,1.8,2,90,90,80,1
Style: Couplet,DejaVu Sans Mono,44,{IVOIRE},{IVOIRE},{CUIVRE},{NOIR},1,0,0,0,100,100,1.0,0,1,2.6,1.4,2,90,90,70,1
Style: PreRefrain,DejaVu Serif,58,{IVOIRE},{IVOIRE},{OR},{NOIR},1,0,0,0,100,100,0.8,0,1,3.0,1.6,2,90,90,84,1
Style: Pont,DejaVu Serif,52,{IVOIRE},{IVOIRE},{NOIR},{NOIR},0,0,0,0,100,100,1.5,0,1,2.4,2.0,5,90,90,0,1
Style: IntroOutro,DejaVu Serif,38,{IVOIRE},{IVOIRE},{NOIR},{NOIR},0,0,0,0,100,100,1.0,0,1,2.0,1.2,2,90,90,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

lignes = [header]
for p in M["paroles"]:
    style = "Hook" if "TechStein beat wê" in p["texte"] else zone(p["debut"])
    txt = p["texte"].replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
    lignes.append(f"Dialogue: 0,{ts(p['debut'])},{ts(p['fin'])},{style},,0,0,0,,{{\\fad(140,140)}}{txt}\n")

with open(os.path.join(ROOT, "lyrics_yt.ass"), "w", encoding="utf-8") as fp:
    fp.writelines(lignes)
print("lyrics_yt.ass :", len(M["paroles"]), "lignes, 6 styles de polices")
