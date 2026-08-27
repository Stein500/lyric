# ⚡ PROGRESS — "Motivé" — Daïsky Prod / TechStein

Repro de référence : PROMPT_UNIVERSEL_MAJ.md (v4.2).
Titre : **Motivé** — Durée audio réelle : **2:38.90** (158.90 s).
Priorité : version **TikTok / Reels (9:16)** d'abord, puis YouTube (16:9).

---

## 🔢 ÉTAT GLOBAL
- [x] Cadre, dossiers, `.gitignore` (livrables/ PAS exclu), PROGRESS.md
- [x] Lecture audio (durée) + parsing des paroles/times fournies
- [x] Univers visuel PROPOSÉ (Dark Trap / Monumental Rise) — à valider artiste
- [x] Salve 1 générée : 10 portraits 9:16 (images 01–10, hyperréel cinématique)
- [ ] Image d'ancrage (01) validée visuellement par l'artiste
- [x] Salve 2 générée : portraits 9:16 (11–20, style seine manga / cel-shaded cyan)
- [ ] Salve 3 : portraits 9:16 (21–30, bonus animé)
- [ ] Salves paysage 16:9 (pour YouTube)
- [ ] Minutage précis : tableau (start, end, text, style, fr) — après 1:50 tout en dur
- [x] Badge PIL "⚡ DAÏSKY PROD" statique bas-gauche
- [x] Montage : prép → clips → concat → burn ASS + mux audio → export 9:16 TikTok/Reels
- [x] Vérifications auto (durée + blackdetect) + frame-by-frame 30 dernières s
- [ ] Export 16:9 YouTube (à venir)
- [ ] Partage curl `-C -` reproductible

---

## 🎞 SECTION PAR SECTION (format fini 9:16)
| Section | Plage lue (audio 2:38.90) |
|---|---|
| Intro | 0:00 – 0:15 |
| Refrain 1 | 0:15 – 0:30 + tagline Wolof |
| Couplet 1 | 0:38 – 0:53 |
| Pré-refrain 1 | 0:53 – 0:57.8 (+ "c'est maintenant") |
| Refrain 2 | ~1:00 – 1:14 + tagline Wolof |
| Couplet 2 | 1:22 – 1:37 |
| Pré-refrain 2 | 1:37 – 1:44 |
| Pont | 1:44 – 1:56.5 |
| Refrain final | 1:56.5 – 2:12 + tagline Wolof |
| Outro | 2:30 – 2:32 (fade piano jusqu'à 2:38.9) |

- Signature "Wolof TechStein beat wê!" : PAS de times (consigne artiste), placée en fin de refrain.
- Correction artiste : "vers les **sommets**" (pas "somment").
- À confirmer à la réécoute : gap 2:12 → 2:30 (instrumental long).

---

## 🖼 SALVE 1 (images 01–10) — cinematic hyperreal, 9:16 ✅
Scènes alignées sur l'intro → refrain 1 → couplet 1 (le "Rise").

| # | Fichier | Scène |
|---|---|---|
| 01 | ancrage_artiste_nuit | Héros déterminé, rue de nuit, rim-light cyan |
| 02 | toit_ville_nuit | Ville vue du toit, horizon |
| 03 | feu_veines_braises | Mains avec braises / "feu dans les veines" |
| 04 | marche_avant_rue | Marche en avant, rue mouillée |
| 05 | escalier_montée | Escalier vertigineux vers la lumière |
| 06 | visages_derriere_verre | Visages derrière la vitre / "amis en retard" |
| 07 | etoiles_yeux | Regard vers les étoiles |
| 08 | construire_abri | Construction de son propre abri |
| 09 | peuple_marche | Marche en groupe / le peuple |
| 10 | triomphe_sommet | Triomphe au sommet, bras levés |

Contrôle : 768×1376 (9:16), tous ok. Planche-contact : `work/contact_salve1.png`.

## 🖼 SALVE 2 (images 11–20) — seinen manga / cel-shaded cyan ✅
Salve des vers rapides (couplet 2), pont, refrain final, outro, cover officielle.

| # | Fichier | Scène |
|---|---|---|
| 11 | cover_hero_manga | Cover : héros manga + éclairs cyan |
| 12 | clash_plus_rapide | Clash, poing fermé / "t'as cru que j'allais plier" |
| 13 | crier_dans_bruit | Cri dans la tempête / "appris à crier" |
| 14 | critiques_du_vent | Critiques qui se dissipent / "c'est du vent" |
| 15 | regarde_nuit | Regard vers la nuit, l'autre regarde en bas |
| 16 | etoiles_dans_les_yeux | Étoiles dans les yeux (extrême close-up) |
| 17 | course_neon | Course dans l'allée néon / "toujours plus haut" |
| 18 | mon_peuple | Le peuple, la foi, les siens |
| 19 | refrain_final_explosif | Décharge cyan massive / ref. final |
| 20 | outro_aube | Outro à l'aube ambre (piano, fade) |

Contrôle : 768×1376 (9:16), tous ok. Planche-contact : `work/contact_salve2.png`.

---

## 🎬 PRODUCTION 9:16 — PREMIER EXPORT ✅
Pipeline (dans `tools/`): `timeline.py` (données) → `prep.py` (upscale + badge) → `build.py` (ASS + clips + concat + burn/mux) → `verify.py` (frames de contrôle).
- **Livrable** : `livrables/Motivé_TikTokReels_9x16_v1.mp4` (2:38.88, 16.4 MB, 1080×1920, CRF 22, badge DAÏSKY PROD).
- Contrôles : durée OK (158.880 vs 158.90), blackdetect 0 trou >300ms, frame-by-frame fin OK, Wolof présent, outro propre.
- Programmes : `tools/` + `PROGRESS.md` + MP4 commités.
