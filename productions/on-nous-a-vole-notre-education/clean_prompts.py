# -*- coding: utf-8 -*-
"""clean_prompts.py — v6.2 : prompts ART SANS AUCUN TEXTE + lettrage peint par lettering.py.

Le générateur ne peint plus un seul mot (mesuré : 0/18 plans dans la boîte, orthographe
non garantie). Il fournit le personnage, le décor, les 2 stickers ; le moteur pose la typo.

Trois consignes ont été ajoutées après mesure :
  • NO TEXT AT ALL            — sinon il peint des tags mal orthographiés ;
  • NO HORIZONTAL BAND        — sinon il colle deux zones (couture pleine largeur) ;
  • floor continues naturally — sinon il trace une ligne nette à y ~1078.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

PAL = {
    "nuit": "deep teal and charcoal night, warm streetlight rim light on his shoulders and cheekbones, "
            "cool cyan highlights",
    "aube-a": "pre-dawn blue-violet sky with a thin rose-gold horizon, faint warm rim light, deep soft shadows",
    "aube-b": "full golden sunrise, warm amber haze, long shadows, luminous gold rim light, "
              "sky glowing peach and gold",
}

HEAD = (
    "Vertical 9:16 street-dance battle anime illustration in the dynamic style of Wandance combined with "
    "clean stylish urban graffiti art, keeping the exact same protagonist and visual style as the reference "
    "image. The canvas is 768 px wide and 1376 px tall; all coordinates are on this native canvas.\n\n"
)

FRAME = (
    "Framing: half-body shot — his head (uncovered, face fully visible, nothing over the forehead) sits "
    "between y 190 and y 400, his shoulders and arms between y 400 and y 465, and the frame cuts his hips "
    "at the bottom edge. Pose: {pose}. His expression: {expr}. Behind him, an attenuated background: "
    "{decor}; {pal}.\n\n"
)

NO_TEXT = (
    "IMPORTANT — NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol "
    "anywhere in the image, not on the walls, not on clothing, not on signs: the whole spray-painted mural "
    "and graffiti background must be pure abstract shapes and colour splashes only.\n\n"
)

NO_BAND = (
    "IMPORTANT — NO HORIZONTAL BAND. The picture is one continuous scene: absolutely no band, strip, panel, "
    "rectangle, frame, seam, colour break or gradient line running across the image, and no zone that looks "
    "pasted or masked. Keep the décor naturally calmer and darker around his torso (roughly the middle third) "
    "simply as a lighting choice — deep ambient shadow — never as a drawn shape.\n\n"
)

STICKERS = (
    "Below that calm area, between y 790 and y 900 and inside x 170 -> 600, paint 2 stylish urban graffiti "
    "sticker icons side by side (these two icons are the only graphic marks allowed, and no letters inside "
    "them): a glowing street-art heart and {icon}, each about 90 px tall, linked by a thin luminous gold line.\n\n"
)

FLOOR = (
    "The floor continues naturally from the stickers down to the bottom edge as one single surface, slowly "
    "sinking into deeper shadow, with no seam, no line and no change of texture. Nothing in the top 100 px, "
    "nothing on the right side beyond x 647, no flag, no logo, no watermark."
)


def prompt(pose, expr, decor, icon, bucket):
    return (HEAD
            + FRAME.format(pose=pose, expr=expr, decor=decor, pal=PAL[bucket])
            + NO_TEXT + NO_BAND
            + STICKERS.format(icon=icon)
            + FLOOR)


def main():
    sys.path.insert(0, HERE)
    import build_map
    items = json.load(open(os.path.join(HERE, "prompts.json"), encoding="utf-8"))
    ids, order = {}, []
    for it in items:
        if it["texte"] not in ids:
            ids[it["texte"]] = len(order) + 1
            order.append(it["texte"])
    out = []
    for it in items:
        bid = ids[it["texte"]]
        pose, expr, decor, icon = build_map.TEXTES[bid][1:]
        it = dict(it)
        it["prompt"] = prompt(pose, expr, decor, icon, it["bucket"])
        out.append(it)
    json.dump(out, open(os.path.join(HERE, "prompts_art.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"{len(out)} prompts art sans texte -> prompts_art.json")
    assert "NO HORIZONTAL BAND" in out[0]["prompt"]
    assert "floor continues naturally" in out[0]["prompt"]
    assert "NO TEXT AT ALL" in out[0]["prompt"]
    print("contrôles internes : OK (NO TEXT / NO BAND / floor continues)")


if __name__ == "__main__":
    main()
