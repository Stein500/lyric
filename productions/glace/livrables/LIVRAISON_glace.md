# LIVRAISON — « Glace » (Dsky)

Production réalisée le 2026-10-14 · branche `arena/b24e91f1-lyric` · moteur : **PROMPT UNIVERSEL v5.9 « Ça bouge, sans voiler la parole » (MODE PEINT)**.
Hash des livrables (vérifié via `git ls-remote` + tailles des blobs via API GitHub) : `3ccd0f201f0416a31a5db7c153e0afd18f3784f8`.

---

## 1 · Titre

**Glace** — Dsky
Sous-titre d'écran : *Je suis la glace, glace, glace* · signature : **Wolof TechStein beat wê !**
Titre TikTok / Reels / Shorts : `Glace — Dsky`

---

## 2 · Captions

> **Version 1 (punchline & code) :**
> « Maintenant j'garde mes sentiments au congélo… La confiance, j'ai mis un verrou. » ❄️🔒
> Chaque parole est peinte directement dans la matière de l'image (36 tableaux, zéro sous-titre collé par-dessus).
> Tu veux un son ou des lyrics à réaliser pour toi ? **Commente le code 0300** 👇
> Wolof TechStein beat wê ! ⚡

> **Version 2 (storytelling duo & résilience) :**
> « Prête-moi ton cœur, j'le congèle en un instant… » ❄️✨
> De la ruelle givrée jusqu'à l'aube dorée : **Glace — Dsky** est disponible.
> Regarde jusqu'à la fin et **commente le code 0300** pour proposer ton prochain son !

---

## 3 · Hashtags (13 max)

`#Glace #Dsky #WolofTechStein #RapFrancais #AfroRap #MelodicRap #LyricVideo #CoeurDeGlace #BigBoss #Benin #Cotonou #MusiqueUrbaine #IAgenerated`

---

## 4 · Fichier 9:16 livré

- **`productions/glace/livrables/glace-916.mp4`** (51 650 704 octets / 49,3 Mo · 1080×1920 @ 30 fps · 5 550 frames = 185,00 s · H.264 High `yuv420p` `bt709` + AAC-LC 48 kHz 256 kb/s · `+faststart`).

---

## 5 · Déclaration IA

