#!/usr/bin/env python3
"""build_map.py — contrat unique de la prod « On nous a volé notre éducation » (Dsky)
v6.0 — 1 plan par vers distinct, variantes d'aube après le pont (§9), zéro code (§7.1).
Usage : python3 build_map.py
Sorties : verses_map.json, CARTE-VERS.md, prompts.json, ANCRE.md
"""
import json, os, re, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "paroles.source.txt")
FONDS = os.path.join(HERE, "fonds")

TITRE = "On nous a volé notre éducation"
ARTISTE = "Dsky"
AUDIO_DUREE = 205.92          # durée décodée ffmpeg (s)
CARTE_FINALE = 5.00
DAWN_A = 138.00               # pont : premières lueurs
DAWN_B = 176.00               # refrain final : plein soleil

# ----------------------------------------------------------------------------
# 32 textes distincts : 2 lignes peintes + pose + expression + décor + 2 icônes
# palette de base = celle de la première occurrence (bucket), cf. §9
# ----------------------------------------------------------------------------
TEXTES = {
 1:  ("Yeah... On nous a volé notre éducation...", "a defiant wide stance, fists half-closed",
      "defiant anger, jaw tight", "ruined schoolyard at night, cracked concrete, faded hand-painted murals", "a broken book icon"),
 2:  ("Attends... On se relève...", "rising out of a deep crouch, one hand on the ground",
      "jaw set, eyes lifting", "rubble and moonlight over a broken school gate", "a raised fist icon"),
 3:  ("On nous a volé notre éducation", "a sharp mid-air freeze over a fallen backpack",
      "burning anger, brows drawn", "collapsed school gate, torn banners, cold streetlight", "a torn notebook icon"),
 4:  ("Ils ont brûlé nos illusions", "a low krump stomp, shoulders rolled forward",
      "cold fury, lips pressed", "smouldering paper ash drifting over asphalt", "a flame icon"),
 5:  ("On se relève, on est des battants", "a rising pop-and-lock, chest lifted",
      "chin up, resolved", "empty night street with wet asphalt reflections", "a lightning bolt icon"),
 6:  ("Wolof TechStein beat wê!", "arms crossed, relaxed swagger",
      "confident half-grin", "night rooftop above the city, warm window glow", "a speaker icon"),
 7:  ("L'école nous a donné des livres poussiéreux", "sitting on a desk edge, a dusty book in hand",
      "wry tired smile", "abandoned classroom, overturned desks, dust in a light beam", "a stack of books icon"),
 8:  ("Des promesses en l'air, des rêves dangereux", "open arms in an ironic shrug",
      "sardonic smirk", "school corridor walls covered in torn posters fluttering", "a paper plane icon"),
 9:  ("On nous a dit \"travaille, t'auras ta place\"", "a finger pointed forward, head tilted",
      "sardonic challenge", "shattered blackboard and chalk dust", "a chalk piece icon"),
 10: ("Mais on a fini par courir, par faire des grâces", "a sprinter's start, body coiled low",
      "determined, eyes forward", "long empty school corridor with flickering tubes", "a feather"),
 11: ("Les profs nous regardaient de haut, de loin", "still pose, head tipped up",
      "cold stare upward", "tall barred windows, harsh light from above", "an eye icon"),
 12: ("Ils nous voyaient comme des moins que rien", "fists clenched at his sides",
      "gritted teeth, defiant", "narrow shadowed corridor, single bulb", "a cracked mirror icon"),
 13: ("Mais j'ai gardé la rage, j'ai gardé le feu", "a chest-beat hit, elbow sharp",
      "fierce pride", "embers floating over a burnt courtyard", "a flame icon"),
 14: ("J'ai transformé leur mépris en un jeu", "a spinning windmill freeze, arms wide",
      "half-smile, eyes sharp", "graffiti wall lit by one streetlamp", "a dice icon"),
 15: ("Yeah... on se relève...", "a slow rise, shoulders rolling back",
      "exhausted but standing", "night rooftop, skyline breathing", "a star icon"),
 16: ("Yeah... on est des battants...", "a wide grounded stance, arms loose",
      "steady stare to camera", "industrial rooftop, cables, city glow", "a lightning bolt icon"),
 17: ("J'ai vu des jaloux autour de moi", "a guarded half-turn, shoulder leading",
      "side glance, wary", "alley of long shadows and wet brick", "an eye icon"),
 18: ("Ils souriaient tout bas, ils tiraient sur moi", "braced arms crossed high, weight back",
      "cold calm", "concrete stairwell, graffiti tags halfway up", "a broken chain icon"),
 19: ("J'ai vu des gens vouloir me voir tomber", "a low freeze, one knee nearly touching the ground",
      "defiance in the eyes", "crumbling stair edge over darkness", "a broken stair icon"),
 20: ("Plutôt que de me voir m'élever", "one arm reaching straight up, body stretched",
      "hope breaking through anger", "shaft of light falling into a ruined hall", "a rising arrow icon"),
 21: ("Mais j'ai avancé, j'ai pas regardé", "a forward walking stride, head high",
      "unbothered focus", "corridor opening toward the night sky", "a winged shoe icon"),
 22: ("J'ai laissé leurs regards empoisonnés", "shoulders back, one hand brushing the air away",
      "disdain, calm", "smoke curling through a broken window frame", "a snake icon"),
 23: ("La désolation est ma compagne", "a quiet standing pose, hands open",
      "quiet grief, eyes lowered yet visible", "empty lot, dead grass, one working lamp", "a wilted flower icon"),
 24: ("Mais je la dompte, je la baigne", "a commanding arm sweep, weight centred",
      "calm power", "night lot, dust swirling in lamplight", "a chain icon"),
 25: ("Je suis un guerrier, un survivant", "a battle-ready stance, chin down, eyes up",
      "hard resolve", "ruined courtyard with a torn bare flagpole", "a shield icon"),
 26: ("Un homme debout, un battant", "standing tall, feet planted wide",
      "chin lifted, first light in the eyes", "edge of a rooftop facing the horizon", "a rising sun icon"),
 27: ("L'éducation est un champ de ruines", "a crouch on a rubble heap, one arm braced",
      "grief turned to iron", "burning school ruin, embers in the air", "a broken column icon"),
 28: ("Mais je cultive mes propres graines", "a planting gesture, hand pressing the ground",
      "focused tenderness", "ash-black soil with warm ember light", "a sprout icon"),
 29: ("La jalousie est un poison lent", "a slow serpentine isolation move",
      "cold fire in the eyes", "dark alley, dripping pipes, green murk", "a vial icon"),
 30: ("Mais je m'en nourris, j'en deviens plus grand", "arms opening wide, chest expanding",
      "rising strength", "smoke parting around a widening light", "a flame icon"),
 31: ("Wolof TechStein beat wê...", "a relaxed shoulder roll, hands loose",
      "soft confident smile", "rooftop in gold first light", "a star icon"),
 32: ("(On se relève...)", "arms open to the sunrise, head lifted",
      "release, quiet pride", "open field at sunrise, city far behind", "a sun icon"),
}

