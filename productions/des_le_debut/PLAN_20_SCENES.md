# « Dès le début » — plan de production 20 scènes × 2 formats = 40 fonds

**Choix validés par l'artiste (2026-10-04)** : héros **inventés** · **aucune photo** envoyée au générateur ·
**40 fonds** (20 scènes × 2 formats) · clochettes **comme l'aperçu** · paroles **mixtes** · style **S6 Aube Sacrée** (proposé).

---

## 1. Comment on obtient l'effet « la personne bouge »

Aucune IA ne produit une vraie animation à partir de 20 images : l'illusion vient de **3 couches combinées**,
c'est exactement la méthode des clips VN / CapCut.

1. **Chorégraphie** — les 20 scènes sont **des instants successifs d'une même action** dans la même pièce :
   l'homme pose la croix → se lève → ouvre les bras → la femme le rejoint → ils s'agenouillent → les mains se lèvent…
   Le spectateur lit une continuité, pas 20 images séparées.
2. **Continuité stricte** — même pièce, même sens de lumière, mêmes vêtements, mêmes tatouages, même position des visages
   (bloc héros recopié mot pour mot).
3. **Mouvement de caméra continu** — Ken Burns 1,1× (zoom 1,02→1,08 alterné) + pan sinusoïdal sur **chaque** fond,
   fondus de 0,4 s entre scènes → le raccord entre deux images ne se voit pas.

## 2. Les 20 scènes (portrait 1080×1920 / paysage 1920×1080)

| # | Plage | Paroles / section | Plan | Action (le storyboard continue) | Lumière |
|---|---|---|---|---|---|
| s01 | 0:00–0:06 | *intro instrumentale* | wide | pièce vide à l'aube, portière entrouverte, rayons qui traversent la poussière | dim |
| s02 | 0:05–0:29 | « Wolof TechStein beat wê… » / Couplet 1 | wide | l'homme entre, la croix de bois à la main, s'arrête au centre | dim→modérée |
| s03 | 0:12–0:29 | « Roi des rois » / « Tu as donné ta vie » | medium | il pose la croix sur un tabouret, tête baissée | modérée |
| s04 | 0:29–0:41 | « Dès le début, Tu m'as aimé » (pré-refrain, voix féminine) | close-up | ses avant-bras tatoués, mains qui se joignent | modérée |
| s05 | 0:41–0:52 | « Ton nom est éternel » | medium | la femme apparaît dans le rai de lumière, linge blanc contre la poitrine | full |
| s06 | 0:52–1:02 | refrain | wide | les deux côte à côte, chacun dans un rayon | full |
| s07 | 1:02–1:20 | Couplet 2 « Tu connaissais mon nom » | medium-close | elle pose le linge, lève les yeux vers la fenêtre | modérée |
| s08 | 1:20–1:32 | « Avant ma naissance » | close-up | mains de l'homme qui se tendent vers la lumière | modérée |
| s09 | 1:32–1:43 | « je Te suivrai toute ma vie » | medium | elle marche lentement vers la droite, il la suit du regard | modérée |
| s10 | 1:43–1:56 | « Jésus… Christ… Sauveur… » | close-up | reflet des deux visages dans une bassine d'eau qui tremble | full |
| s11 | 1:56–2:03 | « Dès le début, Tu étais là » | wide | la poussière danse dans le rayon, silhouettes de dos | full |
| s12 | 2:03–2:12 | **break instrumental** | wide | ils s'agenouillent ensemble, lentement | full |
| s13 | 2:12–2:22 | break | close-up | mains jointes, auriculaire de la femme qui tremble | full |
| s14 | 2:22–2:31 | break | medium | ils se relèvent, la lumière bascule au doré | full→or |
| s15 | 2:31–2:41 | refrain final | wide | deux bras levés, paumes vers le ciel | or |
| s16 | 2:41–2:50 | « Je Te loue, je Te bénis » | medium | la femme sourit, l'homme baisse la tête, apaisé | or |
| s17 | 2:50–3:02 | outro « Wolof TechStein beat wê… » | wide | ils restent immobiles dans la lumière qui décline | décroissant |
| s18 | 3:02–3:10 | « Jésus… Christ… Sauveur… » | close-up | la croix de bois posée au sol, grain de poussière doré | décroissant |
| s19 | 3:10–3:20 | « Dès le début… toujours… » | wide | pièce vide, la porte se referme lentement | sombre |
| s20 | 3:20–3:20 | *endcard* | wide | pièce vide épurée, prête pour titre + contacts | sombre épuré |

