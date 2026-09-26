#!/usr/bin/env python3
"""Record this second, explicitly requested AI-editing pass before generation."""
from pathlib import Path
import hashlib
import json

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
OLD = json.loads((ROOT / 'vivi-oor/manifest.json').read_text())

INTRO = '1. OUTPUT: Retouch the supplied photograph into ONE finished photorealistic vertical 9:16 music-artist portrait, 1080x1920 target. This is the COMPLETE PORTRAIT, NOT an empty background plate.\n2. ENVIRONMENT: '
END = '''
3. SUBJECT LOCK: Image 1 is the original real person and the absolute identity reference. Image 2 is an existing rough composite to refine, not a new identity. Keep exactly this person's face shape, eyes, nose, lips, short natural hair, small chin beard, subtle slightly parted smile, gaze, real build and casual shoulder tilt. Retain the same silver-violet quilted zip vest and vivid patterned sleeves. No change of pose, outfit, age or body shape. Extremely conservative face editing: improve capture quality with lighting and color, not facial reconstruction. Do not make a different or idealized man.
4. PHOTOGRAPHIC FINISH: Turn the rough cutout into a believable single-camera photograph. Refine the hair and clothing boundaries, remove jagged halos, match light direction and depth of field. Reduce compression noise gently, keep natural skin texture and the authentic small asymmetries. No plastic skin. Do not invent new teeth or sharpen the jaw. Aim for a high-quality candid portrait, not beauty advertising.
5. LIGHT: Soft natural portrait fill coherent with this environment, restrained warm romantic cinematic grading, gentle highlights, lifted soft shadows, believable material detail. Correct the excessive magenta color cast without whitening the skin or changing the underlying complexion. Preserve the clothing colors. Softer background detail than the person, realistic optical bokeh, no fake glowing outline, no HDR.
6. COMPOSITION: Follow image 2's existing portrait scale and placement closely. Full head comfortably in frame, torso cropped exactly as the source composition, no invented hands or extra limbs. Keep the environmental story visible above and beside the head, never put scenery over the face. Refined, intimate, understated realism, not a pasted-on sticker or fantasy illustration.
7. EXCLUDE: No text, letters, numbers, titles, logos, watermark, signage, Snapchat hearts, border, collage, extra people, face reshaping, beauty filter, makeup, skin bleaching, slimming, muscular enhancement, new accessories, new clothing or different facial expression.'''


def main():
    entries = []
    for old in OLD['scenes']:
        scene = old['prompt'].split('2. SCENE: ', 1)[1].split('\n3. REFERENCE:', 1)[0]
        stem = f"{old['slot']:02d}_{old['slug']}"
        entries.append(dict(
            slot=old['slot'], title=old['title'], slug=old['slug'],
            lyric_time=old['lyric_time'], lyric_reference=old['lyric_reference'],
            images=[OLD['source'], 'vivi-oor/' + old['output']],
            prompt=INTRO + scene + END,
            raw=f'assets/edits/{stem}.jpg',
            output=f'livrables/VIVI_OOR_V2_{stem}.png',
        ))
    manifest = dict(
        title='Vivi OOR', version=2, date='2026-09-26',
        requested='Afficher les 10 images ici et les retravailler avec IA.',
        source=OLD['source'], source_sha256=hashlib.sha256((ROOT/OLD['source']).read_bytes()).hexdigest(),
        total_images=10, dimensions=[1080,1920], text=False,
        method='AI photographic editing of each existing composition, always using the unmodified original as first reference. Conservative identity instructions, visual review; unlike V1 this is NOT a pixel-locked original portrait.',
        previous_version='vivi-oor/livrables (left unchanged)',
        scenes=entries,
    )
    (PROJECT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    md = ['# VIVI OOR — V2, finition photographique IA', '',
          '## Demande', '',
          'Reprendre les dix compositions avec l’éditeur IA et montrer chaque résultat séparément. Les réglages validés restent : **une seule photo source, dix images, 9:16, aucun texte**.', '',
          'La V1 et la photo source sont conservées sans changement. Chaque appel utilise l’original en première référence et la composition V1 correspondante en seconde référence. Aucune image V2 n’est réutilisée pour inventer le visage d’une autre.', '',
          '**Transparence :** contrairement au détourage V1, la retouche IA complète ne garantit pas des pixels de visage identiques à l’original. Fidélité demandée dans chaque prompt et contrôlée visuellement ; aucune revendication de conservation pixel par pixel pour ces nouvelles images.', '',
          '## Dix prompts complets — rédigés avant lancement', '']
    for s in entries:
        md += [f"### {s['slot']:02d} — {s['title']}", '',
               f"Référence paroles : {s['lyric_time']} — « {s['lyric_reference']} »", '',
               f"Images : `{s['images'][0]}` ; `{s['images'][1]}`.", '',
               '```text',s['prompt'],'```','']
    (PROJECT/'PROMPTS_IMAGES_VIVI_OOR_V2.md').write_text('\n'.join(md))
    print('Ten complete AI-edit prompts recorded.')


if __name__=='__main__':
    main()
