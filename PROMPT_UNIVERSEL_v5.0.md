# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v5.0 « ANY TRACK » (ultra-détaillé, tous morceaux)

**Portée :** N'IMPORTE QUEL audio (mp3/wav) + N'IMPORTE QUELLES paroles (txt/lrc, tous langues) + photos optionnelles → un clip lyrics complet (vidéo 9:16/16:9, MP3 master taggé, covers IA) + livraisons Termux.
**Mode d'emploi :** l'IA exécute **§A (analyse auto, sans questions)** → **§B (questionnaire UNIQUE, 8 questions avec défauts)** → **§C→§F (production complète)**. Si l'artiste dit « vas-y direct / je te fais confiance » : appliquer les défauts marqués (défaut) et les journaliser dans le commit.
**Héritage :** v4.6→v4.9.1 (productions *Le Survivant*, *Seul(e) dans ma tête*, *Je crache mes démons*) — toutes les leçons sont ici des règles.

---

## §A. ANALYSE AUTOMATIQUE (jamais de question à ce stade)

**A.1 Audio.** Durée décodée exacte (`ffmpeg -f null -`), SR/canaux, BPM estimé (flux spectral), structure énergétique (couplets/refrains/ponts par RMS), puis mesure loudnorm **passe 1 avec `-v info`** (le JSON n'est émis qu'au niveau info) : `input_i, input_tp, input_lra, input_thresh, target_offset`.

**A.2 Paroles.** Accepter 4 formats : `-m:ss.x` en fin de ligne · `m:ss-m:ss` · LRC `[mm:ss.xx]` · **sans timestamps** → auto-alignement : onsets détectés répartis sur les sections + validation artiste sur 3 lignes test. Sections `[INTRO]/[REFRAIN]/...` conservées comme métadonnées.

**A.3 Validation vers par vers (règle d'or).** Onset = pic de flux spectral > 1,15 × médiane locale (fenêtre 4 s) ; tolérance **±0,35 s** ; **monotonie stricte** + **fenêtre mini 1,2 s** entre vers consécutifs ; corrections par **miroir de section répétée** (deltas d'un refrain repris = deltas de la 1ʳᵉ apparition) puis pics audio ; sorties : `work/timings_validated.json` + **`<Titre>.lrc` corrigé committé**.

**A.4 Budget images (RÈGLE 1).** Ligne UNIQUE = 1 image par format ; texte identique repris = réutilisation ; texte différent = image différente (même ponctuation : « wê... » ≠ « wê! »). `N = uniques + 2` (fond intro musicale + fond endcard) **par format**. Salves de **10 max** (= quota plateforme 10 générations/tour).

**A.5 Moment fort (cold-open).** Chercher la section la plus énergétique contenant le TITRE (défaut = 1ʳᵉ apparition du refrain-titre) ; extrait audio = 2 lignes si ≥5 s sinon 1 ligne ; durée défaut **6 s** (4 s si refrain <5 s).

**A.6 Identité visuelle.** Si photos fournies : décrire un **BLOC HÉROS fidèle** (corpulence RÉELLE — jamais musclé/embelli si l'artiste ne l'est pas, coupe, barbe, lunettes, vêtements récurrents) + règle ANTI-EMBELLISSEMENT absolue. Sans photos : inventer un bloc héros cohérent (âge, morphologie, vêtements) et le recopier À L'IDENTIQUE partout.

---

## §B. QUESTIONNAIRE DE DÉMARRAGE (le SEUL lot de questions — copier-coller tel quel)

> Poser ces 8 questions en UNE fois (outil ask_user), options + défaut indiqués. Réponse « direct/confiance » = défauts.

1. **🎨 Charte graphique** — (a) **B Dark** : nuit bleu-noir, éclairs cyan/ambre, reflets mouillés, grading seinen · (b) **A Warm** : sunset doré, halo, bokeh, romantique · (c) **Hybride (défaut si pont calme existe)** : B partout + A sur pont/outro doux. *Heuristique auto si confiance : titre/lexique sombre→B, amour→A, mixte→hybride.*
2. **🧍 Héros** — (a) photoréaliste fidèle photos · (b) **semi-réaliste seinen fidèle (défaut si photos)** · (c) inventé cohérent (défaut sans photos) · + lunettes : sans / avec / mixte scènes calmes.
3. **📐 Formats** — (a) **9:16 seul (défaut)** · (b) 9:16 + 16:9 · (c) + version texte droit en parallèle.
4. **✍️ Texte** — (a) **cursive + vague eau (défaut)** · (b) droit gras · (c) les deux styles 9:16.
5. **⚡ Cold-open** — (a) 4 s · (b) **6 s (défaut)** · moment = défaut A.5 sauf choix artiste.
6. **📣 CTA & badge** — icônes like/abonne-toi/commente 2 premières secondes : **rangée bas centrée (défaut)** / bas droite / colonne ; texte badge = label artiste (défaut `DSKY✓` ou initiales+✓) **milieu haut**.
7. **🖼 Cover** — **100 % IA titre intégré (défaut)** · sinon texte post (dérogation tracée).
8. **📦 Livrables** — vidéo+MP3+cover **(défaut)** · +16:9 ? · +version allégée ≤50 Mo ? · destination Termux `/storage/emulated/0/Web+/`.

