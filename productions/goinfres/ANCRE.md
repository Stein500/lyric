# ANCRE — « Goinfres » (Dsky) · production 2026-10-21

Règles appliquées : **PROMPT UNIVERSEL v5.9 « Ça bouge, sans voiler la parole »** (§0 → §15), combiné aux consignes explicites de l'artiste :
- **MODE PEINT** ;
- **Style Animé Seinen (`STUDIO ANIME SEINEN`)** ;
- **Couleurs : strictement NOIR et BLANC** (encre noire profonde `#050608`, blanc franc `#FFFFFF`, gris d'encre `#2A2E35`) ;
- **Décors atténués** (arrière-plans adoucis et assombris en gris/noir d'encre pour ne jamais concurrencer le personnage ni la parole peinte, tout en changeant de décor et d'expression selon l'histoire).

**État actuel (§1)** : **GÉNÉRÉ / CONTRÔLÉ — PROPOSÉ À LA VALIDATION DE L'ARTISTE** *(aucune validation de l'artiste n'est inventée)*.

---

## 1. Paramètres verrouillés de la production (§2)

```
TITRE        : Goinfres
ARTISTE      : Dsky
LANGUES      : français (signature en fon/wolof : « Wolof TechStein beat wê ! »)
PAROLES      : Goinfres.txt            (47 lignes = 47 vers, horodatages de l'artiste non retouchés)
AUDIO        : Goinfres.mp3            (maître fourni par l'artiste, jamais généré)
RECETTE      : STUDIO ANIME SEINEN — NOIR & BLANC, DÉCORS ATTÉNUÉS
CODE DE FIN  : 0342 (4 chiffres, lié à la durée décodée mesurée : 3 min 42 s = 222,92 s)
SIGNATURE    : « Wolof TechStein beat wê ! »
MODE         : PEINT
DOSSIER      : productions/goinfres/   (fonds/ livrables/ fonts/ + verses_map.json + CARTE-VERS.md)
```

---

## 2. Source audio et mesures réelles (§11 — mesurées)

| Mesure | Valeur mesurée | Méthode |
|---|---|---|
| Fichier source | `Goinfres.mp3` | MP3 (`mp3float`), 48 000 Hz, stéréo, 186 kb/s, 10 700 159 échantillons |
| Durée décodée | **222,92 s** (`00:03:42.91`) | `ffmpeg -map 0:a:0 -f null -` → concorde avec `[length:03:42]` → code **`0342`** |
| Loudness source (pass 1) | **−13,06 LUFS**, LRA **8,40 LU** | `loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json` |
| Vraie crête source (pass 1) | **−0,83 dBTP** (seuil −23,36 LUFS) | `loudnorm` pass 1 (`input_tp`) |
| Silences ≥ 3,5 s à −42 dB | **aucun (`[]`)** | `silencedetect=n=-42dB:d=3.5` |
| Master `_master_noart.mp3` | **−14,0 LUFS**, LRA **8,3 LU**, TP **−1,9 dBFS**, crête **−2,21 dB** | `loudnorm` 2 passes linéaires (`offset=-0.88`), 48 kHz, MP3 320 kb/s (`-vn`), contrôlé par `ebur128` + `astats` |
| Paroles chronométrées | **47 vers**, `10,60 s → 222,92 s` | `Goinfres.txt` → normalisé sans retouche d'horodatage dans `timings_source.lrc` |

**Fenêtres de clochette éligibles en MODE PEINT (§6 : `[fin d'affichage + 0,15 s → début du vers suivant]`, seuil ≥ 4,00 s)** :
1. Après v-02 : **`16,89 s → 23,41 s`** (6,52 s libres)
2. Après v-07 : **`39,87 s → 50,26 s`** (10,39 s libres)
3. Après v-19 : **`85,65 s → 89,76 s`** (4,11 s libres)
4. Après v-24 : **`106,04 s → 116,32 s`** (10,28 s libres)
5. Après v-36 : **`151,48 s → 155,96 s`** (4,48 s libres)
6. Après v-45 : **`184,25 s → 193,71 s`** (9,46 s libres)
7. Après v-47 : **`199,98 s → 222,92 s`** (22,94 s libres avant la carte finale `222,92 → 227,92 s`)

---

## 3. Direction artistique — « STUDIO ANIME SEINEN — Noir & Blanc, décors atténués »

1. **Cel-shading seinen noir & blanc** : traits d'encre nets, aplats noirs profonds `#050608`, rehauts blancs `#FFFFFF` sur les contours du personnage et le regard, gris d'encre `#2A2E35`.
2. **Décors atténués et variés** : chaque scène possède son décor propre (salle de banquet des goinfres, studio piano/violon, balcon nocturne, chambre forte de lingots, ruelle populaire, océan de requins, atelier d'artisans, table-monde des rois, arches de pierre), mais toujours **atténué en arrière-plan sombre et brumeux** pour que le personnage et la parole peinte ressortent immédiatement.
3. **Protagoniste (`fonds/scene-01-ancre.png`)** : jeune homme noir en style animé seinen, courtes locks stylisées, manteau noir à col montant fermé souligné d'un filet blanc, expressions du visage variées d'un plan à l'autre (indignation, sourire concentré, gravité lucide, colère accusatrice, compassion main sur le cœur, cri d'alerte, stoïcisme, refus main levée, défi, poing levé).
4. **Typographie peinte & stickers** : capitales serif blanches et gris-argent sur ruban d'encre noire dans la bande centrale (`y 620 → 1340`), accompagnées de 2 icônes au trait d'encre blanche collées au sens du vers et traversées par un fil lumineux blanc.
