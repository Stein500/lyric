#!/usr/bin/env python3
"""Préparer l'index et les empreintes du pack après les deux contrôles vidéo.

Les grosses vidéos ne sont pas dupliquées dans un ZIP. La seule archive est
celle des dix fonds déjà approuvés. Pas de statut de validation vocale inventé.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'productions/concentre_sur_le_chemin'
DELIVERY = ROOT / 'livrables'

# label, chemin Git, nom de téléchargement Android
FILES = [
    ('Clip vertical · TikTok / Reels / Shorts', 'livrables/Concentre_sur_le_chemin_9x16_v1.mp4', 'Concentre_sur_le_chemin_9x16_v1.mp4'),
    ('Clip horizontal · YouTube', 'livrables/Concentre_sur_le_chemin_16x9_YT_v1.mp4', 'Concentre_sur_le_chemin_16x9_YT_v1.mp4'),
    ('Master MP3 · chanson seule, 320 kb/s', 'livrables/Concentre_sur_le_chemin_master_320k.mp3', 'Concentre_sur_le_chemin_master_320k.mp3'),
    ('Pochette carrée · 1080 × 1080', 'livrables/cover_concentre_sur_le_chemin_1080x1080.jpg', 'cover_concentre_sur_le_chemin_1080x1080.jpg'),
    ('Pochette portrait · 1080 × 1920', 'livrables/cover_concentre_sur_le_chemin_9x16.jpg', 'cover_concentre_sur_le_chemin_9x16.jpg'),
    ('Pochette YouTube · 1920 × 1080', 'livrables/cover_concentre_sur_le_chemin_16x9.jpg', 'cover_concentre_sur_le_chemin_16x9.jpg'),
    ('Les dix fonds approuvés · ZIP', 'livrables/Concentre_sur_le_chemin_10_images_v2.zip', 'Concentre_sur_le_chemin_10_images_v2.zip'),
    ('Planche des cinq paires de fonds', 'livrables/Concentre_sur_le_chemin_planche_10_fonds_v2.jpg', 'Concentre_sur_le_chemin_planche_10_fonds_v2.jpg'),
    ('Paroles LRC · horaires de la chanson source', 'Concentré sur le chemin.lrc', 'Concentre_sur_le_chemin.lrc'),
    ('Prompt universel complet à jour', 'PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md', 'PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md'),
    ('Catalogue des prompts d’images', 'PROMPTS_IMAGES_Concentre_sur_le_chemin.md', 'PROMPTS_IMAGES_Concentre_sur_le_chemin.md'),
    ('Index de la livraison et repères d’écoute', 'livrables/LIVRAISON_Concentre_sur_le_chemin.md', 'LIVRAISON_Concentre_sur_le_chemin.md'),
]


def checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(label: str, path: str, name: str) -> dict:
    source = ROOT / path
    if not source.is_file():
        raise RuntimeError(f'Ne pas annoncer un fichier absent : {path}')
    return {'label': label, 'file': path, 'download_name': name,
            'size_bytes': source.stat().st_size, 'sha256': checksum(source)}


def main() -> None:
    state = json.loads((STATE / 'production.json').read_text())
    timeline = json.loads((STATE / 'timings_render.json').read_text())
    if not state['approvals']['image_series']:
        raise RuntimeError('Les dix fonds doivent avoir une vraie approbation.')
    videos = []
    for fmt in ('portrait', 'landscape'):
        qa = json.loads((STATE / f'qa_{fmt}.json').read_text())
        if qa['status'] != 'technical_checks_passed':
            raise RuntimeError(f'Contrôles du {fmt} non terminés.')
        path = ROOT / qa['file']
        if checksum(path) != qa['sha256'] or path.stat().st_size != qa['size_bytes']:
            raise RuntimeError(f'Clip modifié depuis les contrôles : {fmt}')
        if qa['frames'] != timeline['frames'] or abs(qa['duration'] - timeline['encoded_duration']) > .05:
            raise RuntimeError(f'Durée/horloge du {fmt} incohérente.')
        videos.append(qa)
    master = json.loads((STATE / 'audio_master_report.json').read_text())
    if checksum(ROOT / master['file']) != master['sha256']:
        raise RuntimeError('MP3 modifié depuis la mesure et le tagging.')
    with zipfile.ZipFile(DELIVERY / 'Concentre_sur_le_chemin_10_images_v2.zip') as archive:
        if archive.testzip() is not None or len([p for p in archive.namelist() if p.endswith('.jpg')]) != 10:
            raise RuntimeError('Archive des dix fonds invalide.')
    sizes = {Path(q['file']).name: q['size_bytes'] for q in videos}
    text = f'''# Concentré sur le chemin — Daïsky

**Pack exporté et contrôlé · 30 septembre 2026**

Les dix fonds sont approuvés (« Oui je valide !! »). Les clips utilisent ces cinq scènes
animées dans les deux formats, sans nouvelle génération : vêtements usés, fumoir/studio,
cigarette, deux mains sur la tête, gros caractères gras au centre.

## Les fichiers

| Usage | Fichier | Détails |
|---|---|---|
| TikTok / Reels / Shorts | [Clip 9:16](Concentre_sur_le_chemin_9x16_v1.mp4) | 1080 × 1920 · 30 fps · {sizes['Concentre_sur_le_chemin_9x16_v1.mp4'] / 1e6:.2f} Mo |
| YouTube | [Clip 16:9](Concentre_sur_le_chemin_16x9_YT_v1.mp4) | 1920 × 1080 · 30 fps · {sizes['Concentre_sur_le_chemin_16x9_YT_v1.mp4'] / 1e6:.2f} Mo |
| Audio seul | [Master MP3](Concentre_sur_le_chemin_master_320k.mp3) | 320 kb/s · 48 kHz · stéréo · 03:33,160 |
| Pochette carrée | [1080 × 1080](cover_concentre_sur_le_chemin_1080x1080.jpg) | Aussi intégrée au MP3 |
| Pochette portrait | [9:16](cover_concentre_sur_le_chemin_9x16.jpg) | Titre et artiste en post-production |
| Pochette YouTube | [16:9](cover_concentre_sur_le_chemin_16x9.jpg) | Titre et artiste en post-production |
| Dix fonds approuvés | [ZIP des images](Concentre_sur_le_chemin_10_images_v2.zip) | Exactement 5 portraits + 5 paysages |
| Aperçu des fonds | [Planche v2](Concentre_sur_le_chemin_planche_10_fonds_v2.jpg) | Image présentée avant l’approbation |
| Paroles | [LRC source](../Concentr%C3%A9%20sur%20le%20chemin.lrc) | Horaires de la chanson seule, sans hook |
| Prompt complet | [Universel v5.5](../PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md) | Règles et état de cette commande |
| Prompts images | [Catalogue](../PROMPTS_IMAGES_Concentre_sur_le_chemin.md) | Prompts et références autorisées |
| Android / Termux | [Commandes de téléchargement](TERMUX_Concentre_sur_le_chemin_COMPLET.md) | Une ligne par fichier, reprise possible |
| Intégrité | [Empreintes SHA-256](Concentre_sur_le_chemin_SHA256.txt) | Contrôle exact des téléchargements |

Les deux clips durent **03:45,067** : ouverture de **6,90 s**, chanson intégrale de
**213,160 s**, puis **5 s** de fin. Un seul flux de **6 752 frames** ; H.264 / BT.709,
audio AAC 192 kb/s, pas de concaténation de morceaux vidéo.

## Ce qui est contrôlé

- Tous les **58 vers / 389 mots** du texte source sont conservés, sans correction des
  tournures, accents ou mots locaux. Mise en page complète avant apparition des mots.
- Gros texte gras centré, mot actif crème/or + vague d’eau continue. Zones sûres contrôlées.
- Badge **Dsky + Bénin** en fondu entrée/sortie de 0,4 s par vers, opacité plafonnée à 75 %.
  Aucun badge gravé dans les fonds ; bandeau fixe Bénin de 54 px en portrait / 30 px en paysage.
- Aucun gel détecté ; noir seulement à la toute fin du fondu. Frames extraites des deux
  MP4 comparées au rendu attendu, couleurs du drapeau contrôlées après compression.
- Trois corrélations audio n’ont mesuré **aucune dérive de montage**.
- Master : **{master['master_mp3_measurement']['input_i']} LUFS** et
  **{master['master_mp3_measurement']['input_tp']} dBTP** mesurés après encodage.
  ID3v2.4, titre/artiste/contacts, paroles USLT et pochette APIC.

## À confirmer à l’écoute — distinct de la validation des images

**Le mot à mot est estimé à partir de ton LRC et de durées syllabiques. Ce n’est pas un
alignement phonétique validé.** Les tests de dérive audio ne remplacent pas une écoute.
L’extrait d’ouverture demandé est monté, mais sa coupe n’a pas été approuvée séparément.

| Horloge du clip (avec hook) | Horloge de la chanson source | Début du vers |
|---|---|---|
| **00:32,20** | 00:25,30 | Concentré sur le chemin, je regarde plus en arrière |
| **01:32,54** | 01:25,64 | J’suis concentrée, j’regarde droit devant |
| **02:39,74** | 02:32,84 | Concentré sur le chemin, je regarde plus en arrière |

Les paroles sont volontairement affichées environ 0,03 s avant leur repère LRC.
Pour une correction, indique l’heure du clip et le mot/vers concerné ; ne pas confondre
ces trois repères avec les mesures d’attaque vocale, qui restent à confirmer.

## Publication — proposition de légende

> Concentré sur le chemin, je marche vers la lumière. 🎶
> Daïsky — nouveau clip lyrics.
> #Daisky #ConcentreSurLeChemin #MusiqueBeninoise #Lyrics

Contact : `daiskyproduction@gmail.com` · WhatsApp `+229 01 61 16 24 08` /
`+229 01 49 11 49 51`.

## Reproduction technique

Scripts : `scripts/render_clip.py`, `verify_clip.py`, `produce_audio.py`, `design_assets.py`.
Rapports : `productions/concentre_sur_le_chemin/qa_{{portrait,landscape}}.json`,
`audio_master_report.json`, `covers_report.json`, `delivery_manifest.json` et
`delivery_remote_checks.json`. Les caches et WAV sous `work/` ne sont pas versionnés.
La maquette de 14,5 s reste une ancienne étape de validation ; utiliser les clips complets ci-dessus.
'''
    (DELIVERY / 'LIVRAISON_Concentre_sur_le_chemin.md').write_text(text, encoding='utf-8')
    rows = [record(*spec) for spec in FILES]
    fingerprints = DELIVERY / 'Concentre_sur_le_chemin_SHA256.txt'
    fingerprints.write_text(''.join(f'{r["sha256"]}  {r["download_name"]}\n' for r in rows), encoding='utf-8')
    rows.append(record('Empreintes SHA-256 des fichiers', str(fingerprints.relative_to(ROOT)), fingerprints.name))
    report = {'date': '2026-09-30', 'title': timeline['title'], 'artist': timeline['artist'],
              'status': 'exports_technically_checked_artist_word_timing_review_pending',
              'images_artist_approved': True, 'vocal_word_alignment_human_validated': False,
              'video_duration_seconds': timeline['encoded_duration'], 'video_frames': timeline['frames'],
              'song_duration_seconds': timeline['duration_source'], 'hook_duration_seconds': timeline['hook_duration'],
              'new_ai_images_this_step': 0, 'files': rows}
    (STATE / 'delivery_manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(rows)} fichiers réels listés ; index et SHA-256 prêts. Publier avant write_termux_delivery.py.')


if __name__ == '__main__':
    main()
