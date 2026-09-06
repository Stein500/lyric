# Je m'aime tellement — livraison v1 (timings corrigés)

**Statut : prêt pour ton téléchargement et ta validation.**

**Mise à jour 2026-09-06 :** les timings corrigés que tu as fournis remplacent l'ancien LRC. Le clip 9:16 a été entièrement re-rendu sur cette nouvelle timeline (49 vers, mêmes fonds, mêmes réglages). Le MP3 est inchangé au bit près : la correction ne concerne que la synchronisation du texte à l'image.

| Fichier | Caractéristiques |
|---|---|
| [Clip 9:16](Je_maime_tellement_9x16_v1.mp4) | 1080×1920, 30 fps, H.264 / AAC 192 kb/s, **3:18,167**, **69,8 Mo** |
| [MP3 propre](Je_maime_tellement_master_v1.mp3) | 320 kb/s, 48 kHz stéréo, **3:13,160**, **8,0 Mo** |

## Ce qui est conservé

- **Tes paroles et tes timestamps**, sans avance de 0,03 s ni remplacement par les anciens textes intégrés au MP3.
- Daïsky Pro · album Success · Daïsky Prod / TechStein. Genre Rap et année 2026 repris de la source.
- 30 fonds (15 cinéma, 15 animé), héroïne à la silhouette généreuse ; réutilisation autorisée sur les autres vers.
- Ken Burns et vague continue des lettres ; badge fixe, posé en dernier.
- Écran de fin à 3:09,50, pendant le fondu musical, contacts complets et environ 5 s ajoutées au clip. Aucune rallonge du MP3.

## Contrôles réalisés

- 5 945 frames, dimensions et durée conformes, lecture progressive `faststart`.
- Aucune séquence noire hors fondu final ; aucun événement `freezedetect` au seuil −70 dB / 1 s.
- Comparaison de 16 frames encodées avec leur reconstruction, notamment après 2:00 : erreur moyenne maximale **2,25 / 255** (tolérance 6).
- Badge : différence moyenne **0,12 / 255** sur deux instants du même fond (tolérance 4).
- Source/master : aucun décalage détecté par corrélation sur les trois extraits testés.
- **MP3 : −13,93 LUFS / −1,70 dBTP**, durée décodée inchangée à l’échantillon près ; tags, paroles françaises et cover carrée intégrée.
- Audio AAC du clip : **−14,00 LUFS / −1,04 dBTP**, sans clipping.

Le mastering est effectué en deux passes. Pour ce morceau, loudnorm a utilisé son mode dynamique afin de respecter le plafond de crête ; le mode réel est documenté dans le rapport.

**À vérifier à l’écoute :** ton appréciation du son, la correspondance chant/texte et les choix visuels. Il s’agit de contrôles techniques du rendu, pas d’une validation artistique à ta place. Les autres formats attendent ton accord.

## Empreintes SHA-256

- MP4 : `c443ef032a58e75a321f69efc02082e7bafea72c2a065613448c8971872f4b34`
- MP3 : `a1e4fbac58c5f8d17d7c5936037fe9f536d67ea84a6dd64ac351614acdecba94` (identique à la livraison précédente)
