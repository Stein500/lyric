# Catalogue des prompts — Concentré sur le chemin

## Autorisation et budget

Le questionnaire du 2026-09-28 autorise explicitement **les photos du dossier `Samu`** comme références pour ce clip. Choix validés : animé sombre, gros texte gras hybride, badge `Dsky` + drapeau vectoriel Bénin animé par vers, bandeau Bénin fin, pack complet. Ancre approuvée par l’artiste : « Oui continue... » (2026-09-28).

Budget : **cinq portraits + cinq paysages**, intro/endcard/covers réutilisent les fonds. L’ancre approuvée occupe le slot portrait s01. La salve historique contenait uniquement les neuf fonds restants. Les dix compositions courantes (paysages révision 2) ont depuis été approuvées : « Oui je valide !! ». Aucune nouvelle génération pour les clips ou les covers.

## Références originales utilisées pour l'ancre

1. `Samu/Snapchat-1835992965.jpg` — face avec lunettes, proportions et traits.
2. `Samu/Snapchat-1275781156.jpg` — profil avec lunettes, nez, crâne, coupe.
3. `Samu/Snapchat-959878741.jpg` — face sans lunettes, lèvres et forme du visage.

Les références servent à l'identité, pas à recopier le selfie, les vêtements neufs, le décor ou les autocollants. Les lunettes rectangulaires sont conservées et approuvées avec l’ancre.

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

## Salve 02 — neuf prompts complets, écrits avant lancement

Ancre approuvée. Quatre portraits et cinq paysages ; **neuf appels IA au total dans cette salve**. Les trois originaux Samu restent les références d’identité et le quatrième visuel est l’ancre approuvée, sans texte ni badge. La planche contact devra être validée avant le rendu final.

### s02 portrait — Dans le bruit

Sortie : `assets/raw/concentre_sur_le_chemin/portrait/s02_dans_le_bruit.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True vertical 9:16 composition for 1080 by 1920. A single illustrated scene. Keep the seated figure inside generous margins; keep the entire head and both hands high in the upper third, above 36 percent of image height. Top 15 percent is quiet dark wall. The face must be above the middle, not at the center. The two forearms, hands and feet stay inside the central 75 percent width for crop safety.

2 — SUBJECT AND EMOTION. The same musician gathers his thoughts amid the quiet clutter of his humble recording studio smoking room. The aging mixing console is more prominent in the foreground at the left edge; an old speaker and a hanging microphone recede through blue haze. Dim-to-moderate amber light, a subdued cyan rim, worn walls and repaired furniture. Same stool and room as the approved anchor, a distinctly different camera angle.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Three-quarter side view from the console side, medium-wide seated full figure. His face remains turned enough toward the camera to recognize him; neither hand hides his eyes or lips.

5 — STYLE AND LIGHT. Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.

6 — COMPOSITING AREAS. Quiet upper area for UI later. Low-detail dark jacket and room across the middle 40 to 65 percent for large centered lyrics added in post; the face stays clearly above this region. Calm bottom 10 percent and empty floor beyond the shoes. All graphics and national colors will be added later, not generated.

7 — EXCLUSIONS. No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.

### s03 portrait — Tenir le cap

Sortie : `assets/raw/concentre_sur_le_chemin/portrait/s03_tenir_le_cap.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True vertical 9:16 composition for 1080 by 1920. A single illustrated scene. Keep the seated figure inside generous margins; keep the entire head and both hands high in the upper third, above 36 percent of image height. Top 15 percent is quiet dark wall. The face must be above the middle, not at the center. The two forearms, hands and feet stay inside the central 75 percent width for crop safety.

2 — SUBJECT AND EMOTION. The same musician remains seated with his two hands on his head, lifting his determined gaze toward the viewer as if refusing to give up. Stronger warm amber backlight cuts through blue cigarette haze; a subtle cyan edge lights the worn jacket. Same humble studio smoking room, old microphone and pop filter at the far side, speakers softly blurred behind him. Full chorus intensity, dignified and focused rather than glamorous.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Strong almost frontal medium-wide full seated figure, clear expressive face and two hands, shoulders open. The camera is a little closer than the anchor, but the head, hands, knees and shoes stay fully inside generous margins.

