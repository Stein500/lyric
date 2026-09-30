# Point de reprise — ne pas recommencer la production

Mise à jour : **2026-09-30**.

Consigne explicite de l’artiste : **« Continue et arrête de recommencer à chaque fois.. commit chaque changement »**.

## Le pack existe déjà

- Les **dix fonds sont approuvés** : « Oui je valide !! ». Ne pas les régénérer.
- Deux clips complets exportés et contrôlés : `livrables/Concentre_sur_le_chemin_9x16_v1.mp4` et `livrables/Concentre_sur_le_chemin_16x9_YT_v1.mp4`.
- Master MP3 320 kb/s / 48 kHz avec APIC et USLT, trois pochettes, dix fonds, LRC et prompts : présents et publiés.
- Index : `livrables/LIVRAISON_Concentre_sur_le_chemin.md`.
- Commandes : `livrables/TERMUX_Concentre_sur_le_chemin_COMPLET.md`.
- Manifeste des fichiers exacts : `delivery_manifest.json` ; preuves GitHub et contenu téléchargé : `delivery_remote_checks.json`.
- **56 tests réussis, aucune erreur ni test ignoré** : `test_run_report.json`.

Commit immuable des médias et du prompt : `7321792a9d81bff773c695287e58a76b602b0a5e`.

Commit de publication des commandes et contrôles : `5c1798fb9cbe6f2aa325d8b746373a1f74e3ef8e`.

Ces hashes sont des checkpoints effectivement poussés, pas des noms de branche ni des chemins fictifs. Les commandes restent attachées au commit des médias ; les nouveaux commits de suivi ne demandent pas de les réécrire.

## Prochaine action

**Présenter les livrables existants.** Puis attendre un éventuel retour ciblé de l’artiste ; ne pas relancer toute la production pour une demande « continue ».

La validation visuelle ne vaut pas validation vocale : le mot à mot est estimé depuis le LRC, `approvals.vocal_sync=false`. La coupe du hook est montée selon l’option demandée, sans approbation séparée. Ne pas transformer ces limites en prétexte pour regénérer les images ou recommencer l’analyse/audio.

## Règles de continuation

1. Avant toute reprise, lire ce fichier, `production.json` et `delivery_manifest.json`, puis inspecter `git status` et l’historique distant de **`arena/01a0e931-lyric`**.
2. Si le checkout revient à un ancien HEAD alors que la sauvegarde publiée est plus récente : comparer les fichiers locaux aux checkpoints et préserver toute différence non reconnue. Récupérer les artefacts publiés absents, **pas les recréer**. Aucun `reset --hard` ni changement de branche.
3. Vérifier les tailles/SHA-256 du manifeste avant d’annoncer qu’un livrable manque. Un cache WAV/PNG absent sous `work/` ne signifie pas que le pack publié est absent.
4. Ne pas relancer les scripts de rendu, de master, de covers ou de génération IA sur des sorties inchangées et déjà contrôlées. Les vérifications antérieures et leurs rapports sont conservés.
5. Pour une correction explicite : modifier seulement les paramètres/vers/formats concernés, conserver les fonds approuvés et les sources, puis contrôler l’export modifié. Ne pas toucher aux livrables non concernés.
6. **Commit et push immédiatement après chaque changement/étape**, sur la branche de session uniquement. Ne pas laisser de travail non sauvegardé en attendant une autre étape ou un autre tour.
7. Si des médias changent réellement, produire un nouveau manifeste et de nouvelles commandes après leur publication/vérification. Sinon garder les liens immuables actuels.
