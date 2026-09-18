"""§C/§E — Assemble les 38 prompts images 9:16 de 'Nan yi a ga djin wê' (charte S6 Braise d'Ascension)."""
import json

HERO = ("young West African man, early twenties, slim average build, short cropped black hair, "
        "faint thin goatee, rectangular dark tortoiseshell-rimmed glasses, silvery-gray metallic "
        "sheen patterned zip jacket over an orange green yellow African wax-print shirt")

S6 = ("semi-realistic seinen anime style, charcoal-black ashy world, rising golden ember particles, "
      "molten gold rim light, deep indigo night accents, faint woven Benin geometric patterns in "
      "shadow textures, cinematic film grain, dramatic volumetric light")

INTERDITS = ("no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, "
             "no signage")
ANTICROP_WIDE = "full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible"
ANTICROP_MED = "three-quarter figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible"
ANTICROP_CU = "head and shoulders completely in frame, no cropped face, no out-of-frame elements"
ZONE_LYRIC = "darker, less busy lower third with soft bokeh for lyric text readability"

FR916 = "vertical 9:16 portrait composition, tall framing"

# slot, intensité, plan, sujet-vers
SLOTS = [
 ("s00_intro", "dim", "wide",
  "vast charcoal-black stone staircase rising into a deep indigo night sky, embers barely glowing at its base like sleeping coals, tiny lone silhouette of HERO at the foot looking up"),
 ("s01", "dim", "medium",
  "HERO standing before a dark ashy wall, faint golden soundwave ripples rising from the ground at his feet, sparse ember dust in the air"),
 ("s02", "moderate", "close-up",
  "close on HERO's determined face tilted slightly upward, golden ember light beginning to bloom reflected in his glasses lenses, sparse sparks drifting past his cheek"),
 ("s03", "moderate", "wide",
  "HERO placing his foot on the first step of the great stone staircase, the step igniting into warm gold under his shoe, long dark stairway stretching up into indigo mist"),
 ("s04", "full", "wide",
  "HERO standing proudly on the blazing staircase, every step behind him lit molten gold, ember sparks swirling upward like a golden river toward the summit light"),
 ("s05", "full", "medium",
  "HERO striding forward through a dense curtain of golden sparks that parts around his body like a curtain of fire, unstoppable posture, fists relaxed but firm"),
 ("s06", "full", "close-up",
  "close on HERO's chest and face, a radiant golden flame glow emanating from his heart, one hand pressed over his chest, embers orbiting him softly, eyes full of faith"),
 ("s07", "full", "medium",
  "HERO tearing open a heavy dark storm-veil of ash clouds with both hands, brilliant golden light flooding through the tear behind him"),
 ("s08", "full", "wide",
  "concentric rings of golden embers erupting from the ground around HERO like visible soundwaves of a beat, dust and sparks pulsing outward in rhythm"),
 ("s09", "dim", "medium",
  "HERO crouched low on dark wet mud ground at night, both palms pressed into the mud, thin golden threads of light rising from his fingers like roots of hope"),
 ("s10", "dim", "close-up",
  "close on HERO's hands counting faint glowing tally marks of light etched in the dark air, tired but resolute expression in shadow"),
 ("s11", "dim", "medium",
  "blurred shadowy silhouettes of mocking figures pointing at HERO from the darkness, HERO standing small but upright, a single warm ember glowing at his chest"),
 ("s12", "moderate", "wide",
  "HERO carving his name into a massive concrete wall at night, the carved grooves glowing molten gold, golden light trails climbing from the wall up into the starry sky"),
 ("s13", "moderate", "medium",
  "HERO shoulder-checking a heavy dark wooden door that bursts into golden splinters of light, stepping through the broken doorway"),
 ("s14", "moderate", "medium",
  "HERO turning his back on a falling dark rain of grey paper refusals, each rejected page igniting into a small golden spark as it passes him, head held high"),
 ("s15", "moderate", "close-up",
  "close on HERO's fierce eyes, ancestral golden spirit silhouettes faintly shimmering behind him like a chorus of elders, ember light on his face"),
 ("s16", "full", "medium",
  "HERO reaching up and gripping a rope of golden fire, pulling himself upward with raw strength, sparks flying from his grip"),
 ("s17", "moderate", "medium",
  "HERO walking calmly past whispering blurred shadow figures leaning in to gossip, their words dissolving into grey smoke before touching him"),
 ("s18", "full", "wide",
  "night city asleep in darkness below while HERO alone shines on a rooftop, a column of golden ember light rising from him into the indigo sky"),
 ("s19", "moderate", "wide",
  "long winding stone road climbing a dark mountain at night, HERO walking it patiently with a small warm ember lantern glow around him, summit star far above"),
 ("s20", "full", "medium",
  "HERO at a starting line of glowing golden footprints, leaning forward bursting into motion, embers trailing behind him like a comet tail"),
 ("s21", "dim", "close-up",
  "close on HERO smiling serenely at a looming skeletal figure of grey smoke dissolving beside him, calm golden light on one side of his face"),
 ("s22", "dim", "medium",
  "HERO standing over a cowering shape of dark fear made of smoke, his shadow cast long and heroic in golden light across the ground"),
 ("s23", "dim", "medium",
  "HERO kneeling briefly beside fallen shadow silhouettes of friends on the roadside, laying down a small golden flower of light in their honor before rising"),
 ("s24", "moderate", "medium",
  "HERO marching forward through strong wind of ash, jacket flapping, one arm shielding his face but legs driving onward, gold embers streaming horizontally"),
 ("s25", "moderate", "medium",
  "dark hands of smoke reaching from below trying to pull HERO down, he transforms their grip into steps, rising above them on a platform of gold light"),
 ("s26", "full", "wide",
  "HERO ascending a vertical shaft of golden light while dark rubble of his past falls away downward, arms slightly spread in triumph"),
 ("s27", "moderate", "close-up",
  "close on HERO's forearm and face, glowing golden scar lines like kintsugi seams on his skin, each scar shining like a small medal of light"),
 ("s28", "full", "medium",
  "HERO standing tall as a floating crown of woven golden embers descends gently onto his head, regal posture, sparks cascading from the crown"),
 ("s29", "dim", "medium",
  "HERO sitting on cracked ground in the rain at night, head bowed, puddles reflecting a faint indigo sky, a tiny gold ember still glowing in his cupped hands"),
 ("s30", "moderate", "medium",
  "HERO rising to his feet from the cracked ground, rain turning to golden dust around him, unbreakable expression, light growing on his outline"),
 ("s31", "moderate", "close-up",
  "close on HERO's face with a single tear turning into a streak of golden light on his cheek, scars of light faintly visible like a map of battles"),
 ("s32", "full", "wide",
  "HERO climbing the final bright steps, whole staircase now a torrent of golden light, summit glow flooding the frame from above"),
 ("s33", "full", "wide",
  "HERO leaping upward off the summit edge into the indigo sky, wings of golden ember sparks unfolding behind him, rising and flying"),
 ("s34", "full", "medium",
  "HERO blazing like a torch mid-air, endless golden trail behind him, mouth open in a victorious shout, no sign of stopping"),
 ("s35", "dim", "wide",
  "whisper-thin golden mist spelling nothing, shaped like a breath of embers drifting over the dark staircase at night, dreamlike and quiet"),
 ("s36", "moderate", "medium",
  "HERO ripping a final dark banner of storm cloth in half with both hands, golden dawn light bursting through the gap behind him"),
 ("s37_endcard", "dim", "wide",
  "quiet dark ash field at night, the great staircase far in the background now softly glowing gold at its summit, large empty darker center area for credits, minimal embers"),
]

out = []
for slot, inten, plan, sujet in SLOTS:
    anticrop = {"wide": ANTICROP_WIDE, "medium": ANTICROP_MED, "close-up": ANTICROP_CU}[plan]
    zone = ZONE_LYRIC if not slot.endswith(("intro", "endcard")) else (
        "large dark negative space across the top quarter and calm darker center" if "intro" in slot
        else "calm darker center with generous negative space for credit text")
    sujet = sujet.replace("HERO", "the same young man")
    prompt = " ".join([FR916 + ".",
                       f"{sujet}, {inten} glow intensity.",
                       f"HERO: {HERO}.",
                       f"{plan} shot.",
                       S6 + ".",
                       zone + ".",
                       INTERDITS + ", " + anticrop + "."])
    out.append({"slot": slot, "intensite": inten, "plan": plan, "prompt": prompt})

json.dump(out, open("work/prompts.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(out)} prompts écrits")
