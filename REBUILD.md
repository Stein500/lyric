# 🛡️ REBUILD — ANTI-RESET TOTAL

> **Aucun travail ne vit uniquement dans le workspace.** Ce document explique comment tout récupérer / reconstruire en 3 commandes, même après un reset complet de l'espace.

---

## 🎯 Principe (1 ligne)
Tout le nécessaire pour reconstruire les livrables finaux est **commité sur GitHub** : scripts Python, assets images, audio source, prompts, procédures. Seul le venv Python est régénérable automatiquement.

---

## 📦 Récupération après un reset

```bash
# 1. Récupérer le repo (ou juste faire git fetch si le dossier existe déjà)
cd ~
git clone https://github.com/Stein500/lyric.git 2>/dev/null || cd lyric && git fetch origin && git reset --hard origin/arena/01a0386c-lyric
cd lyric

# 2. Rebuild automatique venv
bash setup_venv.sh

# 3. Reconstruire TOUS les livrables (couverture + 2 vidéos + MP3 + vérifications)
bash build_all.sh
```

➡️ Après ça, `livrables/` contient exactement les mêmes fichiers que sur le dernier commit, vérifiés.

---

## 📋 Ce qui est commité (donc restaurable par git pull/reset --hard)
✅ `Lightning_is_my_name_Daïsky.m4a` — audio source (169.48s)  
✅ `assets/raw/portrait/*.jpg` — les 30 portraits 9:16  
✅ `assets/cover/*.jpg` — cover pro carrée (1400 + 3000)  
✅ `livrables/*.mp4` et `*.mp3` — les 3 livrables finaux (9:16, 16:9, MP3)  
✅ `build_video.py` — pipeline vidéo complet (minutage dur v4, vérifications)  
✅ `build_cover.py` — génération cover pro  
✅ `build_mp3.py` — MP3 320kbps + tags ID3 propres + cover embarquée  
✅ `setup_venv.sh` — recrée le venv en 1 commande  
✅ `build_all.sh` — build complet en 1 commande  
✅ `PROMPT_UNIVERSEL_MAJ_v4.2.md` — prompt de production définitif  
✅ `PROGRESS.md` — suivi d'avancement  
✅ `.gitignore` — n'exclut PAS `livrables/` ni `assets/`

## 🔁 Ce qui est régénéré automatiquement (pas besoin de le commiter)
- `tools_venv/` — recréé par `setup_venv.sh` (ffmpeg static est inclus via pip imageio-ffmpeg)
- `work/` et ses sous-dossiers (clips, concat, subs, frames de vérif) — recréés par `build_all.sh`

---

## ✅ Vérification post-rebuild
Après `build_all.sh` :
- 🍿 **Vidéos** : durée 169.45s ±0.1s, 0 trou noir >300ms (test auto par blackdetect)
- 🎧 **MP3** : 320 kbps CBR, cover front (500 KB), tags ID3 : `TIT2`, `TPE1`, `TALB`, `TCON`, `TPUB`, `APIC`, custom `TXXX:PRODUCER/STUDIO/CONTACT/LINKTREE`, 0 mention "suno" / "c2pa"
- Fichiers finaux dans `livrables/` :
  - `Daïsky - Lightning Is My Name (Lyrics 9x16).mp4` — 1080×1920, ~20 MB
  - `Daïsky - Lightning Is My Name (Lyrics 16x9).mp4` — 1920×1080 letterbox, ~13 MB
  - `Daïsky - Lightning Is My Name.mp3` — 320 kbps, ~7 MB, cover embarquée

---

## 🚫 Règles anti-reset à respecter pour les futurs ajouts
1. **Jamais de travail uniquement dans `work/`** : les sorties importantes vont dans `livrables/` qui est commité.
2. **Tout script nouveau doit être à la racine**, dans `.gitignore` on n'exclut jamais les `.py` et `.sh` à la racine.
3. **Les assets images et audio** vont dans `assets/` et sont commités (pas dans le venv ni dans work/).
4. **Après chaque modification importante :** `git add -A && git commit -m "message" && git push origin arena/01a0386c-lyric`.
5. **Jamais de binaire géant** (ffmpeg, venv) commité : on les reconstruit via `setup_venv.sh`.
6. **Le prompt de production** (`PROMPT_UNIVERSEL_MAJ_v*.md`) doit être mis à jour à chaque nouvelle règle, avec version incrémentée.
7. **Avant de partager une URL de téléchargement**, vérifier le hash de commit avec `git rev-parse HEAD` et construire l'URL `https://raw.githubusercontent.com/Stein500/lyric/<HASH>/livrables/<nom_fichier>`.
