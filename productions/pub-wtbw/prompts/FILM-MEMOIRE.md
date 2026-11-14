# PROMPT 2 / 6 — FILM « MÉMOIRE » · 9:16 · 24 s

> Prompt autonome. Ton le plus délicat de la série : hommage à un défunt.
> Tout ce qui est nécessaire est ici.

---

## 1. Mission
Produire un film vertical de **24 secondes** pour **DSKY WTBW** (C. Jésutondji Samuel Stein,
auteur-compositeur béninois, 34 morceaux) qui vend le service **chanson d'hommage / mémoire**.

Public : familles en deuil ou en souvenir (funérailles, anniversaire de décès, commémoration),
Bénin et diaspora. Promesse : une chanson qui garde le nom, la date et l'histoire — sans jamais
imiter la voix du disparu ni inventer son visage.

## 2. Règles absolues (non négociables)
1. **Aucune voix imitée, aucun deepfake, aucune image de visage inventé.** La chanson est chantée
   par Stein, avec les mots de la famille.
2. Photos : uniquement des cadrages qui ne permettent pas d'identifier (mains, dos, objet, cadre).
3. Aucun ressort de peur, aucune urgence commerciale. Le CTA est une phrase, pas un prix.

## 3. Spécifications du livrable
| Élément | Valeur |
|---|---|
| Format | 1080 × 1920, H.264 yuv420p bt709, 30 fps |
| Durée | 24,00 s (7 cartes × 3,43 s, fondu enchaîné 0,34 s) |
| Son | AAC 192 kbps, **−13,9 LUFS**, crête ≤ −1,5 dBFS |
| Registre | noir et blanc pur (pas de duotone), grain σ 0,006, push-in très lent 1,015 → 1,055 |
| Typographie | Playfair Display romain + italique, pose centrée basse (y ≈ 0,44 H) |

## 4. Découpage carte par carte
| # | Visuel | Titre | Micro-ligne |
|---|---|---|---|
| 1 | cadre photo, bougie, fleurs blanches | **ON NE CHOISIT PAS SA MÉMOIRE** / *ON CHOISIT SA CHANSON.* | MÉMOIRE |
| 2 | deux mains d'âgés tenant une photo | **CE QUE LES PHOTOS NE DISENT PAS,** / *LA CHANSON LE CHANTE.* | DSKY · WTBW |
| 3 | album de famille ouvert, doigts | **SON NOM. SA DATE.** / *SON HISTOIRE.* | RIEN D'INVENTÉ. TOUT DE LUI. |
| 4 | chorale de dos dans une église | **CE QUI RESTE QUAND** / *LA LUMIÈRE S'ÉTEINT.* | LA VOIX, LES MOTS, LE NOM |
| 5 | charbon | **PAS DE VOIX IMITÉE.** / *PAS DE VISAGE INVENTÉ.* | DES MOTS. RIEN D'AUTRE. |
| 6 | charbon | **UNE CHANSON POUR** / *CEUX QUI RESTENT.* | POUR CEUX QUI RESTENT |
| 7 | charbon | **DIS-MOI SON NOM.** / *JE T'ÉCRIS SA CHANSON.* | TIKTOK & YOUTUBE — @DSKYWTBW |

## 5. Musique (audio de l'artiste uniquement)
Extraits graves, prière, jamais de morceau de fête — 6,5 s chacun, fondu 0,6 s, −14 LUFS :
1. **Mahu ti tè gbè** (« Dieu est toujours là ») — 0:17,2
2. **Entre tes mains** (la prière) — 0:05,1
3. **Calm in off down** — 0:20,0
4. **Le goût bon de la vie** (fin, lumière) — 0:10,0

## 6. Commande de régénération
```bash
python3 build_bed.py --memoire     # → cache/bed_memoire.m4a (24,2 s)
python3 film_service.py memoire    # → livrables/FILM-MEMOIRE-9x16.mp4
```

## 7. Contrôles avant livraison
- durée 24,00 s, −13,9 LUFS, crête −1,5 ;
- vérifier qu'aucune carte ne montre un visage lisible ;
- le carton 5 (« pas de voix imitée ») doit rester à l'écran ≥ 3 s : c'est l'argument de confiance ;
- envoi : jamais en publicité froide, toujours en réponse à une demande de devis.
