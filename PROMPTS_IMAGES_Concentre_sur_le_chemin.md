# Catalogue des prompts — Concentré sur le chemin

## Autorisation et budget

Le questionnaire du 2026-09-28 autorise explicitement **les photos du dossier `Samu`** comme références pour ce clip. Choix validés : animé sombre, gros texte gras hybride, badge `Dsky` + drapeau vectoriel Bénin animé par vers, bandeau Bénin fin, pack complet. L'ancre reste à valider.

Budget : **cinq portraits + cinq paysages**, intro/endcard/covers réutilisent les fonds. La génération ci-dessous occupe le slot portrait s01 si elle est acceptée. Aucun autre fond ne doit être généré avant son approbation.

## Références originales utilisées pour l'ancre

1. `Samu/Snapchat-1835992965.jpg` — face avec lunettes, proportions et traits.
2. `Samu/Snapchat-1275781156.jpg` — profil avec lunettes, nez, crâne, coupe.
3. `Samu/Snapchat-959878741.jpg` — face sans lunettes, lèvres et forme du visage.

Les références servent à l'identité, pas à recopier le selfie, les vêtements neufs, le décor ou les autocollants. Les lunettes rectangulaires des références sont conservées dans la proposition ; à vérifier lors de la validation de l'ancre.

## Bloc héros invariant

> The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

## s01 portrait — Tête lourde — PROMPT COMPLET (avant lancement)

**Sortie IA brute :** `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`.

**images= :** les trois originaux ci-dessus, dans cet ordre.

### 1 — CADRAGE

True vertical 9:16 portrait composition, very tall cinematic frame, intended final canvas 1080 by 1920. A single illustrated scene, not a collage or poster. Keep the seated figure, entire head, both hands, elbows and shoes inside the frame with generous side margins for safe crop. The top 15 percent is quiet dark wall and haze. Place the head and both hands in the upper third, approximately 18 to 36 percent of the canvas height, so the face is clearly ABOVE the center of the frame. The central 40 to 65 percent should mainly show subdued clothing and softly blurred room, reserved for later compositing.

### 2 — SUJET / ÉMOTION

A tired but determined young independent musician sits on a worn stool inside a cramped smoking room that doubles as his makeshift recording studio, pressing both hands onto his head while he gathers his thoughts. A single cigarette between the fingers of the hand beside his temple releases a delicate curling trail of smoke. An old microphone and circular pop filter stand at the far side, an aging mixing desk, two small speakers, worn acoustic foam, scuffed plaster and a few cables establish a humble real music studio. Low-to-moderate light intensity, intimate introspective mood, dignity amid hardship. One amber practical lamp is the luminous focal point; blue haze provides depth. No other person.

### 3 — HÉROS

The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

### 4 — PLAN

Medium-wide seated full-figure view, almost frontal with a slight three-quarter turn, eye-level perspective without selfie distortion. Face clearly recognizable and relatively large in the upper third, tired focused eyes visible through clear glasses. Keep the palms touching the head, do not put the cigarette in his mouth. The entire pose is readable. Equipment stays at the edges and behind him, never across the face.

### 5 — STYLE / LUMIÈRE

High-quality hand-drawn semi-realistic anime-seinen illustration, confident fine ink outlines, detailed but restrained cel shading, mature believable human anatomy, likeness guided by the real photo references rather than a generic anime hero. Deep blue-black night shadows, warm amber backlight, subtle electric cyan rim light, soft atmospheric cigarette haze, subtle 35mm film grain. Limited charcoal-blue, warm brown skin and amber palette. Preserve facial detail in the shadows; not photorealistic, not glossy 3D, not a caricature. The setting is indoors, with restrained diffuse reflections.

### 6 — ZONES DE COMPOSITION

Keep a quiet dark upper area for later UI compositing. Leave a low-detail soft middle region over the dark jacket and room for large centered lyrics added later, without placing anything over his face. Calm unobstructed bottom edge for post-production. Draw only the illustrated scene; all typography and national colors will be added separately. Safe inner composition: face, hands and elbows remain inside the central 75 percent of image width.

### 7 — INTERDITS / CONTRÔLES

No text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage, no labels on equipment, no emblems, no flag, no artist badge, no copied heart stickers or emoji from the photos. No extra people, no extra arms or fingers, no cropped face, no cut-off hands, no hidden cigarette hand, no out-of-frame limbs. Do not reproduce the reference clothing or background. Do not replace him with a bearded or muscular fictional hero.

## Post-production séparée (pas demandée au générateur)

- Mise au ratio finale sans étirer la personne ; vérifier qu'aucune main n'est coupée.
- Bandeau Bénin **54 px** pleine largeur, y=1866→1920 sur portrait 1080×1920 ; géométrie vectorielle exacte et couleurs #008751 / #FCD116 / #E8112D.
- Badge UI `Dsky` + vrai drapeau vectoriel en calque indépendant, opacité ≤75 %, fondu 0,4 s à chaque début et fin de vers. **Aucun badge permanent sur les fonds destinés au clip.**
- Texte gras, très grand, complet et centré ; apparition mot à mot, vague simultanée, mot actif or/crème. Les temps de mots de la maquette sont provisoires jusqu'à validation vocale.
- Une maquette avec un vrai passage audio sera présentée ; aucun lancement des neuf autres générations avant approbation.

## Neuf prompts restants

**Non lancés et volontairement non finalisés avant validation de l'ancre.** Ils reprendront le bloc héros strictement inchangé, les originaux autorisés dans `images=`, et l'ancre approuvée en référence de style, avec cadrages adaptés au format. Seuls les plans/lumières/éléments secondaires du storyboard changeront ; la pose, les vêtements et le studio resteront cohérents.
