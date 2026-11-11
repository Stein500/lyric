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