5 — STYLE AND LIGHT. Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.

6 — COMPOSITING AREAS. Quiet upper area for UI later. Low-detail dark jacket and room across the middle 40 to 65 percent for large centered lyrics added in post; the face stays clearly above this region. Calm bottom 10 percent and empty floor beyond the shoes. All graphics and national colors will be added later, not generated.

7 — EXCLUSIONS. No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.

### s04 portrait — Patience

Sortie : `assets/raw/concentre_sur_le_chemin/portrait/s04_patience.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True vertical 9:16 composition for 1080 by 1920. A single illustrated scene. Keep the seated figure inside generous margins; keep the entire head and both hands high in the upper third, above 36 percent of image height. Top 15 percent is quiet dark wall. The face must be above the middle, not at the center. The two forearms, hands and feet stay inside the central 75 percent width for crop safety.

2 — SUBJECT AND EMOTION. The same musician breathes quietly and gathers patience in his modest smoking room recording studio, still with both hands on his head and the cigarette held at his temple. Soft warm amber lamplight becomes dominant, thinner blue haze and a very faint cyan rim. Same old console, microphone and worn acoustic panels in soft focus. Gentle bridge mood, low-to-moderate intensity, warm human vulnerability, no location or clothing change.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Intimate three-quarter seated view, natural perspective, head and hands completely visible, full seated body within the frame. The expression softens but the eyes remain recognizable behind the same glasses.

5 — STYLE AND LIGHT. Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.

6 — COMPOSITING AREAS. Quiet upper area for UI later. Low-detail dark jacket and room across the middle 40 to 65 percent for large centered lyrics added in post; the face stays clearly above this region. Calm bottom 10 percent and empty floor beyond the shoes. All graphics and national colors will be added later, not generated.

7 — EXCLUSIONS. No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.

### s05 portrait — Encore debout

Sortie : `assets/raw/concentre_sur_le_chemin/portrait/s05_encore_debout.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True vertical 9:16 composition for 1080 by 1920. A single illustrated scene. Keep the seated figure inside generous margins; keep the entire head and both hands high in the upper third, above 36 percent of image height. Top 15 percent is quiet dark wall. The face must be above the middle, not at the center. The two forearms, hands and feet stay inside the central 75 percent width for crop safety.

2 — SUBJECT AND EMOTION. The same musician sits in the studio smoking room after the final take, both hands still on his head and a small trail of smoke rising from the cigarette between his fingers. The amber lamp has dimmed, the console and microphone recede into deep blue shadows, the floor is quiet and empty. Same room and outfit, calm dark outro atmosphere, dim intensity, one soft luminous accent only. Reserve a calm central area for the later endcard without drawing any graphics.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Wider environmental seated full-figure shot, the studio feels quiet and spacious around him. Keep the face recognizable and entirely in frame, without turning him away from the camera.

5 — STYLE AND LIGHT. Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.

6 — COMPOSITING AREAS. Quiet upper area for UI later. Low-detail dark jacket and room across the middle 40 to 65 percent for large centered lyrics added in post; the face stays clearly above this region. Calm bottom 10 percent and empty floor beyond the shoes. All graphics and national colors will be added later, not generated.

7 — EXCLUSIONS. No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.

### s01 landscape — Tête lourde

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s01_tete_lourde.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 landscape composition for 1920 by 1080, wide YouTube framing, not a cropped portrait and not a collage. Place the seated musician toward the LEFT THIRD, his face and both hands in the UPPER LEFT: head center around x=430, y=240; the entire face must end above y=365. Keep the full seated body, elbows and shoes inside the frame with generous margins. Show the studio extending naturally to the right.

2 — SUBJECT AND EMOTION. A tired but determined musician seated on the same worn stool in the same cramped smoking room recording studio. Old microphone and pop filter at one side, aging mixing desk and two speakers, worn acoustic foam, scuffed plaster, a few cables. A single amber lamp illuminates the room through blue haze, low-to-moderate intensity. This is the wide-format counterpart of the approved anchor, not a different place.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Almost frontal seated full-figure view, slight three-quarter angle, natural eye-level perspective, eyes visible through clear glasses.

