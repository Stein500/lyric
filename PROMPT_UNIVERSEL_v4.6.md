# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v4.6 (FINALE RIGOUREUSE)

**Artiste :** Daïsky · **Projet de référence :** *L'amour est la réponse* (FR/Wolof)
**Utilisation :** Référence OBLIGATOIRE pour tous les futurs clips lyrics Daïsky Prod / TechStein. Toute déviation doit être validée.

---

## 🚨 0. CORRECTION DU DÉSYNCHRONISME (défaut « après 2 min ») — v4.6

> **Problème observé :** après ~1:50–2:00, l'image/la parole affichée ne suit plus les paroles chantées ; l'image donne parfois l'impression de se figer alors que le son continue.
>
> **Cause racine (diagnostiquée) :** la vidéo était découpée en **segments encodés séparément** puis concaténée (`concat demuxer`). Chaque clip est quantifié en **nombre entier de frames** (`round(dur*FPS)`), l'erreur s'**cumule** sur ~34 segments, et surtout la phase de **maintien** d'un vers est **rendue une seule fois puis répétée** → image *statique* + décalage de minutage des paroles vs l'audio réel.

### ✅ SOLUTION RECOMMANDÉE — A : FLUX CONTINU FRAME-ACCURATE (0 dérive)

- Rendre **un seul flux d'images continu** de `ceil((durée_chanson + endcard) * FPS)` frames, où chaque frame `i` correspond **exactement** au temps `t = i/FPS`.
- Affecter la parole/le fond **par interpolation linéaire sur le temps** (pas par sommation de clips) → **zéro accumulation d'erreur**.
- La durée vidéo est donc **construite à partir du nombre de frames** = s'aligne exactement sur l'audio.
- **Aucun** concat ni re-encodage par clip : un seul passe `image2pipe → libx264`, puis mux avec l'audio master **pad** (`apad`) pour couvrir l'endcard.

### SOLUTION B — CONCAT NORMALISÉ (si on garde les clips)
- Forcer **exactement** la durée de chaque clip via `-t` **et** `-vsync cfr` + `setpts=PTS-STARTPTS` (horloge continue).
- Concaténer via **filtre** `concat` (pas demuxer `-c copy`) pour une horloge unique, ou avec `settb=AVTB` identique sur tous les clips.
- Vérif : `showinfo` à chaque frontière prouve que les timestamps sont contigus et égaux à la durée cible.

