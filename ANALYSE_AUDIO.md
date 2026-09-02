# 🎛 ANALYSE AUDIO — « Jsuis pauvre mais je kiffe 2 »

Fichier analysé : `Jsuis pauvre mais je kiffe 2.mp3` (MP3 VBR ~186 kb/s, 48 kHz, stéréo)
Méthode : décodage PCM complet via ffmpeg (imageio-ffmpeg 7.0.2) → numpy.
**Toutes les valeurs ci-dessous sont MESURÉES, pas estimées.**

## 1. Durée exacte (règle v4.7 §1)

| Source | Valeur |
|---|---|
| Tag durée header MP3 | `261.072 s` |
| **Décodage PCM complet** | **12 529 919 échantillons / 48 000 Hz = 261,0400 s = 4:21.04** |
| ffmpeg null mux (`time=`) | `00:04:21.03` |

➡️ **Durée de référence retenue : 261,04 s.**

## 2. Loudness mesurée (passe 1 loudnorm, `print_format=json`)

```
input_i      = -13.51 LUFS     input_tp    = -0.12 dBTP   ⚠️ quasi 0 dBFS (risque d'écrêtage)
input_lra    =  7.20 LU        input_thresh= -23.84
output_i     = -13.23 LUFS     output_tp   = -1.80 dBTP
target_offset= -0.77            → option passe 2 : offset=-0.77
```

Masterisation à faire (v4.7 §11) : `highpass 30 / lowpass 18000 / loudnorm I=-14 TP=-1.8 LRA=11`
en **2 passes** avec `measured_I=-13.51:measured_TP=-0.12:measured_LRA=7.20:measured_thresh=-23.84:offset=-0.77:linear=true`.

## 3. Structure / BPM

- **BPM ≈ 106–107** (autocorrélation de l'enveloppe d'énergie, pic à 107,0 ; plateau 105,5–107,5).
- Attaque du refrain n°1 mesurée à **24,0 s** (saut −31 → −14 dBFS entre 23 s et 24 s).
- Attaque refrain n°2 mesurée à **102 s**, attaque couplet 2 mesurée à **129 s**.
- **Fondu final : 253,9 s → 259,6 s** (le profil passe sous −30 dBFS à 253,9 s ; dernier son > −50 dBFS à 259,6 s ; silence numérique après 260 s).

## 4. Concordance paroles ↔ audio (contrôle vers par vers)

Fichier paroles : `Je suis Pauvre et riche.txt` → **62 vers** (voir `work/timing.csv`).

| Repère paroles | Repère audio mesuré | Écart |
|---|---|---|
| Refrain 1 commence 0:18 (18 s) | drop batterie à 24,0 s | cohérent (les 6 premières secondes sont la montée) |
| Couplet 2 commence 2:09 (129 s) | onset mesuré 129,0 s | **0,0 s** ✅ |
| Refrain 2 commence 1:40 (100 s) | onset mesuré 102 s | ~2 s ✅ |
| Pont calme 3:00 (180 s) | montée piano mesurée 181 s | ~1 s ✅ |
| Refrain final 3:21 (201 s) | montée mesurée 202 s | ~1 s ✅ |

➡️ **Le minutage de l'artiste est fiable** : les écarts sont < 2 s et toujours dans le sens « l'attaque musicale arrive juste après le premier mot », ce qui est normal.

## 5. ⚠️ 3 points à faire valider par l'artiste

1. **Trou instrumental 2:45 → 3:00 (165 s → 178 s).**
   Le dernier vers du pré-refrain 2 finit à `2:44` (`-2:47` dans le fichier = 167 s) et le pont démarre à `3:00`.
   L'audio confirme une zone calme de **165 s à 178 s** (−20 à −23 dBFS) : c'est bien un passage instrumental
   (piano/violon), **pas** une dérive de minutage. → On garde l'image du dernier vers + effet vague pendant ce trou.

2. **La musique continue après le dernier vers.**
   Dernier vers `(Je suis pauvre... mais je suis riche...)` = **4:01–4:05 (241–245 s)**, mais l'audio reste
   **fort jusqu'à 253,9 s** puis fond jusqu'à 259,6 s.
   → **16 secondes de musique sans aucun vers** à la fin. Question : on laisse le fond + vague, ou on ajoute
   une ligne de texte (ex. « Je suis pauvre… mais je suis riche… » en gros, ou un « Merci » / crédits) ?

3. **Endcard.** Règle v4.7 §2 : endcard sur le fondu final + `apad` 5 s.
   Fondu final mesuré à 253,9 s → endcard proposée à **254,0 s**, total = 261,04 + 5 = **266,0 s (4:26.0)**.

## 6. Tags ID3 existants (à corriger, v4.7 §3)

Présents aujourd'hui : `TIT2 = "Je suis pauvre mais je kiffe"`, `TPE1 = "stein2000"`, `TSSE`, `WOAS`,
`TXXX:comment`, `COMM::eng`, `USLT::eng` (paroles sans timestamps, 3 296 caractères — identiques au .txt),
`APIC:Cover` (360×360), `GEOB:c2pa manifest store`.

➡️ Manquent / à remplacer : `TPE1 = Daïsky`, `TALB = TechStein Prod`, `TPE2 = Daïsky Prod`, `TPUB`,
`TCOM`, `TCON`, `TDRC`, `TXXX contact/email/producer/label`, et `APIC` en 1080×1080.

## 7. Police de caractères — ⚠️ blocage à connaître

Le sandbox **n'a pas d'accès réseau** : `curl https://github.com/google/fonts/...` → `SSL_ERROR_SYSCALL`.
Donc **impossible de télécharger `GreatVibes-Regular.ttf`** (déjà annoncé dans v4.7 : « fournir le .ttf dans le repo »).
Polices disponibles localement : `/usr/share/fonts/truetype/dejavu/` →
`DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`, `DejaVuSerif.ttf`, `DejaVuSerif-Bold.ttf`, `DejaVuSansMono*.ttf`.

➡️ Soit l'artiste dépose `GreatVibes-Regular.ttf` dans `work/fonts/` du dépôt, soit on part sur
`DejaVu Serif Bold` incliné + glow ambre (le fallback prévu par v4.7 §10).