5 — STYLE AND LIGHT. Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.

6 — COMPOSITING AREAS. Leave a low-detail dark horizontal middle band around y=430 to y=700 for large centered lyrics added in post, across the room and clothing, never the face. Top center is quiet for a compact UI badge later. Keep the bottom 10 percent calm, with shoes fully above the lower edge. All graphics and national colors will be added later, not generated.

7 — EXCLUSIONS. No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.

### s02 landscape — Dans le bruit

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s02_dans_le_bruit.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 landscape composition for 1920 by 1080, wide YouTube framing, not a cropped portrait and not a collage. Place the seated musician toward the LEFT THIRD, his face and both hands in the UPPER LEFT: head center around x=430, y=240; the entire face must end above y=365. Keep the full seated body, elbows and shoes inside the frame with generous margins. Show the studio extending naturally to the right.

2 — SUBJECT AND EMOTION. The same musician gathers his thoughts amid the quiet clutter of his humble recording studio smoking room. The aging mixing console is more prominent in the foreground at the left edge; an old speaker and a hanging microphone recede through blue haze. Dim-to-moderate amber light, a subdued cyan rim, worn walls and repaired furniture. Same stool and room as the approved anchor, a distinctly different camera angle.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Three-quarter side view from the console side, medium-wide seated full figure. His face remains turned enough toward the camera to recognize him; neither hand hides his eyes or lips.

5 — STYLE AND LIGHT. Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.

6 — COMPOSITING AREAS. Leave a low-detail dark horizontal middle band around y=430 to y=700 for large centered lyrics added in post, across the room and clothing, never the face. Top center is quiet for a compact UI badge later. Keep the bottom 10 percent calm, with shoes fully above the lower edge. All graphics and national colors will be added later, not generated.

7 — EXCLUSIONS. No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.

### s03 landscape — Tenir le cap

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s03_tenir_le_cap.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 landscape composition for 1920 by 1080, wide YouTube framing, not a cropped portrait and not a collage. Place the seated musician toward the LEFT THIRD, his face and both hands in the UPPER LEFT: head center around x=430, y=240; the entire face must end above y=365. Keep the full seated body, elbows and shoes inside the frame with generous margins. Show the studio extending naturally to the right.

2 — SUBJECT AND EMOTION. The same musician remains seated with his two hands on his head, lifting his determined gaze toward the viewer as if refusing to give up. Stronger warm amber backlight cuts through blue cigarette haze; a subtle cyan edge lights the worn jacket. Same humble studio smoking room, old microphone and pop filter at the far side, speakers softly blurred behind him. Full chorus intensity, dignified and focused rather than glamorous.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Strong almost frontal medium-wide full seated figure, clear expressive face and two hands, shoulders open. The camera is a little closer than the anchor, but the head, hands, knees and shoes stay fully inside generous margins.

5 — STYLE AND LIGHT. Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.

6 — COMPOSITING AREAS. Leave a low-detail dark horizontal middle band around y=430 to y=700 for large centered lyrics added in post, across the room and clothing, never the face. Top center is quiet for a compact UI badge later. Keep the bottom 10 percent calm, with shoes fully above the lower edge. All graphics and national colors will be added later, not generated.

7 — EXCLUSIONS. No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.

### s04 landscape — Patience

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s04_patience.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 landscape composition for 1920 by 1080, wide YouTube framing, not a cropped portrait and not a collage. Place the seated musician toward the LEFT THIRD, his face and both hands in the UPPER LEFT: head center around x=430, y=240; the entire face must end above y=365. Keep the full seated body, elbows and shoes inside the frame with generous margins. Show the studio extending naturally to the right.