def painted(text):
    """lignes peintes : mots EXACTS, coupure aux respirations (…) puis aux virgules, sinon équilibre.
    Ponctuation de suspension et guillemets non peints (le modèle les rendait « // ») ;
    la virgule de coupe est retirée, celle qui reste en fin de ligne est conservée."""
    raw = text.replace('"', "").replace("(", "").replace(")", "")
    def norm(x):
        x = x.replace("!", "").replace("...", " ")
        return " ".join(x.split()).upper()

    cands = []
    for i in range(len(raw)):
        if raw.startswith("...", i):
            cands.append(i + 3)
        elif raw[i] == ",":
            cands.append(i + 1)
    for i in cands:
        a, b = norm(raw[:i]).rstrip(","), norm(raw[i:]).strip(", ")
        if 4 <= len(a) <= 27 and 4 <= len(b) <= 27:
            return a, b
    words = norm(raw).replace(",", " ,").split()
    words = [w for w in words if w != ","]
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        if min(len(a), len(b)) < 5:
            continue
        score = (max(len(a), len(b)) > 27, max(len(a), len(b)), abs(len(a) - len(b)))
        if best is None or score < best[0]:
            best = (score, a, b)
    return best[1], best[2]

ICONS = {"love": "a glowing street-art heart ('love' sticker)"}

PALETTES = {
 "nuit": ("deep teal and charcoal night, warm streetlight rim light on his shoulders and cheekbones, cool cyan highlights"),
 "aube-a": ("pre-dawn blue-violet sky with a thin rose-gold horizon, faint warm rim light, deep soft shadows"),
 "aube-b": ("full golden sunrise, warm amber haze, long shadows, luminous gold rim light, sky glowing peach and gold"),
}

def diacritiques(l1, l2):
    """liste courte et exacte des diacritiques présents dans les deux lignes (§4)."""
    acc = "ÉÈÊÀÂÄÔÖÛÙÏÎÇŒÆ"
    found = sorted({c for c in (l1 + l2) if c in acc})
    return ", ".join(found) if found else "none (plain capitals)"

