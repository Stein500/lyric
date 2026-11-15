# PRODUCTION — MESÍAS (Live) · Averly Morillo

**État : audio reçu et mesuré — calage non vérifié à l'écoute.**

---

## 1 — FICHE DE PRODUCTION

```text
TITRE EXACT              : Mesías (Live)
ARTISTE À L'ÉCRAN        : Averly Morillo              (orthographe vérifiée sur la source)
LANGUES                  : espagnol (chant, défilant) / français (traduction, peinte)
PAROLES ET HORODATAGES   : data/paroles_source.lrc      (source lrclib.net id 7723062, durée 743 s)
AUDIO MAÎTRE             : data/master_mesias_audio_only.mp3  (piste audio du MP3 fourni, copie sans réencodage)
PAROLES AFFICHÉES        : espagnol = source intacte ; français = data/traduction_fr.py (traduction de travail à valider)
MODE                     : HYBRIDE (espagnol défilant + traduction peinte)
PEINTURE                 : MOTEUR (PIL, Bebas Neue, contour par dilatation)
COULEUR                  : COULEUR + palette indigo / ambre / crème (validée sur ancre)
STYLE                    : anime seinen peint, aquarelle douce, encrage net
PERSONNAGE / ANCRE       : assets/ancre_01.png — PROPOSÉE, non encore validée par l'artiste
INTRO / OUTRO            : intro carte titre/artiste 0 → 16,84 s ; outro 5,00 s à la fin du morceau
FILET                    : oui, en haut (y = 186) — la place de y = 1560 est prise par le bandeau
BANDEAU DÉFILANT         : oui ; texte = paroles espagnoles (3 lignes, y = 1252 → 1452)
STICKERS / CTA           : non demandés pour l'instant
TEASER                   : 15,00 s ; extrait PROPOSÉ [04:31,39 → 04:46,39] (refrain) — non validé
VERSIONS                 : maquette de démonstration + versions finales à venir
DOSSIER                  : productions/mesias/
```

**Sens de lecture de la vidéo :** la **traduction française est peinte dans l'image** (permanente,
traitée comme la typo d'un manga), et les **paroles espagnoles d'origine défilent** en bas, du plus
ancien (haut, estompé) au plus récent (bas, net). Rien n'est doublé, rien ne couvre le visage.

---

## 2 — CE QUI EST FAIT

| Élément | État | Fichier |
|---|---|---|
| Paroles espagnoles horodatées (190 occurrences) | fait, source conservée | `data/paroles_source.lrc` |
| Traduction française des 117 textes distincts | fait, **à valider** | `data/traduction_fr.py` |
| Contrat de vers | fait, calage **provisoire** | `data/verses_map.json`, `CARTE-VERS.md` |
| Moteur de lettrage + zones sûres | fait, testé | `scripts/render.py` |
| Moteur vidéo (mouvement sans flou sur les mots) | fait, testé | `scripts/render_video.py` |
| Ancre visuelle couleur | proposée | `assets/ancre_01.png` |
| Salve 1 — vers 1 à 10 | générée et contrôlée | `assets/ancre_01.png`, `plan_02 … plan_09.png`, `img_010.png` |
| Salve 2 — vers 11 à 20 | générée et contrôlée | `assets/img_v011 … img_v020.png` |
| Salve 3 — vers 21 à 30 | générée et contrôlée | `assets/img_v021 … img_v030.png` |
| Maquette vers 1→12 (44,40 s) | rendue | `work/maquette_1-12.mp4` |
| Salve 4 — pool polyvalent (10 plans) | générée et contrôlée | `assets/pool_01 … pool_10.png` |
| Maquette vers 11→20 (30,77 s) | rendue | `work/maquette_11-20.mp4` |
| Maquette vers 31→60 (1:40,43) | rendue | `work/maquette_31-60.mp4` |
| Audio maître récupéré du dépôt | fait, mesuré | `data/master_mesias_audio_only.mp3` |
| Master normalisé MP3 320 | rendu et mesuré | `livrables/Averly Morillo - MESIAS (master normalise -14LUFS).mp3` |
| Aperçu synchro image + audio | rendu | `livrables/APERCU_AUDIO_vers1-12_44s.mp4` |
| Tag de paroles du MP3 | extrait, **non retenu** (voir §3) | `data/paroles_du_master.lrc.txt` |

