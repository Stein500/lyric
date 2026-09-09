# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v4.9 (badge DSKY✓ haut-centre, CTA 2 s, icône partage mi-vidéo, teaser 2 images obligatoire)

**Artiste :** Daïsky · **Projets de référence :** *Le Survivant* (FR/Wolof, 2:30, ~128 BPM)
**Utilisation :** Référence OBLIGATOIRE pour tous les clips lyrics Daïsky Prod / TechStein. Toute déviation doit être validée.

---

## 🚨 0. DÉSYNCHRONISME — RÈGLES D'OR (prouvées en production)

1. **SOLUTION A — FLUX CONTINU FRAME-ACCURATE (la seule utilisée désormais)**
   - UN SEUL flux de `ceil((durée_chanson + endcard + apad) × FPS)` frames ; chaque frame `i` correspond **exactement** à `t = i/FPS`.
   - Vers affecté **par temps**, jamais par sommation de clips → 0 accumulation d'erreur, même après 2:00.
   - Encodage en une passe : `image2pipe -framerate FPS -vcodec mjpeg -i - → libx264`, puis mux audio master (`apad`, `afade`, `vf fade`).
   - Interdits : concat demuxer, clips encodés séparément, maintien rendu une fois puis répété.

2. **⏱ RÈGLE DES 0,03 s (v4.7 — validée par l'artiste)**
   - Les vers s'affichent avec **0,03 s D'AVANCE** sur le timestamp des paroles (`ADVANCE = 0.03`).
   - Le texte utilise une fenêtre décalée `d0 = t0 − 0,03` ; les **fonds** restent sur l'horloge musique.

3. **Aucune image statique** : Ken Burns léger (zoom/pan lent sur canvas 1,1×) + **vague continue** pendant tout le maintien.

---

## 🧭 1. ORDRE DE PRODUCTION (séquence validée — ne pas inverser)

1. **Analyse** MP3 (durée exacte décodée, LUFS/TP, structure, BPM) + **validation du fichier de paroles** vers par vers (onsets ±0,35 s).
2. **Décisions** : charte (A/B/hybride), source images, périmètre, endcard.
3. **Image d'ancrage** (1 par charte) + maquette badge/vers → **validation artistique**.
4. **Génération par SALVES de 10 images max/session** (règle absolue §7) : planche contact → validation → salve suivante.
5. Pré-calcul fonds → rendu **9:16 d'abord** (bien fait) → vérifs §8 → **16:9** → **MP3 master + tags** → **covers**.
6. **TEASER (obligatoire, APRÈS la vidéo — §17)** : extrait court à partir de **2 images générées retravaillées par l'IA**, CTA like/abonne/commente visibles les 2 premières secondes, annonce de la sortie du prochain clip + lyrics.
7. Commit + push **après CHAQUE étape** (anti-reset).

### Budget images (règle : 1 vers = une image)
`N vers + 2 (fond intro musicale + fond endcard)` **par format**.
Exemple *Le Survivant* : 47 vers + 2 = **49 images 9:16 + 49 images 16:9 + 1 base cover ×2 formats = 99 images**, 5 salves de 10 max par format.

---

## 🏷 2. CONTACT & CRÉDITS (écran de fin + tags)

- **Téléphones :** `229 01 61 16 24 08 · 229 01 49 11 49 51`
- **Emails :** `daiskypro@proton.me` (principal) · `daiskyproduction@gmail.com` · `techsteinsecureway@gmail.com`
- **Handles :** `@daiskypro`
- Écran de fin : Titre du morceau · Label **Daïsky Prod / TechStein** · Artiste **Daïsky** · Genre · **Année** · **DSKY✓** (badge §5.1) + @daiskypro + « Wolof TechStein beat wê ! »
- **Endcard par défaut :** démarre sur le fondu final de la chanson + `apad` 5 s (ex. *Le Survivant* : endcard 2:29.5 → total **2:35.00**).

## 📦 3. TAGS / MÉTADONNÉES ID3 (obligatoires sur TOUS les MP3)

| Champ | Valeur |
|---|---|
| TIT2 | Titre du morceau |
| TPE1 | `Daïsky` |
| TALB | `TechStein Prod` |
| TPE2 | `Daïsky Prod` |
| TPUB | `TechStein / Daïsky Prod` |
| TCOM | `TechStein · Daïsky` |
| TCON | `Rock / Afro-Rock / World` (adapter) |
| TDRC | année de production |
| TXXX contact | `Tel: 2290161162408 / 2290149114951` |
| TXXX email | les 3 emails |
| TXXX producer | `TechStein` |
| TXXX label | `Daïsky Prod` |
| USLT | paroles complètes (nettoyées des timestamps) |
| APIC | cover carrée 1080×1080 |

## 🧱 4. ANTI-RESET & RÈGLES GIT

- Branche `arena/<id>-<slug>` ; **commit + push après chaque étape majeure** (prouvé : 2 restaurations de sandbox récupérées à 100 % grâce au push).
- Sauvegarde `_reset` : si le HEAD local retombe, `git fetch origin <branche> && git reset --hard FETCH_HEAD`.
- `livrables/` JAMAIS dans `.gitignore` ; `.venv/`, `work/`, `*.pyc`, `bin/` dedans. `work/` n'étant pas versionné, les scripts sont régénérables et l'environnement se reconstruit via `work/setup_env.sh` (venv + imageio-ffmpeg + mutagen + numpy + pillow + matplotlib).
- Ne jamais committer ffmpeg/ffprobe/venv. MP4 > 50 Mo : warning GitHub OK (téléchargeable) ; prévoir version allégée en option.

## 🏷 5. RÈGLE D'OR — BADGE / CTA / ENGAGEMENT (v4.9)

### 5.1 Badge « DSKY✓ » (remplace « ⚡ DAÏSKY PROD » — validé artiste)
- Texte du badge : **`DSKY✓`** (coche de certification dessinée en polygone, PAS d'emoji).
- Position : **EN HAUT, CENTRÉ HORIZONTALEMENT** (cx = W/2, y ≈ 36 px) — plus jamais en haut-gauche.
- Style : **discret MAIS visible** — petite carte semi-opaque sombre (opacité ~70 %), liseré cyan fin, coche cyan/dorée, taille de police réduite (~30-34 px en 9:16). Il ne doit jamais gêner la lecture des paroles ni voler l'attention.
- **100 % STATIQUE** : même taille/position/police/couleurs sur toutes les frames, posé en POST en **dernier** (jamais recouvert). **POLICE DROITE, GRASSE ET LISIBLE (DejaVu Sans Bold, fournie dans `assets/fonts/`) — JAMAIS d'écriture script/cursive sur le badge**. Identique sur les covers et le teaser.

### 5.2 Icônes CTA « Like / S'abonner / Commenter » — 2 premières secondes (OBLIGATOIRE)
- Sur **le lyrics ET le teaser** : une rangée d'icônes **👍 Like · 🔔 S'abonner · 💬 Commenter** (dessinées en vectoriel PIL, style cohérent avec la charte — cyan/ambre sur cartes sombres arrondies, PAS d'emoji système) doit être **visible pendant les 2 premières secondes** de la vidéo (t = 0 → 2,0 s).
- Placement : bandeau discret sous le tiers supérieur (9:16) ou bas-centre (16:9), avec un léger fade-out à 2,0 s (~0,4 s de fondu). Il ne doit jamais recouvrir le badge DSKY✓ ni le titre.
- Posé en POST comme le badge (après le texte, avant rien).

### 5.3 Icône PARTAGE au milieu de la vidéo (OBLIGATOIRE)
- À **t = durée/2** (± ajusté pour tomber entre deux vers, jamais par-dessus un vers en pleine lecture), faire apparaître l'**icône de partage ultra-cool générée par l'IA** (flèche/orbe de partage stylisée charte B, glow cyan) : apparition en fondu + léger pulse (scale 1,0→1,06, ~0,9 Hz), durée d'affichage **~3 s**, puis fondu de sortie.
- Accompagnée d'un micro-texte droit lisible : « Partage ⤴ » (DejaVu Sans Bold, jamais cursive).
- L'icône est générée UNE FOIS (fond transparent ou détouré) et réutilisée sur tous les projets : `assets/icons/share_daisky.png`. Si absente, la générer via IA (prompt : icône de partage néon cyan/ambre, style seinen, fond noir, no text) puis détourer.

## 🎨 6. CHARTE GRAPHIQUE

- **A. Mixte (amour)** : coucher de soleil chaud, halo doré, bokeh, grain 35 mm — suffixe : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading, no text, no watermark, no logo`.
- **B. Dark Trap / Lightning** (titres sombres) : éclairs cyan/ambre, reflets mouillés, noir animé seinen — même suffixe technique.
- **P. Pluie / Fraîcheur (v4.9 — validée artiste sur *Yafoy t'es encore là*)** : nuit de pluie rafraîchissante, palette bleu-teal froide + touches ambre chaudes, rideaux de pluie, reflets sur asphalte mouillé, bokeh de gouttes — suffixe canonique : `cool rain-soaked night, fresh blue-teal palette, falling rain streaks, wet asphalt mirror reflections, raindrop bokeh, atmospheric mist, electric cyan rim light, subtle warm amber accents, crushed blacks with cyan highlights, moody anime-seinen cinematic grading, 35mm film grain`.
- **Hybride autorisé** : B pour couplets/refrains + A pour le pont calme (ex. pont piano *Le Survivant* slots 35-38 → glow ambre au lieu de cyan).
- **Interdit** : tout texte/logo généré par l'IA dans l'image source ; wrap manuel.
- **EXCEPTION v4.8.2 (validée artiste)** : le **titre des covers** (et le titre d'intro si désiré) est **généré PAR l'IA, intégré au rendu** — typographie dorée cursive élégante fondue dans la scène. Vérifier l'orthographe du titre rendu (régénérer si illisible). **Le badge DSKY✓ reste TOUJOURS posé en post** (identité de marque, jamais généré par l'IA).

## 🖼 7. IMAGES — RÈGLES ABSOLUES

> **RÈGLE 1 — UNE IMAGE PAR LIGNE UNIQUE (réutilisation des refrains validée par l'artiste).**
> Chaque **ligne unique** a sa propre image, et ce **dans CHAQUE format** (portrait 9:16 ET paysage 16:9 distincts). **Les répétitions réutilisent la même image** : refrain repris (les lignes du refrain 2 réutilisent les images du refrain 1), tags/outro répétés à l'identique (ex. 2× « Wolof TechStein beat wê... » = 1 seule image).
> **L'IA calcule le décompte** : `N = lignes uniques + 2 (intro + endcard)` **par format**, présente le calcul, puis **c'est L'UTILISATEUR qui choisit le nombre final ET l'ambiance** (charte A/B/hybride) avant toute génération.
> ❌ Interdit : réutiliser une image pour une ligne au texte DIFFÉRENT, partager une image entre formats, dédoublonner une ligne unique.

> **RÈGLE 2 — GÉNÉRATION PAR SALVES DE 10 MAX PAR SESSION.**
> On ne génère **JAMAIS tout d'un coup** : salves de **10 images maximum par session** (limite IA dure). Exemple : 49 images = **5 salves** (10+10+10+10+9). Après **chaque salve** : planche contact → **validation artistique AVANT de lancer la suivante**. Une salve refusée = seuls les slots concernés sont régénérés.

- **RÈGLE SOLO (v4.9)** : tout passage instrumental **> 20 s** (solo guitare, break) reçoit **2-3 images dédiées** épiques (ex. « guitare hero » sous la pluie), enchaînées en Ken Burns — on ne réutilise PAS les images du refrain pour un long solo. Ces images s'ajoutent au budget (`+2 ou +3`).
- **Budget par format = `N lignes uniques + 2`** (fond intro musicale + fond endcard) **+ images solo éventuelles**, refrains/tags répétés dédupliqués. Ex. *Seul(e) dans ma tête* : 50 lignes − 8 (refrain 2 = refrain 1) − 1 (tag outro ×2) = **41 uniques + 2 = 43 par format** au lieu de 52 (économie de 9 images/format). Le décompte exact est présenté à l'utilisateur AVANT génération ; l'utilisateur tranche nombre + ambiance.
- **Nommage** : `assets/raw/{portrait|landscape}/s{slot:02d}_<motclé>.png` · `s00` = intro musicale · `s01…s{N}` = vers 1→N (slot = index vers + 1) · `s{N+1}` = fond endcard.
- **Ancrage** : 1 image de référence par charte (B et/ou A) validée **avant** la salve 1.
- **Arc narratif** : chaque image illustre son vers (métaphores visuelles), même héros d'un bout à l'autre, décrescendo lumineux sur l'outro, fond endcard sombre et épuré.
- Pendant les salves d'un format, on peut continuer le reste du pipeline (rendu de l'autre format, MP3…) — mais **jamais deux salves d'images dans la même session**.
- **Chaque prompt d'image suit la structure à 7 blocs du §16** (cadrage exact, bloc héros identique, plan, suffixe canonique, zone texte, interdits) — **jamais de prompt improvisé** ; les 10 prompts d'une salve sont écrits en entier AVANT de lancer.

## 💫 8. EFFET VAGUE + KEN BURNS

- Apparition : lettres montent une à une (staggered ~0,9 s) · Disparition : cascade inversée · **Ondulation sinusoïdale continue** (amplitude ~6 px, 0,9 Hz, phase par lettre) pendant tout le maintien.
- Rendu image par image (PIL, sprites de lettres avec glow précalculé + cache).
- Ken Burns : canvas 1,1× (1188×2112 pour 1080×1920 ; 2112×1188 pour 1920×1080), zoom 1,02→1,08 alterné par slot, pan sinusoïdal lent.

## 🎞 9. MONTAGE PIPELINE (SOLUTION A)

1. Pré-calcul fonds : upscale LANCZOS → canvas Ken Burns → JPEG q92 (`work/fonds_{portrait|landscape}/f{slot:02d}.jpg`).
2. Rendu : flux continu `ceil(durée_totale × 30)` frames, texte par fenêtres `d0/d1` (avance 0,03 s), overlays d'engagement (icônes CTA 0→2 s + icône partage mi-vidéo, §5.2/§5.3) puis badge DSKY✓ posé en **dernier**, intro musical-only avec titre (0 → 1ʳᵉ voix), endcard à partir du fondu final.
3. Mux : `[1:a]apad=whole_dur=<total>,afade=t=out:st=<total-3>:d=3[a]` + `[0:v]fade=t=out:st=<total-3>:d=3` (PAS de fade-in : il crée des frames noires → blackdetect).
4. Exports : `livrables/<Titre>_9x16_v<N>.mp4` et `livrables/<Titre>_16x9_YT_v<N>.mp4` (crf19, veryfast, aac 192k, +faststart). Texte 9:16 : police 58, base bas H−300, max 920 px. 16:9 : police 62, base bas H−150, max 1640 px, endcard décalé à gauche (cx = 0,38×W).

## 🖼 10. COVER DE PUBLICATION

- Base IA générée **AVEC le titre intégré** (v4.8.2) : le prompt demande le titre exact — ex. `Seul(e) dans ma tête` — en grande cursive dorée lumineuse (zone sombre : haut 9:16 / gauche 16:9), et `Daïsky` en plus petit dessous. **Pas de texte composé manuellement sur la cover** (jugé moche) — seul le badge est posé en post.
- Orthographe du titre rendu par l'IA = point de validation obligatoire (régénérer la base si lettres déformées).
- **Hook visuel** : composition simple et symétrique, UN seul point focal lumineux, compréhensible en 2 s et lisible en vignette (règles du §16).
- Titre **cursive GreatVibes** si `work/fonts/GreatVibes-Regular.ttf` fourni (CDN polices bloqués → **fournir le .ttf dans le repo**), sinon fallback serif incliné + glow ambre.
- Sous-titre : Daïsky · Daïsky Prod / TechStein · Genre · Année · `@daiskypro` + badge **DSKY✓ haut-centre** (§5.1).
- Sorties : `livrables/cover_<titre>_9x16.jpg` (1080×1920) + `cover_<titre>_16x9.jpg` (1920×1080), JPEG q92.

## 🎧 11. MASTERISATION MP3 (prouvée en production)

- Chaîne : `highpass=f=30, lowpass=f=18000, loudnorm=I=-14:TP=-1.8:LRA=11:measured_I=…:measured_TP=…:measured_LRA=…:measured_thresh=…:offset=…:linear=true`
- **2 passes** : passe 1 mesure (`print_format=json`), passe 2 applique en linéaire.
- ⚠️ **Piège** : l'option passe-2 s'appelle **`offset=`** (le JSON passe-1 dit `target_offset`) — sinon `Option not found`.
- ⚠️ Cibler **TP=-1,8** : le décodage MP3 overshoote ~+0,3 dB → résultat final ≤ -1,5 dBTP (mesuré : -13,9 LUFS / -1,7 dBFS ✓).
- Export : libmp3lame **320 k**, 48 kHz, durée conservée `-t <durée>`, puis tags §3 (mutagen, ID3v2.4).

## ✅ 12. VÉRIFICATIONS OBLIGATOIRES AVANT COMMIT

1. Durée : `nb_frames/fps` = durée cible **±0,05 s** ; streams conformes (1080×1920 / 1920×1080, 30 fps).
2. `blackdetect` = 0 (seul le fade-out final est toléré).
3. `freezedetect` = 0 (aucune image figée).
4. **Frontières de vers par diff pixel** : extraire la frame MP4 à des temps clés (début V1, milieu, 2:00+, endcard) et comparer à la frame reconstruite par la logique → écart moyen < ~6 px = bon vers au bon moment ; vérifier l'avance 0,03 s à une frontière.
5. Badge **DSKY✓ haut-centre** statique (écart < ~4 px entre deux instants sur le même fond).
6. **CTA 2 s** : frame à t=1,0 s → icônes Like/S'abonner/Commenter présentes ; frame à t=3,5 s → disparues.
7. **Icône partage mi-vidéo** : frame à t=durée/2 → icône partage visible ; absente 5 s avant/après sa fenêtre.
8. Écran de fin + contacts + apad.
9. MP3 : LUFS/TP/durée + tous les tags présents.
10. Cover lisible (dimensions + zone titre + badge).
11. **Texte non coupé** : audit bbox des sprites à la construction (marge glyphs ≥ 6 px des bords) + sur frames échantillonnées, aucun pixel de texte tronqué ni chevauché.

## 📣 17. TEASER OBLIGATOIRE (v4.9 — après chaque vidéo lyrics)

- **⚠️ LE TEASER EST UNE VIDÉO À PART ENTIÈRE** : un livrable AUTONOME, distinct du clip lyrics, avec son propre fichier, son propre montage, sa propre publication (avant la sortie du clip). Ce n'est PAS un extrait coupé du clip — il est produit avec le même soin (SOLUTION A, vérifs §12, badge, mastering audio de l'extrait).
- **Quand** : systématiquement APRÈS la finalisation du clip lyrics (les deux formats rendus et vérifiés).
- **Matière première : SEULEMENT 2 images générées** (choisies parmi les plus fortes du clip — typiquement l'image d'intro/hook et une image de refrain pleine énergie). **L'IA retravaille ces 2 images** (recadrage dramatique, glow renforcé, contraste boosté, éventuel edit IA image-à-image) pour créer une tension visuelle qui pousse le viewer à **cliquer, s'abonner, liker et commenter**.
- **Contenu** : extrait audio court du morceau (le hook le plus fort, ~15-25 s), les 2 images en Ken Burns dynamique + transitions énergiques, texte d'annonce (droit, DejaVu Sans Bold) : sortie imminente du **prochain clip + lyrics** (« Bientôt… », titre, « Abonne-toi pour ne rien rater »).
- **CTA** : icônes Like/S'abonner/Commenter visibles les **2 premières secondes** (§5.2), rappel CTA en fin de teaser (dernière carte : « 👍 Like · 🔔 Abonne-toi · 💬 Commente »).
- **Badge** : DSKY✓ haut-centre statique (§5.1) présent du début à la fin.
- **Formats** : `livrables/teaser_<titre>_9x16.mp4` (priorité Shorts/TikTok/Reels) ; 16:9 en option si demandé.
- **Pipeline** : même SOLUTION A (flux continu frame-accurate, §0), mêmes vérifs applicables (§12 : durée, blackdetect, freezedetect, badge statique).

## 📦 13. TÉLÉCHARGEMENTS (REPRENABLES)

- Dest `/storage/emulated/0/Web+/` ; `curl -fL --retry 5 --retry-delay 3 -C - -o "fichier" "https://raw.githubusercontent.com/Stein500/lyric/<HASH>/livrables/..."` — **toujours vérifier `git rev-parse HEAD` avant de partager une URL**.

---

## 🎯 16. PROMPTS D'IMAGE — PRÉCISION MAXIMALE (v4.8)

**Structure OBLIGATOIRE d'un prompt d'image (7 blocs, dans l'ordre) :**
1. **Cadrage** : `vertical 9:16 portrait composition, tall framing` OU `horizontal 16:9 landscape composition, wide framing` — toujours en tête.
2. **Sujet + action + émotion du vers** (une phrase visuelle).
3. **BLOC HÉROS** (recopié à l'identique, jamais modifié) : `the same mature androgynous hero, mid-thirties, mixed masculine and feminine features, short dark hair, open dark silk shirt, thin silver chain`.
4. **Plan** (rythme visuel) : `wide shot` (refrains/show, paysages) · `medium shot` (narration) · `close-up` (émotion, pont) — alterner les plans au sein de chaque salve.
5. **Suffixe technique canonique** (recopié tel quel) :
   - **Charte B** : `deep blue-black night, warm amber backlight, subtle electric cyan rim light, wet asphalt reflections, atmospheric haze, crushed blacks with cyan highlights, moody anime-seinen cinematic grading, 35mm film grain`
   - **Charte A** : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading`
   - **Charte P (pluie/fraîcheur)** : `cool rain-soaked night, fresh blue-teal palette, falling rain streaks, wet asphalt mirror reflections, raindrop bokeh, atmospheric mist, electric cyan rim light, subtle warm amber accents, crushed blacks with cyan highlights, moody anime-seinen cinematic grading, 35mm film grain`
6. **Zone réservée au texte** (toujours) :
   - Intro / endcard / covers 9:16 : `large dark negative space across the top quarter of the frame for title text`
   - Covers 16:9 : `large dark negative space across the left third of the frame for title text`
   - Vers (paroles en bas d'écran) : `darker, less busy lower third with soft bokeh for lyric text readability`
7. **Interdictions** (toujours) : `no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders`.

**Règles ANTI-HORS-CADRE (validées artiste) :**
- Sujet TOUJOURS complet : `full figure, head and hands completely in frame, no cropped face, no out-of-frame elements`.
- Mains visibles → ajouter `all fingers visible`. Jamais de main coupée, jamais de visage coupé au bord.
- Pas de perspective extrême qui déforme le héros ; pas de premier plan qui masque le visage.

**Règles qualité / beauté :**
- **Intro, covers, endcard = « hook »** : composition simple et symétrique, UN SEUL point focal lumineux, forte lisibilité en vignette (compréhensible en 2 s).
- **Arc lumineux narratif** : intro = pénombre calme → couplets = cyan modéré → refrains = lumière max → pont = ambre pur → outro = décrescendo → endcard = sombre épuré. Chaque prompt précise l'intensité (`dim`, `moderate`, `full energy`…).
- Cohérence : générer toute une salve dans une même session, blocs 3/5 strictement identiques.
- **Contrôle post-génération** : ratio exact (9:16 ou 16:9), pas de texte/lettre/chiffre détecté, héros conforme → planche contact AVANT la salve suivante.

## 📜 Historique des versions
- **v4.9** — Badge devient **DSKY✓** haut-CENTRE discret+visible (§5.1) · icônes CTA like/abonne/commente visibles les **2 premières secondes** sur lyrics ET teaser (§5.2) · **icône partage IA** en pulse au **milieu de la vidéo** ~3 s (§5.3) · **teaser obligatoire** après chaque clip, à partir de 2 images retravaillées par l'IA, annonçant la sortie du prochain clip+lyrics (§17) · vérifs §12 étendues (CTA, partage) · nouvelle **charte P Pluie/Fraîcheur** (§6/§16, validée sur *Yafoy*) · les longs solos instrumentaux (> 20 s) reçoivent **2-3 images dédiées** (ex. guitare hero épique) au lieu de réutiliser le refrain.
- **v4.8.2** — §6/§10 : titre des covers généré PAR l'IA (intégré au rendu, plus beau que le texte composé), badge toujours en post, orthographe validée.
- **v4.8.1** — RÈGLE 1 modifiée : image par ligne UNIQUE, refrains/tags répétés dédupliqués ; l'IA calcule `N = uniques + 2` et l'utilisateur choisit nombre + ambiance.
- **v4.8** — §16 prompts d'image à 7 blocs (cadrage, bloc héros, plan, suffixe canonique, zone texte, interdits) · règles anti-hors-cadre (sujet complet, mains, visage) · hook covers/intro/endcard · arc lumineux narratif · contrôle post-génération.
- **v4.7.2** — badge/endcard en DejaVu Sans Bold (jamais script), cursive = paroles uniquement (option artiste), règle anti-coupure (bbox ≥ 6 px, jamais de troncature), §12.9.
- **v4.7.1** — §14 charte tout-cursive GreatVibes + §15 deux styles 9:16 (v2 droit / cursive) produits en parallèle.
- **v4.7** — règle 0,03 s d'avance · ordre de production validé · budget images N+2 · correctifs (`offset=`, TP=-1,8, pas de fade-in vidéo, GreatVibes local) · vérifs par diff pixel · endcard par défaut sur fondu + apad 5 s.
- **v4.6** — désynchronisme corrigé (SOLUTION A/B/C), vague continue, endcard, tags ID3, badge haut-gauche, 16:9+9:16, covers, -14 LUFS.
- **v4.3** — première structuration salves/ancrage.

## ✍ 14. CHARTE TEXTE — CURSIVE = PAROLES UNIQUEMENT (v4.7.2)

- **Règle d'or** : la cursive GreatVibes est réservée aux **PAROLES** (et au titre du morceau affiché en intro/endcard/covers) — et seulement **si l'artiste le désire**. **TOUT le reste est en police DROITE, GRASSE et LISIBLE (DejaVu Sans Bold, fournie dans le repo)** : badge, endcard/contacts, téléphones, emails, @daiskypro. **JAMAIS de script sur ces éléments** (validé artiste).
- Police connectée (scripte) → **rendre ligne par ligne en texte connecté**, PAS lettre par lettre (sinon les lettres se déconnectent). L'effet vague se fait par onde verticale douce de la ligne (ampl. ~4 px, ~0,9 Hz), pas de staggering lettre à lettre.
- **RÈGLE ANTI-COUPURE (obligatoire — validée artiste)** : aucun glyphe ne doit être tronqué ni toucher le bord de son sprite. Marges de sécurité **vérifiées par bbox à la construction** (≥ 6 px sur les 4 côtés), padding large (côtés ≥ 0,6× taille, haut ~0,7×, bas ~0,8×, où taille = corps de police). Si une ligne dépasse : **réduction de la taille puis retour à la ligne, jamais de troncature** ; une ligne supplémentaire est autorisée plutôt que couper. Vérif « pire cas » (ligne la plus longue) à l'aperçu AVANT rendu + audit automatique de tous les sprites + vérif pixel sur les frames (§12.9). Les paroles doivent être **intégralement lisibles** du début à la fin de leur fenêtre.
- GreatVibes est fine → tailles adaptées : paroles 9:16 ≈ 76 px (max ~940 px), titre intro ≈ 120 px, endcard 110 px. Contour léger (2 px) + ombre renforcée pour la lisibilité ; ne pas sur-épaissir le contour (cela hache les lettres fines).
- Fallback uniquement si GreatVibes absente (cursive nécessaire), sinon valider la dérogation.

## 🎞 15. DEUX STYLES 9:16 PRODUITS (validation artiste)
1. **`_9x16_v2.mp4`** — texte droit (DejaVu Bold), badge + vague + intro + endcard.
2. **`_9x16_cursive.mp4`** — TOUT en cursive GreatVibes, badge + vague douce + intro + endcard.
Les deux suivent SOLUTION A (§0/§9). **Dans les deux styles, badge + endcard/contacts restent en police droite lisible (DejaVu Sans Bold)** — seule la police des paroles change. Garder les deux jusqu'à ce que l'artiste tranche.

**Signature :** « Wolof TechStein beat wê ! » ⚡
