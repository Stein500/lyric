> **Rendus disponibles :** clip complet, teaser provisoire et cover dans `livraison/`. Contrôles et réserves réels : `livraison/CONTROLES-ET-LIMITES.md`. Teaser et synchronisation non validés à l’écoute ; les états antérieurs ci-dessous sont historiques.

> **Mise à jour de continuation :** les plans 36, 37, 38 et 46 ont été générés puis lettrés. Carte régénérée : **46/46 vers disponibles**, 30 images distinctes cuites et 9 variantes d’aube. La planche de contact a été régénérée et examinée globalement ; la vérification détaillée des quatre nouveaux textes à 1:1 et sur vidéo reste à faire. Aucun MP4 n’a été rendu. L’extrait `controles/extrait-teaser-a-valider.flac` est une copie décodée sans perte de la sélection 155,96–170,96 s, destinée à l’écoute ; il ne prouve pas que les coupes sont bonnes. Les indications plus anciennes ci-dessous décrivent les étapes précédentes.

# FICHE DE PRODUCTION — « Grand Marcheur »

> Branche `arena/2334b1fe-lyric` · 2026-11-15 · référence : **PROMPT UNIVERSEL v7.0** (fourni dans la conversation ; pas encore enregistré comme fichier du dépôt).
> États distingués : **validé / proposé / généré / sélectionné / rendu / contrôlé / livré**.
> À ce stade : **aucune vidéo rendue, aucun contrôle technique final, aucune livraison**.

## Bloc §2 — fiche remplie

```text
TITRE EXACT              : Grand Marcheur — tag ID3 TIT2 du maître (SOURCE, pas validation explicite) ;
                           1er message « grand marcheurs » → ÉCART SIGNALÉ, bascule sur un mot
ARTISTE À L'ÉCRAN        : DSKY WTBW — VALIDÉ (orthographe et capitales exactes)
LANGUES                  : français + signature « Wolof TechStein beat wê » (prononcée, non affichée)
PAROLES ET HORODATAGES   : Grand marcheur.txt (46 vers, [00:01.34] → [03:30.63], + [length:03:40] non-vers)
                           + tag USLT du MP3 (sections)
AUDIO MAÎTRE             : Grand marcheur 2.mp3 (5 074 732 octets) — source conservée, non modifiée
PAROLES AFFICHÉES        : exactes, SAUF exception WTBW DÉCIDÉE : vers 1, 9, 24, 43, 44 → « WTBW »
MODE                     : PEINT — VALIDÉ
PEINTURE                 : MOTEUR — défaut §0, artiste ayant délégué le choix. NO TEXT AT ALL à la
                           génération, puis vers exact cuit dans l'image par le moteur.
COULEUR                  : COULEUR / « Multi » ; palette unique VITRAIL GOSPEL de l'ancre, imposée
                           par la cohérence §5, NON notée « validée par l'artiste »
STYLE                    : identité gospel — VALIDÉE ; anime seinen, encre, arc nuit → premières lueurs → aube
PERSONNAGE / ANCRE       : assets/ancre/ancre-gospel.jpg (option 1/2) ; « On continue » = accord, pas contrôle technique
INTRO / OUTRO            : intro 0 → premier vers, sans déplacer l'horodatage ; outro 5,00 s « MERCI · WTBW »
FILET                    : OUI — VALIDÉ (zone sûre, jamais sur un mot)
BANDEAU DÉFILANT         : OUI — VALIDÉ ; messages courts discrets, texte exact provisoire
STICKERS / CTA           : non demandés → NON PRODUITS
TEASER                   : 15,00 s / 450 frames ; extrait EN ATTENTE DE VALIDATION (voir § Teaser)
VERSIONS                 : deux vidéos (clip complet + teaser) — VALIDÉ ; couverture NON PRODUITE
DOSSIER                  : productions/grand-marcheur/ (slug provisoire)
```

## Exceptions et décisions consignées