### Mesures réelles sur la maquette
- `work/maquette_1-12.mp4` : 1080 × 1920, 30 i/s, yuv420p, BT.709, H.264, 1332 frames.
- Ces chiffres portent **sur la maquette seul**, pas sur un livrable final.

### Ce qui n'est PAS fait
- **Aucun MP3 final, aucun clip complet, aucun teaser, aucune couverture.**
- **Pas de piste audio** : rien n'a été généré, remplacé ni réinterprété.
- **Avec les 40 images actuelles, les 190 vers sont couverts** : plus rien ne bloque côté visuel.
  Le pool peut encore être étoffé (10 plans par salve) pour varier davantage.
- Aucune écoute, donc aucune fin de vers mesurée.

---

## 3 — L'AUDIO REÇU : MESURES RÉELLES

Fichier d'origine : `Averly Morillo - MESIAS.mp3`, 8 954 974 octets, poussé par l'artiste sur
`origin/main` (sha blob `6e567eb`). Contenu : MP3 96 kb/s, **48 kHz, stéréo**, pochette MJPEG 480×265.

| Mesure | Valeur | Outil |
|---|---|---|
| Durée décodée | **744,705 s** (12:24,705) | ffmpeg 9.0.2, décodage intégral |
| LUFS intégré | **−8,7 LUFS** | filtre `ebur128=peak=true` |
| Crête vraie | **+4,7 dBFS** (échantillons en écrêtage) | idem |
| LRA | **11,0 LU** | idem |
| Silence final | 739,349 → 744,709 s (5,360 s) | `silencedetect=n=-40dB:d=1.5` |

**Conséquences directes :**
- la timeline des paroles est compatible avec le fichier (dernier vers à 12:17,22, silence final à
  12:19,35) : aucun décalage global à appliquer ;
- le fichier est **très fort et écrêté**. Normalisation appliquée (`loudnorm` deux passes,
  `linear=true`, cible `I=-14:TP=-1.5:LRA=11`, 48 kHz stéréo, MP3 CBR 320, `-vn`, tags relus) :
  **résultat mesuré −14,1 LUFS, crête vraie −1,5 dBFS, LRA 9,1 LU**. Le `loudnorm` a basculé en
  mode **dynamique** (et non linéaire) parce que la crête d'entrée était à +4,7 dBFS : impossible de
  descendre de 5,3 dB en linéaire sans dépasser la cible de crête. C'est déclaré, pas caché ;
- le clip fera **744,705 + 5,00 = 749,705 s** (12:29,705) avec la carte finale.

### Le tag de paroles du MP3 n'est pas utilisable comme référence
Le fichier porte un `USLT` de 175 lignes horodatées, mais c'est un **résumé fautif** :
lignes fourre-tout (« Oh ven amado ven amado hoy te llamo hoy » à 20,24 s), fragments d'un mot
(« te », « mi »), fautes (« miento » pour « gimiendo », « gimiento »), passages manquants
(11:39 → 6:57 absent). Il a donc été extrait et conservé pour information
(`data/paroles_du_master.lrc.txt`) mais **n'a pas été retenu comme timeline**.

### Tentatives de vérification objective (et leur échec assumé)
- alignement des 190 vers sur les 739 mots du tag : 158 ancrés, mais écarts de −6,7 s à +13,2 s,
  incompatibles avec un texte aussi lacunaire → écarté ;
- corrélation de l'enveloppe d'énergie du master avec la timeline : le mix live est dense et sans
  silence entre les phrases (≈ 55 % du temps au-dessus du seuil adaptatif), l'attaque de voix ne
  se distingue pas → aucun décalage fiable n'en sort.

