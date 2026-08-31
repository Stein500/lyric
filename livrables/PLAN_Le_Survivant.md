# PLAN DE PRODUCTION — « Le Survivant » (conformes PROMPT UNIVERSEL v4.6)

## Décisions validées (2026-08-31)
| Point | Décision |
|---|---|
| Charte visuelle | **HYBRIDE** : B « Dark Trap / Lightning » (couplets/refrains/intro/outro) + A « mixte chaleureux » (pont piano 1:38.5→1:50) |
| Images | **100 % IA** · salves de 10 max · image d'ancrage validée avant salves |
| Ordre | **9:16 d'abord** (bien fait) → 16:9 → MP3 master + tags → cover |
| Endcard | démarre à 2:24 sur le fondu + **apad 5 s → total 2:35,00** |
| Écran de fin | Titre « Le Survivant » · Daïsky Prod / TechStein · Rock/Afro-Rock/World · 2026 · contacts officiels |

## Budget images (règle : 1 vers = 1 image)
47 vers datés + 1 fond intro musical (0:00→0:06) + 1 fond endcard = **49 images par format**.

| Cycle | Format | Nombre | Salves de 10 |
|---|---|---|---|
| 1 — TikTok | 9:16 portrait | **49** | 5 salves (10+10+10+10+9) |
| 2 — YouTube | 16:9 paysage | 49 | 5 salves |
| 3 — Cover publication | base unique → crops 1080×1920 + 1920×1080 | 1 | à part |

**Total cycle complet : 99 images.** (Réutilisation interdite entre vers ; le pont réutilise les 4 visuels A de ses 4 vers.)

## Mapping vers → images (49 slots, 9:16)
| Slots | Section | Charte |
|---|---|---|
| 0 | Intro musical 0:00→0:06 | B |
| 1-4 | Intro vocale (beat wê / survivant / attends / j'arrive) | B |
| 5-9 | REFRAIN 1 (0:25→0:36) | B |
| 10-17 | COUPLET 1 (0:38→0:50) | B |
| 18-19 | PRÉ-REFRAIN 1 (0:53→0:59) | B |
| 20-24 | REFRAIN 2 (1:02→1:12) | B |
| 25-32 | COUPLET 2 (1:13.5→1:25) | B |
| 33-34 | PRÉ-REFRAIN 2 (1:30→1:36) | B |
| 35-38 | **PONT piano (1:38.5→1:47)** | **A** |
| 39-43 | REFRAIN FINAL (1:50→2:01) | B |
| 44-45 | Outro chanté (2:11→2:13) | B |
| 46 | Outro fondu (2:18→2:24) | B |
| 47-48 | Outro/endcard (2:24→2:35) | B assombri |

## Séquencement (une étape = un commit + push)
1. ✅ Analyse MP3 + validation timing (fait — commit 8c77d41)
2. ⏳ **Ancrage** : 1 image B + 1 image A (9:16) + maquette badge/vers → validation
3. Salve 1 (10 img) → salve 2 → salve 3 → salve 4 → salve 5 (49 total)
4. Pré-calcul fonds (upscale, letterbox, badge haut-gauche, JPEG q92)
5. Rendu SOLUTION A : flux continu ceil(155×30)=4650 frames @30 FPS + vague + Ken Burns
6. Mux audio master pad 5 s + afade out 3 s + fade vidéo → `Le_Survivant_9x16_v1.mp4`
7. Vérifs §7 → 16:9 (salves paysages + rendu) → MP3 master + tags → covers
