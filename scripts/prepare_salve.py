#!/usr/bin/env python3
"""Écrit les neuf prompts complets AVANT les appels de génération, sans appel IA."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT/'PROMPTS_IMAGES_Concentre_sur_le_chemin.md'
OUTPUT = ROOT/'productions/concentre_sur_le_chemin/salve_02_prompts.json'

STYLE = ('Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.')
EXCLUSIONS = ('No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.')
SCENES = {
    's01': ('tete_lourde', 'Tête lourde',
            'A tired but determined musician seated on the same worn stool in the same cramped smoking room recording studio. Old microphone and pop filter at one side, aging mixing desk and two speakers, worn acoustic foam, scuffed plaster, a few cables. A single amber lamp illuminates the room through blue haze, low-to-moderate intensity. This is the wide-format counterpart of the approved anchor, not a different place.',
            'Almost frontal seated full-figure view, slight three-quarter angle, natural eye-level perspective, eyes visible through clear glasses.'),
    's02': ('dans_le_bruit', 'Dans le bruit',
            'The same musician gathers his thoughts amid the quiet clutter of his humble recording studio smoking room. The aging mixing console is more prominent in the foreground at the left edge; an old speaker and a hanging microphone recede through blue haze. Dim-to-moderate amber light, a subdued cyan rim, worn walls and repaired furniture. Same stool and room as the approved anchor, a distinctly different camera angle.',
            'Three-quarter side view from the console side, medium-wide seated full figure. His face remains turned enough toward the camera to recognize him; neither hand hides his eyes or lips.'),
    's03': ('tenir_le_cap', 'Tenir le cap',
            'The same musician remains seated with his two hands on his head, lifting his determined gaze toward the viewer as if refusing to give up. Stronger warm amber backlight cuts through blue cigarette haze; a subtle cyan edge lights the worn jacket. Same humble studio smoking room, old microphone and pop filter at the far side, speakers softly blurred behind him. Full chorus intensity, dignified and focused rather than glamorous.',
            'Strong almost frontal medium-wide full seated figure, clear expressive face and two hands, shoulders open. The camera is a little closer than the anchor, but the head, hands, knees and shoes stay fully inside generous margins.'),
    's04': ('patience', 'Patience',
            'The same musician breathes quietly and gathers patience in his modest smoking room recording studio, still with both hands on his head and the cigarette held at his temple. Soft warm amber lamplight becomes dominant, thinner blue haze and a very faint cyan rim. Same old console, microphone and worn acoustic panels in soft focus. Gentle bridge mood, low-to-moderate intensity, warm human vulnerability, no location or clothing change.',
            'Intimate three-quarter seated view, natural perspective, head and hands completely visible, full seated body within the frame. The expression softens but the eyes remain recognizable behind the same glasses.'),
    's05': ('encore_debout', 'Encore debout',
            'The same musician sits in the studio smoking room after the final take, both hands still on his head and a small trail of smoke rising from the cigarette between his fingers. The amber lamp has dimmed, the console and microphone recede into deep blue shadows, the floor is quiet and empty. Same room and outfit, calm dark outro atmosphere, dim intensity, one soft luminous accent only. Reserve a calm central area for the later endcard without drawing any graphics.',
            'Wider environmental seated full-figure shot, the studio feels quiet and spacious around him. Keep the face recognizable and entirely in frame, without turning him away from the camera.')
}


def main():
    source = CATALOG.read_text()
    hero = re.search(r'## Bloc héros invariant\n\n> (.*?)\n\n##', source, re.S)[1]
    references = ['Samu/Snapchat-1835992965.jpg', 'Samu/Snapchat-1275781156.jpg',
                  'Samu/Snapchat-959878741.jpg', 'assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png']
    jobs = []
    for fmt in ['portrait', 'landscape']:
        for slot, (slug, name, subject, shot) in SCENES.items():
            if fmt == 'portrait' and slot == 's01':
                continue
            if fmt == 'portrait':
                framing = ('True vertical 9:16 composition for 1080 by 1920. A single illustrated scene. Keep the seated figure inside generous margins; keep the entire head and both hands high in the upper third, above 36 percent of image height. Top 15 percent is quiet dark wall. The face must be above the middle, not at the center. The two forearms, hands and feet stay inside the central 75 percent width for crop safety.')
                zone = ('Quiet upper area for UI later. Low-detail dark jacket and room across the middle 40 to 65 percent for large centered lyrics added in post; the face stays clearly above this region. Calm bottom 10 percent and empty floor beyond the shoes. All graphics and national colors will be added later, not generated.')
            else:
                framing = ('True horizontal 16:9 landscape composition for 1920 by 1080, wide YouTube framing, not a cropped portrait and not a collage. Place the seated musician toward the LEFT THIRD, his face and both hands in the UPPER LEFT: head center around x=430, y=240; the entire face must end above y=365. Keep the full seated body, elbows and shoes inside the frame with generous margins. Show the studio extending naturally to the right.')
                zone = ('Leave a low-detail dark horizontal middle band around y=430 to y=700 for large centered lyrics added in post, across the room and clothing, never the face. Top center is quiet for a compact UI badge later. Keep the bottom 10 percent calm, with shoes fully above the lower edge. All graphics and national colors will be added later, not generated.')
            blocks = [framing, subject, hero, shot, STYLE, zone, EXCLUSIONS]
            names = ['FRAMING', 'SUBJECT AND EMOTION', 'HERO', 'SHOT', 'STYLE AND LIGHT', 'COMPOSITING AREAS', 'EXCLUSIONS']
            prompt = '\n\n'.join(f'{i+1} — {heading}. {block}' for i, (heading, block) in enumerate(zip(names, blocks)))
            jobs.append({'slot': slot, 'name': name, 'format': fmt,
                         'file_path': f'assets/raw/concentre_sur_le_chemin/{fmt}/{slot}_{slug}.png',
                         'images': references, 'prompt': prompt, 'status': 'ready_not_generated'})
    OUTPUT.write_text(json.dumps(jobs, ensure_ascii=False, indent=2)+'\n')
    source = source.replace("L'ancre reste à valider.", "Ancre approuvée par l’artiste : « Oui continue... » (2026-09-28).")
    source = source.replace("La génération ci-dessous occupe le slot portrait s01 si elle est acceptée. Aucun autre fond ne doit être généré avant son approbation.", "L’ancre approuvée occupe le slot portrait s01. La salve suivante contient uniquement les neuf fonds restants.")
    source = source.replace("Les lunettes rectangulaires des références sont conservées dans la proposition ; à vérifier lors de la validation de l'ancre.", "Les lunettes rectangulaires sont conservées et approuvées avec l’ancre.")
    source = source.split('## Neuf prompts restants')[0]
    source += '## Salve 02 — neuf prompts complets, écrits avant lancement\n\nAncre approuvée. Quatre portraits et cinq paysages ; **neuf appels IA au total dans cette salve**. Les trois originaux Samu restent les références d’identité et le quatrième visuel est l’ancre approuvée, sans texte ni badge. La planche contact devra être validée avant le rendu final.\n\n'
    for job in jobs:
        source += f"### {job['slot']} {job['format']} — {job['name']}\n\nSortie : `{job['file_path']}`.\n\nRéférences : " + ' · '.join(f'`{p}`' for p in job['images'])+'\n\n'+job['prompt']+'\n\n'
    CATALOG.write_text(source.rstrip()+'\n')
    config_path = ROOT/'productions/concentre_sur_le_chemin/production.json'
    config = json.loads(config_path.read_text())
    config['stage'] = 'anchor_approved_remaining_backgrounds_planned'
    config['approvals']['anchor'] = True
    config['approvals']['anchor_message'] = 'Oui continue...'
    config['preview']['artist_approved'] = True
    config['scenes'][0]['status'] = 'portrait_approved_landscape_pending'
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2)+'\n')
    print(f'{len(jobs)} prompts complets écrits dans {OUTPUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
