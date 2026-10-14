# LIVRAISON — « Mahu ti tè gbè » (Dsky)

Production ouverte le 2026-10-10 · clip livré le 2026-10-14 · branche `arena/21016a0d-lyric` · moteur : PROMPT UNIVERSEL v5.7 + **v5.8 (typo peinte)**.
Hash des livrables : `e34df944577af852f2ca99f91a0bd4c892b851d8` (clip 9:16, 34 plans, master, cartes)
— cette page de livraison est committée juste après, le hash ci-dessus contient déjà tous les fichiers à télécharger.

---

## 1 · Titre

**Mahu ti tè gbè** — Dsky
Sous-titre d'écran : *God is always there* · signature : **Wolof TechStein beat wê !**
Titre TikTok : `Mahu ti tè gbè — Dsky`

## 2 · Captions

> MAHU TI TÈ GBÈ — God is always there ️
> Chaque mot est peint dans l'image, pas de sous-titre collé par-dessus.
> Tu veux un son ou des lyrics réalisés pour toi ? **Commente le code 0326** 
> Wolof TechStein beat wê !

## 3 · Hashtags (13)

`#MahutiTegbe #Dsky #WolofTechStein #AfroGospel #GospelMusic #Louange #Chretien #FonMusic #Benin #Cotonou #LyricVideo #MusiqueChretienne #IAgenerated`

## 4 · Déclaration IA (à cocher avant publication)

- **Visuels : OUI, générés par IA.** 34 plans distincts (19 scènes + 12 variantes de vers + 3 variantes aube), typographie,
  icônes et stickers **peints par le même modèle** dans l'image ; le clip 9:16 est construit à partir de ces plans (aucun
  texte incrusté hors cartes d'accueil/finale). Aucun plan issu d'une photo personnelle.
- **Audio : NON, aucun son généré.** Master = l'enregistrement de l'artiste, uniquement régénératif
  (loudnorm 2 passes, résample 48 kHz, MP3 320 kb/s, ID3). Écrêtage de la source (+0,06 dBTP) corrigé.
- Personnages : héros fictifs, tenues fermées, aucun contenu sexuel ou de nudité.

## 5 · Fichiers livrés

| Fichier | Détails |
|---|---|
| `livrables/mahu-ti-te-gbe-916.mp4` | **clip 9:16** · 1080×1920 · H.264 High yuv420p bt709 · 30 fps · 6 342 frames = 211,40 s · 2 035 kb/s · AAC-LC 48 kHz 253 kb/s · 60 715 989 o (57,9 Mo) · `+faststart` |
| `livrables/Mahu ti tè gbè - master 320k.mp3` | 8 570 754 o · 206,40 s · 48 kHz · 320 kb/s CBR · −14,0 LUFS · crête −1,24 dB · pochette 1080 + USLT fre 49 lignes |
| `livrables/cover-1080.jpg` (+ `.png`) | pochette carrée 1080×1080, tête non rognée |
| `livrables/cover-916.jpg` | cover verticale 1080×1920 (plan aube `scene-19`) |
| `livrables/carte-accueil.jpg` · `livrables/carte-finale.jpg` | cartes fixes (aperçu) ; les cartes animées sont dans le MP4 (0→9,33 s et 206,40→211,40 s) |
| `fonds/scene-01-ancre.png` → `scene-19.png` · `fonds/v-*.png` | **34 plans peints** (19 scènes + 12 variantes de vers + 3 variantes aube), orthographe relue image par image |
| `render_lyric_video.py` | moteur du clip (timeline v5.8, travelling par fenêtre glissante, clochettes, badge, filet de progression) |
| `verses_map.json` · `CARTE-VERS.md` | 49 vers → 34 plans, durées §6, 5 fenêtres de clochette, 0 manquant |
| `CONTROLE-mp4-final.jpg` · `CONTROLE-salve4.jpg` · `CONTROLE-typo-zoom.jpg` | planches de contrôle (cadres du MP4, textes peints, typo au zoom 1:1) |
| `ANCRE.md` · `CONTROLES.md` · `CONTROLES-salve2.md` · `PLAN_SALVE2.md` | mesures réelles, journaux de contrôle, plan |
| `livrables/paroles_clean.txt` · `timings_source.lrc` | paroles sans horodatages (USLT) · chronomètres de l'artiste conservés |

