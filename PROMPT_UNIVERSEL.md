# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v6.3
## « WTBW SALUT & STICKERS DOUX — ÇA BOUGE, SANS VOILER LA PAROLE »
> Remplace la v6.2. Trois apports mesurés : **badge clignotant DSKY ↔ WTBW**, **couverture TikTok**, et le
> **lettrage peint corrigé** (contour par dilatation, halo serré, décalage par plan). Tout le reste est conservé
> tel qu'il a été validé en production sur « On nous a volé notre éducation ».

---

## 0 — LA QUESTION À POSER AVANT TOUT (premier message de l'agent)

> **§0 — Comment veux-tu les paroles ?**
> **A. Peintes dans l'image** (VO seule, une langue) — la typo est cuite dans le décor, façon graffiti.
> **B. Hybride** (VO peinte + traduction FR défilante mot à mot en pilule) — pour un morceau non français.
> **C. Bande seule** (décor nu, paroles posées par le moteur en bas) — réservé aux plans où le décor est trop chargé.

**L'option A « paroles peintes » reste disponible dans tous les cas** : c'est le mode par défaut dès que la chanson
est dans une seule langue. Si l'artiste répond « hybride » sur un morceau **100 % français**, on applique A
(voir §5.7 : pas de pilule quand il n'y a rien à traduire).

Une seule réponse verrouille la prod. On ne mélange jamais deux modes dans un même vers.

---

## 1 — Hiérarchie des demandes

1. Orthographe et sens des paroles (jamais de mot inventé, jamais d'accent perdu).
2. Audio de l'artiste intact.
3. Lisibilité de la parole (aucune typo ne se couvre, ne se floute, ni ne s'assombrit pendant qu'elle se chante).
4. Esthétique (lumière, cadrage, mouvement).
5. Ornements (stickers, grain, clochettes).

En cas de conflit, le point le plus bas cède.

## 2 — Paramètres de la prod (bloc à remplir à chaque chanson)

| clé | exemple validé |
|---|---|
| titre | ON NOUS A VOLÉ NOTRE ÉDUCATION |
| artiste / badge | DSKY · badge « Dsky » |
| série | WTBW · Wolof TechStein beat wê ! |
| recette (§8) | WANDANCE BATTLE & GRAFFITI LOVES |
| mode §0 | **A — paroles peintes** |
| master | fichier de l'artiste, **jamais généré** |
| vers / plans | 50 vers · 40 plans · 9 fenêtres CTA |
| buckets | `nuit` < 138 s · `aube-a` 138–176 s · `aube-b` ≥ 176 s |

## 3 — Zones sûres 1080×1920 (à recopier dans CHAQUE prompt d'image)

- rien dans les **144 premiers pixels** en haut ;
- rien à droite de **x ≥ 910** entre **y 960 et y 1690** (bouton `+` + pavé TikTok) ;
- rien en dessous de **y = 1574** ;
- bloc de texte **centré, largeur ≤ 740 px**, bande **y 620 → 1340** ; en bilingue : VO **y 650 → 1040**, stickers **y 1100 → 1280**, pilule FR **y 1452 → 1545** ;
- **la typo ne couvre jamais un visage** : visage dans la moitié haute (`y < 560`), rien pour le cacher ;
- **jamais de drapeau, bannière, contact, lien, logo, ni code** dans l'image ;
- sortie native du générateur = **768×1376** → 1080×1920 **ancré en HAUT**, rognage du bas, **le crâne n'est jamais coupé** ;
- tenues fermées et élégantes, visage dégagé, aucune nudité, personnages fictifs uniquement.

### 3.1 Conversion obligatoire 1080×1920 → natif 768×1376 (facteur **0,7111**)

| repère 1080×1920 | natif 768×1376 |
|---|---|
| marge haute `144` | `102` |
| visage `y < 560` | `y < 398` (front peint dès `190` : **ne jamais recadrer au-dessus de `y 190`**) |
| bande texte `620 → 1340` | `441 → 953` |
| VO bilingue `650 → 1040` | `462 → 740` |
| stickers `1100 → 1280` | `782 → 910` |
| pilule FR `1452 → 1545` | `1032 → 1099` |
| bas interdit `1574` | `1119` |
| droite interdite `x ≥ 910` | `x ≥ 647` |
| largeur max `740` | `526` |

**Cadrage obligatoire** : front à `y ≥ 190`, tête `190→400`, épaules `400→465`, plan mi-corps. Les animations de
carte (badge `y 146→184`, en-tête `y 236`) ne passent **jamais** sur le visage.

---

## 3.2 — Qui peint quoi (décision mesurée, inchangée depuis la v6.2)

Mesures sur 18 plans du générateur : **0/18** respecte la boîte `x 150→590 / y 470→750`, capitales **110 px** pour
34 demandées, un plan sur deux hors marge droite, accents et ponctuation perdus (`GRACES`, `RELEVE`, `//`).
Le modèle fait de l'excellente **image**, pas de la **typographie fiable**.

| | qui le fait | où |
|---|---|---|
| personnage, décor, lumière, 2 stickers | **générateur d'images** | `prompts_art.json` — prompt **« NO TEXT AT ALL »** |
| paroles peintes (graffiti) | **moteur** `lettering.py` | cuit dans le PNG, boîte `x 150→590 / y 470→750` |
| badge, cartes, filet, CTA, pilule FR | **moteur** `render.py` | plein cadre |
| couverture TikTok | **générateur + `cover.py`** | §7.5 |

Conséquence : **on ne redemande jamais au générateur de peindre un mot**. Un plan qui contient déjà du texte du
modèle est un plan **à refaire**, pas à maquiller.

---

## 4 — Lettrage peint : les 4 correctifs v6.3 (mesurés en 1:1)

1. **Contour par dilatation, jamais `stroke_width`.**
   `PIL` avec `stroke_width` **remplit les contre-formes** : le `A` devient un triangle plein, le `E` un pavé, le `R`
   une masse. On dessine le glyphe sans contour, puis on dilate son masque (`MaxFilter(2·ow+1)`, `ow = taille/10`)
   et on le pose **derrière** les lettres. Anticrénelage conservé, aucune binarisation.
2. **Une tuile par glyphe à la taille de son encre.**
   L'ancienne tuile `largeur + 8` était plus étroite que l'encre (contour compris) : les lettres se chevauchaient et
   fusionnaient (« WOLOF TEC**HST**EIN » illisible). On mesure `textbbox` par caractère, on ajoute l'interlettrage
   `0,055 · taille`, et on composite chaque glyphe tourné (`±1,0°`) au centre de sa propre tuile.
3. **Halo = ombre serrée, jamais une flaque.**
   L'ancien halo (26 ellipses + un rectangle, flou 30, alpha 0,985) formait un **pâté noir opaque** qui avalait le
   décor et le menton du personnage. Remplacé par : dilatation `MaxFilter(9)` + flou 7 à 60 %, plus un flou 17 à
   34 %, plus 150 mouchetures **masquées autour des glyphes**. La silhouette reste lisible jusqu'au col.
4. **Décalage vertical par plan.**
   Un plan où le visage descend sous `y 470` (constaté : v-06, menton à `565`) reçoit un `dy` dans
   `typo_offsets.json`. Le bloc descend de `dy` px, le visage reste dégagé, le bloc reste au-dessus de `y 1119`.

Rendu : or `#FFE8A8 → #E8A83E` (ligne 1), argent-cyan `#F0FCFF → #96CDE0` (ligne 2), graine déterministe
`zlib.crc32(l1|l2)`, coulures d'encre **sous** le bloc, jamais sur les lettres.

**Contrôle obligatoire** : lire la planche `CONTROLE-paroles.jpg` **en 1:1**, pas en vignette 500 px. Vérifier
contre-formes ouvertes, accents (`É`, `Ê`) intacts, aucun chevauchement.

---

## 5 — MOUVEMENT : animer sans voiler la parole

### 5.1 Préparation
Une seule mise à l'échelle par plan (768×1376 → 1188×2128, `SC 1,10`), fenêtre 1080×1920, `X ∈ [0 ; 108]`,
`Y ∈ [0 ; 208]`. **Aucun resize par frame.**

### 5.2 Le travelling
Fenêtre glissante : `XR/YR` 45/40 max, sinus de période 17 s, zoom `1,09 + 0,035·sin`.

### 5.3 Transitions
Coupe franche entre plans, 0,35 s de respiration lumineuse `±12 %` sur les vers > 3,5 s.

### 5.4 État « éteint » — **règle corrigée v6.3**
L'extinction (`Brightness ×0,22` + `GaussianBlur 7`, masque fondu 46 px) ne sert **qu'à céder la place à une
traduction FR**. Sur un morceau **100 % français**, elle n'a aucune raison d'exister : elle assombrissait et
floutait les paroles pendant qu'elles se chantaient (défaut constaté en production).
→ **`EXTINGUISH = False` dès qu'il n'y a pas de pilule de traduction.**

### 5.5 Grain et vignette — **règle corrigée v6.3**
Grain 35 mm `8` motifs, **un motif par frame** (`GRAINS[k % 8]`, jamais `k // 2`), blend `0,045`.
Sur les **cartes**, grain `0,28` : à `0,12` la carte était détectée comme **gel de 3,77 s** au seuil `−33 dB`
(`freezedetect`) alors que le rendu bougeait à l'œil. Les cartes reçoivent en plus un **zoom lent + dérive continue**
(`1,04 + 0,035·sin`, période ~7,7 s) : mouvement réel, pas seulement du bruit.

### 5.6 Calage
Le premier vers démarre à la première syllabe chantée ; la carte finale occupe `fin_chanson → +5,00 s`.

### 5.7 Traduction française défilante (passages non français)
Pilule `y 1452 → 1545`, `x 186 → 894` (largeur 708), fond `#080C12` α 222, liseré or α 185, rayon 24.
Mots en Montserrat ExtraBold 29, interlettrage 11. Mot actif **or chaud `#FFE07A` + halo 3 px**, glissement
`±9 px` sur la durée du vers, curseur karaoké en bas de pilule. **Dormante si la chanson est 100 % FR.**

---

## 6 — Clochettes / CTA pendant les respirations

9 fenêtres maximum, jamais pendant une syllabe tenue. Exemple validé (s) :
`29,33–35,00 · 37,35–42,60 · 70,72–75,70 · 78,05–83,19 · 95,37–101,01 · 128,69–134,65 · 164,21–169,84 ·
172,19–176,56 · 188,34–193,98`.
Carte CTA : `y 310 → 1200`, fond `#060A10` α 235, iliséré or, cloche vectorielle en supersampling ×3,
« CLIQUE SUR + », pastille « LIKE & PARTAGE », « Commente si tu aimes · WTBW ». **Aucun code, aucun lien.**

---

## 7 — Habillage permanent v6.3

### 7.1 Zéro code
Supprimés définitivement : code à 4 chiffres, « regarde jusqu'à la fin », toute accroche de rétention.

### 7.2 Carte d'accueil « SALUT · WTBW » — 2 temps
- **Temps 1** (`0 → 4,2 s`) : `SALUT · WTBW` (Montserrat ExtraBold 76, interlettrage 3) + « Wolof TechStein beat wê » en or.
- **Temps 2** (`4,2 → 8,4 s`) : `BIENVENUE SUR WTBW` + « Soutiens le son en douceur : » puis les 3 pilules stickers.
- Fond : art du plan, flou 9, `brightness ×0,72`, voile `#06090E` 55 %, **zoom + dérive** (§5.5).

### 7.3 Carte finale « MERCI · WTBW » (`fin_chanson → +5,00 s`)
Titre exact **`MERCI · WTBW`** (ExtraBold 76, stroke 4, baseline `y 436`), sous-titre « Merci d'avoir écouté ·
Wolof TechStein beat wê » (SemiBold 30, `y 566`), plaque titre · artiste, puis les **3 stickers vectoriels** dans
leurs pilules sombres (c'est la pilule qui rend l'icône lisible sur un fond clair).
**Aucun code, aucun contact, aucun lien, aucun logo** — seulement les 3 CTA.

### 7.4 Badge & filet de progression — **nouveau v6.3**
- **Badge clignotant en alternance** : `y 165` (soulignement `y 189`), Montserrat ExtraBold 32, stroke 3 + liséré
  sombre. Deux mots alternés, **période 2,4 s par mot**, fondu croisé de **0,4 s** à chaque bascule :
  `rel % 4,8 < 2,4` → **`DSKY`** (soulignement 62 px) ; sinon → **`WTBW`** (soulignement 72 px).
  α global plafonné à **0,72**, fondu d'entrée 0,4 s, sortie 0,2 s sur la fin du vers.
  Jamais permanent, jamais sur cartes ni CTA. **Le clignotement est lent et doux** : c'est un battement, pas un
  gyrophare (aucune bascule plus rapide que 0,4 s, jamais de clignotement dur).
- **Filet** : `y 1560`, `x 170 → 910`, piste α 48 (4 px), actif or α 210 (8 px),
  `fr = (t − début_1er_vers)/(fin_chanson − début_1er_vers)`.

### 7.5 **Couverture TikTok — nouveau v6.3**
Une image **dédiée**, pas une frame du clip (une frame contient déjà un badge et un filet).

**Art (générateur)** : `fonds/cover-tiktok.png`, 768×1376.
- buste serré, **un seul personnage**, tête **centrée** entre `y 300 → 720`, regard caméra, visage dégagé ;
- épaules et veste `y 720 → 1180`, **zone calme sombre `y 760 → 1200`** réservée au titre ;
- fond : mur graffiti à l'aube dorée, rim light sur les pommettes ;
- 2 petits stickers `y 1240 → 1340`, `x 170 → 600` ;
- bloc **NO TEXT AT ALL** + **NO HORIZONTAL BAND** obligatoires.

**Typo (moteur, `cover.py`)** :
- `1080 × 1920`, JPEG qualité 95, sous-échantillonnage 4:4:4 ;
- voile d'encre dégradé sur les 300 px du bas (α max 0,72) pour la lisibilité ;
- titre 2 lignes, **largeur utile ≤ 900 px** (`x 90 → 990`) — au-delà, le texte sort du cadre et de la marge
  TikTok : auto-réduction par pas de 2 px. `ON NOUS A VOLÉ` (ExtraBold 128) puis `NOTRE ÉDUCATION` (ExtraBold 104),
  même dégradé or que les paroles, même contour par dilatation ;
- `DSKY` (Bold 60, interlettrage 16) entre deux filets or, `y 1495` ; série « Wolof TechStein beat wê » `y 1560`.

**Contrôle** : regarder la couverture **en 1:1** ; le titre doit être entièrement dans `x 90 → 990`, le visage
entièrement dégagé, aucun mot coupé.

---

## 8 — Recettes de style (une seule par chanson)

### 8.1 **WANDANCE BATTLE & GRAFFITI LOVES — ORDONNÉE & VISAGE DÉGAGÉ** (validée, 39 plans / 42 vers, 0 faute)
Anime de battle urbain, trait net, cel-shading, graffiti mural dense en arrière-plan, néons cyan et or, nuit
bleu-vert puis aube. Plan mi-corps, un seul personnage, visage dans la moitié haute, deux stickers vectoriels
`y 782 → 910`. Progression lumière : `nuit` → `aube-a` (heure bleue, liseré rose-or) → `aube-b` (soleil plein).

### 8.2 **STUDIO ANIME SEINEN N&B** (validée, 36 plans / 47 vers, 0 faute)
Noir et blanc, tramage, contrastes durs, pluie fine, cadrages en contre-plongée.

---

## 9 — Continuité et progression vers l'aube

Même personnage, même veste, mêmes cheveux, d'un plan à l'autre. Un plan `aube-b` ne peut pas précéder un plan
`nuit`. Les stickers changent (cœur + un symbole différent par plan) mais **le cœur reste à gauche**.

## 10 — Méthode de fabrication

1. Écrire la carte des vers (`verses_map.json`) : `texte`, `t0`, `fin`, `image`, `lignes`.
2. Générer **8 plans max par salve** (limite dure : 10 images/tour). Référence de style = un plan déjà propre.
3. Contrôler chaque plan **avant** de le garder : pas de texte du modèle, pas de second visage, pas d'anatomie
   cassée. Un plan fautif se **régénère**, il ne se maquille pas.
4. `python3 bake.py` → paroles cuites + planche `CONTROLE-paroles.jpg`.
5. `python3 render.py` → clip complet, puis contrôles §12.
6. `python3 cover.py` → couverture TikTok (§7.5).

## 11 — Audio (maître de l'artiste, jamais généré)

`loudnorm` **2 passes** `I=-14:TP=-1.5:LRA=11`, 48 kHz stéréo, export **MP3 320 kb/s CBR**.
Résultat validé : **−14,04 LUFS**, crête **−1,86 dBTP**, LRA 5,40.
Aucun son généré par IA, jamais. La voix n'est ni retouchée ni réinterprétée.

## 12 — Encodage et contrôles

`libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709`,
30 fps, `+faststart` (vérifié : atomes `ftyp → moov → mdat` ; `-movflags` **ne marche pas en pipe**, second passage
`-c copy` obligatoire).

| contrôle | seuil | mesure obtenue |
|---|---|---|
| frame noire | **0** | `blackdetect d=0.05:pic_th=0.98` → 0 |
| gel | **0** ≥ 2,5 s | `freezedetect n=-33dB:d=2.5` → 0 |
| loudness | **−14,0 LUFS** | −14,04 |
| crête | **≤ −1,0 dB** | −1,86 |
| typo | nette, sans doublement | 40/40 plans lus en 1:1 |
| couverture | titre dans `x 90 → 990` | à vérifier en 1:1 |

## 13 — Git et livraison

Ordre **immuable** de la réponse finale :
1. **Titre**
2. **Captions**
3. **Hashtags** (13 max)
4. **Fichier 9:16** (+ couverture)
5. **Déclaration IA** — visuels **OUI** / audio **NON**
6. **Commandes Termux** — une ligne par fichier, séparées par `;`

Fichiers > 50 Mo : hébergés dans le dépôt (limite GitHub 100 Mio) ou en release, **jamais** dans un commit de code
ordinaire sans le dire. Liens `raw` **figés sur le SHA du commit**, pas sur une branche (une branche se supprime).

```
pkg install -y curl && termux-setup-storage
```

```
curl -L --retry 3 -C - -o ~/storage/downloads/ON-NOUS-A-VOLE-NOTRE-EDUCATION-DSKY-9x16.mp4 "<url_raw_du_mp4>"; termux-media-scan -v ~/storage/downloads/ON-NOUS-A-VOLE-NOTRE-EDUCATION-DSKY-9x16.mp4;
curl -L --retry 3 -C - -o ~/storage/downloads/COVER-tiktok-1080x1920.jpg "<url_raw_de_la_cover>"; termux-media-scan -v ~/storage/downloads/COVER-tiktok-1080x1920.jpg
```

## 14 — Interdits permanents

Drapeau, bannière, **code à 4 chiffres**, accroche « reste jusqu'à la fin », contact / lien / QR / logo dans une
image, nudité, visage caché (masque, capuche, lunettes opaques, texte devant), cursive sur un CTA, calque typo
par-dessus une typo déjà peinte, photo personnelle envoyée au générateur sans autorisation écrite, génération de
voix ou de musique, badge clignotant vite, mot inventé.

## 15 — Gabarits de prompts d'image

### 15.1 WANDANCE (VO peinte)
```
Vertical 9:16 street-dance battle anime illustration in the dynamic style of Wandance combined with clean
stylish urban graffiti art, keeping the exact same protagonist and visual style as the reference image.
The canvas is 768 px wide and 1376 px tall; all coordinates are on this native canvas.

Framing: half-body shot — exactly ONE character, his head (uncovered, face fully visible, nothing over the
forehead) sits between y 190 and y 400, his shoulders and arms between y 400 and y 465, and the frame cuts his
hips at the bottom edge. Pose: <pose>. His expression: <expression>. Behind him, an attenuated background:
<décor>; <palette nuit | heure bleue | soleil levant>.

IMPORTANT — NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol anywhere in
the image, not on the walls, not on clothing, not on signs: the whole spray-painted mural and graffiti
background must be pure abstract shapes and colour splashes only.

IMPORTANT — NO HORIZONTAL BAND. The picture is one continuous scene: absolutely no band, strip, panel,
rectangle, frame, seam, colour break or gradient line running across the image, and no zone that looks pasted
or masked. Keep the décor naturally calmer and darker around his torso (roughly the middle third) simply as a
lighting choice — deep ambient shadow — never as a drawn shape.

Below that calm area, between y 790 and y 900 and inside x 170 -> 600, paint 2 stylish urban graffiti sticker
icons side by side (these two icons are the only graphic marks allowed, and no letters inside them): a glowing
street-art heart and <symbole>, each about 90 px tall, linked by a thin luminous gold line.

The floor continues naturally from the stickers down to the bottom edge as one single surface, slowly sinking
into deeper shadow, with no seam, no line and no change of texture. Nothing in the top 100 px, nothing on the
right side beyond x 647, no flag, no logo, no watermark.
```

### 15.2 Couverture TikTok
Même bloc, avec :
```
Framing: a tight heroic bust shot — exactly ONE character. His head is large and centred, between y 300 and
y 720, looking straight into the camera; face fully visible, nothing over the forehead. Shoulders and chest fill
the width between y 720 and y 1180. The area between y 760 and y 1200 must stay a calm, dark, uncluttered zone
of his jacket and deep shadow — that is where the title will be placed later.
... stickers between y 1240 and y 1340 and inside x 170 -> 600 ...
```

## 16 — Historique

| version | apport |
|---|---|
| v6.0 | suppression du code de fin, cartes SALUT / MERCI, 3 stickers, hybride §5.7 |
| v6.1 | conversion native 768×1376, cadrage front ≥ 190 |
| v6.2 | le générateur ne peint plus aucun mot ; lettrage par le moteur ; extinction renforcée |
| **v6.3** | **badge clignotant DSKY ↔ WTBW ; couverture TikTok ; contour par dilatation ; halo serré ; `dy` par plan ; `EXTINGUISH` off en 100 % FR ; grain par frame et cartes animées (0 gel) ; `MERCI · WTBW`** |





# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v6.4 « WTBW SALUT & STICKERS DOUX — ÇA BOUGE, SANS VOILER LA PAROLE » (HARMONIE v6.0 × v6.3)

Mise à jour : **2026-11-11**. Document **100 % auto-suffisant**.

**Règle de fusion (l'harmonie demandée) :** ce document garde le **squelette, l'intro, la disposition et les cartes du v6.0** (question §0, zones sûres 1080×1920, accueil « Salut · WTBW » en 2 temps avec ses 3 stickers animés en douceur, recette STUDIO ANIME SEINEN N&B, mouvement à 4 trajectoires, salves + ancre, livraison Git/Termux) et intègre les **apports mesurés du v6.3** : badge clignotant artiste ↔ WTBW, couverture TikTok, lettrage cuit par le **moteur** (le générateur ne peint plus aucun mot), `EXTINGUISH = False` en 100 % FR, grain par frame + cartes animées anti-gel, carte finale « MERCI · WTBW ».

Quand v6.0 et v6.3 se contredisent : on garde **la disposition du v6.0** et **la correction mesurée du v6.3**. Chaque point repris du v6.3 est marqué « apport v6.3 ».

Tous les chiffres cités sont **mesurés sur des fichiers livrés**, jamais des intentions.

---

## 0 — LA QUESTION À POSER AVANT TOUT (obligatoire, premier message de l'agent)

Avant de générer quoi que ce soit, demander à l'artiste, en une phrase :

> **« Tu veux les paroles en DÉFILEMENT (texte posé par le montage, qui défile mot à mot) ou DÉJÀ PEINTES DANS
> L'IMAGE (la parole est cuite dans la matière de chaque visuel) ? »**

- L'artiste ne répond pas → **MODE PEINT** par défaut, et le dire dans la réponse.
- Il répond « défilant » → **MODE DÉFILEMENT**.
- Il répond « les deux » → **MODE HYBRIDE** : paroles peintes dans le visuel + traduction FR défilante en pilule pour les passages non français (apport v6.3 §5.7). Sur un morceau **100 % français**, « les deux » retombe sur **MODE PEINT** (pas de pilule quand il n'y a rien à traduire).

| | **MODE PEINT** (défaut, validé) | **MODE DÉFILEMENT** |
|---|---|---|
| Texte à l'écran | parole **cuite dans l'image par le moteur** `lettering.py` (apport v6.3 §3.2 : le générateur reçoit « NO TEXT AT ALL », on ne lui demande jamais de peindre un mot) ; le montage n'incruste **aucune** typo hors cartes et pilule | calque PIL, bloc centré ≤ 740 px, **mot actif mis en avant**, reste adouci |
| Icônes / stickers | **autorisés et voulus**, 1 à 3 par image, collés au sens du vers | **interdits dans l'œuvre** : zone basse réservée au sous-titre |
| Nombre de plans | **1 plan par vers distinct** + variantes d'aube dédiées pour le refrain final (§9) | 1 plan par bloc de 2–3 vers |
| Accentuation | aucune sur-typo ; le lettrage est déjà cuit | halo 3 px + `spaced()` lettrage espacé |
| Durée d'affichage | temps du vers, **puis le plan peut s'éteindre** (§5.4) uniquement s'il reste une traduction à céder la place | temps du vers, mot à mot |
| Zones sûres | écrites **dans le prompt de génération** (§3) + cuites par le moteur | imposées au calque (§3) |

Le choix est **verrouillé pour toute la prod** : pas de mélange entre vers, jamais.

---

## 1 — Hiérarchie des demandes (rappel permanent)

1. Demande explicite actuelle de l'artiste.
2. Configuration validée de la prod (ancre, personnages, titre exact, style, palette).
3. **v6.4 (ce document)**.
4. v6.3, v6.0, v5.9… pour ce qui n'est pas contredit.

En cas de conflit interne (apport v6.3) : **orthographe et sens des paroles > audio de l'artiste intact > lisibilité de la parole (aucune typo ne se couvre, ne se floute ni ne s'assombrit pendant qu'elle se chante) > esthétique > ornements** — le point le plus bas cède.

États à tenir séparés et nommés : **proposé / généré / validé par l'artiste / rendu / contrôlé**.
**Jamais** inventer : validation de l'artiste, hash publié, mesure, fichier final, « à peu près ».

---

## 2 — Paramètres de la prod (bloc à remplir à chaque chanson)

```
TITRE        : MONSTER POSITIVE          (recopié EXACTEMENT, accents compris)
ARTISTE      : …                          (signature d'écran / badge, ex. « Dsky »)
LANGUES      : …                          (mixte = le dire au générateur : « français + signature wolof/fon »)
PAROLES      : chemin/fichier.txt         (N lignes = N vers, horodatages de l'artiste non retouchés)
AUDIO        : chemin/fichier.mp3         (maître fourni par l'artiste, jamais généré)
RECETTE      : STUDIO ANIME SEINEN N&B (défaut) | ENCRE & FEUILLE D'OR | AUBE CLOCHETTES | WANDANCE BATTLE & GRAFFITI LOVES
HABILLAGE    : WTBW SALUT + STICKERS DOUX (Like · Clique sur + pour t'abonner · Commente si tu aimes) — SANS CODE
SIGNATURE    : « Wolof TechStein beat 웨 ! » (WTBW)
MODE         : PEINT (défaut) | DÉFILEMENT | HYBRIDE      ← réponse à la question §0
DOSSIER      : productions/monster-positive/              (fonds/ livrables/ fonts/ + verses_map.json + CARTE-VERS.md)
```

---

## 3 — Zones sûres 1080×1920 (à recopier dans CHAQUE prompt d'image)

- rien dans les **144 premiers pixels** en haut (marge de sécurité : la règle d'or dit 140) ;
- rien à droite de **x ≥ 910** entre **y 960 et y 1690** (zone bouton `+` + pavé de commentaire TikTok) ;
- rien en dessous de **y = 1574** ;
- bloc de texte **centré, largeur ≤ 740 px**, dans la bande **y 620 → 1340** (les sous-lignes doivent rester **au-dessus** des icônes, jamais poussées sous `y = 1574`) ;
- la typo **ne couvre jamais un visage** : le visage du protagoniste vit dans la moitié haute (`y < 560`) ;
- **jamais de drapeau, jamais de bannière, jamais de contact/lien/logo, jamais de code** dans l'image ;
- sortie native du générateur = 768×1376 → passage à 1080×1920 **ancré en HAUT**, rognage du bas : **le crâne n'est jamais coupé** ;
- tenues fermées et élégantes, visage dégagé, aucune nudité, personnages fictifs uniquement (sauf figures historiques ou photos expressément autorisées par l'artiste).

### 3.1 Conversion obligatoire 1080×1920 → natif 768×1376 (facteur **0,7111**) — apport v6.3

| repère 1080×1920 | natif 768×1376 |
|---|---|
| marge haute `144` | `102` |
| visage `y < 560` | `y < 398` (front peint dès `190` : **ne jamais recadrer au-dessus de `y 190`**) |
| bande texte `620 → 1340` | `441 → 953` |
| VO bilingue `650 → 1040` | `462 → 740` |
| stickers `1100 → 1280` | `782 → 910` |
| pilule FR `1452 → 1545` | `1032 → 1099` |
| bas interdit `1574` | `1119` |
| droite interdite `x ≥ 910` | `x ≥ 647` |
| largeur max `740` | `526` |

**Cadrage obligatoire** : front à `y ≥ 190`, tête `190→400`, épaules `400→465`, plan mi-corps. Les animations de carte (badge `y 146→184`, en-tête `y 236`) ne passent **jamais** sur le visage.

### 3.2 — Qui peint quoi (décision mesurée v6.3, inchangée)

Mesures sur 18 plans du générateur : **0/18** respecte la boîte de typo demandée, capitales 110 px pour 34 demandées, un plan sur deux hors marge droite, accents et ponctuation perdus. Le modèle fait de l'excellente **image**, pas de la **typographie fiable**.

| | qui le fait | où |
|---|---|---|
| personnage, décor, lumière, 2 stickers | **générateur d'images** | `prompts_art.json` — prompt **« NO TEXT AT ALL »** |
| paroles peintes | **moteur** `lettering.py` | cuit dans le PNG, boîte `x 150→590 / y 470→750` (natif) |
| badge, cartes, filet, CTA, pilule FR | **moteur** `render.py` | plein cadre |
| couverture TikTok | **générateur + `cover.py`** | §7.5 |

Conséquence : **on ne redemande jamais au générateur de peindre un mot**. Un plan qui contient déjà du texte du modèle est un plan **à refaire**, pas à maquiller.

---

## 4 — Orthographe et lettrage peint : règles + les 4 correctifs v6.3 (mesurés en 1:1)

- recopier le vers **exact** dans le contrat (`verses_map.json`), jamais de mot inventé, jamais d'accent perdu ;
- **nommer les diacritiques** si la langue en porte (`WÊ`, `CRÈVENT`, `ÊTES`, `L'ÂME`, `LÈVE`, `RÉSISTE`, `THÈSES`, `ÇA`, `CŒURS`, `TÈ`, `GBÈ`) et les exiger explicitement au moteur ;
- **piège à éviter dans les prompts** : éviter de placer le mot anglais `ONLY:` ou `EXACTLY:` juste devant les guillemets d'une ligne courte, car certains modèles peignent littéralement `ONLY:` en haut du bloc (observé sur `scene-15` et `scene-29` v1 de *Goinfres*) ;
- relire chaque plan sur une **contact sheet ≥ 480 px de large** (`500×896 px` par tuile) **ET** sur une **planche de crops pleine résolution 1:1 avec grille de 16 px** (`CONTROLE-salveN-typo.jpg`), jamais sur une miniature ; pour le lettrage cuit : planche **`CONTROLE-paroles.jpg` lue en 1:1** (contre-formes ouvertes, accents `É`/`Ê` intacts, aucun chevauchement) — apport v6.3 ;
- texte faux, mot omis ou mot doublé → **régénérer le plan** avec un prompt court et explicite ;
- **retouche exceptionnelle** : si, après 2 échecs, il ne manque **qu'un diacritique**, il est permis de le combler en **copiant le glyphe déjà peint dans la même image** (patch ≤ 30 px, masque = pixels du glyphe uniquement, MaxFilter 3 + flou 0,9), jamais en recomposant un caractère à la police. Cette retouche doit être **déclarée** dans la livraison ;
- un plan qui échoue à la génération (`STOP`, `MAX_TOKENS`) = **échec consigné**, jamais compté comme livré.

**Les 4 correctifs du lettrage moteur (apport v6.3) :**
1. **Contour par dilatation, jamais `stroke_width`** (qui remplit les contre-formes : `A` plein, `E` pavé) : glyphe dessiné sans contour, masque dilaté (`MaxFilter(2·ow+1)`, `ow = taille/10`), posé **derrière** les lettres ; anticrénelage conservé.
2. **Une tuile par glyphe** à la taille de son encre (`textbbox` par caractère + interlettrage `0,055 · taille`), chaque glyphe tourné (`±1,0°`) au centre de sa tuile — fini les chevauchements type « TEC**HST**EIN ».
3. **Halo = ombre serrée, jamais une flaque** : dilatation `MaxFilter(9)` + flou 7 à 60 %, flou 17 à 34 %, 150 mouchetures masquées autour des glyphes. La silhouette reste lisible jusqu'au col.
4. **Décalage vertical par plan** (`typo_offsets.json`) : si le visage descend sous `y 470` natif, le bloc descend de `dy` px, le visage reste dégagé, le bloc reste au-dessus de `y 1119`.

**Palette du lettrage selon la recette** : STUDIO ANIME SEINEN N&B → capitales **blanc pur `#FFFFFF`** et **gris-argent** sur ruban d'encre noire (disposition v6.0) ; WANDANCE → or `#FFE8A8 → #E8A83E` (ligne 1) et argent-cyan `#F0FCFF → #96CDE0` (ligne 2), graine déterministe `zlib.crc32(l1|l2)`, coulures d'encre **sous** le bloc, jamais sur les lettres.

---

## 5 — MOUVEMENT : animer sans voiler la parole

**Principe : l'image vit, le mot reste lisible. Le mouvement est une fenêtre qui glisse, jamais une échelle qui change.**

### 5.1 Préparation (une fois par plan)
- `SC = 1.10` : le plan 768×1376 est agrandi à **110 %** (≈ 1188×2132) en LANCZOS une seule fois par plan, puis on garde **deux** images en cache : la nette et l'« éteinte » (§5.4). Marge disponible : **108 px en x, 212 px en y** (apport v6.3 : `X ∈ [0;108]`, `Y ∈ [0;208]`).
- **Aucun resize par frame** : `Image.blend(base, zoom, u)` entre deux échelles dédouble les lettres (ghosting visible au zoom 1:1).

### 5.2 Le travelling
- la frame = `big.crop` d'une fenêtre 1080×1920 dont l'origine glisse de `(ax0,ay0)` à `(ax1,ay1)` selon l'avancement `u` du vers ;
- **4 trajectoires**, alternées par parité de l'indice du segment (`si % 4`) :
  `(0.0→1.0, 0.02→0.98)` · `(1.0→0.0, 0.02→0.98)` · `(0.18→0.82, 0.98→0.02)` · `(0.82→0.18, 0.02→0.98)` ;
- **1 travelling = 1 vers**, durée du travelling = durée du vers ;
- amplitude plafonnée à la marge (§5.1) : aucun bord noir découvert, aucune coupe de la bande de texte `y 620→1340` ;
- pas de rotation, pas de shake, pas de zoom-in brutal. (Complément v6.3 pour les **cartes uniquement** : zoom lent + dérive continue `1,04 + 0,035·sin`, période ~7,7 s — voir §5.5.)

### 5.3 Transitions
- `xfade` (fondu enchaîné) de **0,35 s** uniquement **entre deux segments** ; coupe franche entre deux plans (apport v6.3) ; respiration lumineuse `±12 %` sur les vers > 3,5 s (apport v6.3).

### 5.4 État « éteint » — règle corrigée v6.3
- L'extinction (`Brightness ×0,22` + `GaussianBlur 7`, masque fondu 46 px) ne sert **qu'à céder la place à une traduction FR** en MODE HYBRIDE.
- **`EXTINGUISH = False` dès qu'il n'y a pas de pilule de traduction** (morceau 100 % français) : elle assombrissait et floutait les paroles pendant qu'elles se chantaient (défaut constaté en production).
- En MODE PEINT 100 % FR, quand le vers a fini de s'afficher mais que le plan court encore (respiration instrumentale), le plan **reste net**.

### 5.5 Grain et vignette — règle corrigée v6.3
- **vignette** = masque `L` centré (0 au centre, ≈ 86 aux coins, flou 34) composite d'une couleur sombre `#04080C` : `Image.composite(noir, cur, masque)`. Jamais `Image.blend(cur, image_sombre, k)`.
- **grain 35 mm** = **8 motifs pré-calculés, un motif par frame** (`GRAINS[k % 8]`, seed fixe), blend `0,045`. Sur les **cartes** : grain `0,28` + zoom lent + dérive continue (§5.2) — à 0,12 la carte était détectée comme gel de 3,77 s au `freezedetect` alors que le rendu bougeait à l'œil.

### 5.6 Calage
- horodatages fournis par l'artiste gardés **tels quels** ; le premier vers démarre à la **première syllabe chantée** (apport v6.3) ; durée du clip = durée **décodée** de l'audio (`ffmpeg -map 0:a:0 -f null -`) + `5,00 s` de carte finale.
- formule d'affichage par vers en l'absence de calage mot à mot :
  `affichage = min(fin_vers - debut_vers, max(2.2 s, 0.30 s × nombre_de_mots))`, signalée comme **provisoire** dans la livraison.

### 5.7 Traduction française défilante (MODE HYBRIDE, passages non français) — apport v6.3
- Pilule `y 1452 → 1545`, `x 186 → 894` (largeur 708), fond `#080C12` α 222, liseré or α 185, rayon 24.
- Mots en Montserrat ExtraBold 29, interlettrage 11. Mot actif **or chaud `#FFE07A` + halo 3 px**, glissement `±9 px` sur la durée du vers, curseur karaoké en bas de pilule. **Dormante si la chanson est 100 % FR.**

---

## 6 — Clochettes / CTA pendant les respirations instrumentales

- **Fenêtre = temps sans parole en cours de lecture**, donc `[fin d'affichage du vers + 0,15 s → début du vers suivant]`, seuil **4,0 s** en MODE PEINT (5,0 s en MODE DÉFILEMENT). **9 fenêtres maximum** (apport v6.3), **jamais pendant une syllabe tenue** (apport v6.3).
- **Jamais** de clochette sur les cartes d'accueil/finale, ni pendant un vers en cours de lecture.
- Tile **720×720 centré sur x=540, posé en y 620→1340** (strictement dans les zones sûres).
- **Plaque** : `rounded_rectangle([34,8,686,712], radius 54)` + flou 5, composite **sous** les éléments pour neutraliser la parole peinte pendant le CTA.
- Cloche **dessinée en vectoriel** (pas d'emoji) : **36 angles** de balancement supersamplés ×3, pendule `±12°` amortie sur une période `BELL = 4,0 s`, halo `GaussianBlur 18`, 2 ondes concentriques (période 0,9 s), 3 étincelles, flèche clignotante vers la cloche.
- Texte en **Montserrat** (jamais de cursive) aligné sur l'univers **WTBW** :
  - `CLIQUE SUR +` (56 px ExtraBold espacé de 5 px),
  - pilule `LIKE & PARTAGE` (420×96 px),
  - rappel `Commente si tu aimes · WTBW` (30 px SemiBold).
- Entrée/sortie en **fondu 0,35 s** aux deux bouts de la fenêtre. **Aucun code, aucun lien.**

---

## 7 — Habillage permanent v6.4 : Accueil « SALUT · WTBW + STICKERS DOUX », Finale sans code, Badge clignotant, Progression, Couverture

### 7.1 Zéro code (règle obligatoire, v6.0 + v6.3)
- **Interdit** d'afficher « Regarde jusqu'à la fin / la durée c'est le code » à l'accueil.
- **Interdit** d'afficher un code à 4 chiffres ou « Commente le code » sur la carte finale. Toute accroche de rétention est supprimée.

### 7.2 Carte d'accueil « SALUT · WTBW » en 2 temps (`0,00 s → début du 1er vers`)
Fond = plan du 1er vers flouté (`GaussianBlur 9`, `Brightness 0.62`, scrim sombre / voile `#06090E` 55 % — apport v6.3), filets horizontaux (`x = 170 → 910`) en haut (`y = 310`) et en bas (`y = 1470`), **zoom lent + dérive continue + grain 0,28** (apport v6.3 §5.5 : mouvement réel, 0 gel au `freezedetect`).
- **En-tête permanent** : `WTBW · WOLOF TECHSTEIN BEAT WÊ !` (Montserrat ExtraBold, centré ≤ 720 px).
- **Temps 1 (`0,00 → t0/2` ; référence 0 → 4,2 s si le 1er vers démarre après 8,4 s)** :
  - Grand titre salutation avec léger flottement vertical doux (`±6 px`) : **`SALUT · WTBW`**
  - Sous-titre : **`Wolof TechStein beat 웨`**
  - Plaque centrale encadrée : **`<TITRE> — <ARTISTE>`** (ex. `MONSTER POSITIVE — DSKY`)
- **Temps 2 (`t0/2 → t0` ; référence 4,2 → 8,4 s)** :
  - Titre : **`BIENVENUE SUR WTBW`**
  - Sous-titre : **`Soutiens le son en douceur :`** + **`<TITRE> · <ARTISTE>`**
- **Les 3 Stickers vectoriels animés en douceur (`y = 845, 1045, 1245`, pilules `700×152 px` centrées, pilules sombres pour lisibilité sur fond clair — apport v6.3)** présents sur les cartes :
  Chaque sticker flotte avec une trajectoire sinusoïdale fluide et douce déphasée (`dy = ±8 px`, `dx = ±5 px`, période `2,2 s`–`2,8 s`) et son icône vectorielle supersamplée ×3 respire doucement (`±4,5 %`, période `1,6 s`) :
  1. **Sticker LIKE** (icône **Cœur vectoriel**) : **`LIKE LA VIDÉO`** · *« Laisse un cœur si tu valides »*
  2. **Sticker + S'ABONNER** (icône **Bouton `+` vectoriel**) : **`CLIQUE SUR + POUR T'ABONNER`** · *« Rejoins Wolof TechStein beat 웨 »*
  3. **Sticker COMMENTER** (icône **Bulle de dialogue vectorielle**) : **`COMMENTE SI TU AIMES !`** · *« Dis-nous ton vers préféré »*

### 7.3 Carte finale « MERCI · WTBW » (`fin_chanson → fin_chanson + 5,00 s`) — sans code
Fond = plan du dernier vers flouté (`GaussianBlur 9`, `Brightness 0.62`, scrim sombre) + zoom/dérive + grain 0,28 (apport v6.3) :
- En-tête : **`WTBW · WOLOF TECHSTEIN BEAT WÊ !`**
- Titre : **`MERCI · WTBW`** (ExtraBold 76, stroke 4, baseline `y 436` — apport v6.3)
- Sous-titre : **`Merci d'avoir écouté · Wolof TechStein beat 웨 (WTBW)`** (SemiBold 30, `y 566`) · plaque **`<TITRE> · <ARTISTE>`** — fusionne le « MERCI D'AVOIR ÉCOUTÉ ! » du v6.0
- Les **3 mêmes stickers vectoriels animés en douceur** (`LIKE LA VIDÉO`, `CLIQUE SUR + POUR T'ABONNER`, `COMMENTE SI TU AIMES !`) dans leurs pilules sombres. **Aucun code, aucun contact, aucun lien, aucun logo.**

### 7.4 Badge clignotant & Filet de progression — nouveau v6.3
- **Badge clignotant en alternance** : `y 165` (soulignement `y 189`), Montserrat ExtraBold 32, stroke 3 + liseré sombre. Deux mots alternés, **période 2,4 s par mot**, fondu croisé de **0,4 s** à chaque bascule :
  `rel % 4,8 < 2,4` → **`<ARTISTE>`** (ex. `DSKY`, soulignement 62 px) ; sinon → **`WTBW`** (soulignement 72 px).
  α global plafonné à **0,72**, fondu d'entrée 0,4 s, sortie 0,2 s sur la fin du vers. Jamais permanent, jamais sur cartes ni CTA. **Le clignotement est lent et doux** : c'est un battement, pas un gyrophare (aucune bascule plus rapide que 0,4 s, jamais de clignotement dur).
- **Filet de progression** : y = **1560**, x **170→910**, fond α 48 de 4 px, partie active or α 210 de 8 px, `fr = (t − début_du_1er_vers) / (fin_chanson − début_1er_vers)`.

### 7.5 Couverture TikTok — nouveau v6.3
Une image **dédiée**, pas une frame du clip (une frame contient déjà un badge et un filet).

**Art (générateur)** : `fonds/cover-tiktok.png`, 768×1376.
- buste serré, **un seul personnage**, tête **centrée** entre `y 300 → 720`, regard caméra, visage dégagé ;
- épaules et veste `y 720 → 1180`, **zone calme sombre `y 760 → 1200`** réservée au titre ;
- fond : mur graffiti à l'aube dorée (ou ambiance de la recette choisie), rim light sur les pommettes ;
- 2 petits stickers `y 1240 → 1340`, `x 170 → 600` ;
- bloc **NO TEXT AT ALL** + **NO HORIZONTAL BAND** obligatoires.

**Typo (moteur, `cover.py`)** :
- `1080 × 1920`, JPEG qualité 95, sous-échantillonnage 4:4:4 ;
- voile d'encre dégradé sur les 300 px du bas (α max 0,72) pour la lisibilité ;
- titre 2 lignes, **largeur utile ≤ 900 px** (`x 90 → 990`) — auto-réduction par pas de 2 px au-delà ; `<LIGNE 1>` (ExtraBold 128) puis `<LIGNE 2>` (ExtraBold 104), même dégradé/palette que les paroles de la recette, même contour par dilatation ;
- `<ARTISTE>` (Bold 60, interlettrage 16) entre deux filets or, `y 1495` ; série « Wolof TechStein beat 웨 » `y 1560`.

**Contrôle** : regarder la couverture **en 1:1** ; le titre doit être entièrement dans `x 90 → 990`, le visage entièrement dégagé, aucun mot coupé.

---

## 8 — Recettes de style (une seule par chanson, validée avec l'artiste)

- **8.1 STUDIO ANIME SEINEN — NOIR & BLANC, DÉCORS ATTÉNUÉS & EXPRESSIONS MULTIPLES** *(recette par défaut, celle du v6.0 — validée 36 plans / 47 vers sur « Goinfres », 0 faute)* :
  cel-shading seinen au trait d'encre noir franc (`#050608`), rehauts blancs purs (`#FFFFFF`), gris d'encre (`#2A2E35`), **strictement monochrome noir & blanc** ; **décors variés mais toujours atténués/assombris en arrière-plan brumeux** pour que le protagoniste et le lettrage blanc dominent ; **expressions faciales variées** d'un plan à l'autre selon la dramaturgie du vers ; lettrage cuit par le moteur en capitales serif **blanches et gris-argent sur ruban d'encre noire** dans `y 620→1340` + 2 stickers au trait d'encre blanche collés au sens du vers + fil lumineux blanc.
- **8.2 ENCRE & FEUILLE D'OR — « la nuit qui finit bien »** *(validée sur « Mahu ti tè gbè » et « On est réel »)* :
  peinture numérique matière épaisse, clair-obscur Rembrandt, palette bleu nuit `#0B1B2A` / ambre `#E8A33D` / or `#D9A441` / crème `#F3E7D3`, capitales serif d'or et crème, stickers dorés.
- **8.3 AUBE CLOCHETTES** *(v5.6)* : fonds clairs, lumière d'aube volumétrique.
- **8.4 WANDANCE BATTLE & GRAFFITI LOVES — ORDONNÉE & VISAGE DÉGAGÉ** *(apport v6.3, validée 39 plans / 42 vers, 0 faute)* :
  anime de battle urbain, trait net, cel-shading, graffiti mural dense en arrière-plan, néons cyan et or, nuit bleu-vert puis aube. Plan mi-corps, un seul personnage, visage dans la moitié haute, deux stickers vectoriels `y 782 → 910` (natif). Lettrage or/argent-cyan (§4). Progression lumière : `nuit` → `aube-a` (heure bleue, liseré rose-or) → `aube-b` (soleil plein).

---

## 9 — Continuité entre plans et progression vers l'aube

- l'arc lumineux avance par paliers continus (nuit / ombre → premières lueurs au pont → **aube lumineuse / plein soleil levant** sur le refrain final et l'outro) ;
- **pas de retour en arrière de la lumière** (apport v6.3) : toute reprise du refrain ou de la signature arrivant après le pont d'aube reçoit sa **variante aube dédiée** (ex. `v-167-69-aube.png` sur *Goinfres*) ; un plan `aube-b` ne peut pas précéder un plan `nuit` ;
- buckets de lumière indicatifs (apport v6.3) : `nuit` < 138 s · `aube-a` 138–176 s · `aube-b` ≥ 176 s (à recalibrer sur la durée réelle du morceau) ;
- même personnage, même veste, mêmes cheveux, d'un plan à l'autre ; les stickers changent (cœur + un symbole différent par plan) mais **le cœur reste à gauche**.

---

## 10 — Méthode de fabrication (salves, ancre, contrôle)

1. **Ancre d'abord** : générer `fonds/scene-01-ancre.png`, la contrôler et la valider avec l'artiste (`ANCRE.md`). Elle sert de `images=[…]` de référence à **toutes** les salves.
2. **Salves ≤ 8 images par salve** (limite dure : 10 images/tour) — apport v6.3 ; consigner chaque tour : demandées / réussies / échouées.
3. `verses_map.json` = contrat unique généré par `build_map.py` : `{i, t, fin, affichage_s, texte, image, lignes, disponible, reprise}` où `disponible` est **recalculé avec `os.path.exists`**.
4. `CARTE-VERS.md` générée automatiquement depuis `verses_map.json`.
5. `python3 lettering.py` (ou `bake.py`) → paroles cuites dans les PNG + planche **`CONTROLE-paroles.jpg`** (§4).
6. `python3 render.py` → clip complet, puis contrôles §12.
7. `python3 cover.py` → couverture TikTok (§7.5).
8. QC visuel obligatoire : planche contact `CONTROLE-salveN.jpg` (tuiles ≥ 480 px de large) + planche de crops 1:1 `CONTROLE-salveN-typo.jpg` (grille 16 px) + planche du MP4 final `CONTROLE-mp4-final.jpg` + zoom 1:1 `CONTROLE-typo-zoom.jpg`. Contrôler chaque plan **avant** de le garder : pas de texte du modèle, pas de second visage, pas d'anatomie cassée — un plan fautif se **régénère**, il ne se maquille pas.

---

## 11 — Audio (maître de l'artiste, jamais généré)

- mesurer avant de promettre : durée décodée (`ffmpeg -map 0:a:0 -f null -`), LUFS, TP, LRA, silences.
- `loudnorm` **2 passes linéaires** `I=-14:TP=-1.5:LRA=11`, 48 kHz, stéréo, `libmp3lame -b:a 320k` (CBR 320 kbps), **`-vn` obligatoire**, puis tags ID3v2.4 (`TIT2`, `TALB`, `TPE1`, `TPE2`, `TCON`, `APIC` 1080², `USLT` propre sans horodatages, `TXXX` SIGNATURE/MASTER/IA) et relecture des tags après écriture.
- pour le clip : `apad=pad_dur=6.00` sur le maître avec **`-map 0:a:0 -vn`**, AAC 256k 48 kHz.
- résultat de référence mesuré (apport v6.3) : **−14,04 LUFS**, crête **−1,86 dBTP**, LRA 5,40. Aucun son généré par IA, jamais ; la voix n'est ni retouchée ni réinterprétée.

---

## 12 — Encodage et contrôles obligatoires du rendu

- `libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709`, 30 fps ; pipe `rawvideo` `rgb24` 1080×1920@30 → un seul passage (`n = round(t_end × fps)`).
- **faststart** (apport v6.3) : `-movflags +faststart` **ne marche pas en pipe** → second passage `-c copy -movflags +faststart` obligatoire ; vérifier l'ordre des atomes `ftyp → moov → mdat`.
- **Contrôles à publier avec les chiffres réels** :
  | contrôle | commande | attendu |
  |---|---|---|
  | durée | `ffmpeg -i` | = `frames/fps` à 0,01 s près |
  | frames noires | `blackdetect=d=0.05:pix_th=0.10` (et `pix_th=0.98`, apport v6.3) | **0** |
  | gel | `freezedetect=n=-33dB:d=2.5` | 0 sur les vers ; cartes et CTA animés (grain 0,28 + dérive) et assumés |
  | loudness | `ebur128` | −14,0 LUFS |
  | crête | `astats` | ≤ −1,0 dB |
  | faststart | octets | `moov` avant `mdat` |
  | typo | zoom 1:1 d'un frame rendu + `CONTROLE-paroles.jpg` | nette, contre-formes ouvertes, **aucun doublement de lettre** |
  | couverture | 1:1 | titre dans `x 90 → 990`, visage dégagé |

---

## 13 — Git et livraison

- commit + push **après chaque étape**, uniquement sur la **branche de la session**.
- **toute** réponse de livraison finale contient, dans cet ordre :
  **1)** Titre · **2)** Captions · **3)** Hashtags (13 max) · **4)** le fichier 9:16 (présenté à l'utilisateur) **+ la couverture TikTok** ·
  **5)** Déclaration IA (visuels OUI / audio NON) · **6)** commandes Termux, **une ligne par fichier, séparées par `;`**, sur le hash du commit **après le push** (vérifié avec `git ls-remote` + taille du blob via API), et le détail des contrôles + le prompt universel mis à jour.
- Fichiers > 50 Mo : hébergés dans le dépôt (limite GitHub 100 Mio) ou en release, **jamais** dans un commit de code ordinaire sans le dire. Liens `raw` **figés sur le SHA du commit**, pas sur une branche.

```
pkg install -y curl && termux-setup-storage
```

```
curl -L --retry 3 -C - -o ~/storage/downloads/<TITRE>-<ARTISTE>-9x16.mp4 "<url_raw_du_mp4>"; termux-media-scan -v ~/storage/downloads/<TITRE>-<ARTISTE>-9x16.mp4;
curl -L --retry 3 -C - -o ~/storage/downloads/COVER-tiktok-1080x1920.jpg "<url_raw_de_la_cover>"; termux-media-scan -v ~/storage/downloads/COVER-tiktok-1080x1920.jpg
```

---

## 14 — Interdits permanents (union v6.0 + v6.3)

Drapeau, bannière nationale · système de code à 4 chiffres ou accroche « reste jusqu'à la fin pour le code » · contact, lien, QR, logo dans une image · nudité, anatomie exhibée · photo personnelle envoyée au générateur sans autorisation écrite · cursive sur un CTA · calque typo par-dessus une typo déjà peinte/cuite · horodatages de l'artiste modifiés · validation ou mesure inventée · **texte peint par le générateur d'images** (apport v6.3 : NO TEXT AT ALL) · visage caché (masque, capuche, lunettes opaques, texte devant) · badge clignotant vite · mot inventé · génération de voix ou de musique.

---

## 15 — Gabarits de prompts d'image

### 15.1 STUDIO ANIME SEINEN N&B (recette par défaut — disposition v6.0, garde-fous v6.3)

```
Vertical 9:16, dark seinen anime cel-shaded illustration in strict BLACK AND WHITE monochrome (pure black ink,
stark white highlights, muted charcoal grey tones, zero color), same anime protagonist and style as the reference
image. The canvas is 768 px wide and 1376 px tall; all coordinates below are on this native canvas.

Framing: half-body shot — exactly ONE character, the same Black male anime protagonist with short stylized locks
and closed high-collar black coat. His head (uncovered, face fully visible, nothing over the forehead) sits between
y 190 and y 400, shoulders between y 400 and y 465, frame cuts his hips at the bottom edge. Expression: <expression
faciale précise du vers>. Behind him, an ATTENUATED, darkened, low-contrast charcoal background of <décor adapté au
vers> (rain, rooftops, alley, crowd silhouettes…), palette strictly black and white — deep jet black #050608,
stark pure white #FFFFFF, soft attenuated charcoal grey #2A2E35 in the background. Keep the middle band around
his torso naturally calm and dark (deep ambient shadow only) so the painted lyrics will be added later by the editor.

IMPORTANT — NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol anywhere in the
image, not on walls, clothing or signs: the background must be pure shapes only.

IMPORTANT — NO HORIZONTAL BAND. One continuous scene: no band, strip, panel, rectangle, seam or gradient line across
the image; the calm torso area is a lighting choice, never a drawn shape.

Between y 782 and y 900, inside x 170 -> 600, paint 2 white ink line-art sticker icons side by side (the only graphic
marks allowed, no letters inside them): a glowing white heart and <symbole>, each about 90 px tall, linked by a thin
luminous white line. The floor continues naturally from the stickers to the bottom edge as one single surface sinking
into deeper shadow, with no seam or line. Nothing in the top 102 px, nothing on the right beyond x 647, nothing below
y 1119. No flag, no logo, no watermark.
```

### 15.2 WANDANCE BATTLE & GRAFFITI LOVES (recette v6.3)

```
Vertical 9:16 street-dance battle anime illustration in the dynamic style of Wandance combined with clean
stylish urban graffiti art, keeping the exact same protagonist and visual style as the reference image.
The canvas is 768 px wide and 1376 px tall; all coordinates are on this native canvas.

Framing: half-body shot — exactly ONE character, his head (uncovered, face fully visible, nothing over the
forehead) sits between y 190 and y 400, his shoulders and arms between y 400 and y 465, and the frame cuts his
hips at the bottom edge. Pose: <pose>. His expression: <expression>. Behind him, an attenuated background:
<décor>; <palette nuit | heure bleue | soleil levant>.

IMPORTANT — NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol anywhere in
the image: the whole spray-painted mural and graffiti background must be pure abstract shapes and colour splashes only.

IMPORTANT — NO HORIZONTAL BAND. One continuous scene: no band, strip, panel, rectangle, frame, seam, colour break
or gradient line running across the image. Keep the décor naturally calmer and darker around his torso (middle
third) as a lighting choice — deep ambient shadow — never as a drawn shape.

Below that calm area, between y 790 and y 900 and inside x 170 -> 600, paint 2 stylish urban graffiti sticker
icons side by side (the only graphic marks allowed, no letters inside them): a glowing street-art heart and <symbole>,
each about 90 px tall, linked by a thin luminous gold line. The floor continues naturally to the bottom edge as one
single surface, slowly sinking into deeper shadow, no seam, no line, no texture change. Nothing in the top 100 px,
nothing on the right beyond x 647, no flag, no logo, no watermark.
```

### 15.3 Couverture TikTok (v6.3)

Même bloc que 15.1/15.2 selon la recette, avec :

```
Framing: a tight heroic bust shot — exactly ONE character. His head is large and centred, between y 300 and
y 720, looking straight into the camera; face fully visible, nothing over the forehead. Shoulders and chest fill
the width between y 720 and y 1180. The area between y 760 and y 1200 must stay a calm, dark, uncluttered zone
of his jacket and deep shadow — that is where the title will be placed later.
... stickers between y 1240 and y 1340 and inside x 170 -> 600 ...
```

---

## 16 — Historique

| version | apport |
|---|---|
| v5.9 (2026-10-14) | « Ça bouge, sans voiler la parole » : question §0, mouvement par fenêtre glissante sur source 110 %, état éteint, grain cyclé, vignette masque L. Validé sur `productions/mahu-ti-te-gbe/` et `productions/on-est-reel/`. |
| v6.0 (2026-10-21) | « WTBW Salut & Stickers Doux » : suppression définitive du code de fin ; accueil 2 temps « Salut · WTBW » + finale sans code animés avec 3 stickers vectoriels doux ; recette STUDIO ANIME SEINEN N&B ; note anti-`ONLY:`. Validé sur `productions/goinfres/` (36 plans, 47 vers, 6 838 frames / 227,933 s, −14,0 LUFS, blackdetect 0, faststart OK). |
| v6.3 | badge clignotant DSKY ↔ WTBW ; couverture TikTok ; le générateur ne peint plus aucun mot (lettrage moteur) ; contour par dilatation ; halo serré ; `dy` par plan ; `EXTINGUISH` off en 100 % FR ; grain par frame + cartes animées (0 gel) ; `MERCI · WTBW`. Validé sur « On nous a volé notre éducation » (50 vers, 40 plans, 9 fenêtres CTA). |
| **v6.4 (2026-11-11)** | **Harmonie v6.0 × v6.3** : squelette, intro, disposition, cartes « Salut · WTBW » 2 temps et recette N&B du **v6.0** conservés ; apports mesurés du **v6.3** intégrés (badge clignotant artiste↔WTBW, couverture TikTok, lettrage moteur 4 correctifs, `EXTINGUISH=False` en 100 % FR, grain 8 motifs/frame + cartes animées, `MERCI · WTBW` + sous-titre « Merci d'avoir écouté », conversion native 768×1376, salves ≤ 8, gabarits NO TEXT AT ALL). Prod en cours : **MONSTER POSITIVE** → `productions/monster-positive/`. |

**Signature :** « Wolof TechStein beat 웨 ! » (WTBW) ⚡


# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v6.5 « PILULE LISIBLE, BADGE DSKY WTBW, ZÉRO VOILE SUR LA PAROLE » (HARMONIE v6.0 × v6.3, NETTOYÉE)

Mise à jour : **2026-11-13** (v6.5 : nettoyage des redondances + correctifs mesurés après rejet du rendu du 2026-11-13). Document **100 % auto-suffisant**.

**Règle de fusion (l'harmonie demandée) :** ce document garde le **squelette, l'intro, la disposition et les cartes du v6.0** (question §0, zones sûres 1080×1920, accueil « Salut · WTBW » en 2 temps avec ses 3 stickers animés en douceur, recette STUDIO ANIME SEINEN N&B, mouvement à 4 trajectoires, salves + ancre, livraison Git/Termux) et intègre les **apports mesurés du v6.3** : badge clignotant artiste ↔ WTBW, couverture TikTok, lettrage cuit par le **moteur** (le générateur ne peint plus aucun mot), grain par frame + cartes animées anti-gel (l'extinction `EXTINGUISH` introduite en v6.3 est **supprimée définitivement en v6.5**, §5.4), carte finale « MERCI · WTBW ».

Quand v6.0 et v6.3 se contredisent : on garde **la disposition du v6.0** et **la correction mesurée du v6.3**. Chaque point repris du v6.3 est marqué « apport v6.3 ».

Tous les chiffres cités sont **mesurés sur des fichiers livrés**, jamais des intentions.

---

## 0 — LA QUESTION À POSER AVANT TOUT (obligatoire, premier message de l'agent)

Avant de générer quoi que ce soit, demander à l'artiste, en une phrase :

> **« Tu veux les paroles en DÉFILEMENT (texte posé par le montage, qui défile mot à mot) ou DÉJÀ PEINTES DANS
> L'IMAGE (la parole est cuite dans la matière de chaque visuel) ? »**

- L'artiste ne répond pas → **MODE PEINT** par défaut, et le dire dans la réponse.
- Il répond « défilant » → **MODE DÉFILEMENT**.
- Il répond « les deux » → **MODE HYBRIDE** : paroles peintes dans le visuel + traduction FR défilante en pilule pour les passages non français (apport v6.3 §5.7). Sur un morceau **100 % français**, « les deux » retombe sur **MODE PEINT** (pas de pilule quand il n'y a rien à traduire).

| | **MODE PEINT** (défaut, validé) | **MODE DÉFILEMENT** |
|---|---|---|
| Texte à l'écran | parole **cuite dans l'image par le moteur** `lettering.py` (apport v6.3 §3.2 : le générateur reçoit « NO TEXT AT ALL », on ne lui demande jamais de peindre un mot) ; le montage n'incruste **aucune** typo hors cartes et pilule | calque PIL, bloc centré ≤ 740 px, **mot actif mis en avant**, reste adouci |
| Icônes / stickers | **autorisés et voulus**, 1 à 3 par image, collés au sens du vers | **interdits dans l'œuvre** : zone basse réservée au sous-titre |
| Nombre de plans | **1 plan par vers distinct** + variantes d'aube dédiées pour le refrain final (§9) | 1 plan par bloc de 2–3 vers |
| Accentuation | aucune sur-typo ; le lettrage est déjà cuit | halo 3 px + `spaced()` lettrage espacé |
| Durée d'affichage | temps du vers, et le plan **reste net** jusqu'au bout (aucune extinction, §5.4 supprimé en v6.5) | temps du vers, mot à mot |
| Zones sûres | écrites **dans le prompt de génération** (§3) + cuites par le moteur | imposées au calque (§3) |

Le choix est **verrouillé pour toute la prod** : pas de mélange entre vers, jamais.

---

## 1 — Hiérarchie des demandes (rappel permanent)

1. Demande explicite actuelle de l'artiste.
2. Configuration validée de la prod (ancre, personnages, titre exact, style, palette).
3. **v6.4 (ce document)**.
4. v6.3, v6.0, v5.9… pour ce qui n'est pas contredit.

En cas de conflit interne (apport v6.3) : **orthographe et sens des paroles > audio de l'artiste intact > lisibilité de la parole (aucune typo ne se couvre, ne se floute ni ne s'assombrit **JAMAIS** — règle absolue v6.5 (2026-11-13) : aucune extinction, aucun flou, aucun assombrissement, aucun voile sur les paroles peintes, pendant qu'elles se chantent **ni après**, dans **aucun** mode) > esthétique > ornements** — le point le plus bas cède.

États à tenir séparés et nommés : **proposé / généré / validé par l'artiste / rendu / contrôlé**.
**Jamais** inventer : validation de l'artiste, hash publié, mesure, fichier final, « à peu près ».

---

## 2 — Paramètres de la prod (bloc à remplir à chaque chanson)

```
TITRE        : MONSTER POSITIVE          (recopié EXACTEMENT, accents compris)
ARTISTE      : …                          (badge clignotant ARTISTE ↔ WTBW, orthographe EXACTE en capitales, ex. « DSKY » — jamais « Daïsky » à l'écran)
LANGUES      : …                          (mixte = le dire au générateur : « français + signature wolof/fon »)
PAROLES      : chemin/fichier.txt         (N lignes = N vers, horodatages de l'artiste non retouchés)
AUDIO        : chemin/fichier.mp3         (maître fourni par l'artiste, jamais généré)
RECETTE      : STUDIO ANIME SEINEN N&B (défaut) | ENCRE & FEUILLE D'OR | AUBE CLOCHETTES | WANDANCE BATTLE & GRAFFITI LOVES
HABILLAGE    : WTBW SALUT + STICKERS DOUX (Like · Clique sur + pour t'abonner · Commente si tu aimes) — SANS CODE
SIGNATURE    : « Wolof TechStein beat 웨 ! » (WTBW)
MODE         : PEINT (défaut) | DÉFILEMENT | HYBRIDE      ← réponse à la question §0
DOSSIER      : productions/monster-positive/              (fonds/ livrables/ fonts/ + verses_map.json + CARTE-VERS.md)
```

---

## 3 — Zones sûres 1080×1920 (à recopier dans CHAQUE prompt d'image)

- rien dans les **144 premiers pixels** en haut (marge de sécurité : la règle d'or dit 140) ;
- rien à droite de **x ≥ 910** entre **y 960 et y 1690** (zone bouton `+` + pavé de commentaire TikTok) ;
- rien en dessous de **y = 1574** ;
- bloc de texte **centré, largeur ≤ 740 px**, dans la bande **y 620 → 1340** (les sous-lignes doivent rester **au-dessus** des icônes, jamais poussées sous `y = 1574`) ;
- la typo **ne couvre jamais un visage** : le visage du protagoniste vit dans la moitié haute (`y < 560`) ;
- **jamais de drapeau, jamais de bannière, jamais de contact/lien/logo, jamais de code** dans l'image ;
- sortie native du générateur = 768×1376 → passage à 1080×1920 **ancré en HAUT**, rognage du bas : **le crâne n'est jamais coupé** ;
- tenues fermées et élégantes, visage dégagé, aucune nudité, personnages fictifs uniquement (sauf figures historiques ou photos expressément autorisées par l'artiste).

### 3.1 Conversion obligatoire 1080×1920 → natif 768×1376 (facteur **0,7111**) — apport v6.3

| repère 1080×1920 | natif 768×1376 |
|---|---|
| marge haute `144` | `102` |
| visage `y < 560` | `y < 398` (front peint dès `190` : **ne jamais recadrer au-dessus de `y 190`**) |
| bande texte `620 → 1340` | `441 → 953` |
| VO bilingue `650 → 1040` | `462 → 740` |
| stickers `1100 → 1280` | `782 → 910` |
| pilule FR `1444 → 1556` | `1027 → 1107` |
| bas interdit `1574` | `1119` |
| droite interdite `x ≥ 910` | `x ≥ 647` |
| largeur max `740` | `526` |

**Cadrage obligatoire** : front à `y ≥ 190`, tête `190→400`, épaules `400→465`, plan mi-corps. Les animations de carte (badge `y 146→184`, en-tête `y 236`) ne passent **jamais** sur le visage.

### 3.2 — Qui peint quoi (décision mesurée v6.3, inchangée)

Mesures sur 18 plans du générateur : **0/18** respecte la boîte de typo demandée, capitales 110 px pour 34 demandées, un plan sur deux hors marge droite, accents et ponctuation perdus. Le modèle fait de l'excellente **image**, pas de la **typographie fiable**.

| | qui le fait | où |
|---|---|---|
| personnage, décor, lumière, 2 stickers | **générateur d'images** | `prompts_art.json` — prompt **« NO TEXT AT ALL »** |
| paroles peintes | **moteur** `lettering.py` | cuit dans le PNG, boîte `x 150→590 / y 470→750` (natif) |
| badge, cartes, filet, CTA, pilule FR | **moteur** `render.py` | plein cadre |
| couverture TikTok | **générateur + `cover.py`** | §7.5 |

Conséquence : **on ne redemande jamais au générateur de peindre un mot**. Un plan qui contient déjà du texte du modèle est un plan **à refaire**, pas à maquiller.

---

## 4 — Orthographe et lettrage peint : règles + les 4 correctifs v6.3 (mesurés en 1:1)

- recopier le vers **exact** dans le contrat (`verses_map.json`), jamais de mot inventé, jamais d'accent perdu ;
- **nommer les diacritiques** si la langue en porte (`WÊ`, `CRÈVENT`, `ÊTES`, `L'ÂME`, `LÈVE`, `RÉSISTE`, `THÈSES`, `ÇA`, `CŒURS`, `TÈ`, `GBÈ`) et les exiger explicitement au moteur ;
- **piège à éviter dans les prompts** : éviter de placer le mot anglais `ONLY:` ou `EXACTLY:` juste devant les guillemets d'une ligne courte, car certains modèles peignent littéralement `ONLY:` en haut du bloc (observé sur `scene-15` et `scene-29` v1 de *Goinfres*) ;
- relire chaque plan sur une **contact sheet ≥ 480 px de large** (`500×896 px` par tuile) **ET** sur une **planche de crops pleine résolution 1:1 avec grille de 16 px** (`CONTROLE-salveN-typo.jpg`), jamais sur une miniature ; pour le lettrage cuit : planche **`CONTROLE-paroles.jpg` lue en 1:1** (contre-formes ouvertes, accents `É`/`Ê` intacts, aucun chevauchement) — apport v6.3 ;
- texte faux, mot omis ou mot doublé → **régénérer le plan** avec un prompt court et explicite ;
- **retouche exceptionnelle** : si, après 2 échecs, il ne manque **qu'un diacritique**, il est permis de le combler en **copiant le glyphe déjà peint dans la même image** (patch ≤ 30 px, masque = pixels du glyphe uniquement, MaxFilter 3 + flou 0,9), jamais en recomposant un caractère à la police. Cette retouche doit être **déclarée** dans la livraison ;
- un plan qui échoue à la génération (`STOP`, `MAX_TOKENS`) = **échec consigné**, jamais compté comme livré.

**Les 4 correctifs du lettrage moteur (apport v6.3) :**
1. **Contour par dilatation, jamais `stroke_width`** (qui remplit les contre-formes : `A` plein, `E` pavé) : glyphe dessiné sans contour, masque dilaté (`MaxFilter(2·ow+1)`, `ow = taille/10`), posé **derrière** les lettres ; anticrénelage conservé.
2. **Une tuile par glyphe** à la taille de son encre (`textbbox` par caractère + interlettrage `0,055 · taille`), chaque glyphe tourné (`±1,0°`) au centre de sa tuile — fini les chevauchements type « TEC**HST**EIN ».
3. **Halo = ombre serrée, jamais une flaque** : dilatation `MaxFilter(9)` + flou 7 à 60 %, flou 17 à 34 %, 150 mouchetures masquées autour des glyphes. La silhouette reste lisible jusqu'au col.
4. **Décalage vertical par plan** (`typo_offsets.json`) : si le visage descend sous `y 470` natif, le bloc descend de `dy` px, le visage reste dégagé, le bloc reste au-dessus de `y 1119`.

**Palette du lettrage selon la recette** : STUDIO ANIME SEINEN N&B → capitales **blanc pur `#FFFFFF`** et **gris-argent** sur ruban d'encre noire (disposition v6.0) ; WANDANCE → or `#FFE8A8 → #E8A83E` (ligne 1) et argent-cyan `#F0FCFF → #96CDE0` (ligne 2), graine déterministe `zlib.crc32(l1|l2)`, coulures d'encre **sous** le bloc, jamais sur les lettres.

---

## 5 — MOUVEMENT : animer sans voiler la parole

**Principe : l'image vit, le mot reste lisible. Le mouvement est une fenêtre qui glisse, jamais une échelle qui change.**

### 5.1 Préparation (une fois par plan)
- `SC = 1.10` : le plan 768×1376 est agrandi à **110 %** (≈ 1188×2132) en LANCZOS une seule fois par plan, puis on garde **une seule** image en cache : la nette (plus d'image « éteinte », §5.4 supprimé en v6.5). Marge disponible : **108 px en x, 212 px en y** (apport v6.3 : `X ∈ [0;108]`, `Y ∈ [0;208]`).
- **Aucun resize par frame** : `Image.blend(base, zoom, u)` entre deux échelles dédouble les lettres (ghosting visible au zoom 1:1).

### 5.2 Le travelling
- la frame = `big.crop` d'une fenêtre 1080×1920 dont l'origine glisse de `(ax0,ay0)` à `(ax1,ay1)` selon l'avancement `u` du vers ;
- **4 trajectoires**, alternées par parité de l'indice du segment (`si % 4`) :
  `(0.0→1.0, 0.02→0.98)` · `(1.0→0.0, 0.02→0.98)` · `(0.18→0.82, 0.98→0.02)` · `(0.82→0.18, 0.02→0.98)` ;
- **1 travelling = 1 vers**, durée du travelling = durée du vers ;
- amplitude plafonnée à la marge (§5.1) : aucun bord noir découvert, aucune coupe de la bande de texte `y 620→1340` ;
- pas de rotation, pas de shake, pas de zoom-in brutal. (Complément v6.3 pour les **cartes uniquement** : zoom lent + dérive continue `1,04 + 0,035·sin`, période ~7,7 s — voir §5.5.)

### 5.3 Transitions
- `xfade` (fondu enchaîné) de **0,35 s** uniquement **entre deux segments** ; coupe franche entre deux plans (apport v6.3) ; respiration lumineuse `±12 %` sur les vers > 3,5 s (apport v6.3).

### 5.4 AUCUNE EXTINCTION — règle absolue v6.5 (décision 2026-11-13, DÉFINITIVE)
- L'ancien « état éteint » (`Brightness ×0,22` + `GaussianBlur 7` + masque fondu sur la bande de texte) est **SUPPRIMÉ DÉFINITIVEMENT**. Aucune extinction, aucun flou, aucun assombrissement, aucun voile, aucune plaque ne recouvre **jamais** les paroles peintes — pendant qu'elles se chantent **ni après**, dans **aucun** mode (PEINT / DÉFILEMENT / HYBRIDE). Le plan reste net 100 % du temps. **Ne pas réintroduire sous aucune forme.**
- Seuls les **fonds des cartes** d'accueil/finale (§7.2/§7.3) peuvent être floutés — jamais un plan de vers en cours de lecture.

### 5.5 Grain et vignette — règle corrigée v6.3
- **vignette** = masque `L` centré (0 au centre, ≈ 86 aux coins, flou 34) composite d'une couleur sombre `#04080C` : `Image.composite(noir, cur, masque)`. Jamais `Image.blend(cur, image_sombre, k)`.
- **grain 35 mm** = **8 motifs pré-calculés, un motif par frame** (`GRAINS[k % 8]`, seed fixe), blend `0,045`. Sur les **cartes** : grain `0,28` + zoom lent + dérive continue (§5.2) — à 0,12 la carte était détectée comme gel de 3,77 s au `freezedetect` alors que le rendu bougeait à l'œil.

### 5.6 Calage
- horodatages fournis par l'artiste gardés **tels quels** ; le premier vers démarre à la **première syllabe chantée** (apport v6.3) ; durée du clip = durée **décodée** de l'audio (`ffmpeg -map 0:a:0 -f null -`) + `5,00 s` de carte finale.
- formule d'affichage par vers en l'absence de calage mot à mot :
  `affichage = min(fin_vers - debut_vers, max(2.2 s, 0.30 s × nombre_de_mots))`, signalée comme **provisoire** dans la livraison.

### 5.7 Pilule de traduction FR (MODE HYBRIDE, passages non FR) — cotes mesurées v6.5 (2026-11-13)
- Pilule `y 1444 → 1556`, `x 186 → 894` (708 px hors tout, **≤ 620 px utiles pour le texte**), fond `#080C12` α 228, liseré or α 200, rayon 26, **barre de progression** en bas `y 1548 → 1556` (x 186 → 894, or).
- Texte Montserrat ExtraBold **32 px**, interlettrage **6 px** ; **auto-fit** : pas de 2 px vers le bas (min 12 px) tant que la largeur mesurée > 620 px.
- **Anti-collage (règle absolue)** : l'espace entre deux mots = le tracking seul (6 px), **aucun resserrement** de l'interlettrage sous 6 px, aucun mot collé au suivant ; texte **centré exactement sur x = 540** (glissement doux `±9 px` uniquement) et **masqué aux bords intérieurs** de la pilule (`x 198 → 882`) : aucune lettre ne sort du fond sombre, jamais de débordement.
- Mot actif **or chaud `#FFE07A` + halo 3 px** (`MaxFilter 7` + flou 3), autres mots blanc cassé α 235. Une seule traduction par vers, jamais deux pilules qui se chevauchent. **Dormante si la chanson est 100 % FR.**

---

## 6 — Clochettes / CTA pendant les respirations instrumentales

- **Fenêtre = temps sans parole en cours de lecture**, donc `[fin d'affichage du vers + 0,15 s → début du vers suivant]`, seuil **4,0 s** en MODE PEINT (5,0 s en MODE DÉFILEMENT). **9 fenêtres maximum** (apport v6.3), **jamais pendant une syllabe tenue** (apport v6.3).
- **Jamais** de clochette sur les cartes d'accueil/finale, ni pendant un vers en cours de lecture.
- Tile **720×720 centré sur x=540, posé en y 620→1340** (strictement dans les zones sûres).
- **Plaque** : `rounded_rectangle([34,8,686,712], radius 54)` + flou 5, composite **sous** les éléments pour neutraliser la parole peinte pendant le CTA.
- Cloche **dessinée en vectoriel** (pas d'emoji) : **36 angles** de balancement supersamplés ×3, pendule `±12°` amortie sur une période `BELL = 4,0 s`, halo `GaussianBlur 18`, 2 ondes concentriques (période 0,9 s), 3 étincelles, flèche clignotante vers la cloche.
- Texte en **Montserrat** (jamais de cursive) aligné sur l'univers **WTBW** :
  - `CLIQUE SUR +` (56 px ExtraBold espacé de 5 px),
  - pilule `LIKE & PARTAGE` (420×96 px),
  - rappel `Commente si tu aimes · WTBW` (30 px SemiBold).
- Entrée/sortie en **fondu 0,35 s** aux deux bouts de la fenêtre. **Aucun code, aucun lien.**

---

## 7 — Habillage permanent v6.4 : Accueil « SALUT · WTBW + STICKERS DOUX », Finale sans code, Badge clignotant, Progression, Couverture

### 7.1 Zéro code (règle obligatoire, v6.0 + v6.3)
- **Interdit** d'afficher « Regarde jusqu'à la fin / la durée c'est le code » à l'accueil.
- **Interdit** d'afficher un code à 4 chiffres ou « Commente le code » sur la carte finale. Toute accroche de rétention est supprimée.

### 7.2 Carte d'accueil « SALUT · WTBW » en 2 temps (`0,00 s → début du 1er vers`)
Fond = plan du 1er vers flouté (`GaussianBlur 9`, `Brightness 0.62`, scrim sombre / voile `#06090E` 55 % — apport v6.3), filets horizontaux (`x = 170 → 910`) en haut (`y = 310`) et en bas (`y = 1470`), **zoom lent + dérive continue + grain 0,28** (apport v6.3 §5.5 : mouvement réel, 0 gel au `freezedetect`).
- **En-tête permanent** : `WTBW · WOLOF TECHSTEIN BEAT WÊ !` (Montserrat ExtraBold, centré ≤ 720 px).
- **Temps 1 (`0,00 → t0/2` ; référence 0 → 4,2 s si le 1er vers démarre après 8,4 s)** :
  - Grand titre salutation avec léger flottement vertical doux (`±6 px`) : **`SALUT · WTBW`**
  - Sous-titre : **`Wolof TechStein beat 웨`**
  - Plaque centrale encadrée : **`<TITRE> — <ARTISTE>`** (ex. `MONSTER POSITIVE — DSKY`)
- **Temps 2 (`t0/2 → t0` ; référence 4,2 → 8,4 s)** :
  - Titre : **`BIENVENUE SUR WTBW`**
  - Sous-titre : **`Soutiens le son en douceur :`** + **`<TITRE> · <ARTISTE>`**
- **Les 3 Stickers vectoriels animés en douceur (`y = 845, 1045, 1245`, pilules `700×152 px` centrées, pilules sombres pour lisibilité sur fond clair — apport v6.3)** présents sur les cartes :
  Chaque sticker flotte avec une trajectoire sinusoïdale fluide et douce déphasée (`dy = ±8 px`, `dx = ±5 px`, période `2,2 s`–`2,8 s`) et son icône vectorielle supersamplée ×3 respire doucement (`±4,5 %`, période `1,6 s`) :
  1. **Sticker LIKE** (icône **Cœur vectoriel**) : **`LIKE LA VIDÉO`** · *« Laisse un cœur si tu valides »*
  2. **Sticker + S'ABONNER** (icône **Bouton `+` vectoriel**) : **`CLIQUE SUR + POUR T'ABONNER`** · *« Rejoins Wolof TechStein beat 웨 »*
  3. **Sticker COMMENTER** (icône **Bulle de dialogue vectorielle**) : **`COMMENTE SI TU AIMES !`** · *« Dis-nous ton vers préféré »*

### 7.3 Carte finale « MERCI · WTBW » (`fin_chanson → fin_chanson + 5,00 s`) — sans code
Fond = plan du dernier vers flouté (`GaussianBlur 9`, `Brightness 0.62`, scrim sombre) + zoom/dérive + grain 0,28 (apport v6.3) :
- En-tête : **`WTBW · WOLOF TECHSTEIN BEAT WÊ !`**
- Titre : **`MERCI · WTBW`** (ExtraBold 76, stroke 4, baseline `y 436` — apport v6.3)
- Sous-titre : **`Merci d'avoir écouté · Wolof TechStein beat 웨 (WTBW)`** (SemiBold 30, `y 566`) · plaque **`<TITRE> · <ARTISTE>`** — fusionne le « MERCI D'AVOIR ÉCOUTÉ ! » du v6.0
- Les **3 mêmes stickers vectoriels animés en douceur** (`LIKE LA VIDÉO`, `CLIQUE SUR + POUR T'ABONNER`, `COMMENTE SI TU AIMES !`) dans leurs pilules sombres. **Aucun code, aucun contact, aucun lien, aucun logo.**

### 7.4 Badge clignotant & Filet de progression — nouveau v6.3
- **Badge clignotant en alternance** : `y 165` (soulignement `y 189`), Montserrat ExtraBold 32, stroke 3 + liseré sombre. Deux mots alternés, **période 2,4 s par mot**, fondu croisé de **0,4 s** à chaque bascule :
  `rel % 4,8 < 2,4` → **`<ARTISTE>`** (soulignement 62 px) ; sinon → **`WTBW`** (soulignement 72 px). Le badge lit **toujours les DEUX mots `<ARTISTE> WTBW` en alternance** — pour MONSTER POSITIVE : exactement **« DSKY » ↔ « WTBW »** (jamais « Daïsky », jamais un seul des deux mots).
  α global plafonné à **0,72**, fondu d'entrée 0,4 s, sortie 0,2 s sur la fin du vers. Jamais permanent, jamais sur cartes ni CTA. **Le clignotement est lent et doux** : c'est un battement, pas un gyrophare (aucune bascule plus rapide que 0,4 s, jamais de clignotement dur).
- **Filet de progression** : y = **1560**, x **170→910**, fond α 48 de 4 px, partie active or α 210 de 8 px, `fr = (t − début_du_1er_vers) / (fin_chanson − début_1er_vers)`.

### 7.5 Couverture TikTok — nouveau v6.3
Une image **dédiée**, pas une frame du clip (une frame contient déjà un badge et un filet).

**Art (générateur)** : `fonds/cover-tiktok.png`, 768×1376.
- buste serré, **un seul personnage**, tête **centrée** entre `y 300 → 720`, regard caméra, visage dégagé ;
- épaules et veste `y 720 → 1180`, **zone calme sombre `y 760 → 1200`** réservée au titre ;
- fond : mur graffiti à l'aube dorée (ou ambiance de la recette choisie), rim light sur les pommettes ;
- 2 petits stickers `y 1240 → 1340`, `x 170 → 600` ;
- bloc **NO TEXT AT ALL** + **NO HORIZONTAL BAND** obligatoires.

**Typo (moteur, `cover.py`)** :
- `1080 × 1920`, JPEG qualité 95, sous-échantillonnage 4:4:4 ;
- voile d'encre dégradé sur les 300 px du bas (α max 0,72) pour la lisibilité ;
- titre 2 lignes, **largeur utile ≤ 900 px** (`x 90 → 990`) — auto-réduction par pas de 2 px au-delà ; `<LIGNE 1>` (ExtraBold 128) puis `<LIGNE 2>` (ExtraBold 104), même dégradé/palette que les paroles de la recette, même contour par dilatation ;
- `<ARTISTE>` (Bold 60, interlettrage 16) entre deux filets or, `y 1495` ; série « Wolof TechStein beat 웨 » `y 1560`.

**Contrôle** : regarder la couverture **en 1:1** ; le titre doit être entièrement dans `x 90 → 990`, le visage entièrement dégagé, aucun mot coupé.

---

## 8 — Recettes de style (une seule par chanson, validée avec l'artiste)

- **8.1 STUDIO ANIME SEINEN — NOIR & BLANC, DÉCORS ATTÉNUÉS & EXPRESSIONS MULTIPLES** *(recette par défaut, celle du v6.0 — validée 36 plans / 47 vers sur « Goinfres », 0 faute)* :
  cel-shading seinen au trait d'encre noir franc (`#050608`), rehauts blancs purs (`#FFFFFF`), gris d'encre (`#2A2E35`), **strictement monochrome noir & blanc** ; **décors variés mais toujours atténués/assombris en arrière-plan brumeux** pour que le protagoniste et le lettrage blanc dominent ; **expressions faciales variées** d'un plan à l'autre selon la dramaturgie du vers ; lettrage cuit par le moteur en capitales serif **blanches et gris-argent sur ruban d'encre noire** dans `y 620→1340` + 2 stickers au trait d'encre blanche collés au sens du vers + fil lumineux blanc.
- **8.2 ENCRE & FEUILLE D'OR — « la nuit qui finit bien »** *(validée sur « Mahu ti tè gbè » et « On est réel »)* :
  peinture numérique matière épaisse, clair-obscur Rembrandt, palette bleu nuit `#0B1B2A` / ambre `#E8A33D` / or `#D9A441` / crème `#F3E7D3`, capitales serif d'or et crème, stickers dorés.
- **8.3 AUBE CLOCHETTES** *(v5.6)* : fonds clairs, lumière d'aube volumétrique.
- **8.4 WANDANCE BATTLE & GRAFFITI LOVES — ORDONNÉE & VISAGE DÉGAGÉ** *(apport v6.3, validée 39 plans / 42 vers, 0 faute)* :
  anime de battle urbain, trait net, cel-shading, graffiti mural dense en arrière-plan, néons cyan et or, nuit bleu-vert puis aube. Plan mi-corps, un seul personnage, visage dans la moitié haute, deux stickers vectoriels `y 782 → 910` (natif). Lettrage or/argent-cyan (§4). Progression lumière : `nuit` → `aube-a` (heure bleue, liseré rose-or) → `aube-b` (soleil plein).

---

## 9 — Continuité entre plans et progression vers l'aube

- l'arc lumineux avance par paliers continus (nuit / ombre → premières lueurs au pont → **aube lumineuse / plein soleil levant** sur le refrain final et l'outro) ;
- **pas de retour en arrière de la lumière** (apport v6.3) : toute reprise du refrain ou de la signature arrivant après le pont d'aube reçoit sa **variante aube dédiée** (ex. `v-167-69-aube.png` sur *Goinfres*) ; un plan `aube-b` ne peut pas précéder un plan `nuit` ;
- buckets de lumière indicatifs (apport v6.3) : `nuit` < 138 s · `aube-a` 138–176 s · `aube-b` ≥ 176 s (à recalibrer sur la durée réelle du morceau) ;
- même personnage, même veste, mêmes cheveux, d'un plan à l'autre ; les stickers changent (cœur + un symbole différent par plan) mais **le cœur reste à gauche**.

---

## 10 — Méthode de fabrication (salves, ancre, contrôle)

1. **Ancre d'abord** : générer `fonds/scene-01-ancre.png`, la contrôler et la valider avec l'artiste (`ANCRE.md`). Elle sert de `images=[…]` de référence à **toutes** les salves.
2. **Salves ≤ 8 images par salve** (limite dure : 10 images/tour) — apport v6.3 ; consigner chaque tour : demandées / réussies / échouées.
3. `verses_map.json` = contrat unique généré par `build_map.py` : `{i, t, fin, affichage_s, texte, image, lignes, disponible, reprise}` où `disponible` est **recalculé avec `os.path.exists`**.
4. `CARTE-VERS.md` générée automatiquement depuis `verses_map.json`.
5. `python3 lettering.py` (ou `bake.py`) → paroles cuites dans les PNG + planche **`CONTROLE-paroles.jpg`** (§4).
6. `python3 render.py` → clip complet, puis contrôles §12.
7. `python3 cover.py` → couverture TikTok (§7.5).
8. QC visuel obligatoire : planche contact `CONTROLE-salveN.jpg` (tuiles ≥ 480 px de large) + planche de crops 1:1 `CONTROLE-salveN-typo.jpg` (grille 16 px) + planche du MP4 final `CONTROLE-mp4-final.jpg` + zoom 1:1 `CONTROLE-typo-zoom.jpg`. Contrôler chaque plan **avant** de le garder : pas de texte du modèle, pas de second visage, pas d'anatomie cassée — un plan fautif se **régénère**, il ne se maquille pas.

---

## 11 — Audio (maître de l'artiste, jamais généré)

- mesurer avant de promettre : durée décodée (`ffmpeg -map 0:a:0 -f null -`), LUFS, TP, LRA, silences.
- `loudnorm` **2 passes linéaires** `I=-14:TP=-1.5:LRA=11`, 48 kHz, stéréo, `libmp3lame -b:a 320k` (CBR 320 kbps), **`-vn` obligatoire**, puis tags ID3v2.4 (`TIT2`, `TALB`, `TPE1`, `TPE2`, `TCON`, `APIC` 1080², `USLT` propre sans horodatages, `TXXX` SIGNATURE/MASTER/IA) et relecture des tags après écriture.
- pour le clip : `apad=pad_dur=6.00` sur le maître avec **`-map 0:a:0 -vn`**, AAC 256k 48 kHz.
- résultat de référence mesuré (apport v6.3) : **−14,04 LUFS**, crête **−1,86 dBTP**, LRA 5,40. Aucun son généré par IA, jamais ; la voix n'est ni retouchée ni réinterprétée.

---

## 12 — Encodage et contrôles obligatoires du rendu

- `libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709`, 30 fps ; pipe `rawvideo` `rgb24` 1080×1920@30 → un seul passage (`n = round(t_end × fps)`).
- **faststart** (apport v6.3) : `-movflags +faststart` **ne marche pas en pipe** → second passage `-c copy -movflags +faststart` obligatoire ; vérifier l'ordre des atomes `ftyp → moov → mdat`.
- **Contrôles à publier avec les chiffres réels** :
  | contrôle | commande | attendu |
  |---|---|---|
  | durée | `ffmpeg -i` | = `frames/fps` à 0,01 s près |
  | frames noires | `blackdetect=d=0.05:pix_th=0.10` (et `pix_th=0.98`, apport v6.3) | **0** |
  | gel | `freezedetect=n=-33dB:d=2.5` | 0 sur les vers ; cartes et CTA animés (grain 0,28 + dérive) et assumés |
  | loudness | `ebur128` | −14,0 LUFS |
  | crête | `astats` | ≤ −1,0 dB |
  | faststart | octets | `moov` avant `mdat` |
  | typo | zoom 1:1 d'un frame rendu + `CONTROLE-paroles.jpg` | nette, contre-formes ouvertes, **aucun doublement de lettre** |
  | couverture | 1:1 | titre dans `x 90 → 990`, visage dégagé |

---

## 13 — Git et livraison

- commit + push **après chaque étape**, uniquement sur la **branche de la session**.
- **toute** réponse de livraison finale contient, dans cet ordre :
  **1)** Titre · **2)** Captions · **3)** Hashtags (13 max) · **4)** le fichier 9:16 (présenté à l'utilisateur) **+ la couverture TikTok** ·
  **5)** Déclaration IA (visuels OUI / audio NON) · **6)** commandes Termux, **une ligne par fichier, séparées par `;`**, sur le hash du commit **après le push** (vérifié avec `git ls-remote` + taille du blob via API), et le détail des contrôles + le prompt universel mis à jour.
- Fichiers > 50 Mo : hébergés dans le dépôt (limite GitHub 100 Mio) ou en release, **jamais** dans un commit de code ordinaire sans le dire. Liens `raw` **figés sur le SHA du commit**, pas sur une branche.

```
pkg install -y curl && termux-setup-storage
```

```
curl -L --retry 3 -C - -o ~/storage/downloads/<TITRE>-<ARTISTE>-9x16.mp4 "<url_raw_du_mp4>"; termux-media-scan -v ~/storage/downloads/<TITRE>-<ARTISTE>-9x16.mp4;
curl -L --retry 3 -C - -o ~/storage/downloads/COVER-tiktok-1080x1920.jpg "<url_raw_de_la_cover>"; termux-media-scan -v ~/storage/downloads/COVER-tiktok-1080x1920.jpg
```

---

## 14 — Interdits permanents (union v6.0 + v6.3)

Drapeau, bannière nationale · système de code à 4 chiffres ou accroche « reste jusqu'à la fin pour le code » · contact, lien, QR, logo dans une image · nudité, anatomie exhibée · photo personnelle envoyée au générateur sans autorisation écrite · cursive sur un CTA · calque typo par-dessus une typo déjà peinte/cuite · horodatages de l'artiste modifiés · validation ou mesure inventée · **texte peint par le générateur d'images** (apport v6.3 : NO TEXT AT ALL) · visage caché (masque, capuche, lunettes opaques, texte devant) · badge clignotant vite · badge sans les deux mots ARTISTE + WTBW · **extinction / flou / assombrissement / voile sur les paroles peintes (définitif v6.5, 2026-11-13)** · pilule FR resserrée sous les cotes §5.7 (interlettrage < 6 px, texte > 620 px ou débordant de la pilule, traductions collées) · mot inventé · génération de voix ou de musique.

---

## 15 — Gabarits de prompts d'image

### 15.1 STUDIO ANIME SEINEN N&B (recette par défaut — disposition v6.0, garde-fous v6.3)

```
Vertical 9:16, dark seinen anime cel-shaded illustration in strict BLACK AND WHITE monochrome (pure black ink,
stark white highlights, muted charcoal grey tones, zero color), same anime protagonist and style as the reference
image. The canvas is 768 px wide and 1376 px tall; all coordinates below are on this native canvas.

Framing: half-body shot — exactly ONE character, the same Black male anime protagonist with short stylized locks
and closed high-collar black coat. His head (uncovered, face fully visible, nothing over the forehead) sits between
y 190 and y 400, shoulders between y 400 and y 465, frame cuts his hips at the bottom edge. Expression: <expression
faciale précise du vers>. Behind him, an ATTENUATED, darkened, low-contrast charcoal background of <décor adapté au
vers> (rain, rooftops, alley, crowd silhouettes…), palette strictly black and white — deep jet black #050608,
stark pure white #FFFFFF, soft attenuated charcoal grey #2A2E35 in the background. Keep the middle band around
his torso naturally calm and dark (deep ambient shadow only) so the painted lyrics will be added later by the editor.

IMPORTANT — NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol anywhere in the
image, not on walls, clothing or signs: the background must be pure shapes only.

IMPORTANT — NO HORIZONTAL BAND. One continuous scene: no band, strip, panel, rectangle, seam or gradient line across
the image; the calm torso area is a lighting choice, never a drawn shape.

Between y 782 and y 900, inside x 170 -> 600, paint 2 white ink line-art sticker icons side by side (the only graphic
marks allowed, no letters inside them): a glowing white heart and <symbole>, each about 90 px tall, linked by a thin
luminous white line. The floor continues naturally from the stickers to the bottom edge as one single surface sinking
into deeper shadow, with no seam or line. Nothing in the top 102 px, nothing on the right beyond x 647, nothing below
y 1119. No flag, no logo, no watermark.
```

### 15.2 WANDANCE BATTLE & GRAFFITI LOVES (recette v6.3)

```
Vertical 9:16 street-dance battle anime illustration in the dynamic style of Wandance combined with clean
stylish urban graffiti art, keeping the exact same protagonist and visual style as the reference image.
The canvas is 768 px wide and 1376 px tall; all coordinates are on this native canvas.

Framing: half-body shot — exactly ONE character, his head (uncovered, face fully visible, nothing over the
forehead) sits between y 190 and y 400, his shoulders and arms between y 400 and y 465, and the frame cuts his
hips at the bottom edge. Pose: <pose>. His expression: <expression>. Behind him, an attenuated background:
<décor>; <palette nuit | heure bleue | soleil levant>.

IMPORTANT — NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol anywhere in
the image: the whole spray-painted mural and graffiti background must be pure abstract shapes and colour splashes only.

IMPORTANT — NO HORIZONTAL BAND. One continuous scene: no band, strip, panel, rectangle, frame, seam, colour break
or gradient line running across the image. Keep the décor naturally calmer and darker around his torso (middle
third) as a lighting choice — deep ambient shadow — never as a drawn shape.

Below that calm area, between y 790 and y 900 and inside x 170 -> 600, paint 2 stylish urban graffiti sticker
icons side by side (the only graphic marks allowed, no letters inside them): a glowing street-art heart and <symbole>,
each about 90 px tall, linked by a thin luminous gold line. The floor continues naturally to the bottom edge as one
single surface, slowly sinking into deeper shadow, no seam, no line, no texture change. Nothing in the top 100 px,
nothing on the right beyond x 647, no flag, no logo, no watermark.
```

### 15.3 Couverture TikTok (v6.3)

Même bloc que 15.1/15.2 selon la recette, avec :

```
Framing: a tight heroic bust shot — exactly ONE character. His head is large and centred, between y 300 and
y 720, looking straight into the camera; face fully visible, nothing over the forehead. Shoulders and chest fill
the width between y 720 and y 1180. The area between y 760 and y 1200 must stay a calm, dark, uncluttered zone
of his jacket and deep shadow — that is where the title will be placed later.
... stickers between y 1240 and y 1340 and inside x 170 -> 600 ...
```

---

## 16 — Historique

| version | apport |
|---|---|
| v5.9 (2026-10-14) | « Ça bouge, sans voiler la parole » : question §0, mouvement par fenêtre glissante sur source 110 %, état éteint, grain cyclé, vignette masque L. Validé sur `productions/mahu-ti-te-gbe/` et `productions/on-est-reel/`. |
| v6.0 (2026-10-21) | « WTBW Salut & Stickers Doux » : suppression définitive du code de fin ; accueil 2 temps « Salut · WTBW » + finale sans code animés avec 3 stickers vectoriels doux ; recette STUDIO ANIME SEINEN N&B ; note anti-`ONLY:`. Validé sur `productions/goinfres/` (36 plans, 47 vers, 6 838 frames / 227,933 s, −14,0 LUFS, blackdetect 0, faststart OK). |
| v6.3 | badge clignotant DSKY ↔ WTBW ; couverture TikTok ; le générateur ne peint plus aucun mot (lettrage moteur) ; contour par dilatation ; halo serré ; `dy` par plan ; `EXTINGUISH` off en 100 % FR ; grain par frame + cartes animées (0 gel) ; `MERCI · WTBW`. Validé sur « On nous a volé notre éducation » (50 vers, 40 plans, 9 fenêtres CTA). |
| **v6.5 (2026-11-13)** | **Nettoyage + correctifs mesurés après rejet du rendu** : §5.4 « état éteint » supprimé définitivement (aucun voile sur les paroles peintes, jamais) ; §5.7 pilule FR cotes réelles du rendu (y 1444→1556, 32 px auto-fit ≤ 620 px, tracking 6 px, masquée aux bords intérieurs, anti-collage) ; §3.1 conversion à jour ; badge explicitement « DSKY ↔ WTBW » ; ARTISTE en capitales exactes. Validé sur MONSTER POSITIVE (clip v4, 7 161 f, −14,0 LUFS, 0 frame noire, faststart OK). |
| **v6.4 (2026-11-11)** | **Harmonie v6.0 × v6.3** : squelette, intro, disposition, cartes « Salut · WTBW » 2 temps et recette N&B du **v6.0** conservés ; apports mesurés du **v6.3** intégrés (badge clignotant artiste↔WTBW, couverture TikTok, lettrage moteur 4 correctifs, `EXTINGUISH=False` en 100 % FR, grain 8 motifs/frame + cartes animées, `MERCI · WTBW` + sous-titre « Merci d'avoir écouté », conversion native 768×1376, salves ≤ 8, gabarits NO TEXT AT ALL). Prod en cours : **MONSTER POSITIVE** → `productions/monster-positive/`. |

**Signature :** « Wolof TechStein beat 웨 ! » (WTBW) ⚡


# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v7.0
## « WTBW · IMAGE VIVANTE, PAROLE INTACTE · CLIP + TEASER »

**Version autonome — 2026-11-15.** Ce document suffit à lancer une nouvelle production. Il ne suppose aucun autre prompt, aucun morceau, aucune mesure et aucune validation antérieure. Les valeurs ci-dessous sont des consignes ou des objectifs, pas des résultats mesurés.

---

## 0 — PREMIER CONTACT : LES QUESTIONS AVANT DE PRODUIRE

Avant toute génération ou modification, poser ces questions clairement, en un seul message. Ne pas choisir à la place de l'artiste lorsqu'une réponse est nécessaire.

1. **Paroles :** « Tu veux les paroles déjà peintes dans chaque image, ou en défilement mot à mot par-dessus les images ? »
2. **Couleur :** « Tu préfères des images strictement en noir et blanc ou en couleur ? Si couleur, quelle ambiance ou palette ? »
3. **Peinture :** si les paroles doivent être peintes : « Tu veux que le générateur les intègre directement dans l'image, ou que le moteur les cuise ensuite dans l'image pour mieux garantir l'orthographe ? »
4. **Matière première :** « Où sont l'audio maître et les paroles exactes, avec leurs horodatages si disponibles ? Quel est le titre exact et le nom d'artiste exact à afficher ? » Vérifier d'abord les fichiers du dépôt ou ceux déjà fournis avant de redemander.
5. **Direction :** « As-tu une référence visuelle, un personnage ou une ambiance à respecter ? Sinon, je te proposerai une ancre. » Ne jamais envoyer une photo personnelle au générateur sans autorisation explicite.
6. **Habillage :** « Souhaites-tu le filet de progression, un bandeau de messages défilants, les deux ou aucun ? Les trois stickers WTBW te conviennent-ils ? » Ne jamais supposer que « ce qui défile » signifie les paroles.
7. **Livrables :** « Je prépare un clip complet et un teaser séparé de 15 secondes : quel passage veux-tu pour le teaser ? Veux-tu comparer plusieurs versions ? » Si l'artiste ne connaît pas le passage, proposer un extrait identifiable et préciser qu'il est provisoire.

Si l'artiste dit « les deux » à la question 1, demander s'il veut **une seule vidéo hybride** ou **deux versions distinctes**. Pour une vidéo hybride, demander explicitement ce qui défile : traduction ou paroles originales, et où. Ne pas superposer le même vers sur lui-même ni masquer des paroles peintes. Si une traduction n'est pas demandée ou si rien n'est à traduire, aucune pilule de traduction n'est nécessaire.

**Defaults seulement lorsque l'artiste laisse le choix :** mode peint par moteur ; noir et blanc seinen ; filet et messages discrets ; un clip complet, une couverture et un teaser de 15 s. Les choix explicites de l'artiste priment sur ces valeurs. Si le choix du mode, de la couleur ou de la méthode de peinture reste ambigu, demander au lieu de prétendre qu'il a été validé.

---

## 1 — HIÉRARCHIE ET ÉTATS DE PRODUCTION

1. Demande explicite actuelle de l'artiste.
2. Choix déjà validés pour le morceau : titre, artiste, source audio et paroles, mode, méthode de peinture, couleur, personnage et référence.
3. Ce document, pour tout ce qui n'est pas contredit.

**Priorités permanentes :** exactitude des mots et du sens > audio de l'artiste intact > lisibilité des paroles et visage dégagé > synchronisation > esthétique > ornements. L'élément le moins prioritaire cède. Toute exception demandée explicitement par l'artiste est consignée.

Distinguer : **proposé**, **généré**, **validé par l'artiste**, **rendu**, **contrôlé** et **livré**. Une image sélectionnée n'est pas nécessairement une validation technique ; un fichier existant n'est pas nécessairement conforme. Ne jamais inventer un résultat, une mesure, une approbation, un hash publié ou un fichier final.

---

## 2 — FICHE DE PRODUCTION À REMPLIR

```text
TITRE EXACT              : …
ARTISTE À L'ÉCRAN        : …                         (orthographe et capitales validées)
LANGUES                  : …
PAROLES ET HORODATAGES   : chemin/fichier             (sources conservées)
AUDIO MAÎTRE             : chemin/fichier             (fourni par l'artiste)
PAROLES AFFICHÉES        : exactes / exceptions explicitement autorisées et listées
MODE                     : PEINT / DÉFILEMENT / HYBRIDE PRÉCISÉ
PEINTURE                 : GÉNÉRATEUR / MOTEUR / sans objet
COULEUR                  : NOIR ET BLANC / COULEUR + palette
STYLE                    : …
PERSONNAGE / ANCRE       : proposé / généré / validé : …
INTRO / OUTRO            : …
FILET                    : oui / non
BANDEAU DÉFILANT         : oui / non ; texte : …
STICKERS / CTA           : …
TEASER                   : 15,00 s ; extrait source [début, fin] : … ; proposé / validé
VERSIONS                 : nombre et différences prévues : …
DOSSIER                  : productions/<titre>/
```

**WTBW s'écrit uniquement « WTBW » dans l'habillage, sauf instruction explicite contraire de l'artiste.** Ne pas le développer automatiquement dans l'intro, l'outro, les bandeaux, les CTA, la couverture ou le badge. Si la chanson prononce un développement de WTBW, demander si les paroles affichées doivent être fidèles à l'audio ou remplacées par « WTBW ». Consigner l'exception ; ne jamais modifier l'audio pour la faire correspondre.

---

## 3 — SOURCE, CALAGE ET CONTRAT DES VERS

- Utiliser l'audio maître réel fourni par l'artiste : ne jamais générer, rejouer, remplacer ou réinterpréter voix ou musique. Une conversion de format est une opération d'encodage, à déclarer ; elle ne doit pas changer le contenu musical. Préserver la source originale.
- Lire les paroles dans leur fichier, conserver les accents, apostrophes, ponctuation et horodatages fournis. Une différence d'affichage autorisée doit être enregistrée séparément, sans modifier la transcription source.
- Créer un contrat unique `verses_map.json`, généré depuis les sources et traçable. Champs minimum : `i`, `debut_source`, `fin` (ou `null`), `texte_source`, `texte_affiche`, `image`, `disponible`, `reprise`, `statut_controle`. Recalculer `disponible` à partir des fichiers présents. Générer `CARTE-VERS.md` depuis ce contrat.
- **Un vers distinct = une image dédiée** en mode peint ; une reprise identique peut réutiliser son image si l'artiste n'exige pas une image nouvelle pour chaque occurrence. Après le passage vers l'aube, produire des variantes d'aube pour les reprises concernées. Ne jamais combiner arbitrairement plusieurs vers sur une seule image en mode peint.
- Garder les débuts fournis intacts. Les fins de vers ne sont pas nécessairement les débuts suivants : identifier les syllabes tenues et les respirations en écoutant ou en contrôlant le signal ; ne pas inventer une fin. Si elles restent inconnues, les noter `null` et signaler le calage comme provisoire.
- Si l'artiste ne fournit pas de calage mot à mot, toute estimation doit être déclarée. Formule indicative d'affichage : `min(fin_vers − début_vers, max(2,2 s, 0,30 s × nombre_de_mots))`, utilisable seulement lorsque la fin est connue. Elle ne remplace pas l'écoute.
- Aucun CTA pendant une syllabe tenue. La durée du clip complet = durée **décodée mesurée** du morceau + 5,00 s de carte finale, sauf décision explicite différente.

---

## 4 — FORMAT ET ZONES DE SÉCURITÉ TIKTOK

Sortie de référence : **1080 × 1920**, portrait 9:16, 30 i/s, pixels carrés. Toutes les scènes d'une même production sont normalisées à la même résolution sans déformer le personnage ni couper les mots. Conserver les originaux.

- Zone supérieure de sécurité : `y < 144` libre de texte et éléments essentiels.
- Zone droite à éviter : `x ≥ 910` entre `y = 960` et `y = 1690`.
- Aucun élément essentiel sous `y = 1574`.
- Paroles centrées, largeur cible **≤ 740 px**, dans `y = 620 → 1340`. Visage dégagé, idéalement dans `y < 560`. Aucun lettrage, bandeau, icône ou effet ne couvre le visage ou les paroles.
- Si les sources ne sont pas au bon ratio, recadrer seulement si aucune parole, tête ou élément essentiel n'est coupé. Sinon, adapter le fond ou conserver l'image entière avec marges et **déclarer** le compromis ; ne pas étirer l'image pour faire disparaître les marges. Contrôler la vidéo finale, pas seulement l'image source.
- Pour une source native **768 × 1376**, le facteur de conversion largeur est `768/1080 ≈ 0,7111` : marge haute 102, visage 398, bande texte 441–953, limite basse 1119, droite interdite 647, largeur texte 526 px. La sortie 9:16 impose un léger recadrage vertical : ancrer en haut et vérifier la tête et les éléments utiles. Les coordonnées ne s'appliquent pas aveuglément à d'autres dimensions.
- Tenues fermées, visage visible, personnages fictifs ; pas de drapeau national, bannière nationale, QR code, coordonnées, lien ou logo dans les images. Un **bandeau de messages** demandé par l'artiste est autorisé : il n'est pas un drapeau ni une bannière nationale et doit rester discret et lisible.

---

## 5 — STYLE VISUEL ET ANCRE

### Noir et blanc
Anime seinen, encre noire franche, blancs nets, gris d'encre, décors atténués et expressions variées. **Aucune couleur** si le noir et blanc strict a été choisi. Personnage, coupe de cheveux et tenue restent cohérents d'un plan à l'autre. Arc lumineux : ombre/nuit → premières lueurs → aube lumineuse, sans retour arbitraire en arrière.

### Couleur
Choisir et noter avec l'artiste une seule palette cohérente pour le morceau. Exemples à proposer, jamais à imposer : encre bleu nuit / ambre / crème ; aube claire ; battle urbain cyan et or. Conserver la lisibilité et la progression lumineuse, sans faire dériver les couleurs du personnage entre plans.

### Ancre et salves
1. Générer une **seule ancre de référence**, vérifier visage, style, cadrage et orthographe si elle comporte une parole. Demander la validation du personnage et du style avant les salves.
2. Salves de **8 images maximum** par tour ; consigner demandées, réussies et échouées. Utiliser l'ancre validée comme référence pour chaque scène.
3. Un échec de génération est un échec, pas un fichier livré. Une image anatomiquement incorrecte, avec personnage en trop, texte non demandé ou mot erroné est régénérée.

---

## 6 — PAROLES DANS LES IMAGES : DEUX MÉTHODES, UN CHOIX

### A. Peintes directement par le générateur
Utiliser uniquement si l'artiste l'a choisi. Le prompt demande **un seul vers exact**, sans autre mot, les accents et la ponctuation inclus. Contrôler chaque mot et chaque caractère sur image pleine résolution et sur le rendu ; le générateur peut inventer, répéter, oublier ou mal positionner du texte. Tout défaut impose une nouvelle génération du plan. **Ne jamais prétendre que l'orthographe est garantie.**

### B. Cuites par le moteur après génération
Le générateur reçoit `NO TEXT AT ALL` : aucun mot, lettre, chiffre, logo, filigrane ou marque typographique. Le moteur ajoute ensuite le vers exact dans l'image, de manière permanente, avant montage. Il ne pose jamais une nouvelle typographie sur des paroles déjà peintes par le modèle.

Pour le lettrage moteur : contour par dilatation du masque placé derrière les glyphes, non par remplissage des contre-formes ; glyphes espacés et tournés individuellement avec rotation faible ; halo serré ; position verticale ajustée au besoin pour éviter le visage. Vérifier lettres, contre-formes et diacritiques en 1:1. Une retouche exceptionnelle limitée à un diacritique doit être déclarée ; une erreur de mot implique une correction complète et un nouveau contrôle.

### C. Défilement ou hybride
Le défilement utilise un calque lisible et synchronisé, largeur ≤ 740 px, sans sticker dans la zone de sous-titres. Un mot actif peut être mis en valeur si le calage mot à mot est réel ; sinon signaler l'estimation. Pour une traduction demandée : une pilule maximum, `x 186 → 894`, `y 1444 → 1556`, largeur utile ≤ 620 px, texte centré, espacement au moins 6 px et auto-ajustement. Ne pas cacher ou doubler les paroles peintes. Aucun mélange de modes d'un vers à l'autre sans accord de l'artiste.

---

## 7 — MOUVEMENT : PLUS VIVANT, JAMAIS AU DÉTRIMENT DES MOTS

- Le principe est **l'image vit, le mot reste net**. Aucun flou, extinction, assombrissement, plaque ou voile sur les paroles, pendant qu'elles sont chantées **ni après**, dans aucun mode. Seuls les fonds des cartes d'intro/outro peuvent être floutés.
- Préparer une image agrandie une seule fois par plan ; faire glisser une fenêtre de recadrage sans double exposition ni redimensionnement par frame. Quatre trajectoires alternées et douces ; pas de rotation, secousse, zoom brutal ou bord noir découvert. Une amplitude jusqu'à 10 % est indicative, jamais une autorisation de couper une lettre, un visage ou la zone sûre. Réduire l'amplitude ou adapter le fond si nécessaire.
- Un déplacement perceptible sur les plans longs, des détails vivants et un rythme visuel pensé sur la musique valent mieux qu'un simple habillage immobile. Les animations doivent rester élégantes, pas mécaniques ni agressives.
- Cœurs vectoriels qui se dessinent progressivement, pulsations, étincelles ou traits lumineux : placer hors visage et hors texte, avec trajectoires douces. Varier les mouvements et vérifier sur la vidéo réelle. Aucune animation ne peut voler la lecture.
- Coupes franches entre plans ; fondu uniquement lorsque les paroles restent lisibles et que les timings ne sont pas brouillés. Grain éventuel de motifs cycliques déterministes : jamais une couche qui salit, voile ou dédouble les lettres. Les fonds des cartes peuvent recevoir davantage de mouvement et de grain.
- Un fichier détecté comme gelé n'est pas « zéro gel », même si un détail bouge à l'œil. Relever les intervalles, les visionner, améliorer si nécessaire, puis publier les mesures réelles.

---

## 8 — INTRO, OUTRO ET HABILLAGE WTBW

### Intro
Durée : de 0 au premier vers, sans déplacer l'horodatage de l'artiste. Si cet intervalle est court, adapter le rythme au temps réellement disponible ; ne pas couper une syllabe pour allonger la carte.

Proposer une ouverture cinématographique propre : titre exact, artiste exact, filet fin, apparition progressive et cœur qui se dessine, suivis si le temps le permet de `SALUT · WTBW` puis `BIENVENUE SUR WTBW`. S'inspirer d'une référence validée pour son rythme et sa finition sans copier une photo ou un élément personnel sans autorisation. Trois stickers vectoriels animés, si souhaités : `LIKE LA VIDÉO`, `CLIQUE SUR + POUR T'ABONNER`, `COMMENTE SI TU AIMES !`. Les sous-textes n'expliquent pas WTBW. Aucun code de rétention, aucun lien.

### Outro
À la fin du morceau : **5,00 s** de carte `MERCI · WTBW`, titre et artiste, avec les mêmes stickers et animations, sans code, coordonnées ni lien. Adapter aux préférences validées de l'artiste.

### Badge
Hors cartes et CTA, alterner `<ARTISTE>` ↔ `WTBW`, à l'orthographe exacte, en haut sans couvrir le visage. Référence : 2,4 s par mot, fondu croisé de 0,4 s, opacité ≤ 0,72, entrée/sortie douces. Pas de clignotement rapide. Vérifier que les deux noms sont réellement lisibles, notamment pendant les fondus.

### Filet de progression
Si demandé, prévoir un filet allant de `x = 170` à `910`, proportionnel au temps écoulé entre premier vers et fin du morceau. Position indicative `y = 1560`, **seulement si elle ne croise ni texte ni sticker**. Si elle gêne la lecture, déplacer le filet dans une zone sûre dégagée, par exemple sous le badge en haut si le visage le permet, ou masquer localement le filet ; déclarer l'adaptation. Ne jamais tracer une ligne sur un mot pour respecter une cote.

### Bandeau de messages défilants
Si demandé, faire défiler des messages courts (`LIKE`, abonnement, commentaire, `WTBW`) dans une bande transparente ou un espace naturellement calme ; masquer aux limites latérales, garder un contraste suffisant et une vitesse lisible. Éviter les visages, paroles, badge et commandes TikTok ; aucun lien, code ou expansion automatique de WTBW. Ne pas confondre ce bandeau avec des paroles défilantes.

### CTA clochette
Uniquement si demandé et dans une fenêtre **effectivement sans parole**, après vérification des fins réelles et syllabes tenues. Pas de CTA sur les cartes ni sur des paroles ; pas de plaque qui neutralise un texte peint. Cloche vectorielle, mouvement amorti, texte lisible, apparition et sortie douces. Maximum indicatif 9 fenêtres. Si aucune fenêtre sûre n'est confirmée, ne pas en inventer.

---

## 9 — COUVERTURE TIKTOK

Créer une image dédiée, distincte d'une frame du clip : personnage unique, regard caméra, visage dégagé, style/palette validés. Le générateur ne peint aucun mot sur cette couverture ; ajouter ensuite le **titre exact**, l'**artiste exact** et `WTBW` par moteur. Format JPEG 1080×1920, qualité élevée, 4:4:4 si disponible. Contrôler à 1:1 : titre dans `x 90 → 990`, aucun caractère coupé, aucun texte sur le visage. Pas de drapeau, lien, QR ou logo.

---

## 10 — TEASER SÉPARÉ DE 15 SECONDES

Le teaser est une **vidéo à part**, en 1080×1920, 30 i/s, **450 frames / 15,00 s**, avec un extrait réel du maître audio. Ce n'est pas simplement un fichier tronqué sans intention : construire une accroche visuelle lisible, conserver le personnage, proposer une dynamique adaptée au passage et une fin propre. Une sélection de refrain peut être proposée ; noter son intervalle source exact et demander validation lorsque nécessaire.

Ne pas couper arbitrairement au milieu d'un mot ou d'une syllabe : choisir les bornes par écoute. Si un extrait exact de 15 s impose une coupure, proposer un autre passage, un silence naturel ou demander l'accord de l'artiste. Ne pas générer de voix, musique, bruitage ou effet sonore. Un extrait peut nécessiter un réencodage AAC : le signal vient toujours du maître, et l'opération est déclarée. Les paroles et zones sûres sont contrôlées à nouveau sur le teaser ; aucun ornement ne les couvre.

---

## 11 — SON, ENCODAGE ET CONTRÔLES

### Audio
Avant d'annoncer un résultat, mesurer le maître : durée décodée, LUFS intégré, crête vraie, LRA et silences, en mentionnant l'outil. Si un master MP3 séparé est demandé, utiliser `loudnorm` deux passes linéaires lorsque applicable, cible indicative `I=-14:TP=-1.5:LRA=11`, 48 kHz, stéréo, MP3 CBR 320 kb/s, `-vn`, tags corrects et relus. Signaler si la normalisation réelle ne peut pas être linéaire ou n'atteint pas la cible. Ne pas dire « audio intact » au sens binaire lorsqu'il est normalisé ou réencodé : dire que le contenu musical d'origine est conservé et préciser les traitements.

Pour la vidéo complète : source audio de l'artiste + silence pour l'outro, AAC 256 kb/s / 48 kHz, sans ajouter de son. Le teaser peut avoir un LUFS différent du morceau entier ; mesurer plutôt qu'inventer.

### Vidéo
Cible : H.264 `libx264`, `yuv420p`, 1080×1920, pixels carrés, 30 i/s, BT.709, qualité adaptée à la complexité. La taille du fichier n'est pas une fin en soi : privilégier la netteté des mots et la fluidité. Éviter les passes et réencodages inutiles. `+faststart`, vérifier l'ordre `moov` avant `mdat`. Si un procédé en pipe empêche le faststart, faire un remux `-c copy -movflags +faststart` et vérifier.

### Contrôles obligatoires, avec chiffres du fichier réel
- Durée, nombre de frames, dimensions, cadence, pixels carrés et format audio/vidéo.
- `blackdetect=d=0.05:pix_th=0.10` et `pix_th=0.98` : rapporter les intervalles détectés. Le second seuil est très sévère sur du noir et blanc sombre ; examiner les intervalles, ne pas les qualifier automatiquement de frames entièrement noires.
- `freezedetect=n=-33dB:d=2.5` : publier le nombre et les intervalles détectés ; inspecter les vers, cartes et CTA, et améliorer si nécessaire. Ne jamais affirmer zéro sur la base d'une intention.
- `ebur128` : LUFS intégré, LRA et crête vraie pour chaque livrable audio/vidéo. Vérifier `moov` avant `mdat`.
- Feuille contact de tous les plans avec tuiles ≥ 480 px de large ; crops pleine résolution 1:1, avec repères de grille au besoin ; images extraites du MP4 final ; contrôle d'orthographe, accents, visage, surimpressions, marges et mouvement. Contrôler **chaque vers**, pas seulement quelques échantillons. Vérifier séparément le teaser et la couverture.
- Vérifier l'audio et le calage à l'écoute ; consigner les parties non vérifiées. Si une exigence reste non satisfaite, la nommer et ne pas appeler le rendu pleinement conforme.

---

## 12 — LIVRAISON, GIT ET TERMUX

Travailler uniquement sur la branche de session. Sauvegarder l'avancement par étapes si l'artiste le demande. Ne jamais inventer un push, une mesure ou un SHA. Vérifier la branche publiée avec `git ls-remote`, et l'existence et la taille des fichiers avec l'API GitHub avant de donner des liens. Les fichiers dépassant 50 Mo ne vont pas dans un commit ordinaire sans le signaler ; au-delà des limites GitHub, utiliser une release ou un stockage approprié. Les liens de téléchargement sont figés sur le SHA publié, pas sur une branche mouvante.

À la livraison, dans cet ordre :
1. **Titre et artiste exacts.**
2. **Caption(s)** et au plus 13 hashtags.
3. **Clip complet, teaser 15 s, couverture** : présenter les fichiers, préciser les versions et ce qui les différencie.
4. **Déclaration IA** : visuels oui/non, audio fourni ou généré, et traitements audio réellement effectués.
5. **Contrôles et limites réels** : durées, images, audio, noir, gel, faststart, typo et zones sûres ; distinguer non mesuré, défaut et conforme.
6. **Commandes Termux** vérifiées : une ligne par fichier, avec `curl -L --retry 3 -C - -o ...` puis `termux-media-scan -v ...`, URLs figées sur le commit publié. Donner les commandes pour les deux vidéos et la couverture si demandée.
7. En cas de demande, livrer aussi le prompt universel autonome mis à jour et les scripts nécessaires à la reproduction.

Installation initiale si nécessaire :

```sh
pkg install -y curl && termux-setup-storage
```

La réponse doit rester honnête : si l'artiste veut choisir entre plusieurs versions, ce sont des **versions à comparer**, pas des validations qu'il n'a pas encore données.


