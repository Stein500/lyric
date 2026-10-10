# Contrôles — salve 1 (scene-01 → scene-10)

Contrôle visuel fait après génération, sur les 10 images. Grille v5.7 §7 :
orthographe du texte peint, zones sûres, visages non coupés, continuité, ancre respectée, aucun drapeau/logo/filigrane.

| # | Fichier | Horodatage source | Texte peint (attendu) | Orthographe | Zones sûres | Visage | Ancre | Verdict |
|---|---|---|---|---|---|---|---|---|
| 01 | `scene-01-ancre.png` | 9,33 → 17,24 | `MAHU TI TÈ GBÈ` + `God is always there` | **OK** (graves sur les 2 E) | OK | entier | définit l'ancre | validé |
| 02 | `scene-02.png` | tag 9,33 | `WOLOF TECHSTEIN BEAT WÊ` + `signature du producteur` | **OK** (WÊ accentué) | OK | entier, texte frôle la mâchoire | ✓ | validé |
| 03 | `scene-03.png` | 17,24 | `YEAH... MAHU TI TÈ GBÈ` + `17 s — la nuit commence` | **OK** | OK | entier | ✓ | validé |
| 04 | `scene-04.png` | 26,06 | `GOD IS ALWAYS THERE` + `une lanterne allumée suffit` | **OK** | OK | sujet très petit (plan large) | ✓ | validé |
| 05 | `scene-05.png` | 28,10 → 31,67 | `MAHU TI TÈ GBÈ` / `HE NEVER LEAVES ME BARE` + pastille `0326` | **OK**, BARE en or vif | OK | entier | ✓ | validé |
| 06 | `scene-06.png` | 35,04 | `IN THE SHADOWS` (or) / `AND THE LIGHT` (crème) | **OK** | OK | entier, texte sur la bouche → **à surveiller au montage** | ✓ | validé avec note |
| 07 | `scene-07.png` | 45,88 | `I BEEN THROUGH NIGHTS` / `where I couldn't see the light` | **OK** | OK | de profil, entier | ✓ | validé |
| 08 | `scene-08.png` | 49,49 | `I SCREAMED INTO THE VOID` / `I CRIED THROUGH THE NIGHT` (VOID crème, NIGHT or) | **OK** | OK | dos/trois quarts, bouche ouverte | ✓ | validé |
| 09 | `scene-09.png` | 56,17 | `A VOICE SAID` / `SON, I'M HERE` / `IT'S ALRIGHT` dans une bulle | **OK**, apostrophes propres | OK | de profil flou, non coupé | ✓ | validé |
| 10 | `scene-10.png` | 59,16 → 62,83 | `I SEEN DOORS CLOSE` / `I SEEN FRIENDS WALK AWAY` (AWAY en or vif) | **OK** | OK | entier | ✓ | validé |

## Icônes et stickers réellement obtenus (demande du jour)

Colombe au trait d'or (01, 04) • point d'interrogation en pastille (01, 03) • flèche peinte vers la lampe (01) •
pastille vinyle rayée + ondes sonores (02) • main ouverte (03) • lanterne + étoiles filantes + soulignement (04) •
paire d'ailes + pastille `0326` (05) • demi-lune / demi-soleil + flèche de jonction (06) • cadenas + chaîne +
étiquette arrachée + croix barrée (07) • ondes concentriques + larme + sticker **SILENCE barré** (08) •
empreinte de main en lumière + bulle de dialogue + pouce levé + gouttes (09) • numéros de porte 1→5 +
trousseau de clés + flèche courbe (10).

## Continuité vérifiée

Même visage, mêmes locks courtes, même chemise de lin crème fermée, même chaîne à croix, mêmes pieds nus dans
la flaque, même ruelle bleu nuit avec une seule source ambre. La pluie baisse d'intensité à partir du plan 09
(mur plus sec) : cohérent avec l'arc qui doit finir à l'aube.

## Réserves écrites (ne pas les cacher à la livraison)

1. `scene-02` et `scene-06` : la typo peinte touche la zone de la bouche. Ce n'est pas illisible, mais au montage
   ces deux plans doivent rester courts (≤ 3 s) pour qu'on ne cherche pas le regard.
2. Résolution native des images = **768×1376** (ratio 0,558, pas 0,5625) → un léger recadrage/upscale est
   nécessaire avant le rendu 1080×1920, **sans rognage vertical du visage** (règle « portrait non recadré »).
3. `scene-04` : sujet minuscule → le texte porte tout le plan, vérifier la lisibilité après encode H.264 CRF 24.
4. Aucun texte de ma main n'a été incrusté en post-production sur ces 10 plans : tout est peint par le modèle,
   comme demandé. Les seules incrustations restantes seront les cartes d'accueil/finale (§3).