> **s20 = fond endcard** (titre cursive + WhatsApp + e-mail + badge). **s01 = fond intro**.
> Aucun personnage dans s01/s20 : la lumière, la pièce, le silence.

## 3. Salves de génération (quota plateforme : 10 images / tour)

| Salve | Contenu | Images |
|---|---|---|
| **A** | s01→s05 en portrait | 5 |
| **B** | s01→s05 en paysage | 5 |
| **C** | s06→s10 des deux formats | 10 |
| **D** | s11→s15 des deux formats | 10 |
| **E** | s16→s20 des deux formats | 10 |

Règle de continuité : **l'ancre paysage sert de guide de style** (`images=`) pour toutes les générations suivantes,
avec le bloc héros recopié. Une scène refusée = on ne régénère **que** ce slot.

## 4. Clochettes CTA (règle validée « comme l'aperçu »)

Déclenchement sur **7 fenêtres sans parole > 5 s** (mesurées) :

`0:00–0:05,7` · `0:05,7–0:12,6` · `0:19,4–0:29,0` · `0:62,6–1:08,3` · `1:43,7–1:56,5` · **`2:06,6–2:31,8` (25,2 s)** · **`2:49,2–3:20,0` (30,8 s)**

- **≈ 97 s** de clochettes au total (≈ 48 % du clip).
- Une **séquence** = 3,0 s (entrée 0,35 s → maintien → sortie 0,35 s) ; dans les fenêtres longues,
  **répétition toutes les 4 s** (≈ 6 passages sur 25 s), jamais une icône figée.
- Animation : balancement ±12° / 1,2 s, halo pulsé 0,8 s, 2 anneaux d'onde, étincelles,
  flèche clignotante vers la cloche, **« PARTAGE » mis en avant** (contour cyan pulsé) + « ABONNE-TOI ».
- Dessin **vectoriel** (aucune emoji système) ; variante cloche « sonne » (double frappe) pour les fenêtres de 3-5 s si tu veux.
- Safe zones respectées : ni bande haute (y 0–144), ni rail droit (x ≥ 910 ∧ y 960–1690), ni bande basse (y ≥ 1574).

## 5. Paroles — mode « mixte » (ton choix)

- **Pendant les vers** → texte **centré H/2**, gros et gras, mot à mot hybride (mot actif or/crème,
  vague d'eau continue ≈ 4,5 px / 0,9 Hz), largeur sûre ≤ 720 px, aucune dérive de recentrage.
- **Pendant les clochettes** → le bandeau de paroles **remonte et s'estompe** (fondu 0,35 s) :
  la cloche occupe le centre. Le dernier mot reste 1,2 s, puis silence visuel.
  Si deux vers encadrent la fenêtre, le texte revient **exactement à la même position** (aucun saut perçu).
- Aucune parole au-dessus des visages pendant les gros plans (s10, s13) : bascule automatique en mode haut.

## 6. Réglages hérités v5.5 encore à confirmer (défauts appliqués si tu ne dis rien)

| Réglage | Défaut appliqué |
|---|---|
| Cold-open | extrait refrain-titre 6,0 s avant la chanson |
| Badge | `Dsky` + pictogramme Bénin, fondu 0,4 s **avec chaque vers**, opacité ≤ 75 % |
| Bandeau Bénin | portrait y 1866→1920 (54 px), vert/jaune/rouge #008751 · #FCD116 · #E8112D |
| Master | chanson seule, 48 kHz, MP3 320 kb/s, APIC + USLT, loudnorm 2 passes (−14 LUFS / −1,8 dBTP) |
| Covers | 1080² + 9:16 + 16:9, fond IA **sans texte**, titre/artiste/badge en post |
| Livraison | 2 clips + MP3 + covers + prompt à jour + commandes Termux (HASH après push) |

## 7. Pipeline technique (déjà préparé)

- FFmpeg via wheel `imageio-ffmpeg` (aucun binaire dans le dépôt), Python 3.11 + Pillow + numpy.
- Ratio : les fonds IA arrivent en **768×1376** (portrait) et **1376×768** (paysage) —
  0,8 % d'écart avec le 9:16 → recadrage centré de 11 px après mise à l'échelle, absorbe par le canvas Ken Burns 1,1×.
- Rendu : un flux unique `ceil(TOTAL×FPS)` frames, `TOTAL = cold-open + 199,99 + 5 s`, 30 fps,
  H.264 BT.709, avance des paroles 0,03 s, fade final 3 s seulement.

## 8. Prochaine action après ta validation du style S6

Salve A (s01→s05 portrait) → planche contact → validation → Salve B → … → puis timings, rendu 9:16, 16:9, master, covers.
