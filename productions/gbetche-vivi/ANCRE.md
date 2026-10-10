# Gbètché vivi — Ancre, règles portrait et plan des 30 fonds

Production ouverte le 2026-10-10 · cadre : `PROMPT_UNIVERSEL_v5.7` (fusion v5.5 + v5.6).
État : **ancre validée par l'artiste** (choix 2 sur 2) · **salve 1 générée (S01→S10)** · **salve 2 et 3 en attente** (quota de 10 générations/tour atteint).

---

## 1 — Ancrage proposé et retenu : « MIDI POSITIF »

Une seule idée visuelle porte tout le clip : **la rue au petit matin qui devient pleine lumière.**
Le morceau dit « ma vie me plaît, je suis béni, je suis en paix » sans rien nier de la rue :
l'image ne doit donc être ni miséreuse ni festive à outrance — **digne, chaude, debout.**

| Élément | Décision d'ancre |
|---|---|
| Univers | Quartier populaire ouest-africain (Cotonou / Porto-Novo) : ruelle en terre, murs ocres et vert d'eau, manguier, marché qui ouvre, lagon en fin de parcours |
| Heure | Lever du soleil (5 h 30 → 8 h) puis lumière de matinée haute : contre-jour doux, poussières visibles |
| Palette | Or / ocre / terre cuite + **teal-indigo** du wax ; un seul accent rouge (bissap, fleurs) |
| Texture | Photo argentique 35 mm, grain fin, contraste doux, pas d'HDR, pas d'effet vidéo |
| Énergie | Dignité tranquille : tête haute, épaules relâchées, sourires vrais, geste d'ouverture — jamais de pose agressive, jamais d'arme, jamais d'argent étalé |
| Symboles porteurs | chaîne rouillée **jetée au sol** (« je marche sans chaîne »), plant qu'on arrose (« je construis les miens »), mains qui se serrent (Nonvi), pain partagé, toast de bissap, pirogues au lagon |
| Interdits | aucune nudité ni cadrage sur la poitrine/fesses, aucun membre coupé, aucun visage absent, aucun texte/lettre/logo/drapeau/filigrane, aucune bande noire |

**Personnages (bloc héros, recopié mot pour mot dans les 30 prompts — ne pas paraphraser) :**

> Lui : jeune homme béninois, teint brun profond, visage ovale, barbe courte taillée, cheveux très courts, chemise en coton blanc cassé fermée jusqu'au col, manches longues retroussées aux poignets, pantalon en lin sable, collier de petites perles noires, montre bronze au poignet gauche.
> Elle : jeune femme béninoise, teint brun cuivré, visage rond, cheveux tressés en vanilles basses ramenées sur l'épaule gauche, robe longue en wax indigo à manches trois-quarts descendant jusqu'aux mollets, boucles d'oreilles dorées rondes, foulard ocre noué à la taille.

Fichier ancre de référence : `personnages/ancre-01.png` — **1080×1920 natif, bande noire de 109 px retirée** (voir §7). **Toute génération repart de ce fichier via `images=`.**

---

## 2 — Règle « portrait non coupé » (demande explicite de l'artiste)

Le problème venu des précédents clips : les images paysage étaient recadrées en haut et en bas pour remplir le 9:16. Décision appliquée ici :

1. **Les images sont générées nativement en 9:16 vertical** — pas de détour, pas de reprise paysage.
2. Chaque prompt impose : tête entièrement visible avec marge d'air au-dessus, corps complet jusqu'aux mi-mollets/genoux, **mains et pieds non coupés**, rien d'important dans les 8 % supérieurs ni les 18 % inférieurs du cadre (zones réservées au badge et aux CTA, cf. §5 v5.7).
3. Au rendu, le filtre est **`scale=1080:1920:flags=lanczos` seul** — **jamais** `force_original_aspect_ratio=increase` + `crop`, jamais de pad. Les fichiers sortent en 768×1376 (ratio 0,5581 contre 0,5625) : l'étirement vertical de **0,8 %** est retenu plutôt qu'une coupe de 8 px. Non perceptible, et aucune information ne disparaît.
4. Contrôle de sortie obligatoire : aucune frame où un crâne, un menton ou des mains touchent les bords haut/bas.

## 3 — Plan des 30 fonds (segments calés sur les débuts de vers)

