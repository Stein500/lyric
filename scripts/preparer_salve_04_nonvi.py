#!/usr/bin/env python3
"""Dernière salve : sept prompts intégraux AVANT génération (6 vers + endcard)."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'assets/nonvi_konou'
HERO=('Recurring HERO: fictional Beninese man about 27 years old, naturally average build, '
      'medium-dark brown skin, rounded-oval face, short natural tightly coiled black hair, '
      'short tidy beard, no glasses, deep-indigo short-sleeved collared cotton shirt and '
      'sand-colored trousers, unembellished realistic proportions; exact same features and clothing in every scene.')
SUFFIX=('REALISTIC editorial photography in Benin, cinematic 35mm film grain, natural skin texture, '
        'cool deep indigo twilight contrasted with a subtle warm amber backlight and fine cyan rim, '
        'gentle atmospheric haze, intimate believable documentary-real composition, '
        'dominant colors indigo amber green, luminosity decrescendo toward the end.')
ZONE=('Centered calm darker negative space around the middle for a two-line lyric; '
      'generous dark negative space in the top quarter; quiet natural scenery in the lower eighth '
      'to allow precise graphic compositing after generation.')
NO=('No text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, '
    'no signage, no medallions, no circular ornaments, no decorative stripes; '
    'authentic camera scene only. Uncropped faces and fully visible hands where near camera, '
    'natural number of fingers, no artificial beauty retouching.')
# Slot et paroles exactes du manifeste ; métaphore propre, jamais le vers literal.
DATA=[
 ('s30','Dokpè pour la vie, dokpè pour toujours',
  'The hero and his friend gently plant a young tree in a modest courtyard at late dusk, earth in their natural hands, one last shaft of golden light on the leaves: gratitude rooted into the future.', 'medium-wide', 'moderate amber'),
 ('s31','Nonvi konou, mon frère, tu es ma force',
  'The hero and his friend work side by side to lift a modest wooden fishing canoe above a calm shore, mutual trust shown through balanced effort and a warm shared smile, no display of muscle or danger.', 'wide', 'moderate amber'),
 ('s32','Gbè manfo do ohin min, ensemble on trace',
  'The hero and his friend leave two parallel sets of footprints on a damp sandy shoreline as they walk together toward the last amber stripe of the horizon, quiet resolve and companionship.', 'wide from behind', 'soft sunset'),
 ('s33','Nonvi konou...',
  'The hero pauses alone on a lagoon embankment at blue hour and watches his friend approaching from the far side of a pedestrian path; an intimate nostalgic smile, distant lamp bokeh, no melancholy.', 'medium-wide', 'dim amber'),
 ('s34','Dokpè... Gbètché vivi...',
  'The hero sits quietly with a friend at a small outdoor family table after sundown, both sharing a simple glass of water and an affectionate smile, a single warm window glow in the background.', 'medium close-up', 'dim warm'),
 ('s35','(La joie... toujours la joie...)',
  'The hero and two friends stand together beneath trees in a quiet Beninese courtyard at night, looking toward the last reflected lantern light in a shallow puddle, contentment and gratitude lingering.', 'wide', 'dim twilight'),
 ('s36_endcard','ENDCARD',
  'A tranquil Beninese lagoon after dusk, indigo water with one subdued amber glow at the horizon; the recurring hero is a very small natural silhouette on the far left shoreline with recognizable deep-indigo shirt and sand trousers, almost entirely dark empty CENTER for later title and contacts, contemplative but hopeful.', 'very wide symmetrical landscape within vertical frame', 'very dim, no black frame'),
]

def main():
    plan=json.loads((DIR/'plan_images.json').read_text())
    items=[]
    for i,(slot,lyric,visual,shot,light) in enumerate(DATA,30):
        assert plan[i]['slot']==slot and plan[i]['text']==lyric and plan[i]['status']=='pending', (i,plan[i])
        zone=ZONE if slot!='s36_endcard' else ('Large dark empty central rectangle occupying 55 percent width from '
              '25 percent to 75 percent height for title, WhatsApp and email composed later; '
              'uncluttered top quarter and bottom eighth for later graphic compositing.')
        blocks=[
          'CADRAGE: vertical 9:16 portrait composition, tall cinematic documentary framing in a real Beninese setting.',
          f'SUJET-VERS: {visual} Light intensity: {light}. This is a visual metaphor; never display any words inside the picture.',
          'HEROS: '+HERO,
          f'PLAN: {shot}, one natural luminous focal point, credible anatomy, all bodies naturally proportioned.',
          'SUFFIXE: '+SUFFIX,
          'ZONE: '+zone,
          'INTERDITS: '+NO,
        ]
        items.append(dict(slot=slot,lyric=lyric,blocks=blocks,prompt=' '.join(blocks)))
    outfile=DIR/'salve_04_prompts.json'
    outfile.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Sept prompts intégraux écrits AVANT lancement :',outfile)
    for item in items: print(item['slot'],item['lyric'])

if __name__=='__main__':main()
