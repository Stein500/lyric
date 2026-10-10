# 🚀 DSKY QUOTES — DOSSIER SAISON 2
### Améliorations, restrictions honnêtes & plan Lyrics-Vidéos
*Préparé d'après l'analyse du repo `lyric` (mp3, .lrc, .txt) et de la Saison 1 (84 visuels livrés).*

---

## 1️⃣ RESTRICTIONS & RÉALITÉS TECHNIQUES (à connaître)

| # | Restriction | Impact | Parade |
|---|---|---|---|
| R1 | **≈ 10 générations d'images IA par session** | 1 salve = 10 visuels max par tour | on procède salve par salve (déjà notre rythme) |
| R2 | **Fidélité du visage** dépend de la photo source | photo floue/sombre = dérives possibles | photo nette, visage bien éclairé, ≥ 20 % du cadre ; je fais toujours une planche-contact de contrôle |
| R3 | **Texte 100 % codé (PIL), jamais généré par l'IA** | zéro faute, mais police réduite si citation très longue (> ~350 caractères) | option « 2 panneaux » (1/2, 2/2) pour les longues : 14, 22, 29 |
| R4 | **Workspace limité (~128 MB)** | ~15-18 salves en local max | GitHub =archive illimitée ; nettoyage régulier (déjà automatisé) |
| R5 | **ffmpeg non préinstallé** chez moi | vidéos = 1-2 clips par tour seulement | installation possible (imageio-ffmpeg) → pipeline lyric-video réaliste mais 1 son/session |
| R6 | **Échange de fichiers uniquement via GitHub** | je ne vois pas ton téléphone | tu pousses photos/sons/`.lrc`, j'exploite → le repo est notre studio |
| R7 | **Token = secret** | fuite = takeover du repo | révoquer après chaque série de pushes (déjà 2 fois brûlé 😅) |
| R8 | **Langues** : FR/EN impeccables ; wolof/fon affichables | orthographe locale à valider par toi | tu m'écris la ligne exacte, je l'incruste telle quelle |

---

## 2️⃣ SAISON 2 — AMÉLIORATIONS QUOTES

### Format
- **F1. Carré 1080×1080 en 3ᵉ format** (post LinkedIn/X, profil) → généré automatiquement avec chaque quote
- **F2. Panneaux 1/2 · 2/2** pour citations longues → carousel Instagram
- **F3. Numérotation de saison** : `S2 · N°01` (redémarre à 1, pas de confusion avec la Saison 1)

### Design
- **F4. Mode « son associé »** : chaque quote porte en signature un vers de ta musique
  → ex : quote « Ce qui t'aime… » (24) taguée *— « Seul dans ma tête », 2026* → cross-promo musique ↔ quotes
- **F5. Fils d'ambre (watermark) DSKY semi-transparent** au centre : anti-réposte sans crédit
- **F6. Fonds par univers de son** :
  *Guerrier* → braises/ocre · *Le Survivant* → rouge sombre/guitare · *Je m'aime tellement* → piano/or doux · *Testostérone* → noir mat/rouge sang · *Seul dans ma tête* → bleu 3h du matin, lune, horloge · *Drague moi* → rose néon · *Je crache mes démons* → fumée grise · *Je suis pauvre et riche* → billets stylisés/or
- **F7. Lien streaming / QR discret** (YouTube, Audiomack…) si tu m'en fournis

### Photos (checklist pour la Saison 2)
- **F8. Envoie-moi 6-8 nouveaux clichés** : de dos, contre-jour, mains croisées, assis sur un tabouret, grand-angle plein pied, rire franc, regard caméra, profil gauche **et** droit
  → plus de poses = plus de variété = des salves encore moins répétitives

---

## 3️⃣ LYRICS VIDÉOS — LE PLAN (priorité demandée)

**Ce que j'ai trouvé dans `lyric@main`** :
- ✅ `.lrc` propres (timestamps précis) : *Seul dans ma tête*, *Je m'aime tellement*, *Drague moi 1*, *TOKO-LONGA*
- 🟡 *guerrier.txt* — déjà au format `[mm:ss.xx]` → convertible tel quel
- 🟡 *le survivant… timing.txt* — timing approximatif (`-0:25`) → à normaliser
- 🔴 *Testostérone, Je crache les démons, Ayon dèkpè, Nan yi a ga djin wê, yafoy, Je suis pauvre et riche* — sans timestamps
- 🎵 masters mp3 présents (racine + `Samu/`) — parfait pour coller l'audio

### Produits possibles (par ordre de valeur)
| Produit | Description | Faisabilité |
|---|---|---|
| **L1. Lyric Video officiel** (MP4 1080×1920) | fond IA (ta photo, visage intact) + paroles **karaoké ligne par ligne** suivant le `.lrc` + badge DSKY 🇧🇯 + liseré + l'audio du master → prêt YouTube/Statut | ✅ ~1 clip par session (R5) ; nécessite `.lrc` propre |
| **L2. Quote animée 5-8 s** | zoom lent sur la quote + apparition du texte ligne à ligne, sans audio | ✅ très rapide, idéal Reels/Statut quotidien |
| **L3. Audiogramme 30 s** | forme d'onde animée + cover du son + extrait → teaser TikTok/YT Shorts | ✅ |
| **L4. Normalisation des lyrics** | je convertis `guerrier.txt` en `.lrc` immédiatement ; les autres exigent les timestamps exacts | 🟡 collaborative : soit tu exportes les `.lrc` de ton app karaoké, soit tu me valides ligne par ligne |
| **L5. Sous-titres `.srt`** | exportés avec chaque vidéo → upload YouTube propre | ✅ automatique avec L1 |

### Pipeline proposé (à construire au prochain tour)
```
lyric-videos/
├── seul-dans-ma-tete/
│   ├── audio.mp3        ← déjà dans le repo
│   ├── paroles.lrc      ← déjà dans le repo ✅
│   └── fond.jpg         ← base IA générée (ta photo)
└── ...
+ lyricvideo.py          ← moteur : fond + karaoké .lrc + audio → MP4 + .srt
```
**Premier clip recommandé : « Seul dans ma tête »** (le `.lrc` est le plus propre et le thème colle aux fonds nuit « 3h du mat »).

---

## 4️⃣ PROCESS Amélioré pour la Saison 2
1. Tu ouvres un dossier `saison-2/` dans `lyric` avec : nouvelles photos + nouveaux textes + (option) `.lrc`
2. Moi : correction des textes → JSON de salve → génération → planche-contact de contrôle → push → lien Termux
3. Chaque session se termine par : push + commandes Termux de la session

*— Document vivant : modifie-le ou dicte-moi tes choix, j'actualise.*
