#!/usr/bin/env python3
"""Record the approved brief and the ten full image prompts BEFORE generation."""
from pathlib import Path
import hashlib
import json

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parent
SOURCE = 'Samu/Snapchat-795169778.jpg'
SCENES = [
    ('invitation', 'Invitation dorée', '00:21.13', "Djalé, s’il te plaît, yiwan noumi, aime-moi", 'A quiet coastal terrace at golden hour, sculptural ivory limewashed arches on the left, one palm frond entering the upper right, distant lagoon and a low peach sun. Refined natural materials, romantic but understated. Soft amber sunset light, muted mauve shadows. The bright architectural arch and the horizon remain visible above and beside the future portrait.'),
    ('miel', 'Le goût du miel', '00:52.71', 'Kissi noumi, ta bouche a le goût du miel', 'An intimate amber-glass conservatory at late sunset. Translucent honey-colored fluted glass panels catch liquid golden reflections across the top and right side; a small cluster of softly blurred white jasmine flowers frames the upper left. Sensuous material textures, creamy light, elegant photographic realism. No actual honey, no dripping liquid. Amber, cream and muted violet shadows.'),
    ('etincelles', 'Chaque baiser, une étincelle', '00:56.07', 'Chaque baiser est une étincelle', 'A romantic open-air garden courtyard at blue hour. Many tiny warm fairy lights hang in loose elegant arcs across the upper quarter; dusty rose bougainvillea frames the left side and a few distant lights become luminous golden bokeh. A natural twilight violet sky, warm rose ambience. The feeling of little sparks without fire, fireworks or fantasy effects.'),
    ('reste', 'Reste avec moi', '00:47.10', 'Djalé, reste avec moi, ne t’en va pas', 'A peaceful intimate veranda at dusk. A large softly illuminated ivory linen curtain hangs on the left, another sheer curtain at the far right, and an open terracotta arch reveals a lavender evening horizon behind. Warm indirect peach light on plaster, quiet waiting and tenderness, uncluttered architectural photography. Airy cream, terracotta amber and muted lavender.'),
    ('instants', 'Savourer chaque instant', '00:35.59', 'Vivi oor, vivi oor, je savoure chaque instant avec toi', 'A tranquil tropical lagoon just after sunset, photographed from a low lakeside veranda. The upper third shows a generous pale apricot sky fading into lavender, distant palm silhouettes along the left and right edges, and a delicate ribbon of warm light reflected on water. A weathered wooden jetty enters at the far right edge only. Quiet, expansive, romantic, photorealistic. No boats or people.'),
    ('coeur', 'Je t’ouvre mon cœur', '01:39.85', 'Djalé, je t’attends, je t’ouvre mon cœur', 'Two tall beautifully weathered open wooden doors frame a lush secret garden at the end of twilight. Both doors stay at the extreme left and right edges, welcoming and open. Beyond them, softly blurred foliage, a few cream flowers and a single warm lantern glow in the upper background. Amber illumination, restrained olive foliage and violet dusk. No literal heart shapes. Low camera viewpoint looking gently upward through the entrance.'),
    ('tresor', 'Notre amour est un trésor', '02:10.71', 'Notre amour est un trésor, on le garde encore', 'An elegant intimate night courtyard with a deep plum limewashed wall. A tall recessed arch along the right edge holds one softly glowing brushed-brass lantern; delicate golden reflected light grazes the textured wall across the top. A small shadowed palm leaf enters the upper left. Rich but restrained, the treasure is warm shared light, not money. Amber gold, deep plum and warm cream. No coins or jewels.'),
    ('festin', 'La vie est un festin', '01:53.38', 'La vie est un festin, je suis le mangeur', 'A welcoming candlelit outdoor restaurant courtyard at night, viewed from a low seated camera position. A timber pergola and woven pendant lamps overhead form a beautiful amber canopy in the upper half. Far behind, at the left and right edges, softly blurred small tables with terracotta dishes, clear water glasses and cream flowers suggest a dinner for two. No people, no alcohol labels. Warm celebratory intimacy, amber and dusky rose with deep violet shadows.'),
    ('danse', 'Dansons jusqu’au matin', '02:13.89', 'Wadjaya, dansons jusqu’au matin', 'An empty intimate open-air dance terrace late at night. Elegant strings of amber festoon lights cross the upper quarter, a large soft circular moon sits high at the far left, and subtle peach stage light glows through a very light natural haze at the far right. Palm silhouettes and a deep indigo sky, distant warm bokeh. A festive but tender atmosphere, not a nightclub, no lasers or visible performers. Amber, indigo and soft peach.'),
    ('aube', 'La douceur de l’aube', '02:32.68', 'Vivi oor, vivi oor, je savoure chaque instant avec toi', 'A minimalist rooftop terrace overlooking calm coastal water at the first light of dawn. Broad luminous pale peach and rose sky in the upper third, a soft lavender horizon, one delicate out-of-focus palm frond at the far left and an ivory curved parapet at the far right. No direct sun disk. A quiet hopeful ending, airy natural light, subtle atmospheric perspective, simple and deeply romantic. Cream, pale amber and lavender.'),
]

