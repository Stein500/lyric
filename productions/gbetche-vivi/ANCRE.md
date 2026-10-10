# Gbètché vivi — Production lyrics · dossier de fabrication

Cadre appliqué : `PROMPT_UNIVERSEL_v5.7` (2026-10-10, fusion v5.5 + v5.6). Source audio : `Gbètché vivi.mp3` · paroles + horodatages : `Gbètché vivi - Bandit positif.txt` (47 vers). Mise à jour : 2026-10-10, tour 3.

## 0 — Décisions de l'artiste (dans l'ordre où elles sont tombées)

1. **Les images portrait ne doivent pas être coupées en haut ni en bas dans la vidéo** → générer des images **natives 9:16**, pas de reprise paysage recadrée. (§2)
2. **30 images** pour ce morceau, avec un ancrage proposé. (§3)
3. **Tour 2 — pivot** : « je préfère une seule personne… un homme qui me ressemble, prendre mes photos dans `Sam` et générer… personne animée dans un studio ». → **un seul héros**, inspiré du visage de l'artiste, en **rendu 3D « long-métrage d'animation »**, dans un **studio**. La salve photo « couple » (10 images) est **archivée**, non montée.
4. Autorisation d'usage du visage : **donnée explicitement par la personne concernée** (§2 v5.7 respecté). Les images de référence faciale sont extraites des deux mp4 de `Sam/` par `ffmpeg`, stockées dans `_refs/` et **volontairement hors Git** (`_refs/.gitignore`). Elles ne sont plus renvoyées au générateur après l'ancre.

## 1 — Ancrage retenu : « STUDIO POSITIF »

| Élément | Décision |
|---|---|
| Nombre de personnages | **1 seul** : l'avatar animé de l'artiste, dans tous les plans |
| Style | Rendu 3D cinématique de long-métrage d'animation, proportions réalistes, peau subsurface, tissu mat ; **pas** de caricature, pas de nez exagéré, pas de plastique luisant |
| Lieu | Studio (cyclorama gris chaud, béton ciré, néons teal, spot doré, brume légère) |
| Palette | Or / ambre + teal-indigo, accent rouge sobre |
| Tenue (bloc héros, à recopier mot pour mot) | Chemise col mandarin tie-dye indigo et bleu-gris à manches noires, **fermée jusqu'en haut** ; pantalon noir droit ; baskets blanches ; montre sombre au poignet gauche ; lunettes rectangulaires à monture fine sombre ; cheveux très courts |
| Visage | Jeune homme noir, visage rond-ovale, peau brune chaude, barbe naissante, expression calme, digne, souriante |
| Énergie | Tête haute, épaules relâchées, mains ouvertes ; aucun geste d'intimidation, aucune arme, aucun argent étalé, aucune deuxième personne au premier plan |
| Interdits | nudité, cadrage sur le corps, membre coupé, texte/lettre/logo/drapeau/filigrane/emoji, bande noire, bordure parasite |

Ancre validée par l'artiste (choix 2 sur 2) : `personnages/ancre-anim-01.png` — **toute génération repart de ce fichier via `images=`**.

## 2 — Règle « portrait jamais coupé » (la demande n°1)

1. Images générées **en 9:16 vertical natif**, jamais de conversion paysage → portrait.
2. Chaque prompt impose : tête entièrement visible avec **≥ 10 % d'air au-dessus**, corps complet jusqu'aux chaussures, mains non coupées, rien d'important dans les 8 % supérieurs (zone badge) ni les 18 % inférieurs (zone CTA/crédits).
3. Rendu : **`scale=1080:1920:flags=lanczos` seul** — jamais `force_original_aspect_ratio=increase` + `crop`, jamais de `pad`. Sortie mesurée 768×1376 (ratio 0,5581 pour 0,5625 visé) → **étirement vertical de 0,8 %** absorbé à la place d'une coupe de 8 px : imperceptible, aucune information perdue.
4. Contrôle de sortie : aucune frame où un crâne ou des chaussures touchent les bords haut/bas ; vérifié par `qa_fonds.py` (§7).

## 3 — Plan des 30 fonds studio (segments calés sur les débuts de vers)

Durée **décodée mesurée : 194,83 s** (start offset 0,023 s) — le `[length:03:14]` du fichier texte est un arrondi. Découpe en 30 segments par programmation dynamique : moyenne **6,30 s**, **aucune coupe d'image en milieu de vers**, minimum 2,57 s, maximum 15,07 s. Table de travail : `plan_fonds.tsv`.

