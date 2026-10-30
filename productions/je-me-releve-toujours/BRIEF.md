# Brief de production — « Je me relève toujours »

> **État général :** ancre **générée, contrôlée et validée par l’artiste**. La carte des paroles est construite. La salve 01 a produit 10 images; 8 passent le contrôle préliminaire, 2 sont écartées et à régénérer. Les autres visuels et le rendu 9:16 ne sont pas encore livrés.

## Paramètres

| Champ | Valeur / état |
|---|---|
| Titre | `Je me relève toujours` — présent dans le nom du fichier de paroles et dans la balise `TIT2` du maître audio. |
| Artiste affiché | **À confirmer.** La balise `TPE1` du MP3 indique `stein2000`; à utiliser comme nom d’écran seulement après confirmation, ou à remplacer par la signature souhaitée. |
| Paroles | `../../Je me relève toujours.txt` — 58 lignes horodatées et 43 textes distincts; horodatages source conservés. |
| Audio maître | `../../je me relève toujours 3.mp3` — durée décodée **229,91 s (3:49.91)** avec ffmpeg 7.0.2. ebur128 : **−13,6 LUFS intégrés**, **LRA 6,6 LU**, **true peak −0,9 dBFS**; astats : crête réelle observée −0,896 dBFS. Le calage de la dernière ligne est donc 225,02 → 229,91 s. |
| Mode | **PEINT**, choisi par l’artiste. |
| Style / personnage | Tomate-héroïne 3D douce et cinématographique, avec yeux, sourcils-feuilles, petits bras et pieds. L’ancre de cette direction est **validée**. |
| Langues | Principalement FR; une ligne EN; une ligne multilingue (« Arigato, gracias, merci, monwê »); signatures WTBW. La traduction FR de `Yeah... I'm still standing...` est proposée « Ouais... je suis toujours debout... ». Le sens de `monwê` reste à confirmer. |
| Habillage | WTBW v6.0 sans code; cartes accueil/finale à créer. |

## Provenance audio — point à confirmer avant la livraison finale

Les commentaires/étiquettes ID3 du fichier contiennent `made with suno`. Cela ne permet pas de déclarer « audio NON généré ». La directive de livraison v6.0 indique « visuels OUI / audio NON » et le maître est supposé fourni par l’artiste, jamais généré : il y a donc une **contradiction à résoudre avec l’artiste** avant d’écrire la déclaration IA finale. Le fichier maître fourni n’a pas été modifié.

## État des paroles et des images

- `build_map.py` génère `verses_map.json` et `CARTE-VERS.md`; le champ `disponible` est recalculé avec l’existence réelle de l’image.
- Les répétitions textuellement identiques réutilisent leur image de base; les reprises du refrain final ont des chemins de variantes d’aube dédiés.
- L’affichage `affichage_s` suit la formule v6.0 et reste **provisoire** jusqu’au calage mot à mot.
- Traduction du vers multilingue bloquée tant que le sens de `monwê` n’est pas établi.
- Aucun code de fin, drapeau, contact, lien, QR ou logo ne sera ajouté.

## Prochaine étape

Générer et contrôler la première salve de 10 nouveaux visuels (scènes 02 à 11), en utilisant l’ancre comme référence. Avant les cartes finales, confirmer le nom d’artiste à l’écran et la provenance IA réelle de l’audio.
