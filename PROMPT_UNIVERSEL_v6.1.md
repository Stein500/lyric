# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v6.1
## « WTBW SALUT & STICKERS DOUX — ÇA BOUGE, SANS VOILER LA PAROLE »

Mise à jour : **2026-10-25 (v6.1)**. Document **100 % auto-suffisant** : il intègre l'intégralité du moteur v5.9 et le remplace par les directives officielles v6.0, **corrigées de leur incohérence d'auteur** (§18).

**Signature d'écran de l'artiste : `Dsky` — et RIEN d'autre.**
Le nom `Daïsky` / `DAÏSKY` est **retiré définitivement** de tous les prompts, prompts d'image, cartes, badges, tags ID3, métadonnées et livraisons. Les fichiers historiques qui portent encore l'ancien nom dans leur *nom de fichier* sont conservés tels quels (traçabilité), mais **aucune chaîne affichée** ne doit le contenir. Écritures autorisées : **`Dsky`** (cartes, badge, titres) et **`DSKY`** (lettrage capital, hashtags). Interdit : `Daïsky`, `DAÏSKY`, `daisky`.

---

## 0 — LA QUESTION À POSER AVANT TOUT (obligatoire, premier message de l'agent)

> **« Tu veux les paroles en DÉFILEMENT (texte posé par le montage, qui défile mot à mot) ou DÉJÀ PEINTES DANS L'IMAGE (le modèle écrit la parole dans la matière de chaque visuel) ? »**

- pas de réponse → **MODE PEINT** par défaut, et le dire ;
- « défilant » → **MODE DÉFILEMENT** ;
- « les deux » / « hybride » → **PEINT (VO) + TRADUCTION FR DÉFILANTE** — la couche défilante **ne s'active que sur les vers dont la langue n'est pas le français** (§5.7). Sur une chanson 100 % française, la pilule de traduction reste **dormante** : le mode est dit « PEINT (hybride prêt) ».

| | **MODE PEINT** | **MODE DÉFILEMENT** | **HYBRIDE BILINGUE** |
|---|---|---|---|
| Texte écran | peint **dans l'image** ; aucune typo incrustée hors cartes | calque PIL, bloc ≤ 740 px, mot actif en avant | VO peinte (`y 650→1040`) + **traduction FR défilante** (`y 1452→1545`) |
| Stickers | 1 à 3 par image | interdits dans l'œuvre | 1 à 2 sous la VO (`y 1100→1280`) |
| Plans | **1 plan par vers distinct** + variantes d'aube (§9) | 1 plan / 2–3 vers | 1 plan par vers + variantes d'aube |
| Accentuation | aucune sur-typo | halo 3 px + `spaced()` | mot actif FR or chaud `#FFE07A` + halo 3 px |
| Fin de vers | le plan s'éteint (§5.4) | mot à mot | VO + FR mot à mot, puis extinction (§5.4) |

Choix **verrouillé** pour toute la prod : jamais de mélange entre vers.

---

## 1 — Hiérarchie des demandes

1. Demande explicite actuelle de l'artiste.
2. Configuration validée de la prod (ancre, personnages, titre exact, style, palette).
3. **v6.0 (ce document)**.
4. v5.9 → v5.5 pour tout ce qui n'est pas contredit.

États tenus séparés : **proposé / généré / validé par l'artiste / rendu / contrôlé**.
**Jamais** inventer : validation, hash, mesure, fichier final, « à peu près ».

---

## 2 — Paramètres de la prod (bloc à remplir à chaque chanson)