2 — SUBJECT AND EMOTION. The same musician breathes quietly and gathers patience in his modest smoking room recording studio, still with both hands on his head and the cigarette held at his temple. Soft warm amber lamplight becomes dominant, thinner blue haze and a very faint cyan rim. Same old console, microphone and worn acoustic panels in soft focus. Gentle bridge mood, low-to-moderate intensity, warm human vulnerability, no location or clothing change.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Intimate three-quarter seated view, natural perspective, head and hands completely visible, full seated body within the frame. The expression softens but the eyes remain recognizable behind the same glasses.

5 — STYLE AND LIGHT. Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.

6 — COMPOSITING AREAS. Leave a low-detail dark horizontal middle band around y=430 to y=700 for large centered lyrics added in post, across the room and clothing, never the face. Top center is quiet for a compact UI badge later. Keep the bottom 10 percent calm, with shoes fully above the lower edge. All graphics and national colors will be added later, not generated.

7 — EXCLUSIONS. No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.

### s05 landscape — Encore debout

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s05_encore_debout.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 landscape composition for 1920 by 1080, wide YouTube framing, not a cropped portrait and not a collage. Place the seated musician toward the LEFT THIRD, his face and both hands in the UPPER LEFT: head center around x=430, y=240; the entire face must end above y=365. Keep the full seated body, elbows and shoes inside the frame with generous margins. Show the studio extending naturally to the right.

2 — SUBJECT AND EMOTION. The same musician sits in the studio smoking room after the final take, both hands still on his head and a small trail of smoke rising from the cigarette between his fingers. The amber lamp has dimmed, the console and microphone recede into deep blue shadows, the floor is quiet and empty. Same room and outfit, calm dark outro atmosphere, dim intensity, one soft luminous accent only. Reserve a calm central area for the later endcard without drawing any graphics.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Wider environmental seated full-figure shot, the studio feels quiet and spacious around him. Keep the face recognizable and entirely in frame, without turning him away from the camera.

5 — STYLE AND LIGHT. Match the approved fourth reference exactly: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, believable human anatomy, deep blue-black shadows, warm amber light, a subtle cyan rim, atmospheric cigarette haze, very fine restrained film grain. Keep the same recognizable face, glasses, patch placement and worn clothing as the approved anchor. Not photorealistic, not glossy 3D, not a generic anime hero.

6 — COMPOSITING AREAS. Leave a low-detail dark horizontal middle band around y=430 to y=700 for large centered lyrics added in post, across the room and clothing, never the face. Top center is quiet for a compact UI badge later. Keep the bottom 10 percent calm, with shoes fully above the lower edge. All graphics and national colors will be added later, not generated.

7 — EXCLUSIONS. No text, letters, numbers, logos, watermark, subtitles, borders, signage, labels, emblems, flags, artist badges or copied heart stickers. No extra people, limbs or fingers, no cropped face or hands. No new beard, muscles, luxury clothing or jewelry. The cigarette is between the fingers, not in the mouth. Do not change the identity, outfit or two-hands-on-head pose. All hands, wrists and feet must be inside the frame.

## Correction de s05 paysage — dixième et dernier appel du tour

Le premier essai présente un cadrage trop serré et des aplats parasites. Il est conservé uniquement dans le cache ignoré. Reformulation positive : ne plus nommer les objets graphiques indésirables ni demander une bande centrale au modèle. Cette correction remplace s05 ; **aucune sixième scène**.

1 — FRAMING. True horizontal 16:9 wide cinematic illustration. Full room view from a slightly distant camera. Place the seated man in the left third at a modest size: his entire seated figure takes about 70 percent of the image height. His shoes and the stool legs are completely visible, with a generous area of natural floor below. Head and hands are in the upper left third; the right two thirds show the rest of the studio.

2 — SUBJECT. A quiet late-night smoking room that is also a humble home recording studio. One seated musician, an old microphone and circular pop filter, a worn mixing console, two old speakers, acoustic foam, scuffed plaster walls, a lamp with a small warm amber glow, floor cables. Soft blue cigarette haze recedes into the background. The lamp is dimmer than in the fourth reference; the mood is peaceful after a recording session.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Wide head-to-toe seated view from eye level, face turned toward the camera, both hands on top and sides of the head. Make him small enough to fit his whole body comfortably inside the image. The hands, elbows, knees, lower legs and shoes are all fully visible and connected naturally. Maintain his identity from the first three photos and the approved illustrated likeness from the fourth.