## 5bis · Contrôles du clip (mesures réelles sur le fichier livré)

| Contrôle | Commande | Résultat |
|---|---|---|
| Durée | `ffmpeg -i` | `Duration: 00:03:31.40` = 211,40 s = 6 342 frames / 30 — **exactement** `frames/fps` |
| Flux | `ffmpeg -i` | vidéo 1080×1920 h264 High yuv420p (bt709) 30 fps 2 035 kb/s · audio aac LC 48 kHz stéréo 253 kb/s |
| Frames noires | `blackdetect=d=0.05:pix_th=0.10` | **0** détection |
| Gels | `freezedetect=n=-33dB:d=2.5` | 4 segments signalés, tous voulus : 0→9,37 (carte d'accueil), 20,47→26,13 (clochette posée sur image fixe), 207,43→fin (carte finale). **Aucun gel sur les 49 segments de vers.** À `d=4.0` : 1 seul |
| Loudness clip | `ebur128` | I = **−14,0 LUFS** (cible −14) · RMS −14,76 dB |
| Crête clip | `astats` | **−1,011 dB** (MP3 source à −1,24 dB, +0,23 dB introduits par le décodage AAC) |
| Streaming | octets d'en-tête | `moov` à l'octet 36, `mdat` à 221 860 → **faststart OK** |
| Typo peinte | zoom 1:1 (`CONTROLE-typo-zoom.jpg`, `CONTROLE-mp4-v3-titre.jpg`) | nette, **aucun ghosting** (le 1er rendu faisait un blend de deux échelles : corrigé en travelling par fenêtre glissante, zéro ré-échantillonnage par frame) |

## 5ter · Retouche de typographie peinte (seule intervention manuelle sur les visuels)

- **`fonds/v-152-10.png` — « MAHU TI TÈ GBE »** : le modèle n'a pas écrit le accent grave du second « GBÈ »
  (2 tentatives de régénération, dont un édit ciblé : le caractère restait absent). Faute corrigée par **copie du « È »
  déjà peint par le modèle sur « TÈ »** (patch 25×26 px, masque = pixels or de l'ilot, MxFilter 3 + flou 0,9,
  collé en x 668..693, y 636..661) — même matière, même inclinaison, aucune lettre recomposée à la police.
  Vérification : `QC-accent-zoom.jpg` (grille 16 px) et `QC-accent-final.jpg`. Aucun autre plan n'a été retouché :
  les 33 autres textes peints sont sortis tels quels du générateur et relus (`CONTROLE-salve4.jpg`, cartes aube).
- Les reprises 160,26 / 166,97 portent bien « TÈ GBÈ » accentué dès la génération ; le texte peint de chaque variante
  correspond au vers chanté (contrôle vers→image ligne à ligne dans `CARTE-VERS.md`).

## 6 · Commandes Termux (une ligne par fichier, séparateur `;`)

Récupération du commit livré (hash vérifié sur la branche distante) :

```
cd ~/lyric ; git fetch origin arena/21016a0d-lyric ; git checkout e34df944577af852f2ca99f91a0bd4c892b851d8 ;
```

Fichiers (le `;` final laisse la chaîne s'exécuter jusqu'au bout) :

```
curl -L -o "mahu-ti-te-gbe-916.mp4" "https://github.com/Stein500/lyric/raw/e34df944577af852f2ca99f91a0bd4c892b851d8/productions/mahu-ti-te-gbe/livrables/mahu-ti-te-gbe-916.mp4";  # clip 9:16 57,9 Mo;
curl -L -o "Mahu ti tè gbè - master 320k.mp3" "https://github.com/Stein500/lyric/raw/e34df944577af852f2ca99f91a0bd4c892b851d8/productions/mahu-ti-te-gbe/livrables/Mahu%20ti%20t%C3%A8%20gb%C3%A8%20-%20master%20320k.mp3";  # master 320k;
curl -L -o "cover-1080.jpg" "https://github.com/Stein500/lyric/raw/e34df944577af852f2ca99f91a0bd4c892b851d8/productions/mahu-ti-te-gbe/livrables/cover-1080.jpg";  # pochette 1080;
curl -L -o "cover-916.jpg" "https://github.com/Stein500/lyric/raw/e34df944577af852f2ca99f91a0bd4c892b851d8/productions/mahu-ti-te-gbe/livrables/cover-916.jpg";  # cover verticale;
curl -L -o "carte-accueil.jpg" "https://github.com/Stein500/lyric/raw/e34df944577af852f2ca99f91a0bd4c892b851d8/productions/mahu-ti-te-gbe/livrables/carte-accueil.jpg";  # carte accueil;
curl -L -o "carte-finale.jpg" "https://github.com/Stein500/lyric/raw/e34df944577af852f2ca99f91a0bd4c892b851d8/productions/mahu-ti-te-gbe/livrables/carte-finale.jpg";  # carte finale;
curl -L -o "rendu_stats.json" "https://github.com/Stein500/lyric/raw/e34df944577af852f2ca99f91a0bd4c892b851d8/productions/mahu-ti-te-gbe/livrables/rendu_stats.json";  # stats du rendu;
curl -L -o "CARTE-VERS.md" "https://github.com/Stein500/lyric/raw/e34df944577af852f2ca99f91a0bd4c892b851d8/productions/mahu-ti-te-gbe/CARTE-VERS.md";  # carte des 49 vers;
curl -L -o "PROMPT_UNIVERSEL_v5.8.md" "https://github.com/Stein500/lyric/raw/e34df944577af852f2ca99f91a0bd4c892b851d8/PROMPT_UNIVERSEL_v5.8_MAHU_TYPO_PEINTE.md";  # prompt a jour (racine);
```

## 7 · Points ouverts (livrés comme non finis)

1. **Calage des mots provisoire** (formule §6 du prompt) : les durées d'affichage par vers ne sont pas calées mot à mot
   sur la voix. À valider à l'écoute, surtout vers 118-124 s où les lignes s'enchaînent à 1,4 s d'écart.
2. **Clochettes : 5 fenêtres, pas 9.** La liste « brute » des 9 trouées ≥ 5 s empiétait sur la lecture de vers en cours
   (interdit par §3). Recalculées en [fin d'affichage + 0,15 s → vers suivant] avec seuil 4,00 s, il reste
   12,50→17,24 · 20,34→26,06 · 175,42→182,73 · 192,00→196,07 · 199,10→206,40. Les 4 trouées écartées font moins de
   4 s une fois le vers lu. Si tu veux les 9, il faut abaisser le seuil à 3,0 s : une ligne à changer dans le moteur.
3. **Deux plans à la limite des zones sûres** : `scene-16` (bloc bas ≈ y 1560) et `scene-18` (bloc haut ≈ y 150).
   Gardés tels quels, régénérables si tu veux de la marge.
4. **Rendu en CRF 24 / veryfast** (réglage du prompt). Pour un upload qui repacke, c'est large ; pour archiver au
   maximum, relancer avec `--crf 18 --preset slow` (~2,5× plus long, ~2,5× plus lourd).

Déjà fermé depuis la 1re livraison : les 3 vers sans plan (`v-120-11`, `v-148-92`, `v-152-10`), les 3 variantes aube
des reprises (160,26 / 163,62 / 166,97) et le clip 9:16 lui-même.
