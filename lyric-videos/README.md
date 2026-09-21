# 🎬 DSKY LYRIC VIDEOS 🇧🇯 — clips karaoké

> **Projet TechStein / Daïsky** — clips verticalisés 1080×1920 pour les chansons de l'auteur
> **C. Jésutondji Samuel Stein « Dsky »** · Lyriciste · Bénin
>
> ⚠️ **Produit SÉPARÉ du projet `dsky-quotes`** (qui publie des *citations*). Ici, on affiche
> les **PAROLES des chansons**, synchronisées sur le master mp3 du repo. La charte graphique
> (badge DSKY 🇧🇯, liseré tricolore, signature, typographies Playfair/Montserrat) est
> **commune**, le contenu est distinct.

---

## 1. Principe

```
lyricvideo.py  ──►  MP4 1080×1920 (karaoké synchronisé) + .srt (YouTube) + mp3 master normalisé
      │
      ├── .lrc / .txt  du repo   → timings des paroles (karaoké ligne par ligne)
      ├── master .mp3  du repo   → audio (loudnorm −14 LUFS, coupe finale douce)
      ├── photos de l'auteur     → fonds (VISAGE JAMAIS MODIFIÉ, jamais flouté)
      └── fonds IA (f1…fN)       → ambiances générées (sans texte, sans visage)
```