5 — STYLE. Exactly the drawing style of the approved fourth reference: hand-drawn semi-realistic anime-seinen, fine ink outlines, restrained cel shading, dark blue-black palette, soft amber illumination and very faint cyan rim, subtle film texture. Keep the approved clothing and same patch details. His face has the same natural proportions and glasses.

6 — ROOM. The studio has continuous, natural lighting across the walls, clothing, equipment and floor. The room extends smoothly behind the musician. Soft hazy shadows blend gradually and organically; the upper wall is simple and the floor has little clutter. This is a physical room observed by a camera.

7 — ANATOMY. One coherent illustrated room, one recognizable person, exactly two hands resting on his head, the cigarette held between fingers near the temple, both feet on the floor. Keep a generous breathing margin around the entire figure and show his shoes clearly.

## Reprise des paysages — 2026-09-29 — révision 2

Ancre approuvée : « Oui continue... ». La salve précédente a été récupérée depuis le commit `67525732617ae9b6acfb23243b43c8f3f999004c`, sans effacer des changements locaux. Les cinq portraits sont conservés. s03/s04 paysage étaient trop serrés ; les autres paysages présentaient des aplats ou prolongements de bords peu naturels. **Cinq corrections remplacent les cinq slots paysage, sans ajouter de scène.**

Reformulation positive après hallucination de lettrage/aplats : les nouveaux prompts ne nomment plus les objets graphiques indésirables et ne demandent plus de bande centrale. La lisibilité, le badge et le drapeau sont traités uniquement en post. Tous les prompts ci-dessous sont écrits avant lancement.

### s01_tete_lourde — paysage corrigé

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s01_tete_lourde.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 wide cinematic illustration. Observe a complete room from its doorway with a distant camera, showing the full seated man on the LEFT THIRD. Keep him modest in size: the entire seated figure, from the top of his hands to the soles of BOTH SHOES, occupies at most 62 percent of the image height. His head starts near 12 percent height and his shoes finish by 78 percent height. Leave a broad expanse of natural floor beneath his feet and ample air around both elbows. The right two thirds contain the rest of the studio. His face is in the upper left third, above the vertical middle.

2 — SUBJECT. A tired but determined independent musician sits on the same worn stool in his cramped smoking room recording studio. An old microphone and round pop filter stand beside him, an aging mixing desk and two small speakers recede to the right, worn acoustic foam and scuffed plaster complete the modest room. One amber lamp shines softly through blue cigarette haze. Low-to-moderate light, the same introspective mood and equipment as the approved fourth reference.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Wide environmental head-to-toe seated shot with a natural 35mm perspective. The whole stool, both knees, calves, ankles, shoe heels and shoe toes are visible with breathing room. The lower fifth of the picture is empty physical floor. Keep the head and the two hands clearly visible, the eyes unobstructed behind the glasses. Use the first three photographs only for identity and the fourth illustration for the approved likeness and drawing style. The figure must be much smaller within this wide frame than within the portrait reference.

5 — STYLE. Exactly the approved fourth reference drawing style: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, dark blue-black shadows, warm amber practical light, subtle cyan rim, light atmospheric smoke and restrained fine film texture. Retain the same glasses, natural facial proportions, patch positions and worn charcoal jacket with brown trousers. The whole composition is one continuous illustrated room.

6 — ROOM. Natural continuous illumination across all walls, furniture, clothing and floor. Shadows blend gradually in a physically coherent room, and surfaces have smooth uninterrupted shading. Simple unadorned upper walls and a quiet natural floor. All visible details belong to the physical studio. The space to the right is softly lit, uncluttered and atmospheric.

7 — ANATOMY. One recognizable person with exactly two arms and two anatomically plausible hands touching the top and sides of his head. One cigarette held between the fingers beside his temple, pointed away from his hair. Both feet stand on the floor, fully enclosed within the picture. Preserve the approved pose, face and body proportions; keep all extremities comfortably inside the frame.

