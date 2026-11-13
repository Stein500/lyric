# PROMPT — MARQUE & SIGNATURE « DSKY · WTBW »

Objectif : une marque **simple à reproduire**, qui tient sur un t-shirt, un sac de luxe et une chaussure, sans jamais avoir l'air d'un logo de club vidéo.

---

## ─── DÉBUT DU BLOC À COPIER ───

Tu es **designer d'identité** (niveau studio de luxe). Tu crées la marque de **DSKY · WTBW**, artiste béninois, Wolof TechStein beat wê.

### Le principe

Un **sigle géométrique** + un **lettrage**. Rien d'autre. Pas de dégradé, pas d'effet 3D, pas d'ombre portée, pas de slogan dans le logo : un logo qui se **brode** et s'**imprime au pochoir** doit rester lisible à 8 mm.

### 1. Le sigle (à construire, pas à imiter)

- Un **anneau** fin (trait = 1,4 % du diamètre) contenant un second anneau très fin à 91 % du rayon (trait 0,6 %), à 60 % d'opacité.
- Au centre, un **W** en trait épais (7,2 % du côté), joints arrondis, tracé en polyligne avec ces points (repère : centre 0,0 ; unité = côté du carré) :
  `(-0.245, -0.135) → (-0.120, 0.150) → (0.000, -0.055) → (0.120, 0.150) → (0.245, -0.135)`
- Sous le W, une **barre de mesure** horizontale de −0,150 à +0,150 en y = 0,265 (trait 0,9 %, opacité 85 %).
- Sous la barre, une **étoile à 5 branches** (rayon 0,042, ratio branches 0,42) centrée en y = 0,345.
- Le tout tient dans le cercle : rien ne touche l'anneau.

Pourquoi ça marche : à 8 mm (bouton de manchette, broderie de casquette) on lit encore **un W dans un cercle** ; à 2 m on lit une **pastille de label**.

### 2. Le lettrage

- **DSKY** — serif à empattements (Playfair Display / Bodoni), capitales, interlettrage **+16 %**, hauteur de capitale = 30 % de la largeur du bloc.
- **WTBW** — sans-serif géométrique, capitales, interlettrage **+30 %**, hauteur = 9 % du bloc, placé sous DSKY avec un blanc de 2 %.
- **Baseline** — `WOLOF TECHSTEIN BEAT WÊ · BÉNIN`, sans-serif, hauteur 7,5 % du bloc, interlettrage +20 %, alignée sur la largeur totale, **toujours ajustée pour tenir dans 86 %** de la largeur (jamais coupée).
- Bloc vertical, centré : sigle → DSKY → WTBW → baseline. C'est la version « affiche / t-shirt ».
- Version horizontale : sigle à gauche, DSKY au centre vertical, WTBW en dessous — pour les bandeaux et les sacs.

### 3. Couleurs

| Rôle | Valeur |
|---|---|
| Fond | `#0B0B0C` (charbon, jamais #000 pur) |
| Encre principale | `#F2EFE9` (blanc cassé) |
| Accent unique | `#C8A16B` (laiton) — un seul élément par visuel |
| Version claire | encre `#111111` sur `#F2EFE9` |
| Version Bénin | vert `#008751` · jaune `#FCD116` · rouge `#E8112D` — réservée à la planche identité, jamais sur le merch (elle « casse » le luxe) |

### 4. Règles d'usage (à respecter sur tous les supports)

- **Zone de respiration** : autour du bloc, un vide égal à 25 % de sa largeur. Rien n'entre dedans.
- **Taille minimum** : sigle seul 8 mm ; bloc complet 25 mm de large à l'impression.
- **Une seule encre** par support. Pas de logo en dégradé, pas de logo sur photo détaillée : on le pose sur une zone calme, ou sur un cartouche charbon.
- **Broderie** : le sigle seul (les anneaux fins disparaissent en dessous de 20 mm).
- **Chaussures** : sigle seul, 12 mm, sur le quartier extérieur, ou lettrage `DSKY` sur la semelle.
- **Sac de luxe** : lettrage seul en marquage à chaud, 35 mm, centré, + une petite étiquette sigle à l'intérieur.
- Jamais d'italique, jamais d'ombre, jamais de contour sur le lettrage.

### 5. Le prompt pour générer les mises en situation (mockups)

Pour chaque support, demande :

> Photographie produit **noir et blanc**, studio, 4:5, **[SUPPORT : t-shirt noir épais à plat / casquette noire trois-quarts / sac cabas toile naturelle debout / baskets blanches en cuir vues de côté / sac week-end cuir noir / planche de stickers vierges / carte de visite noire mate en relief / pochette vinyle noire]**, fond charbon sans raccord, lumière douce directionnelle haut-gauche, texture de matière visible, **surface entièrement vierge, sans aucun texte, sans logo, sans lettre, sans graphisme**, grain fin, esthétique campagne de mode.

Puis tu poses la marque par-dessus **toi-même**, à l'échelle et à l'endroit exacts (voir §4). Tu ne laisses jamais l'IA dessiner les lettres : elle les rate.

### 6. Ce qui est déjà produit

Dossier `livrables/brand/` :

- `BRAND-01-LOGO` → planche identité (sigle + lettrage + drapeau)
- `BRAND-02` à `BRAND-10` → t-shirt, sweat, tote, casquette, baskets, sac cuir, stickers, cartes, vinyle
- `print/DSKY-WTBW-lockup-blanc-2400px.png` → **fond transparent, pour l'imprimeur**
- `print/DSKY-WTBW-lockup-noir-2400px.png` → version encre noire
- `print/DSKY-WTBW-sigle-blanc-2000px.png` → sigle seul
- `print/DSKY-WTBW-sigle.svg` → **vectoriel**, pour la broderie et la découpe

### 7. Contrôle

- [ ] le sigle reste lisible à 8 mm
- [ ] la baseline ne touche jamais le bord
- [ ] une seule encre par support
- [ ] aucune lettre générée par IA sur le merch
- [ ] le drapeau Bénin n'apparaît que sur la planche identité

## ─── FIN DU BLOC À COPIER ───
