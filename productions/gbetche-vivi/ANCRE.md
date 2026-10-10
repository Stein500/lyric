# Gbètché vivi — Ancre, règles portrait et plan des 30 fonds

Production ouverte le 2026-10-10 · cadre : `PROMPT_UNIVERSEL_v5.7` (fusion v5.5 + v5.6).
État : **PIVOT DEMANDÉ PAR L'ARTISTE le 2026-10-10** — la salve « couple photo » (S01→S10) est **mise de côté** pour ce morceau.

## 0 — Décision artiste (tour 2)

Demande actuelle : **une seule personne à l'image**, un **homme qui ressemble à l'artiste**, en **personnage animé (rendu 3D) dans un studio**. Autorisation d'usage du visage : **donnée explicitement par l'intéressé lui-même** (« prendre mes photos dans Sam et génère ») — conformité §2 v5.7 respectée.

- Références faciales extraites de `Sam/Snapchat-174169237.mp4` (11,77 s) et `Sam/Snapchat-2050730153.mp4` (9,15 s), 1280×720, via `ffmpeg` : 5 images frontales nettes.
- Ces fichiers sont **personnels et volontairement hors Git** (`_refs/.gitignore`).
- Traité visuel retenu pour les 30 fonds : **un seul héros, rendu 3D « long-métrage d'animation », en studio**, 9:16 natif, corps entier jamais rogné (§2).
- Les 30 prompts de la table §3 restent la **grille de montage** (timings, durée des segments, fenêtres clochettes) : seules les scènes changent de contenu (rue → studio, couple → homme seul).
- Ancre « MIDI POSITIF » (couple photographique) conservée comme archive : `personnages/scene-01…10`, `ancre-01.png` / `ancre-01-brut.png`. À réutiliser uniquement sur un autre morceau, jamais reportée ici.

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

| # | t0 → t1 | s | Scène studio — homme seul, personnage animé, 9:16 natif jamais rogné en haut/bas | État |
|---|---|---|---|---|
| A01 | 5,87 → 11,94 | 6,07 | Présentation : debout au micro, main sur la poitrine | généré |
| A02 | 11,94 → 17,49 | 5,55 | Gratitude : assis sur le tabouret, mains jointes | généré |
| A03 | 17,49 → 24,19 | 6,70 | Bénédiction : bras ouverts, paumes vers le haut, halo doré | généré |
| A04 | 24,19 → 27,36 | 3,17 | Paix : mains jointes devant la bouche, yeux fermés | généré |
| A05 | 27,36 → 41,60 | 14,24 | Marche sans chaîne : couloir de studio, chaîne au sol (fenêtre clochettes) | généré |
| A06 | 41,60 → 45,45 | 3,85 | La cabine : casque devant la vitre acoustique — second personnage en fond à retirer | régénérer |
| A07 | 45,45 → 52,32 | 6,87 | Rire : tête renversée, micro détendu | généré |
| A08 | 52,32 → 55,97 | 3,65 | Bandit positif : index à la tempe — liseré clair + tête trop haute | régénérer |
| A09 | 55,97 → 59,36 | 3,39 | Plan large assis au sol béton, spot unique | **à générer** |
| A10 | 59,36 → 64,70 | 5,34 | Il ajuste ses lunettes, sourire tranquille, fond teal | **à générer** |
| A11 | 64,70 → 70,93 | 6,23 | Main posée sur un caisson de monitoring, menton haut | **à générer** |
| A12 | 70,93 → 75,00 | 4,07 | Plan serré visage, lumière dorée rasante | **à générer** |
| A13 | 75,00 → 81,82 | 6,82 | Il écrit dans un carnet au banc de mixage | **à générer** |
| A14 | 81,82 → 88,26 | 6,44 | Poing serré vers la caméra — Nonvi, parole tenue | **à générer** |
| A15 | 88,26 → 91,50 | 3,24 | Partage un verre d'eau, studio vide autour de lui | **à générer** |
| A16 | 91,50 → 106,57 | 15,07 | La cabine s'ouvre, équipe qui lève les bras en silhouette (fenêtre clochettes) | **à générer** |
| A17 | 106,57 → 112,45 | 5,88 | Toast au studio : verre levé, un seul personnage visible | **à générer** |
| A18 | 112,45 → 118,07 | 5,62 | Cri de ralliement : poings levés dans la brume | **à générer** |
| A19 | 118,07 → 124,51 | 6,44 | Danse douce sur place, épaules, sourire | **à générer** |
| A20 | 124,51 → 128,58 | 4,07 | Contre-jour total, silhouette dorée, visage lisible | **à générer** |
| A21 | 128,58 → 135,62 | 7,04 | Marche latérale devant le cyclorama, plan large | à planifier |
| A22 | 135,62 → 139,12 | 3,50 | Derrière la baie vitrée, deux mains ouvertes | à planifier |
| A23 | 139,12 → 146,00 | 6,88 | Épaule contre une silhouette floue, regard ferme | à planifier |
| A24 | 146,00 → 149,52 | 3,52 | Dagbé : il règle un casque, manches retroussées | à planifier |
| A25 | 149,52 → 156,01 | 6,49 | Avance en ligne, trois silhouettes lointaines dans le couloir | à planifier |
| A26 | 156,01 → 162,75 | 6,74 | Libération : fumée, néons, bras ouverts | à planifier |
| A27 | 162,75 → 170,09 | 7,34 | Béni, en paix : assis au bord du cyclorama, lumière d'aube | à planifier |
| A28 | 170,09 → 181,17 | 11,08 | Vue de dessus : minuscule au centre du studio vide (fenêtre clochettes) | à planifier |
| A29 | 181,17 → 183,74 | 2,57 | Trois visages de front, lui au centre, calme | à planifier |
| A30 | 183,74 → 194,83 | 11,09 | Face caméra, main sur le cœur, lumière d'or → fond de la carte finale | à planifier |