| Décision | Traitement |
|---|---|
| « WTBW partout » | 5 vers affichent « WTBW » ; `texte_source` et audio intacts. Habillage « WTBW » uniquement, badge `DSKY WTBW` ↔ `WTBW`. |
| « Choisi le mode peint… le mieux » | Défaut §0 **moteur**, dit explicitement. |
| « 10 images par Salve » | **Exception au §5 (8 max)**, consignée selon §1. |
| « Filet + bandeaux oui », « deux vidéos » | Validés ; pas de couverture. |
| « C'est tout » | Les valeurs non répondues sont **déclarées**, jamais présentées comme validées. |

## État des salves (relevé réel)

| Salve | Demandées | Générées | Échecs | État |
|---|---:|---:|---:|---|
| 01 | 10 | 10 | 3 détectés puis **régénérés + contrôlés conformes** | **10/10** |
| 02 | 10 | 10 | 0 | **10/10** (`plan-12…18` + `plan-19, 25, 26`) |
| 03 | 10 | 6 | **`plan-36` : échec de génération** | **6/10** |

- **Limite de 10 générations d'images par tour atteinte** ce tour : `plan-36` n'a **pas** pu être relancé. Ce n'est **pas un fichier livré** (§5).
- **4 vers distincts restent sans image** : i = **36, 37, 38, 46** (`plan-36`, `plan-37`, `plan-38`, `plan-46`), reportés au prochain tour.
- Les 9 nouveaux plans (`19, 25, 26, 27, 28, 29, 30, 31, 32`) ont été contrôlés : visage visible, un seul personnage au premier plan, aube lumineuse, aucun texte/logo/drapeau/QR généré. `plan-25` et `plan-26` suggèrent les « frères » par des pierres et des empreintes, **sans personnage supplémentaire**.

## Images cuites par le moteur

