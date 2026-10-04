# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v5.5 « HYBRIDE & COMMANDE »

Mise à jour : **2026-09-30**. Ce document est universel ; les paramètres d'une chanson ne doivent jamais être attribués automatiquement à une autre. Il consolide v5.4 et les consignes récentes de « Concentré sur le chemin ». Le référentiel v5.3 est conservé ci-dessous comme archive technique, **subordonnée aux règles de priorité de cette page**.

## 0 — Priorité et états de validation

1. Demande explicite actuelle de l'artiste et réponses au questionnaire.
2. Configuration de la production confirmée, puis ancre validée.
3. Règles universelles v5.5 ci-dessous.
4. Référentiel historique v5.3 ; ses titres, noms et anciennes mesures sont des exemples, jamais des valeurs universelles ni des résultats de contrôle de la production actuelle.

Les états « proposé », « généré », « validé par l'artiste », « rendu » et « contrôlé » sont distincts. Ne jamais inventer une validation, un fichier final, un hash publié ou une mesure.

## 1 — Images : budget explicite avant la règle par vers

Paramètres : `MODE_IMAGES`, `N_SCENES`, `FORMATS`, `INTRO_REUTILISE`, `ENDCARD_REUTILISE`, `COVERS_REUTILISENT`.

- **Défaut v5.4 :** un fond par texte distinct et par format ; reprise strictement identique = réemploi. Respecter casse, accents et ponctuation. Deux fonds dédiés intro/endcard seulement si le budget l'autorise.
- **Dérogation « cinq images portrait et cinq paysage » :** `MODE_IMAGES=cinq_scenes`, `N_SCENES=5`, `FORMATS=[9:16,16:9]` → **dix fonds finaux en tout**, jamais 38×2 images ni cinq images au total. Chaque scène existe dans les deux cadrages. Répartition des scènes selon sections/énergie ; tous les vers réutilisent cet ensemble.
- Dans ce mode, intro, endcard et covers dérivent des cinq scènes par format, sans nouvelle génération. L'ancre portrait compte comme le premier des cinq portraits si elle est acceptée. Une correction remplace un slot, elle n'ajoute pas une sixième scène.
- Une ancre unique à valider **avant** la salve restante. Prompts complets écrits avant chaque lancement ; dix générations maximum par tour. Planche contact et validation après salve ; ne régénérer que les slots refusés.
- Préserver les originaux IA utiles, les scripts et prompts. Ne pas stocker de caches WAV, binaires FFmpeg ni environnements dans Git.

## 2 — Héros fidèle, références expressément autorisées

Paramètres : `HEROS_MODE`, `PHOTOS_AUTORISEES`, `STYLE`, `BLOC_HEROS`, `TENUE`, `POSE`.

- Photos présentes dans le dépôt ≠ autorisation de les envoyer au générateur. Faire confirmer le dossier/fichiers de la chanson.
- Si l'artiste demande sa ressemblance, ne pas utiliser un héros fictif d'un autre morceau. Examiner les originaux approuvés ; préserver traits, proportions, teint, corpulence, cheveux, pilosité et lunettes. Aucun embellissement, vieillissement, musculation ou barbe inventée.
- Chaque génération de cette personne utilise les originaux autorisés dans `images=` ; l'ancre approuvée peut s'ajouter comme guide de style mais ne remplace pas les références d'identité.
- Si l'artiste choisit au contraire un héros inventé : ne transmettre aucune photo personnelle au générateur.
- Recopier le bloc héros à l'identique après validation. Les vêtements et la pose demandés priment sur les habits d'une référence photo et sur les exemples antérieurs.
- La fidélité visuelle reste à valider par l'artiste ; ne pas promettre une identité pixel à pixel après stylisation IA.

## 3 — Paroles très grandes, hybrides et centrées

Paramètres : `TEXTE_HYBRIDE=true`, `POLICE_PAROLES`, `TAILLE_MAX`, `TAILLE_MIN`, `MAX_LIGNES`, `CENTRE=(W/2,H/2)`.

- **Une seule variante fusionnée :** apparition/lecture mot à mot, mot actif or/crème, mots passés atténués mais lisibles, et vague d'eau continue des glyphes présents (amplitude ≈4,5 px, fréquence ≈0,9 Hz).
- Calculer la disposition du **vers complet** avant animation. Chaque ligne et le bloc sont centrés ; aucune dérive/recentrage progressif quand les mots apparaissent. Tous les mots finissent visibles, sans troncature.
- Préférer les retours à la ligne équilibrés à une taille illisible. Pour une demande de gros caractères gras : police condensée grasse lisible autorisée, caractères accentués vérifiés ; pas de substitution automatique par une cursive.
- Conserver le centre vertical **dans les deux formats**. Prévoir dès l'ancre le visage au-dessus/à côté du texte. Ne pas rabattre automatiquement les paroles dans la bande basse pour cacher un mauvais cadrage.
- Portrait : rail droit x≥910 à partir de y=960 ; avec un bloc centré à x=540, largeur sûre ≤720 px (x=180→900), et non 880 px. Aucune parole ni contact à y≥1574 ; haut y≤144 réservé. Paysage : contrôles bas y≥H−120 vides.
- Scrim central doux, localisé et adapté pour ne pas noircir le visage. Marges de glyphes ≥6 px **après** vague/contour ; contrôler les vrais vers longs sur une frame mobile.
- Le mode « mot grossit puis petit trail, sans vague » de l'ancien addendum ne s'applique que si l'artiste le redemande explicitement. Il ne remplace pas le mode hybride courant.