- **Visuels : OUI (générés par IA).** 36 plans peints distincts (`scene-01-ancre.png` → `scene-19.png` + 17 plans dédiés `v-66-12.png` → `v-165-25.png` incluant les variantes d'aube finales), typographie, icônes et stickers dorés peints par le modèle dans la matière de chaque tableau. Personnages 100 % fictifs, tenues fermées et élégantes, aucune photo personnelle utilisée, aucune nudité.
- **Audio : NON (aucun son généré par IA).** Le master (`Glace - master 320k.mp3`) provient exclusivement de l'enregistrement maître fourni par l'artiste (`Glace - Daïsky.mp3`), traité uniquement en mastering linéaire (`loudnorm` 2 passes à −14,0 LUFS / −2,5 dBTP, 48 kHz, MP3 320 kb/s, `-vn`, tags ID3 complets).

---

## 6 · Commandes Termux (une ligne par fichier, séparées par `;`, sur le hash vérifié `3ccd0f201f0416a31a5db7c153e0afd18f3784f8`)

### A. Via `git fetch` + `git checkout` dans le dépôt local

```
cd ~/lyric ; git fetch origin arena/b24e91f1-lyric ; git checkout 3ccd0f201f0416a31a5db7c153e0afd18f3784f8 ;
```

### B. Téléchargement direct fichier par fichier (`curl -L`, une ligne par fichier, séparateur `;`)

```
curl -L -o "glace-916.mp4" "https://github.com/Stein500/lyric/raw/3ccd0f201f0416a31a5db7c153e0afd18f3784f8/productions/glace/livrables/glace-916.mp4";
curl -L -o "Glace - master 320k.mp3" "https://github.com/Stein500/lyric/raw/3ccd0f201f0416a31a5db7c153e0afd18f3784f8/productions/glace/livrables/Glace%20-%20master%20320k.mp3";
curl -L -o "cover-1080.jpg" "https://github.com/Stein500/lyric/raw/3ccd0f201f0416a31a5db7c153e0afd18f3784f8/productions/glace/livrables/cover-1080.jpg";
curl -L -o "cover-916.jpg" "https://github.com/Stein500/lyric/raw/3ccd0f201f0416a31a5db7c153e0afd18f3784f8/productions/glace/livrables/cover-916.jpg";
curl -L -o "carte-accueil.jpg" "https://github.com/Stein500/lyric/raw/3ccd0f201f0416a31a5db7c153e0afd18f3784f8/productions/glace/livrables/carte-accueil.jpg";
curl -L -o "carte-finale.jpg" "https://github.com/Stein500/lyric/raw/3ccd0f201f0416a31a5db7c153e0afd18f3784f8/productions/glace/livrables/carte-finale.jpg";
curl -L -o "rendu_stats.json" "https://github.com/Stein500/lyric/raw/3ccd0f201f0416a31a5db7c153e0afd18f3784f8/productions/glace/livrables/rendu_stats.json";
curl -L -o "CARTE-VERS.md" "https://github.com/Stein500/lyric/raw/3ccd0f201f0416a31a5db7c153e0afd18f3784f8/productions/glace/CARTE-VERS.md";
curl -L -o "PROMPT_UNIVERSEL_v5.9_MOUVEMENT_SANS_VOILER.md" "https://github.com/Stein500/lyric/raw/3ccd0f201f0416a31a5db7c153e0afd18f3784f8/PROMPT_UNIVERSEL_v5.9_MOUVEMENT_SANS_VOILER.md";
```

---

## 7 · Détail des contrôles mesurés sur les fichiers livrés (§11, §12, §13)

| Contrôle | Commande | Attendu (v5.9 §12) | Mesure réelle sur `glace-916.mp4` / master |
|---|---|---|---|
| **Durée clip** | `ffmpeg -i glace-916.mp4` | `= frames/fps` à 0,01 s près (`5550 / 30 = 185,00 s`) | `00:03:05.00` (**185,00 s** exactement, 5 550 frames @ 30 fps) |
| **Frames noires** | `blackdetect=d=0.05:pix_th=0.10` | **0** | **0** |
| **Gel (`freezedetect`)** | `freezedetect=n=-33dB:d=2.5` | **0 sur les vers** ; cartes & CTA sur image fixe signalés et assumés | **0 sur les 45 vers chantés** ; uniquement `0→6,07 s` (carte d'accueil), `167,8→180,0 s` (CTA clochette finale sur plan éteint) et `180,97→185,0 s` (carte finale) |
| **Loudness** | `ebur128=peak=true` | **−14,0 LUFS** | **−14,0 LUFS** (LRA = 6,9 LU, True Peak = −2,4 dBFS) |
| **Crête (`astats`)** | `astats=metadata=1:reset=0` | **≤ −1,0 dB** | **−2,47 dB** sur le clip (`-2,48 dB` sur le MP3 master 320k) |
| **Faststart** | octets d'en-tête | `moov` avant `mdat` | `moov` à l'octet **36**, `mdat` à l'octet **197 556** (`moov < mdat`) |
| **Typo (zoom 1:1)** | `CONTROLE-typo-zoom.jpg` (1080×400 1:1 à `t=37,00 s`) | nette, **aucun doublement de lettre** | **0 ghosting / 0 dédoublement** (fenêtre glissante sur plan à 110 %, aucun resize par frame) |
| **Tailles API GitHub** | `gh api .../git/trees/3ccd0f2` | blobs présents et complets | `glace-916.mp4` = **51 650 704 o** · `Glace - master 320k.mp3` = **7 562 693 o** · `cover-1080.jpg` = **348 213 o** · `cover-916.jpg` = **601 614 o** |

---

## 8 · Notes déclarées (transparence §4 & §5.6)

1. **Aucune retouche bitmap manuelle de diacritique** n'a été nécessaire : les 36 plans peints sont sortis directement du générateur avec leurs accents exacts (`Ç`, `Û`, `É`, `È`, `Ê`, `À`, `Œ`), vérifiés sur `CONTROLE-salve1.jpg`, `CONTROLE-salve2.jpg`, `CONTROLE-salve3.jpg` et `CONTROLE-salve4.jpg`.
2. **Vers 22 (`scene-19.png` à 64,26 s)** : le mot initial de `Glace.txt` déclenchant un blocage lexical (`Response contains no images` sur 2 tentatives), le modèle a peint le segment exact `VEULENT MA PLACE / ILS SONT TROP SUR LE PAL'` (conforme au tag ID3 du MP3 source).
3. **Durées d'affichage par vers (`affichage_s`)** : calculées par la formule provisoire du §5.6 (`min(fin_vers, début_vers + max(2.2 s, 0.30 s × nb_mots))`), générant **5 fenêtres de clochettes CTA ≥ 4,00 s** (`42,50→47,16` · `145,56→150,14` · `152,49→157,79` · `160,14→165,25` · `167,60→180,00`).
