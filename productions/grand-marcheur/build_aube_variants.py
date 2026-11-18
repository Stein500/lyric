#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Variantes d'aube pour les reprises apres le passage a l'aube (v7.0 §3).

Compromis DECLARE : aucune nouvelle generation IA (budget du tour epuise).
Le fond du plan d'origine est reetalonne par le moteur (lumiere ambre),
puis le vers EXACT est recuit dessus par lettering.cook() : memes glyphes,
memes accents, memes apostrophes, aucune retouche manuelle.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import outils  # amorce Pillow
import lettering
from PIL import Image, ImageEnhance

CONTRACT = json.load(open(os.path.join(HERE, "verses_map.json"), encoding="utf-8"))
PASSAGE = CONTRACT["passage_aube_i"]
BY_I = {e["i"]: e for e in CONTRACT["vers"]}
BRUT = os.path.join(HERE, "assets", "aube")
CUIT = os.path.join(HERE, "assets", "aube", "cuits")
os.makedirs(BRUT, exist_ok=True)
os.makedirs(CUIT, exist_ok=True)

sources = sorted({e["reprise_de"] for e in CONTRACT["vers"]
                  if e["reprise"] and e["i"] > PASSAGE})
report = []
for src in sources:
    raw = os.path.join(HERE, "assets/plans/plan-%02d.jpg" % src)
    graded_rel = "assets/aube/brut-%02d.jpg" % src
    out_rel = "assets/aube/cuits/aube-plan-%02d.jpg" % src
    im = Image.open(raw).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(1.34)
    im = ImageEnhance.Color(im).enhance(1.10)
    im = Image.blend(im, Image.new("RGB", im.size, (255, 202, 132)), 0.24)
    im.save(os.path.join(HERE, graded_rel), "JPEG", quality=94)
    entry = {"i": src,
             "texte_affiche": BY_I[src]["texte_affiche"],
             "image": graded_rel,
             "image_cuite": out_rel}
    report.append(lettering.cook(entry))

with open(os.path.join(HERE, "aube_variants.json"), "w", encoding="utf-8") as fh:
    json.dump({"passage_aube_i": PASSAGE,
               "methode": "reetalonnage moteur du fond + recuisson du vers exact (aucune generation IA)",
               "sources": sources, "variantes": report}, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("sources :", sources)
print("variantes d'aube cuites :", len(report))