```
TITRE        : …                      (recopié EXACTEMENT, accents compris)
ARTISTE      : Dsky                   (jamais « Daïsky »)
LANGUES      : …                      (si non français : le dire au générateur + traduction FR défilante)
PAROLES      : chemin/fichier.txt     (N lignes = N vers, horodatages de l'artiste NON retouchés)
AUDIO        : chemin/fichier.mp3/m4a (maître fourni, jamais généré)
RECETTE      : STUDIO ANIME SEINEN N&B DÉCORS ATTÉNUÉS | WANDANCE BATTLE & GRAFFITI LOVES | ENCRE & FEUILLE D'OR | AUBE CLOCHETTES
HABILLAGE    : WTBW SALUT + STICKERS DOUX (Like · Clique sur + pour t'abonner · Commente si tu aimes) — SANS CODE
SIGNATURE    : « Wolof TechStein beat wê ! » (WTBW)
MODE         : PEINT (défaut) | DÉFILEMENT | PEINT (VO) + TRADUCTION FR DÉFILANTE
DOSSIER      : productions/<slug>/    (fonds/ livrables/ fonts/ audio/ + verses_map.json + CARTE-VERS.md)
```

---

## 3 — Zones sûres 1080×1920 (à recopier dans CHAQUE prompt d'image)

- rien dans les **144 premiers pixels** en haut ;
- rien à droite de **x ≥ 910** entre **y 960 et y 1690** (bouton `+` + pavé TikTok) ;
- rien en dessous de **y = 1574** ;
- bloc de texte **centré, largeur ≤ 740 px**, bande **y 620 → 1340** ; en bilingue : VO **y 650 → 1040**, stickers **y 1100 → 1280**, pilule FR **y 1452 → 1545** ;
- **la typo ne couvre jamais un visage** : visage dans la moitié haute (`y < 560`), rien pour le cacher (ni masque, ni capuche sur les yeux, ni lunettes opaques, ni texte) ;
- **jamais de drapeau, bannière, contact, lien, logo, ni code** dans l'image ;
- sortie native du générateur = **768×1376** → 1080×1920 **ancré en HAUT**, rognage du bas, **le crâne n'est jamais coupé** ;
- tenues fermées et élégantes, visage dégagé, aucune nudité, personnages fictifs uniquement (sauf figures historiques ou photos expressément autorisées).

---

### 3.1 Conversion obligatoire 1080×1920 → natif 768×1376 (facteur **0,7111**)

Les zones §3 sont écrites en 1080×1920 (le rendu). Le générateur, lui, sort du **768×1376** : **tout prompt d'image doit être exprimé dans le repère natif**, sinon le bloc descend de 40 % et les stickers tombent sous `y = 1574` (échec réellement constaté le 2026-10-25).

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

**Cadrage obligatoire (correctif v6.1)** : front à `y ≥ 190`, tête `190→400`, épaules `400→465`, **plan mi-corps**,
buste quittant le bord haut du crop à `1080` (haut du buste visible `y ≈ 165→260`) ⇒ les animations de carte
(badge `y 146→184`, en-tête `y 236`) ne passent **jamais** sur le visage.

**Calibrage typographique natif** : `hauteur de capitale ≈ min(46 ; 505 / (0,66 × nb_caractères))` px — une ligne de 22 caractères tombe à ≈ 34 px, une ligne de 9 caractères à ≈ 46 px. Cadrage recommandé : **plan mi-corps** (tête en `y 120→380`, épaules et bras levés `380→470`, hanches au bord bas), la bande peinte `470→750` passe sur le torse et le décor assombri.

## 4 — Orthographe : règle, pièges, droit de retouche exceptionnel

