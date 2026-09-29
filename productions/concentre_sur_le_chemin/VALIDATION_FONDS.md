# Dix fonds — contrôle de la salve, 2026-09-29

**Ancre approuvée par l’artiste : « Oui continue... ». Série complète encore à confirmer.**

## Livraison de cette étape

- `livrables/Concentre_sur_le_chemin_planche_10_fonds_v2.jpg` : planche des cinq paires, sans faux statut « approuvé » sur les nouvelles compositions.
- `livrables/Concentre_sur_le_chemin_10_images_v2.zip` : **exactement dix JPG** et un court `LISEZ_MOI.txt`.
- Dossier des JPG individuels : `livrables/images_concentre_sur_le_chemin/{portrait,landscape}/`.
- Prompt universel complet à jour : `PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md`.
- Prompts complets des générations : `PROMPTS_IMAGES_Concentre_sur_le_chemin.md`, y compris la reprise du 29 septembre écrite avant lancement.
- État courant, hashes et corrections : `production.json`, `backgrounds_manifest.json`, `landscape_corrections_v2.json`.

La planche v1 historique signalait des paysages incomplets : **elle est remplacée par la v2**, qui montre dix exports disponibles.

## Budget et continuité

Les fichiers locaux étaient au checkpoint précédent tandis que la branche distante contenait la salve. Reprise depuis `67525732617ae9b6acfb23243b43c8f3f999004c` après comparaison des contenus avec le dernier checkpoint publié : fichiers locaux distincts refusés par le script de récupération, pas de `reset --hard` ni effacement du travail utilisateur.

- Cinq portraits existants conservés ; **aucune nouvelle génération portrait** pendant cette étape.
- Cinq appels correctifs pour remplacer les cinq paysages : cadrages plus complets, lumière continue, suppression des anciens aplats rectangulaires par nouvelle composition plutôt que réutilisation de masques d’éclaircissement.
- Les anciens paysages restent dans l’historique Git, **pas comme cinq scènes supplémentaires** dans le pack.
- Chaque correction utilise les trois originaux autorisés du dossier **Samu** et l’ancre approuvée en quatrième référence.
- Total livré : **cinq scènes × deux formats = dix fonds**, pas une image par vers.

## Contrôles effectués

| Contrôle | Résultat |
|---|---|
| Inventaire | 5 portraits + 5 paysages, slots s01 à s05, aucun doublon |
| Dimensions JPG | Portrait 1080×1920 ; paysage 1920×1080 |
| Personnage | Visages, lunettes, mains sur la tête, cigarette et vêtements usés contrôlés visuellement sur la série |
| Post-production locale | Intégrité des pixels du personnage vérifiée hors masques de nettoyage |
| Badge | **Aucun badge permanent dans les fonds** ; il sera animé séparément à chaque vers dans les clips |
| Drapeau | Géométrie vectorielle : tiers gauche vert, haut droit jaune, bas droit rouge |
| Hauteur bandeau | 54 px portrait ; 30 px paysage |
| Couleurs PNG | Pixels exacts #008751 / #FCD116 / #E8112D |
| Couleurs JPG | Échantillons contrôlés à ±5 niveaux par canal après compression |
| Archive | Dix images, CRC ZIP valide, chaque contenu correspond au SHA-256 du manifeste |
| Tests | **31 tests automatisés réussis**, analyse + ancre + fonds |

### Nettoyages précis

1. **s02 portrait** : lettrage parasite au plafond, loin du personnage, retiré uniquement dans un masque de glyphes. Les pixels sous y=210 de l’original restent intacts.
2. **s03 paysage** : trois autocollants repris des références retirés par des masques ciblés, sans repeindre une grande bande du plafond. Trois faux libellés du rack à droite sont également effacés localement, sans supprimer les commandes matérielles. Le tiers gauche contenant le personnage reste identique.
3. **Portraits** : reprise du cadrage de l’ancre. Le sol ajouté sur les autres portraits est adouci, sans changer les pixels d’origine du personnage. La composition de s01 reste exactement celle approuvée.
4. **Paysages** : mise au ratio proportionnelle puis cadrage relevé de 80 px dans la marge de plafond. Prolongement du seul sol en bas, pas de bordures latérales floues ni de mise à l’échelle non proportionnelle du corps. La personne reste entière au-dessus du bandeau dans les exports.

Les originaux IA ne sont pas modifiés par ces opérations : les nettoyages s’effectuent sous `work/`, puis les exports sont composés avec le drapeau en post.

## Ce qui reste à faire

- **Validation de la série par l’artiste** : choix des dix compositions avant de figer leur utilisation dans les clips.
- Les grosses paroles, le mode mot-à-mot + vague et le badge en fondu restent ceux de la maquette approuvée. Les fonds sans texte sont volontairement des calques de montage, pas des captures finales du clip.
- Tester le cadrage pendant les mouvements et l’overlay des paroles dans les deux formats ; ne pas déduire d’une image fixe que tous les futurs Ken Burns sont sûrs. Le paysage s03 nécessite notamment un mouvement horizontal conservateur, car la chaussure gauche est proche du bord.
- Valider les trois passages de synchronisation, les fins des vers et le calage des mots. La proximité d’un pic instrumental n’est pas une validation vocale.
- Clips complets, MP3 master deux passes, covers et commandes Termux finales : **non livrés à cette étape**.

## Reproduire les exports et les tests

```sh
bash scripts/setup_env.sh
/tmp/lyric-venv/bin/python scripts/prepare_backgrounds.py
/tmp/lyric-venv/bin/python -m unittest discover -s tests -v
```

`opencv-python-headless` est désormais épinglé dans les dépendances, car le nettoyage local l’exige. Aucun appel IA dans ces commandes. Les caches PNG sans perte se régénèrent sous `work/concentre_sur_le_chemin/backgrounds/`. Ne pas appliquer les anciens masques de gain de la révision 1 aux nouveaux paysages.