Durée **décodée mesurée : 194,83 s** (start offset 0,023 s) — le `[length:03:14]` du fichier texte est un arrondi. Source : 48 kHz stéréo, **−14,8 LUFS intégrés, crête −0,0 dBFS** → loudnorm 2 passes (−14 LUFS / −1,5 dBTP) obligatoire avant publication.
Découpe : 30 segments, moyenne **6,30 s**, aucune coupe d'image en milieu de vers, minimum 2,57 s.

| # | t0 → t1 | s | Scène (toutes en 9:16 natif, non recadrées) | État |
|---|---|---|---|---|
| S01 | 5,87 → 11,94 | 6,07 | Réveil : le couple avance dans la ruelle, lumière rasante | généré |
| S02 | 11,94 → 17,49 | 5,55 | Gratitude : lui, mains ouvertes sur la poitrine | généré |
| S03 | 17,49 → 24,19 | 6,70 | Paix : elle, menton haut, foulard au vent | généré |
| S04 | 24,19 → 27,36 | 3,17 | Fraternité : fronts presque touchés, yeux fermés | généré |
| S05 | 27,36 → 41,60 | 14,24 | Libre : chaîne rouillée jetée au sol, marche (fenêtre clochettes) | généré |
| S06 | 41,60 → 45,45 | 3,85 | Le quartier : marché qui ouvre, salut main sur le cœur | généré |
| S07 | 45,45 → 52,32 | 6,87 | Rire partagé : plan rapproché à deux | généré |
| S08 | 52,32 → 55,97 | 3,65 | Célébration : bras levés, enfants en second plan | généré |
| S09 | 55,97 → 59,36 | 3,39 | Enfant de la rue : ruelle mouillée, reflets dorés | généré |
| S10 | 59,36 → 64,70 | 5,34 | Bandit positif : index à la tempe, rire franc | généré |
| S11 | 64,70 → 70,93 | 6,23 | Construire : elle arrose un plant contre un mur de briques | **à générer** |
| S12 | 70,93 → 75,00 | 4,07 | Sans validation : menton haut, lumière de fin de matinée | **à générer** |
| S13 | 75,00 → 81,82 | 6,82 | Le prix du pain : pièces dans la paume devant la boutique | **à générer** |
| S14 | 81,82 → 88,26 | 6,44 | Nonvi : deux mains qui se serrent au centre du cadre | **à générer** |
| S15 | 88,26 → 91,50 | 3,24 | Partager le pain : assis sur le muret, pain cassé | **à générer** |
| S16 | 91,50 → 106,57 | 15,07 | On avance ensemble : trois amis bras dessus bras dessous (fenêtre clochettes) | **à générer** |
| S17 | 106,57 → 112,45 | 5,88 | Rien ne nous sépare : toast de bissap sous l'auvent | **à générer** |
| S18 | 112,45 → 118,07 | 5,62 | Cri de ralliement : poings levés dans la rue, sans drapeau | **à générer** |
| S19 | 118,07 → 124,51 | 6,44 | Wanyiyi : danse douce dans la cour | **à générer** |
| S20 | 124,51 → 128,58 | 4,07 | Le lagon : pirogues, lever de soleil sur l'eau | **à générer** |
| S21 | 128,58 → 135,62 | 7,04 | Tête haute : marche de face dans la lumière du matin | à planifier |
| S22 | 135,62 → 139,12 | 3,50 | Multipliés : la rue se remplit derrière le couple | à planifier |
| S23 | 139,12 → 146,00 | 6,88 | Renforcés : épaules serrées, regards fermes | à planifier |
| S24 | 146,00 → 149,52 | 3,52 | Dagbé : il répare une moto, manches retroussées | à planifier |
| S25 | 149,52 → 156,01 | 6,49 | Le but : le groupe avance en ligne dans la ruelle | à planifier |
| S26 | 156,01 → 162,75 | 6,74 | Libération : contre-jour, têtes hautes, tissu au vent | à planifier |
| S27 | 162,75 → 170,09 | 7,34 | Béni, en paix : sous l'arbre, mains jointes | à planifier |
| S28 | 170,09 → 181,17 | 11,08 | Beat wê… : plan large, quartier vu de dessus, couple minuscule (fenêtre clochettes) | à planifier |
| S29 | 181,17 → 183,74 | 2,57 | Trois mots : elle, lui, l'ami — front de trois visages sereins | à planifier |
| S30 | 183,74 → 194,83 | 11,09 | Bandit Positif : le couple face caméra, gestes de paix, lumière d'or → fond de la carte finale | à planifier |