**Statut honnête : la timeline reste celle des paroles fournies, NON VÉRIFIÉE À L'ÉCOUTE.**
Pour la valider, il faut une écoute de contrôle (ou un calage mot à mot de l'artiste) sur quelques
points : 32,32 s, 1:38,76, 4:31,39, 8:18,11, 12:17,22.

---

## 3 bis — BLOCAGE LEVÉ



Je n'ai **pas** téléchargé « le MP3 en ligne ». Raisons vérifiables :

1. Les paroles de cet enregistrement sont protégées (écrivains crédités : Averly Morillo,
   Janiel Ponciano, Jose Silverio Green, Junior Ponciano) et le flux officiel n'est pas
   accessible depuis cet environnement ; les copies qui circulent sur des hébergeurs tiers
   sont des republications non autorisées.
2. Le prompt v7 §3 impose d'utiliser **l'audio maître réel fourni par l'artiste**, jamais un
   fichier récupéré au hasard : une prise live de 12:23 peut décaler de plusieurs secondes,
   ce qui ruinerait la synchronisation de 190 vers.
3. Sans le fichier, je ne peux pas mesurer les fins de vers, vérifier les syllabes tenues ni
   placer un CTA sans risque.

**Ce qu'il me faut :** `Mesías (Live) — Averly Morillo` en MP3 (ou WAV/M4A), poussé sur **`master`**
(le dépôt `Stein500/lyric` n'a pas de branche `main` : la branche par défaut s'appelle `master`).
Vérifié le 15/11/2026 : aucun fichier MESÍAS n'y est encore ; seul `i'm not dying 1 Techstein.mp3`
est présent. Dès qu'il arrive, je mesure durée décodée, LUFS, crête vraie et LRA, puis je recale
le contrat sur le fichier réel.

---

## 3 bis — RÈGLE DE PRODUCTION VISUELLE

- **Images polyvalentes** (décision du 15/11/2026) : les vers 1 → 30 gardent leur plan dédié
  (progression d'ouverture), puis les vers 31 → 190 puisent dans un **pool réutilisable de 10 plans
  thématiques** (`assets/pool_01 … pool_10`), assignés par règle sémantique dans
  `scripts/assign_pool.py` : jamais deux fois de suite la même image, jamais la même à moins de
  2 vers d'écart. Le pool réemploie aussi les plans dédiés existants (ancre, nef, cierges, porte).
- **10 images par salve**, jamais plus. État : salves 1, 2, 3 (dédiées) + salve 4 (pool polyvalent).
- Couverture du morceau : **40 images** pour 190 vers. Ajouter un plan au pool = couvrir d'autres
  vers sans régénérer, il suffit de relancer `assign_pool.py`.
- Chaque image reçoit `NO TEXT AT ALL` au générateur ; tout le texte est cuit par le moteur.
- Contrôle de salve : planche contact, vérification du visage, des mains, du cadrage, de la palette,
  puis normalisation en 1080 × 1920 (ancrage en haut, bas complété par le fond flouté).

---

## 4 — DÉCISIONS QUI RESTENT À PRENDRE

1. **Ancre** : le personnage ci-dessous te convient-il (visage, cheveux, tunique blanche, palette
   indigo/ambre/crème) avant que je génère les 108 plans restants ?
2. **Traduction** : je te la relis intégralement ; tu corriges les vers dont le sens ne te va pas.
3. **Teaser** : l'extrait proposé est `[04:31,39 → 04:46,39]` (le refrain « Ven, ven, ven… »).
   Tu en veux un autre ?
4. **Habillage** : garde-t-on le filet en haut et le badge `AVERLY MORILLO` ↔ `WTBW`, et veut-on
   les trois stickers d'intro/outro ?

---

## 5 — COMMANDES DE REPRODUCTION

```sh
cd productions/mesias
python3 -c "import sys;sys.path.insert(0,'scripts');import render;render.base_image('assets/plan_04.png').save('work/base/plan_04.png')"
python3 scripts/render.py                       # images de base 1080x1920
python3 scripts/render_video.py --from 1 --to 12 --out work/maquette.mp4   # maquette
python3 scripts/carte_vers.py                    # régénère CARTE-VERS.md
```

Dépendances : `pillow`, `imageio-ffmpeg` (ffmpeg 9.0.2 embarqué, `libx264` + `aac` disponibles).
Police : `assets/fonts/BebasNeue-Regular.ttf` (SIL OFL 1.1, licence jointe).
