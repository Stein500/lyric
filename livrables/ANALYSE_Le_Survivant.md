# 🎧 ANALYSE — « Le Survivant » (Daïsky) · MP3 + paroles minutées

> Généré le 2026-08-31 · branche `arena/01a0594e-lyric` · conformément au **PROMPT UNIVERSEL v4.6**
> Outils : décodage PCM intégral (imageio-ffmpeg / ffmpeg 7.0.2), STFT numpy, ebur128, mutagen.
> Graphique : `livrables/analyse/le_survivant_structure.png`

---

## 1. Fichier audio — état des lieux

| Propriété | Valeur mesurée |
|---|---|
| Fichier | `Le Survivant.mp3` (3 500 350 octets) |
| Durée nominale | **2:30.000** (150,000 s) |
| Durée décodée exacte | **149,960 s** (7 198 079 échantillons @48 kHz) |
| Format | MP3 stéréo 48 kHz, ~185 kbps, ID3 **v2.4** |
| Cover intégrée | ✅ APIC 360×360 (front) — exploitable en base de cover ?  ❌ trop petite pour 1080p, à régénérer |
| Premier son | 0,03 s (aucun silence mort à l'ouverture) |
| Fin du son | 149,93 s — fondu final de ~2:24 → 2:29 (-62 dB à 2:29) |
| Loudness intégré | **-13,8 LUFS** (cible charte -14 → quasi conforme, Δ ≈ +0,2 LU) |
| True Peak | **-0,7 dBTP** ⚠️ (plafond charte ≤ -1,5 dBTP → **non conforme**, ~0,8 dB à récupérer) |
| LRA | 6,1 LU (dynamique saine) |

### ⚠️ Tags ID3 actuels — NON conformes à la charte §Tags
Présents : `TIT2=Le Survivant` · `TPE1=stein2000` · `TSSE=Lavf60` · `USLT` (paroles **sans** minutage) · `WOAS` + `COMM` (traces Suno, id `6c340dfd…`).
Manquants / à corriger : `TPE1=Daïsky`, `TALB=TechStein Prod`, `TPE2=Daïsky Prod`, `TPUB`, `TCOM=TechStein · Daïsky`, `TCON=Rock / Afro-Rock / World`, `TDRC=2026`, `TXXX` (contact, email, producer, label), `USLT` complet. → **passe masterisation + retag complète requise** (§6 du prompt).

---

## 2. Structure musicale détectée (validation automatique)

Analyse : enveloppe RMS (pas 10 ms), flux spectral (onsets), bandes graves/médiums/aigus (STFT 4096).

| # | Section | Début→Fin | Signature énergétique | timing.txt dit | Verdict |
|---|---|---|---|---|---|
| 1 | Intro instrumentale (guitare saturée) | 0:00→0:06 | énergie moyenne, aucun silence initial | — | ✅ |
| 2 | Vox d'intro (« Wolof TechStein beat wê! » … « J'arrive… ») | 0:06→0:24 | onsets voix nets à 5,94 / 10,90 / 13,53 / 16,05 s | 0:06 / 0:11 / 0:13.5 / 0:16 | ✅ ±0,1 s |
| 3 | **REFRAIN 1** (agressif) | 0:25→0:36 | palier haut ~71 dB rel. | 0:25→0:36 | ✅ |
| 4 | COUPLET 1 (flow rapide) | 0:38→0:50 | énergie 66-68 dB, onsets denses | 0:38→0:50 | ✅ |
| 5 | PRÉ-REFRAIN 1 (ad-libs) | 0:53→0:59 | maintien ~70 dB | 0:53 / 0:59 | ✅ |
| 6 | **REFRAIN 2** | 1:02→1:12 | palier ~71,6 dB | 1:02→1:12 | ✅ |
| 7 | COUPLET 2 | 1:13.5→1:25 | 66-69 dB ; **chute des guitares à 1:25** (aigus -16 dB) | 1:13.5→1:25 | ✅ |
| 8 | PRÉ-REFRAIN 2 | 1:30→1:36 | creux relatif (62-64 dB) | 1:30 / 1:36 | ✅ |
| 9 | PONT piano (calme) | 1:38.5→1:47 | aigus en retrait, remontée 1:42→1:48 | 1:38.5→1:47 | ✅ |
| 10 | **REFRAIN FINAL** (tutti) | 1:50→2:00 | **max énergie de la chanson** (71,9 dB) | 1:50→2:00 | ✅ |
| 11 | Outro chanté | 2:01→2:12 | 67-69 dB décroissant | 2:01 / 2:11 | ✅ |
| 12 | Outro fondu (« …beat wê… », « Yeah… ») | 2:13→2:24 | décroissance régulière 64→59 dB | 2:13 / 2:18 / 2:24 | ✅ |
| 13 | Fondu final → silence | 2:24→2:29.9 | -10,9 → -61,8 dB | — | ✅ |

