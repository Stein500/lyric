#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LOGO WTBW — versions VECTORIELLES (SVG), contours de glyphes, aucun modèle d'image.

Le lettrage est converti en courbes à partir du fichier de police Montserrat.ttf
(pas d'appel à une IA, pas de texte « vivant » dans le SVG : uniquement des tracés).

Sortie : livrables/brand/print/WTBW-lettrage.svg
         livrables/brand/print/WTBW-sigle-lettrage.svg
Usage : python3 logo_svg.py
"""
import sys

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

OUT = "/home/user/lyric/productions/pub-wtbw"
FONT = f"{OUT}/../imelda-13-novembre/Montserrat.ttf"
LIV = f"{OUT}/livrables/brand/print"

TRACK = 0.24          # interlettrage, en fraction de la taille
STROKE = 0.055        # épaississement (équivalent du trait)


def glyph_paths(text, size=100.0, track=TRACK):
    """renvoie (liste de (dx, path), largeur_totale) en unités px, y vers le bas."""
    font = TTFont(FONT)
    upem = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    s = size / upem
    x = 0.0
    out = []
    for ch in text:
        gname = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[gname].draw(pen)
        d = pen.getCommands()
        out.append((x, d))
        x += hmtx[gname][0] * s + track * size
    total = x - track * size
    return out, total, s, upem


def word_svg(text="WTBW", size=100.0, color="#000000", stroke_px=0.0, track=TRACK, base=None):
    base = 0.725 * size if base is None else base
    paths, total, s, upem = glyph_paths(text, size, track)
    body = []
    for dx, d in paths:
        body.append(
            f'  <path transform="translate({dx:.3f} {base:.3f}) scale({s:.6f} {-s:.6f})" d="{d}"/>'
        )
    g = "\n".join(body)
    st = f' stroke="{color}" stroke-width="{stroke_px / s:.2f}" stroke-linejoin="round"' if stroke_px else ""
    return (f'<g fill="{color}"{st}>\n{g}\n</g>', total)


def sigil_group(cx, cy, r, color="#000000"):
    """le sigle : double cercle + W en polyligne + filet + étoile (mêmes cotes que logo.py)."""
    w = r * 0.060 * 2.092          # épaisseur du trait du W (0,060 · S, S = r / 0,478)
    pts = [(-0.235, -0.140), (-0.117, 0.140), (0.000, -0.050), (0.117, 0.140), (0.235, -0.140)]
    poly = " ".join(f"{cx + px * r / 0.478:.2f},{cy + py * r / 0.478:.2f}" for px, py in pts)
    star = []
    import math
    sy0 = cy + 0.350 * 2.092 * r
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = 0.046 * 2.092 * r if k % 2 == 0 else 0.046 * 2.092 * r * 0.42
        star.append(f"{cx + rr * math.cos(a):.2f},{sy0 + rr * math.sin(a):.2f}")
    return f'''  <g fill="none" stroke="{color}" stroke-width="{r * 0.0335:.2f}">
    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}"/>
  </g>
  <g fill="none" stroke="{color}" stroke-width="{r * 0.0126:.2f}" stroke-opacity="0.66">
    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r * 0.912:.2f}"/>
  </g>
  <polyline points="{poly}" fill="none" stroke="{color}" stroke-width="{w:.2f}"
            stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="{cx - r * 0.314:.2f}" y1="{cy + r * 0.561:.2f}" x2="{cx + r * 0.314:.2f}" y2="{cy + r * 0.561:.2f}"
        stroke="{color}" stroke-width="{r * 0.0209:.2f}"/>
  <polygon points="{' '.join(star)}" fill="{color}"/>'''


def write_lettering(path):
    """WTBW seul, prêt à poser : marges de 10 unités, encre noire."""
    word, total = word_svg("WTBW", 100.0, "#000000", stroke_px=5.5, base=80)
    W, H = int(total + 20), 106
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <g transform="translate(10 0)">
{word}
  </g>
</svg>
'''
    open(path, "w").write(svg)
    return path


def write_combo(path):
    """sigle au-dessus, lettrage en dessous."""
    word, total = word_svg("WTBW", 100.0, "#000000", stroke_px=5.5, base=72)
    r = 140.0
    W = int(total + 40)
    H = 436
    cx, cy = W / 2.0, 150.0
    body = f'''{sigil_group(cx, cy, r)}
  <g transform="translate({(W - total) / 2:.2f} 356)">{word}</g>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
{body}
</svg>
'''
    open(path, "w").write(svg)
    return path


def write_sigil(path):
    """le sigle seul, cadré au plus juste (marges de 10 unités)."""
    r = 150.0
    W = H = 320
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
{sigil_group(W / 2, H / 2, r)}
</svg>
'''
    open(path, "w").write(svg)
    return path


if __name__ == "__main__":
    print(write_lettering(f"{LIV}/WTBW-lettrage.svg"))
    print(write_sigil(f"{LIV}/WTBW-sigle.svg"))
    print(write_combo(f"{LIV}/WTBW-sigle-lettrage.svg"))
