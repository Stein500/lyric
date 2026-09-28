# Analyse — Concentré sur le chemin

Mesures du 2026-09-28. **Analyse structurelle, pas encore une validation vocale ni une livraison finale.**

## Audio décodé

| Mesure | Résultat |
|---|---:|
| Source | `Concentré sur le chemin.mp3` |
| Durée décodée par FFmpeg | **213,160 s — 03:33.160** |
| Fréquence source | 48 000 Hz |
| Canaux | Stéréo |
| Tempo estimé, flux spectral | ≈143,55 BPM |
| Alternative demi-tempo | ≈71,78 BPM |

La durée provient du `out_time_us` final de FFmpeg avec `-map 0:a:0 -vn -f null -`, pas de la durée d'une éventuelle pochette intégrée ni du `[length:03:33]` arrondi des paroles. FFmpeg système absent : utilisation de la wheel `imageio-ffmpeg` dans `/tmp/lyric-venv`, sans binaire ajouté au dépôt.

### Loudnorm passe 1

Mesure avec `-v info` après `highpass=f=30,lowpass=f=18000`, cibles I=−14 LUFS, TP=−1,8 dBTP, LRA=11 :

| Champ JSON | Valeur |
|---|---:|
| input_i | −14,72 LUFS |
| input_tp | −0,22 dBTP |
| input_lra | 4,70 LU |
| input_thresh | −24,80 LUFS |
| target_offset | −0,53 LU |

La marge de crête doit être réduite avant livraison. Ce sont des **mesures d'entrée**, pas les caractéristiques d'un master déjà livré. La passe 2 devra utiliser les mêmes pré-filtres, les valeurs mesurées et `offset=-0.53`, puis une nouvelle mesure contrôlera le MP3 encodé (LUFS≈−14 ; TP≤−1,5 dBTP). Aucun audio source n'a été modifié.

## Paroles

- Fichier confirmé par correspondance de titre : `concentré sur le chemin.txt`, contenu LRC UTF-8.
- **58 occurrences de vers, 38 textes distincts.** Ponctuation, accents, casse et espaces internes conservés ; aucune correction rédactionnelle inventée.
- 58 marques directionnelles invisibles U+200E retirées de la copie destinée au rendu. Le TXT original est intact.
- Départ du premier vers : **00:04.44** ; départ du dernier : **03:10.90**.
- Tous les départs sont strictement croissants et dans la durée audio.
- Plus petit intervalle entre départs : **1,30 s** ; zéro anomalie structurelle détectée à la limite de 1,2 s.
- Les 58 départs ont un pic musical à moins de ±0,35 s (flux positif >1,15×médiane locale 4 s, FFT 2048 / hop 256 à 22 050 Hz).
- **Important : une percussion proche n'est pas une preuve d'alignement vocal.** Aucun timestamp n'a été déplacé vers un pic instrumental. Les propositions de proximité sont dans le cache, `vocal_alignment_validated=false` partout.
- Le fichier `Concentré sur le chemin.lrc` est une copie nettoyée avec durée exacte et horaires conservés, **pas un recalage vocal présenté comme validé**.

Exemples textuels à préserver tels quels : « J'suis concentrée, j'regarde droit devant », « Nonvi konou, mon frère sourit, on avance ». Leur présence ne change ni le titre du morceau ni l'identité de la production.

### Structure proposée (déduite des paroles + énergie RMS)

Le fichier source ne contient pas de balises de section. Les frontières ci-dessous sont des repères de travail, pas une annotation musicologique validée ; les fins de phrases et silences restent à écouter.

