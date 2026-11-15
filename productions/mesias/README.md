# PRODUCTION — MESÍAS (Live) · Averly Morillo

**État : en cours — blocage sur la matière première audio.**

---

## 1 — FICHE DE PRODUCTION

```text
TITRE EXACT              : Mesías (Live)
ARTISTE À L'ÉCRAN        : Averly Morillo              (orthographe vérifiée sur la source)
LANGUES                  : espagnol (chant, défilant) / français (traduction, peinte)
PAROLES ET HORODATAGES   : data/paroles_source.lrc      (source lrclib.net id 7723062, durée 743 s)
AUDIO MAÎTRE             : MANQUANT — à fournir par l'artiste
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

## 3 — BLOCAGE : LE MP3 DE L'ARTISTE

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
