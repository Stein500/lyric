#!/usr/bin/env python3
"""Écrit les dix prompts COMPLETS de la salve 02 avant toute génération IA.

Ne mentionner ni drapeau ni badge dans les prompts d'image : leur mention a causé
les artefacts de salve 01. Ces incrustations sont faites en post-production.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'assets/nonvi_konou'
HERO=('Recurring HERO: fictional Beninese man about 27 years old, naturally average build, '
      'medium-dark brown skin, rounded-oval face, short natural tightly coiled black hair, '
      'short tidy beard, no glasses, deep-indigo short-sleeved collared cotton shirt and '
      'sand-colored trousers, unembellished realistic proportions; exact same features and clothing in every scene.')
SUFFIX=('REALISTIC editorial street photography in Benin, warm golden sunset backlight with a '
        'subtle electric cyan rim light, soft atmospheric haze, amber accents, fine 35mm film grain, '
        'believable skin texture and natural documentary-real cinematic grading, dominant colors indigo amber green.')
ZONE=('Calm, slightly darker CENTER THIRD with photographic bokeh and room for a centered two-line '
      'lyric overlay; generous dark negative space in the top quarter; bottom eighth shows only '
      'ordinary natural scenery, quiet enough for later graphic compositing.')
NO=('No text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no '
    'signage, no medallions, no circular ornaments, no decorative stripes; authentic camera scene only. '
    'Uncropped faces, heads and hands fully within the image, natural number of fingers, no artificial beauty retouching.')
# slot, vers EXACT, métaphore VISUELLE, plan, énergie
DATA=[
 ('s10',"J'ai pas besoin de leur approbation pour vivre",
  'The hero walks toward warm daylight along a neighborhood street while a few indistinct passersby stay out of focus behind him; he chooses his own path with a serene smile, without looking for anyone’s judgment or approval.', 'medium-wide', 'moderate'),
 ('s11','Dokpè, je remercie pour ce que j\'ai',
  'At a modest family table the hero slowly raises a clear glass of water in quiet gratitude; a single amber ray illuminates the glass and his sincere face, humble abundance rather than riches.', 'medium', 'moderate'),
 ('s12','Un toit, un repas, une famille, la santé',
  'The hero shares a simple meal with a small multigenerational family beneath the shelter of a plain courtyard roof; attentive smiles and healthy everyday warmth, no staged perfection.', 'wide', 'full'),
 ('s13','Nonvi konou, regarde mon frère, il brille',
  'The hero looks proudly toward his close friend as a natural low sunbeam falls on that friend’s smiling face in a Beninese street; friendship is the light, no supernatural aura or ornaments.', 'medium', 'full'),
 ('s14','On a connu la galère, maintenant on rit',
  'The hero and the friend laugh at a quiet street corner just after a rainstorm, wet pavement catches the returning sun; their easy mutual relief implies yesterday was difficult but today is light.', 'medium-wide', 'full'),
 ('s15',"Gbè manfo do ohin min, la misère n'est pas notre fin",
  'The hero steps through an open doorway from a dim modest room toward a sunlit green courtyard, friend walking beside him; believable transition from difficulty to hope without any depiction of suffering.', 'wide', 'moderate-to-full'),
 ('s16','On avance, on progresse, on trace notre chemin',
  'The hero takes a confident walking step on a long sandy lane with puddles reflecting sky; its perspective leads clearly toward a single amber opening on the horizon, friend slightly behind.', 'wide', 'full'),
 ('s17',"Wanyiyi dans nos cœurs, c'est ça notre force",
  'The hero helps his friend carry a basket of fresh produce in an ordinary courtyard, hands cooperating and expressions affectionate; one soft glow of late sunlight falls exactly where their hands meet.', 'medium', 'moderate'),
 ('s18',"Dagbé dans nos rires, c'est ça notre torque",
  'The hero and two friends share unforced laughter next to a welcoming street produce stall; warm light reflected in a small puddle visually ripples outward like the energy of their laughter.', 'medium-wide', 'full'),
 ('s19','Gbètché vivi, on crie notre joie',
  'The hero and a few friends celebrate together under trees with open arms and delighted natural faces, no microphones or stage; a single warm backlight captures a fleeting joyous shout.', 'wide', 'full'),
]

def main():
    plan=json.loads((DIR/'plan_images.json').read_text())
    items=[]
    for i,(slug,lyric,visual,shot,light) in enumerate(DATA,10):
        assert plan[i]['text']==lyric and plan[i]['slot']==slug and plan[i]['status']=='pending', (i,plan[i],lyric)
        blocks=[
            'CADRAGE: vertical 9:16 portrait cinematic composition, tall framing, documentary-real Beninese environment.',
            f'SUJET-VERS: {visual} Light intensity: {light}. Visual metaphor only, never write the lyric in the image.',
            'HEROS: '+HERO,
            f'PLAN: {shot}, hero on left third where practical, one photographic luminous focal point, accurate anatomy.',
            'SUFFIXE: '+SUFFIX,
            'ZONE: '+ZONE,
            'INTERDITS: '+NO,
        ]
        items.append(dict(slot=slug,lyric=lyric,blocks=blocks,prompt=' '.join(blocks)))
    outfile=DIR/'salve_02_prompts.json'
    outfile.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
    print('10 prompts intégralement écrits avant toute génération :', outfile)
    for x in items:print(x['slot'],x['lyric'])

if __name__=='__main__':main()