## 4 — Badge : présence par vers ou permanente, jamais les deux

Paramètres : `BADGE_ARTISTE`, `BADGE_MODE`, `BADGE_DRAPEAU`, `BADGE_BAKED_IN`.

- **Défaut et demande « apparaît et disparaît à chaque vers » :** calque UI compact, position fixe sous la bande haute interdite, opacité maximale 75 %, fondu d'entrée 0,4 s et de sortie 0,4 s **pour chaque occurrence de vers**, y compris deux vers qui partagent un fond ou un refrain repris.
- Dans ce mode, **ne pas graver le badge dans les fonds**. Il doit pouvoir disparaître ; ne jamais superposer un second badge sur un badge intégré. Intro/hook/endcard suivent leurs fenêtres propres.
- Dérogation v5.4 « badge sur toutes les images » : valable uniquement si cette demande est explicite et toujours actuelle. Composer alors un seul badge dans chaque image ; ne pas réanimer un doublon. Une demande plus récente de badge temporaire annule cette dérogation.
- Police UI nette (DejaVu Sans Bold ou équivalente), nom exact. Si drapeau demandé, dessiner un pictogramme vectoriel, pas un carré tofu ni un emoji dépendant du système.
- Pas de gros CTA permanent ou d'icônes sociales non demandées. Le « badge statique » des anciens contrôles signifie position fixe, **pas opacité permanente**.

## 5 — Drapeau et texte en post-production

Paramètres : `DRAPEAU_PAYS` (nullable), `BANDEAU_DRAPEAU` (booléen), `TITRE_EXACT`, `ARTISTE`.

- Ne pas imposer le Bénin ni `Dsky` à un artiste différent. Une demande de badge avec drapeau et une demande de bandeau sont deux choix séparés.
- **Bénin si confirmé :** bande fine pleine largeur ; portrait 1080×1920 = y=1866→1920, **54 px**. Vert sur le tiers gauche, jaune en haut des deux tiers droits, rouge en bas. Couleurs #008751 / #FCD116 / #E8112D. Hauteur relative identique pour les variantes (≈30 px sur hauteur 1080).
- Le bandeau décoratif est permis dans la zone basse interdite aux paroles/contacts ; son existence ne permet pas d'y déplacer les paroles.
- Composer le bandeau en post sur les images livrées, covers, intro/endcard et frames finales. S'il doit rester collé au bord, l'ajouter après le Ken Burns ; ne pas zoomer un drapeau pré-incrusté et en redessiner un deuxième.
- Fonds IA : aucune lettre, nombre, logo, filigrane, enseigne ou emblème. Titre exact, artiste, badge, drapeau et marques sociales optionnelles sont ajoutés séparément. Si citer un objet interdit provoque son hallucination répétée, ne plus le nommer dans les prompts suivants ; réserver seulement les espaces de compositing.
- Tester les pixels du drapeau sur un export sans perte, puis vérifier la version encodée avec une tolérance de compression. Lire le badge à taille téléphone.

## 6 — Analyse, audio et synchronisation honnêtes

- Analyser automatiquement les sources avant le questionnaire : durée **décodée** (`-map 0:a:0 -vn -f null -`), fréquence/canaux, tempo estimé et ambiguïté demi/double tempo, énergie RMS, loudnorm passe 1 au niveau info.
- Lire LRC, heure en fin de vers, intervalles début-fin, ou paroles sans heure ; préserver sections et texte. Convertir proprement l'encodage et retirer les contrôles directionnels parasites sans modifier les caractères visibles. Original inchangé.
- Vérifier monotonie, plage audio et intervalle minimal de travail 1,2 s ; un pic de flux spectral à ±0,35 s est **un indice musical, pas une preuve d'attaque vocale**.
- Ne pas déplacer automatiquement des départs valables sur des percussions. Comparer les reprises sans imposer les deltas du premier refrain lorsque la performance diffère. Trois passages test à écouter au minimum ; contrôle des fins et du mot à mot séparément.
- Conserver `timings_audited.json` pour les résultats structurels ; ne créer/nommer `timings_validated.json` qu'après une véritable validation. Un calage des mots au nombre de caractères dans une maquette doit être signalé comme **provisoire**.
- Ne pas prolonger mécaniquement un dernier vers pendant toute une queue instrumentale. Le badge suit la fenêtre vocale définie, pas l'image ni toute la plage entre deux départs éloignés.
- Hook : extrait du refrain-titre énergétique ; ne pas couper un vers pour imposer 6,00 s arbitrairement. Proposer une coupe naturelle proche de 6 s et faire approuver ; sans hook si demandé.
- Master : chanson seule, audio explicitement mappé, 48 kHz / MP3 320 kb/s. Loudnorm deux passes avec mêmes pré-filtres, `offset=` à la passe 2, cible −14 LUFS / −1,8 dBTP ; contrôler le MP3 final (TP≤−1,5). APIC avec Mutagen après encodage, USLT propre, tags/contact confirmés. Ne pas inventer producteur/compositeur/genre.
- Un flux de `ceil(TOTAL×FPS)` frames, `TOTAL=HOOK+DUREE_AUDIO+5`, musique et fonds sur la même horloge ; avance des paroles 0,03 s. Aucun concat demuxer vidéo ni fade-in noir. Fade final uniquement. Décoder les segments audio avant concaténation hook/chanson.

