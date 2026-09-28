#!/usr/bin/env python3
"""Écrit les 10 prompts complets YouTube 16:9 avant l'unique salve IA."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/nonvi_konou/youtube_16x9/salve_01_prompts.json'
HERO = (
    'Recurring HERO, matching the supplied fictional identity reference only: Beninese man about 27 years old, '
    'naturally average build, medium-dark brown skin, rounded-oval face, short natural tightly coiled black hair, '
    'short tidy beard, no glasses, deep-indigo short-sleeved collared cotton shirt and sand-colored trousers, '
    'unembellished realistic proportions; keep the same face and clothing while creating an entirely new wide scene.'
)
STYLE = (
    'REALISTIC cinematic editorial photography in Benin, warm golden-hour or blue-hour backlight, subtle cyan rim, '
    'soft atmospheric haze, amber accents, believable natural skin texture, restrained fine 35mm grain, '
    'documentary-real color grade, dominant indigo amber and green, one luminous focal point.'
)
ZONE = (
    'Keep a calm gently darker central band for later lyric compositing, broad photographic breathing room, '
    'an uncluttered upper-center area, and a quiet narrow lower edge for precise post-production. '
    'No important face, hand, feet, object, or architecture touching the frame edges.'
)
NO = (
    'No text, no letters, no numbers, no logos, no watermark, no subtitles, no border, no signage, '
    'no medallions, no circular ornaments, no decorative stripes. Natural anatomy, complete hands, believable fingers, '
    'uncropped heads and faces, no artificial beauty retouching, no luxury fantasy.'
)
# output slot, source slot, exact verse, visual metaphor, shot, light
DATA = [
    ('y00_intro', 's00_intro', 'INTRO INSTRUMENTALE',
     'A calm Cotonou lagoon at twilight reflects a single amber break in the clouds; the hero is seen from behind on the far left third looking toward the horizon, while gentle water ripples lead across the wide frame toward a new day.',
     'wide establishing landscape', 'dim-to-moderate'),
    ('y01_wolof', 's01_wolof', 'Wolof TechStein beat wê...',
     'On a quiet Beninese terrace the hero gently taps an unmarked wooden hand drum; small concentric ripples in a shallow rain puddle catch the sunset rhythm, with open street depth extending across the right side.',
     'medium-wide environmental', 'moderate'),
    ('y02_yeah', 's02_yeah', 'Yeah... Nonvi konou...',
     'The hero greets a distinct close friend with an open-handed natural gesture on a pedestrian footbridge; their shared smile and early rays reveal the city and lagoon stretching behind them.',
     'wide two-person', 'moderate'),
    ('y03_on_est_la', 's03_on_est_la', 'On est là, on brille, on remercie...',
     'The hero and his friend share a grateful pause beside a modest neighborhood market at dusk; one warm lantern reflection brightens their faces, expressing everyday dignity and community rather than wealth.',
     'medium environmental', 'full amber'),
    ('y04_nonvi_sourit', 'ancre_01', 'Nonvi konou, mon frère sourit',
     'The hero walks with his close friend on a lively Beninese street at golden hour, laughing with an arm resting naturally around his friend; one warm sun flare anchors their genuine friendship in a spacious horizontal streetscape.',
     'medium-wide two-person', 'full joyful'),
    ('y05_misere', 's05_misere', 'Gbè manfo do ohin min, la vie ne finit pas dans la misère',
     'The hero and friend walk out of a gently shadowed neighborhood lane into a broad welcoming patch of sunlight; the road perspective opens across the frame toward hope, without depicting violence or distress.',
     'wide forward-moving', 'bright full'),
    ('y06_dokpe', 's06_dokpe', 'Dokpè nou mahou nou kpèè or, remercie Dieu pour le peu',
     'The hero sits at a modest outdoor table and holds a tiny sunlit seed in naturally open palms; his recognizable grateful face remains clear while a glass of water and simple courtyard fall into soft bokeh.',
     'medium close environmental', 'warm moderate'),
    ('y07_vivi', 's07_vivi', 'Gbètché vivi, ma vie me plaît, je suis heureux',
     'The hero laughs joyfully with two friends outdoors under leafy shade; authentic relaxed expressions, ordinary cotton clothes, and one ray of sunlight catching his smile, with room around the group.',
     'medium-wide group', 'warm full'),
    ('y08_beat', 's08_beat', 'Wolof TechStein beat wê!',
     'The hero takes a rhythmic dance step on a clean rain-darkened street beside his friend; tiny sunset reflections tremble across puddles as if dancing too, in a broad energetic streetscape.',
     'wide dynamic', 'full lively'),
    ('y09_millions', 's09_millions', "J'ai pas besoin de millions pour sourire",
     'The hero smiles genuinely at the first rays of morning from a modest open balcony; no display of wealth, his close friend soft in the distance, and a wide city-lagoon view expressing gratitude.',
     'medium-wide environmental', 'warm moderate'),
]

def main():
    plan = json.loads((ROOT / 'assets/nonvi_konou/plan_images.json').read_text())
    by_slot = {x['slot']: x for x in plan}
    items = []
    for output, source, lyric, visual, shot, light in DATA:
        assert by_slot[source]['text'] == lyric, (source, by_slot[source]['text'], lyric)
        blocks = [
            'CADRAGE: horizontal 16:9 YouTube landscape composition, cinematic wide framing, authentic Beninese setting.',
            f'SUJET-VERS: {visual} Light intensity: {light}. Visual metaphor only; never write the lyric inside the image.',
            'HEROS: ' + HERO,
            f'PLAN: {shot}; place the hero on a lateral third where practical and preserve layered photographic depth.',
            'STYLE: ' + STYLE,
            'ZONE: ' + ZONE,
            'INTERDITS: ' + NO,
        ]
        prompt = ' '.join(blocks)
        assert all(term not in prompt.lower() for term in ('flag', 'badge', 'drapeau'))
        items.append({'slot': output, 'source_slot': source, 'lyric': lyric,
                      'blocks': blocks, 'prompt': prompt})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n')
    print('10 prompts paysage complets écrits AVANT génération :', OUT)
    for item in items:
        print(item['slot'], '<-', item['source_slot'], item['lyric'])

if __name__ == '__main__':
    main()
