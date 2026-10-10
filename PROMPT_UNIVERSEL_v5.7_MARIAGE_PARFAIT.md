# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v5.7 « MARIAGE PARFAIT »

Mise à jour : **2026-10-10**. Ce document **fusionne** `PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md` et `PROMPT_UNIVERSEL_v5.6_AUBE_CLOCHETTES.md`, et intègre les décisions prises sur « Ça monte, ça descend ». Il **remplace** v5.5 et v5.6 là où il y a conflit. Les paramètres d'une chanson ne se reportent **jamais** automatiquement sur une autre.

## 0 — Priorité et états

1. Demande explicite actuelle de l'artiste.
2. Configuration validée de la production (ancre, personnages, titre exact).
3. Règles universelles v5.7 (ce document).
4. v5.6 puis v5.5 pour tout ce qui n'est pas repris ici. v5.3 reste une archive technique.

Les états « proposé », « généré », « validé par l'artiste », « rendu » et « contrôlé » sont distincts. Ne jamais inventer une validation, un fichier final, un hash publié ou une mesure.

## 1 — Résolution des conflits v5.5 / v5.6

| Sujet | Décision v5.7 |
|---|---|
| Paroles | Mode mixte : centrées pendant les vers, mot actif or, mots passés crème, vague d'eau 4,5 px / 0,9 Hz. Effacées (fondu 0,35 s) pendant les clochettes. |
| Badge | « Dsky » seul, **sans drapeau**. Un fondu 0,4 s par vers, opacité ≤ 75 %. Jamais permanent. |
| Drapeau | **Retiré par défaut de toutes les vidéos** (bandeau et pictogramme). Réservé à une demande explicite et actuelle. |
| Clochettes | Déclenchées sur toute fenêtre sans texte ≥ 5 s. Typographie **premium** (voir §4). |
| Fin de clip | **Plus de contacts.** Carte finale : « Merci d'avoir regardé » + un code facile à retenir. |
| Début de clip | Carte d'accueil d'environ 5 s qui invite à regarder jusqu'à la fin. |
| Personnages | Héros fictifs ou ancre validée. Vêtements fermés et élégants. L'accent est mis sur le visage et l'attitude, jamais sur les parties du corps. |
| Livraison | **Toujours** : Titre, Captions, Hashtags, fichier 9:16, déclaration IA si besoin. |

## 2 — Images et personnages

- **Ancre** : un seul couple de référence, validé par l'artiste avant toute salve (variantes proposées puis choix).
- **Salves de 10 maximum par tour** (quota de génération). Un lot de 20 images = 2 salves sur 2 tours.
- Chaque génération reprend l'ancre via `images=` pour garder les mêmes personnages.
- Cadrage 9:16, pas de texte, lettres, logos, filigrane, ni bandes noires. Tous les visages visibles, aucun membre coupé.
- Recopier le bloc héros mot pour mot dans chaque prompt : origine, teint, tenue exacte, coiffure, bijoux.
- Images de personnages sans nudité, sans poses à caractère sexuel, sans mise en avant de la poitrine ni des fesses. Cadrages acceptés : gros plan du visage, plan moyen, plan large.
- Aucune photo personnelle envoyée au générateur sans autorisation écrite de la personne.

## 3 — Carte d'accueil, carte finale et code

- **Accueil** (0 → ~4,9 s) : deux cartes successives sur le fond d'intro. Phrase de référence : « Regarde jusqu'à la fin » puis « pour découvrir comment proposer un son ou des lyrics à réaliser pour toi ! ». Lecture ~4 mots/s maximum. Si trop rapide, décaler de 2 s, pas de coupe au milieu d'un vers.
- **Carte finale** (5 s après la fin de la chanson) : « Merci d'avoir regardé », « Tu veux un son ou des lyrics à réaliser pour toi ? », « Commente le code », puis le code en grand et une légende courte. Aucun contact, aucun lien, aucun logo.
- **Code** : 4 chiffres, facile à retenir, lié à la chanson si possible (ex. `1010` = « 1 = ça monte · 0 = ça descend »).

## 4 — Clochettes premium (remplace DejaVu / rendu archaïque)

- Polices : **Montserrat** (variable : ExtraBold 800 à Black 900). Jamais de cursive pour les CTA.
- `ABONNE-TOI` : blanc → bleu pâle, espacement 7 px, halo cyan léger.
- `PARTAGE` : pastille sombre translucide, contour dégradé cyan → magenta, texte dégradé, halo pulsé 0,8 s.
- Rappel : « Clique sur la cloche, puis PARTAGE » (600, crème).
- Cloche vectorielle supersamplée ×3 : dégradé or → bronze, reflets, anse, battant, halo. Balancement ±12° amorti, période 1,2 s, pulsation 0,8 s.
- 2 ondes concentriques (0,9 s), 3 étincelles, flèche clignotante vers la cloche.
- Entrée et sortie en fondu 0,35 s. Séquence répétée toutes les 4 s dans les longues fenêtres.
- Zone : cloche et textes entre y 620 et 1340, rien sous y 1574, rien à droite de x 910 entre y 960 et 1690.