> Points courts (S04, S06, S08, S09, S15, S20, S22, S24, S29 = < 4 s) : le rendu garde l'image jusqu'à la coupe suivante, mais si l'artiste trouve le montage nerveux, on fusionne avec le voisin sans régénérer.

**Fenêtres sans texte ≥ 5 s (clochettes, à re-vérifier au décodage) :** 30,24 → 41,60 · 94,38 → 106,57 · 173,11 → 181,17. La fenêtre 186,27 → 194,83 est tenue par **la carte finale**, pas par les clochettes.

## 4 — Carte d'accueil, carte finale, code

- Accueil ~5 s sur S01 : « Regarde jusqu'à la fin » puis « pour découvrir comment proposer un son ou des lyrics à réaliser pour toi ! » (≈ 4 mots/s, fondu 0,35 s, aucune coupe de vers).
- Finale 5 s après la chanson, sur S30 : « Merci d'avoir regardé » · « Tu veux un son ou des lyrics à réaliser pour toi ? » · « Commente le code » · **code**.
- **Code proposé : `0314`** — la durée exacte du morceau (03:14), donc inratable et propre à cette chanson. Alternatives : `1414` (le 14 de 3:14) ou `3030` (trois mots-clés — Wanyiyi, Nonvi, Dagbé — une seule victoire). **En attente du choix de l'artiste.**
- Badge « Dsky » seul, **sans drapeau**, y = 160, opacité ≤ 75 %, fondu 0,4 s par vers.

## 5 — À livrer (rappel v5.7)

9:16 1080×1920 · Titre · Captions (légende courte + code) · 10 à 13 hashtags · déclaration IA (visuels générés par IA) · master 48 kHz MP3 320 kb/s loudnorm −14 LUFS / −1,5 dBTP avec ID3 (APIC + USLT propre) · commandes Termux une ligne par fichier, `;` en séparateur, hash du commit **après** push.

## 7 — Contrôles de la salve 1 (mesurés, pas déclarés)

Méthode : lecture PNG directe, bande noire = lignes dont la luminance max < 10 ; densité de contours dans les bandes hautes (8 %) et basses (18 %).

| Fichier | Ratio | Taille | Bandes noires h/b | Remarque |
|---|---|---|---|---|
| `ancre-01.png` | 0,5625 | **1080×1920** | 0 / 0 | **109 px de noir en haut (8,5 %) détectés → réparés** : bande supprimée, puis 61 px rognés sur chaque côté (densité de contours des lisères 4,4 contre 6,9 au centre → du fond, aucun personnage touché). Original conservé : `ancre-01-brut.png`. |
| `scene-01` → `scene-10` | 0,5581 | 768×1376 | 0 / 0 | Aucune bande noire, aucun recadrage nécessaire. Écart de 0,8 % avec le 9:16 absorbé par un étirement vertical (`scale` pur, jamais de `crop`). |

- Passage vérifié dans ce sandbox : `scale=1080:1920:flags=lanczos` sur scene-01 / 05 / 10 → sortie 1080×1920 exacte, **rien de rogné en haut ni en bas** (le contrôle que l'artiste demandait).
- Plans où les jambes sortent du cadre **par le cadrage interne** (S02, S07, S09, S10 : plan taille ou genoux) : conforme à v5.7 (plan moyen accepté), mais si l'artiste veut du corps entier partout, on régénère ces quatre slots en plan large.
- Consistance des personnages sur les 10 scènes : même homme (chemise blanc cassé, lin sable, perles noires), même femme (wax indigo, foulard ocre, vanilles basses) — aucune dérive de visage ou de tenue relevée sur la planche.

## 6 — Prochain tour

1. **Salve 2** : S11 → S20 (prompts déjà écrits et lancés au prochain tour, quota 10/tour).
2. **Salve 3** : S21 → S30.
3. Planche contact des 30 + validation, puis montage 9:16 (script `render_lyric_video.py` à porter dans `productions/gbetche-vivi/`), contrôles `blackdetect` / `freezedetect`, master et covers.
