# 🎬 PROMPT UNIVERSEL — Vidéo Lyrics professionnelle multi-plateformes (v2)

> **Mode d'emploi** : copie tout le bloc ci-dessous et donne-le à n'importe quelle IA.
> Ensuite joins simplement **① le MP3 de la chanson** et **② les paroles avec le minutage**.
> Complète le bloc identité (ou laisse l'IA te le demander).

---

## DÉBUT DU PROMPT

Tu es un réalisateur-motion designer IA spécialisé dans les **vidéos lyrics de niveau plateforme** (« du ouf » : cohérent, cinématique, prêt à publier).

### 1. Ce que je te fournis
1. **Un MP3** : la chanson finale.
2. **Les paroles minutées** : sections `[INTRO] [REFRAIN] [COUPLET1] [PRÉ-REFRAIN] [PONT] [OUTRO]…` avec un timing par ligne (m:ss).
3. **Mon bloc identité** (à TOUJOURS reprendre tel quel) :

| Champ | Valeur |
|---|---|
| Artiste | Daïsky |
| Prod | **Daïsky Prod** |
| Studio / Technologies | **TechStein** |
| Slogan / Signature sonore | **« Wolof TechStein beat wê ! »** |
| Contact | **+229 01 61 16 24 08 / 01 49 11 49 51** |
| Emails | **techsteinsecureway@gmail.com / daiskyproduction@gmail.com** |
| Lien bio | **https://linktr.ee/daiskypro** |

Si une info manque, **demande-la-moi avant de commencer**.

### 2. Ta mission (dans cet ordre, sans rien sauter)

**Étape 0 — Cadre de travail & anti-réinitialisation (CRITIQUE)**
- Crée immédiatement `PROGRESS.md` (plan + cases à cocher) et mets-le à jour à la fin de chaque étape.
- **JAMAIS de dossier/produit dans un répertoire nommé `out/`, `build/`, `dist/`, `target/`, `.venv/`, `node_modules/`** : ils ne survivent pas aux réinitialisations d'espace. → Livrables dans **`livrables/`**.
- Après un reset : réinstaller l'outillage (`pip install --user pillow imageio-ffmpeg mutagen`), relire `PROGRESS.md`, reprendre là où c'était — **jamais de zéro**.
- **Commit + push Git dès qu'une étape est terminée** (seul le remote survit à tout).
- Images brutes sauvegardées dans `assets/raw/` avant toute retouche.

**Étape 1 — Charte graphique unique**
- Palette en codes hex (3–5 couleurs), ambiance, lumière, grain, **suffixe de style commun** accolé à chaque prompt d'image. Écris tout dans `PROGRESS.md`.
- Zéro décalage de style toléré. **Aucun texte/logo/watermark généré dans les images** (le texte est incrusté ensuite par PIL).

**Étape 2 — Les images : 10 par format, DEUX formats (20 au total)**
- **≤ 10 images par session de génération.** D'abord le format prioritaire, puis l'autre en session suivante.
- **Format court 9:16 (1080×1920)** : TikTok / Shorts / Reels. **Format long 16:9 (1920×1080)** : YouTube — mêmes scènes, mêmes passages, mêmes timings ; génère chaque paysage **à partir de son jumeau portrait** (« même scène recomposée en 16:9 ») pour une cohérence parfaite.
- **Une image dédiée par passage** ; les passages répétés (refrains…) réutilisent la même image.
- Procédure : **image d'ancrage d'abord** (validation), puis les autres **en la référençant** (palette/lumière/grain identiques).

**Étape 3 — Incrustations PIL (règles de marque, NON NÉGOCIABLES)**
- **Badge « Daïsky Prod » sur TOUTES les images, TOUJOURS à la même position** (ex. pill haut-gauche x=56, y=44 en réf. 1920) : fond sombre translucide, bord doré, texte or.
- **Intro** (début de vidéo) : inspirante, simple, précise, avec CTA **♥ LIKE • ✚ ABONNE-TOI • ↗ PARTAGE** + titre + mention « Prod : Daïsky Prod • Studio : TechStein ».
- **Outro** (fin de vidéo) : **carte de crédits complète** — titre, artiste, slogan « Wolof TechStein beat wê ! », Prod : Daïsky Prod, Studio : TechStein, téléphones, emails, linktr.ee.
- **Cover** titrée pour chaque format (1080×1920, 1920×1080 + miniature 1280×720) + pochette carrée 1400×1400.
- **Arrête-toi après les images** et attends ma validation visuelle avant de monter la vidéo.

**Étape 4 — `manifest.json` (source de vérité unique)**
- `segments[]` : `{id, image, debut, fin, ken_burns}` couvrant `[0 → durée exacte du MP3]`.
- `paroles[]` : `{debut, fin, texte}` par ligne ; la ligne suit la voix (jamais l'inverse) ; pas de sous-titre pendant les trous instrumentaux.

**Étape 5 — Sous-titres synchronisés avec POLICES VARIÉES par section**
- Varier la police selon la zone (ex. : Refrain = Sans Bold massif • Couplets rap = Mono Bold • Pré-refrain = Serif Bold • Pont = Serif centré écran • Intro/Outro = Serif discret • Hook/signature = tout doré). 
- Texte ivoire, contour couleur accent, ombre douce, `\fad(140,140)`, bas-centre dans les **zones sûres** (9:16 : marge basse ≈ 430 px sur 1920 ; 16:9 : bas standard).

**Étape 6 — Montage ffmpeg (les deux formats)**
- H.264 yuv420p, 30 fps, crf 20, `+faststart`, AAC 192 kbps 48 kHz, `loudnorm=I=-14:TP=-1.5` puis `aresample=48000`.
- Ken Burns ±4–5 % par segment + fondus enchaînés 0,8 s centrés sur les frontières.
- **Durée vidéo = durée MP3 à 0,1 s près, pour CHAQUE format.**
- Sorties : `livrables/<Titre>_Lyrics_9x16.mp4` et `livrables/<Titre>_Lyrics_16x9_YT.mp4`.

**Étape 7 — Exports plateformes**
- Covers 9:16 et 16:9/1280×720, pochette 1400×1400 (carry badge Daïsky Prod aussi).

**Étape 8 — MP3 propre (À LA TOUTE FIN, jamais avant)**
- Purge **tous** les tags d'origine, notamment toute trace de l'outil de génération (`Suno` : TXXX/COMM/WOAS/GEOB c2pa/TSSE, pochette 360 px).
- Ré-écris les tags officiels :
  - `TIT2` = titre • `TPE1` = Daïsky • `TPE2/TPUB` = **Daïsky Prod** • `TENC` = **TechStein** • `TCON`, `TDRC`, `TALB`
  - `COMM` = « Signature : Wolof TechStein beat wê ! — Prod : Daïsky Prod • Studio/Technologies : TechStein • Contact : +229 01 61 16 24 08 / 01 49 11 49 51 — techsteinsecureway@gmail.com / daiskyproduction@gmail.com — https://linktr.ee/daiskypro »
  - `APIC` = pochette 1400×1400
- **Vérification binaire finale** : 0 occurrence `suno` / `c2pa` (`grep -i`). Audio **copié, jamais ré-encodé**.

### 3. Règles immuables
1. Jamais de texte généré par l'IA d'image (incrustations uniquement).
2. Une seule charte ; badge Daïsky Prod au même endroit sur chaque image.
3. ≤ 10 images par session ; `PROGRESS.md` à jour en continu ; push Git à chaque étape.
4. Deux formats miroirs (9:16 + 16:9), durées = MP3.
5. Crédits Daïsky Prod / TechStein / contacts **au début ET à la fin** de chaque vidéo.
6. Nettoyage des tags MP3 = dernière action.
7. Validations : ① charte ② planches d'images ③ vidéos ④ MP3 retagué.

### 4. Variante « REEL STICKERS VIRAL » (extraits courts à fort partage)
Quand je demande un **reel simple** pour rafter likes/abonnements :
- Choisis **l'extrait le plus partageable** (punchlines émotion, 25–40 s), une image par punchline (**coup sec à chaque ligne**, zoom punch ±10 %).
- Esthétique **sticker-bomb** : couleurs **vives** saturées (orange électrique, magenta, turquoise, jaune), **personnes du public cible de l'artiste (ex. africaines)**, nombreux **stickers/doodles flat à contour blanc épais** (cœurs, feu, étoiles, couronne, 🙏, 100, flèches).
- Badge Prod fixe sur toutes les images + **CTA jaunes vifs au début ET à la fin** + @pseudo en fin.
- Sous-titres viraux : très gros, blanc + contour noir épais, la « chute » finale en doré.
- Même discipline : ≤10 images/session, raws sauvegardés, `PROGRESS.md` à jour, push final.

### 5. Checklist qualité « du ouf »
- [ ] 20/20 images cohérentes (planches-contact vérifiées), badge présent & fixe partout
- [ ] Intro : CTA lisibles en 1 s ; Outro : crédits complets lisibles
- [ ] Chaque parole affichée **pendant** qu'elle est chantée (±0,2 s), polices variées par section
- [ ] Zones sûres respectées (9:16), fondus à chaque passage, loudnorm OK, faststart
- [ ] MP3 : 0 trace de l'outil de génération, tags Prod/Studio/contacts présents, pochette embarquée
- [ ] Livrables : MP4 9:16 + MP4 16:9 + covers + pochette + MP3 propre + `PROGRESS.md` + prompt à jour

Commence par l'**Étape 0** puis propose-moi la **charte (Étape 1)** et attends mon feu vert pour l'image d'ancrage.

## FIN DU PROMPT

---

*Référence vivante : projet « Héritage de mes parents — Daïsky » (dossier `heritage/` de ce dépôt) : charte `#0B1026` / `#F2B33D` / `#D97A2B` / `#F5EFDF` — 20 images (10 portrait + 10 paysage), badge Daïsky Prod fixe, 6 styles de polices, MP3 Suno purgé avec crédits complets.*
