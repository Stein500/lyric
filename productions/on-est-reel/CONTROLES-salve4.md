# Contrôles — Salve 4 (`scene-22` retry + `scene-30` → `scene-38`)

Contrôle visuel effectué après génération sur la planche contact `CONTROLE-salve4.jpg` (tuiles de **500×896 px**, ≥ 480 px de large conformément à v5.9 §4), sur la planche de crops 1:1 pleine résolution du texte `CONTROLE-salve4-typo.jpg`, ET sur la planche de crops 1:1 des visages/portraits `CONTROLE-salve4-portraits.jpg`.

- **Bilan de la salve 4 (§10.2)** : **10 images demandées / 10 générées avec succès / 0 échec système / 9 sur 10 validées à 100 % au zoom 1:1** (`scene-32.png` a repris par erreur la ligne haute de l'image de référence `MAINTENANT ON SE RELÈVE` au-dessus de `JE VIENS DE LA STREET` → consignée en priorité n°1 de la Salve 5 finale avec prompt court §4).
- **Contrôle des portraits (`CONTROLE-salve4-portraits.jpg`)** : les visages des **trois présidents de l'AES** (`scene-30`, `scene-38`), de **Camara tombé au combat** (`scene-22`, `scene-33` en médaillon de laurier d'or, `scene-35`, `scene-37`), de **Thomas Sankara**, **Patrice Lumumba**, **Roi Béhanzin**, **Roi Bio Guéra** et de la **famille relevée** (`scene-36`) sont tous **nets, symétriques, bien proportionnés et sans déformation**.
- **Cumul après Salve 4** : **38 plans distincts présents dans `fonds/`** sur 46, couvrant **48 vers sur 57**.

---

## Grille de contrôle plan par plan (Salve 4)

| # | Fichier | Vers couverts | Texte peint lu au zoom 1:1 (`CONTROLE-salve4-typo.jpg`) | Orthographe & diacritiques | Portraits & visages (`CONTROLE-salve4-portraits.jpg`) | Verdict QC |
|---|---|---|---|---|---|---|
| 01 | `scene-22.png` *(retry §4)* | v-23 (`94,48 s`), v-44 (`166,64 s`) | `UN COMBATTANT,` / `UN SURVIVANT` / `PLUS FORT QUE TOI` | **OK** (`UN SURVIVANT` corrigé avec `U-N`) | **OK** (portraits nets de **Thomas Sankara** et **Camara**, sans déformation) | **Contrôlé OK** |
| 02 | `scene-30.png` | v-36 (`142,48 s`) | `J'AI BESOIN` / `DE LA JUSTICE` / `J'AI BESOIN DE MON DESTIN` | **OK** (toutes lettres nettes) | **OK** (**les 3 présidents de l'AES** — Goïta, Traoré, Tiani — visages nets, symétriques, sans déformation, sans drapeau) | **Contrôlé OK** |
| 03 | `scene-31.png` | v-37 (`145,68 s`) | `MES MOTS SONT` / `DES MISSILES` / `MES RIMES SONT DES BOUCLIERS` | **OK** (toutes lettres nettes) | **OK** (**Bio Guéra** et **Béhanzin** nets et symétriques) | **Contrôlé OK** |
| 04 | `scene-32.png` | v-38 (`148,71 s`) | `MAINTENANT ON SE RELÈVE` / `JE VIENS DE LA STREET` | **FAUTE** (reprise de la ligne de l'ancre au lieu de `J'SUIS NÉ POUR BRILLER`) | **OK** | **À régénérer (priorité n°1 salve 5, prompt court §4)** |
| 05 | `scene-33.png` | v-39 (`151,51 s`) | `ALORS FRAPPE-` / `MOI, J'AI TENU` / `J'AI SURVÉCU` | **OK** (`É` sur `SURVÉCU` net) | **OK** (médaillon d'or lauriers en hommage à **Camara tombé**, traits nets + colombe) | **Contrôlé OK** |
| 06 | `scene-34.png` | v-40 (`153,90 s`) | `JE SUIS LE FILS` / `DU SOLEIL` / `LA LUMIÈRE QUI A VAINCU` | **OK** (`È` sur `LUMIÈRE` net) | **OK** (soleil levant + portraits dorés nets et symétriques) | **Contrôlé OK** |
| 07 | `scene-35.png` | v-45 (`170,43 s`) | `LA NUIT` / `EST LONGUE` / `LES ÉTOILES SONT LOIN` | **OK** (`É` sur `ÉTOILES` net) | **OK** (portraits célestes de **Lumumba/Camara** et **Sankara** dans les étoiles) | **Contrôlé OK** |
| 08 | `scene-36.png` | v-46 (`173,36 s`) | `MAIS J'AI LA` / `FOI, J'AI LE SON` / `J'AI LES MIENS` | **OK** (toutes lettres nettes) | **OK** (**famille africaine relevée** souriante et unie + colombe d'or) | **Contrôlé OK** |
| 09 | `scene-37.png` | v-47 (`175,85 s`) | `ON TOMBE,` / `ON SE RELÈVE` / `ON RECOMMENCE` | **OK** (`È` sur `RELÈVE` net) | **OK** (main tendue relevant le frère tombé + plaque commémorative **Camara** et **Thomas Sankara**) | **Contrôlé OK** |
| 10 | `scene-38.png` | v-48 (`178,86 s`) | `ON EST LES ROIS` / `DE L'ÉPREUVE` / `ON EST LA CHANCE` | **OK** (`É` sur `L'ÉPREUVE` net) | **OK** (panthéon net : **Sankara, Bio Guéra, et les 3 présidents de l'AES** sans déformation) | **Contrôlé OK** |
