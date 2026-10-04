# « Dès le début » — lecture du brief & compréhension

**Statut :** lecture seule — aucune génération d'images ni rendu lancé.
**Date :** 2026-10-04 · branche `arena/01a10746-lyric` (commit de départ `582b89f`).
**Sources reçues :** `Dès le début.mp3`, `Dès le début- Jésus-Christ sauveur.txt`, `indications additifs - dès le début.txt`,
+ le référentiel `PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md` (et l'archive v5.3/§G/§H).

---

## 1. Ce que j'ai compris — la demande du jour

1. La prochaine production complète est **« Dès le début »** (gospel / louange, Jésus-Christ Sauveur),
   produite avec le **prompt v5.5 Hybride & Commande** déjà présent dans le dépôt.
2. **Nouvelle règle CTA (la tienne, prioritaire) :** pendant **toutes les fenêtres de plus de 5 secondes sans parole**
   (intro, trous instrumentaux, ponts, outro), afficher une **animation de clochettes** qui incite à
   **s'abonner** et **surtout à partager** — dans l'esprit des effets des applis de design
   (VN, VivaCut, CapCut). C'est testé ✅ dans le cadrage v5.5.
3. **20 images pour « Dès le début »**, **le même personnage** dans toute la vidéo, construites comme
   **plusieurs frames qui se suivent** : au fil de la musique, les images s'enchaînent comme si la
   personne **bougeait** (décor lui aussi synchronisé). Tu me demandes de dire honnêtement
   **combien d'images** sont nécessaires si 20 ne suffisent pas.
4. **Personnage :** un **homme et une femme**, humbles devant Dieu (l'un tatoué « Jésus » et de ses
   bienfaits sur le corps), **pas un beau gars** — réaliste, « assez » ressemblant, sans embellissement.
   C'est la dérogation **la plus récente** et elle **annule** la règle v5.5 « pas de héros fictif hérité
   de Nonvi Konou » **si et seulement si** tu choisis bien l'option « héros inventé » (§4, Q2).
5. **Photos :** lisibles dans le dépôt ≠ autorisation d'envoi au générateur. Je te demande
   explicitement le dossier/l'option avant tout envoi.
6. **Les 12 images de Samuel/** : il s'agit d'une **retouche photo** (7 prompts d'amélioration : look DSLR,
   lumière, color grading, peau, nettoyage du fond, look cinéma, finition) à appliquer « correctement »,
   **10 images max par salve**.

---

## 2. Ce que dit le v5.5 (rappel des règles qui s'appliquent ici)

| Point | Règle héritée |
|---|---|
| Budget images | `MODE_IMAGES`, `N_SCENES` explicites ; héros **recopié à l'identique** ; une **ancre unique validée avant la salve** ; **planche contact** puis validation ; seuls les slots refusés sont régénérés |
| Héros | Référence autorisée **obligatoire** dans `images=` si ressemblance demandée ; sinon héros inventé, cohérent, jamais embelli |
| Paroles | **Gros, gras, centrés H/2**, mot à mot hybride (or/crème + vague d'eau), jamais dans le rail droit (x ≥ 910) ni la bande basse (y ≥ 1574) |
| Badge | Apparaît/disparaît **en fondu 0,4 s à chaque occurrence de vers** — jamais les deux (badge vivant **ou** badge gravé) |
| Drapeau Bénin | Bandeau fin 54 px en bas de frame, si confirmé |
| Audio / master | Loudnorm 2 passes, 48 kHz, MP3 320 kb/s, APIC + USLT, tags réels |
| Livrables | Clip(s) + MP3 + cover ≥1080² + **prompt à jour** + commandes Termux au HASH du commit de livraison |
| Git | Commit/push **après chaque étape**, sur la branche de session uniquement |

⚠️ **Conflit à trancher** : « paroles centrées H/2 » (§3 v5.5) ↔ « zone paroles ≤ y 1560 » (§0.9 v5.3,
héritage *Le goût bon de la vie*) ↔ « clochettes en ⊥ du rail droit ». Voir §4 Q4.

---

## 3. Chiffres mesurés sur ton MP3 (pas d'estimation)

- **Durée décodée :** 00:03:19,99 (≈ **200,0 s**) · 48 000 Hz · stéréo · 185 kb/s · pochette 360×360 intégrée.
- **Tags présents :** `title=Dès le début`, `artist=codjosamuelstein`, **USLT = paroles complètes avec sections**
  (`[Couplet 1 - Voix masculine, flow posé]`, `[Pré-refrain - Voix féminine, montée]`… — utile pour la narration visuelle).
- **Non silencieux :** le morceau n'a **aucun silence numérique** > 3 s (le beat tourne en continu) →
  les clochettes se déclenchent donc **sur les fenêtres sans VOIX**, pas sur du silence.

### Fenêtres sans parole (> 5 s) — mesurées depuis les horaires du fichier

| # | Début → Fin | Durée | Contexte |
|---|---|---|---|
| 1 | 0,00 → 5,68 | 5,7 s | intro (avant la 1ʳᵉ ligne) |
| 2 | 5,68 → 12,56 | 6,9 s | après « Wolof TechStein beat wê… » |
| 3 | 19,43 → 29,03 | 9,6 s | après « Jésus, Christ Sauveur, Roi des rois » |
| 4 | 62,56 → 68,25 | 5,7 s | après « Wolof TechStein beat wê… » |
| 5 | 103,65 → 116,54 | 12,9 s | après « Jésus… Christ… Sauveur… » |
| 6 | **126,61 → 151,82** | **25,2 s** | après « Dès le début, Tu es là, Tu es là » (pont instrumental) |
| 7 | 169,18 → 200,0 | 30,8 s | outro / queue instrumentale |
| — | 13 autres écarts de 3 à 5 s | — | **non retenus** (seuil = 5 s) |

**Total clochettes ≈ 97 s** sur 200 s (≈ 48 % du clip). Trois apparitions de 25-31 s sont très longues :
proposition de cadence ci-dessous.

**Autres données :** 51 vers · **32 textes distincts** → en mode v5.4 « une image par texte » = 64 fonds
(32 × 2 formats) ; en mode `cinq_scenes` = **10 fonds** (5 scènes × 2 formats). C'est l'arbitrage à faire (§4 Q3).

---

## 4. Ce qu'il me manque avant de produire (réponds en une fois)

1. **Photos autorisées** → `Samuel/` (8 jpg) · `Samu/` (12 jpg) · `klo/` (9 jpg) · `Sam/` (2 mp4) ?
   J'envoie au générateur **uniquement** ce que tu désignes. Rien n'est envoyé sans ton accord.
2. **Types de héros** : (a) les deux, **inventés** — j'applique intégralement « pas un beau gars », photo
   (vide) ; (b) les deux, **à ta ressemblance d'après les photos autorisées** ; (c) mixte (femme inventée + toi).
3. **Budget images** : (a) **10 fonds** (5 scènes × 2 formats, défaut v5.5) ; (b) **20 fonds** (10 scènes × 2 formats) ;
   (c) one-shot « 1 image par texte » = 64 fonds (non recommandé).
4. **Paroles** : (a) **centrées H/2** avec clochettes sur le rail gauche/au-dessus (défaut v5.5) ;
   (b) **hors visage, ≤ y 1560** (héritage §0.9) ; (c) mode A pendant les vers, mode B pendant les clochettes.
5. **Cadence des clochettes** (ma proposition, à valider) : entrée/sortie en **fondu 0,35 s**, **balancement
   amplitude ≈ ±12°**, période **1,2 s**, halo pulsé **0,8 s**, 2 anneaux d'onde, étincelles ;
   apparitions répétées toutes les **4 s** dans une longue fenêtre (≈ 6 passages sur 25 s — pas d'icône figée 25 s)
   → en gardant « abonne-toi » + **« PARTAGE »** (prioritaire, contour cyan pulsé).
6. **Style graphique** (v5.5 §G) : S1 Dark Lightning · S2 Golden Sunset · S3 Neon Afro-Futurism · S4 Ink & Fire ·
   S5 Retro Film 70s · Hybride (S1 + S2 sur ponts) — le gospel appellerait plutôt **S2/Hybride**, mais je ne décide pas à ta place.
7. **Formats / cold-open / badge / cover / livrables** : mêmes questions que §B (défauts v5.5 si tu dis « je te fais confiance »).
8. **Retouche photo** : j'applique les 7 prompts de `Samuel/Indications.txt` aux photos que tu désignes
   (10 max par salve), avec l'ancre « 1 photo » validée avant la salve.

---

## 5. Aperçu déjà prêt

`productions/des_le_debut/apercu/CLOCHETTES_apercu.gif` (+ `.png`) : maquette animée **fond provisoire**
de l'effet clochettes décrit en §4 Q5, avec les zones réelles 1080×1920 (rapport 1:1/2,25), le texte
« Dès le début, Tu es là, Tu es là » au-dessus et le bandeau Bénin en pied de frame.
→ Si l'effet te convient, il est **codé** dans `productions/des_le_debut/scripts/apercu_clochettes.py`
et sera réutilisé tel quel au rendu final (vectoriel, aucune emoji système, glyphes contrôlés).

## 6. Ce que je ne ferai pas sans ton accord

- aucune génération d'image (ni 20, ni ancre, ni salve) ;
- aucun envoi de photo personnelle au générateur ;
- aucune modification du MP3 source ; aucun commit d'un fichier « final » qui n'existe pas ;
- pas de hash/URL Termux avant que le fichier existe réellement dans un commit poussé.