- recopier le vers **exact** dans le prompt, entre guillemets, sur **2 lignes équilibrées** ;
- **nommer les diacritiques** (`É È Ê À Â Ô Û Ï Ç Œ`) et exiger leur présence ;
- **calibrer la taille** : à 768×1376, chaque capitale peinte ≈ **52–62 px** de haut, deux lignes maximum, bloc entier dans `x 190 → 880` — **c'est la première cause d'échec** (texte qui déborde ou se coupe) ;
- éviter `ONLY:` / `EXACTLY:` juste devant les guillemets (le modèle les peint) ;
- relire chaque plan sur **contact sheet ≥ 480 px de large** (`500×896 px`/tuile) **ET** sur **planche de crops 1:1 avec grille de 16 px** (`CONTROLE-salveN-typo.jpg`) ;
- texte faux / mot omis / mot doublé / débordement → **régénérer avec un prompt court et explicite** ;
- **retouche exceptionnelle** : après 2 échecs, s'il ne manque **qu'un diacritique**, le combler en **copiant le glyphe déjà peint dans la même image** (patch ≤ 30 px, masque = pixels du glyphe, MaxFilter 3 + flou 0,9), jamais en recomposant un caractère à la police ; **déclarer** la retouche ;
- `STOP` / `MAX_TOKENS` = **échec consigné**, jamais compté comme livré.

---

## 5 — MOUVEMENT : animer sans voiler la parole

> **L'image vit, le mot reste lisible. Le mouvement est une fenêtre qui glisse, jamais une échelle qui change.**

### 5.1 Préparation (une fois par plan)
- Source native **768×1376** → agrandie en LANCZOS à **1188 × 2128** (= `1080 × 1,10`), une seule fois, puis **deux** images en cache : la nette et l'« éteinte » (§5.4).
- Marge de travelling disponible, calculée (et non plus approximée) : **108 px en x**, **208 px en y**.
- **Aucun resize par frame** : `Image.blend(base, zoom, u)` dédouble les lettres peintes (ghosting visible au zoom 1:1).

### 5.2 Le travelling
- frame = `big.crop` d'une fenêtre **1080×1920** dont l'origine glisse de `(ax0,ay0)` à `(ax1,ay1)` selon l'avancement `u` du vers ;
- **4 trajectoires** alternées par parité (`si % 4`), exprimées en déplacement **centré** (`fx,fy ∈ [-1,1]`) :
  `(-1→1,-1→1)` · `(1→-1,-1→1)` · `(-0,6→0,6,1→-1)` · `(0,6→-0,6,-1→1)` ;
- **1 travelling = 1 vers**, durée = durée du vers (cycle cosinus `2,2 s` si `durée > 3,5 s`) ;
- **amplitude plafonnée à la BANDE, pas à la marge** (correctif v6.1) : `XR = 45 px`, `YR = 40 px` autour du
  centre de la marge. La marge réelle est de 108 px en x / 208 px en y, mais un déplacement latéral de 108 px
  *coupe la typo peinte* (bloc natif `x 150→590`, rideau gauche du crop final à `x 84`) et un déplacement
  vertical de 208 px *coupe le front* (visage natif dès `y 190`). L'ancienne règle « amplitude = marge » était
  fausse : elle garantissait l'absence de bord noir mais **décapitait le personnage** ;
- aucun bord noir découvert, la bande `y 620→1340` jamais coupée, **le crâne et le front jamais coupés** ;
- pas de rotation, pas de shake, pas de zoom brutal.

### 5.3 Transitions
- `xfade` **0,35 s**, uniquement **entre deux segments**.

### 5.4 État « éteint » d'un vers déjà lu
- après `disp` et si le plan court encore (respiration `> 1,0 s`) : la bande centrale `y 620→1340` passe à **Brightness 0,38 + GaussianBlur 3**, en fondu de **0,35 s**, `Image.blend(nette, eteinte, g)` avec `g = min(1, (t − disp)/0,35)` — même fenêtre que l'image nette : zéro ghosting, zéro gel.

### 5.5 Grain et vignette
- **vignette** : masque `L` centré (0 au centre, ≈ 86 aux coins, flou 34), `Image.composite` d'un `#04080C` — jamais `Image.blend`.
- **grain 35 mm** : **4 variantes pré-calculées** cyclées (`grains[(k // 2) % 4]`, seed fixe) sur `Brightness 1.09`.