**Règles tenues par le code**
| Règle | Implémentation |
|---|---|
| Visage intact | la photo est **recadrée**, jamais retouchée ; sur les photos : pas de flou, pas de déformation — seuls un voile dégradé et le grain « cinéma » s'appliquent |
| Paroles rendues PAR CODE (jamais par l'IA) | sprites PIL + remplissage progressif « karaoké » |
| Paroles au centre (§0.1 du prompt) | bloc centré horizontalement, bande verticale réglable (`--cy`, défaut 0,52) |
| Badge discret qui **vit avec les paroles** (§0.2) | fondu 0,4 s à l'apparition et à la disparition de chaque ligne, opacité ≈ 72 % |
| Endcard simple (§0.3) | titre cursif + WhatsApp + e-mail + badge |
| Liseré tricolore béninois | vert / jaune / rouge sur le bord inférieur (charte `dsky-quotes`) |
| Safe zones plateformes (§H) | badge y=150, paroles dans la zone centrale, rien sous y=1574 |

---

## 2. Morceau en cours : « Noukiko tché wê »

| Élément | Valeur |
|---|---|
| Paroles | `Noukiko.txt` (timestamps `[mm:ss.xx]`, 50 lignes) |
| Master audio | `Noukiko tché wê.mp3` — **165,96 s** |
| Dernière ligne | 150,91 s → 15 s d'outro musicale |
| Style détecté | **gold** (lexique : sourire, joie, soleil…) |
| Fonds | `noukiko/fonds/f1-couplet.jpg` · `f2-refrain.jpg` · `f3-pont.jpg` · `f4-endcard.jpg` |
| Sortie | `lyric-videos/noukiko/` |

> Les autres morceaux du repo (Seul dans ma tête, Drague moi 1, TOKO-LONGA, Guerrier,
> Le Survivant, Testostérone…) ne sont **pas** traités pour l'instant : on réalise
> **Noukiko uniquement**, puis on décidera de la suite.

## 3. Installation (aucun ffmpeg préinstallé au départ)

```bash
cd lyric-videos && bash setup_env.sh
```

Le script installe `pillow`, `numpy` et `imageio-ffmpeg` (binaire ffmpeg embarqué, aucune
compilation) puis vérifie l'environnement. Sous **Termux** : `pkg install -y python ffmpeg`
puis `pip install pillow numpy` — le script utilise le `ffmpeg` du système s'il existe
(sinon la variable d'environnement `FFMPEG`, sinon le binaire embarqué).

---

## 4. Utilisation

```bash
# contrôle rapide : 5 images PNG (aucune vidéo) — 8 s, à faire AVANT tout rendu long
python3 lyricvideo.py --song "Noukiko" --preview \
        --photo "../Snapchat-539918723.jpg" --photo "../Samuel/Snapchat-1058718015.jpg"

# clip complet (≈ 15 min pour 3-4 min de chanson)
python3 lyricvideo.py --song "Noukiko" \
        --photo "../Snapchat-539918723.jpg" --photo "../Samuel/Snapchat-1058718015.jpg" \
        --photo "../Samu/Snapchat-1029267384.jpg"

# extrait de contrôle (rapide) : de 60 s à 90 s
python3 lyricvideo.py --song "Noukiko" --start 60 --limit 30 --crf 24

# variantes
python3 lyricvideo.py --song "Noukiko" --style neon        # S3 Afro-futurism
python3 lyricvideo.py --song "Noukiko" --texte cursive      # paroles Playfair italique
python3 lyricvideo.py --song "Noukiko" --cy 0.44            # paroles plus haut (visage bas)
python3 lyricvideo.py --song "Noukiko" --fonds ../dsky-quotes/assets/bases   # sans photos
```

### Options

| Option | Défaut | Rôle |
|---|---|---|
| `--song` | — | titre (approché) ; le script apparie seul `.lrc`/`.txt` + `.mp3` |
| `--photo` (répétable) | — | photo réelle de l'auteur (visage préservé) |
| `--fonds DOSSIER` | dossier `fonds/` du morceau | banque d'images (IA et/ou photos) |
| `--style` | `auto` | `dark` · `gold` · `neon` · `ink` · `retro` (lexique du texte si `auto`) |
| `--texte` | `droit` | `droit` (Montserrat) ou `cursive` (Playfair italique) |
| `--cy` | `0.52` | hauteur du bloc de paroles (0,30 haut → 0,66 bas) |
| `--hook` / `--start` / `--limit` | 0 | cold-open, rendu partiel |
| `--crf` / `--fps` | 19 / 30 | qualité / cadence |
| `--preview` | off | 5 PNG de contrôle au lieu de la vidéo |
| `--no-endcard` / `--no-srt` | off | désactiver la carte finale / les sous-titres |

### Sorties — `lyric-videos/<morceau>/`

```
<morceau>/
├── fonds/                  ← images IA d'ambiance (f1-couplet.jpg, f2-refrain.jpg, …)
├── work/                   ← cache non versionné (preview PNG, master.wav, video.mp4)
├── <Titre>_9x16.mp4        ← LE CLIP (1080×1920, audio normalisé)
├── <Titre>.srt             ← sous-titres pour YouTube
├── <Titre>_master_320k.mp3 ← master normalisé −14 LUFS / TP −1,8 dB
└── timings.json            ← timings normalisés (traçabilité)
```

---

## 5. Ce que fait automatiquement `lyricvideo.py`

1. **Appariement** paroles ↔ audio (normalisation accents / suffixes `Daïsky`, `Official Audio`…).
2. **Décodage** des `.lrc`/`.txt` en encodage mixte, parsing `[mm:ss.xx]`, `[mm:ss.x]`, `[m:ss]`.
3. **Classification des lignes** : paroles, refrain (lignes répétées ou contenant le titre),
   jingle `Wolof TechStein beat wê!`, didascalies `(Voix 1)…` (affichées en petit italique).
4. **Nettoyage des timings** : monotonie stricte + fenêtre mini entre vers ; les didascalies
   inline `(Voix 1) Mmh…` sont retirées à l'affichage (mais restent dans le `.srt` si utiles).
5. **Cadrage intelligent** : détection de peau → le **visage est placé à 30 % du haut**,
   les paroles passent sous le menton ; sur les fonds IA, la bande de paroles la moins
   détaillée est choisie et légèrement floutée pour la lisibilité.
6. **Scrim adaptatif** : voile dégradé calibré sur la luminance de la zone de paroles
   (+ 0,35 sur les photos pour garantir le contraste).
7. **Habitillage** : Ken Burns (zoom 1,02→1,09 + pan), crossfade 0,55 s entre plans,
   grain cinéma, liseré tricolore, badge DSKY 🇧🇯, carte de titre à l'intro, endcard.
8. **Audio** : loudnorm 2 passes (−14 LUFS / TP −1,8), coupe-bas 30 Hz, fondu final 1,4 s.
9. **Mux** : H.264 crf 19 + AAC 192 k + `+faststart`, et export du `.srt`.

---

## 6. Sons sans timestamps (Testostérone, Ayon dèkpè, …)

Le script **n'invente pas** de synchronisation : une paroles sans horodatage produit un clip
désynchronisé. Deux voies prévues par la consigne du projet :

1. **Recommandé** — l'auteur exporte le `.lrc` depuis son application de paroles et le dépose
   dans le repo (nom au choix, `Noukiko.txt` fonctionne déjà : le format `.lrc` est reconnu
   même dans un `.txt`) → rendu immédiat.
2. **Sinon** — création d'un `.lrc` ligne par ligne (assistant + validation de l'auteur).

Un alignement automatique sur les onsets audio est prévu comme option, mais il sera toujours
livré **à valider** : la règle d'or reste la validation humaine du timing.

---

## 7. Suite

- [x] moteur `lyricvideo.py` + environnement
- [x] moteur + fonds IA Noukiko (4 plans, style gold)
- [ ] clip **Noukiko tché wê**
- [ ] clips `.lrc` déjà propres : Je m'aime tellement · Drague moi 1 · TOKO-LONGA · Guerrier
- [ ] téléchargement direct des livrables (Termux, cf. §E.6 du prompt universel)
- [ ] chantier `.lrc` des 6 sons sans timestamps

**Signature :** « Wolof TechStein beat wê ! » ⚡
