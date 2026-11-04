#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bake.py — cuit les paroles dans les PNG (§10.4) + planche CONTROLE-paroles.jpg.
Usage : python3 bake.py prods/TU-ES-TROP-BELLE
Sorties dans <prod>/baked/ : {vers}.png (art+lettres), letters/{vers}.png, plans/{plan}.png
"""
import json, os, sys
from PIL import Image, ImageDraw
from common import load_plan, ensure_dir, font, NATIVE
import lettering

def main(prod):
    with open(os.path.join(prod, "verses_map.json"), encoding="utf-8") as f:
        vm = json.load(f)
    off_path = os.path.join(prod, "typo_offsets.json")
    offsets = json.load(open(off_path, encoding="utf-8")) if os.path.exists(off_path) else {}

    art_dir = os.path.join(prod, "art")
    out = os.path.join(prod, "baked")
    ensure_dir(out); ensure_dir(os.path.join(out, "letters")); ensure_dir(os.path.join(out, "plans"))

    plans_cache = {}
    def plan_img(pid):
        if pid not in plans_cache:
            p = os.path.join(art_dir, f"{pid}.png")
            if not os.path.exists(p):
                plans_cache[pid] = None
            else:
                im = load_plan(p)
                im.save(os.path.join(out, "plans", f"{pid}.png"))
                plans_cache[pid] = im
        return plans_cache[pid]

    tiles = []
    for v in vm["verses"]:
        pid = v["plan"]
        if plan_img(pid) is None:
            print(f"  skip {v['id']} (art {pid} pas encore généré)")
            continue
        art = plan_img(pid).copy()
        dy = int(offsets.get(pid, {}).get("dy", 0))
        letters, meta = lettering.paint(v["lignes"], seed_key=v["id"], dy=dy)
        letters.save(os.path.join(out, "letters", f"{v['id']}.png"))
        baked = Image.alpha_composite(art.convert("RGBA"), letters).convert("RGB")
        baked.save(os.path.join(out, f"{v['id']}.png"))
        # tuile de contrôle : zone typo à 1:1
        crop = baked.crop((0, 380, NATIVE[0], 1000))
        tiles.append((v["id"], v["texte"], crop))
        print(f"  baked {v['id']} plan={pid} corps={meta['size']} lignes={len(meta['lines'])} dy={dy}")

    # planche CONTROLE-paroles.jpg — 2 colonnes, crops 1:1 (y380→1000)
    cols, tw, th = 2, NATIVE[0], 620
    rows = -(-len(tiles) // cols)
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * (th + 34) + 8), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    f = font("Bold", 20)
    for i, (vid, txt, crop) in enumerate(tiles):
        cx = 8 + (i % cols) * (tw + 8)
        cy = 8 + (i // cols) * (th + 34)
        sheet.paste(crop, (cx, cy + 26))
        d.text((cx, cy), f"{vid} — {txt[:56]}", font=f, fill=(255, 210, 120))
    sheet.save(os.path.join(prod, "CONTROLE-paroles.jpg"), quality=92)
    print(f"planche : {sheet.size} -> {os.path.join(prod, 'CONTROLE-paroles.jpg')}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "prods/TU-ES-TROP-BELLE")