## 7 — Production et livraisons

Ordre : analyse → questionnaire groupé (ne pas redemander les choix déjà explicites) → ancre + maquette texte/badge → validation → salve autorisée → planche contact/validation → portrait → contrôles → paysage → master et covers → livraison.

- Scripts versionnés, caches sous `work/` ignorés, environnements et binaires hors dépôt. FFmpeg absent : wheel PyPI `imageio-ffmpeg` dans environnement temporaire, pas de changement de pipeline arbitraire.
- Commit/push après chaque étape, **sur la branche de la session uniquement**. Ne pas lancer de `git reset --hard` automatique : inspecter les changements et préserver le travail de l'utilisateur.
- Livrables finaux : clips demandés, MP3, cover carrée ≥1080 et variantes demandées, prompt actuel complet, commandes Termux. Maquette/ancre ≠ clip final : les nommer clairement et demander validation sans lancer silencieusement le reste.
- Contrôles réels : taille/durée/streams, absence de frames noires hors fade final et de gel non prévu, texte complet/centré/hors UI, badge unique et fondus par vers, drapeau conforme, glyphes et visages non coupés, audio/tags/covers. Les mesures des anciennes productions ne sont pas des preuves pour la nouvelle.
- Termux : une ligne par fichier, séparateur `;`, `curl -fL --retry 5 --retry-delay 3 -C -`, destination `/storage/emulated/0/Web+/`. Hash obtenu **après commit/push**, fichier vérifié dans ce hash ; encoder les chemins URL si accents/espaces. Ne jamais fournir de hash ou URL d'un fichier qui n'existe pas encore. Les scripts de récupération restent reprenables. Un document texte peut légitimement faire moins de 100 ko ; la règle de fichier minuscule vise les médias supposés volumineux, pas tous les fichiers indiscriminément.

## 8 — Couche validée : Concentré sur le chemin

Cette section est **locale à cette commande**, non un défaut pour les suivantes.

- Titre exact : **Concentré sur le chemin** ; artiste/contacts du pack : Daïsky, `daiskyproduction@gmail.com`, WhatsApp `+229 01 61 16 24 08` / `+229 01 49 11 49 51`.
- Sources : `Concentré sur le chemin.mp3` et `concentré sur le chemin.txt` ; copie nettoyée `Concentré sur le chemin.lrc`. Audio 213,160 s ; 58 vers / 38 textes distincts, horaires source conservés.
- Questionnaire : **Samu autorisé**, **gras**, **Dsky + drapeau Bénin + bandeau fin**, **pack complet**, ouverture souhaitée.
- `MODE_IMAGES=cinq_scenes`, deux formats 1080×1920 / 1920×1080, **dix fonds en tout** ; ancre s01 portrait comprise.
- Héros animé à la ressemblance de l'artiste, lunettes des références, habits très usés/rapiécés, deux mains sur la tête avec une cigarette entre les doigts, fumoir qui est aussi un studio de musique. Aucun personnage fictif indigo/pantalon sable hérité de Nonvi Konou.
- Barlow Condensed Bold, mots or/crème, vague simultanée, centre H/2 ; badge `Dsky` + pictogramme Bénin en fondu 0,4 s, plafond 75 % ; bandeau portrait 54 px fixe au bord inférieur.
- **Ancre et maquette de 14,5 s approuvées** : ressemblance, lunettes et taille des caractères conservées. **Dix fonds approuvés** (cinq scènes dans les deux formats) après la planche v2 : « Oui je valide !! ». Les cinq paysages ont été repris pour un cadrage complet et un éclairage continu ; aucune scène supplémentaire. Les deux clips complets sont rendus et contrôlés techniquement : 1080×1920 / 1920×1080, H.264 BT.709, 30 fps, 6 752 frames chacun, durée 225,066667 s (ouverture 6,90 s + chanson 213,160 s + fin 5 s). Master MP3 320 kb/s / 48 kHz exporté, ID3v2.4 avec APIC/USLT, mesuré −14,02 LUFS / −1,64 dBTP ; trois covers exportés depuis les fonds approuvés. Le calage des mots reste une estimation depuis les horaires source ; la synchronisation vocale complète est à confirmer à l’écoute, indépendamment de la validation visuelle.
- Index de la livraison complète : `livrables/LIVRAISON_Concentre_sur_le_chemin.md` ; commandes réelles après publication : `livrables/TERMUX_Concentre_sur_le_chemin_COMPLET.md`. Rapports vidéo : `qa_portrait.json` / `qa_landscape.json` (dans le dossier de production). Aucun nouveau fond généré pour ce montage.
- Détails et états courants : `productions/concentre_sur_le_chemin/production.json`, `BRIEF.md`, `ANALYSE.md`, `VALIDATION_FONDS.md`, `backgrounds_manifest.json` et `PROMPTS_IMAGES_Concentre_sur_le_chemin.md`. Pack des dix fonds : `livrables/Concentre_sur_le_chemin_10_images_v2.zip`.

---

# Archive technique v5.3 (conservée, sous réserve des priorités v5.5)

Les consignes, valeurs fixes et addenda de chansons ci-dessous ne prévalent jamais sur les sections 0–8 ci-dessus.

# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v5.3 « FINAL RÉSILIENT » (covers universelles + audio propre + solutions Termux)