- **26 plans cuits** (`assets/cuits/plan-XX.jpg`) + **9 variantes d'aube cuites** (`assets/aube/cuits/aube-plan-XX.jpg`) = **35 images finales**.
- `disponible = 42/46` = 26 vers distincts + 16 reprises (dont 10 pointent vers une variante d'aube).
- **Encodage déclaré** : JPEG **qualité 96, `subsampling=0` (4:4:4)**, aucun sous-échantillonnage de la chrominance, lettres nettes. Dossier de production : **36 Mo**.
- Police réellement utilisée : **DejaVuSans-Bold** (`Montserrat-Bold.ttf` absent du dépôt) — déclaré, non validé.
- Lettrage : contour par dilatation `MaxFilter(7)` **derrière** les glyphes (contre-formes ouvertes), halo serré, glyphes espacés et tournés ±1,5°, lignes équilibrées par programmation dynamique. **Correctif 2026-11-15** : apostrophes/points/virgules rendus solidaires après un zoom 1:1 qui avait révélé « J 'suis », « d 'en » → **correction complète, 17 plans recuits, nouveau contrôle**. Aucune retouche manuelle.
- Chiffres réels (`lettering_report.json`) : largeur **263 → 490 px** (limite 500, §4 = 526 px natif), bande **y 535 → 859** (cible 441–953, sous le visage 398), aucun débordement.
- `plan-01` et `plan-09` portent **« WTBW »** ; l'audio, lui, prononce toujours le développement.

## Variantes d'aube (§3) — compromis déclaré

Les 10 reprises après le **passage à l'aube (i = 25)** utilisent 9 variantes : fond du plan d'origine **réétalonné par le moteur** (lumière ambre, luminosité ×1,34, mélange chaud 24 %) puis **vers exact recuit** dessus par `lettering.cook()`. **Aucune nouvelle génération IA** (budget du tour épuisé) : c'est un compromis, pas une validation d'images dédiées. Des images IA dédiées peuvent être produites si tu le demandes.
- Mapping : i=33→`aube-plan-18`, 34→`19`, 35→`16`, 39/41→`05`, 40→`06`, 42→`08`, 43→`09`, 44→`01`, 45→`03`.
- **Limite constatée** : `aube-plan-01` (issue du plan de nuit i=1) reste plus sombre que les autres variantes ; l'arc lumineux n'est pas parfaitement continu sur la reprise i=44. Signalé, non corrigé.

## Timeline provisoire (§3)

`timeline.json` / `TIMELINE.md` : **46 vers**, fins estimées au début du vers suivant, dernier vers → 220,07 s. `fin` reste **`null`** dans `verses_map.json` : aucune fin de vers n'est présentée comme mesurée. Intro 0 → 1,34 s ; outro 5,00 s ; **durée clip estimée 225,07 s** (~6 752 frames à 30 i/s). Formule d'affichage indicative `min(fin−début, max(2,2 s, 0,30 s × mots))`, **jamais** utilisée pour masquer ou éteindre des paroles (§7). Plan le plus court 2,12 s, le plus long 11,99 s. **Aucune écoute humaine du calage** : syllabes tenues et respirations non vérifiées.

## Teaser — bornes non validées

`teaser_bounds.json` : analyse **RMS 20 ms** sur PCM décodé 16 kHz mono (ffmpeg n9.0.2). Ce n'est **pas une écoute**.
- La proposition initiale `[164.99 → 179.99]` (refrain final) **coupe dans une zone sonore active** en fin (RMS ~2 184) → risque de couper une syllabe.
- `silencedetect=-50dB:d=0.5` = **0 intervalle** : aucun silence naturel dans le morceau.
- **Nouvelle proposition** `[155.96 → 170.96]` (15,00 s) : début exact du vers i=36, fin 0,31 s avant le vers i=40, RMS 644,7 / 1 048,4. Alternative refrain conservée `[164.99 → 179.99]`.
- **Aucune des deux n'est validée** : §10 exige des bornes choisies à l'écoute ; accord de l'artiste ou changement de passage nécessaire avant rendu.

## Mesures réelles du maître (ffmpeg n9.0.2, 2026-11-15)

- Durée décodée **220,07 s** (`[length:03:40]` = 220,00 s est une valeur **déclarée**), MP3 48 kHz stéréo, image jointe MJPEG 360×360 → réencodage avec `-map 0:a:0`.
- `ebur128=peak=true` : **−14,5 LUFS · LRA 6,7 LU · crête vraie +0,1 dBFS** (> 0 dBFS, signalé ; **aucune normalisation**).
- `silencedetect=noise=-50dB:d=0.5` : **0 intervalle**. Ces chiffres ne concernent que le maître, pas les livrables.

## Contrôles effectués / restants

Effectués : `controles/contact-plans.jpg`, `contact-cuits.jpg` (tuiles 480 × 860), `crops-texte-1-1.jpg` (**26 crops 1:1**, tuiles 526 × 600), `zoom-diacritiques.jpg` (zoom 2×), `contact-variantes-aube.jpg`, `contact-nouveaux-bruts.jpg`. Vérifiés : orthographe, accents, apostrophes, contre-formes, texte hors visage, aucun voile/plaque sur les mots, cohérence personnage/palette.

**Non mesurés** (pas de MP4 rendu) : durées/frames du clip et du teaser, `blackdetect` aux deux seuils, `freezedetect`, `ebur128` des livrables, ordre `moov` avant `mdat`, zones sûres sur la vidéo finale, écoute du calage.

## Reste à faire

1. Terminé : plans 36, 37, 38 et 46 générés et cuits ; contrôler leur texte à 1:1 et sur le rendu.
2. Trancher l'extrait du teaser et le calage (`fin`).
3. Habillage : filet de progression, bandeau de messages, badge `DSKY WTBW` ↔ `WTBW`, cartes d'intro/outro, mouvement doux des plans.
4. Rendu clip complet (1080×1920, 30 i/s, H.264/yuv420p/BT.709, AAC 256 kb/s 48 kHz, `+faststart`) et teaser séparé 15,00 s / 450 frames.
5. Contrôles obligatoires §11 puis livraison (titre, captions, hashtags, déclaration IA, commandes Termux figées sur SHA publié).

**Aucun commit, aucun push, aucun SHA publié.** Aucune modification de l'audio. Photos personnelles du dépôt jamais envoyées au générateur. Outils locaux (`.tools/`) réinstallés à la demande par `outils.py`, exclus de Git par `.gitignore`.
