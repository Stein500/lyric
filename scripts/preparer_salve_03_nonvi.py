#!/usr/bin/env python3
"""Écrit l'intégralité des 10 prompts de la salve 03 AVANT génération IA."""
import json
from pathlib import Path
from preparer_salve_02_nonvi import HERO,SUFFIX,ZONE,NO

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'assets/nonvi_konou'
# slot, texte EXACT, métaphore visuelle action+objet+émotion, plan, lumière
DATA=[
 ('s20','Nonvi konou, on sourit à la vie',
  'The hero and his close friend smile while walking beside a calm lagoon under the first sunbeams; the new day reflected in moving water becomes their quiet shared invitation to life. Not the same composition as earlier street scenes.', 'wide', 'full'),
 ('s21','Je marche dans la rue, je souris aux passants',
  'The hero smiles warmly at a passing elderly neighbor in a sunlit Beninese neighborhood lane; a natural greeting mid-stride, both people fully in frame, an everyday moment of kindness.', 'medium-wide', 'moderate'),
 ('s22',"Wanyiyi me guide, l'amour est mon carburant",
  'The hero and a friend gently push an old bicycle together up a small road in afternoon light; their companionship, not an engine, visibly keeps them moving forward.', 'wide', 'moderate'),
 ('s23',"Dagbé n'est pas un rêve, c'est ma réalité",
  'The hero opens the simple wooden gate to a lively home courtyard where friends welcome him; his joyful expression shows that belonging is real, tangible and present, not a dream.', 'medium', 'full'),
 ('s24','Chaque jour je me lève avec la joie dans le nez',
  'The hero begins the day by an open window, morning breeze gently moving a curtain as he smiles at sunlight and a small cup of warm breakfast tea on a nearby table; subtle delight, no exaggerated facial expression.', 'close-up', 'moderate'),
 ('s25','Ils ont voulu nous voir pleurer, on a dansé',
  'The hero and his close friend answer a gloomy rainy evening by dancing together under an awning, warm light reflected in puddles; background onlookers remain indistinct, no confrontation, just irrepressible joy.', 'medium-wide', 'full'),
 ('s26',"Ils ont voulu nous voir tomber, on s'est relevés",
  'In a sunlit neighborhood lane the hero offers an open hand to help his smiling friend stand up after resting on a low step; mutual resilience and dignity, no injury or aggression.', 'medium', 'full'),
 ('s27',"Gbètché vivi, c'est mon hymne, mon credo",
  'The hero quietly hums a joyful melody while walking through a green courtyard, hand lightly over his heart, sunlight filtering through leaves as though the whole day is music; no instruments with writing or stages.', 'medium-close-up', 'moderate'),
 ('s28',"Bandit Positif, je vole que du bonheur, c'est mon lot",
  'The hero playfully shares fresh oranges from a small basket with friends and children on a welcoming street; every person offers a smile back, suggesting happiness given and received, never theft.', 'medium-wide', 'full'),
 ('s29',"Dokpè pour le peu, dokpè pour l'amour",
  'The hero offers the last piece of homemade bread to a friend at a humble courtyard table at amber sunset; their mutual grateful smile and the small shared meal are the one luminous focal point.', 'medium', 'soft moderate'),
]

def main():
    plan=json.loads((DIR/'plan_images.json').read_text())
    items=[]
    for index,(slug,lyric,visual,shot,light) in enumerate(DATA,20):
        assert plan[index]['slot']==slug and plan[index]['text']==lyric and plan[index]['status']=='pending', (index,lyric)
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
    path=DIR/'salve_03_prompts.json'
    path.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(items)} prompts intégraux écrits avant lancement : {path}')
    for x in items:print(x['slot'],x['lyric'])

if __name__=='__main__':main()
