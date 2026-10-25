#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qc_typo.py — contrôle automatique du bloc peint (repère natif 768x1376).

Mesure la boîte réelle des lettres claires (L > 168), évalue la hauteur de capitale
et rend un verdict :
  OK      boîte dans x 140→600, y 430→810, capitale 22→62 px
  HORS-X  déborde la marge droite/gauche (zone TikTok x ≥ 647)
  HORS-Y  trop haut (sous le badge / sur le visage) ou trop bas (zone 1574)
  GROS    capitales > 62 px (bloc « affiche »)
  PETIT   capitales < 22 px (illisible)

  python3 qc_typo.py                # tous les plans
  python3 qc_typo.py --json         # sortie machine
"""
import json, os, sys
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONDS = os.path.join(HERE, "fonds")
X0, X1, Y0, Y1 = 140, 600, 430, 810
CAP_MIN, CAP_MAX = 22, 62


def letter_mask(im):
    """pixels clairs ENTOURÉS de sombre = lettres sur halo d'encre (le décor clair est éliminé)."""
    import numpy as np
    a = np.asarray(im, dtype=np.uint8)
    bright = a > 168
    dark = a < 72
    from PIL import ImageFilter as IF
    dark_wide = np.asarray(Image.fromarray((dark * 255).astype("uint8")).filter(IF.MaxFilter(11))) > 0
    m = bright & dark_wide
    return m


def measure(path):
    import numpy as np
    im = Image.open(path).convert("L").filter(ImageFilter.MedianFilter(5))
    m = letter_mask(im)
    h, w = m.shape
    cols = m[300:1000, :].sum(axis=0)
    rows = m[:, 40:730].sum(axis=1)
    xs = [x for x in range(140, 601) if cols[x] > 2]
    ys = [y for y in range(300, 1000) if rows[y] > 2]
    if not xs or not ys:
        return None
    # lignes de texte = paquets de lignes denses ; hauteur de capitale = paquet le plus haut
    groups, cur = [], [ys[0]]
    for y in ys[1:]:
        if y - cur[-1] <= 6:
            cur.append(y)
        else:
            groups.append(cur)
            cur = [y]
    groups.append(cur)
    cap = max(len(g) for g in groups)
    return {"x0": xs[0], "x1": xs[-1], "y0": ys[0], "y1": ys[-1], "cap": cap,
            "lignes": len(groups)}


def verdict(r):
    if r is None:
        return "VIDE"
    if r["x0"] < X0 or r["x1"] > X1:
        return "HORS-X"
    if r["y0"] < Y0 or r["y1"] > Y1:
        return "HORS-Y"
    if r["cap"] > CAP_MAX:
        return "GROS"
    if r["cap"] < CAP_MIN:
        return "PETIT"
    return "OK"


def main():
    out = {}
    for f in sorted(os.listdir(FONDS)):
        if not f.startswith("v-") or not f.endswith(".png"):
            continue
        r = measure(os.path.join(FONDS, f))
        out[f] = {"mesure": r, "verdict": verdict(r)}
    if "--json" in sys.argv:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    ok = sum(1 for v in out.values() if v["verdict"] == "OK")
    print(f"{ok}/{len(out)} plans conformes")
    for f, v in out.items():
        r = v["mesure"] or {}
        print(f"  {f:22s} {v['verdict']:7s} x {r.get('x0','-'):>3}→{r.get('x1','-'):<3} "
              f"y {r.get('y0','-'):>3}→{r.get('y1','-'):<4} cap {r.get('cap','-'):>3} lignes {r.get('lignes','-')}")


if __name__ == "__main__":
    main()
