# Je plane — livraison et contrôles

## Direction et sources
- Titre : Je plane ; artiste et badge : DSKY, alternant avec WTBW. Ancre et style validés par l'artiste. 48 vers et 26 images distinctes utilisées avec réutilisation à sa demande ; fichiers et correspondances dans `verses_map.json`.
- Paroles défilantes ; signature chantée affichée « WTBW » selon sa demande. Texte et audio sources conservés. Le marqueur technique `[reference:0]` a été omis de l'affichage.
- Deux teasers à partir de deux occurrences du refrain : positions source 10,41–25,41 s et 133,54–148,54 s ; bornes provisoires, non contrôlées à l'écoute. Deux couvertures verticales ; cover carrée choisie intégrée au MP3.

## Mouvement et habillage
- Travelling/zoom lent, grain léger sur le fond avant les paroles, transitions de fond courtes en trois étapes, vagues et étincelles animées sous les paroles, filet de progression et badge DSKY ↔ WTBW. Paroles appliquées après les transitions, sans mélange des lettres.
- Clochette vectorielle animée et CTA courts sur la carte finale, après la fin du morceau, sans bruitage ajouté ni parole recouverte. Ensuite « LIKE · PARTAGE · COMMENTE ».

## Contrôles techniques réellement effectués
- Clip : H.264 1080×1920, 30 i/s, 178,44 s, audio AAC stéréo 48 kHz ; teasers H.264/AAC 1080×1920 à 30 i/s, chacun 450 images / 15 s. Les trois fichiers ont `moov` avant `mdat` (faststart).
- Audio source décodé : 173,439979 s. `ebur128` : clip −13,3 LUFS / LRA 5,7 / crête vraie −2,2 dBFS ; teaser 1 −12,3 / LRA 1,0 / −2,9 dBFS ; teaser 2 −12,1 / LRA 5,0 / −2,6 dBFS. Master MP3 −14,0 LUFS / LRA 5,7 / crête vraie −2,9 dBFS ; normalisation loudnorm à deux passes, seconde passe linéaire, 48 kHz stéréo, MP3 CBR 320 kb/s.
- Tags du MP3 relus : titre Je plane, artiste et artiste d'album DSKY, album Je plane, série WTBW, paroles et pochette carrée ; aucune métadonnée de plateforme héritée. Le fichier original reste inchangé. Aucun nom ou lien personnel supplémentaire n'a été inventé.
- `blackdetect` au seuil `pix_th=0.10` : aucun intervalle ; au seuil très sévère `pix_th=0.98` : 0–178,4 s détecté comme sombre, ce qui ne prouve pas des images entièrement noires. `freezedetect=n=-33dB:d=2.5` : 26 débuts de gel détectés malgré les animations ; intervalles dans `CONTROLE-VIDEO-v2.txt`. L'objectif zéro gel n'est pas atteint.
- Planche de 48 images extraites du MP4 : un échantillon par vers a été examiné ; contrôle exhaustif à chaque image et en 1:1 non réalisé.

## Limites
- Calage mot à mot estimé et fins de vers inconnues. Les deux coupes de teaser et la synchronisation avec la voix ne sont pas vérifiées à l'écoute. À valider avant diffusion ; ne pas prétendre qu'elles sont parfaites.
- Visuels générés par IA ; audio issu de la source fournie, normalisé pour le MP3 et réencodé en AAC pour les vidéos. Son origine de création n'a pas été établie indépendamment ; le nettoyage des tags ne prouve pas que l'audio serait exempt d'IA.

## Reproduction
Depuis la racine : créer `.venv` avec Pillow, mutagen et imageio-ffmpeg, puis exécuter `.venv/bin/python productions/je-plane/produire.py prepare`, `render`, puis `teasers`. Les fichiers temporaires sous `travail/` sont ignorés et recréés. Les mesures ci-dessus concernent les fichiers rendus, pas uniquement la source.