| # | t0 → t1 | s | Scène studio — homme seul, personnage animé, 9:16 natif non rogné | État |
|---|---|---|---|---|
| A01 | 5,87 → 11,94 | 6,07 | Présentation : debout au micro, main sur la poitrine | généré |
| A02 | 11,94 → 17,49 | 5,55 | Gratitude : assis sur le tabouret, mains jointes | généré |
| A03 | 17,49 → 24,19 | 6,70 | Bénédiction : bras ouverts, paumes vers le haut, halo doré | généré |
| A04 | 24,19 → 27,36 | 3,17 | Paix : mains jointes devant la bouche, yeux fermés | généré |
| A05 | 27,36 → 41,60 | 14,24 | Marche sans chaîne : couloir de studio, chaîne au sol (fenêtre clochettes) | généré |
| A06 | 41,60 → 45,45 | 3,85 | La cabine : casque devant la vitre acoustique — 2ᵉ personne en fond à retirer | **régénérer** |
| A07 | 45,45 → 52,32 | 6,87 | Rire : tête renversée, micro détendu | généré |
| A08 | 52,32 → 55,97 | 3,65 | Bandit positif : index à la tempe — liseré clair + tête trop haute | **régénérer** |
| A09 | 55,97 → 59,36 | 3,39 | Plan large assis au sol béton, spot unique | **à générer** |
| A10 | 59,36 → 64,70 | 5,34 | Il ajuste ses lunettes, sourire tranquille, fond teal | **à générer** |
| A11 | 64,70 → 70,93 | 6,23 | Main posée sur un caisson de monitoring, menton haut | **à générer** |
| A12 | 70,93 → 75,00 | 4,07 | Plan serré visage, lumière dorée rasante | **à générer** |
| A13 | 75,00 → 81,82 | 6,82 | Il écrit dans un carnet au banc de mixage | **à générer** |
| A14 | 81,82 → 88,26 | 6,44 | Poing serré vers la caméra — Nonvi, parole tenue | **à générer** |
| A15 | 88,26 → 91,50 | 3,24 | Partage un verre d'eau, studio vide autour de lui | **à générer** |
| A16 | 91,50 → 106,57 | 15,07 | La cabine s'ouvre, équipe en silhouette qui lève les bras (fenêtre clochettes) | **à générer** |
| A17 | 106,57 → 112,45 | 5,88 | Toast au studio : verre levé, un seul personnage visible | **à générer** |
| A18 | 112,45 → 118,07 | 5,62 | Cri de ralliement : poings levés dans la brume | **à générer** |
| A19 | 118,07 → 124,51 | 6,44 | Danse douce sur place, épaules, sourire | **à générer** |
| A20 | 124,51 → 128,58 | 4,07 | Contre-jour total, silhouette dorée, visage lisible | **à générer** |
| A21 | 128,58 → 135,62 | 7,04 | Marche latérale devant le cyclorama, plan large | à planifier |
| A22 | 135,62 → 139,12 | 3,50 | Derrière la baie vitrée, deux mains ouvertes | à planifier |
| A23 | 139,12 → 146,00 | 6,88 | Épaule contre une silhouette floue, regard ferme | à planifier |
| A24 | 146,00 → 149,52 | 3,52 | Dagbé : il règle un casque, manches retroussées | à planifier |
| A25 | 149,52 → 156,01 | 6,49 | Avance en ligne, trois silhouettes lointaines dans le couloir | à planifier |
| A26 | 156,01 → 162,75 | 6,74 | Libération : fumée, néons, bras ouverts | à planifier |
| A27 | 162,75 → 170,09 | 7,34 | Béni, en paix : assis au bord du cyclorama, lumière d'aube | à planifier |
| A28 | 170,09 → 181,17 | 11,08 | Vue de dessus : minuscule au centre du studio vide (fenêtre clochettes) | à planifier |
| A29 | 181,17 → 183,74 | 2,57 | Trois visages de front, lui au centre, calme | à planifier |
| A30 | 183,74 → 194,83 | 11,09 | Face caméra, main sur le cœur, lumière d'or → fond de la carte finale | à planifier |

**Fenêtres sans texte ≥ 5 s** (clochettes, calculées avec la durée d'affichage v5.7, à confirmer à l'écoute) : 30,24 → 41,60 · 94,38 → 106,57 · 173,11 → 181,17. La fenêtre 186,27 → 194,83 est tenue par **la carte finale**, pas par les clochettes.

## 4 — Carte d'accueil, carte finale, code

- **Accueil ~5 s** sur A01 : « Regarde jusqu'à la fin » puis « pour découvrir comment proposer un son ou des lyrics à réaliser pour toi ! » (≈ 4 mots/s, fondu 0,35 s, pas de coupe au milieu d'un vers).
- **Finale 5 s** après la chanson, sur A30 : « Merci d'avoir regardé » · « Tu veux un son ou des lyrics à réaliser pour toi ? » · « Commente le code » · code en grand.
- **Code proposé : `0314`** (la durée du morceau, 03:14 — facile à retenir, propre à cette chanson). Alternatives : `1414`, `3030` (trois mots-clés — Wanyiyi, Nonvi, Dagbé — une seule victoire). **En attente du choix de l'artiste.**
- Badge **« Dsky » seul, sans drapeau**, y = 160, opacité ≤ 75 %, fondu 0,4 s par vers. Paroles centrées sur H/2, largeur sûre ≤ 740 px, mot actif or / mots passés crème, vague 4,5 px à 0,9 Hz ; effacement fondu 0,35 s pendant les clochettes.

