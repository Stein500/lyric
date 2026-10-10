# Plan salve 2 — scene-11 → scene-19 + pochette (prochain tour)

Même ancre (visage, locks courtes, chemise de lin crème fermée jusqu'au col, chaîne à croix de laiton, pieds nus,
ruelle bleu nuit → aube), même technique « encre & feuille d'or », texte **toujours peint par le modèle** dans la
matière, jamais incrusté après coup. Blocs d'horodatage issus de `timings_source.lrc` (49 vers, 206,40 s).

| # | Fenêtre source | Verses couverts | Texte peint attendu (orthographe exacte) | Icônes / stickers | Lieu & lumière |
|---|---|---|---|---|---|
| 11 | 62,83 → 66,20 | « I seen loneliness pull up and decide to stay » | `LONELINESS PULLED UP` / `AND DECIDED TO STAY` | chaise vide + étiquette « occupé » | palier d'escalier, une ampoule nue |
| 12 | 66,20 → 69,34 | « But every time I was about to fall » | `EVERY TIME I WAS` / `ABOUT TO FALL` | flèche vers le bas + fissure | marche humide, corps en déséquilibre |
| 13 | 69,34 → 72,57 | « An invisible hand pulled me through it all » | `AN INVISIBLE HAND` / `PULLED ME THROUGH IT ALL` | main de lumière dorée, pas de bras | retour ruelle, câble doré tendu |
| 14 | 72,57 → 76,12 | « When I'm weak, He carries me » | `WHEN I'M WEAK` / `HE CARRIES ME` | deux mains sous les épaules + plume | marcheur porté dans la brume |
| 15 | 76,12 → 79,66 | « When I'm lost, He lights the way » | `WHEN I'M LOST` / `HE LIGHTS THE WAY` | rang de 5 lampadaires qui s'allument + boussole | avenue déserte, aube naissante |
| 16 | 79,66 → 87,07 | « speechless… / He's in control » | `WHEN I'M SPEECHLESS` / `HE HEARS MY SOUL` / `HE'S IN CONTROL` | oreille au trait + halo doré | plan rapproché, silence |
| 17 | 105,03 → 118,65 | miracles / guérison / larmes→sourires | `I SEEN MIRACLES` / `WHERE HOPE WAS DEAD` | germe qui sort du béton + heart recousu | cour intérieure, première lumière rasante |
| 18 | 118,65 → 139,00 | grâce / guide / refrain final | `IT AIN'T MY STRENGTH` / `IT'S HIS GRACE` | empreinte de pas + croix dorée au sol | toit-terrasse, ciel qui vire à l'ambre |
| 19 | 156,66 → 196,07 | dernier refrain + sortie | `MAHU TI TÈ GBÈ` / `GOD IS ALWAYS THERE` | colombe qui part + aube pleine + pastille `0326` | rue au lever du jour, pluie finie |
| PC | pochette carrée | hors clip | `MAHU TI TÈ GBÈ` / `DSKY` | idem ancre, cadrage 1:1 sans rogner la tête | **1080×1080** |

## Après les images, dans le même ordre que §7

1. Carte d'accueil et carte finale (incrustation PIL cette fois, textes §3 : « Regarde jusqu'à la fin… »,
   « Merci d'avoir regardé », « Commente le code **0326** ») — **aucun contact, aucun lien, aucun drapeau**.
2. Rendu 9:16 : H.264 CRF 24, AAC 256, `+faststart`, bt709 ; fenêtres clochettes = les 9 fenêtres ≥ 5 s listées
   dans `ANCRE.md` §1 (sauf 0→9,33 qui est la carte d'accueil).
3. Master audio : `_master_noart.mp3` déjà produit (48 kHz, 320 kb/s, **−14 LUFS mesurés, TP −1,5 dBTP,
   crête −1,24 dB**, écrêtage +0,06 dBTP de la source corrigé) → ajouter `-vn` pour tuer la pochette 360×360
   héritée, puis ID3 `TIT2` / `TPE1` / `TALB` + `APIC` 1080 + `USLT` propre.
4. Contrôles : durée décodée du clip, `blackdetect`, `freezedetect`, texte complet, badge unique, clochettes.
5. `livrables/LIVRAISON_mahu_ti_te_gbe.md` : Titre · Captions · Hashtags · déclaration IA · commandes Termux.
6. `PROMPT_UNIVERSEL_v5.8_MAHU_TYPO_PEINTE.md` : la règle « typo peinte + icônes/stickers par le modèle,
   plus de sous-titrage incrusté », la grille de zones sûres pour texte peint, et le § ancre annulant explicitement
   les points 11→13 de `Instructions A.txt`.