PREFIX = '1. FRAMING: One photorealistic vertical 9:16 background plate, target 1080x1920, full bleed, no collage.\n2. SCENE: '
SUFFIX = '''
3. REFERENCE: Use the attached original photo ONLY to guide composition and lighting. The real portrait will be pasted afterward using its original pixels. Generate the environment ALONE, absolutely NO PERSON. Leave room for the future portrait: head centered around x=0.46, y=0.39, top of hair at y=0.22, shoulders and torso occupying most of the lower half. Important scenery belongs in the top quarter and lateral gaps.
4. CAMERA: A gently low camera viewpoint consistent with the source selfie; professional 35mm environmental portrait background, soft but recognizable depth of field, realistic perspective, graceful large shapes rather than tiny clutter.
5. LOOK: Warm romantic cinematic photography inspired by Golden Sunset, believable materials, soft diffuse warm fill, restrained highlights, natural color transitions, subtle fine film grain. Coordinate with the source portrait's warm rosy light and violet-grey clothing. No artificial HDR or crushed blacks.
6. LAYOUT: Frame the future face with scenery, never put a bright object directly behind its center. Keep the lower center calm. No foreground props covering the portrait. One coherent photographic environment, not a stage cutout or graphic illustration.
7. EXCLUDE: No people, human figures, faces, hands, animals, text, letters, numbers, logos, watermark, subtitles, signage, emojis, heart symbols, borders or split panels. Do not reproduce the reference brick wall or Snapchat stickers.'''


def main():
    scenes = []
    for idx, (slug, title, t, lyric, scene) in enumerate(SCENES, 1):
        stem = f'{idx:02d}_{slug}'
        scenes.append(dict(slot=idx, slug=slug, title=title, lyric_time=t,
                           lyric_reference=lyric,
                           background=f'assets/backgrounds/{stem}.jpg',
                           output=f'livrables/VIVI_OOR_{stem}.png',
                           reference_image=SOURCE, prompt=PREFIX + scene + SUFFIX))
    manifest = dict(
        title='Vivi OOR', artist='Daïsky', date='2026-09-26',
        source=SOURCE,
        source_sha256=hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest(),
        prompts_consulted=['PROMPT_UNIVERSEL_v5.1.1.md', 'PROMPT_UNIVERSEL_v5.2_FINAL.md',
                          'PROMPT_UNIVERSEL_v5.3_FINAL.md (including v5.3.1 addendum)'],
        user_choices=dict(photo='validated', art_direction='carte blanche / S2 romantic',
                          format='9:16', text='none', total_images=10),
        method='Generate only ten background plates, each referencing the same original. Composite the untouched original portrait through a shared alpha mask. Never generate or beautify the face, body, clothes or pose.',
        dimensions=[1080, 1920], alpha='assets/portrait_alpha.png',
        original_changes='None. A separate alpha mask removes only the wall and Snapchat stickers. Uniform 1.5x resampling for delivery, no facial reconstruction or skin retouch.',
        scenes=scenes,
    )
    PROJECT.mkdir(parents=True, exist_ok=True)
    (PROJECT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    lines = ['# VIVI OOR — Catalogue des 10 prompts', '',
             '## Brief validé', '',
             f'- Photo unique : `{SOURCE}`.',
             '- Carte blanche : romantique doré S2, du couchant à l’aube.',
             '- Exactement **10 compositions finales**, en **1080 × 1920**, **sans texte**.',
             '- La limite explicite de 10 remplace « une image par vers ». Pas d’ancre ni de cover supplémentaire.',
             '- Dernière priorité documentaire : addendum v5.3.1, visage protégé.',
             '- Méthode renforcée : l’IA ne dessine que les décors ; le portrait photographique d’origine est recomposé ensuite. Même photo passée dans `images=` à chacune des dix générations.',
             '- Aucun autre personnage, aucune tenue inventée, aucune correction esthétique du visage.',
             '- Les repères ci-dessous proviennent du fichier de paroles ; ce ne sont pas des timings audio réalignés.', '',
             '## Prompts complets (écrits avant génération)', '']
    for s in scenes:
        lines += [f"### {s['slot']:02d} — {s['title']}", '',
                  f"Paroles : **{s['lyric_time']}** — « {s['lyric_reference']} »", '',
                  f"Référence `images` : `{s['reference_image']}`", '',
                  f"Décor : `{s['background']}` → composition : `{s['output']}`", '',
                  '```text', s['prompt'], '```', '']
    (PROJECT / 'PROMPTS_IMAGES_VIVI_OOR.md').write_text('\n'.join(lines))
    print('Prepared 10 complete prompts and approved manifest.')


if __name__ == '__main__':
    main()
