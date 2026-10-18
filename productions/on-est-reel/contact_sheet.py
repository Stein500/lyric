#!/usr/bin/env python3
"""Contact sheet d'une salve de plans (§10.5 QC visuel, ≥ 480 px de large)."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FONDS = os.path.join(ROOT, "fonds")

def sheet(indices, out):
    d = json.load(open(os.path.join(ROOT, "verses_map.json"), encoding="utf-8"))
    texts = {p["i"]: p["texte"] for p in d["plans"]}
    CW, CH, LABEL = 360, 645, 92
    COLS = 3
    ROWS = (len(indices) + COLS - 1) // COLS
    W = COLS * CW + (COLS + 1) * 16
    H = ROWS * (CH + LABEL) + (ROWS + 1) * 16 + 70
    s = Image.new("RGB", (W, H), (11, 27, 42))
    dr = ImageDraw.Draw(s)
    f_head = ImageFont.truetype(os.path.join(ROOT, "fonts", "Montserrat.ttf"), 32)
    f_lab = ImageFont.truetype(os.path.join(ROOT, "fonts", "Montserrat.ttf"), 21)
    dr.text((16, 16), f"« On est réel » · Dsky — salve {out.split('-')[-1].split('.')[0]} — QC §10.5", font=f_head, fill=(243, 231, 211))
    for k, i in enumerate(indices):
        r, c = divmod(k, COLS)
        x = 16 + c * (CW + 16)
        y = 70 + r * (CH + LABEL + 16)
        fn = os.path.join(FONDS, "scene-01-ancre.png" if i == 1 else f"v-{i:02d}.png")
        if not os.path.exists(fn):
            dr.rectangle([x, y, x + CW, y + CH], outline=(217, 164, 65))
            dr.text((x + 10, y + 10), f"v-{i:02d} MANQUANT", font=f_lab, fill=(243, 231, 211))
            continue
        im = Image.open(fn).convert("RGB").resize((CW, CH), Image.LANCZOS)
        s.paste(im, (x, y))
        dr.text((x + 4, y + CH + 10), f"v-{i:02d}", font=f_lab, fill=(217, 164, 65))
        t = texts[i]
        dr.text((x + 78, y + CH + 10), (t[:48] + "…") if len(t) > 48 else t, font=f_lab, fill=(243, 231, 211))
    s.save(os.path.join(ROOT, "livrables", out))
    print("contact sheet →", out, s.size)

if __name__ == "__main__":
    idx = [int(a) for a in sys.argv[1:-1]] if len(sys.argv) > 2 else list(range(1, 11))
    sheet(idx, sys.argv[-1] if len(sys.argv) > 1 else "contact-sheet-salve-01.png")