## 5 — Safe zones 9:16 (1080×1920, obligatoire)

| Zone | Interdit |
|---|---|
| y 0 → 144 | badge, titres, CTA |
| x ≥ 910 et y 960 → 1690 | paroles, icônes, texte long |
| y ≥ 1574 | paroles, CTA, crédits |

Badge en y = 160. Paroles centrées sur H/2, largeur sûre ≤ 740 px. Scrim central doux.

## 6 — Audio et synchronisation

- Analyser la durée **décodée** (`ffmpeg -map 0:a:0 -f null -`), le tempo (demi/double tempo signalé), la crête (TP ≤ −1,5 dBTP au master).
- Horodatages fournis par l'artiste : les garder tels quels. Corriger seulement les erreurs de copier-coller évidentes, en le signalant.
- Durée d'affichage d'un vers : `min(4 s, max(2 s, 0,07 s × nb_caractères + 1,2 s))`, bornée par le vers suivant. **Hypothèse à valider à l'écoute.**
- Calage des mots au nombre de caractères : **provisoire**, à signaler dans la livraison.
- Master : chanson seule, 48 kHz, MP3 320 kb/s, loudnorm deux passes (−14 LUFS / −1,5 dBTP), ID3 avec pochette et paroles USLT propres.

## 7 — Production et livraisons

Ordre : analyse → cartes d'accueil/finale et code → ancre validée → salve 1 (≤ 10) → salve 2 (≤ 10) → montage 9:16 → contrôles → master et covers → livraison.

- **Rendu** : script versionné (`render_lyric_video.py`), H.264 CRF 24 (taille raisonnable pour le dépôt), AAC 256 kb/s, `+faststart`, `bt709`.
- **Contrôles obligatoires** : durée = frames / FPS, pas de frame noire hors fondu final (`blackdetect`), pas de gel (`freezedetect`), texte complet, centré, hors zones UI, badge unique, clochettes présentes dans toutes les fenêtres ≥ 5 s, visages non coupés, audio et métadonnées conformes.
- **Livraison (toujours)** :
  1. Fichier 9:16.
  2. Titre.
  3. Captions (légende courte + code).
  4. Hashtags (≈ 10 à 13).
  5. Déclaration IA si des visuels ou l'audio sont générés.
  6. Commandes Termux, une ligne par fichier, `;` comme séparateur, sur le hash du commit **après** push.
- **Git** : commit + push après chaque étape, sur la branche de la session uniquement. Pas de `git reset --hard` automatique.

## 8 — Couche validée : « Ça monte, ça descend » (Dsky)

- Titre exact : **Ça monte, ça descend** · artiste : Dsky · signature : « Wolof TechStein beat wê ! ».
- Source audio : `Ça monte_ ça descend.mp3`, 197,60 s décodées. Horodatages : `productions/ca-monte-ca-descend/timings_source.lrc` (55 vers).
- Fenêtres clochettes (calculées) : 114,63 → 120,05 s · 146,00 → 152,40 s · 157,08 → 173,13 s · 189,76 → 197,60 s.
- Fonds : 9 scènes du couple validé (fichiers `personnages/scene-01` à `scene-09`), plus 10 scènes de la salve 2 (`scene-10` à `scene-19`) en attente d'intégration.
- Code de fin : **1010**. Drapeau : **aucun**.
- Titre TikTok : « Ça monte, ça descend — Dsky ». Hashtags et légende : `livrables/LIVRAISON_Ca_monte_ca_descend.md`.
- Points ouverts : calage des mots à écouter ; texte parfois devant les visages (à déplacer) ; déclaration IA à cocher.

## 9 — Historique

- **v5.7** (2026-10-10) — « Mariage parfait » : fusion v5.5 + v5.6 ; badge sans drapeau ; carte d'accueil et carte finale sans contacts ; code de fin ; clochettes premium ; personnages habillés ; livraison systématique Titre + Captions + Hashtags.
- **v5.6** (2026-10-05) — clochettes CTA, style S6 Aube Sacrée, mot sacré en post-production.
- **v5.5** (2026-09-30) — hybride, commande, paroles centrées, safe zones, Termux une ligne.

**Signature :** « Wolof TechStein beat wê ! » ⚡