### 5.6 Calage
- horodatages de l'artiste **gardés tels quels** ; durée du clip = durée **décodée** de l'audio + `5,00 s` de carte finale ;
- sans calage mot à mot : `affichage = min(fin_vers − debut_vers, max(2,2 s ; 0,30 s × nb_mots))`, **signalé provisoire** ;
- segment long (`> 3,5 s`), ponts, cartes : travelling cyclé cosinus `2,1–2,2 s` + respiration lumineuse `±12 %` (période `1,7 s`) ⇒ **0 segment gelé** à `freezedetect=n=-33dB:d=2.5`.

### 5.7 Traduction française défilante (passages non français)
Pilule `708 × (20 + N_lignes × 34..38)` px, `radius 24`, `x 186 → 894`, `y 1452 → 1545`, plaque `(8,12,18,222)`, liseré or `(244,197,98,185)` 2 px, barre karaoké 3 px `#FFDE76`, glissement `±9 px` (`dx = round((0,5 − u)·18)`), mot actif **or chaud `#FFE07A`** + halo 3 px + pastille `(244,197,98,52)`, mots passés `#F4F7FC`, mots à venir `(175,190,210,158)`, entrée 0,22 s / sortie 0,35 s.
`verses_map.json` porte `"langue"` (`FR`, `EN`, `ES`, `EN+ES`, `WTBW`) et `"traduction_fr"` ; **vide** pour `FR` et `WTBW` ⇒ **aucune pilule**.

---

## 6 — Clochettes / CTA pendant les respirations