---

## §C. ORDRE DE PRODUCTION (universel, ne pas inverser)

1. §A complet → 2. §B → 3. **Ancres** (1/charte retenue) + maquette badge/vers/CTA → validation artiste → 4. **Salves de 10** : prompts écrits EN ENTIER avant lancement (§E.1), planche contact + validation entre salves, salve refusée = seuls slots concernés → 5. Pré-calcul fonds → rendu 9:16 d'abord → vérifs §D.10 → 16:9 si demandé → MP3 master + tags → covers → 6. **Commit + push après CHAQUE étape** (branche `arena/<id>-<slug>`).

---

## §D. RÈGLES TECHNIQUES UNIVERSELLES (leçons gravées)

**D.1 Sync SOLUTION A.** Un seul flux de `ceil(TOTAL×FPS)` frames, frame `i` ↔ `t=i/FPS` ; `TOTAL = HOOK + durée_chanson + apad(5 s)` ; fenêtres de vers décalées de HOOK ; vers avec **0,03 s d'AVANCE** ; fonds sur horloge musique. Interdits : concat demuxer vidéo, clips séparés, fade-in vidéo (frames noires).

**D.2 Mouvement permanent.** Ken Burns canvas 1,1× (1188×2112 / 2112×1188), zoom 1,02→1,08 alterné par slot, pan sinusoïdal ; **vague eau** : cursive = ligne connectée ondulée par colonnes (ampl. ~4,5 px, 0,9 Hz) + apparition staggered 0,9 s / cascade inversée ; texte droit = lettres une à une (ampl. ~6 px).

**D.3 Anti-coupure & anti-mélange.** Bbox sprites : marges glyphs **≥6 px** (padding 0,6/0,7/0,8 × corps) ; dépassement = réduction puis retour à ligne, JAMAIS troncature. Positions UI canoniques 9:16 : badge y=36 centré · titre hook/intro y≈210-300 · paroles base H−300 (max 940 px, cursive 76) · CTA 72 px `y=H−30−h` (≥10 px sous les descenders) · icône partage 150 px à 0,40×H, `TOTAL/2 ±2,5 s`, pulse 1,4 Hz. 16:9 : paroles base H−150 max 1640 px, endcard cx=0,38×W.

**D.4 Audio.** loudnorm 2 passes : passe 1 `-v info` ; passe 2 `offset=` (pas target_offset) + `highpass=30,lowpass=18000` ; **TP cible −1,8** ; concat hook+chanson : **tout décoder en WAV 48 k d'abord** (concat pcm+mp3 = durées/gains faux) ; MP3 livrable = chanson seule 320 k 48 k `-t durée` ; tags ID3v2.4 : TIT2/TPE1/TALB/TPE2/TPUB/TCOM/TCON/TDRC + TXXX contact,email,producer,label + **USLT paroles nettoyées** + **APIC cover carrée**.

**D.5 Vidéo.** Encodage image2pipe mjpeg → libx264 une passe ; master local crf19 ; **export git crf21 ≤ ~95 Mo** (limite GitHub 100 Mo/fichier, warning OK >50 Mo) ; aac 192k +faststart ; fades out audio+vidéo 3 s fin uniquement ; mux = ré-encodage vidéo obligatoire si filtre fade (`-c:v copy` + filtre = erreur).

**D.6 Images.** Prompt 7 blocs (§E.1) ; suffixes canoniques A/B (§E.3) ; interdits toujours + `no signage` (enseignes néon = texte !) ; anti-hors-cadre (sujet complet, mains, visage) ; arc lumineux (intro dim → refrains full → pont ambre → outro décrescendo → endcard sombre) ; post-contrôle ratio/texte/héros ; **modération bloquante = reformuler** (retenue physique → « poids de fumée », « soutenir un ami »).

**D.7 Polices.** Cursive GreatVibes = paroles + titres intro/endcard/covers SEULEMENT ; UI (badge, endcard, contacts) = DejaVu Sans Bold jamais script. Acquisition CDN bloqués : `npm pack @fontsource/<police>` → woff2 → **fontTools+brotli → .ttf committé dans `assets/fonts/`** ; vérifier coverage glyphs du texte réel (ex. « œuvre »).

**D.8 Endcard.** Fond sombre épuré dédié (slot s{N+1}) ; titre cursive + crédits DROITS : label, artiste, genre, année, téléphones, emails, handle, signature « Wolof TechStein beat wê ! » (ou signature artiste) ; démarre au fondu final + apad 5 s.

**D.9 Covers.** Base IA **titre intégré** : grande cursive dorée lumineuse + nom artiste dessous, orthographe VÉRIFIÉE (régénérer si lettres déformées), hook visuel 1 point focal, lisible en vignette ; **badge posé en post** (bas-centre si haut occupé par le titre) ; sorties 1080×1920 q92 + carré 1080×1080 (APIC) + 1920×1080 si 16:9 ; pièges réels : cigarette ajoutée par l'IA si « smoke » → écrire « smoke from mouth, no cigarette » ; enseignes → `no signage`.

