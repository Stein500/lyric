# Concentré sur le chemin — brief de production

Création : 2026-09-28. Mise à jour : 2026-09-30. Branche de session : `arena/01a0e931-lyric`.

**Étape actuelle : les dix fonds sont approuvés (« Oui je valide !! »). Clips portrait et YouTube complets contrôlés, master et trois pochettes exportés. Livraison v1 prête techniquement ; contrôle vocal à l’écoute toujours distinct.**
Les références originales du dossier `Samu` ont été explicitement autorisées. Les cinq scènes sont disponibles en portrait et paysage ; chaque correction IA utilise les trois originaux Samu autorisés et l’ancre approuvée. Le mot à mot reste estimé depuis le LRC source : contrôle technique du montage ≠ validation vocale à l’écoute.

## Sources confirmées

L'artiste a confirmé : « C'est concentré sur le chemin..la chanson ».

- Audio : `Concentré sur le chemin.mp3`.
- Paroles source : `concentré sur le chemin.txt`.
- Copie LRC UTF-8 : `Concentré sur le chemin.lrc` (horaires source conservés ; seuls les caractères directionnels invisibles et les métadonnées de durée sont normalisés).
- Voir `ANALYSE.md` pour les mesures, limites et commande de reproduction.

## Consignes explicites prioritaires

Ces choix remplacent les exemples contradictoires de « Nonvi Konou », les défauts du référentiel v5.3 et l'addendum d'une autre chanson.

1. **Paroles très grandes**, vers complets, au centre du bloc final. Retours à la ligne avant toute réduction excessive. Aucun texte coupé. Réserver le visage au-dessus du bloc central dès le cadrage, plutôt que déplacer les paroles dans la bande basse.
2. **Un badge qui apparaît et disparaît avec CHAQUE vers**, même quand le fond reste le même. Fondus de 0,4 s, opacité maximale 75 %, pas de badge permanent gravé dans les fonds. Position fixe pendant chaque apparition ; animation de l'opacité seulement.
3. **Cinq scènes, chacune déclinée en deux compositions : cinq portraits 9:16 et cinq paysages 16:9.** Dix fonds finaux, pas une image par vers. Les reprises et tous les autres vers réutilisent ce petit ensemble selon la structure musicale. Aucune génération supplémentaire pour l'intro, l'endcard ou les covers.
4. **Héros animé à la ressemblance de l'artiste**, pas le héros fictif photoréaliste d'un autre morceau. Ne jamais envoyer une photo du dépôt au générateur sans confirmation qu'elle est une référence autorisée de cette chanson. Conserver proportions, traits, teint, cheveux, barbe et lunettes selon les photos retenues ; ne pas embellir ni muscler le personnage.
5. **Vêtements de misère** : vêtements ordinaires très usés, délavés, rapiécés, manches effilochées. Tenue cohérente sur les cinq scènes, sans luxe ni accessoires inventés.
6. **Fumoir qui est aussi un studio de musique**, matériel ancien, cabine, microphone, console et enceintes sans marques ; fumée atmosphérique.
7. **Les deux mains sur la tête et une cigarette tenue entre les doigts**. Pose proposée : cigarette entre index et majeur de la main droite posée près de la tempe, extrémité dirigée loin du visage. Les deux mains restent sur la tête, sans main surnuméraire et sans visage caché. Aucun changement de pose incompatible dans les scènes suivantes.

## Choix du questionnaire validés et détails de maquette

