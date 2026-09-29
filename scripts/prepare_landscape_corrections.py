#!/usr/bin/env python3
"""Écrire la salve corrective AVANT les appels IA. Ne lance aucune génération.

Révision 2 des cinq slots paysage existants : cadrage complet et éclairage
continu. Les versions refusées restent dans l'historique Git (6752573), pas
comme des scènes supplémentaires. Les cinq portraits sont conservés.
"""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT/'PROMPTS_IMAGES_Concentre_sur_le_chemin.md'
MARKER = '## Reprise des paysages — 2026-09-29 — révision 2'
REFERENCES = [
    'Samu/Snapchat-1835992965.jpg',
    'Samu/Snapchat-1275781156.jpg',
    'Samu/Snapchat-959878741.jpg',
    'assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png',
]
SUBJECTS = {
    's01_tete_lourde': 'A tired but determined independent musician sits on the same worn stool in his cramped smoking room recording studio. An old microphone and round pop filter stand beside him, an aging mixing desk and two small speakers recede to the right, worn acoustic foam and scuffed plaster complete the modest room. One amber lamp shines softly through blue cigarette haze. Low-to-moderate light, the same introspective mood and equipment as the approved fourth reference.',
    's02_dans_le_bruit': 'The same musician gathers his thoughts in the quiet clutter of his smoking room recording studio. View the room from the mixing-console side: the worn desk occupies the far left foreground, the musician sits behind it and a suspended microphone hangs to his right. A soft amber practical lamp and dim cyan side light reveal worn acoustic panels and cables against the wall. A distinct three-quarter camera angle, dim-to-moderate intensity, the same room and furniture as the fourth reference.',
    's03_tenir_le_cap': 'The same musician sits determined and focused in his humble recording studio smoking room, keeping both hands on his head while looking toward the camera. Stronger amber backlight shines through blue cigarette haze and a gentle cyan edge lights his worn jacket. An old microphone and pop filter stand at the far right; speakers and an aging mixing desk recede naturally in the room. Full chorus intensity, one warm focal light, dignity and resolve rather than glamour.',
    's04_patience': 'The same musician pauses quietly in his humble studio smoking room, with both hands resting on his head and the cigarette between his fingers. Softer warm amber lamplight dominates, the blue haze is thin and the cyan rim very faint. A worn mixing desk, microphone and acoustic panels sit quietly behind him. A gentle three-quarter view and a calmer expression convey patience; keep his recognizable face, glasses and original proportions. The mood is warm and vulnerable, with low-to-moderate light.',
    's05_encore_debout': 'The same musician remains seated in the recording studio smoking room after the final take. Both hands are still on his head, and a fine smoke trail rises from the cigarette beside his temple. The amber lamp is dim, the mixing desk and old microphone recede into deep blue shadows and the floor is quiet and uncluttered. One soft warm accent, calm darkness, the same worn furniture and clothing, a contemplative ending rather than a new location.',
}
FRAMING = ('True horizontal 16:9 wide cinematic illustration. Observe a complete room from its doorway with a distant camera, showing the full seated man on the LEFT THIRD. Keep him modest in size: the entire seated figure, from the top of his hands to the soles of BOTH SHOES, occupies at most 62 percent of the image height. His head starts near 12 percent height and his shoes finish by 78 percent height. Leave a broad expanse of natural floor beneath his feet and ample air around both elbows. The right two thirds contain the rest of the studio. His face is in the upper left third, above the vertical middle.')
SHOT = ('Wide environmental head-to-toe seated shot with a natural 35mm perspective. The whole stool, both knees, calves, ankles, shoe heels and shoe toes are visible with breathing room. The lower fifth of the picture is empty physical floor. Keep the head and the two hands clearly visible, the eyes unobstructed behind the glasses. Use the first three photographs only for identity and the fourth illustration for the approved likeness and drawing style. The figure must be much smaller within this wide frame than within the portrait reference.')
STYLE = ('Exactly the approved fourth reference drawing style: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, dark blue-black shadows, warm amber practical light, subtle cyan rim, light atmospheric smoke and restrained fine film texture. Retain the same glasses, natural facial proportions, patch positions and worn charcoal jacket with brown trousers. The whole composition is one continuous illustrated room.')
ROOM = ('Natural continuous illumination across all walls, furniture, clothing and floor. Shadows blend gradually in a physically coherent room, and surfaces have smooth uninterrupted shading. Simple unadorned upper walls and a quiet natural floor. All visible details belong to the physical studio. The space to the right is softly lit, uncluttered and atmospheric.')
ANATOMY = ('One recognizable person with exactly two arms and two anatomically plausible hands touching the top and sides of his head. One cigarette held between the fingers beside his temple, pointed away from his hair. Both feet stand on the floor, fully enclosed within the picture. Preserve the approved pose, face and body proportions; keep all extremities comfortably inside the frame.')


def main():
    source = CATALOG.read_text()
    hero = re.search(r'## Bloc héros invariant\n\n> (.*?)\n\n##', source, re.S)[1]
    source = source.split(MARKER)[0].rstrip()
    heading = ('\n\n'+MARKER+'\n\n'
               'Ancre approuvée : « Oui continue... ». La salve précédente a été récupérée depuis '
               'le commit `67525732617ae9b6acfb23243b43c8f3f999004c`, sans effacer des changements locaux. '
               'Les cinq portraits sont conservés. s03/s04 paysage étaient trop serrés ; les autres '
               'paysages présentaient des aplats ou prolongements de bords peu naturels. '
               '**Cinq corrections remplacent les cinq slots paysage, sans ajouter de scène.**\n\n'
               'Reformulation positive après hallucination de lettrage/aplats : les nouveaux prompts '
               'ne nomment plus les objets graphiques indésirables et ne demandent plus de bande centrale. '
               'La lisibilité, le badge et le drapeau sont traités uniquement en post. '
               'Tous les prompts ci-dessous sont écrits avant lancement.\n')
    jobs = []
    for stem, subject in SUBJECTS.items():
        path = ROOT/f'assets/raw/concentre_sur_le_chemin/landscape/{stem}.png'
        prompt = '\n\n'.join(f'{i} — {label}. {text}' for i, (label, text) in enumerate([
            ('FRAMING', FRAMING), ('SUBJECT', subject), ('HERO', hero), ('SHOT', SHOT),
            ('STYLE', STYLE), ('ROOM', ROOM), ('ANATOMY', ANATOMY)], 1))
        jobs.append({'slot': stem.split('_')[0], 'format': 'landscape', 'revision': 2,
                     'file_path': str(path.relative_to(ROOT)), 'images': REFERENCES,
                     'replaced_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'rejected_version_commit': '67525732617ae9b6acfb23243b43c8f3f999004c',
                     'prompt': prompt, 'status': 'planned_not_generated'})
        heading += f'\n### {stem} — paysage corrigé\n\nSortie : `{path.relative_to(ROOT)}`.\n\nRéférences : '+ ' · '.join(f'`{p}`' for p in REFERENCES)+'\n\n'+prompt+'\n'
    CATALOG.write_text(source+heading)
    destination = ROOT/'productions/concentre_sur_le_chemin/landscape_corrections_v2.json'
    destination.write_text(json.dumps(jobs, ensure_ascii=False, indent=2)+'\n')
    print(f'{len(jobs)} prompts complets prêts, aucune génération lancée.')


if __name__ == '__main__':
    main()
