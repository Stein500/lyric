# LIVRAISON — « Mahu ti tè gbè » (Dsky)

Production : 2026-10-10 · branche `arena/21016a0d-lyric` · moteur : PROMPT UNIVERSEL v5.7 + **v5.8 (typo peinte)**.
Hash des livrables : `6b16bac120fd98474fec54d7e1076d9d65b31001`

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

- **Visuels : OUI, générés par IA.** 31 plans distincts (19 blocs + 12 plans de vers, dont 3 restants), typographie,
  icônes et stickers **peints par le même modèle** dans l'image. Aucun plan issu d'une photo personnelle.
- **Audio : NON, aucun son généré.** Master = l'enregistrement de l'artiste, uniquement régénératif
  (loudnorm 2 passes, résample 48 kHz, MP3 320 kb/s, ID3). Écrêtage de la source (+0,06 dBTP) corrigé.
- Personnages : héros fictifs, tenues fermées, aucun contenu sexuel ou de nudité.

## 5 · Fichiers livrés

| Fichier | Détails |
|---|---|
| `livrables/Mahu ti tè gbè - master 320k.mp3` | 8 570 754 o · 206,40 s · 48 kHz · 320 kb/s CBR · −14,0 LUFS · crête −1,24 dB · pochette 1080 + USLT fre 49 lignes |
| `livrables/cover-1080.jpg` (+ `.png`) | pochette carrée 1080×1080, tête non rognée |
| `livrables/cover-916.jpg` | cover verticale 1080×1920 (plan aube `scene-19`) |
| `livrables/carte-accueil.jpg` · `livrables/carte-finale.jpg` | Montserrat ExtraBold/SemiBold, code `0326`, aucun contact |
| `fonds/scene-01-ancre.png` → `scene-19.png` · `fonds/v-*.png` | 28 plans peints et contrôlés (orthographe vérifiée) |
| `verses_map.json` · `CARTE-VERS.md` | 49 vers → 31 plans, durées §6, 3 plans restants listés |
| `ANCRE.md` · `CONTROLES.md` · `CONTROLES-salve2.md` · `PLAN_SALVE2.md` | mesures réelles, journaux de contrôle, plan |
| `livrables/paroles_clean.txt` · `timings_source.lrc` | paroles sans horodatages (USLT) · chronomètres de l'artiste conservés |

## 6 · Commandes Termux (une ligne par fichier, séparateur `;`)

```
cd ~/lyric ; git fetch origin arena/21016a0d-lyric ; git checkout 6b16bac120fd98474fec54d7e1076d9d65b31001 ;
```

```
curl -L -o "Mahu ti tè gbè - master 320k.mp3" "https://github.com/Stein500/lyric/raw/6b16bac120fd98474fec54d7e1076d9d65b31001/productions/mahu-ti-te-gbe/livrables/Mahu%20ti%20t%C3%A8%20gb%C3%A8%20-%20master%20320k.mp3";
curl -L -o "cover-1080.jpg" "https://github.com/Stein500/lyric/raw/6b16bac120fd98474fec54d7e1076d9d65b31001/productions/mahu-ti-te-gbe/livrables/cover-1080.jpg";
curl -L -o "cover-916.jpg" "https://github.com/Stein500/lyric/raw/6b16bac120fd98474fec54d7e1076d9d65b31001/productions/mahu-ti-te-gbe/livrables/cover-916.jpg";
curl -L -o "carte-accueil.jpg" "https://github.com/Stein500/lyric/raw/6b16bac120fd98474fec54d7e1076d9d65b31001/productions/mahu-ti-te-gbe/livrables/carte-accueil.jpg";
curl -L -o "carte-finale.jpg" "https://github.com/Stein500/lyric/raw/6b16bac120fd98474fec54d7e1076d9d65b31001/productions/mahu-ti-te-gbe/livrables/carte-finale.jpg";
curl -L -o "PROMPT_UNIVERSEL_v5.8.md" "https://github.com/Stein500/lyric/raw/6b16bac120fd98474fec54d7e1076d9d65b31001/PROMPT_UNIVERSEL_v5.8_MAHU_TYPO_PEINTE.md";
```

## 7 · Points ouverts (livrés comme non finis)

1. **3 vers sans plan peint** : `v-120-11` (échec du modèle), `v-148-92`, `v-152-10` → à générer au prochain tour
   (limite de 10 générations par tour atteinte). En attendant, le montage utilisera le plan du vers précédent.
2. **Clip 9:16 non encore rendu** : `render_lyric_video.py` à écrire sur `verses_map.json` (1 plan/vers, fondu 0,35 s,
   badge « Dsky » en y=160, un seul fondu par vers, clochettes dans les 9 fenêtres ≥ 5 s, cartes 0→9,33 s et
   206,40→211,40 s), H.264 CRF 24 + AAC 256 + `+faststart` + bt709, puis contrôles `blackdetect`/`freezedetect`.
3. **Calage des mots provisoire** (formule §6) : à valider à l'écoute, notamment vers 118-124 s où les lignes se
   suivent très vite (1,4 s d'écart).
4. Deux plans à la limite des zones sûres : `scene-16` (bloc bas ≈ y 1560) et `scene-18` (bloc haut ≈ y 150).
   Gardés, régénérables si tu veux la marge.
5. Reprises de refrains qui réutilisent un plan « nuit » en pleine séquence aube → 3 variantes aube possibles
   (`v-160-26`, `v-163-62`, `v-166-97`) si tu veux 100 % de continuité.
