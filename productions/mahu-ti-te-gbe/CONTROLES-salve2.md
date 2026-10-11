# Contrôles — salve 2 (scene-11 → 19) + pochette + vers peints (v-*)

## Salve 2 — blocs (19 plans) : orthographe et zones sûres

| # | Fichier | Texte peint | Ortho. | Zones | Visage | Stickers obtenus | Verdict |
|---|---|---|---|---|---|---|---|
| 11 | `scene-11.png` | `LONELINESS PULLED UP` / `AND DECIDED TO STAY` | **OK** | OK | entier | `OCCUPÉ` sur l'étiquette, cercle d'or autour de l'ampoule, étoile | validé |
| 12 | `scene-12.png` | `EVERY TIME I WAS` / `ABOUT TO FALL` (FALL penché, crème) | **OK** | OK | entier | flèche vers le bas, fissure en or, traits de glissade | validé |
| 13 | `scene-13.png` | `AN INVISIBLE HAND` / `PULLED ME THROUGH IT ALL` | **OK** | OK | entier | bobine de corde, flèche courbe, étincelles | validé |
| 14 | `scene-14.png` | `WHEN I'M WEAK` / `HE CARRIES ME` | **OK** | OK | entier, yeux clos | deux mains de lumière, plume, 3 points | validé |
| 15 | `scene-15.png` | `WHEN I'M LOST` / `HE LIGHTS THE WAY` | **OK** | OK | entier | boussole, 5 étoiles numérotées 1→5, ligne d'horizon | validé |
| 16 | `scene-16.png` | `WHEN I'M SPEECHLESS` / `HE HEARS MY SOUL` / `HE'S IN CONTROL` | **OK** | **limite basse** (3ᵉ ligne ≈ y 1560/1920, sous la borne 1574 de justesse) | profil entier | oreille dans ondes, bulle barrée, piquage de points | validé avec note |
| 17 | `scene-17.png` | `I SEEN MIRACLES` / `WHERE HOPE WAS DEAD` | **OK** | OK | entier | cœur recousu d'or, feuilles sur le M, flèche | validé |
| 18 | `scene-18.png` | `IT AIN'T MY STRENGTH` / `IT'S HIS GRACE` | **OK** | **limite haute** (bloc à y ≈ 150 → dans la bande interdite 0→144 par 6 px) | de trois quarts, entier | croix d'or au sol, pastille « 3 », empreintes 1-2-3 | validé avec note |
| 19 | `scene-19.png` | `MAHU TI TÈ GBÈ` / `GOD IS ALWAYS THERE` | **OK** (graves respectées) | OK | entier, **1ᵉʳ sourire de l'arc** | pastille `0326` décollée, colombe, soleil rayonnant | validé |
| PC | `livrables/pochette-brute.png` | `MAHU TI TÈ GBÈ` / `DSKY` / `Wolof TechStein beat wê !` | **OK** | 1:1, tête non rognée | entier | colombe, pastille `0326`, liseré d'or ouvert aux coins | validée |

Dérivés produits sans toucher à l'image : `cover-1080.jpg` (1080×1080, JPG 92), `cover-1080.png`,
`cover-916.jpg` (1080×1920, ancrage haut → **jamais de rognage du crâne**), `carte-accueil.jpg`, `carte-finale.jpg`
(PIL + **Montserrat** ExtraBold/SemiBold, récupérées du dépôt amont `JulietaUla/Montserrat`, pas de DejaVu).

## Vers peints — salve 3 (9 plans)

| Fichier | t (s) | Texte peint | Ortho. | Verdict |
|---|---|---|---|---|
| `v-38-50.png` | 38,50 (repris à 97,52 et 166,97) | `MAHU TI TÈ GBÈ` / `HE HEARS ME EVERY NIGHT` | **OK** | validé |
| `v-52-37.png` | 52,37 | `I DOUBTED` / `I ALMOST GAVE UP THE FIGHT` | **OK** | validé |
| `v-108-32.png` | 108,32 | `I SEEN HEALING` / `WHERE THE PAIN HAD SPREAD` | **OK** | validé |
| `v-111-58.png` | 111,58 | `I SEEN TEARS TURN` / `TO SMILES OVERNIGHT` | **OK** | validé |
| `v-115-59.png` | 115,59 | `BROKEN HEARTS` / `LEARN TO SHINE SO BRIGHT` | **OK** | validé |
| `v-121-70.png` | 121,70 | `EVERY STEP I TAKE` / `HE'S THE ONE WHO GUIDES` | **OK** | validé |
| `v-123-62.png` | 123,62 | `MAHU TI TÈ GBÈ` / `RIGHT BY MY SIDE` | **OK** | validé |
| `v-142-28.png` | 142,28 | `EVEN WHEN I DON'T FEEL HIM` / `HE'S THERE` | **OK** | validé |
| `v-145-11.png` | 145,11 | `EVEN WHEN I DON'T HEAR HIM` / `HE CARES` | **OK** | validé |

**Restent à générer : 3 vers** → `v-120-11.png` (120,11 « It ain't my name, it's His face » — échec du modèle,
réponse sans image), `v-148-92.png` (148,92 « Even when my whole world falls apart »), `v-152-10.png`
(152,10 « Mahu ti tè gbè, He holds my heart »). Limite de 10 générations par tour atteinte sur ce tour.
Contact sheet de contrôle : `CONTROLE-vers1.jpg`.

## Audio — master livré et vérifié

`livrables/Mahu ti tè gbè - master 320k.mp3`, 8 570 754 o :
durée décodée **206,40 s** (= source, aucun allongement) · 48 000 Hz · **320 kb/s CBR** ·
**loudness intégrée −14,0 LUFS** (ebur128) · crête **−1,24 dB** (source à +0,06 dBTP écrêtée → corrigée) ·
pochette héritée 360×360 supprimée (`-vn`) puis remplacée · ID3 v2.4 relu : `TIT2` `TPE1` `TALB` `TPE2` `TCON=Gospel`
`TDOR=2026-10-10` · `APIC` 1080×1080 (cover front) · `USLT` fre **49 lignes**, sans horodatages ·
4 `TXXX` (SIGNATURE, PAROLES, MASTER, IA).

## Ce qui est encore ouvert (ne pas livrer comme fini)

1. 3 vers sans plan (ci-dessus) → sans eux, le clip aura 3 plans de reprise à la place.
2. Le clip 9:16 **n'est pas encore rendu** : script `render_lyric_video.py` à écrire sur `verses_map.json`
   (1 plan par vers, fondu 0,35 s, badge « Dsky » en y=160 avec un seul fondu par vers, clochettes dans les
   9 fenêtres, cartes 0→9,33 et 206,40→211,40).
3. Calage des mots : **provisoire** (durées §6), à valider à l'écoute.
4. Deux plans à la limite des zones sûres (16 bas, 18 haut) — soit on les garde, soit on les régénère avec la
   typo recentrée.