### s02_dans_le_bruit — paysage corrigé

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s02_dans_le_bruit.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 wide cinematic illustration. Observe a complete room from its doorway with a distant camera, showing the full seated man on the LEFT THIRD. Keep him modest in size: the entire seated figure, from the top of his hands to the soles of BOTH SHOES, occupies at most 62 percent of the image height. His head starts near 12 percent height and his shoes finish by 78 percent height. Leave a broad expanse of natural floor beneath his feet and ample air around both elbows. The right two thirds contain the rest of the studio. His face is in the upper left third, above the vertical middle.

2 — SUBJECT. The same musician gathers his thoughts in the quiet clutter of his smoking room recording studio. View the room from the mixing-console side: the worn desk occupies the far left foreground, the musician sits behind it and a suspended microphone hangs to his right. A soft amber practical lamp and dim cyan side light reveal worn acoustic panels and cables against the wall. A distinct three-quarter camera angle, dim-to-moderate intensity, the same room and furniture as the fourth reference.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Wide environmental head-to-toe seated shot with a natural 35mm perspective. The whole stool, both knees, calves, ankles, shoe heels and shoe toes are visible with breathing room. The lower fifth of the picture is empty physical floor. Keep the head and the two hands clearly visible, the eyes unobstructed behind the glasses. Use the first three photographs only for identity and the fourth illustration for the approved likeness and drawing style. The figure must be much smaller within this wide frame than within the portrait reference.

5 — STYLE. Exactly the approved fourth reference drawing style: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, dark blue-black shadows, warm amber practical light, subtle cyan rim, light atmospheric smoke and restrained fine film texture. Retain the same glasses, natural facial proportions, patch positions and worn charcoal jacket with brown trousers. The whole composition is one continuous illustrated room.

6 — ROOM. Natural continuous illumination across all walls, furniture, clothing and floor. Shadows blend gradually in a physically coherent room, and surfaces have smooth uninterrupted shading. Simple unadorned upper walls and a quiet natural floor. All visible details belong to the physical studio. The space to the right is softly lit, uncluttered and atmospheric.

7 — ANATOMY. One recognizable person with exactly two arms and two anatomically plausible hands touching the top and sides of his head. One cigarette held between the fingers beside his temple, pointed away from his hair. Both feet stand on the floor, fully enclosed within the picture. Preserve the approved pose, face and body proportions; keep all extremities comfortably inside the frame.

### s03_tenir_le_cap — paysage corrigé

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s03_tenir_le_cap.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 wide cinematic illustration. Observe a complete room from its doorway with a distant camera, showing the full seated man on the LEFT THIRD. Keep him modest in size: the entire seated figure, from the top of his hands to the soles of BOTH SHOES, occupies at most 62 percent of the image height. His head starts near 12 percent height and his shoes finish by 78 percent height. Leave a broad expanse of natural floor beneath his feet and ample air around both elbows. The right two thirds contain the rest of the studio. His face is in the upper left third, above the vertical middle.

2 — SUBJECT. The same musician sits determined and focused in his humble recording studio smoking room, keeping both hands on his head while looking toward the camera. Stronger amber backlight shines through blue cigarette haze and a gentle cyan edge lights his worn jacket. An old microphone and pop filter stand at the far right; speakers and an aging mixing desk recede naturally in the room. Full chorus intensity, one warm focal light, dignity and resolve rather than glamour.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Wide environmental head-to-toe seated shot with a natural 35mm perspective. The whole stool, both knees, calves, ankles, shoe heels and shoe toes are visible with breathing room. The lower fifth of the picture is empty physical floor. Keep the head and the two hands clearly visible, the eyes unobstructed behind the glasses. Use the first three photographs only for identity and the fourth illustration for the approved likeness and drawing style. The figure must be much smaller within this wide frame than within the portrait reference.

