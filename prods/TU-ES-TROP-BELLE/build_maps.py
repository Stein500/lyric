#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit verses_map.json + prompts_art.json pour « Tu es trop belle » (prod v6.3)."""
import json, re, os, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(BASE))
SRC = os.path.join(REPO, "Tu es trop belle.txt")

SONG_END = 205.08          # durée réelle du master (ffprobe)
ACCUEIL_END = 6.0          # carte SALUT 2x3.0s (libère le 1er vers à 6.16, cf §5.6)

# ---------- 1. parse du fichier de paroles ----------
verses = []
with open(SRC, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        m = re.match(r"\[(\d+):(\d+\.\d+)\](.+)", line)
        if m:
            t0 = int(m.group(1)) * 60 + float(m.group(2))
            verses.append({"t0": round(t0, 2), "texte": m.group(3).strip()})
assert len(verses) == 50, len(verses)

VOW = set("aeiouyàâäéèêëîïôöùûüÿœ")
def syllables(t):
    t = t.lower()
    n, prev = 0, False
    for ch in t:
        v = ch in VOW
        if v and not prev: n += 1
        prev = v
    # e muets finaux
    words = re.findall(r"[\w'’-]+", t)
    silent = sum(1 for w in words if re.search(r"(?<![aeiouyàâäéèêëîïôöùûüÿ])es?$", w) and len(w) > 2)
    return max(2, n - 0.6 * silent)

HOOK = re.compile(r"^(I'm scared|T'es trop belle|Wolof TechStein)")
for i, v in enumerate(verses):
    s = syllables(v["texte"])
    rate = 0.34 if HOOK.match(v["texte"]) else 0.27
    est = rate * s + 0.80
    nxt = verses[i + 1]["t0"] if i + 1 < len(verses) else SONG_END
    v["fin"] = round(min(v["t0"] + est, nxt - 0.12), 2)
    v["syll"] = round(s, 1)

# ---------- 2. plans d'art (32) ----------
# plan -> (vers index 0-based, bucket, pose, expression, décor, symbole)
PLANS = [
    ( 0,"nuit", "standing tall in the pouring rain, chin slightly up, hands relaxed at his sides", "calm and steady, a flicker of awe in his eyes", "a narrow city street with abstract spray-painted walls, wet asphalt", "star"),
    ( 1,"nuit", "one hand pressed over his heart, the other open with the palm up", "flustered and sincere, brows slightly raised", "a quiet alley of abstract mural shapes, puddles reflecting light", "crescent moon"),
    ( 2,"nuit", "leaning back against a graffiti wall, arms crossed, looking down at the camera", "shy confidence, a half-smile", "an abstract mural wall of bold black shapes, rain streaks", "lightning bolt"),
    ( 3,"nuit", "mid-step walking toward the camera through the rain, shoulders squared", "determined but soft-eyed", "a long street receding into darkness, streetlight haze", "musical note"),
    ( 4,"nuit", "head turned three-quarters, jacket collar raised", "melancholy, eyes lowered then lifted", "a wet crosswalk and abstract painted wall panels", "flame"),
    ( 5,"nuit", "both hands raised, palms forward, as if shyly surrendering", "overwhelmed, laughing softly in the rain", "a corner of abstract graffiti shapes under a lamp", "diamond"),
    ( 6,"nuit", "standing still, head tilted, listening", "serene, present", "a dark doorway framed by abstract painted shapes", "wing"),
    ( 7,"nuit", "hands in his jacket pockets, steady stance, feet apart", "quiet and grounded", "an industrial wall of abstract spray shapes, light rain", "spiral"),
    ( 8,"nuit", "one fist pressed to his chest, jaw set", "resolute, intense gaze up at the camera", "a tunnel mouth with abstract graffiti sides", "water drop"),
    ( 9,"nuit", "looking up over his shoulder at the camera", "startled, vulnerable", "a rain-slick stairway with abstract painted walls", "crown"),
    (10,"nuit", "arms wide open, jacket soaked, face up to the rain", "ecstatic surrender", "a rooftop against a black sky, abstract mural below", "arrow"),
    (11,"nuit", "crouched low, elbows on knees, looking up through the rain", "tired and tender", "a flooded pavement, abstract reflection shapes", "eye"),
    (12,"nuit", "pointing at himself with his thumb, wry half-smile", "self-mocking, warm", "a bus stop against an abstract painted panel", "star"),
    (13,"nuit", "walking away and glancing back at the camera", "hesitant, caught between fear and longing", "a long alley of abstract shapes, rain in the light", "crescent moon"),
    (14,"nuit", "standing straight on a rooftop edge silhouette, hands at his sides", "heroic and calm", "city rooftop, black sky, abstract mural parapet", "lightning bolt"),
    (15,"nuit", "one arm shielding his eyes from the light, the other clenched", "shaken, defiant", "a harsh streetlight cone in the rain, abstract wall", "musical note"),
    (16,"nuit", "both hands clasped together in front of him", "hopeful, almost praying", "a quiet corner of abstract spray shapes", "flame"),
    (17,"nuit", "leaning forward from the waist, intense gaze at the camera", "urgent, sincere", "a dark street with one glowing abstract mural", "diamond"),
    (18,"nuit", "standing straight, both fists clenched at his sides", "pent-up, trembling with resolve", "an underpass with abstract graffiti arches", "wing"),
    (19,"nuit", "shrugging with open palms, gentle eyes", "disarming, honest", "a plain wall of soft abstract shapes, drizzle", "spiral"),
    (20,"nuit", "head bowed then lifted, rain dripping from his hair", "raw emotion, eyes shining", "a downpour in a narrow abstract-painted lane", "water drop"),
    (21,"nuit", "one hand reaching toward the camera, the other on his heart", "yearning, exposed", "an open plaza with abstract mural fragments", "crown"),
    (22,"nuit", "leaning on a railing, ankles crossed", "reflective, half-amused", "a bridge railing over abstract painted concrete", "arrow"),
    (23,"nuit", "sitting on stairs, elbows on knees, chin on clasped hands", "dreamy, smitten", "wide wet stairs with abstract riser art", "eye"),
    (24,"aube-a", "standing in the middle of a crosswalk, arms loose", "open, unguarded", "a misty crosswalk at first light, abstract walls", "star"),
    (25,"aube-a", "hand on his forehead, laughing softly, shoulders dropping", "relieved, charmed", "a dawn-lit street of pale abstract shapes", "crescent moon"),
    (26,"aube-a", "marching forward, jacket flaring, determined stride", "fierce and joyful", "a broad avenue in morning mist, abstract murals", "lightning bolt"),
    (27,"aube-a", "standing under a streetlight, face tilted up into the rain", "luminous, at peace", "a lamp post glow over pale abstract wall shapes", "musical note"),
    (28,"aube-a", "both arms crossed over his chest, defiant", "proud, chin high", "a pale skyline of abstract rooftops, thin rain", "flame"),
    (29,"aube-a", "open-handed gesture toward the sky, head back", "ecstatic, free", "bright overcast sky over abstract painted walls", "diamond"),
    (30,"aube-b", "one knee down, one fist on the ground, rising", "triumphant, gentle", "a gleaming wet street in pale morning light", "wing"),
    (31,"aube-b", "standing calm, hands folded, gentle smile, rain easing", "serene gratitude", "a bright morning street, drizzle thinning, abstract murals", "spiral"),
]
assert len(PLANS) == 32

# vers 0..49 -> plan (P01..P32) : v24 réutilise P07 (même tag)
PLAN_OF_VERSE = [
    1, 2, 3, 4, 5, 6, 7,        # v1..v7 (v7 tag = P07)
    8, 8, 9, 9,                 # v8..v11
    10, 10, 11, 11,             # v12..v15
    12, 12, 13, 13,             # v16..v19
    14, 15, 16, 17,             # v20..v23 chorus B
    7,                          # v24 tag -> P07
    18, 18, 19, 19, 20, 20, 21, 21,  # v25..v32
    22, 22, 23, 23,             # v33..v36
    24, 24, 25, 25, 26, 26, 27, 27,  # v37..v44 pont
    28, 29, 30, 31,             # v45..v48 chorus C
    32, 32,                     # v49..v50 outro
]
assert len(PLAN_OF_VERSE) == 50

EN_LINE = "I'm scared of you, I'm scared of you"
PILL_WORDS = ["J'ai", "peur", "de", "toi", "J'ai", "peur", "de", "toi"]

for i, v in enumerate(verses):
    v["id"] = f"v-{i+1:02d}"
    v["plan"] = f"p-{PLAN_OF_VERSE[i]:02d}"
    v["pill"] = PILL_WORDS if v["texte"] == EN_LINE else None
    v["extinguish"] = bool(v["pill"])   # §5.4 : seulement pour céder la place à la pilule FR
    # découpe en lignes peintes (§4 boîte x150→590 / y470→750)
    words = v["texte"].split()
    if len(words) <= 3:
        lines = [v["texte"]]
    else:
        # coupure équilibrée en 2 (3 si vraiment long)
        nlines = 2 if len(v["texte"]) <= 44 else 3
        per = -(-len(words) // nlines)
        lines, cur = [], []
        for w in words:
            cur.append(w)
            if len(cur) >= per and len(lines) < nlines - 1:
                lines.append(" ".join(cur)); cur = []
        if cur: lines.append(" ".join(cur))
    v["lignes"] = lines

# ---------- 3. fenêtres CTA (§6) ----------
cands = []
for i, v in enumerate(verses):
    nxt = verses[i + 1]["t0"] if i + 1 < len(verses) else SONG_END
    a, b = v["fin"] + 0.55, nxt - 0.45
    if b - a >= 2.6:
        if b - a > 5.7: b = a + 5.6   # fenêtre max ~5.6 s (exemples validés 5.0–5.7)
        cands.append([round(a, 2), round(b, 2)])
# fusion des fenêtres jointives — calées sur l'analyse vocale (bande 300-3400 Hz)
# deux vrais souffles : 51.3-54.0 s (après v11) et l'outro 196.6-204.9 s
windows = [[51.6, 53.65], [197.2, 202.8]]

# ---------- 4. JSON ----------
bucket_of = {f"p-{i+1:02d}": b for i, (vi, b, *rest) in enumerate(PLANS)}
verses_map = {
    "titre": "TU ES TROP BELLE",
    "artiste": "DSKY",
    "badge": "Dsky",
    "serie": "WTBW · Wolof TechStein beat wê !",
    "recette": "STUDIO ANIME SEINEN N&B",
    "mode": "B — hybride (VO peinte + pilule FR sur passages EN)",
    "master": "Tu es trop belle.mp3",
    "song_end": SONG_END,
    "fin_video": round(SONG_END + 5.0, 2),
    "accueil": [[0.0, 3.0], [3.0, ACCUEIL_END]],
    "cta_windows": windows,
    "verses": verses,
}
with open(os.path.join(BASE, "verses_map.json"), "w", encoding="utf-8") as f:
    json.dump(verses_map, f, ensure_ascii=False, indent=1)

HEADER = ("Vertical 9:16 gritty adult seinen manga-style anime illustration, black and white only, "
 "heavy ink blacks, fine halftone screentone shading, hard dramatic contrasts, fine rain, "
 "cinematic low-angle framing, keeping the exact same protagonist and visual style as the reference image. "
 "The canvas is 768 px wide and 1376 px tall; all coordinates are on this native canvas.")
BUCKETS = {
 "nuit": "Night scene: deep black shadows, fine cold rain streaks, one harsh streetlight from above, high-contrast monochrome.",
 "aube-a": "First grey dawn light through the rain, misty air, soft luminous sky, medium-contrast monochrome.",
 "aube-b": "Bright pale overcast morning, rain thinning to a drizzle, luminous white sky, high-key monochrome with deep ink accents.",
}
NO_TEXT = ("IMPORTANT — NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol "
 "anywhere in the image, not on the walls, not on clothing, not on signs: the whole spray-painted mural and "
 "graffiti background must be pure abstract shapes and colour splashes only.")
NO_BAND = ("IMPORTANT — NO HORIZONTAL BAND. The picture is one continuous scene: absolutely no band, strip, panel, "
 "rectangle, frame, seam, colour break or gradient line running across the image, and no zone that looks pasted "
 "or masked. Keep the décor naturally calmer and darker around his torso (roughly the middle third) simply as a "
 "lighting choice — deep ambient shadow — never as a drawn shape.")
STICKERS = ("Below that calm area, paint exactly 2 stylish urban graffiti sticker icons side by side, floating like "
 "glowing spray-paint decals in the dark calm zone right below his chest: their centre MUST sit between y 790 and "
 "y 900 from the top of the 1376 px canvas (about 58 to 65 percent down the image), inside x 170 -> 600. Do NOT "
 "paint them lower: absolutely nothing important near the bottom edge, nothing on his legs or trousers. These two "
 "icons are the only graphic marks allowed, and no letters inside them: a glowing street-art heart and {sym}, "
 "each about 90 px tall, linked by a thin luminous white line.")
TAIL = ("The floor continues naturally from the stickers down to the bottom edge as one single surface, slowly "
 "sinking into deeper shadow, with no seam, no line and no change of texture. Nothing in the top 100 px, "
 "nothing on the right side beyond x 647, no flag, no logo, no watermark.")

prompts = []
for i, (vi, bucket, pose, expr, decor, sym) in enumerate(PLANS):
    p = (f"{HEADER}\n\nFraming: half-body shot — exactly ONE character, a stylish young man in a dark fitted "
         f"streetwear jacket, his head (uncovered, face fully visible, nothing over the forehead) sits between "
         f"y 190 and y 400, his shoulders and arms between y 400 and y 465, and the frame cuts his hips at the "
         f"bottom edge. Pose: {pose}. His expression: {expr}. Behind him, an attenuated background: {decor}; "
         f"{BUCKETS[bucket]}\n\n{NO_TEXT}\n\n{NO_BAND}\n\n"
         f"{STICKERS.format(sym=sym)}\n\n{TAIL}")
    prompts.append({"plan": f"p-{i+1:02d}", "bucket": bucket, "symbole": sym, "prompt": p})

COVER = (f"{HEADER}\n\nFraming: a tight heroic bust shot — exactly ONE character, a stylish young man in a dark "
 "fitted streetwear jacket. His head is large and centred, between y 300 and y 720, looking straight into the "
 "camera; face fully visible, nothing over the forehead. Shoulders and chest fill the width between y 720 and "
 "y 1180. The area between y 760 and y 1200 must stay a calm, dark, uncluttered zone of his jacket and deep "
 "shadow — that is where the title will be placed later. Expression: radiant quiet confidence, gentle eyes, "
 "slight smile. Behind him: a wall of abstract spray-painted mural shapes at luminous golden dawn (rendered in "
 "monochrome), rim light on his cheekbones, thin drizzle. "
 f"{NO_TEXT}\n\n{NO_BAND}\n\nBetween y 1240 and y 1340 and inside x 170 -> 600, paint 2 stylish urban graffiti "
 "sticker icons side by side (the only graphic marks allowed, no letters inside them): a glowing street-art "
 "heart and a star, each about 90 px tall, linked by a thin luminous white line.\n\n{TAIL}")
prompts.append({"plan": "cover-tiktok", "bucket": "aube-b", "symbole": "star", "prompt": COVER})

with open(os.path.join(BASE, "prompts_art.json"), "w", encoding="utf-8") as f:
    json.dump(prompts, f, ensure_ascii=False, indent=1)

# ---------- 5. rapport ----------
print(f"vers: {len(verses)} | plans: 32 | fenêtres CTA: {len(windows)}")
for w in windows: print(f"  CTA {w[0]:7.2f} -> {w[1]:7.2f}  ({w[1]-w[0]:.2f}s)")
print("buckets:", {b: sum(1 for x in PLANS if x[1] == b) for b in ("nuit","aube-a","aube-b")})