- Passage vérifié dans ce sandbox : `scale=1080:1920:flags=lanczos` sur scene-01 / 05 / 10 → sortie 1080×1920 exacte, **rien de rogné en haut ni en bas** (le contrôle que l'artiste demandait).
- Plans où les jambes sortent du cadre **par le cadrage interne** (S02, S07, S09, S10 : plan taille ou genoux) : conforme à v5.7 (plan moyen accepté), mais si l'artiste veut du corps entier partout, on régénère ces quatre slots en plan large.
- Consistance des personnages sur les 10 scènes : même homme (chemise blanc cassé, lin sable, perles noires), même femme (wax indigo, foulard ocre, vanilles basses) — aucune dérive de visage ou de tenue relevée sur la planche.

## 9 — Contrôles de la salve anim (script `qa_fonds.py`, mesures réelles)

| Fichier | Ratio | Bandes noires h/b | Air au-dessus du crâne (mesuré) | Verdict |
|---|---|---|---|---|
| `ancre-anim-01` | 0,5581 | 0 / 0 px | 11,0 % | OK (guide d'identité, hors montage) |
| `anim-01` | 0,5581 | 0 / 0 | 11,0 % | OK |
| `anim-02` | 0,5581 | 0 / 0 | 11,6 % | OK |
| `anim-03` | 0,5581 | 0 / 0 | 11,4 % | OK |
| `anim-04` | 0,5581 | 0 / 0 | 11,2 % | OK |
| `anim-05` | 0,5581 | 0 / 0 | 0,0 % → **faux positif** | crâne en réalité vers 38 % : le crible accroche les néons du plafond, pas la tête. OK |
| `anim-06` | 0,5581 | 0 / 0 | 10,8 % | **à régénérer** : un deuxième personnage (l'engineer) apparaît au fond alors que l'artiste veut un homme seul |
| `anim-07` | 0,5581 | 0 / 0 | 11,8 % | OK |
| `anim-08` | 0,5581 | 0 / 0 | **2,5 %** | **à régénérer** : tête dans la zone badge (y 0→144) + trait clair vertical à 4,3 % du bord (cadre parasite visible sur la planche) |

- **Zéro bande noire** et ratio 9:16 au dixième de pour cent sur les 9 fichiers : le rendu applique `scale=1080:1920:flags=lanczos` **sans `crop` ni `pad`** — testé sur `anim-05`, sortie 1080×1920 exacte, rien de perdu en haut ni en bas (la demande initiale de l'artiste).
- Le crible « liseré clair » automatique est **peu fiable sur ce décor** (fond de studio déjà lumineux : au seuil 140 tous les fichiers déclenchent, au seuil 150 + 45 % de couverture aucun ne déclenche). Il est donc **informatif seulement** ; la détection du trait de cadre sur A08 a été faite à la planche, et sera confirmée au montage par `cropdetect`.
- Zone basse (18 % = y ≥ 1574) : chaussures, chaîne au sol, tabouret y figurent — c'est voulu, cette zone est réservée à l'**absence de texte**, pas à l'absence de décor.
- Planche de validation : `PLANCHE-anim-all.jpg` (3×3, ancre + A01→A08).

## 6 — Prochain tour

1. **Ancre anim validée** (choix 2/2) → `personnages/ancre-anim-01.png`, 768×1376, guide unique des 30 fonds ; les photos personnelles ne sont plus renvoyées au générateur après l'ancre.
2. **A01 → A08 générés** et contrôlés (`qa_fonds.py`).
3. **Prochain tour** : régénérer A06 (homme seul) et A08 (tête plus basse), puis produire A09 → A20 — quota 10 générations/tour.
4. **Ensuite** : A21 → A30, planche contact complète, validation artiste, montage 9:16 (`scale` pur, jamais de `crop`), contrôles `blackdetect` / `freezedetect`, master −14 LUFS / −1,5 dBTP, covers, livrables (titre, captions, hashtags, déclaration IA, code **0314** en attente de validation).
