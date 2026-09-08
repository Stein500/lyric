# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v4.7.2 (badge droit obligatoire + anti-coupure)

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
6. Commit + push **après CHAQUE étape** (anti-reset).

### Budget images (règle : 1 vers = une image)
`N vers + 2 (fond intro musicale + fond endcard)` **par format**.
Exemple *Le Survivant* : 47 vers + 2 = **49 images 9:16 + 49 images 16:9 + 1 base cover ×2 formats = 99 images**, 5 salves de 10 max par format.

---

## 🏷 2. CONTACT & CRÉDITS (écran de fin + tags)

- **Téléphones :** `229 01 61 16 24 08 · 229 01 49 11 49 51`
- **Emails :** `daiskypro@proton.me` (principal) · `daiskyproduction@gmail.com` · `techsteinsecureway@gmail.com`
- **Handles :** `@daiskypro`
- Écran de fin : Titre du morceau · Label **Daïsky Prod / TechStein** · Artiste **Daïsky** · Genre · **Année** · « ⚡ DAÏSKY PROD » + @daiskypro + « Wolof TechStein beat wê ! »
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

## 🏷 5. RÈGLE D'OR — BADGE / CTA

- Badge « ⚡ DAÏSKY PROD » (+ @daiskypro) = **100 % STATIQUE**, **EN HAUT-GAUCHE** (36,36 px), même taille/position/police/couleurs sur toutes les frames, posé en POST en **dernier** (jamais recouvert), carte OPAQUE + liseré cyan + éclair polygonal (pas d'emoji). **POLICE DROITE, GRASSE ET LISIBLE (DejaVu Sans Bold, fournie dans `assets/fonts/`) — JAMAIS d'écriture script/cursive sur le badge** (validé artiste : le script sur le badge est illisible). Identique sur les covers.

## 🎨 6. CHARTE GRAPHIQUE

- **A. Mixte (amour)** : coucher de soleil chaud, halo doré, bokeh, grain 35 mm — suffixe : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading, no text, no watermark, no logo`.
- **B. Dark Trap / Lightning** (titres sombres) : éclairs cyan/ambre, reflets mouillés, noir animé seinen — même suffixe technique.
- **Hybride autorisé** : B pour couplets/refrains + A pour le pont calme (ex. pont piano *Le Survivant* slots 35-38 → glow ambre au lieu de cyan).
- **Interdit** : tout texte/logo généré par l'IA dans l'image source ; wrap manuel.

## 🖼 7. IMAGES — RÈGLES ABSOLUES

> **RÈGLE 1 — UN VERS = UNE IMAGE (à lui, uniquement la sienne).**
> Chaque vers a **sa propre image, générée pour illustrer ce vers précis** — et ce, **dans CHAQUE format** : le vers n°12 possède une image portrait 9:16 **et** une image paysage 16:9, distinctes. ❌ Interdit : réutiliser l'image d'un vers pour un autre vers, partager une image entre plusieurs vers, dédoublonner.

> **RÈGLE 2 — GÉNÉRATION PAR SALVES DE 10 MAX PAR SESSION.**
> On ne génère **JAMAIS tout d'un coup** : salves de **10 images maximum par session** (limite IA dure). Exemple : 49 images = **5 salves** (10+10+10+10+9). Après **chaque salve** : planche contact → **validation artistique AVANT de lancer la suivante**. Une salve refusée = seuls les slots concernés sont régénérés.

- **Budget par format = `N vers + 2`** (fond intro musicale + fond endcard). Ex. *Le Survivant* : 47+2 = 49 par format → 98 images + 1 base cover = 99.
- **Nommage** : `assets/raw/{portrait|landscape}/s{slot:02d}_<motclé>.png` · `s00` = intro musicale · `s01…s{N}` = vers 1→N (slot = index vers + 1) · `s{N+1}` = fond endcard.
- **Ancrage** : 1 image de référence par charte (B et/ou A) validée **avant** la salve 1.
- **Arc narratif** : chaque image illustre son vers (métaphores visuelles), même héros d'un bout à l'autre, décrescendo lumineux sur l'outro, fond endcard sombre et épuré.
- Pendant les salves d'un format, on peut continuer le reste du pipeline (rendu de l'autre format, MP3…) — mais **jamais deux salves d'images dans la même session**.

## 💫 8. EFFET VAGUE + KEN BURNS

- Apparition : lettres montent une à une (staggered ~0,9 s) · Disparition : cascade inversée · **Ondulation sinusoïdale continue** (amplitude ~6 px, 0,9 Hz, phase par lettre) pendant tout le maintien.
- Rendu image par image (PIL, sprites de lettres avec glow précalculé + cache).
- Ken Burns : canvas 1,1× (1188×2112 pour 1080×1920 ; 2112×1188 pour 1920×1080), zoom 1,02→1,08 alterné par slot, pan sinusoïdal lent.

## 🎞 9. MONTAGE PIPELINE (SOLUTION A)

1. Pré-calcul fonds : upscale LANCZOS → canvas Ken Burns → JPEG q92 (`work/fonds_{portrait|landscape}/f{slot:02d}.jpg`).
2. Rendu : flux continu `ceil(durée_totale × 30)` frames, texte par fenêtres `d0/d1` (avance 0,03 s), badge posé en dernier, intro musical-only avec titre (0 → 1ʳᵉ voix), endcard à partir du fondu final.
3. Mux : `[1:a]apad=whole_dur=<total>,afade=t=out:st=<total-3>:d=3[a]` + `[0:v]fade=t=out:st=<total-3>:d=3` (PAS de fade-in : il crée des frames noires → blackdetect).
4. Exports : `livrables/<Titre>_9x16_v<N>.mp4` et `livrables/<Titre>_16x9_YT_v<N>.mp4` (crf19, veryfast, aac 192k, +faststart). Texte 9:16 : police 58, base bas H−300, max 920 px. 16:9 : police 62, base bas H−150, max 1640 px, endcard décalé à gauche (cx = 0,38×W).

## 🖼 10. COVER DE PUBLICATION

- Base IA : héros + éclair doré + cœur lumineux (ou équivalent selon titre), zones sommes réservées au texte (haut 9:16 / gauche 16:9).
- Titre **cursive GreatVibes** si `work/fonts/GreatVibes-Regular.ttf` fourni (CDN polices bloqués → **fournir le .ttf dans le repo**), sinon fallback serif incliné + glow ambre.
- Sous-titre : Daïsky · Daïsky Prod / TechStein · Genre · Année · `@daiskypro` + badge haut-gauche.
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
5. Badge statique (écart < ~4 px entre deux instants sur le même fond).
6. Écran de fin + contacts + apad.
7. MP3 : LUFS/TP/durée + tous les tags présents.
8. Cover lisible (dimensions + zone titre + badge).
9. **Texte non coupé** : audit bbox des sprites à la construction (marge glyphs ≥ 6 px des bords) + sur frames échantillonnées, aucun pixel de texte tronqué ni chevauché.

## 📦 13. TÉLÉCHARGEMENTS (REPRENABLES)

- Dest `/storage/emulated/0/Web+/` ; `curl -fL --retry 5 --retry-delay 3 -C - -o "fichier" "https://raw.githubusercontent.com/Stein500/lyric/<HASH>/livrables/..."` — **toujours vérifier `git rev-parse HEAD` avant de partager une URL**.

---

## 📜 Historique des versions
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
