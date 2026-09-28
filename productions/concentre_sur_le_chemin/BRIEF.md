# Concentré sur le chemin — brief de production

Date : 2026-09-28. Branche de session : `arena/01a0e931-lyric`.

**Étape actuelle : questionnaire validé, une ancre portrait générée, maquette en préparation ; ancre non encore approuvée par l’artiste.**
Les références originales du dossier `Samu` ont été explicitement autorisées. Seul le slot portrait s01 a été généré avec trois de ces originaux. Aucun clip/master final n’est livré à ce stade.

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
- Cold-open proposé : deux premières lignes du refrain le plus énergétique, intervalle source 01:53.28 → 02:00.18, soit **6,90 s**. Un hook de 6 s exactement pourrait couper le second vers ; vérifier à l'écoute et faire approuver l'extrait. Variante sans cold-open possible.
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

Le bloc héros et la tenue sont documentés dans `PROMPTS_IMAGES_Concentre_sur_le_chemin.md`. Les trois originaux autorisés utilisés sont `Samu/Snapchat-1835992965.jpg`, `Samu/Snapchat-1275781156.jpg` et `Samu/Snapchat-959878741.jpg`. Lunettes rectangulaires conservées. La ressemblance et les traits de l’ancre restent soumis à l’approbation de l’artiste avant de recopier le bloc dans les neuf autres prompts complets.

| Scène | Mise en scène, même studio et même pose | Usage proposé |
|---|---|---|
| s01 — Tête lourde | Plan moyen assis, les deux mains sur la tête, cigarette entre les doigts ; lueur ambre faible dans la fumée, visage lisible au-dessus des paroles. **Ancre portrait.** | Intro, début, cover possible |
| s02 — Dans le bruit | Trois-quarts plus large, console vieillie et enceinte en profondeur, ombres bleu-noir, même tenue et pose. | Couplets |
| s03 — Tenir le cap | Plan moyen frontal, regard déterminé, contre-jour ambre plus intense, microphone latéral, centre calme. | Refrains / hook |
| s04 — Patience | Trois-quarts intime mais tête et mains entièrement cadrées, lumière ambre adoucie, fumée plus légère, même pose. | Pré-refrains / pont |
| s05 — Encore debout | Plan large du studio silencieux, même héros, même pose, éclairage en décroissance et centre peu chargé. | Outro / endcard |

Cette répartition est une proposition, pas une salve validée. Tous les prompts devront interdire le lettrage du décor ; titre, paroles, badge et éventuel drapeau sont composés séparément.

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
- Ancre s01 portrait : **générée, à valider**. Autres fonds : **non générés**.
- Typographie grasse et badge/drapeau : **validés au questionnaire**. Extrait d’ouverture demandé ; coupe exacte et lisibilité à valider sur la maquette.
- Horaires : sources conservées, aucun faux statut « alignement vocal validé ».
