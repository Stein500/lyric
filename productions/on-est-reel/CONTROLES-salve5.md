# Contrôles — Salve 5 (`scene-10`, `26`, `27`, `30`, `34`, `38` régénérés avec vraies photos AES + `scene-32` retry + `scene-39`, `40`, `41-final`)

Suite à la demande explicite de l'artiste (*« Cherche sur le net les images des présidents, Tiani, Traoré, et Goïta ....pour bien les générer .car ce que tu as fait ne ressemble pas bien »*), les portraits officiels des trois présidents de l'AES ont été récupérés par recherche d'images (`notreafrik.com`) et assemblés sans aucun drapeau ni micro en planche de référence faciale passée directement au générateur :
- **Assimi Goïta** (Mali — bonnet traditionnel blanc brodé *kufi*, barbe courte taillée le long de la mâchoire)
- **Ibrahim Traoré** (Burkina Faso — béret rouge incliné, foulard beige autour du cou, visage jeune sans barbe)
- **Abdourahamane Tiani** (Niger — béret marron/kaki à deux étoiles dorées, visage mûr rasé de près)

---

## Bilan de la Salve 5 (§4 & §10.2)

- **Quota du tour** : **10 images demandées / 10 générées avec succès / 0 échec système / 10 sur 10 validées à 100 % au zoom 1:1** (`CONTROLE-salve5-aes.jpg`, `CONTROLE-salve5-portraits.jpg` et `CONTROLE-salve5-typo.jpg`).
- **Cumul dans `fonds/`** : **41 plans distincts disponibles sur 46** (100 % des plans présents sont validés sans aucune faute d'orthographe), couvrant **51 vers sur 57** (`v-01` à `v-50` et `v-57`). Il ne reste plus que les **5 variantes d'aube dédiées du refrain final (`v-51` à `v-56`, §9)** pour lancer le rendu vidéo complet.

| # | Fichier | Vers couverts | Texte peint lu au zoom 1:1 (`CONTROLE-salve5-typo.jpg`) | Ressemblance & portraits (`CONTROLE-salve5-portraits.jpg`) | Verdict QC |
|---|---|---|---|---|---|
| 01 | `scene-10.png` *(v2 AES)* | v-11 (`58,63 s`) | `MOI J'AI LE STYLO` / `QUI BRÛLE` / `J'ÉCRIS MA ROUTE` | **OK** (`Û`, `É` nets) · **Goïta, Traoré, Tiani** fidèles aux photos de référence | **Contrôlé OK** |
| 02 | `scene-26.png` *(v2 AES)* | v-32 (`130,48 s`) | `J'AI VU DES` / `FRÈRES SE LEVER` / `POUR SE BATTRE, POUR DANSER` | **OK** (`È` net) · **Goïta, Traoré, Tiani** fidèles au-dessus des frères levés | **Contrôlé OK** |
| 03 | `scene-27.png` *(v2 AES)* | v-33 (`133,57 s`) | `ON EST LA NOUVELLE` / `GÉNÉRATION` / `ON A LA RAGE EN HÉRITAGE` | **OK** (`É`, `É`, `É` nets) · **Goïta, Traoré, Tiani** fidèles au-dessus de la jeunesse | **Contrôlé OK** |
| 04 | `scene-30.png` *(v2 AES)* | v-36 (`142,48 s`) | `J'AI BESOIN` / `DE LA JUSTICE` / `J'AI BESOIN DE MON DESTIN` | **OK** · **Goïta, Traoré, Tiani** en grands bustes d'or fidèles | **Contrôlé OK** |
| 05 | `scene-34.png` *(v2 AES)* | v-40 (`153,90 s`) | `JE SUIS LE FILS` / `DU SOLEIL` / `LA LUMIÈRE QUI A VAINCU` | **OK** (`È` net) · **Goïta, Traoré, Tiani** dans le soleil levant | **Contrôlé OK** |
| 06 | `scene-38.png` *(v2)* | v-48 (`178,86 s`) | `ON EST LES ROIS` / `DE L'ÉPREUVE` / `ON EST LA CHANCE` | **OK** (`É` net) · Fresque dorée Sankara, Béhanzin, Bio Guéra | **Contrôlé OK** |
| 07 | `scene-32.png` *(retry §4)* | v-38 (`148,71 s`) | `JE VIENS` / `DE LA STREET` / `J'SUIS NÉ POUR BRILLER` | **OK** (texte corrigé à 100 %, `É` sur `NÉ` net) | **Contrôlé OK** |
| 08 | `scene-39.png` | v-49 (`181,81 s`) | `LE PASSÉ EST PASSÉ` / `LES CHAÎNES` / `SONT BRISÉES` | **OK** (double `É`, `Î`, `É` nets) · Chaînes brisées sous le regard de Béhanzin & Bio Guéra | **Contrôlé OK** |
| 09 | `scene-40.png` | v-50 (`184,50 s`) | `AUJOURD'HUI` / `JE SUIS DEBOUT` / `JE SUIS NÉ POUR CHANTER` | **OK** (`É` net) · **Goïta, Traoré, Tiani** fidèles dans l'aube dorée | **Contrôlé OK** |
| 10 | `scene-41-final.png` | v-57 (`232,32 s`) | `ON EST RÉELS...` / `ON EST DEBOUT...` | **OK** (`É` net) · **Famille relevée** + **Goïta, Traoré, Tiani** en plein soleil levant | **Contrôlé OK** |