- fenêtre = `[fin d'affichage du vers + 0,15 s → début du vers suivant]`, seuil **4,0 s** (PEINT) / **5,0 s** (DÉFILEMENT) ;
- **jamais** sur les cartes, ni pendant un vers ;
- tile **720×720**, centrée `x=540`, `y 620→1340` ; plaque `rounded_rectangle([34,8,686,712], r=54)` flou 4 **sous** les éléments ;
- cloche **vectorielle** (pas d'emoji) : silhouette à doucine + **jupe évasée**, anse et battant, 36 angles supersamplés ×3, pendule `±12°` amorti, période `4,0 s`, halo flou 18, 2 ondes (0,9 s), 3 étincelles, **flèche clignotante AU-DESSUS de la cloche** (`y 300→334`, correctif v6.1 : sous la cloche elle tombait sur le `+` du titre) ;
- **plaque à α 244** (correctif v6.1 : à 196 la typo peinte « éteinte » traversait le CTA) ;
- textes Montserrat : `CLIQUE SUR +` (56 ExtraBold, +5 px), pilule `LIKE & PARTAGE` 420×96, rappel `Commente si tu aimes · WTBW` (30 SemiBold) ;
- fondus 0,35 s aux deux bouts.

---

## 7 — Habillage permanent v6.0

### 7.1 Zéro code
Interdit : « Regarde jusqu'à la fin / la durée c'est le code » ; code à 4 chiffres ; « Commente le code ».

### 7.2 Carte d'accueil « SALUT · WTBW » en 2 temps
Fond = plan du 1er vers à `1,10×`, **`GaussianBlur 9`, `Brightness 0,72`, scrim 0,55** (correctif v6.1 : à `flou 4 / 0,80` la typo peinte du 1er plan concurrençait la carte et descendait dans la zone TikTok), glissement continu ; filets `x 170→910` en `y 310` et `y 1470`.
- **En-tête** : `WTBW · WOLOF TECHSTEIN BEAT WÊ !`
- **Temps 1** (flottement ±10 px) : `SALUT · WTBW` / `Wolof TechStein beat wê` / plaque `<TITRE> — DSKY`
- **Temps 2** : `BIENVENUE SUR WTBW` / `Soutiens le son en douceur :` / `<TITRE> · DSKY`
- **3 stickers vectoriels** (`y = 845, 1045, 1245`, pilules `700×144` à `radius 52`, texte auto-ajusté : la taille descend jusqu'à tenir dans `508 px` de large — sinon « CLIQUE SUR + POUR T'ABONNER » débordait), flottement `dy ±12`, `dx ±14` (périodes `1,8–2,1 s`), icônes supersamplées ×3 en respiration `±5 %` (`1,4 s`) :
  1. **LIKE** — cœur vectoriel — `LIKE LA VIDÉO` · « Laisse un cœur si tu valides »
  2. **+ S'ABONNER** — bouton `+` vectoriel — `CLIQUE SUR + POUR T'ABONNER` · « Rejoins Wolof TechStein beat wê »
  3. **COMMENTER** — bulle vectorielle — `COMMENTE SI TU AIMES !` · « Dis-nous ton vers préféré »
- **Bornage** : `t0` = début du premier **vers chanté** ; la **signature `WTBW` d'ouverture** fait partie de la carte (elle EST son en-tête) — elle n'est pas redoublée en plan peint.

### 7.3 Carte finale « MERCI · WTBW » (`fin_chanson → +5,00 s`) — sans code
Fond = dernier plan `1,10×` en glissement ; en-tête, `MERCI D'AVOIR ÉCOUTÉ !`, `Wolof TechStein beat wê (WTBW)`, `<TITRE> · DSKY`, **les 3 mêmes stickers**. Aucun code, contact, lien, logo.

### 7.4 Badge & filet de progression
- **Badge `Dsky`** : `y 146→184`, Montserrat ExtraBold 32, **un fondu de 0,4 s par vers**, α max **0,72**, soulignement 2 px, liseré sombre. Jamais permanent, jamais sur cartes/CTA.
- **Filet** : `y 1560`, `x 170→910`, fond α 48 (4 px), actif α 210 (8 px), `fr = (t − début_1er_vers)/(fin_chanson − début_1er_vers)`.

---

## 8 — Recettes de style (une seule par chanson)

- **WANDANCE BATTLE & GRAFFITI LOVES** *(validée 39 plans / 42 vers, 0 faute)* — street-dance battle inspirée de *Wandance*, visage 100 % dégagé `y < 560`, décors urbains atténués ; paroles peintes en graffiti **structuré, net, très lisible** (or chaud `#F4C562`, blanc, cyan-argent `#B8E6F2`) sur ruban d'encre noire `y 650→1040` ; stickers « love » + icône thématique `y 1100→1280` ; bande `y 1452→1545` **réservée** à la traduction FR.
- **STUDIO ANIME SEINEN — N&B, décors atténués** *(validée 36 plans / 47 vers, 0 faute)* — cel-shading monochrome, trait `#050608`, blancs `#FFFFFF`, gris `#2A2E35`.
- **ENCRE & FEUILLE D'OR — « la nuit qui finit bien »**.
- **AUBE CLOCHETTES** — fonds clairs, lumière d'aube volumétrique.

---

## 9 — Continuité et progression vers l'aube

- l'arc lumineux avance par paliers (nuit / ombre → premières lueurs au pont → **aube / plein soleil** sur le refrain final et l'outro) ;
- **pas de retour en arrière de la lumière** : toute reprise de refrain ou de signature après le pont reçoit sa **variante d'aube dédiée** (`…-aube.png`) ;
- **réutilisation maîtrisée** : un même texte chanté plusieurs fois **avant** le pont peut partager le même plan (le travelling alterne par parité de segment) ; **après** le pont, la variante d'aube est **obligatoire** ;
- toute variante manquante est **déclarée en repli** dans la livraison, jamais passée sous silence.

---

## 10 — Méthode de fabrication

