#!/usr/bin/env python3
"""
generate_prompts_catalog.py - Catalogue des prompts d'images pour 'Nan yi a ga djin wê'
selon PROMPT_UNIVERSEL_v5.1.1.md
"""

hero_desc = (
    "a young 20-year-old Black West African man with smooth dark brown skin, "
    "rounded short textured afro fade haircut, neat sparse chin goatee fuzz, "
    "warm dark brown almond-shaped expressive eyes, natural authentic slim-athletic build, "
    "wearing a simple clean white short-sleeved t-shirt, completely natural realistic facial features, "
    "no exaggerated muscles, no cosmetic enhancement, authentic true-to-life likeness"
)

suffix_b = (
    "deep blue-black night, warm amber backlight, subtle electric cyan rim light, "
    "wet asphalt reflections, atmospheric haze, crushed blacks with cyan highlights, "
    "moody anime-seinen cinematic grading, 35mm film grain"
)

suffix_a = (
    "warm golden sunset backlight, subtle electric cyan rim light, amber accents, "
    "soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, "
    "moody romantic cinematic grading"
)

prohibitions = (
    "no text, no letters, no numbers, no logos, no watermark, no subtitles, "
    "no borders, no signage, full figure, head and hands completely in frame, "
    "no cropped face, no out-of-frame elements, all fingers visible"
)

slots = [
    ("s00_intro", "empty rainy city street at midnight, deep shadows, wet asphalt reflecting soft distant streetlights, moody atmospheric mist, dim intensity", "wide", suffix_b, "large dark negative space across the top quarter", False),
    ("s01_beat_we", "hero standing looking towards the horizon with calm intense determination, subtle cyan rim light tracing his shoulders, moderate intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s02_yeah_nan_yi", "hero lifting his head with a sharp focused gaze full of inner spark, atmospheric smoke swirling around, moderate intensity", "close-up", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s03_sommet_arrive", "hero looking up toward the distant glowing summit of an urban skyscraper tower beneath stormy clouds, moderate intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s04_refrain_sommet", "hero stepping forward powerfully, clenched fist, dynamic volumetric lightning bolt cutting across the dark sky, full intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s05_refrain_arreter", "hero standing immovable like a statue against a flurry of electric cyan sparks and warm embers, full intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s06_refrain_feu_foi", "hero hands open toward the sky, warm amber fire glow and vibrant cyan energy flowing around him, full intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s07_refrain_dechirer", "hero shattering metaphysical smoke constraints with powerful burst of energy, shockwave across wet ground, full intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s08_beat_we_excl", "hero in triumphant dynamic stance, single bright electric cyan arc lighting the dark avenue, full intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s09_boue_sol", "hero sitting on stone steps in a modest city alley under soft drizzle, reflective humble mood, dim intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s10_defaites_epaules", "hero seen from slight angle straightening his shoulders, looking at his hands, quiet resilient focus, dim intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s11_place_rien", "distant blurred silhouettes in the deep shadows behind, hero walking forward unbothered into the light, moderate intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s12_beton_ciel", "hero placing hand upon rough concrete wall that subtly glows with faint cyan cracks of light, moderate intensity", "close-up", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s13_porte_casse", "hero walking decisively through a massive broken gateway into an open illuminated avenue, moderate intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s14_moteur_audace", "hero walking with confident rhythmic stride down wet urban avenue, amber reflections on pavement, moderate intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s15_rage_ancetres", "hero with passionate fierce expression, warm golden inner fire reflected in eyes, ancient protective mist, moderate intensity", "close-up", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s16_tout_arracher", "hero reaching hand forward decisively, swirling atmospheric cyan mist parting before him, full intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s17_parler_douter", "hero standing completely still and composed at a foggy urban crossroads, distant blurred taillights, moderate intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s18_briller_nuit", "sleeping dark city skyline below, hero standing on a rooftop ledge bathed in clear cyan and gold moonlight, moderate intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s19_route_longue", "long glistening wet highway stretching toward distant illuminated highrises, hero walking steadily ahead, moderate intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s20_maintenant", "hero gazing upward as first rays of energetic cyan-gold dawn break through storm clouds, full intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s21_mort_souri", "hero showing a subtle calm fearless smile facing swirling dark mist, crisp cyan rim lighting, moderate intensity", "close-up", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s22_peur_punie", "hero slashing through hovering shadows with a confident motion of his arm, warm amber sparks dispersing, moderate intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s23_freres_tomber", "hero kneeling with deep respect, one hand gently resting on the wet asphalt, gentle falling embers, dim intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s24_avance_tiens", "hero standing tall again with resolute iron jawline, looking straight at viewer with unbreakable will, moderate intensity", "close-up", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s25_revolte", "hero caught in sudden vortex of wind and electric cyan flashes, defiant heroic stance, full intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s26_ascension", "hero ascending steep monumental urban stone steps leading toward radiant beacon above, full intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s27_cicatrice_medaille", "close-up on hero proud resilient face, warm golden backlight accentuating his features and steady gaze, moderate intensity", "close-up", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s28_couronne", "hero holding head high, subtle elegant constellation of glowing amber floating sparks hovering above like a crown, full intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s29_bridge_broken", "hero leaning against a high urban bridge railing, thoughtful and introspective under gentle dusk sky, soft dim intensity", "medium", suffix_a, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s30_bridge_chosen", "hero standing tall in warm golden sunset haze, soft glowing halo behind silhouette, serene strength, soft moderate intensity", "wide", suffix_a, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s31_bridge_fight", "hero looking at his open hands illuminated by the rich amber glow of setting sun, soft moderate intensity", "close-up", suffix_a, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s32_bridge_shine", "hero smiling with authentic warmth and confident hope, brilliant golden sunset rays illuminating his face, soft full intensity", "close-up", suffix_a, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s33_bridge_fly", "hero standing on high cliff edge overlooking vast city bathed in dusk, arms slightly spread in feeling of freedom, full intensity", "wide", suffix_a, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s34_bridge_never_die", "hero radiating vibrant blend of golden solar light and electric cyan energy, climax of power, full intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s35_outro_echo", "hero sitting peacefully on rooftop parapet looking over glittering night city under starry dark blue sky, dim intensity", "wide", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s36_outro_dechirer", "final dramatic arc of electric cyan lightning touching the dark pavement with dispersing azure particles, full intensity", "medium", suffix_b, "darker, less busy lower third with soft bokeh for lyric text readability", True),
    ("s37_endcard", "minimalist ultra-clean deep charcoal-black asphalt texture with very faint floating cyan dust motes, center dark space, dim intensity", "wide", suffix_b, "center dark negative space for credits and typography", False)
]

