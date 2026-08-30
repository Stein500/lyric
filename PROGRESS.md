# 🎬 PROGRESS — « L'amour est la réponse » — Daïsky

**Style :** Mixte — amour/légèreté/chaleur + touches cyan/ambre (écart à la charte Dark Trap validé par l'artiste).
**Format demandé :** TikTok 9:16 (1080×1920).
**Audio :** `L'amour est la réponse - Daïsky.mp3` — durée exacte **214,92 s (3:34,9)**.

---

## ✅ État d'avancement

- [x] **Étape 1 — Cadre** : dossiers `assets/raw/portrait/`, `assets/raw/landscape/`, `livrables/`, `work/prep/`, `.gitignore` (livrables/ PAS exclu), `PROGRESS.md`.
- [x] **Étape 2 — Image d'ancrage** : `01_ancrage_couple_enlace.jpg` validée (tendresse + sensualité classe, diffuse TikTok).
- [x] **Étape 3 — Salve 1 (10 images)** : 10 portraits 9:16 générés dans `assets/raw/portrait/`.
- [x] **Étape 4 — Frames préparées** : up-scale 1080×1920 + **écriture cursive** (GreatVibes) + **badge statique « ⚡ DAÏSKY PROD »** (éclair vectoriel dessiné, même position/taille partout).
- [x] **Étape 5 — Minutage** : timeline 34 plans (3:34,92 découpée selon les paroles) ; **après 1:50 → horaires hardcodés en secondes** (règle v4.2).
- [x] **Étape 6 — Montage** : prép → clips → **concat demuxer (zéro trou noir)** → burn + mux audio → **fade-in 0,3 s / fade-out 3 s**.
- [x] **Étape 7 — Vérifs auto** : durée exacte (3:34,90 ✓), **blackdetect = 0 trou noir > 300 ms** ✓, frame-by-frame des 30 dernières secondes + sections clés ✓ (badge fixe, fade-out propre).
- [ ] **Étape 8 — Commit + push** : à faire.
- [ ] **Étape 9 — Partage** : commande curl `-C -` (voir section 6).

---

## 🖼 Images générées (10 portraits 9:16)

| # | Fichier | Section |
|---|---|---|
| 01 | `01_ancrage_couple_enlace.jpg` | Refrain / couple tendre |
| 02 | `02_intro_appel_wolof.jpg` | Intro « Wolof TechStein beat wê ! » |
| 03 | `03_refrain_danse_liberte.jpg` | Danse / liberté |
| 04 | `04_couplet1_brise_chaines.jpg` | Couplet 1 « Brise les chaînes » |
| 05 | `05_prerefrain_coeurs_feu.jpg` | Pré-refrain / cœurs |
| 06 | `06_refrain2_unite_musique.jpg` | Refrain 2 / unité |
| 07 | `07_couplet2_flamme_univers.jpg` | Couplet 2 / flamme cosmique |
| 08 | `08_unite_sans_frontieres.jpg` | Sans frontières |
| 09 | `09_passion_connection.jpg` | Passion |
| 10 | `10_final_union_puissance.jpg` | Final / union |

---

## 🎬 Livrables TikTok 9:16

- `livrables/L'amour_est_la_reponse_Daïsky_9x16_v1.mp4`
  - Résolution **1080×1920** (9:16), 25 fps, H.264, AAC.
  - Durée **3:34,90** (calée sur l'audio).
  - **13 MB**. Badge statique, sous-titres en **cursive GreatVibes**.
  - **0 trou noir**. Fade-in 0,3 s / fade-out 3 s.

---

## ⚠️ Notes / points d'attention

1. **Outro instrumentale** : les paroles fournies s'arrêtent à **2:56**, mais l'audio dure **3:34,9**. L'outro (~39 s) est couverte par le plan final « union » + badge (sans paroles).
   - Si l'artiste a **des paroles pour l'outro** ou veut couper la chanson à 2:56, il faut me le dire pour ajuster.
2. **Format 16:9 (YouTube)** non encore généré (le prompt v4.3 demande aussi 20 paysages) — demandé pour la suite.
3. **Pas de texte peint dans les images source** (règle d'or v4.3) : tout le texte est incrusté en POST.

---

## 🧰 Env / Outils

- venv `.venv` (pillow, mutagen, imageio-ffmpeg) — NON commité (`.gitignore`).
- **FFmpeg** fourni par `imageio-ffmpeg` (binaire statique, hors dépôt).
- **Polices** : GreatVibes + Pacifico dans `assets/fonts/` (le .ttf est à garder, le `.licence` en gitignore).
- Le rendu des paroles en **cursive** a été validé sur frames (accents FR OK).

---

**Signature :** « Wolof TechStein beat wê ! » ⚡