**Portée :** N'IMPORTE QUEL audio (mp3/wav) + N'IMPORTE QUELLES paroles (txt/lrc, tous langues) + photos optionnelles → un clip lyrics complet (vidéo 9:16/16:9, MP3 master propre taggé, cover universelle carrée + variantes plateformes) + livraisons Termux.
**Règle de continuité :** en cas de blocage d'outil ou de réseau, appliquer §0.6 avant de changer de pipeline ou de demander un nouvel envoi à l'artiste.
**Mode d'emploi :** l'IA exécute **§A (analyse auto, sans questions)** → **§B (questionnaire UNIQUE, 8 questions avec défauts)** → **§C→§F (production complète)**. Si l'artiste dit « vas-y direct / je te fais confiance » : appliquer les défauts marqués (défaut) et les journaliser dans le commit.
**Héritage :** v4.6→v4.9.1 (productions *Le Survivant*, *Seul(e) dans ma tête*, *Je crache mes démons*) — toutes les leçons sont ici des règles.

---

## §0. ADDITIONS v5.3 FINAL (retours artiste — OBLIGATOIRES, priorité max)

**0.1 Paroles AU MILIEU.** Les vers sont centrés **horizontalement ET verticalement** (base y = H/2), jamais en bas de frame ; scrim dégradé doux **central** (bande ±260 px autour de H/2) pour la lisibilité. Le centrage se fait sur la largeur FINALE du vers (pas de dérive pendant l'apparition staggered).

**0.2 Badge DISCRET qui vit avec les paroles.** Badge artiste (défaut `DSKY✓`) : compact (police UI ~40 px), opacité **≤ 75 %**, il **apparaît en fondu 0,4 s avec chaque vers et disparaît en fondu 0,4 s à sa fin** — rien de permanent, jamais de grosse pastille fixe. Présent aussi pendant le hook (discret) et l'endcard.

**0.3 Endcard SIMPLE.** Fini la longue liste de crédits : endcard = titre cursive + **WhatsApp + email seulement** + badge DSKY✓. Contacts défaut artiste : `daiskyproduction@gmail.com` · WhatsApp `+229 01 61 16 24 08` / `+229 01 49 11 49 51`. Les mêmes contacts vont dans les tags ID3 (TXXX contact/email).

**0.4 Douceur optionnelle.** Si l'artiste dit « adoucis » : voile lumineux chaud (blend glow 0,22), contraste ×0,92, noirs relevés (+14), et suffixe de style soft (haze ambre, ombres douces) sur TOUTES les salves suivantes — appliqué rétroactivement aux salves déjà validées pour cohérence.

**0.5 Livraison = clip + prompt à jour + commandes Termux.** Chaque livraison inclut OBLIGATOIREMENT : le clip final, le **prompt universel à jour** (ce fichier) et les **commandes Termux §E.6** régénérées avec le nouveau HASH de commit (fichiers : clip, master, covers, prompt md).

**0.6 SOLUTIONS DE SECOURS VALIDÉES — ne jamais bloquer la livraison.**

- **FFmpeg/ffprobe indisponible ou téléchargement GitHub bloqué :** créer un environnement temporaire Python et installer la wheel PyPI `imageio-ffmpeg` : `python3 -m venv /tmp/lyric-venv; /tmp/lyric-venv/bin/pip install --no-cache-dir imageio-ffmpeg`; récupérer le binaire avec `imageio_ffmpeg.get_ffmpeg_exe()`. Ne jamais ajouter le binaire FFmpeg ou le venv au dépôt.
- **Durée audio sans ffprobe :** mesurer avec le FFmpeg de la wheel (`ffmpeg -hide_banner -i audio.mp3 -f null -`) et prendre la durée décodée réelle ; cette valeur commande le rendu, l'export MP3 et les contrôles.
- **Paroles longues coupées horizontalement :** générer l'ASS avec `WrapStyle: 1`, largeur maximale contrôlée, aucune troncature ; réextraire une planche de contrôle après rerendu.
- **MP3 qui s'arrête à la durée d'une cover incorporée :** mapper explicitement l'audio (`-map 0:a:0 -vn`), produire le MP3 sans image, puis ajouter la pochette en APIC avec Mutagen ; ne jamais laisser une image entrée imposer la durée audio.
- **Coupure réseau Termux :** commande copiable en **une seule ligne**, séparée par `;`, `curl -fL --retry 5 --retry-delay 3 -C - -o ... URL` ; relancer la même commande pour reprendre. Ne pas utiliser `&&` ni une continuation `\` dans une commande affichée dans un viewer HTML.
- **Fichier téléchargé minuscule ou erreur HTTP :** `curl -fL` doit échouer ; supprimer le fichier partiel de moins de 100 ko, contrôler `ls -lh`, puis relancer avec le même hash immuable.

---

## §A. ANALYSE AUTOMATIQUE (jamais de question à ce stade)

**A.1 Audio.** Durée décodée exacte (`ffmpeg -f null -`, sans dépendre de `ffprobe`), SR/canaux, BPM estimé (flux spectral), structure énergétique (couplets/refrains/ponts par RMS), puis mesure loudnorm **passe 1 avec `-v info`** (le JSON n'est émis qu'au niveau info) : `input_i, input_tp, input_lra, input_thresh, target_offset`.

**A.2 Paroles.** Accepter 4 formats : `-m:ss.x` en fin de ligne · `m:ss-m:ss` · LRC `[mm:ss.xx]` · **sans timestamps** → auto-alignement : onsets détectés répartis sur les sections + validation artiste sur 3 lignes test. Sections `[INTRO]/[REFRAIN]/...` conservées comme métadonnées.

**A.3 Validation vers par vers (règle d'or).** Onset = pic de flux spectral > 1,15 × médiane locale (fenêtre 4 s) ; tolérance **±0,35 s** ; **monotonie stricte** + **fenêtre mini 1,2 s** entre vers consécutifs ; corrections par **miroir de section répétée** (deltas d'un refrain repris = deltas de la 1ʳᵉ apparition) puis pics audio ; sorties : `work/timings_validated.json` + **`<Titre>.lrc` corrigé committé**.

**A.4 Budget images (RÈGLE 1).** Ligne UNIQUE = 1 image par format ; texte identique repris = réutilisation ; texte différent = image différente (même ponctuation : « wê... » ≠ « wê! »). `N = uniques + 2` (fond intro musicale + fond endcard) **par format**. Salves de **10 max** (= quota plateforme 10 générations/tour).

**A.5 Moment fort (cold-open).** Chercher la section la plus énergétique contenant le TITRE (défaut = 1ʳᵉ apparition du refrain-titre) ; extrait audio = 2 lignes si ≥5 s sinon 1 ligne ; durée défaut **6 s** (4 s si refrain <5 s).

**A.6 Identité visuelle.** Si photos fournies : décrire un **BLOC HÉROS fidèle** (corpulence RÉELLE — jamais musclé/embelli si l'artiste ne l'est pas, coupe, barbe, lunettes, vêtements récurrents) + règle ANTI-EMBELLISSEMENT absolue. Sans photos : inventer un bloc héros cohérent (âge, morphologie, vêtements) et le recopier À L'IDENTIQUE partout.

---

## §B. QUESTIONNAIRE DE DÉMARRAGE (le SEUL lot de questions — copier-coller tel quel)

> Poser ces 8 questions en UNE fois (outil ask_user), options + défaut indiqués. Réponse « direct/confiance » = défauts.

1. **🎨 Style graphique — 5 STYLES au choix (§G)** — (a) **S1 Dark Lightning** · (b) **S2 Golden Sunset** · (c) **S3 Neon Afro-Futurism** · (d) **S4 Ink & Fire** · (e) **S5 Retro Film 70s** · (f) **Hybride (défaut)** : S1 partout + S2 sur ponts/outro doux · (g) **Innovation IA** : l'IA propose un 6ᵉ style moodboard (1 ancre) si l'artiste curieux. *Heuristique auto si confiance : lexique sombre→S1, amour→S2, fête/urbain→S3, deuil/introspectif→S4, nostalgie→S5.*
2. **🧍 Héros** — (a) photoréaliste fidèle photos · (b) **semi-réaliste seinen fidèle (défaut si photos)** · (c) inventé cohérent (défaut sans photos) · + lunettes : sans / avec / mixte scènes calmes.
3. **📐 Formats** — (a) **9:16 seul (défaut)** · (b) 9:16 + 16:9 · (c) + version texte droit en parallèle.
4. **✍️ Texte** — (a) **cursive + vague eau (défaut)** · (b) droit gras · (c) les deux styles 9:16.
5. **⚡ Cold-open** — (a) 4 s · (b) **6 s (défaut)** · moment = défaut A.5 sauf choix artiste.
6. **📣 Badge** — **discret, apparaît/disparaît AVEC les paroles (§0.2)**, JAMAIS permanent ; pas d'icônes CTA fixes sauf demande artiste ; label défaut `DSKY✓` milieu haut ; contacts défaut §0.3.
7. **🖼 Cover** — **100 % IA titre intégré (défaut)** · sinon texte post (dérogation tracée).
8. **📦 Livrables** — vidéo+MP3+cover+**prompt à jour** **(défaut)** · +16:9 ? · +version allégée ≤50 Mo ? · destination Termux `/storage/emulated/0/Web+/` avec commandes §E.6 régénérées au HASH du commit de livraison (§0.5).

---

## §C. ORDRE DE PRODUCTION (universel, ne pas inverser)

1. §A complet → 2. §B → 3. **Ancres** (1/charte retenue) + maquette badge/vers/CTA → validation artiste → 4. **Salves de 10** : prompts écrits EN ENTIER avant lancement (§E.1), planche contact + validation entre salves, salve refusée = seuls slots concernés → 5. Pré-calcul fonds → rendu 9:16 d'abord → vérifs §D.10 → 16:9 si demandé → MP3 master + tags → covers → 6. **Commit + push après CHAQUE étape** (branche `arena/<id>-<slug>`).

---

## §D. RÈGLES TECHNIQUES UNIVERSELLES (leçons gravées)

**D.1 Sync SOLUTION A.** Un seul flux de `ceil(TOTAL×FPS)` frames, frame `i` ↔ `t=i/FPS` ; `TOTAL = HOOK + durée_chanson + apad(5 s)` ; fenêtres de vers décalées de HOOK ; vers avec **0,03 s d'AVANCE** ; fonds sur horloge musique. Interdits : concat demuxer vidéo, clips séparés, fade-in vidéo (frames noires).

**D.2 Mouvement permanent.** Ken Burns canvas 1,1× (1188×2112 / 2112×1188), zoom 1,02→1,08 alterné par slot, pan sinusoïdal ; **vague eau** : cursive = ligne connectée ondulée par colonnes (ampl. ~4,5 px, 0,9 Hz) + apparition staggered 0,9 s / cascade inversée ; texte droit = lettres une à une (ampl. ~6 px).

**D.3 Anti-coupure, anti-mélange & SAFE ZONES PLATFORMES (§H).** Bbox sprites : marges glyphs **≥6 px** ; dépassement = réduction puis retour à ligne, JAMAIS troncature. Positions UI canoniques 9:16 = **§H (safe zones TikTok/Reels/Shorts)** : badge y=150 centré **discret ≤75 % opacité, fondu avec les vers (§0.2)** · titres hook y=330 · paroles **centrées H/2 (§0.1)** + **scrim dégradé central** derrière · endcard contacts dans [0,25H ; 0,75H]. 16:9 YouTube : paroles base H−170, endcard cx=0,38×W, bande basse H−120 vide.

**D.4 Audio.** loudnorm 2 passes : passe 1 `-v info` ; passe 2 `offset=` (pas target_offset) + `highpass=30,lowpass=18000` ; **TP cible −1,8** ; concat hook+chanson : **tout décoder en WAV 48 k d'abord** (concat pcm+mp3 = durées/gains faux) ; MP3 livrable = chanson seule 320 k 48 k `-t durée` ; tags ID3v2.4 : TIT2/TPE1/TALB/TPE2/TPUB/TCOM/TCON/TDRC + TXXX contact,email,producer,label + **USLT paroles nettoyées** + **APIC cover carrée**. Si le fichier source contient déjà une image attachée, utiliser `-map 0:a:0 -vn` pour produire l'audio seul puis injecter l'APIC après encodage.

**D.5 Vidéo.** Encodage image2pipe mjpeg → libx264 une passe ; master local crf19 ; **export git crf21 ≤ ~95 Mo** (limite GitHub 100 Mo/fichier, warning OK >50 Mo) ; aac 192k +faststart ; fades out audio+vidéo 3 s fin uniquement ; mux = ré-encodage vidéo obligatoire si filtre fade (`-c:v copy` + filtre = erreur).

**D.6 Images.** Prompt 7 blocs (§E.1) ; suffixes canoniques A/B (§E.3) ; interdits toujours + `no signage` (enseignes néon = texte !) ; anti-hors-cadre (sujet complet, mains, visage) ; arc lumineux (intro dim → refrains full → pont ambre → outro décrescendo → endcard sombre) ; post-contrôle ratio/texte/héros ; **modération bloquante = reformuler** (retenue physique → « poids de fumée », « soutenir un ami »).

**D.7 Polices.** Cursive GreatVibes = paroles + titres intro/endcard/covers SEULEMENT ; UI (badge, endcard, contacts) = DejaVu Sans Bold jamais script. Acquisition CDN bloqués : `npm pack @fontsource/<police>` → woff2 → **fontTools+brotli → .ttf committé dans `assets/fonts/`** ; vérifier coverage glyphs du texte réel (ex. « œuvre »).

**D.8 Endcard.** Fond sombre épuré dédié (slot s{N+1}) en Ken Burns (freezedetect 0) ; titre cursive + **WhatsApp + email seulement (§0.3)** + badge DSKY✓ discret ; démarre au fondu final + apad 5 s.

**D.9 Covers.** La cover universelle de référence est carrée **1080×1080 minimum** (ou 3000×3000 si le diffuseur l'exige), lisible en vignette et utilisable pour les plateformes audio ; produire aussi 1080×1920 et 1920×1080 lorsque la plateforme le demande. Base IA : sujet et ambiance **sans texte, sans lettres et sans logos** ; incruster ensuite en post le titre exact `Noukiko tché wê`, l'artiste `Daïsky`, le badge `DSKY✓`, la bande de couleurs béninoises et, seulement si demandé, des marques sociales Facebook/TikTok discrètes dans une zone secondaire. Les logos Facebook/TikTok doivent être des marques vectorielles/post-production propres, jamais du texte illisible généré par l'IA. Grande typographie lisible, hook visuel 1 point focal, orthographe vérifiée, marges de sécurité ≥8 %. Sorties : 1080×1080 APIC + 1080×1920 + 1920×1080 ; pièges réels : cigarette ajoutée par l'IA si « smoke » → écrire « smoke from mouth, no cigarette » ; enseignes → `no signage`.

**D.10 Vérifs avant commit.** Durée `nb_frames/fps` ±0,05 s · streams conformes · blackdetect = fade final seul · freezedetect 0 · frontières vers par diff pixel MP4 vs reconstruction <6 px (mesuré 1,8-2,6) · badge statique · bbox sprites ≥6 px (mesuré 39) · MP3 LUFS≈−14/TP≤−1,5/durée/tags · covers lisibles + badge.

**D.11 Git/anti-reset.** Push après chaque étape ; reset sandbox → `git fetch origin <branche> && git reset --hard FETCH_HEAD` ; **scripts VERSIONNÉS dans `scripts/`** (setup_env.sh, pipeline_rendu_9x16.py, rebuild_timings.py) ; `work/` = cache non versionné (fonds, wav, icônes régénérables 4 gén.) ; `.gitignore` : .venv/, work/, *.pyc, bin/ ; livrables/ et assets/ JAMAIS ignorés. Les wheels et binaires temporaires restent hors dépôt.

**D.12 Quotas.** 10 générations d'images/tour = 1 salve ; jamais 2 salves/session ; slots manquants complétés au tour suivant sans bloquer le pipeline (fonds/rendu continuent).

---

## §E. GABARITS UNIVERSELS (copier-coller, remplir les {})

**E.1 Prompt image (7 blocs, dans l'ordre) :**
`{CADRAGE : vertical 9:16 portrait composition, tall framing | horizontal 16:9 landscape composition, wide framing}` · `{SUJET-VERS : une phrase VISUELLE = métaphore du vers, jamais le texte literal, intensité lumineuse précisée (dim/moderate/full)}` · `{HÉROS : bloc §A.6 recopié à l'identique}` · `{PLAN : wide (refrains/show) | medium (narration) | close-up (émotion/pont) — alterner dans la salve}` · `{SUFFIXE : §E.3}` · `{ZONE : vers → darker, less busy lower third with soft bokeh for lyric text readability | intro/covers 9:16 → large dark negative space across the top quarter | covers 16:9 → left third | endcard → center}` · `{INTERDITS : no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage}` + anti-hors-cadre `full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible`.

**E.2 Écriture SUJET-VERS (méthode) :** verbe d'action + objet métaphorique + émotion ; fumée/lumière/eau pour l'abstrait ; jamais d'objets à risque modération (armes, retenue physique) → substituts (fumée pesante, silhouettes floues, mains tendues).

**E.3 Suffixes canoniques :**
B : `deep blue-black night, warm amber backlight, subtle electric cyan rim light, wet asphalt reflections, atmospheric haze, crushed blacks with cyan highlights, moody anime-seinen cinematic grading, 35mm film grain`
A : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading`

**E.4 Endcard/crédits :** `{TITRE cursive 110}` · `{LABEL / ARTISTE}` · `{GENRE} · {ANNÉE}` · `{TÉLÉPHONES}` · `{EMAILS}` · `{@HANDLE}` · `{SIGNATURE}`.

**E.5 Tags ID3 :** voir D.4 ; USLT = paroles sans timestamps ; APIC = cover carrée.

**E.6 Termux (FORMAT ANTI-CASSE, leçon 2026-09-23) :** commande **UNE SEULE LIGNE**, séparateur `;` (JAMAIS `&&` ni `\` multiligne : le copier-coller depuis un viewer HTML transforme `&&` en `&amp;&amp;` et casse les continuations). Sur Termux fraîchement installé : `pkg update -y; pkg install -y curl ca-certificates; termux-setup-storage` puis accepter le popup et utiliser `/storage/emulated/0/Web+`. Modèle robuste : `mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/NOM_FICHIER https://raw.githubusercontent.com/{OWNER}/{REPO}/{HASH}/livrables/NOM_FICHIER; ls -lh /storage/emulated/0/Web+/NOM_FICHIER`. `-fL` arrête les erreurs HTTP, `--retry` retente, `-C -` reprend un téléchargement partiel. Si le shell affiche `>` : Ctrl+C puis recoller la ligne entière. Ne partager que `{HASH}` obtenu par `git rev-parse HEAD` **après** commit/push et vérifié comme contenant le fichier. Pour plusieurs fichiers, une ligne par fichier ; si un fichier fait moins de 100 ko, le supprimer avant reprise.

---

## §G. LES 5 STYLES CANONIQUES + LIBERTÉ D'INNOVATION (v5.1)

> L'artiste choisit 1 style (ou hybride) au §B.Q1. L'IA dispose d'**une liberté d'innovation encadrée** :
> variantes de textures/lumières/composition AUTOUR du style choisi (jamais contre lui),
> proposition d'un 6ᵉ style moodboard (1 ancre) si l'artiste est curieux, mélange de 2 styles
> autorisé UNIQUEMENT sur pont/outro (décrescendo). Le BLOC HÉROS et les règles §D/H ne changent JAMAIS.

**S1 DARK LIGHTNING** (titres sombres, combat) — suffixe : `deep blue-black night, warm amber backlight, subtle electric cyan rim light, wet asphalt reflections, atmospheric haze, crushed blacks with cyan highlights, moody anime-seinen cinematic grading, 35mm film grain`
**S2 GOLDEN SUNSET** (amour, espoir, ponts calmes) — suffixe : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading`
**S3 NEON AFRO-FUTURISM** (fête, urbain, fierté) — suffixe : `vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain`
**S4 INK & FIRE** (deuil, introspection, acoustique) — suffixe : `minimal charcoal-black background, sumi-e ink brush strokes swirling like smoke, floating warm ember sparks, high contrast monochrome with a single amber accent, paper texture grain, elegant japanese ink painting cinematic grading`
**S5 RETRO FILM 70s** (nostalgie, storytelling) — suffixe : `faded Kodak film palette, warm halation around highlights, heavy 35mm grain, soft light leaks at frame edges, slightly desaturated teal shadows and cream highlights, vintage anamorphic bokeh, 1970s documentary film grading`

**RÈGLES DE BEAUTÉ UNIVERSELLES (tous styles) :** UN seul point focal lumineux · règle des tiers pour le héros · rim light systématique · palette ≤ 3 couleurs dominantes · profondeur (bokeh/brume/atmosphère) · grain film léger toujours · lisible en vignette 2 s (hook covers/intro/endcard = composition simple symétrique) · héros soigné mais FIDÈLE (peau propre, jamais embelli/musclé sans demande) · décrescendo lumineux sur outro · fond endcard sombre épuré.

## §H. SAFE ZONES PLATEFORMES (v5.1 — TikTok / Reels / Shorts / YouTube)

> Problème réel constaté : la **barre de recherche + tabs** (haut), le **rail de boutons** (droite : like/comment/share), la **caption + bottom nav (+ bouton ➕)** (bas) masquent badge, paroles et CTA. Règles OBLIGATOIRES 9:16 (1080×1920) :

| Zone | Pixels | Interdit d'y mettre |
|---|---|---|
| Bande haute (recherche/tabs) | y 0 → 144 | badge, titres, CTA |
| Rail droit (boutons action) | x ≥ 910 ET y 960 → 1690 | paroles, icônes CTA, partage |
| Bande basse (caption + nav + ➕) | y ≥ 1574 | paroles, CTA, crédits endcard |

**Positions canoniques v5.1 (9:16) :** badge `y=150` centré (sous la barre) · rangée CTA 72 px `y=232` (sous le badge, visible 2 s) · titres hook/intro `y=330` · **paroles : top sprite `H−520`** (glyphs finissent ≤ 1560, au-dessus de la caption) largeur max **880 px** centrée (bord droit ≤ 910) · **scrim dégradé sombre** (alpha max ~110, bande y 1330→1650) derrière les paroles pour lisibilité sur toute UI/image · icône partage 150 px à `0,40×H` centrée (hors rail) · endcard : titre cursive y≈260 + crédits centrés dans [560 ; 1400].
**16:9 YouTube :** bande basse contrôles y ≥ H−120 vide · paroles base H−170 max 1640 px · titre intro haut-gauche sous y=140 · endcard cx=0,38×W.
**Vérif ajoutée §D.10 :** frame test avec overlay UI TikTok (template `work/overlay_tiktok.png` si fourni) → aucun élément clé masqué.

## §F. NOMMAGE & RÉFÉRENCES

`assets/raw/{portrait|landscape}/s{slot:02d}_{motclé}.png` (s00 intro, s{N+1} endcard) · `work/fonds_{format}/f{slot:02d}.jpg` · `livrables/{Titre}_9x16_v{N}.mp4`, `{Titre}_16x9_YT_v{N}.mp4`, `cover_{titre}_9x16.jpg`, `cover_{titre}_1080x1080.jpg`, `cover_{titre}_universelle_3000.jpg`, `cover_{titre}_16x9.jpg`, `{Titre}_master_320k.mp3` · `PROMPTS_IMAGES_{Titre}.md` (catalogue prompts séparés) · `<Titre>.lrc`.

## 📜 Historique
- **v5.3** — cover universelle carrée + variantes 9:16/16:9, logos sociaux post-produits optionnels, MP3 320 kb/s propre avec APIC/USLT, et solutions validées `imageio-ffmpeg`/durée via FFmpeg/ASS wrap/Termux reprenable.
- **v5.1** — §G **5 styles canoniques + liberté d'innovation IA** + règles de beauté universelles · §H **SAFE ZONES plateformes** (barre recherche haut, rail droit, caption/nav bas) avec positions canoniques v5.1 (badge y150, CTA y232, titres y330, paroles top H−520 + scrim) · §B.Q1 et §D.3 mis à jour · production de référence re-rendue en `..._9x16_v3_safezones.mp4`.
- **v5.0** — UNIVERSALISATION : §A analyse auto tout format · §B questionnaire unique 8 questions avec défauts (« direct/confiance » = défauts) · §E gabarits à trous pour tout morceau · hérite v4.9.1.
- v4.x : productions & leçons archivées (`PROMPT_UNIVERSEL_v4.8.2.md`, `PROMPT_UNIVERSEL_v4.9.md`).

**Signature :** « Wolof TechStein beat wê ! » ⚡

# 🎬 PROMPT UNIVERSEL — v5.3.1 (addendum *Le goût bon de la vie*)

**Hérite 100 % de `PROMPT_UNIVERSEL_v5.3_FINAL.md`.** Ajouts = leçons 2026-09-25. Priorité : ces lignes > v5.3 en cas de conflit.

## §0.7 Push Git après CHAQUE étape (anti-reset)

La sandbox peut revenir à un vieux HEAD. **Commit + `git push origin arena/<id>-<slug>` après : salve images, scripts, clip, covers, master MP3.** Ne jamais laisser des livrables uniquement en local.

## §0.8 Visage = photos lockées

Si l’artiste dit « sans modifier mon visage / uniquement ces photos » : **interdire** de régénérer un autre visage. Salve « lock » = 10 max, **chaque génération prend l’original en `images=`**. Variantes = lumière / grade / pose légère, pas une autre personne.

## §0.9 Paroles hors visage

Si le héros est en portrait (tête au centre) : **ne pas coller les vers sur H/2**. Zone paroles = hoodie / bas de frame, **au-dessus de la caption TikTok (y ≤ 1560)**. Scrim bas seulement.

## §0.10 Mot-à-mot (si demandé « gros puis petit »)

Chaque mot du vers : **attaque scale ~1,5 → tient ~1,2**, puis passe en **trail petit** quand le mot suivant arrive. Mot courant DejaVu Bold or/crème, glow. Pas de vague colonne (trop lente) dans ce mode.

## §0.11 Covers sans faux visage

Si cover IA + « pas mon visage généré » : still-life / décor S2, **titre GreatVibes en post**, bande Bénin, badge DSKY✓. Carré 1080 APIC + 9:16.

## Livraison type

Clip 9:16 + master 320k (APIC/USLT) + covers + caption 4 hashtags + ce prompt + commandes Termux **une ligne** au HASH du commit de livraison.