def generate_catalog():
    lines = [
        "# 🎬 Catalogue des Prompts Images — Nan yi a ga djin wê (38 slots)",
        "",
        "**Artiste :** Daïsky  ",
        "**Titre :** Nan yi a ga djin wê  ",
        "**Charte :** Hybride S1 Dark Lightning (couplets/refrains) + S2 Golden Sunset (pont doux s29-s33)  ",
        f"**Bloc Héros fidèle (A.6) :** `{hero_desc}`  ",
        "",
        "---",
        ""
    ]
    for slot_id, subject, plan, suffix, zone, has_hero in slots:
        hero_part = f"{hero_desc}, " if has_hero else ""
        prompt_916 = f"vertical 9:16 portrait composition, tall framing, {subject}, {hero_part}{plan} shot, {suffix}, {zone}, {prohibitions}"
        lines.append(f"### Slot `{slot_id}`")
        lines.append(f"- **Sujet :** {subject}")
        lines.append(f"- **Plan :** {plan}")
        lines.append(f"- **Prompt 9:16 :**")
        lines.append(f"  > `{prompt_916}`")
        lines.append("")

    with open("PROMPTS_IMAGES_Nan_yi_a_ga_djin_wê.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Catalogue généré : {len(slots)} prompts -> PROMPTS_IMAGES_Nan_yi_a_ga_djin_wê.md")

if __name__ == "__main__":
    generate_catalog()
