# PROMPT 6 / 6 — MARQUE DSKY WTBW · logo, sigle, déclinaisons imprimées

> Prompt autonome. Tout le branding : la marque, le sigle, les fichiers imprimeur,
> les applications merch. Aucune lettre n'est jamais générée par un modèle d'image.

---

## 1. Mission
Définir et produire l'identité de **DSKY WTBW** — C. Jésutondji Samuel Stein « Dsky »,
lyriciste, éducateur, compositeur, producteur, Bénin.

## 2. Ce que veut dire le nom (à ne jamais déformer)
- **DSKY** = Dsky, nom d'artiste (se prononce « Daïsky ») ;
- **WTBW** = **W**olof **T**ech**S**tein **B**eat **W**ê — le nom complet de l'artiste est donc
  déjà contenu dans le sigle : *Stein* est dans Tech**Stein** ;
- signature longue officielle : **C. JÉSUTONDJI SAMUEL STEIN** · LYRICISTE · ÉDUCATEUR · BÉNIN.

## 3. Le sigle
Cercle double (rayon 478 / 436, trait 14 / 6), un « W » tracé en polyligne
(`-245,-135 → -120,150 → 0,-55 → 120,150 → 245,-135`, trait 72, bouts arrondis),
filet horizontal sous le W, étoile à 5 branches dessous.
Lisible à 16 px comme à 20 m. Monochrome uniquement : noir, blanc, ou laiton `#C8A16B`.

## 4. Le lockup vertical
1. sigle (hauteur 60 % de la largeur du bloc) ;
2. **DSKY** en Playfair Display, interlettrage 0,125 ;
3. **WTBW** en Montserrat, interlettrage 0,32, trait +2 ;
4. filet laiton (34 %–66 % de la largeur) ;
5. baseline : `WOLOF TECHSTEIN BEAT WÊ · BÉNIN`
   **ou** variante état civil : `C. JÉSUTONDJI SAMUEL STEIN` + `LYRICISTE · ÉDUCATEUR · BÉNIN`.

## 5. Palette
| Rôle | Hex |
|---|---|
| Fond | `#0B0B0C` (charbon) / `#0E0B08` (charbon chaud) |
| Encre claire | `#F2EFE9` |
| Accent | `#C8A16B` (laiton) |
| Bénin (usage rare, jamais en fond) | `#008751` `#FCD116` `#E8112D` |

## 6. Fichiers à produire
| Fichier | Usage |
|---|---|
| `print/DSKY-WTBW-lockup-blanc-2400px.png` | transfert textile clair, flocage |
| `print/DSKY-WTBW-lockup-noir-2400px.png` | papier, carte, tampon |
| `print/DSKY-WTBW-lockup-STEIN-blanc-2400px.png` | variante avec l'état civil |
| `print/DSKY-WTBW-lockup-STEIN-noir-2400px.png` | variante avec l'état civil |
| `print/DSKY-WTBW-sigle-blanc-2000px.png` | badge, étiquette, avatar |
| `print/DSKY-WTBW-sigle.svg` | imprimeur, broderie, découpe vinyle |

Tous en **PNG transparent**, noir ou blanc pur, **sans dégradé ni ombre** : c'est ce qu'exige
un imprimeur ou une brodeuse. Le SVG est la source vectorielle du sigle.

## 7. Applications merch (règles)
- t-shirt / hoodie : lockup poitrine 9 cm, jamais plus de 2 couleurs ;
- casquette : sigle seul, broderie 6 cm ;
- tote / sac : lockup 20 cm centré ;
- sneakers / cartes / vinyle : sigle seul, laiton autorisé ;
- l'accent Bénin reste réservé à la planche identité, pas sur le textile.

## 8. Commande de régénération
```bash
python3 brand_kit.py              # planche identité + 10 applications merch
python3 -c "import brand_kit as B; print(B.print_files()); print(B.print_files_stein())"
```

## 9. Contrôles
- lisibilité du sigle à 32 px (avatar) et à 15 cm (imprimé) ;
- aucun texte courbé, aucun effet, aucune ombre dans les fichiers imprimeur ;
- les 2 variantes de baseline existent (avec et sans état civil) ;
- vérifier que DSKY et WTBW ne sont jamais séparés, ni abrégés, ni traduits.
