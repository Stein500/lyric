# PUB — DSKY · WTBW

Publicité courte de marque et de services (fêtes, célébration, mémoire, anniversaire),
plus l'identité visuelle **DSKY · WTBW**.

> Aucune photo d'Imelda n'est utilisée ici. Ce n'est pas un hommage, c'est une pub.

## Livrables

| Fichier | Quoi | Durée / format |
|---|---|---|
| `livrables/PUB-WTBW-CATALOGUE-9x16.mp4` | le film complet, 20 cartons, 34 titres cités | 28,87 s · 1080×1920 · 30 i/s · −13,9 LUFS |
| `livrables/PUB-WTBW-BUMPER-5s-9x16.mp4` | version ultra-courte, signature → morceau → promesse | 5,00 s · 1080×1920 · −16,2 LUFS |
| `livrables/FILM-CITATIONS-9x16.mp4` | film citations, 8 cartons, lit musical du catalogue | 20,40 s · −14,2 LUFS |
| `livrables/FILM-SERVICES-9x16.mp4` | film services (mariage, anniversaire, hommage, clip) | 13,00 s · −13,0 LUFS |
| `livrables/brand/BRAND-01…10` | planche identité + 9 mises en situation merch | 1080×1350 |
| `livrables/universel/UNI-01…10` | salve « universel » : citations, mains, silhouettes, services | 1080×1350 |
| `livrables/brand/print/` | fichiers imprimeur (PNG transparents 2400 px + SVG) | vectoriel / 300 dpi |

## Prompts

| Fichier | À quoi ça sert |
|---|---|
| `PROMPT-MAITRE.md` | le prompt A→Z : l'IA **t'interroge** (couleur, effet, rythme…), tu valides, elle produit. Tu ne livres que tes photos/vidéos. |
| `PROMPT-PUB-5-30s.md` | la pub : 15 s, 30 s, et le couplet catalogue de 60 s qui cite les 34 morceaux |
| `PROMPT-MARQUE.md` | la marque : géométrie du sigle, lettrage, règles merch, fichiers d'impression |

## Fabrication (reproductible)

```bash
pip3 install --break-system-packages numpy pillow scipy imageio-ffmpeg

python3 build_pub_audio.py     # 20 refrains de 1,5 s → cache/pub.m4a (28,86 s, −13,9 LUFS)
python3 pub_video.py           # le film 9:16
python3 pub_video.py --bumper  # la version 5 s
python3 brand_kit.py           # les 10 visuels de marque + fichiers d'impression
python3 logo.py                # exporte les 4 déclinaisons du logo (PNG + SVG)
python3 universel.py           # la salve universelle (10 visuels)
python3 build_bed.py           # lit musical calme 21 s du catalogue
python3 film_uni.py            # film CITATIONS 20 s
python3 film_uni.py --services # film SERVICES 13 s
```

`pub_video.py --stills 3.2,12.0` sort des images fixes pour contrôler la typo avant de rendre.
`assets/` contient les mockups vierges générés par IA ; **les lettres ne sont jamais générées par IA**,
elles sont posées par `brand_kit.py` à partir du sigle vectoriel et des polices d'`engine.py`.

## La marque — trois déclinaisons

| Variante | Usage | Fichier |
|---|---|---|
| **stack** sigle + DSKY + WTBW + baseline | affiche, t-shirt, sweat, tote | `print/DSKY-WTBW-lockup-*-2400px.png` |
| **type** DSKY / WTBW énormes | mode, sac de luxe, vinyle, couverture | `print/DSKY-WTBW-lettrage-blanc-2400px.png` |
| **badge** rond, texte courbé | pastille, broderie, étiquette, sticker | `print/DSKY-WTBW-badge-blanc-2000px.png` |
| **sigle** seul | 8 mm minimum, broderie, semelle | `print/DSKY-WTBW-sigle-blanc-2000px.png` + `.svg` |

Tout est généré par `logo.py` (aucune lettre dessinée par une IA) : `python3 logo.py` réexporte les fichiers d'impression.

## Le catalogue cité (34 titres)

Noukiko tché wê · Ayon dèkpè · Tu es trop belle · Monster Positive · Je me relève toujours ·
Gbètché vivi · Nan yi a ga djin wê · Concentré sur le chemin · Sanguin ·
On nous a volé notre éducation · Ça monte, ça descend · Le goût bon de la vie · Mahu ti tè gbè ·
Vivi O O R · Glace · Goinfres · Grand marcheur · Masque · Ghost u see · Nonvi konou · Yafoy ·
Le Survivant · Je suis pauvre et riche · Testostérone · Je crache les démons · Dès le début ·
Entre tes mains · Calm in off down · Drague moi · Je m'aime tellement · Seul dans ma tête ·
L'amour est la réponse · Motivé · Wolof TechStein — Essaie

## Chaîne graphique

Charbon `#0B0B0C` (jamais du noir pur : il clignote sur OLED et déclenche les détecteurs de coupure),
blanc cassé `#F2EFE9`, laiton `#C8A16B`. Serif éditorial pour les titres, sans-serif espacé pour les étiquettes.
