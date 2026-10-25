# -*- coding: utf-8 -*-
"""clean_prompts.py — v6.2 : prompts ART SANS AUCUN TEXTE + lettrage peint par lettering.py.
Le générateur ne peint plus un seul mot (mesuré : 0/18 plans dans la boîte, orthographe
non garantie). Il fournit le personnage, le décor, les 2 stickers ; le moteur pose la typo.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PAL = {
 "nuit": "deep teal and charcoal night, warm streetlight rim light on his shoulders and cheekbones, cool cyan highlights",
 "aube-a": "pre-dawn blue-violet sky with a thin rose-gold horizon, faint warm rim light, deep soft shadows",
 "aube-b": "full golden sunrise, warm amber haze, long shadows, luminous gold rim light, sky glowing peach and gold",
}
ICON = {"nuit": "\u2014", }


def prompt(pose, expr, decor, icon, bucket, sign=""):
    pal = PAL[bucket]
    sig = (" " + sign) if sign else ""
    return (
        "Vertical 9:16 street-dance battle anime illustration in the dynamic style of Wandance combined with "
        "clean stylish urban graffiti art, keeping the exact same protagonist and visual style as the reference "
        "image. The canvas is 768 px wide and 1376 px tall; all coordinates are on this native canvas.\n\n"
        "Framing: half-body shot \u2014 his head (uncovered, face fully visible, nothing over the forehead) sits "
        "between y 190 and y 400, his shoulders and arms between y 400 and y 465, and the frame cuts his hips at "
        f"the bottom edge. Pose: {pose}. His expression: {expr}. Behind him, an attenuated background: {decor}; "
        f"{pal}.{sig}\n\n"
        "IMPORTANT \u2014 NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol "
        "anywhere in the image, not on the walls, not on clothing, not on signs: the whole spray-painted mural and "
        "graffiti background must be pure abstract shapes and colour splashes only. Leave the middle band "
        "(y 470 to y 750, x 150 to x 590) visually calm and dark: this area is reserved and will be lettered "
        "afterwards, so keep it free of characters, objects and detail \u2014 just shallow shadow, concrete or sky.\n\n"
        f"Below that reserved band, between y 790 and y 900 and inside x 170 -> 600, paint 2 stylish urban graffiti "
        f"sticker icons side by side (these two icons are the only graphic marks allowed, with no letters inside "
        f"them): a glowing street-art heart and {icon}, each about 90 px tall, linked by a thin luminous gold line.\n\n"
        "From y 920 down to the bottom edge keep only clean dark floor and his legs. Nothing in the top 100 px, "
        "nothing on the right side beyond x 647, no flag, no logo, no watermark."
    )


def main():
    SRC = os.path.join(HERE, "prompts.json")
    items = json.load(open(SRC, encoding="utf-8"))
    TEXTES = __import__("build_map").TEXTES
    ids = {}
    for it in items:
        key = it["texte"]
        if key not in ids:
            ids[key] = len(ids) + 1
    out = []
    for it in items:
        bid = ids[it["texte"]]
        pose, expr, decor, icon = TEXTES[bid][1:]
        it = dict(it)
        it["prompt"] = prompt(pose, expr, decor, icon, it["bucket"])
        out.append(it)
    json.dump(out, open(os.path.join(HERE, "prompts_art.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"{len(out)} prompts art sans texte -> prompts_art.json")
    print(out[0]["prompt"])


if __name__ == "__main__":
    import sys
    sys.path.insert(0, HERE)
    main()