### SOLUTION C — SOUS-TITRES ASS MINUTÉS SUR L'AUDIO (le plus propre pour le texte)
- Générer la vidéo de fond comme **un seul long métrage** (chaque image = sa durée exacte, en une commande concat filtre), **puis** brûler les paroles via un fichier **.ass dont les timestamps sont calés sur l'audio réel** (`fad`, `\t`).
- Comme le texte est minuté par `Dialog Start/End` réels (et non par les coupes d'image), **aucune dérive possible** du texte, indépendamment du montage.

### ✅ VÉRIFICATIONS OBLIGATOIRES (à l'appui)
1. `ffmpeg -i` : **durer vidéo (frames) ≈ durée audio à ±0,05 s** (calcul : `nb_frames / fps`).
2. **Frontières** : extraire une frame à chaque `start` de vers → la parole affichée correspond au vers attendu (check visuel sur les 3 sections clés : début V1, milieu V2, 2:00+, fin).
3. **Aucune frame statique longue** : pendant le maintien, appliquer un **Ken Burns léger (zoom/pan lent)** + **vague continue** → jamais d'image figée.
4. Blackdetect = 0. Badge **EN HAUT-GAUCHE** identique partout (zéro dérive).
5. Écran de fin présent + contact lisible + mux audio pad couvrant l'endcard.

---

## 🧭 NOUVEAUTÉS v4.6 (synthèse)

1. **Désynchronisme corrigé** via flux continu frame-accurate (recommandé) + 3 solutions (voir §0).
2. **Animation continue pendant le maintien** : Ken Burns + vague → aucune image statique.
3. **Écran de fin (crédits + CONTACT)** obligatoire en fin de chaque vidéo.
4. **Tags / métadonnées ID3** remplis sur TOUS les MP3 (voir §tags).
5. **Badge / CTA = EN HAUT-GAUCHE** (position fixe).
6. **Paysage 16:9 (YouTube) + 9:16 (TikTok)** couverts par salves.
7. **Effet « VAGUE »** sur apparition/disparition des vers.
8. **Musical-only** intro & outro.
9. **Cover de publication** (TikTok + YouTube) Disney/anime + titre cursive + @daiskypro.
10. **Masterisation MP3 -14 LUFS**.

---

## 🏷 CONTACT & CRÉDITS (écran de fin + tags)

### Contacts officiels
- **Téléphones :** `229 01 61 16 24 08 · 229 01 49 11 49 51`
- **Emails :** `daiskypro@proton.me` (principal) · `daiskyproduction@gmail.com` · `techsteinsecureway@gmail.com`
- **Handles :** `@daiskypro`

### Crédits écran de fin
- Titre « L'amour est la réponse » · Label **Daïsky Prod / TechStein** · Artiste **Daïsky**
- **Genre** Rock · Afro-Rock · World · **Année** 2026 · Badge « ⚡ DAÏSKY PROD » + @daiskypro

---

## 📦 TAGS / MÉTADONNÉES ID3 (obligatoire sur les MP3)

| Champ | Valeur |
|---|---|
| TIT2 | `L'amour est la réponse` |
| TPE1 | `Daïsky` |
| TALB | `TechStein Prod` |
| TPE2 | `Daïsky Prod` |
| TPUB | `TechStein / Daïsky Prod` |
| TCOM | `TechStein · Daïsky` |
| TCON (genre) | `Rock / Afro-Rock / World` |
| TDRC (année) | `2026` |
| TXXX contact | `Tel: 2290161162408 / 2290149114951` |
| TXXX email | `daiskypro@proton.me · daiskyproduction@gmail.com · techsteinsecureway@gmail.com` |
| TXXX producer | `TechStein` |
| TXXX label | `Daïsky Prod` |
| USLT | paroles complètes |

---

## 🧱 0bis. ANTI-RESET & RÈGLES GIT
- Branche `arena/<id>-<slug>` ; commit + push après chaque étape majeure.
- `livrables/` JAMAIS dans `.gitignore` ; `.venv/`, `work/`, `*.pyc` dedans.
- `PROGRESS.md` à jour ; vérifier `git rev-parse HEAD` avant de partager une URL.
- Ne jamais committer ffmpeg/ffprobe/venv.

## 🏷 RÈGLE D'OR ABSOLUE — BADGE / CTA
- Badge « ⚡ DAÏSKY PROD » (+ CTA @daiskypro) = **100 % STATIQUE**, **EN HAUT-GAUCHE**, même taille/position/police/couleurs sur toutes les frames. Incrusté en POST (PIL/ASS), jamais dans l'image source. Jamais recouvert par les sous-titres.

## 🎨 1. CHARTE GRAPHIQUE
- **A. Mixte (amour)** par défaut : coucher de soleil chaud, halo doré, bokeh, grain 35 mm, formes soulignées classe + touches cyan/ambre. Suffixe : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading, no text, no watermark, no logo`.
- **B. Dark Trap / Lightning** option (titres sombres) : éclairs cyan/ambre, reflets mouillés, noir animé seinen.
- **Interdit** : AUCUN texte/logo généré par IA dans l'image source ; pas de wrap manuel.

## 🖼 2. IMAGES
- 20 portraits **9:16** + 20 paysages **16:9**. **10 max par salve**, image d'ancrage validée. Un **vers = une image**. `assets/raw/portrait/` ou `assets/raw/landscape/`.

## 💫 3. EFFET VAGUE (non statique)
- Apparition : lettres montent/ondulent une à une (staggered). Disparition : cascade inversée. **Ondulation continue pendant tout le maintien** (pas d'image figée). Transition ~0,9 s. Rendu image par image (PIL). **+ Ken Burns léger** sur le fond pendant le maintien.

## 🎞 4. MONTAGE PIPELINE (v4.6 — frame-accurate)
1. Pré-calcul des fonds : upscale + letterbox + badge **haut-gauche** → JPEG q92.
2. **Rendu d'UN SEUL flux continu** : `ceil((durée + endcard)*FPS)` frames, affectation du vers par temps (`t=frame_index/FPS`), encodé en une passe `image2pipe -framerate FPS -vcodec mjpeg -i - → libx264`.
3. **Mux avec audio master** pad (`apad`) pour couvrir l'endcard + `afade=t=out:st=DUR-3:d=3` + `vf fade` identique.
4. Deux exports : `*_9x16_vN.mp4` et `*_16x9_YT_vN.mp4`.

## 🖼 5. COVER DE PUBLICATION
- Couple **Disney/anime** (inspiré des photos de l'artiste) + éclair doré + cœur lumineux + dégradé cyan/ambre.
- Titre en **grande cursive GreatVibes** + sous-titre + **@daiskypro** haut-gauche.
- `cover_daïsky_9x16.jpg` (1080×1920) & `cover_daïsky_16x9.jpg` (1920×1080).

## 🎧 6. MASTERISATION MP3
- **-14 LUFS** (ebur128), TP ≤ -1,5 dBTP, `highpass=f=30, lowpass=f=18000`, loudnorm 2 passes linéaire, durée conservée, `livrables/*_MASTER.mp3`.

## ✅ 7. VÉRIFICATIONS OBLIGATOIRES AVANT COMMIT
1. Durée exacte (chanson + endcard) : `nb_frames/fps ≈ audio ±0,05 s`.
2. Blackdetect = 0. 3. Frontieres de vers : frame au start de chaque section clé = bonne parole. 4. Aucune image figée (Ken Burns/vague pendant maintien). 5. Badge haut-gauche identique. 6. Écran de fin + contact. 7. MP3 tags remplis. 8. Cover lisible.

## 📦 8. TÉLÉCHARGEMENTS (REPRENABLE)
- Dest `/storage/emulated/0/Web+/` ; `curl -fL --retry 5 --retry-delay 3 -C - -o "fichier" "https://raw.githubusercontent.com/Stein500/lyric/<HASH>/livrables/..."`.

---

**Signature :** « Wolof TechStein beat wê ! » ⚡
