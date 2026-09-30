# Concentré sur le chemin — Daïsky

**Pack exporté et contrôlé · 30 septembre 2026**

Les dix fonds sont approuvés (« Oui je valide !! »). Les clips utilisent ces cinq scènes
animées dans les deux formats, sans nouvelle génération : vêtements usés, fumoir/studio,
cigarette, deux mains sur la tête, gros caractères gras au centre.

## Les fichiers

| Usage | Fichier | Détails |
|---|---|---|
| TikTok / Reels / Shorts | [Clip 9:16](Concentre_sur_le_chemin_9x16_v1.mp4) | 1080 × 1920 · 30 fps · 30.15 Mo |
| YouTube | [Clip 16:9](Concentre_sur_le_chemin_16x9_YT_v1.mp4) | 1920 × 1080 · 30 fps · 29.38 Mo |
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
- Master : **-14.02 LUFS** et
  **-1.64 dBTP** mesurés après encodage.
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
Rapports : `productions/concentre_sur_le_chemin/qa_{portrait,landscape}.json`,
`audio_master_report.json`, `covers_report.json`, `delivery_manifest.json` et
`delivery_remote_checks.json`. Les caches et WAV sous `work/` ne sont pas versionnés.
La maquette de 14,5 s reste une ancienne étape de validation ; utiliser les clips complets ci-dessus.