---

## 3. Validation ligne par ligne du fichier `le survivant... timing.txt`

- **47 vers datés** · 10 sections déclarées.
- **46/47 vers** tombent sur un onset musical/voix à **±0,35 s**.
- 1 seul écart : « *(Le survivant…)* » à 2:24 → onset flou à -0,62 s (voix chuchotée **dans** le fondu — onset indétectable de façon fiable). **Conserver 2:24.**

### 🏁 VERDICT
> **Le fichier de paroles minutées est FIABLE DE BOUT EN BOUT — y compris après 2:00.**
> La dérive « après ~1:50-2:00 » constatée sur l'ancienne vidéo vient donc **exclusivement du montage en segments concaténés** (défaut diagnostiqué §0 v4.6), **pas** du fichier de paroles. La SOLUTION A (flux continu frame-accurate) corrigera le problème.

### ⚠️ Pièges de parsing à normaliser pour le pipeline
1. Le tiret est un **séparateur**, pas un signe négatif : `…le feu -1:02` = **1:02** (≠ -58 s !).
2. La 1ʳᵉ ligne est une **plage** : `Wolof TechStein beat wê! 0:06-0:07` → start = 0:06.
3. Une ligne a un tiret collé (`Yeah...-2:18`) et un espace final traînant (1:38.5) → parsing robuste requis.
4. Recommandation : **rescaler chaque start sur l'onset détecté le plus proche** (≤ 0,35 s) pour un calage à la frame.

---

## 4. Données prêtes pour la production (pipeline v4.6)

| Paramètre | Valeur |
|---|---|
| Durée audio master | 149,960 s |
| Tempo | ≈ **128-129 BPM** (groove half-time ~64,5 — cohérent rock/afro-rock) |
| Nombre de vers à afficher | **47** (+ intro/outro musical-only 0:00-0:06 et 2:13-2:30) |
| Fin de chant utile | 2:24 → **~6 s de queue musicale** disponible pour l'écran de fin |
| Endcard recommandé | démarrage à 2:24 sur le fondu (pas d'`apad` nécessaire si total = 150,000 s) ; si endcard > 6 s → `apad` |
| Frames @30 FPS | ceil(150,000×30) = **4500 frames** (0 dérive, chaque frame = t = i/30) |
| Images (charte : 20 portrait + 20 paysage, 10 max/salve) | 20+20 suffisent par **réutilisation par section** (47 vers ≠ 47 images uniques — à confirmer) |
| Audio pour le clip | master -14 LUFS / TP ≤ -1,5 dBTP (highpass 30 Hz, lowpass 18 kHz, loudnorm 2 passes) |

---

## 5. Points à valider avant production (questions posées)

1. **Charte visuelle** : A « mixte amour » (coucher de soleil doré) ou **B « Dark Trap / Lightning »** — reco : **B**, titre sombre/agressif (éclairs cyan/ambre, reflets mouillés, seinen noir animé).
2. **Source des images** : génération IA 100 % (20+20 conformes charte) ou incorporation des photos fournies (`Sam/`, `Samu/`, `klo/` = photos réelles de l'entourage) ?
3. **Périmètre de ce cycle** : 9:16 + 16:9 + cover + MP3 master complet, ou d'abord une version 9:16 de validation ?
4. **Écran de fin** : adapter à ce titre — « **Le Survivant** » (le bloc §Contact du prompt cite « L'amour est la réponse » comme exemple) ; crédits/contacts identiques.

---

**Wolof TechStein beat wê !** ⚡
