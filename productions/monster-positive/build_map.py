#!/usr/bin/env python3
"""build_map.py — parse LRC paroles + master, génère verses_map.json, CARTE-VERS.md, prompts_art.json.
Contrat v6.4 §10.3 : {i, t, fin, affichage_s, texte, image, lignes, traduction, langue, bucket, reprise, disponible}.
"""
import json, os, re, subprocess, textwrap, zlib

ROOT = os.path.dirname(os.path.abspath(__file__))
FFMPEG = "/usr/local/lib/python3.13/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v9.0.2"
PAROLES = os.path.join(ROOT, "paroles.txt")
MASTER = os.path.join(ROOT, "master_Daïsky.m4a")

# --- durée décodée de l'audio maître (jamais modifié) ---
out = subprocess.run([FFMPEG, "-i", MASTER, "-map", "0:a:0", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
m = re.findall(r"time=(\d+):(\d+):([\d.]+)", out)
D = max(int(h) * 3600 + int(mm) * 60 + float(s) for h, mm, s in m)
print(f"durée audio décodée: {D:.2f} s")

# --- parse LRC ---
verses = []
for line in open(PAROLES, encoding="utf-8"):
    line = line.strip()
    mm = re.match(r"\[(\d+):(\d+\.\d+)\](.*)", line)
    if mm:
        t = int(mm.group(1)) * 60 + float(mm.group(2))
        texte = mm.group(3).strip()
        if texte:
            verses.append({"t": round(t, 2), "texte": texte})
print(f"{len(verses)} vers parsés")

# --- traduction FR (pilule défilante §5.7) pour les passages non français ---
TRAD = {
 1:"On a dit malédiction… moi j'en ai fait ma force.",
 2:"J'étais enfermé dans l'ombre, à me battre contre moi-même.",
 3:"Chaque miroir montrait un monstre — je devenais aveugle.",
 4:"Mais je l'ai regardé dans les yeux : « tu ne gagneras pas. »",
 5:"J'ai changé l'obscurité en armure — plus aucune peur.",
 6:"Des cicatrices, comme une bataille que j'ai survécue.",
 7:"Chaque coup qui voulait me briser m'a rendu plus vivant.",
 8:"Ils ignorent le poids que je portais, chaque nuit.",
 9:"Mais ce poids est devenu mon arme — maintenant je me bats.",
 14:"Monster Positive — je suis la tempête qu'ils n'ont pas vue.",
 15:"Monster Positive — brise chaque chaîne, chaque loi.",
 16:"Ils ont bâti la cage — je suis le mur.",
 17:"Je renais des cendres quand ils m'avaient vu tomber.",
 18:"Monster Positive, Monster Positive.",
 19:"Regarde-moi devenir ce qu'ils disaient impossible.",
 20:"Je sors de la chambre d'ombre, j'entre dans ma lumière.",
 21:"Plus question de cacher ce que je ressens, ce soir.",
 22:"Comme Kamen Rider — je transforme la douleur.",
 23:"Chaque cicatrice devient un signal, chaque perte un gain.",
 24:"Je fuyais mon reflet — maintenant je le porte avec fierté.",
 25:"Ce qu'ils chuchotaient dans le noir, je le dis à voix haute.",
 26:"Je suis la bête et la beauté, le feu et la pluie.",
 27:"On ne peut pas contenir ce qui est libéré — plus de chaîne.",
 38:"Je voulais être quelqu'un d'autre.",
 39:"Tant d'années à avoir peur de moi-même.",
 40:"Chaque monstre a une histoire qu'on n'a pas racontée.",
 41:"La mienne : le feu qui apprend à devenir de l'or.",
 42:"« Tu n'es pas cassé. Tu es en train de devenir. »",
 43:"Monster Positive — JE SUIS la tempête — écoute mon rugissement !",
 44:"Monster Positive — ils n'ont encore rien vu.",
 45:"J'ai fait mes ailes de la douleur de la chute.",
 46:"Maintenant je suis tout — je suis TOUT.",
 47:"Monster Positive, Monster Positive — MONSTER POSITIVE !",
 48:"« On a fait de moi le monstre… j'en ai fait du positif. »",
}
# les vers FR (10-13, 28-31) et la signature wolof (49) : pilule dormante
FR_IDX = {10, 11, 12, 13, 28, 29, 30, 31, 49}

# --- buckets lumière (recalibrés sur D=233.69 s) ---
def bucket(t):
    if t < 140: return "nuit"
    if t < 190: return "aube-a"
    return "aube-b"

# --- (expression, décor, pose, symbole sticker) par vers 1-based ---
SCENES = {
 1:("defiant glare, chin up","dark alley with one flickering neon sign","fists clenched at his sides","lightning bolt"),
 2:("brooding, eyes low then lifting","shadowed stairwell, single shaft of light from above","arms crossed tight over the high collar","chain link"),
 3:("horrified, then resolved","hall of mirrors, all attenuated charcoal","one hand reaching toward his reflection","cracked mirror"),
 4:("fierce stare, unafraid","mirror shard reflecting distant city lights","pointing at his own reflection","broken shard"),
 5:("cold, quiet confidence","darkness swirling around his shoulders like armor plates","standing straight, dark aura coiling","shield"),
 6:("tired but proud half-smile","rain on rooftops at night, all dimmed","rolling up one sleeve, line-art scars","crossed bandage"),
 7:("determined grit between the teeth","boxing-gym shadows, punching bag silhouette","guard up, ready","fist"),
 8:("weary eyes, heavy shoulders","bedroom window, fine night rain","head slightly bowed, then lifting","weight/anvil"),
 9:("fierce, light in his hand raised","storm clouds massing behind him","arm raised, palm open","sword of light"),
 10:("calm defiance, eyes bright","crowd silhouettes behind, heavily attenuated","standing straight, chin up","eye"),
 11:("mysterious half-smile","foggy street at night, lamplight halos","hands in coat pockets, looking away then back","mask"),
 12:("mocking grin","dark forest / storybook shadows closing in","leaning forward, inviting the story","open book"),
 13:("quiet, certain power","first grey edge of dawn at the window","standing still, eyes closed then open","key"),
 14:("roaring intensity, eyes glowing white","lightning storm sky, city below","arms spread wide, storm answering","storm cloud"),
 15:("controlled fury","broken chains on the ground, white sparks","fist crushing a chain link","broken chain"),
 16:("solid, unmovable stare","iron cage bars bending under his shoulder","arms crossed, planted like a wall","cage"),
 17:("triumphant rise","ashes and white ember sparks swirling","rising pose, arms lifting the debris","phoenix flame"),
 18:("chanting intensity, focused","night city skyline behind","both fists raised","double star"),
 19:("victorious grin","single spotlight beam from above","pointing at the viewer","spotlight"),
 20:("blinking into the light","doorway from a dark room into a bright beam","stepping forward, one foot in the light","open door"),
 21:("liberated smile","torn curtain, light pouring through","arms open wide","sun"),
 22:("transformation surge, eyes blazing","rider-like armor of white light forming around his body, energy cracks","henshin pose, arms crossed then bursting out","rider belt / star"),
 23:("wise, calm focus","radio tower in the rain, signal waves","hand over chest scar glowing faintly","signal waves"),
 24:("proud stance, chin up","mirror now showing his confident self","standing before the mirror, shoulders back","mirror"),
 25:("shouting defiance","dark room, visible sound waves","hand cupped at mouth","sound wave"),
 26:("dual calm and fire in the eyes","rain and flame contrast — white streaks only, monochrome","arms half open, rain on one side, glow on the other","drop + flame"),
 27:("wild confident grin, hair swept by wind","broken wall behind him, debris floating","leaning forward, arms loose","burst"),
 28:("unmovable stare","cliff edge at night, wind","standing at the edge, not stepping back","mountain"),
 29:("serene, faint glow around him","his shadow on the ground turning into light","standing over his own shadow","shadow→sun"),
 30:("cold, clear stare","ghostly whisper shapes around, all dimmed","turning his back to them","whisper"),
 31:("guardian stance","glowing boundary line on the ground","one foot on the line, arms at sides","boundary line"),
 37:("victorious grin at dawn","spotlight beam in the sunrise haze (aube-a)","pointing at the viewer, sun behind","spotlight"),
 38:("wistful, then hopeful","shadow of his past self in an old doorway","looking back, then forward","old photo frame"),
 39:("trembling, then steady","cracked mirror, mended with golden light (white in N&B)","hands on the mirror, steadying","mended crack"),
 40:("storyteller calm","open book pages floating in the air, dimmed","holding an open book","book"),
 41:("wonder turning to resolve","forge sparks turning bright white","hands shaping a glowing form","forge spark"),
 42:("gentle, reassuring smile","soft halo of light around him","open palm, reassuring gesture","halo"),
 43:("roaring with joy, mouth open","full sunrise storm sky, lightning, sun rays (aube-b)","roaring pose, head back","roar waves"),
 44:("smirking challenge","sunrise over the city skyline (aube-b)","leaning against a rooftop edge","city sun"),
 45:("awe, wonder","sky with clouds parting, sun rays, white line-art wings unfolding","arms out, wings spreading","wings"),
 46:("transcendent calm","sun blazing directly behind him, halo (aube-b)","arms wide, sun centred","sun halo"),
 47:("triumphant shout","festival light rays, crowd silhouettes cheering (aube-b)","fist raised to the sky","star burst"),
 48:("peaceful, gentle smile","warm quiet sunrise street (aube-b)","relaxed, sun on his face","sunrise"),
 49:("cool, confident nod","sunrise light streaks, calm sky (aube-b)","hand on chest, nodding","lightning bolt"),
}
DEFAULT_SCENE = ("determined expression","attenuated urban night background","standing pose, half-body","star")

def wrap_lines(texte, width=24, maxl=3):
    lines = textwrap.wrap(texte, width=width)
    if len(lines) > maxl:  # re-wrap plus large
        lines = textwrap.wrap(texte, width=34)
    return lines[:4]

# --- plans : 1 plan par vers distinct ; reprise = variante aube si le même texte retombe dans un bucket plus tard ---
seen = {}   # texte -> premier index
plans = {}  # index -> plan filename
for i, v in enumerate(verses, start=1):
    txt = v["texte"]
    b = bucket(v["t"])
    if txt in seen:
        j = seen[txt]
        if bucket(verses[j-1]["t"]) == b:
            plans[i] = plans[j]          # même plan (même lumière)
            continue
        else:
            plans[i] = f"plan-v{i:02d}-aube.png"   # variante aube dédiée (§9)
            continue
    seen[txt] = i
    plans[i] = f"plan-v{i:02d}.png"

# --- contrat ---
cmap = []
for i, v in enumerate(verses, start=1):
    fin = verses[i]["t"] if i < len(verses) else round(D, 2)
    nb = len(v["texte"].split())
    aff = round(min(fin - v["t"], max(2.2, 0.30 * nb)), 2)
    fr = i in FR_IDX
    cmap.append({
        "i": i, "t": v["t"], "fin": round(fin, 2), "affichage_s": aff,
        "texte": v["texte"], "lignes": wrap_lines(v["texte"]),
        "image": os.path.join("fonds", plans[i]),
        "langue": "wolof" if i == len(verses) else ("fr" if fr else "en"),
        "traduction": None if fr else TRAD.get(i),
        "bucket": bucket(v["t"]),
        "reprise": plans[i] != f"plan-v{i:02d}.png" and v["texte"] in seen and seen[v["texte"]] != i,
        "disponible": os.path.exists(os.path.join(ROOT, "fonds", plans[i])),
    })

# --- fenêtres CTA (§6) : [fin_affichage + 0.15 → t vers suivant], seuil 4.0 s ---
cta = []
for c in cmap:
    if c["i"] < len(cmap):
        a, b = c["t"] + c["affichage_s"] + 0.15, cmap[c["i"]]["t"]
        if b - a >= 4.0:
            cta.append([round(a, 2), round(b, 2)])
print("fenêtres CTA:", cta)

os.makedirs(os.path.join(ROOT, "fonds"), exist_ok=True)
json.dump({"titre": "MONSTER POSITIVE", "artiste": "Daïsky", "duree_audio_s": round(D, 2),
           "duree_clip_s": round(D + 5.0, 2), "mode": "HYBRIDE", "verses": cmap, "cta": cta},
          open(os.path.join(ROOT, "verses_map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# --- CARTE-VERS.md ---
with open(os.path.join(ROOT, "CARTE-VERS.md"), "w", encoding="utf-8") as f:
    f.write(f"# CARTE-VERS — MONSTER POSITIVE · Daïsky · {len(cmap)} vers · audio {D:.2f} s · clip {D+5:.2f} s\n\n")
    f.write("| # | t | fin | aff. | bucket | plan | vers | traduction FR (pilule) |\n|---|---|---|---|---|---|---|---|\n")
    for c in cmap:
        tr = (c["traduction"] or "—").replace("|", "\\|")
        f.write(f"| {c['i']} | {c['t']:.2f} | {c['fin']:.2f} | {c['affichage_s']:.2f} | {c['bucket']} | {os.path.basename(c['image'])} | {c['texte'].replace('|','\\|')} | {tr} |\n")

# --- prompts_art.json (un prompt par plan, gabarit §15.1 adapté N&B + NO TEXT AT ALL) ---
BUCKET_FR = {"nuit": "night palette, deep jet black and stark white only",
             "aube-a": "dawn palette — first grey-white light breaking through, still mostly monochrome, faint bright horizon (rendered as pure white glow in this black-and-white piece)",
             "aube-b": "full sunrise palette — blazing white sun and light rays, high-key monochrome with deep black shadows"}
prompts = {}
for i, c in enumerate(cmap, start=1):
    plan = os.path.basename(c["image"])
    if plan in prompts:
        continue
    expr, decor, pose, sym = SCENES.get(i, DEFAULT_SCENE)
    b = c["bucket"]
    prompts[plan] = (
        "Vertical 9:16, dark seinen anime cel-shaded illustration in strict BLACK AND WHITE monochrome "
        "(pure black ink #050608, stark white highlights #FFFFFF, muted charcoal grey #2A2E35, zero color), "
        "same anime protagonist and style as the reference image. The canvas is 768 px wide and 1376 px tall; "
        "all coordinates are on this native canvas.\n\n"
        "Framing: half-body shot — exactly ONE character, the same Black male anime protagonist with short "
        "stylized locks and a closed high-collar black coat. His head (uncovered, face fully visible, nothing "
        "over the forehead) sits between y 190 and y 400; his shoulders and arms between y 400 and y 465; the "
        f"frame cuts his hips at the bottom edge. Pose: {pose}. His expression: {expr}. "
        f"Behind him, an ATTENUATED, darkened, low-contrast charcoal background of {decor}; {BUCKET_FR[b]}. "
        "Keep the middle band around his torso (roughly y 470 to y 950) naturally calm and dark — deep ambient "
        "shadow only — because painted lyrics will be baked there later by the editor.\n\n"
        "IMPORTANT — NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol "
        "anywhere in the image, not on walls, clothing or signs: the background must be pure shapes only.\n\n"
        "IMPORTANT — NO HORIZONTAL BAND. One continuous scene: no band, strip, panel, rectangle, frame, seam, "
        "colour break or gradient line across the image; the calm torso area is a lighting choice, never a "
        "drawn shape.\n\n"
        f"Between y 782 and y 900, inside x 170 -> 600, paint 2 white ink line-art sticker icons side by side "
        f"(the only graphic marks allowed, no letters inside them): a glowing white heart on the LEFT and a "
        f"{sym} on the right, each about 90 px tall, linked by a thin luminous white line. The floor continues "
        "naturally from the stickers to the bottom edge as one single surface sinking into deeper shadow, with "
        "no seam, no line, no texture change. Nothing in the top 102 px, nothing on the right beyond x 647, "
        "nothing below y 1119. No flag, no logo, no watermark."
    )
json.dump(prompts, open(os.path.join(ROOT, "prompts_art.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"plans distincts: {len(prompts)} -> prompts_art.json")
print("verses_map.json + CARTE-VERS.md écrits")