| Départ source | Section proposée |
|---|---|
| 00:00.00 | Intro musicale / ad-libs |
| 00:25.30 | Refrain 1 |
| 00:38.96 | Couplet 1 |
| 00:59.32 | Pré-refrain 1 |
| 01:06.71 | Refrain 2 / respiration musicale avant le couplet suivant |
| 01:25.64 | Couplet 2 |
| 01:46.60 | Pré-refrain 2 |
| 01:53.28 | Refrain 3 / respiration musicale avant le pont |
| 02:20.00 | Pont |
| 02:32.84 | Refrain final |
| 02:52.01 | Outro / ad-libs jusqu'à la fin audio |

### Refrains répétés et choix du hook

Une suite de **cinq textes strictement identiques** est retrouvée quatre fois. Les deux premiers contiennent le titre. Énergie ci-dessous : moyenne des niveaux RMS mono par seconde sur cette fenêtre, indicative.

| Départ | Fin des deux lignes (départ de la troisième) | Fenêtre | RMS moyen indicatif |
|---|---|---:|---:|
| 00:25.30 | 00:31.89 | 6,59 s | −16,265 dBFS |
| 01:06.71 | 01:13.60 | 6,89 s | −13,576 dBFS |
| **01:53.28** | **02:00.18** | **6,90 s** | **−13,174 dBFS** |
| 02:32.84 | 02:40.25 | 7,41 s | −16,561 dBFS |

**Proposition, non validée :** prendre les deux lignes à 01:53.28 pour le cold-open. Les paroles source situent cette paire sur 6,90 s ; ne pas imposer arbitrairement une coupure à 6,00 s en plein mot. Vérifier les attaques et fins réelles avant de fixer l'extrait.

Les deltas internes diffèrent entre reprises (la seconde ligne arrive à +3,13 / +3,67 / +3,70 / +4,22 s). **Ne pas recopier aveuglément les délais du premier refrain** et dégrader des horaires plausibles. Le miroir n'est qu'un indice de correction lorsqu'une erreur est avérée.

Si ce hook est confirmé : total théorique 6,90 + 213,16 + 5 = **225,06 s** ; à 30 fps, **6 752 images** et durée vidéo 225,0667 s. Sinon, recalculer ces valeurs depuis la configuration réellement approuvée.

### Trois passages à vérifier à l'écoute

1. 00:25.30 — « Concentré sur le chemin, je regarde plus en arrière ».
2. 01:25.64 — « J'suis concentrée, j'regarde droit devant ».
3. 02:32.84 — « Concentré sur le chemin, je regarde plus en arrière ».

Les fenêtres de fin et les temps mot à mot ne sont pas encore validés. Ne pas laisser le dernier vers affiché automatiquement pendant toute la queue instrumentale de 22,26 s. Les mêmes précautions concernent les longues respirations entre sections.

## Budget visuel appliqué

La consigne explicite **5 portraits + 5 paysages** remplace la règle générique « une image par vers distinct ». Ne pas lancer 38×2 images, ni ajouter deux fonds par format pour intro/endcard.

- 5 scènes × 2 compositions = **10 fonds finaux**.
- Ancre portrait comprise dans le budget.
- Intro, endcard et covers dérivées de ces fonds en post, sans génération supplémentaire.
- Références photo, ancre et choix typographique : en attente d'approbation.

## Reproduire les mesures

Depuis la racine du dépôt :

```sh
bash scripts/setup_env.sh
/tmp/lyric-venv/bin/python scripts/analyse_chanson.py --audio 'Concentré sur le chemin.mp3' --lyrics 'concentré sur le chemin.txt' --title 'Concentré sur le chemin' --output work/concentre_sur_le_chemin --clean-lrc 'Concentré sur le chemin.lrc'
/tmp/lyric-venv/bin/python -m unittest discover -s tests -v
```

Le cache ignoré contient `analyse.json` (empreintes SHA-256 des sources, valeurs loudnorm, courbe RMS, pics, timings et reprises), `timings_audited.json`, `decode.log` et `loudnorm_pass1.log`. Il est régénérable et ne doit pas être confondu avec `timings_validated.json`, qui n'existera qu'après une vraie validation vocale.
