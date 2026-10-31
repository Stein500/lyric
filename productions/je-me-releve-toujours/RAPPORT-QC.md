# Rapport de contrôle — « Je me relève toujours » / proposition 9:16

## Statut et limites

Une **proposition de montage** est rendue; le QC technique et la lecture visuelle décrits ci-dessous ont été effectués. L’ancre seule a été approuvée par l’artiste. Les autres scènes, la proposition vidéo, le calage des voix et la pause/clochette doivent encore être validés par l’artiste. Aucun contrôle auditif de synchronisation mot à mot n’est revendiqué.

## Fichiers et intégrité

| Fichier | Taille | SHA-256 |
|---|---:|---|
| Maître source `../../je me relève toujours 3.mp3` | inchangé | `7be46536d3ddf4df3ca0fdda37ff2c1777409cb0c470e62cd83176935add473e` |
| Dérivé `livrables/Je_me_releve_toujours_Dsky.mp3` | 7 086 668 octets | `0827adf23044ca7172f6aabb3dadf73cc9769d69f85176bcddb43e419ec42f7f` |
| Proposition `livrables/Je_me_releve_toujours_9x16.mp4` | 21 482 658 octets | `01283a504d1707e3c77664c05b5e66ae84ef04ddb2f6236cd6fed23395718e95` |
| Pochette `livrables/cover-dsky-1080.jpg` | 242 748 octets | `b0dbb6fd4089d82ed46818b802f7b3956da60ca4943093abd93acd5c18bde5e1` |

Le maître a été relu après fabrication et son hash est identique. Le dérivé est une nouvelle copie normalisée/taguée; les commentaires `made with suno` et l’URL de provenance du maître sont conservés dans ses métadonnées. Le manifeste C2PA du maître n’a pas été recopié comme valide sur un fichier transcodé. **Déclaration : visuels IA OUI; audio IA OUI — provenance Suno indiquée dans le maître.**

## Durées, flux et structure

- Maître et dérivé : **11 036 159 échantillons décodés à 48 000 Hz**, soit **229,919979 s**. Le temps d’en-tête MP3 donné par Mutagen est **229,944 s**; il ne remplace pas la durée décodée.
- MP4 : **7 048 frames**, **30/1 fps**, **1080 × 1920**, H.264 High, `yuv420p`, BT.709; **234,933333 s** pour le conteneur et la piste vidéo, 234,933 s pour la piste AAC. L’AAC décodé brut peut contenir environ 10,7 ms de padding silencieux supplémentaires; la durée des pistes dans le conteneur correspond au montage. Données brutes dans `QC-ffprobe.json`.
- Carte finale : première frame à **229,933333 s**, dernière fin à **234,933333 s**; 5,0 s. Le titre d’accueil occupe le début instrumental et le premier vers commence au premier frame ≥ **5,03 s**.
- `moov` à l’octet 36, `mdat` à l’octet 260 496 : **faststart présent**.
- Les 58 timestamps source sont inchangés dans la carte; l’arrondi au premier frame disponible ajoute de **0 à 30 ms**, toujours moins d’une frame à 30 fps. Ceci contrôle le calcul, pas l’alignement réel de chaque mot chanté.
- Comparaison MP3 dérivé / audio MP4 par corrélation sur six extraits à 10, 60, 120, 180, 210 et 220 s : décalage mesuré **0,000 s** à la résolution 1/8 000 s, corrélations de **0,99951 à 0,99995**. Script : `verify_audio_alignment.py`. Ce contrôle vérifie la position du son, **pas** la justesse des paroles par rapport au chant.

## Mesures audio après encodage

Mesures ffmpeg `ebur128=peak=true`; la normalisation emploie deux passes `loudnorm` avec cible pré-encodage −14 LUFS / −2,0 dBTP et peut agir dynamiquement.

| Source mesurée | LUFS intégrés | LRA | Crête vraie |
|---|---:|---:|---:|
| Maître | −13,6 | 6,6 LU | −0,9 dBTP |
| MP3 dérivé encodé | −13,9 | 5,2 LU | −1,8 dBTP |
| Audio AAC du MP4 | −14,0 | 5,2 LU | −1,4 dBTP |

Le MP4 utilise la même matière audio que la copie dérivée, avec fondu d’entrée de 0,30 s, fondu de sortie sur les trois dernières secondes et silence de carte finale. Après conservation supplémentaire du commentaire source dans les tags du MP3, le SHA-256 du PCM décodé est resté identique (`63167cd8b428b7a9049663a7725b503e35dba1ecbfddd9176d27f81776911731`).

## Contrôles vidéo réels

- `blackdetect=d=0.05:pix_th=0.10` : **0 intervalle noir** détecté.
- `freezedetect=n=-33dB:d=2.5` : **6 débuts de plage signalés**, pas « zéro gel » :
  - 0,000 → 5,033 s : carte d’accueil fixe;
  - 203,733 → 208,700 → 215,167 → 222,400 → 225,033 s : quatre plages contiguës dans la longue pause **supposée** instrumentale; le décor est animé par un déplacement trop lent pour ce seuil et la clochette apparaît à 208,0–212,5 s;
  - début à 229,933 s jusqu’à la fin du fichier : carte finale fixe. `freezedetect` ne signale pas de fin après la dernière frame.
- Ces détections ne prouvent pas que la pause soit sans voix. Il faut **l’écouter**, valider la clochette et, si nécessaire, modifier/rerendre. Les autres vers ne sont pas signalés par ce réglage.
- 61 frames réellement extraites du MP4 : une pour chaque occurrence, plus accueil, clochette et finale. Planches `CONTROLE-rendu-01.jpg` à `06.jpg` et `CONTROLE-rendu-cartes-clochette.jpg` relues; 16 frames des 30 dernières secondes dans `CONTROLE-rendu-30dernieres-secondes.jpg` relues.
- Crops 1:1 aux secondes 12,60 / 123,80 / 190,10 / 225,60 : lettrages sérif et cursif lisibles, sans dédoublement constaté; notamment texte et traduction de `monwê`, scène 04-aube corrigée et outro. Planche : `CONTROLE-rendu-typo.jpg`.
- Scène 04-aube v1 rejetée pour contraste après le premier rendu; v2 régénérée avec même style sérif, contrôlée et incorporée. Comparaison et historique : `CONTROLE-salve07.jpg`, `SALVE-07.md`.
- Les traductions anglaise et multilingue sont dans la bande basse; l’original est peint. Les signatures WTBW restent sans traduction; le sens isolé de `wê` n’a pas été confirmé. Tous les autres états de validation restent dans `BRIEF.md`.

## Vérifications reproductibles

```sh
python3 -m venv .venv
.venv/bin/pip install -r productions/je-me-releve-toujours/requirements.txt
.venv/bin/python -m unittest discover -s productions/je-me-releve-toujours/tests -v
.venv/bin/python productions/je-me-releve-toujours/verify_audio_alignment.py
```

Les 5 tests structurels passent; ils ne remplacent ni une lecture visuelle, ni une écoute, ni l’approbation de l’artiste. Le clip dure près de 3 min 55 s : vérifier la limite de durée applicable au mode de publication choisi sur chaque plateforme.
