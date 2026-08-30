# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v4.5 (FINALE RIGOUREUSE)

**Artiste :** Daïsky · **Projet de référence :** *L'amour est la réponse* (FR/Wolof)
**Utilisation :** Référence OBLIGATOIRE pour tous les futurs clips lyrics Daïsky Prod / TechStein. Toute déviation doit être validée.

---

## 🧭 0. NOUVEAUTÉS v4.5

1. **Écran de fin (crédits + CONTACT)** obligatoire à la fin de CHAQUE vidéo générée, pour permettre le contact facile.
2. **Tags / métadonnées (ID3)** remplis sur TOUS les MP3 livrés.
3. **Badge / CTA = EN HAUT-GAUCHE** (position fixe définitive).
4. **Format PAYSAGE 16:9 (YouTube)** + 9:16 (TikTok). Couvert par salves.
5. **Effet « VAGUE »** sur apparition/disparition des vers.
6. **Musical-only** : intro & outro sans paroles.
7. **Cover de publication** (TikTok + YouTube), style Disney/anime, titre en cursive + @daiskypro.
8. **Masterisation MP3 -14 LUFS**.

---

## 🏷 CONTACT & CRÉDITS (à incruster en fin de vidéo + en tags)

### Contacts officiels
- **Téléphones :** `229 01 61 16 24 08 · 229 01 49 11 49 51`
- **Emails :** `daiskypro@proton.me` (principal) · `daiskyproduction@gmail.com` · `techsteinsecureway@gmail.com`
- **Réseaau / Handles :** `@daiskypro`

### Crédits à afficher (écran de fin)
- **Titre :** « L'amour est la réponse »
- **Label / Maison :** Daïsky Prod / TechStein
- **Artiste :** Daïsky
- **Genre :** Rock · Afro-Rock · World
- **Année :** 2026
- **Badge :** « ⚡ DAÏSKY PROD » + **@daiskypro**

---

## 📦 METADONNÉES / TAGS (fill systématiquement sur les MP3)

| Champ ID3 | Valeur |
|---|---|
| Titre (TIT2) | `L'amour est la réponse` |
| Artiste (TPE1) | `Daïsky` |
| Album / Label (TALB) | `TechStein Prod` |
| Album artist (TPE2) | `Daïsky Prod` |
| Label (TPUB) | `TechStein / Daïsky Prod` |
| Compositeur (TCOM) | `TechStein · Daïsky` |
| Genre (TCON) | `Rock / Afro-Rock / World` |
| Année (TDRC) | `2026` |
| Contact (TXXX) | `Tel: 2290161162408 / 2290149114951` |
| Email (TXXX) | `daiskypro@proton.me · daiskyproduction@gmail.com · techsteinsecureway@gmail.com` |
| Producer (TXXX) | `TechStein` |
| Label (TXXX) | `Daïsky Prod` |
| Paroles (USLT) | paroles complètes |

---

## 🧱 0bis. ANTI-RESET & RÈGLES GIT

- Branche `arena/<id>-<slug>`. Commit + push après chaque étape majeure.
- `livrables/` JAMAIS dans `.gitignore` ; `.venv/`, `work/`, `*.pyc` dedans.
- Garder `PROGRESS.md` à jour et toujours vérifier `git rev-parse HEAD` avant de partager une URL.
- Ne jamais committer ffmpeg/ffprobe/venv.

---

## 🏷 RÈGLE D'OR ABSOLUE — BADGE / CTA

> **Badge « ⚡ DAÏSKY PROD » (et tout CTA : @daiskypro, « abonne-toi », crédits) = 100 % STATIQUE.**
> - **Position : EN HAUT-GAUCHE** (par défaut) — même taille/position/police/couleurs sur TOUTES les frames.
> - AUCUN waver/animation/zoom/apparition.
> - Incrusté en **POST (PIL/ASS)**, jamais peint dans l'image source.
> - Au-dessus de la vidéo, jamais recouvert par les sous-titres.

---

## 🎨 1. CHARTE GRAPHIQUE

### A. Style mixte (amour) — défaut
Coucher de soleil chaud, halo doré, bokeh, grain 35 mm, formes soulignées classe + touches cyan/ambre.
Suffixe : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading, no text, no watermark, no logo`.

### B. Style Dark Trap / Lightning — option (titres sombres)
Éclairs cyan/ambre, reflets mouillés, noir animé seinen.

### Interdit
- AUCUN texte / logo généré par IA dans l'image source. Tout incrusté en POST.
- Pas de wrap manuel des vers (wrap auto au mot).

---

## 🖼 2. IMAGES

- 20 portraits **9:16** (1080×1920) TikTok + 20 paysages **16:9** (1376×768 → 1920×1080) YouTube.
- **10 images max par salve**, image d'ancrage validée.
- Un **vers = une image**.
- Nomenclature `NN_descriptif_courte.jpg` dans `assets/raw/portrait/` ou `assets/raw/landscape/`.

---

## 💫 3. EFFET VAGUE

- Apparition : lettres qui **montent/ondulent** et apparaissent une à une (staggered).
- Disparition : lettres qui **descendent/s'évanouissent** en cascade.
- Ondulation continue par lettre. Transition ~0,9 s. Rendu image par image (PIL).

---

## 🎞 4. MONTAGE PIPELINE

1. Frames PIL : resize/letterbox + badge **haut-gauche** + cursive animée (vague) → JPEG q92.
2. Clips silencieux par segment : `-loop 1 -i frame.jpg -t dur -f lavfi -i anullsrc=... -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -r 24 -c:a aac`.
3. Concat demuxer `concat.txt` → `-f concat -safe 0 -c copy` (**0 trou noir**).
4. **Écran de fin** concaténé (clip statique de l'endcard, ~6 s) — puis mux audio étendu (`apad`) pour couvrir l'endcard + fades.
- Deux exports : `*_9x16_vN.mp4` et `*_16x9_YT_vN.mp4`.

---

## 🖼 5. COVER DE PUBLICATION

- Visuel : couple **Disney/anime** (inspiré des photos de l'artiste) + éclair doré + cœur lumineux + dégradé cyan/ambre.
- Titre en **grande cursive GreatVibes** + sous-titre.
- **@daiskypro** en haut-gauche avec éclair.
- Livrables `cover_daïsky_9x16.jpg` (1080×1920) et `cover_daïsky_16x9.jpg` (1920×1080).

---

## 🎧 6. MASTERISATION MP3

- Objectif **-14 LUFS** (ebur128), TP ≤ -1,5 dBTP.
- `highpass=f=30, lowpass=f=18000` · loudnorm 2 passes linéaire.
- Durée conservée. Nom `livrables/*_MASTER.mp3`.

---

## ✅ 7. VÉRIFICATIONS OBLIGATOIRES AVANT COMMIT

1. Durée exacte (chanson + endcard). 2. Blackdetect = 0. 3. Frame-by-frame fin : badge identique (haut-gauche), écran de fin présent avec contact, pas de coupure. 4. Vers intacts. 5. MP3 tags remplis. 6. Cover lisible. 7. Poids cohérent.

---

## 📦 8. TÉLÉCHARGEMENTS (REPRENABLE)

- Dest `/storage/emulated/0/Web+/` ; `curl -fL --retry 5 --retry-delay 3 -C - -o "fichier" "https://raw.githubusercontent.com/Stein500/lyric/<HASH>/livrables/..."`.

---

**Signature :** « Wolof TechStein beat wê ! » ⚡
