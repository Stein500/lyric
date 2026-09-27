#!/usr/bin/env python3
"""Manifeste intégral des 9 nouveaux prompts de la salve 01, à créer AVANT génération.

1 ancre déjà générée + 9 slots ci-dessous = 10 générations dans ce tour.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'assets/nonvi_konou/salve_01_prompts.json'
HERO=('Recurring HERO: fictional Beninese man about 27 years old, naturally average build, '
      'medium-dark brown skin, rounded-oval face, short natural tightly coiled black hair, '
      'short tidy beard, no glasses, deep-indigo short-sleeved collared cotton shirt and '
      'sand-colored trousers, unembellished realistic proportions; exact same features and clothing in every scene.')
SUFFIX=('REALISTIC editorial street photography in Benin, warm golden sunset backlight with a '
        'subtle electric cyan rim light, soft atmospheric haze, amber accents, fine 35mm film grain, '
        'believable skin texture and natural documentary-real cinematic grading, dominant colors indigo amber green.')
BAN=('No text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, '
     'no signage, no flags, no icons, no cropped face, no unnatural fingers, no out-of-frame elements; '
     'head and hands fully in frame, all fingers visible. Flag footer and badge added in precise post-production.')
ZONE=('Center third gently darker and less busy with soft bokeh for centrally placed lyric words; '
      'large dark negative space across the top quarter for Dsky badge; bottom 12 percent '
      'quiet and unobstructed for long Benin flag footer, with no content touching bottom edge.')
DATA=[
 ('s00_intro','INTRO INSTRUMENTALE','Wide establishing shot. A calm Cotonou lagoon at twilight reflects a single amber sunbreak; hero seen from behind on the left third looking toward a new day, full natural figure visible, atmospheric water ripples foreshadowing the lyric wave. Dim-to-moderate luminous intensity.','wide'),
 ('s01_wolof','Wolof TechStein beat wê...','The hero gently taps an unmarked wooden hand drum on a quiet Beninese terrace, concentric ripples of light in a shallow rain puddle echo the rhythm; restrained anticipation, moderate amber intensity.','medium'),
 ('s02_yeah','Yeah... Nonvi konou...','The hero greets a distinct close friend with an open-handed, natural friendly gesture on a pedestrian footbridge, shared smile and early morning rays revealing the city beyond; moderate luminous intensity.','medium-wide'),
 ('s03_on_est_la','On est là, on brille, on remercie...','The hero and his friend share a grateful pause beside a small market at dusk; one warm lantern reflection brightens their faces like quiet stars, everyday dignity and community rather than luxury; full amber intensity.','medium'),
 ('s05_misere','Gbè manfo do ohin min, la vie ne finit pas dans la misère','The hero walks beside his friend out of a gently shadowed lane into a broad welcoming patch of sunlight; hopeful forward motion, no images of violence or distress, bright full intensity.','wide'),
 ('s06_dokpe','Dokpè nou mahou nou kpèè or, remercie Dieu pour le peu','Close-up on the hero’s naturally proportioned open palms cupping a tiny sunlit seed while his recognizable face remains clearly visible, grateful expression, a modest table with water in soft bokeh; warm medium intensity, no religious writing.','close-up'),
 ('s07_vivi','Gbètché vivi, ma vie me plaît, je suis heureux','The hero laughs joyfully among friends outdoors under leafy shade, authentic relaxed expressions and ordinary cotton clothes; one ray of sunlight catches his smile, warm full intensity.','medium-wide'),
 ('s08_beat','Wolof TechStein beat wê!','The hero takes a rhythmic dance step on a clean rain-darkened street beside his friend, tiny reflections of sunset light tremble in the puddles as if dancing too; full lively intensity, natural anatomy.','wide'),
 ('s09_millions','J’ai pas besoin de millions pour sourire','The hero smiles genuinely at the first rays of morning from a modest balcony, no banknotes, no gold, no luxury; a close friend seen in soft distance; gratitude rather than wealth, warm moderate intensity.','medium'),
]

def main():
    items=[]
    for slug,lyric,visual,plan in DATA:
        blocks=[
            'CADRAGE: vertical 9:16 portrait composition, tall framing, Beninese setting, clear photographic depth.',
            'SUJET-VERS: '+visual,
            'HEROS: '+HERO,
            'PLAN: '+plan+' composition, hero on left third where appropriate, focal light in a single place.',
            'SUFFIXE: '+SUFFIX,
            'ZONE: '+ZONE,
            'INTERDITS: '+BAN,
        ]
        items.append(dict(slot=slug,lyric=lyric,blocks=blocks,prompt=' '.join(blocks)))
    OUTPUT.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Prompts complets écrits avant lancement :', OUTPUT, len(items))
    for p in items:print(p['slot'],p['lyric'])

if __name__=='__main__': main()
