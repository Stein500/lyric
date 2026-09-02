# 🚧 PROGRESS.md — Clip lyrics « Je suis pauvre mais je kiffe »

**Artiste :** Daïsky · **Label :** Daïsky Prod / TechStein
**Spéc suivie :** `PROMPT_UNIVERSEL_v4.7.md` (la plus récente du dépôt — v4.7 > v4.3 > v4.2)
**Branche :** `arena/01a06299-lyric`
**Dernière mise à jour :** 2026-09-02

---

## 📊 Chiffres mesurés (pas estimés)

| Donnée | Valeur | Comment |
|---|---|---|
| Audio source | `Jsuis pauvre mais je kiffe 2.mp3` | MP3 VBR 186 kb/s, 48 kHz, stéréo |
| **Durée exacte** | **261,04 s (4:21.04)** | 12 529 919 échantillons PCM décodés / 48 000 |
| Loudness entrée | **−13,51 LUFS / −0,12 dBTP / LRA 7,20** | loudnorm passe 1 (`print_format=json`) |
| offset passe 2 | **−0,77** | `target_offset` du JSON → option `offset=` |
| **BPM** | **≈ 106–107** | autocorrélation enveloppe d'énergie |
| Fondu final audio | **253,9 s → 259,6 s** | profil dBFS 1 s + détection de seuil |
| **Nombre de vers** | **62** | parse de `Je suis Pauvre et riche.txt` |
| Fin du dernier vers | **245,00 s (4:05)** | plage explicite artiste `4:01-4:05` |
| Musique sans vers à la fin | **245 s → 253,9 s (≈ 9 s)** | ⚠️ à trancher avec l'artiste |

**Budget images (v4.7 §7, règle « 1 vers = 1 image ») : 62 + 2 = 64 par format.**
→ 64 portraits 9:16 (**7 salves** : 10+10+10+10+10+10+4) + 64 paysages 16:9 (**7 salves**) + 1 base cover ×2.
Slots : `s00` = fond intro musicale (0 → 9 s) · `s01…s62` = vers 1→62 · `s63` = fond endcard.

---

## ✅ Étapes

### 0. Cadre & analyse
- [x] Lecture de la spec la plus récente (`PROMPT_UNIVERSEL_v4.7.md`, 148 lignes)
- [x] Environnement reconstruit : `.venv/` (imageio-ffmpeg 7.0.2, mutagen 1.48.1, numpy 2.4.6, pillow 12.3.0) — `.venv/` et `work/` dans `.gitignore`
- [x] Durée exacte décodée + LUFS/TP/LRA + BPM + structure → `ANALYSE_AUDIO.md`
- [x] Parse des paroles → `work/timing.csv` (62 vers, `work/parse_lyrics.py`, 0 ligne non parsée)
- [x] Contrôle paroles ↔ audio (écarts < 2 s, voir `ANALYSE_AUDIO.md` §4)
- [x] `.gitignore` (livrables/ **pas** exclu)
- [x] PROGRESS.md

### 1. Décisions artistiques — ⏳ EN ATTENTE DE L'ARTISTE
- [ ] Charte : B (dark trap) / A (mixte amour) / **hybride B + A sur le pont (178–201 s)**
- [ ] Traitement des 9 s de musique sans vers (245 → 253,9 s)
- [ ] Ordre des formats (9:16 d'abord ?) + périmètre (vidéo / MP3 master / covers)
- [ ] Titre exact + année pour les tags ID3 et l'endcard

### 2. Image d'ancrage
- [x] Ancrage charte **B** généré : `assets/raw/portrait/s00_ANCRAGE_darktrap_lightning.png` (768×1376, upscale LANCZOS → 1080×1920)
- [ ] **Validation artistique de l'ancrage** (bloquant avant la salve 1)
- [ ] Ancrage charte **A** (si hybride retenu)
- [ ] Maquette badge « ⚡ DAÏSKY PROD » + vers (police, taille, position haut-gauche 36,36)

### 3. Salves d'images (7 salves × 2 formats)
- [ ] Salve 1 portrait (s01–s10) · [ ] Salve 2 (s11–s20) · [ ] Salve 3 (s21–s30) · [ ] Salve 4 (s31–s40)
- [ ] Salve 5 (s41–s50) · [ ] Salve 6 (s51–s60) · [ ] Salve 7 (s61–s63)
- [ ] idem 7 salves paysage 16:9
- [ ] Base cover

### 4. Rendu (v4.7 §9, SOLUTION A — flux continu frame-accurate)
- [ ] Script `work/render.py` (30 fps, ADVANCE = 0,03 s, vague + Ken Burns, badge posé en dernier)
- [ ] Export 9:16 `livrables/Je_suis_pauvre_mais_je_kiffe_9x16_v1.mp4`
- [ ] Export 16:9 `livrables/Je_suis_pauvre_mais_je_kiffe_16x9_YT_v1.mp4`

### 5. Master MP3 + covers
- [ ] Master 2 passes loudnorm → −14 LUFS / −1,8 dBTP, 320 k, tags ID3 v4.7 §3
- [ ] `livrables/cover_..._9x16.jpg` + `_16x9.jpg`

### 6. Vérifications (v4.7 §12) & livraison
- [ ] Durée ±0,05 s · blackdetect 0 · freezedetect 0 · diff pixel aux frontières · badge statique · endcard
- [ ] Commit + push, `git rev-parse HEAD`, commandes curl `-C -` vers `/storage/emulated/0/Web+/`

---

## ⚠️ Contraintes détectées dans ce sandbox

1. **Pas d'accès réseau** (`curl` → `SSL_ERROR_SYSCALL`) → **GreatVibes-Regular.ttf introuvable**.
   Polices locales disponibles : DejaVu Sans / Sans Bold / Serif / Serif Bold (`/usr/share/fonts/truetype/dejavu/`).
2. **2 CPU / 3,9 Go RAM / 20 Go libres** → rendu 7 980 frames (9:16) en PIL pur : compter plusieurs dizaines
   de minutes par format. Faisable, mais à lancer en processus de fond.
3. ffmpeg n'est **pas** installé système : on utilise le binaire embarqué `imageio-ffmpeg` (lien `work/ffmpeg`),
   jamais commité (v4.7 §4).

**Signature :** « Wolof TechStein beat wê ! » ⚡