5 — STYLE. Exactly the approved fourth reference drawing style: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, dark blue-black shadows, warm amber practical light, subtle cyan rim, light atmospheric smoke and restrained fine film texture. Retain the same glasses, natural facial proportions, patch positions and worn charcoal jacket with brown trousers. The whole composition is one continuous illustrated room.

6 — ROOM. Natural continuous illumination across all walls, furniture, clothing and floor. Shadows blend gradually in a physically coherent room, and surfaces have smooth uninterrupted shading. Simple unadorned upper walls and a quiet natural floor. All visible details belong to the physical studio. The space to the right is softly lit, uncluttered and atmospheric.

7 — ANATOMY. One recognizable person with exactly two arms and two anatomically plausible hands touching the top and sides of his head. One cigarette held between the fingers beside his temple, pointed away from his hair. Both feet stand on the floor, fully enclosed within the picture. Preserve the approved pose, face and body proportions; keep all extremities comfortably inside the frame.

### s04_patience — paysage corrigé

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s04_patience.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 wide cinematic illustration. Observe a complete room from its doorway with a distant camera, showing the full seated man on the LEFT THIRD. Keep him modest in size: the entire seated figure, from the top of his hands to the soles of BOTH SHOES, occupies at most 62 percent of the image height. His head starts near 12 percent height and his shoes finish by 78 percent height. Leave a broad expanse of natural floor beneath his feet and ample air around both elbows. The right two thirds contain the rest of the studio. His face is in the upper left third, above the vertical middle.

2 — SUBJECT. The same musician pauses quietly in his humble studio smoking room, with both hands resting on his head and the cigarette between his fingers. Softer warm amber lamplight dominates, the blue haze is thin and the cyan rim very faint. A worn mixing desk, microphone and acoustic panels sit quietly behind him. A gentle three-quarter view and a calmer expression convey patience; keep his recognizable face, glasses and original proportions. The mood is warm and vulnerable, with low-to-moderate light.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Wide environmental head-to-toe seated shot with a natural 35mm perspective. The whole stool, both knees, calves, ankles, shoe heels and shoe toes are visible with breathing room. The lower fifth of the picture is empty physical floor. Keep the head and the two hands clearly visible, the eyes unobstructed behind the glasses. Use the first three photographs only for identity and the fourth illustration for the approved likeness and drawing style. The figure must be much smaller within this wide frame than within the portrait reference.

5 — STYLE. Exactly the approved fourth reference drawing style: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, dark blue-black shadows, warm amber practical light, subtle cyan rim, light atmospheric smoke and restrained fine film texture. Retain the same glasses, natural facial proportions, patch positions and worn charcoal jacket with brown trousers. The whole composition is one continuous illustrated room.

6 — ROOM. Natural continuous illumination across all walls, furniture, clothing and floor. Shadows blend gradually in a physically coherent room, and surfaces have smooth uninterrupted shading. Simple unadorned upper walls and a quiet natural floor. All visible details belong to the physical studio. The space to the right is softly lit, uncluttered and atmospheric.

7 — ANATOMY. One recognizable person with exactly two arms and two anatomically plausible hands touching the top and sides of his head. One cigarette held between the fingers beside his temple, pointed away from his hair. Both feet stand on the floor, fully enclosed within the picture. Preserve the approved pose, face and body proportions; keep all extremities comfortably inside the frame.

### s05_encore_debout — paysage corrigé

Sortie : `assets/raw/concentre_sur_le_chemin/landscape/s05_encore_debout.png`.

Références : `Samu/Snapchat-1835992965.jpg` · `Samu/Snapchat-1275781156.jpg` · `Samu/Snapchat-959878741.jpg` · `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png`

1 — FRAMING. True horizontal 16:9 wide cinematic illustration. Observe a complete room from its doorway with a distant camera, showing the full seated man on the LEFT THIRD. Keep him modest in size: the entire seated figure, from the top of his hands to the soles of BOTH SHOES, occupies at most 62 percent of the image height. His head starts near 12 percent height and his shoes finish by 78 percent height. Leave a broad expanse of natural floor beneath his feet and ample air around both elbows. The right two thirds contain the rest of the studio. His face is in the upper left third, above the vertical middle.