1. **Ancre d'abord** : `fonds/scene-01-ancre.png`, contrôlée et validée (`ANCRE.md`) ; elle sert de `images=[…]` à **toutes** les salves.
2. **Salves ≤ 10 images par tour** ; consigner demandées / réussies / échouées.
3. `verses_map.json` = contrat unique (`build_map.py`) : `{i, t, fin, affichage_s, texte, langue, traduction_fr, image, disponible, reprise}` ; `disponible` recalculé avec `os.path.exists`.
4. `CARTE-VERS.md` générée depuis `verses_map.json`.
5. QC obligatoire : `CONTROLE-salveN.jpg` (tuiles ≥ 480 px), `CONTROLE-salveN-typo.jpg` (crops 1:1, grille 16 px), `CONTROLE-mp4-final.jpg`, `CONTROLE-typo-zoom.jpg`.

---

## 11 — Audio (maître de l'artiste, jamais généré)

- mesurer avant de promettre : durée décodée (`ffmpeg -map 0:a:0 -f null -`), LUFS, TP, LRA, silences ;
- `loudnorm` 2 passes linéaires `I=-14:TP=-1.5:LRA=11`, 48 kHz, stéréo, `libmp3lame -b:a 320k` CBR, **`-vn`**, puis ID3v2.4 (`TIT2`, `TALB`, `TPE1`, `TPE2`, `TCON`, `APIC` 1080², `USLT` sans horodatages, `TXXX` SIGNATURE/MASTER/IA), **relecture des tags** après écriture ;
- clip : `apad=pad_dur=6.00`, `-map 0:a:0 -vn`, AAC 256k 48 kHz.

---

## 12 — Encodage et contrôles

- `libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart` ;
- pipe `rawvideo rgb24 1080×1920@30`, un seul passage (`n = round(t_end × fps)`).

| contrôle | commande | attendu |
|---|---|---|
| durée | `ffmpeg -i` | = `frames/fps` à 0,01 s |
| frames noires | `blackdetect=d=0.05:pix_th=0.10` | **0** |
| gel | `freezedetect=n=-33dB:d=2.5` | **0** |
| loudness | `ebur128` | −14,0 LUFS |
| crête | `astats` | ≤ −1,0 dB |
| faststart | octets | `moov` avant `mdat` |
| typo | zoom 1:1 | nette, aucun dédoublement |

---

## 13 — Git et livraison

- commit + push **après chaque étape**, uniquement sur la **branche de la session** ;
- **toute** livraison finale contient, dans cet ordre : **1)** Titre · **2)** Captions · **3)** Hashtags (13 max) · **4)** le fichier 9:16 présenté · **5)** déclaration IA (visuels OUI / audio NON) · **6)** commandes Termux, **une ligne par fichier séparée par `;`**, sur le hash **après push** (`git ls-remote` + taille du blob).

---

## 14 — Interdits permanents

Drapeau / bannière · code à 4 chiffres & accroche « reste jusqu'à la fin » · contact, lien, QR, logo dans une image · nudité, anatomie exhibée · visage caché par masque/capuche/lunettes/texte · photo personnelle envoyée au générateur sans autorisation écrite · cursive sur un CTA · calque typo par-dessus la typo peinte · horodatages modifiés · **`Daïsky` / `DAÏSKY`** · validation ou mesure inventée.

---

## 15 — Gabarits de prompts d'image

### 15.1 WANDANCE BATTLE & GRAFFITI LOVES (VO peinte + bande FR libre)

