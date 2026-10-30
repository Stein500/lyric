# Salve 03 — corrections + scènes 20 à 26

## Bilan réel

- **Demandées** : 10 images (corrections des scènes 10, 13 et 16; scènes 20 à 26)
- **Générées** : 10 images
- **QC visuel/typo accepté par l’agent** : 8 images — scènes 10, 13, 20, 21, 22, 23, 24 et 26
- **Échecs consignés** : 2 images — scènes 16 et 25
- **Taille** : 768 × 1376 px par image
- **Contact sheet** : `CONTROLE-salve03.jpg`, 2 colonnes × 5 rangées; chaque tuile fait 500 × 896 px
- **Contrôle typo 1:1** : `CONTROLE-salve03-typo.jpg`, grille de 16 px
- **Retouche de lettres** : aucune
- **Validation par l’artiste** : en attente pour cette salve; l’ancre seule est déjà validée.

## Contrôle par scène

| Scène | Vers source | État QC | Note |
|---:|---|---|---|
| 10 | `J'ai vu des promesses s'envoler comme des abeilles` | QC accepté — correction | Vers exact, sans point final; palette bleue sombre, sans soleil. |
| 13 | `On m'a dit "t'es trop petit, t'es trop lent, t'es trop différent"` | QC accepté — correction | Une seule paire de guillemets autour de la parole citée; plus de guillemets externes. |
| 16 | `Chaque larme versée est devenue une œuvre` | **Échec — à régénérer** | Le texte est correct, mais le modèle a dessiné une barre d’interface sociale et des icônes sur la droite. Version écartée dans `fonds/rejected/scene-16-v2-ui-overlay.png`. |
| 20 | `Je pleure, je rêve` | QC accepté | Texte relu. |
| 21 | `Je lutte, je vis` | QC accepté | Texte relu. |
| 22 | `Je suis le fils de la pluie et du cri` | QC accepté | Texte relu. |
| 23 | `J'ai touché le fond, j'ai vu le vide en face` | QC accepté | Texte relu. |
| 24 | `J'ai senti la mort frôler ma peau, ma trace` | QC accepté | Texte relu; ombre symbolique, sans gore. |
| 25 | `Mais j'ai gardé la tête haute, j'ai gardé l'envie` | **Échec — à régénérer** | Le modèle a ajouté un point final après `envie`; le vers source n’en a pas. Version écartée dans `fonds/rejected/scene-25-v1-extra-period.png`. |
| 26 | `Je suis un guerrier, je suis né pour la vie` | QC accepté | `né` relu avec accent; pose sans arme. |

## Contrat texte

Tous les mots demandés pour les plans de cette salve figurent explicitement dans le prompt correspondant. Le modèle a tout de même ajouté une interface à la scène 16 et un point final à la scène 25; ces deux images sont rejetées, pas livrées.

## Prochaine salve

Régénérer les scènes 16 et 25, puis produire les scènes 27 à 34 — **10 générations maximum**. Les chemins rejetés restent exclus des images actives.
