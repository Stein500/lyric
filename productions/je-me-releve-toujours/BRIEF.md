# Brief de production — « Je me relève toujours »

> **État général :** ancre **générée, contrôlée et validée par l’artiste**. Trois salves de 10 images ont été générées. La carte des paroles est construite; certains plans restent à refaire. Aucun rendu 9:16 final n’est déclaré livré.

## Paramètres validés / source

| Champ | Valeur / état |
|---|---|
| Titre | `Je me relève toujours` — nom du fichier de paroles et balise `TIT2` du maître audio. |
| Artiste | **Dsky** — choisi par l’artiste pour les métadonnées et l’écran. Le badge vidéo alterne **WTBW / DSKY** d’un vers au suivant. |
| Paroles | `../../Je me relève toujours.txt` — 58 lignes horodatées et 43 textes distincts; horodatages source conservés. |
| Mode | **PEINT**, choisi par l’artiste. Toutes les paroles visibles dans une image sont écrites explicitement dans le prompt de cette image; texte ajouté par le modèle = rejet QC. |
| Style / personnage | Tomate-héroïne 3D douce et cinématographique, avec yeux, sourcils-feuilles, petits bras et pieds. Ancre validée par l’artiste. |
| Motif d’histoire | La tomate tombe et se relève; l’arc passe des ombres/pluie aux premières lueurs au pont, puis à l’aube sur le refrain final et l’outro. |
| Langues | Principalement FR; une ligne EN; signatures WTBW; une ligne multilingue. Pour `Yeah... I'm still standing...`, traduction FR proposée : `Ouais... je suis toujours debout...`. Pour `Arigato, gracias, merci, monwê`, gloss artiste : `monwê` = « c’est ça / c’est confirmé »; traduction retenue : `Merci, merci, merci — c’est confirmé.` |
| Habillage | WTBW v6.0 sans code; accueil/finale et stickers doux à construire. Badge alterné WTBW/DSKY. |

## Progression des images

- Carte : `verses_map.json` et `CARTE-VERS.md`, générés par `build_map.py`; `disponible` est recalculé par existence de fichier.
- Le texte identique est réutilisé; les reprises du refrain final ont des variantes d’aube dédiées.
- **Contrat d’affichage** : chaque parole peinte est écrite verbatim dans son prompt; tout mot, signe ou texte ajouté par le modèle entraîne le rejet. Le badge vidéo `WTBW` / `DSKY` alterné, les cartes et les CTA seront composités selon les chaînes exactes du prompt, jamais improvisés par le générateur.
- **24 fichiers image actifs sur 47 chemins d’image distincts** sont disponibles après contrôle; les scènes 16 et 25 restent rejetées à refaire. Les journaux et planches sont dans `SALVE-01.md`, `SALVE-02.md`, `SALVE-03.md` et `CONTROLE-salve*.jpg`.
- `affichage_s` applique la formule v6.0 et reste **provisoire** jusqu’au calage mot à mot.
- Aucun code de fin, drapeau, contact, lien, QR ou logo ne sera ajouté.

## Métadonnées audio — modification demandée

L’artiste a demandé le changement des métadonnées et a choisi **Dsky**. Le maître fourni restera intact; la version normalisée/taguée sera un **fichier dérivé** dans `livrables/` avec titre `Je me relève toujours` et artiste/album-artiste `Dsky`. Les paroles USLT seront propres, sans horodatages; une pochette APIC carrée 1080 × 1080 sera produite; les champs TXXX incluront la signature WTBW, le maître source et la déclaration IA.

Durée décodée avec ffmpeg 7.0.2 : **229,91 s (3:49.91)**. Mesures ebur128 : **−13,6 LUFS intégrés**, **LRA 6,6 LU**, **true peak −0,9 dBFS**; astats : crête −0,896 dBFS.

Les commentaires ID3 source contiennent `made with suno` et un lien Suno. La déclaration de provenance de la copie balisée indiquera donc **audio IA : OUI**, à moins que l’artiste fournisse un autre maître dont la provenance non-IA est vérifiable. Ces métadonnées de provenance ne seront pas effacées pour faire croire à un audio non généré.

## Prochaines étapes

1. Régénérer les scènes 16 et 25; créer les scènes 27–34 en salve de 10 maximum.
2. Continuer les salves, le contrôle typo et les variantes aube.
3. Fabriquer le rendu et le fichier audio dérivé après validation des assets et des champs finaux.
4. À la fin, livrer le **prompt universel complet mis à jour**, auto-suffisant, intégrant la tomate-héroïne, le badge WTBW/DSKY alterné, les glosses bilingues et les contrôles observés.