> Vertical 9:16 street-dance battle anime illustration in the dynamic style of Wandance combined with clean, well-ordered, stylish urban graffiti art, keeping the exact same protagonist and visual style as the reference image.
> Scene: In the upper frame (between y 150 and y 550, head fully inside the frame), the same charismatic young Black male street dancer with short stylized locks and closed high-collar dark urban battle jacket performs `<pose>`, his uncovered face showing `<expression>`. Behind him, an attenuated `<décor>`.
> In the middle band (between y 650 and y 1040, centred, max width 720 px, never over the face) over a clean dark ink-black spray brushstroke, paint two lines of neat, well-ordered, ultra-legible stylized graffiti block capital letters, **each capital about 56 px tall on a 1376-px-tall canvas, both lines fully inside x 190 → 880**:
> First line in bold warm white and gold graffiti capitals: "`<LIGNE 1>`"
> Second line below it in crisp cyan-tinted silver-white graffiti capitals: "`<LIGNE 2>`" (include every accent mark: `<diacritiques>`).
> Just below the text (around y 1150, strictly above y 1290), paint 2 stylish urban graffiti sticker icons: a glowing street-art heart ("love" sticker) and `<icône>`, linked by a thin luminous gold graffiti line.
> Keep the lower area below y 1300 as clean dark concrete floor with no text or icons. Nothing in the top 144 px, nothing on the right side x >= 910, no flags, no logos, no other words.

### 15.2 STUDIO ANIME SEINEN N&B

> Vertical 9:16, dark seinen anime cel-shaded illustration in strict BLACK AND WHITE monochrome (pure black ink, stark white highlights, muted charcoal grey, zero colour), same protagonist and style as the reference image, attenuated background.
> Scene: above y 560, head fully inside the frame, the same Black male anime protagonist with short stylized locks and closed high-collar black coat has a `<expression>`. Behind him an attenuated, darkened, low-contrast charcoal `<décor>`.
> In the middle band over a deep black ink brushstroke, two lines of white serif capitals, **each capital about 56 px tall, both lines fully inside x 190 → 880**: "`<LIGNE 1>`" / "`<LIGNE 2>`" (accents: `<diacritiques>`).
> Below (around y 1200, above y 1500), 2 white ink line-art sticker icons: `<icône 1>` and `<icône 2>`; a thin luminous white ink thread crosses the frame.
> Text between y 620 and y 1340, centred, max 740 px, never over the face, nothing in top 144 px, nothing below y 1574. No flag, no logo, no other text.

---

## 16 — Historique

- **v6.1** (2026-10-25) — correctifs issus du premier rendu réel de `productions/on-nous-a-vole-notre-education/` :
  **amplitude du travelling bornée à la bande** (`XR 45 / YR 40`, §5.2 — l'ancienne règle décapitait le
  personnage) ; **cadrage natif imposé** (front `≥ 190`, plan mi-corps, §3.1) ; **§3.1 conversion
  1080×1920 → 768×1376** (le bloc peint descendait sous la zone TikTok) ; **stickers à texte auto-ajusté** et
  pilules `700×144` ; **fond de carte flou 9 / 0,72 / scrim 0,55** ; **cloche redessinée** + flèche au-dessus +
  plaque α 244 ; badge `Dsky` vérifié hors du visage.

- **v6.0 FINAL** (2026-10-25) — correction d'auteur : **`Dsky` remplace définitivement `Daïsky`** (cartes, badge, prompts, tags, livraisons) ; **calage corrigé du `SC`** (source 768×1376 → 1188×2128, marges réelles 108 × 208 px, au lieu de « 1188×2132 / 212 px » hérité d'une source 1080) ; **calibration typographique** ajoutée (capitales ≈ 56 px, bloc `x 190→880`) après débordement constaté sur planche 1:1 ; **bornage de l'accueil** clarifié (la signature d'ouverture appartient à la carte) ; **réutilisation de plans** encadrée (§9) ; rappel que la pilule FR reste **dormante** sur une chanson française.
- **v6.0** (2026-10-21 / 24) — « WTBW Salut & Stickers Doux » : suppression du système de code ; accueil 2 temps ; finale « MERCI · WTBW » ; 3 stickers vectoriels ; clochettes WTBW ; recettes SEINEN et WANDANCE validées.
- **v5.9** (2026-10-14) — « Ça bouge, sans voiler la parole » : question §0, fenêtre glissante 110 %, état éteint, 4 grains, vignette masque L.

**Signature :** « Wolof TechStein beat wê ! » (WTBW) ⚡