**D.10 Vérifs avant commit.** Durée `nb_frames/fps` ±0,05 s · streams conformes · blackdetect = fade final seul · freezedetect 0 · frontières vers par diff pixel MP4 vs reconstruction <6 px (mesuré 1,8-2,6) · badge statique · bbox sprites ≥6 px (mesuré 39) · MP3 LUFS≈−14/TP≤−1,5/durée/tags · covers lisibles + badge.

**D.11 Git/anti-reset.** Push après chaque étape ; reset sandbox → `git fetch origin <branche> && git reset --hard FETCH_HEAD` ; **scripts VERSIONNÉS dans `scripts/`** (setup_env.sh, pipeline_rendu_9x16.py, rebuild_timings.py) ; `work/` = cache non versionné (fonds, wav, icônes régénérables 4 gén.) ; `.gitignore` : .venv/, work/, *.pyc, bin/ ; livrables/ et assets/ JAMAIS ignorés.

**D.12 Quotas.** 10 générations d'images/tour = 1 salve ; jamais 2 salves/session ; slots manquants complétés au tour suivant sans bloquer le pipeline (fonds/rendu continuent).

---

## §E. GABARITS UNIVERSELS (copier-coller, remplir les {})

**E.1 Prompt image (7 blocs, dans l'ordre) :**
`{CADRAGE : vertical 9:16 portrait composition, tall framing | horizontal 16:9 landscape composition, wide framing}` · `{SUJET-VERS : une phrase VISUELLE = métaphore du vers, jamais le texte literal, intensité lumineuse précisée (dim/moderate/full)}` · `{HÉROS : bloc §A.6 recopié à l'identique}` · `{PLAN : wide (refrains/show) | medium (narration) | close-up (émotion/pont) — alterner dans la salve}` · `{SUFFIXE : §E.3}` · `{ZONE : vers → darker, less busy lower third with soft bokeh for lyric text readability | intro/covers 9:16 → large dark negative space across the top quarter | covers 16:9 → left third | endcard → center}` · `{INTERDITS : no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage}` + anti-hors-cadre `full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible`.

**E.2 Écriture SUJET-VERS (méthode) :** verbe d'action + objet métaphorique + émotion ; fumée/lumière/eau pour l'abstrait ; jamais d'objets à risque modération (armes, retenue physique) → substituts (fumée pesante, silhouettes floues, mains tendues).

**E.3 Suffixes canoniques :**
B : `deep blue-black night, warm amber backlight, subtle electric cyan rim light, wet asphalt reflections, atmospheric haze, crushed blacks with cyan highlights, moody anime-seinen cinematic grading, 35mm film grain`
A : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading`

**E.4 Endcard/crédits :** `{TITRE cursive 110}` · `{LABEL / ARTISTE}` · `{GENRE} · {ANNÉE}` · `{TÉLÉPHONES}` · `{EMAILS}` · `{@HANDLE}` · `{SIGNATURE}`.

**E.5 Tags ID3 :** voir D.4 ; USLT = paroles sans timestamps ; APIC = cover carrée.

**E.6 Termux :** `mkdir -p /storage/emulated/0/Web+ && cd /storage/emulated/0/Web+ && curl -fL --retry 5 --retry-delay 3 -C - -o "{FICHIER}" "https://raw.githubusercontent.com/{OWNER}/{REPO}/{HASH}/livrables/{FICHIER}"` avec `HASH = git rev-parse HEAD` vérifié AVANT partage (le commit doit contenir les livrables).

---

## §F. NOMMAGE & RÉFÉRENCES

`assets/raw/{portrait|landscape}/s{slot:02d}_{motclé}.png` (s00 intro, s{N+1} endcard) · `work/fonds_{format}/f{slot:02d}.jpg` · `livrables/{Titre}_9x16_v{N}.mp4`, `{Titre}_16x9_YT_v{N}.mp4`, `cover_{titre}_9x16.jpg`, `cover_{titre}_1080x1080.jpg`, `{Titre}_master_320k.mp3` · `PROMPTS_IMAGES_{Titre}.md` (catalogue prompts séparés) · `<Titre>.lrc`.

## 📜 Historique
- **v5.0** — UNIVERSALISATION : §A analyse auto tout format · §B questionnaire unique 8 questions avec défauts (« direct/confiance » = défauts) · §E gabarits à trous pour tout morceau · heuristiques charte/moment fort · pièges covers (cigarette, enseignes) · hérite v4.9.1 (cold-open moment fort, DSKY✓, anti-mélange, quotas, scripts versionnés, Termux).
- v4.x : productions & leçons archivées (`PROMPT_UNIVERSEL_v4.8.2.md`, `PROMPT_UNIVERSEL_v4.9.md`).

**Signature :** « Wolof TechStein beat wê ! » ⚡
