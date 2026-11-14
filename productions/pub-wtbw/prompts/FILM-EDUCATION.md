# PROMPT 4 / 6 — FILM « ÉDUCATION / ATELIERS » · 9:16 · 20 s

> Prompt autonome. C'est le film qui différencie DSKY : personne d'autre au Bénin
> ne vend de la chanson sur mesure **et** n'apprend aux jeunes à écrire.

---

## 1. Mission
Produire un film vertical de **20 secondes** pour **DSKY WTBW** qui vend les **ateliers
d'écriture et de composition** (écoles, centres, églises, ONG, mairies, particuliers).

Public : directeurs d'école, responsables d'associations, parents. Argument : il n'apprend pas
à chanter, il apprend à écrire — et il écrit avec eux, pas pour eux.

## 2. Spécifications du livrable
| Élément | Valeur |
|---|---|
| Format | 1080 × 1920, H.264 yuv420p bt709, 30 fps |
| Durée | 20,00 s (6 cartes × 3,33 s, fondu 0,34 s) |
| Son | AAC 192 kbps, −14 LUFS, crête ≤ −1,5 dBFS |
| Série | « laiton » (#0E0B08 / #F4E7CC / #C8A16B / #F6EFE3), grain σ 0,006 |
| Interdits | visages d'enfants identifiables, ton publicitaire agressif |

## 3. Découpage
| # | Visuel | Titre | Micro-ligne |
|---|---|---|---|
| 1 | classe, enfants de dos, cahiers | **J'ÉCRIS AVEC LES JEUNES.** / *PAS POUR EUX. AVEC EUX.* | ÉDUCATION · ATELIERS D'ÉCRITURE · BÉNIN |
| 2 | main + stylo, cahier noirci | **TROUVER SES MOTS** / *AVANT DE TROUVER SA VOIX.* | ON N'ÉCRIT PAS UNE CHANSON, ON LA CHERCHE |
| 3 | studio, clavier, carnet | **ÉCRIRE.** / **COMPOSER.** / *ENREGISTRER.* | DU CAHIER AU MASTER |
| 4 | enfants qui courent, poussière | **LA SCÈNE S'APPREND** / *COMME UN REFRAIN.* | RÉPÉTER, RATER, RECOMMENCER |
| 5 | charbon | **ÉDUCATEUR · PAROLIER** / **COMPOSITEUR · PRODUCTEUR** | QUATRE MÉTIERS, UNE SEULE VOIX |
| 6 | charbon | **AMÈNE TES JEUNES.** / *JE M'OCCUPE DES MOTS.* | TIKTOK & YOUTUBE — @DSKYWTBW |

## 4. Musique (audio de l'artiste uniquement)
4 extraits de 5,4 s, fondu 0,5 s, −14 LUFS — tous thématiquement liés à l'école et au combat :
**On nous a volé notre éducation** (0:07,5) → **Nan yi a ga djin wê** (0:08,4) →
**Concentré sur le chemin** (0:11,4) → **Je me relève toujours** (0:06,0).

## 5. Commande de régénération
```bash
python3 build_bed.py --education     # → cache/bed_education.m4a (20,1 s)
python3 film_service.py education    # → livrables/FILM-EDUCATION-9x16.mp4
```

## 6. Contrôles
- durée 20,00 s, LUFS −14 ;
- carte 5 : les 4 métiers lisibles d'un seul coup d'œil (c'est le message de crédibilité) ;
- aucune image d'enfant reconnaissable (dos, silhouettes, cadrage serré sur les mains) ;
- utiliser ce film en ouverture des demandes d'intervention scolaire, pas en publicité froide.