- Style validé : animé seinen semi-réaliste, nuit bleu-noir, contre-jour ambre et bord cyan discret ; lumière plus douce sur le pont.
- Texte : mode hybride **mot à mot + vague simultanée**, mot actif or/crème, mots passés atténués mais lisibles. Largeur finale du vers calculée avant animation. **Gras validé** : Barlow Condensed Bold pour les paroles, DejaVu Sans Bold pour l’UI ; « gros puis petit sans vague » n'est pas activé automatiquement.
- Repères de taille à tester : gras 104–112 px en 1080×1920 ; 96–112 px en 1920×1080. Tailles indicatives, validation sur les vrais vers longs et sur mobile. Le bloc entier est centré verticalement, chaque ligne horizontalement.
- Badge validé : `Dsky` + drapeau vectoriel Bénin, fondu à chaque vers. **Bandeau Bénin de 54 px validé**. Ces choix viennent du questionnaire de cette chanson, pas d’une attribution automatique depuis un autre exemple.
- Cold-open monté selon l’option demandée : deux premières lignes du refrain le plus énergétique, intervalle source 01:53.28 → 02:00.18, soit **6,90 s**. La coupe n’a pas reçu d’approbation séparée ; vérifier à l’écoute. Variante sans ouverture possible si demandée.
- Covers : réutilisation d'un fond validé, titre exact et artiste en post-production ; aucun lettrage généré par IA.
- Pack complet validé : clips 1080×1920 + 1920×1080, MP3 320 kb/s 48 kHz de la chanson seule, covers carré 1080 + portrait + paysage, prompt universel mis à jour, commandes Termux au hash publié. Variante ≤50 Mo uniquement si demandée.
- Artiste / contacts du pack validé : Daïsky ; `daiskyproduction@gmail.com` ; WhatsApp `+229 01 61 16 24 08` / `+229 01 49 11 49 51`. Ne pas ajouter une longue liste de crédits.

## Cadrage et safe zones

- Portrait 1080×1920 : badge sous y=144 ; visage et mains dans le tiers supérieur en laissant la place au badge ; paroles centrées autour de y=960. Pour un bloc symétrique à x=540, **largeur ≤720 px** (x=180→900) pour rester avant le rail droit x≥910. L'ancienne largeur de 880 px centrée dépasserait ce rail.
- Aucune parole/contact à y≥1574 ; pas de CTA fixe.
- Paysage 1920×1080 : bloc paroles au centre, largeur contrôlée, pas dans la bande des contrôles y≥960. Le visage est décalé à un tiers si nécessaire.
- Scrim central doux localisé sous les paroles, pas un voile opaque sur le visage.
- Bandeau Bénin validé : vectoriel en post, 54 px tout en bas du portrait (y=1866→1920), vert #008751 sur le tiers gauche, jaune #FCD116 en haut à droite, rouge #E8112D en bas à droite. Hauteur relative identique pour les autres formats ; tests de pixels. Le badge reste animé séparément.

## Storyboard proposé — cinq scènes seulement

Le bloc héros et la tenue sont documentés dans `PROMPTS_IMAGES_Concentre_sur_le_chemin.md`. Les trois originaux autorisés utilisés sont `Samu/Snapchat-1835992965.jpg`, `Samu/Snapchat-1275781156.jpg` et `Samu/Snapchat-959878741.jpg`. Lunettes rectangulaires conservées. La ressemblance, les lunettes et la maquette de l’ancre ont été approuvées. Le même bloc héros figure dans les autres prompts ; la série complète est désormais approuvée par l’artiste.

| Scène | Mise en scène, même studio et même pose | Usage proposé |
|---|---|---|
| s01 — Tête lourde | Plan moyen assis, les deux mains sur la tête, cigarette entre les doigts ; lueur ambre faible dans la fumée, visage lisible au-dessus des paroles. **Ancre portrait.** | Intro, début, cover possible |
| s02 — Dans le bruit | Trois-quarts plus large, console vieillie et enceinte en profondeur, ombres bleu-noir, même tenue et pose. | Couplets |
| s03 — Tenir le cap | Plan moyen frontal, regard déterminé, contre-jour ambre plus intense, microphone latéral, centre calme. | Refrains / hook |
| s04 — Patience | Trois-quarts intime mais tête et mains entièrement cadrées, lumière ambre adoucie, fumée plus légère, même pose. | Pré-refrains / pont |
| s05 — Encore debout | Plan large du studio silencieux, même héros, même pose, éclairage en décroissance et centre peu chargé. | Outro / endcard |

Cette répartition est utilisée dans le montage des cinq scènes approuvées. Les prompts interdisent le lettrage du décor ; titre, paroles, badge et drapeau sont composés séparément.

## Portes de validation et budget

1. Analyse audio et paroles : effectuée structurellement ; écoute vocale encore nécessaire.
2. Questionnaire groupé : photos autorisées, typographie, signature/drapeau, options restantes. Les formats, la pose et le budget ne sont pas redemandés.
3. Une ancre portrait `s01` + maquette du véritable vers long / badge, à faire valider. Elle compte comme l'une des cinq images portrait si acceptée.
4. Après validation, produire au plus les **neuf fonds restants**, prompts complets écrits avant lancement ; 10 générations maximum par tour. Une correction remplace le slot refusé, elle n'ajoute pas une sixième scène.
5. Planche contact → validation → contrôle trois passages de synchronisation → rendu portrait → contrôles → paysage → master et covers.
6. Commit/push de chaque étape sur la branche de session uniquement. Pas de reset destructif. Les commandes Termux finales n'utiliseront qu'un hash contenant des fichiers réellement poussés et vérifiés.