## 5 — Audio et master (mesuré, pas supposé)

- Fichier source lu : **194,83 s décodées**, 48 kHz stéréo, 182 kb/s.
- **−14,8 LUFS intégrés**, crête **−0,0 dBFS** → master à repasser en loudnorm **deux passes** (−14 LUFS / −1,5 dBTP), sinon la crête est hors marge.
- MP3 320 kb/s 48 kHz, ID3v2.4 avec APIC (cover) + USLT (paroles propres, sans le caractère `‎` U+200E présent dans le fichier texte).
- Tempo non encore attaqué : le calage mot-à-mot au nombre de caractères reste **provisoire** et doit être signalé à la livraison.

## 6 — Livrables dus (§7 v5.7)

9:16 1080×1920 · titre · captions (légende courte + code) · 10 à 13 hashtags · déclaration IA (visuels 3D générés) · commandes Termux une ligne par fichier, `;` en séparateur, sur le hash du commit **après** push. Titre proposé : « Gbètché vivi — Dsky ».

## 7 — Contrôles de la salve anim (script `qa_fonds.py`, mesures réelles)

Commande : `/home/user/venv/bin/python productions/gbetche-vivi/qa_fonds.py 'anim-*'` (sortie = tableau + planche de validation).

| Fichier | Ratio | Bandes noires h/b | Air au-dessus du crâne | Verdict |
|---|---|---|---|---|
| `ancre-anim-01` | 0,5581 | 0 / 0 px | 11,0 % | OK (guide d'identité, hors montage) |
| `anim-01` | 0,5581 | 0 / 0 | 11,0 % | OK |
| `anim-02` | 0,5581 | 0 / 0 | 11,6 % | OK |
| `anim-03` | 0,5581 | 0 / 0 | 11,4 % | OK |
| `anim-04` | 0,5581 | 0 / 0 | 11,2 % | OK |
| `anim-05` | 0,5581 | 0 / 0 | 0,0 % → **faux positif** | crâne en réalité vers 38 % : le crible accroche les néons du plafond. OK |
| `anim-06` | 0,5581 | 0 / 0 | 10,8 % | **à régénérer** : un 2ᵉ personnage (l'engineer) apparaît au fond, l'artiste veut un homme seul |
| `anim-07` | 0,5581 | 0 / 0 | 11,8 % | OK |
| `anim-08` | 0,5581 | 0 / 0 | **2,5 %** | **à régénérer** : tête dans la zone badge (y 0→144) + trait clair vertical à ~4 % du bord (cadre parasite visible à la planche) |

- **Zéro bande noire** sur les 9 fichiers et ratio 9:16 au dixième de pour cent : le montage applique un `scale` pur — testé sur `anim-05` → sortie **1080×1920 exacte, rien de rogné en haut ni en bas**. C'est le contrôle que l'artiste avait demandé.
- Le crible « liseré clair » automatique est **peu fiable sur ce décor** (fond de studio déjà lumineux : seuil 140 → tout déclenche, seuil 150 + 45 % de couverture → rien). Il reste **informatif** ; le trait de cadre de A08 est relevé à la planche et sera confirmé au montage par `cropdetect`.
- Zones basses (y ≥ 1574) : chaussures, tabouret, chaîne au sol y figurent — voulu : cette zone interdit le **texte**, pas le décor.
- Tenue constante vérifiée à la planche `PLANCHE-anim-all.jpg` (ancre + A01→A08) : même visage, mêmes lunettes, même chemise tie-dye, même pantalon/baskets sur les 8 scènes.

## 8 — Archive : salve photo « MIDI POSITIF » (couple, 10 images)

Générée avant le pivot, **non montée**. Contrôle de l'époque : `ancre-01.png` présentait **109 px de noir en haut (8,5 %)** → réparé (bande retirée, puis 61 px rognés sur chaque côté, densité de contours des lisères 4,4 contre 6,9 au centre : du fond uniquement, aucun personnage touché) ; l'original est conservé en `ancre-01-brut.png`. Les 10 scènes (`scene-01…10`) sont propres (aucune bande noire, 768×1376). **Ces images ne se reportent jamais sur un autre morceau sans nouvelle validation de l'artiste.**

## 9 — Prochain tour (ordre)

1. Régénérer **A06** (homme seul, sans engineer) et **A08** (tête descendue sous la zone badge, sans trait de cadre).
2. Produire **A09 → A18** (quota 10 générations/tour), chacune repartant de `ancre-anim-01.png`.
3. Puis **A19 → A30**, planche complète, validation de l'artiste.
4. Montage 9:16 (`scale` pur, jamais de `crop`), cartes d'accueil/finale, clochettes premium sur les 3 fenêtres, contrôles `blackdetect` / `freezedetect`, master et covers, livraison (titre, captions, hashtags, déclaration IA, code **0314** à valider).
5. Commit + push après chaque étape, sur `arena/f0df3f2f-lyric` uniquement.