# ----------------------------------------------------------------------------
def slug(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:34]

def parse():
    rows = []
    for line in open(SRC, encoding="utf-8"):
        m = re.match(r"\[(\d+):(\d+)\.(\d+)\](.*)", line.strip())
        if m:
            rows.append((round(int(m.group(1))*60 + int(m.group(2)) + int(m.group(3))/100, 2),
                         m.group(4).strip()))
    merged, i = [], 0
    while i < len(rows):
        t, txt = rows[i]
        if txt == "Attends..." and i+1 < len(rows) and rows[i+1][1] == "On se relève...":
            merged.append((t, "Attends... On se relève...")); i += 2; continue
        merged.append((t, txt)); i += 1
    return merged[1:]                      # la signature d'ouverture appartient à la carte (§7.2)

def bucket(t):
    return "nuit" if t < DAWN_A else ("aube-a" if t < DAWN_B else "aube-b")

def langue(txt):
    return "WTBW" if txt.lower().startswith("wolof techstein") else "FR"

def main():
    vers = parse()
    # id de texte par ordre de première apparition
    ids, order = {}, []
    for t, txt in vers:
        key = txt.strip()
        if key not in ids:
            ids[key] = len(order) + 1
            order.append(key)
    # buckets nécessaires par texte
    need = {}
    for t, txt in vers:
        need.setdefault(txt.strip(), set()).add(bucket(t))
    plan = {}
    for txt, bid in ids.items():
        for b in sorted(need[txt], key=lambda x: ["nuit", "aube-a", "aube-b"].index(x)):
            plan[(txt, b)] = os.path.join(FONDS, f"v-{bid:02d}-{b}.png")

    slots = []
    for i, (t, txt) in enumerate(vers, 1):
        fin = vers[i][0] if i < len(vers) else AUDIO_DUREE
        b = bucket(t)
        img = plan[(txt.strip(), b)]
        words = len(re.findall(r"\S+", txt))
        aff = min(fin - t, max(2.2, 0.30 * words))
        slots.append({
            "i": i, "t": round(t, 2), "fin": round(fin, 3), "affichage_s": round(aff, 3),
            "texte": txt, "langue": langue(txt), "traduction_fr": "",
            "image": os.path.relpath(img, HERE), "disponible": os.path.exists(img),
            "reprise": any(s["image"] == os.path.relpath(img, HERE) for s in slots),
            "lignes": [painted(TEXTES[ids[txt.strip()]][0])[0] or ""],
            "bucket": b, "mots": words,
        })

    # fenêtres de CTA (§6) : [fin d'affichage + 0,15 -> début du vers suivant], seuil 4,0 s
    cta = []
    for k, s in enumerate(slots):
        nxt = slots[k+1]["t"] if k+1 < len(slots) else AUDIO_DUREE
        a, b = s["t"] + s["affichage_s"] + 0.15, nxt
        if b - a >= 4.0:
            cta.append({"debut": round(a, 2), "fin": round(b, 2), "duree": round(b-a, 2), "apres_vers": s["i"]})

    doc = {
        "titre": TITRE, "artiste": ARTISTE, "signature": "Wolof TechStein beat wê !",
        "audio": "On a nous volé notre éducation.mp3",
        "audio_duree_s": AUDIO_DUREE, "carte_finale_s": CARTE_FINALE,
        "clip_duree_s": round(AUDIO_DUREE + CARTE_FINALE, 3),
        "mode": "PEINT (hybride prêt — aucune traduction FR nécessaire : chanson 100 % FR/WTBW)",
        "recette": "WANDANCE BATTLE & GRAFFITI LOVES",
        "debut_premier_vers": slots[0]["t"],
        "cta": cta, "vers": slots,
    }
    json.dump(doc, open(os.path.join(HERE, "verses_map.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # CARTE-VERS.md
    lines = [f"# CARTE-VERS — {TITRE} · {ARTISTE}", "",
             f"Durée audio décodée **{AUDIO_DUREE:.2f} s** · clip **{AUDIO_DUREE+CARTE_FINALE:.2f} s** · "
             f"{len(slots)} vers · {len(plan)} plans", "",
             "| # | t | fin | affichage | langue | vers | plan | dispo |", "|---:|---:|---:|---:|---|---|---|:--:|"]
    for s in slots:
        lines.append(f"| {s['i']:02d} | {s['t']:.2f} | {s['fin']:.2f} | {s['affichage_s']:.2f} | "
                     f"{s['langue']} | {s['texte']} | `{s['image'].split('/')[-1]}` | "
                     f"{'✅' if s['disponible'] else '—'} |")
    lines += ["", "## Fenêtres CTA (clochettes)", ""]
    for c in cta:
        lines.append(f"- après le vers {c['apres_vers']:02d} · {c['debut']:.2f} → {c['fin']:.2f} s ({c['duree']:.2f} s)")
    lines += ["", "## Plans à générer", ""]
    for (txt, b), p in sorted(plan.items(), key=lambda kv: kv[1]):
        lines.append(f"- `{os.path.basename(p)}` — {b} — « {txt} »")
    open(os.path.join(HERE, "CARTE-VERS.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

    # prompts.json (un prompt par plan)
    prompts = []
    for (txt, b), p in sorted(plan.items(), key=lambda kv: kv[1]):
        bid = ids[txt]
        pose, expr, decor, icon = TEXTES[bid][1:]
        l1, l2 = painted(TEXTES[bid][0])
        prompts.append({
            "image": os.path.relpath(p, HERE), "bucket": b, "texte": txt, "lignes": [l1, l2],
            "prompt": prompt_wandance(l1, l2, pose, expr, decor, icon, b),
        })
    json.dump(prompts, open(os.path.join(HERE, "prompts.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print(f"vers={len(slots)} plans={len(plan)} cta={len(cta)} "
          f"dispo={sum(s['disponible'] for s in slots)}/{len(slots)}")
    for p in prompts[:2]:
        print("\n---", p["image"], "\n", p["prompt"])

def cap_h(n):
    """hauteur de capitale native (768 px de large) pour tenir dans 510 px (§4)."""
    return max(19, min(46, int(435 / (0.66 * max(1, n)))))

def prompt_wandance(l1, l2, pose, expr, decor, icon, b):
    pal = PALETTES[b]
    h1, h2 = cap_h(len(l1)), cap_h(len(l2) or 1)
    return (
        "Vertical 9:16 street-dance battle anime illustration in the dynamic style of Wandance combined "
        "with clean, well-ordered, stylish urban graffiti art, keeping the exact same protagonist and visual "
        "style as the reference image. The canvas is 768 px wide and 1376 px tall; all coordinates below are "
        "given on this native canvas.\n"
        "Framing: half-body shot \u2014 his head (uncovered face fully visible, nothing over the forehead) sits between "
        "y 190 and y 400, his shoulders and arms stay between y 400 and y 465, and the frame cuts his hips at the "
        "bottom edge. "
        f"Pose: {pose}. His expression: {expr}. Behind him, an attenuated background: {decor}; {pal}.\n"
        "Lettering layout (layout guide only): keep the painted lettering block inside the rectangle y 470 to "
        "y 750, x 150 to x 590, on this 768x1376 canvas \u2014 a SMALL, tidy tag block, not a poster, with clear "
        "empty background on both sides. IMPORTANT: do NOT draw that rectangle, do NOT draw any panel, card, "
        "plate, border, frame or filled box of any kind; the letters sit directly on the scene over a loose "
        "organic dark ink spray halo with soft torn edges and no straight lines. The background stays visible "
        "between and around the letters.\n"
        + (f"Paint two lines of neat, well-ordered, ultra-legible stylized graffiti block capital letters inside that box. "
           f"The first line has {len(l1)} characters and its capitals are about {h1} px tall; the second line has "
           f"{len(l2)} characters and its capitals are about {h2} px tall.\n"
           f"First line in bold warm white and gold graffiti capitals: \"{l1}\"\n"
           f"Second line below it in crisp cyan-tinted silver-white graffiti capitals: \"{l2}\" "
           f"(keep every accent and apostrophe exactly; the accented capitals in these lines are: {diacritiques(l1, l2)}).\n"
           if l2 else
           f"Paint one single line of neat, well-ordered, ultra-legible stylized graffiti block capitals, centred in "
           f"that box, in bold warm white and gold: \"{l1}\" "
           f"(keep every accent exactly; accented capitals: {diacritiques(l1, '')}).\n")
        + f"Below the text, between y 790 and y 900 and inside x 170 -> 600, paint 2 stylish urban graffiti sticker "
        f"icons side by side: {ICONS['love']} and {icon}, each about 90 px tall, linked by a thin luminous "
        "gold graffiti line.\n"
        "From y 920 down to the bottom edge keep only clean dark concrete floor and his legs: no text, no icons, no "
        "signs. Nothing in the top 100 px, nothing on the right side beyond x 647, no flag, no logo, no watermark, "
        "no other words."
    )

if __name__ == "__main__":
    main()
