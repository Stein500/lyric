# ANCRE — « Calm in off down » (Daïsky) · production 2026-10-24

Règles appliquées : **PROMPT UNIVERSEL v6.0 « WTBW Salut & Stickers Doux — Ça bouge, sans voiler la parole »** (§0 → §16), combiné aux consignes explicites de l'artiste dans `Calm in off down.txt` :
- **Mode Hybride Bilingue (directive permanente de l'artiste)** :
  - **Paroles originales (anglais, espagnol & signature WTBW) PEINTES DANS L'IMAGE** dans un **style graffiti urbain bien ordonné, propre et stylé** ;
  - **Traduction en français DÉFILANTE mot à mot** (calque PIL centré `≤ 708 px`, posé dans `y = 1452 → 1545` juste au-dessus du filet de progression `y = 1560`, mot actif mis en avant en or chaud `#FFDE76` + halo 3 px, mots prononcés en blanc crème, mots à venir adoucis) **uniquement sur les passages non français** ;
- **Recette visuelle : « WANDANCE BATTLE & GRAFFITI LOVES — ORDONNÉ & VISAGE DÉGAGÉ »** :
  - Scènes de battle de street-dance / hip-hop inspirées de l'animé ***Wandance* (ワンダンス)** (isolations, freezes, footwork, krump, pop-and-lock) ;
  - **Mise en avant des « loves »** : chaque plan intègre un **sticker cœur « love » en graffiti lumineux** accompagné d'une icône thématique reliée par un fil d'or ;
  - **Rien pour cacher le visage** : visage du protagoniste 100 % dégagé dans la moitié haute (`y < 560`, crâne jamais coupé).
- **Habillage v6.0 WTBW sans code** :
  - **Zéro système de code** (aucune accroche « regarde jusqu'à la fin », aucun code à 4 chiffres sur la carte finale) ;
  - **Carte d'accueil WTBW en 2 temps (`0,00 → 4,97 → 9,94 s`)** et **carte finale WTBW (`183,61 → 188,61 s`)** avec les **3 stickers vectoriels animés en douceur** (`LIKE LA VIDÉO`, `CLIQUE SUR + POUR T'ABONNER`, `COMMENTE SI TU AIMES !`).

**État actuel (§1)** : **GÉNÉRÉ / CONTRÔLÉ — PROPOSÉ À LA VALIDATION DE L'ARTISTE** *(aucune validation de l'artiste n'est inventée)*.

---

## 1. Paramètres verrouillés de la production (§2)

```
TITRE        : Calm in off down
ARTISTE      : Daïsky
LANGUES      : anglais + espagnol + signature WTBW (VO peinte en graffiti + traduction française défilante)
PAROLES      : Calm in off down.txt           (42 lignes = 42 vers, horodatages de l'artiste non retouchés)
AUDIO        : Calm_in _off_down Daïsky.m4a   (maître fourni par l'artiste, jamais généré)
RECETTE      : WANDANCE BATTLE & GRAFFITI LOVES — ORDONNÉ & VISAGE DÉGAGÉ
HABILLAGE    : WTBW SALUT + STICKERS DOUX (Like · Clique sur + pour t'abonner · Commente si tu aimes) — SANS CODE
SIGNATURE    : « Wolof TechStein beat wê ! » (WTBW)
MODE         : PEINT (VO anglais/espagnol en graffiti) + DÉFILEMENT (traduction française mot à mot)
DOSSIER      : productions/calm-in-off-down/  (fonds/ livrables/ fonts/ + verses_map.json + CARTE-VERS.md)
```

---

## 2. Source audio et mesures réelles (§11 — mesurées)

| Mesure | Valeur mesurée | Méthode |
|---|---|---|
| Fichier source | `Calm_in _off_down Daïsky.m4a` | Opus (`0x7375704F`), 48 000 Hz, stéréo, 133 kb/s, `3 054 575` octets |
| Durée décodée | **183,61 s** (`00:03:03.61`, exact `183,6135 s`) | `ffmpeg -map 0:a:0 -f null -` → concorde avec `[length:03:03]` |
| Loudness source (pass 1) | **−13,50 LUFS**, LRA **5,60 LU** | `loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json` |
| Vraie crête source (pass 1) | **−0,72 dBTP** (seuil −23,70 LUFS) | `loudnorm` pass 1 (`input_tp`) |
| Silences ≥ 3,5 s à −42 dB | `179,824 s → 183,614 s` (**3,789 s** en fin de queue) | `silencedetect=n=-42dB:d=3.5` |
| Master `_master_noart.mp3` | **−14,0 LUFS**, LRA **4,4 LU**, TP **−1,4 dBFS**, crête **−1,42 dB** | `loudnorm` 2 passes linéaires (`offset=-0.68`), 48 kHz, MP3 320 kb/s CBR (`-vn`), contrôlé par `ebur128` + `astats` (`8 813 448` échantillons) |
| Paroles chronométrées | **42 vers**, `09,94 s → 183,61 s` | `Calm in off down.txt` → normalisé sans retouche d'horodatage dans `timings_source.lrc` |

**Fenêtres de clochette éligibles (§6 : `[fin d'affichage + 0,15 s → début du vers suivant]`, seuil ≥ 4,00 s)** :
1. Après v-01 : **`12,29 s → 24,82 s`** (12,53 s libres)
2. Après v-26 : **`106,78 s → 115,17 s`** (8,39 s libres)
3. Après v-42 : **`166,68 s → 183,61 s`** (16,93 s libres avant la carte finale `183,61 → 188,61 s`)

---

## 3. Direction artistique — « WANDANCE BATTLE & GRAFFITI LOVES — ORDONNÉ & VISAGE DÉGAGÉ »

1. **Énergie Battle *Wandance*** : chorégraphie hip-hop / freestyle expressive, mouvements d'isolation, footwork sur béton froid, krump, pop-and-lock et élévation solaire.
2. **Visage 100 % dégagé (`y < 560`)** : jeune danseur urbain noir aux locks courtes stylisées et veste de battle à col montant fermé souligné d'or et de cyan ; **aucun masque, aucune capuche sur les yeux, aucune lunette, aucun texte sur le visage**.
3. **Graffiti ordonné & Stickers « Loves »** :
   - Paroles originales (anglais/espagnol) peintes en capitales graffiti structurées et très lisibles (or chaud & blanc en ligne 1, cyan-argent en ligne 2) sur ruban d'encre noire centrale ;
   - Sticker **cœur « love » graffiti lumineux** + icône thématique juste sous le bloc graffiti ;
   - Bande basse (`y = 1452 → 1545`) laissée libre sur le béton sombre pour accueillir la **traduction française défilant mot à mot** sans jamais voiler ni la VO peinte ni le sticker « love ».
