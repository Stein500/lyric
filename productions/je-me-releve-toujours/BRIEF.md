# Brief de production — « Je me relève toujours »

> **État actuel :** ancre validée par l’artiste; sept salves consignées, dont la correction de contraste de la scène 04-aube après le premier rendu. **Une proposition de montage 9:16 est rendue et contrôlée techniquement**, avec MP3 dérivé et prompt universel complet. La validation artistique des scènes et du montage ainsi que l’écoute du calage restent à faire : ne pas présenter cette proposition comme approuvée définitivement.

## Paramètres et décisions

| Champ | Valeur / état |
|---|---|
| Titre | `Je me relève toujours`, titre du fichier de paroles et balise `TIT2` du maître. |
| Artiste | **Dsky**, choisi par l’artiste pour les métadonnées. Badge vidéo alterné **WTBW / DSKY** d’un vers au suivant. |
| Paroles | `../../Je me relève toujours.txt` — 58 lignes horodatées et 43 textes distincts; horodatages source conservés. |
| Mode | **PEINT**, choisi par l’artiste. Toute parole générée est écrite explicitement dans son prompt; ajout non sollicité = échec QC. |
| Personnage | Tomate ronde rouge 3D, yeux expressifs, sourcils/calyx feuillus, petits bras et pieds. Ancre approuvée; autres scènes non encore approuvées par l’artiste. |
| Arc | La tomate tombe et se relève; les ombres et la pluie laissent place à l’aube au pont, au refrain final et à l’outro. |
| Traductions | `Yeah... I'm still standing...` → `Ouais... je suis toujours debout...`; `Arigato, gracias, merci, monwê` → `Merci, merci, merci — c'est confirmé.` L’artiste confirme `monwê` = « c’est ça / c’est confirmé ». |
| Signature | `Wolof TechStein beat wê...` / `Wolof TechStein beat wê!` restent peintes comme signatures, sans traduction; le sens isolé de `wê` n’a pas été confirmé pour une éventuelle traduction. |
| Habillage | Stickers WTBW d’accueil/finale, badge alterné, traductions compositées en bande basse; pas de code à quatre chiffres, drapeau, contact, lien, QR ou logo parasite à l’écran. |

## Images et carte

- `verses_map.json` et `CARTE-VERS.md` sont générés par `build_map.py`; l’existence des chemins est recalculée. **58/58 occurrences** disposent d’une image; **47/47 chemins distincts** sont actifs.
- Journaux : `SALVE-01.md` à `SALVE-07.md`; planches : `CONTROLE-salve*.jpg`. Après le premier rendu, la scène 04-aube v1 a été rejetée pour contraste insuffisant et remplacée par la v2; voir `SALVE-07.md` et `CONTROLE-salve07.jpg`.
- Les lettrages sérif, script ou cursifs de chaque scène sont conservés; aucune lettre n’a été retouchée ou recomposée. Les ajouts d’habillage sont des chaînes explicites, pas des inventions du modèle.
- La carte distingue l’heuristique `affichage_s` et le montage réellement utilisé. Faute de fin chantée fournie, chaque vers reste lisible jusqu’au suivant, sauf la signature n°57, provisoirement éteinte après 2,20 s dans une longue pause supposée. Le calage à l’oreille et la clochette à 3:28–3:32,5 restent à vérifier.

## Audio et provenance

- Maître `../../je me relève toujours 3.mp3` intact : SHA-256 `7be46536d3ddf4df3ca0fdda37ff2c1777409cb0c470e62cd83176935add473e`. Durée décodée **11 036 159 échantillons à 48 kHz = 229,919979 s**. L’ancienne valeur 229,91 s provenait de l’affichage tronqué de ffmpeg.
- Maître mesuré : **−13,6 LUFS**, **LRA 6,6 LU**, **−0,9 dBTP**. Ses commentaires ID3 indiquent `made with suno` et contiennent une provenance Suno.
- Dérivé `livrables/Je_me_releve_toujours_Dsky.mp3` : titre/artiste/album-artiste vérifiés, paroles `USLT` sans horodatages, pochette 1080², commentaire Suno et URL de provenance préservés dans les tags. **Audio IA : OUI**. Le manifeste C2PA du maître n’est pas recopié comme valide après transcodage; maître et hash restent traçables.
- Dérivé encodé mesuré : **−13,9 LUFS**, **LRA 5,2 LU**, **−1,8 dBTP**. Traitement `loudnorm` deux passes, cible pré-encodage −14 LUFS / −2,0 dBTP; source et dérivé ne sont pas confondus.

## Montage rendu et contrôles

- Proposition : `livrables/Je_me_releve_toujours_9x16.mp4` — 1080 × 1920, 30 fps, 7 048 frames, **234,933333 s**, H.264/AAC, 21 482 658 octets; carte finale après l’audio. Contrôles détaillés et limites dans `RAPPORT-QC.md`.
- Frames du MP4 : `CONTROLE-rendu-01.jpg` à `CONTROLE-rendu-06.jpg`, `CONTROLE-rendu-typo.jpg`, `CONTROLE-rendu-cartes-clochette.jpg` et `CONTROLE-rendu-30dernieres-secondes.jpg`. Coupes nettes entre vers pour éviter deux textes simultanés; un décor sans paroles accompagne la pause supposée.
- **0 intervalle noir** détecté à `d=0,05` / `pix_th=0,10`; niveau MP4 **−14,0 LUFS / −1,4 dBTP**; `moov` avant `mdat`. `freezedetect` signale les cartes fixes et les déplacements très lents entre 3:23,73 et 3:45,03 : voir rapport, ne pas déclarer « zéro gel ».
- La comparaison audio automatisée ne révèle pas de décalage entre la copie MP3 et le son du MP4 sur six extraits; elle **ne remplace pas une écoute des paroles** ni l’approbation artistique.

## Prochaines étapes

1. Faire écouter et valider artistiquement le montage et les scènes; vérifier notamment la fenêtre de clochette présumée instrumentale et le calage des voix.
2. Si la signature WTBW doit également être traduite, demander le sens de `wê` au lieu de le deviner.
3. Appliquer les corrections demandées, rerendre et revérifier avant de déclarer une version finale approuvée.
4. Prompt complet mis à jour : `../../PROMPT_UNIVERSEL_v6.1_COMPLET.md`; les versions précédentes sont conservées.
