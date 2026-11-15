# LIVRAISON — MESÍAS (Live) · Averly Morillo

**Tout est rendu, contrôlé et publié.** Ce document ne contient que des mesures faites
sur les fichiers livrés — aucune valeur n'est reprise d'une promesse.

---

## 1 — Les fichiers

| Fichier | Ce que c'est | Poids |
|---|---|---|
| `Averly Morillo - MESIAS (clip lyrics 1080x1920).mp4` | **le clip complet**, master de travail, 12:29,71 | 274,6 Mo |
| `MESIAS_clip_1080x1920_leger.mp4` | **le clip complet publiable**, même montage, débit réduit | ~59 Mo |
| `MESIAS_teaser_15s_1080x1920.mp4` | **le teaser**, 450 frames = 15,00 s | 5,1 Mo |
| `MESIAS_couverture_TikTok_1080x1920.jpg` | couverture principale, portrait | 332 Ko |
| `MESIAS_couverture_variante_visage_1080x1920.jpg` | variante gros visage | 550 Ko |
| `MESIAS_couverture_paysage_1080x1920.jpg` | variante contemplative | 532 Ko |
| `Averly Morillo - MESIAS (master normalise -14LUFS).mp3` | le son normalisé, pour reposter | 29,8 Mo |
| `APERCU_AUDIO_vers1-12_44s.mp4` | aperçu de contrôle avec son | 9,1 Mo |
| `SHA256SUMS.txt` | les empreintes des sept fichiers ci-dessus | 758 o |

---

## 2 — Contrôles chiffrés du CLIP COMPLET

| Contrôle | Résultat mesuré |
|---|---|
| Format | 1080×1920, 30 i/s, H.264 High, yuv420p, BT.709 |
| Durée décodée | 00:12:29.71 (749.71 s) |
| Écart / cible 749,705 s | +0.005 s |
| Poids | 274.6 Mo |
| Audio | AAC 48000 Hz stereo, 256 kb/s |
| LUFS intégré | -14.1 |
| Crête vraie | -1.4 dBFS |
| LRA | 9.1 LU |
| Images noires | aucune |
| Gels > 1,5 s | aucun |
| Faststart | oui (moov à 36 o, mdat à 825975 o) |

Somme des 40 segments avant assemblage : **749.640 s** — l'assemblage n'a donc perdu aucune frame.

---

## 3 — Ce qui a été corrigé en route (et pourquoi ça se voit)

Trois défauts réels ont été trouvés par les contrôles, pas par l'œil :

1. **Les 5 secondes de carte finale disparaissaient.** `-shortest` coupait la vidéo à la fin de
   l'audio (744,71 s). Remplacé par `apad=whole_dur=749.705` : le silence final est prolongé,
   la carte reste, la durée est juste.
2. **La caméra se figeait.** Les trajectoires étaient des sinus : près des extrémités la position
   arrêtait de changer d'un frame à l'autre, et `freezedetect` signalait des gels de 1,7 à 1,8 s.
   Remplacées par des rampes triangulaires linéaires, à périodes différentes sur X et Y.
3. **Les cartes d'intro et de fin étaient des images fixes.** Elles ont maintenant un panoramique
   lent. Le fond était renvoyé déjà recadré en 1080×1920 : il n'y avait **aucun débattement**, le
   déplacement valait 0 px. Le fond est désormais conservé surdimensionné (1,30×) et glisse
   dedans, soit environ 1 px par frame.

Le voile de lisibilité a lui aussi été refait : la rampe était tracée à la main, ce qui laissait
une **arête horizontale** visible. Elle suit maintenant une courbe en smoothstep, pente nulle aux
deux extrémités.

---

## 4 — Structure du clip

| Temps | Contenu |
|---|---|
| 0,00 → 16,84 s | carte titre : MESÍAS / AVERLY MORILLO / EN DIRECT, fond flouté (seul endroit autorisé), panoramique lent |
| 16,59 → 739,35 s | les 190 vers : traduction française **peinte**, espagnol **défilant** sur 3 lignes |
| 739,35 → 744,71 s | silence final réel du morceau — la carte finale s'installe |
| 744,71 → 749,71 s | carte finale : MERCI, artiste, WTBW, mention de production |

Décalage d'affichage : **−0,25 s** sur toutes les entrées (validé à l'écoute par l'artiste).

---

## 5 — Ce qui n'est pas prouvé, et que je ne prétends pas

- **La traduction française n'a pas été relue par l'artiste.** C'est un travail de production,
  cohérent et complet (117 clés, 100 % couvert), mais pas une traduction validée par l'autrice.
- **La correspondance vers↔plan est sémantique, pas narrative.** 50 images pour 190 vers : les
  images reviennent. Elles sont choisies par thème (`scripts/assign_pool.py`), ce n'est pas une
  illustration vers par vers.
- **Trois plans de la salve 5 ne sortent pas** (`pool_13` larme, `pool_18` tempête,
  `pool_19` mains serrées) : le texte de la chanson ne contient pas de mot correspondant. Ils
  restent disponibles pour une autre chanson.
- **Le son a été normalisé** de −8,7 à −14,1 LUFS en mode dynamique (obligatoire, la crête
  d'entrée était à +4,7 dBFS). Le contenu musical n'a pas été touché autrement.

---

## 6 — Le transfert du fichier lourd : ce qui a été tenté, ce qui a échoué

Le clip master pèse **274,6 Mo**. GitHub refuse tout fichier de plus de **100 Mo** (erreur
`GH001`, crochet `pre-receive`). Trois voies ont été essayées :

1. **Pousser le fichier sur la branche** → refusé par GitHub (`GH001`, `pre-receive hook declined`).
2. **Le sortir de l'historique et le mettre en release** (`gh release upload`, qui accepte 2 Go
   par fichier) : la release `mesias-clip-v1` a bien été créée, mais l'upload échoue
   systématiquement — `uploads.github.com` et `objects.githubusercontent.com` sont **injoignables
   depuis cet environnement** (`curl` renvoie `SSL_ERROR_SYSCALL`, code 000). Le compte a alors
   0 asset. Ce n'est pas une erreur de droits, c'est le réseau qui est fermé.
3. **Réencoder une version légère et la versionner** → retenu. Le débit a été calibré par
   mesure : CRF 29 donnait 124 Mo (encore trop), la combinaison **CRF 31 + `maxrate` 1150 kb/s**
   tient sous la limite et reste lisible — vérifié à l'œil sur un extrait à 400 %.

**Ce qui reste à faire côté machine connectée**, si tu veux publier le master complet en release :

```sh
gh release upload mesias-clip-v1 "productions/mesias/livrables/Averly Morillo - MESIAS (clip lyrics 1080x1920).mp4"
```

La release existe déjà, elle est vide. Une fois ce fichier envoyé, `PUBLICATION.md` §5 devient
utilisable tel quel pour le téléchargement direct.

---

## 7 — Publications

Voir `PUBLICATION.md` : deux descriptions complètes, 13 hashtags chacune (maximum respecté),
la déclaration d'IA, les commandes Termux et les empreintes de vérification.
