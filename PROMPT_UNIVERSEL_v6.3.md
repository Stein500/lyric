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
