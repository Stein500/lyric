# PROGRESS.md — État du chantier lyrics (Stein500/lyric)

> Mis à jour à chaque étape majeure. Commit + push après chaque case cochée.
> Règle anti-reset : `git fetch origin arena/<branche> && git reset --hard FETCH_HEAD`.

## 📄 Prompt universel — v4.9 (courant)
- Fichier `PROMPT_UNIVERSEL_v4.9.md` (canonique) : badge **DSKY✓** haut-CENTRE discret+visible (§5.1) · CTA like/abonne/commente **0–2 s** sur lyrics ET teaser (§5.2) · icône partage IA **mi-vidéo** (§5.3) · **teaser obligatoire** après chaque clip à partir de **2 images retravaillées par l'IA** (§17). Mises à jour artiste **intégrées**. v4.8.2 / v4.7 = historique.

## 🧰 Environnement
- venv dans `.venv` (non versionné) — reconstruire : `bash pipeline/setup_env.sh`
- ffmpeg via imageio-ffmpeg (v7.0.2), jamais committé · fontes DejaVu versionnées `assets/fonts/`
- Dossiers versionnés : `assets/raw/{portrait,landscape}/`, `assets/icons/`, `livrables/` (jamais ignoré), `pipeline/` (scripts)

---

## 🎵 Projet en cours : *Yafoy t'es encore là* — Daïsky / TechStein
- **Style :** Rock'n'Roll / Hard Rock · **140 BPM** · Duo vocal (masc. grave / fém. claire) · **4:05**
- **Sources :** `yafoy.txt` (paroles + maquette timing) · `Yafoy t'es encore là.mp3`

### Analyse audio (v1)
| Paramètre | Valeur |
|---|---|
| Durée exacte | **244,99 s = 4:05** (mutagen) |
| LUFS intégrés | ~ -14,5 dB (≈ cible -14, déjà masterisé) |
| True Peak | ~ -2,5 dBTP |
| Conclusion | utiliser le MP3 fourni comme master (pas de remaster agressif) |

### Décisions VALIDÉES par l'artiste (2026-09-09)
- [x] **Charte : S — Printemps ensoleillé** (changement artiste 2026-09-09 : paysages de printemps ensoleillés en arrière-plan, v4.9.1 §6 — remplace la charte P initialement choisie)
- [x] **Budget images : 34 + 3 solo = 37 en 9:16** (32 lignes uniques + intro + endcard + 2-3 images dédiées au solo guitare 2:48→3:30)
- [x] **Police paroles : ÉCRITURE SCRIPT ÉLÉGANTE** (GreatVibes, à fournir dans `work/fonts/` ou `assets/fonts/`) — badge/endcard/contacts restent DejaVu Bold (§14)
- [x] **Périmètre actuel : 9:16 cursive + covers + MP3 taggé + prompt à jour.** 16:9 et teaser = plus tard.
- [ ] Icône partage IA `assets/icons/share_daisky.png` — à générer + valider

### Pipeline *Yafoy*
- [x] Cadre : PROMPT v4.9, .gitignore, PROGRESS.md, assets/fonts, setup_env, venv OK
- [ ] Maquette timing → onsets validés par écoute (fichier `work/timeline_yafoy.json`)
- [ ] Image(s) d'ancrage + maquette badge DSKY✓ / CTA / vers → validation
- [ ] Salves 9:16 (34 imgs → 4 salves) → planches contact + validations
- [ ] Salves 16:9 (34 imgs) → planches contact + validations
- [ ] Pré-calcul fonds → rendu 9:16 (SOLUTION A) → vérifs §12
- [ ] Rendu 16:9
- [ ] MP3 master + tags ID3 (si besoin)
- [ ] Covers (2 formats, titre IA + badge DSKY✓ post)
- [ ] **Teaser §17** : 2 images retravaillées IA + CTA 0–2 s + annonce sortie
- [ ] CTA like/sub/comment 0→2 s sur lyrics (§5.2) + icône partage mi-vidéo (§5.3)
- [ ] Vérifs finales §12 + livrables dans `livrables/`
- [ ] Commit final + commandes curl `-C -` reprenables avec hash

### Maquette timing (issue de yafoy.txt — à confirmer à l'écoute)
```
INTRO        Wolof TechStein beat wê!         4.0 – 6.0
INTRO        Yeah... Yafoy t'es encore...     6.0 – 12.0
R1           4 x « Yafoy t'es encore … »      12.0 – 25.5
R1 (tag)     Wolof TechStein beat wê!         25.5 – 27.5
C1           8 lignes                         34.0 – 61.0
PR1          4 x « T'es encore … »            61.0 – 74.5
R2           = R1 (réutilise)                 74.5 – 91.0
C2           8 lignes                         96.0 – 123.0
PR2          = PR1                            123.0 – 137.0
PONT         4 lignes (calme, piano/violon)   144.0 – 168.5
[solo]       guitare                          168.5 – 210.0
RF           = R1                             210.0 – 226.0
OUTRO        Wolof TechStein beat wê...       226.0 – 235.0
OUTRO        (Yafoy... t'es encore...)        235.0 – 240.0
fin audio / fade                            ~240.0 – 244.99
```
- **Lignes uniques : 32** → proposition **34 images par format** (+2 : intro musicale s00 + endcard)
- Refrains R2 & RF et PR2 réutilisent les images de R1 / PR1 (règle §7 R1)