## État / prochaine action

- Titre, formats et budget : confirmés.
- Photos de référence : **dossier Samu confirmé et autorisé** ; trois originaux utilisés pour l’ancre.
- Ancre s01 portrait : **approuvée**. **5 portraits + 5 paysages exportés**, contrôlés et approuvés après la planche v2 (« Oui je valide !! »).
- Typographie grasse, taille, ressemblance et lunettes : **approuvées sur la maquette**. Badge/drapeau validés. Extrait d’ouverture demandé ; la validation vocale complète reste distincte.
- Horaires : sources conservées, aucun faux statut « alignement vocal validé ».

## Maquette livrée pour validation (pas le clip final)

- Vidéo : `livrables/Concentre_sur_le_chemin_maquette_9x16_v1.mp4` (1080×1920, 14,5 s, vrai audio source).
- Image fixe : `livrables/Concentre_sur_le_chemin_ancre_9x16_v1.jpg` ; version PNG sans perte également disponible.
- Prompt complet : `PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md`.
- Contrôles et limites : `VALIDATION_ANCRE.md`.
- **L’ancre et les dix fonds sont désormais approuvés. La maquette est conservée comme étape historique, pas comme livraison du clip entier.** Le calage mot à mot reste provisoire, pas un alignement vocal validé.

## Salve complète — étape du 2026-09-29

- Planche courante : `livrables/Concentre_sur_le_chemin_planche_10_fonds_v2.jpg`. La v1 historique signalait deux cadrages incomplets et n’est plus la version à valider.
- Pack courant : `livrables/Concentre_sur_le_chemin_10_images_v2.zip` ; exactement cinq portraits 1080×1920 et cinq paysages 1920×1080.
- Les cinq portraits récupérés de la sauvegarde sont conservés ; les cinq paysages sont recomposés proprement, sans ajouter de scène. Originaux refusés disponibles dans le commit `67525732617ae9b6acfb23243b43c8f3f999004c`.
- Éléments parasites du décor nettoyés localement, mains/visages/tenues intacts en post. Le badge n’est gravé dans aucun fond pour permettre son animation par vers.
- Bandeau vectoriel Bénin : 54 px portrait, 30 px paysage ; pixels PNG exacts et contrôle JPEG.
- Scripts et 31 tests : voir `VALIDATION_FONDS.md`.
- État historique de la salve du 29 septembre : aucun clip complet n’était alors annoncé. Voir l’état actuel en tête de ce brief.

## Exports complets — 2026-09-30

- Portrait : `livrables/Concentre_sur_le_chemin_9x16_v1.mp4` ; 1080×1920, 30 fps, 30 147 295 octets.
- YouTube : `livrables/Concentre_sur_le_chemin_16x9_YT_v1.mp4` ; 1920×1080, 30 fps, 29 379 843 octets.
- Deux clips de 225,066667 s / 6 752 frames ; ouverture 6,90 s + chanson 213,160 s + fin 5 s.
- Master : `livrables/Concentre_sur_le_chemin_master_320k.mp3` ; MP3 320 kb/s, 48 kHz stéréo, chanson seule. Mesuré −14,02 LUFS / −1,64 dBTP, ID3v2.4 avec APIC/USLT.
- Pochettes : carré 1080×1080, portrait 1080×1920, paysage 1920×1080, texte en post.
- L’index du pack et les repères d’écoute : `livrables/LIVRAISON_Concentre_sur_le_chemin.md`. Les commandes Termux sont écrites après publication et contrôle des vrais téléchargements au hash immuable.
- Contrôles : `VALIDATION_CLIPS.md`, `qa_portrait.json`, `qa_landscape.json`, `audio_master_report.json`, `covers_report.json`.
- **Aucune dérive de montage mesurée sur trois passages ; ce n’est pas une validation vocale du mot-à-mot.** La validation des dix fonds n’est pas une validation finale des clips.