2 — SUBJECT. The same musician remains seated in the recording studio smoking room after the final take. Both hands are still on his head, and a fine smoke trail rises from the cigarette beside his temple. The amber lamp is dim, the mixing desk and old microphone recede into deep blue shadows and the floor is quiet and uncluttered. One soft warm accent, calm darkness, the same worn furniture and clothing, a contemplative ending rather than a new location.

3 — HERO. The same young adult man depicted in the three authorized reference photographs, recognizable faithful facial likeness, natural slim-to-average build, medium-dark brown skin, softly oval face with a natural rounded jaw, the same broad nose and full lips as the references, short dense black naturally textured hair with a softly squared top and shorter sides, very minimal facial hair and clean cheeks, rectangular dark-rimmed clear-lens glasses matching the first two references. Preserve his real facial proportions and body, no beautification, no muscular redesign, no invented thick beard. He wears an old faded charcoal hooded zip jacket with a broken zipper, frayed cuffs and visibly hand-stitched patches, a plain worn gray tee underneath, faded patched brown trousers and battered plain shoes; modest impoverished clothing without luxury accessories. His two hands rest on the top and sides of his head, elbows open; one plain cigarette is held between the index and middle fingers of his right hand beside his temple, its ember pointing safely away from his hair. The face remains visible between his forearms. Exactly two anatomically plausible hands, all fingers and both wrists correctly connected to the arms.

4 — SHOT. Wide environmental head-to-toe seated shot with a natural 35mm perspective. The whole stool, both knees, calves, ankles, shoe heels and shoe toes are visible with breathing room. The lower fifth of the picture is empty physical floor. Keep the head and the two hands clearly visible, the eyes unobstructed behind the glasses. Use the first three photographs only for identity and the fourth illustration for the approved likeness and drawing style. The figure must be much smaller within this wide frame than within the portrait reference.

5 — STYLE. Exactly the approved fourth reference drawing style: hand-drawn semi-realistic anime-seinen, crisp fine ink outlines, restrained detailed cel shading, dark blue-black shadows, warm amber practical light, subtle cyan rim, light atmospheric smoke and restrained fine film texture. Retain the same glasses, natural facial proportions, patch positions and worn charcoal jacket with brown trousers. The whole composition is one continuous illustrated room.

6 — ROOM. Natural continuous illumination across all walls, furniture, clothing and floor. Shadows blend gradually in a physically coherent room, and surfaces have smooth uninterrupted shading. Simple unadorned upper walls and a quiet natural floor. All visible details belong to the physical studio. The space to the right is softly lit, uncluttered and atmospheric.

7 — ANATOMY. One recognizable person with exactly two arms and two anatomically plausible hands touching the top and sides of his head. One cigarette held between the fingers beside his temple, pointed away from his hair. Both feet stand on the floor, fully enclosed within the picture. Preserve the approved pose, face and body proportions; keep all extremities comfortably inside the frame.

## État après la reprise du 2026-09-29

Cinq appels de correction effectués, un par paysage ; tous les slots ont été remplacés sans nouvelle scène. Les cinq portraits de la première salve sont conservés. La planche v2 et le ZIP contiennent exactement dix images.

- Nettoyage local du plafond de s02 portrait (lettrage parasite).
- Nettoyage local du plafond de s03 paysage (autocollants recopiés des références) et de trois libellés d’appareil ; aucun pixel du personnage modifié.
- Recadrage portrait hérité de l’ancre ; paysage relevé de 80 px pour protéger les chaussures du bandeau, avec prolongement du seul sol en bas. Pas de bordures latérales ajoutées.
- Le bandeau est dessiné en post. **Badge non intégré** aux fonds, car il doit apparaître/disparaître à chaque vers.
- Géométrie, tailles, checksums, archive et intégrité du personnage dans les masques contrôlées ; **validation artiste de la série obtenue : « Oui je valide !! »**. Validation visuelle distincte du futur calage vocal. Mise à jour de statut : 2026-09-30.
