# Livraison — Nonvi Konou

## Fichiers

- `Nonvi_Konou_9x16_v2.mp4` — clip lyrics vertical corrigé, 1080×1920, 30 fps, H.264/AAC, 204,47 s.
- `Nonvi_Konou_master_320k.mp3` — chanson seule, 320 kb/s, 48 kHz stéréo, ID3v2.4 complet, paroles et cover APIC.
- `cover_nonvi_konou_1080.jpg` — cover carrée 1080×1080 utilisée dans le MP3.
- `cover_nonvi_konou_universelle_3000.jpg` — cover universelle carrée 3000×3000.
- `cover_nonvi_konou_9x16.jpg` — cover verticale 1080×1920.
- `CAPTION_NONVI_KONOU.txt` — légende de publication avec quatre hashtags.
- `CONTROLES_NONVI_KONOU.json` — mesures, validations techniques et SHA-256.
- `COMMANDES_TERMUX_NONVI_KONOU.txt` — téléchargement mobile depuis un commit Git immuable.

## Construction du clip

Le clip commence par un extrait de refrain de 6 secondes pris à 02:15,56, puis joue la chanson complète et une endcard de 5 secondes. Les paroles restent centrées ; le mot actif passe en or pendant qu'une vague d'eau anime simultanément le bloc. Les 35 textes distincts utilisent 35 fonds distincts ; seules les 15 reprises textuellement identiques réemploient un fond. L'intro et l'endcard portent le total à 37 fonds.

Dans la v2, les paroles utilisent une cursive de 126 px — environ 46 % plus grande que dans le premier rendu — et les vers longs passent jusqu'à trois lignes sans coupure. Le badge `Dsky` et son pictogramme béninois apparaissent et disparaissent en fondu avec chaque vers ; ils sont absents dans les intervalles sans paroles. Le bandeau du Bénin reste fixe, mesure 54 px sur 1920 et conserve la géométrie officielle demandée.

## Contrôles finaux

Résultat global : **PASS**.

- vidéo : 6134 images, 204,4667 s par calcul images/fps, aucun événement `blackdetect` ni `freezedetect` au seuil standard ;
- correction v2 : police de paroles 126 px, badge présent pendant les vers et vérifié absent dans l'intervalle sans paroles à 7,2 s ;
- audio master : 193,488 s, −13,84 LUFS, −1,53 dBTP, 320 kb/s, 48 kHz ;
- covers : 1080×1920, 1080×1080 et 3000×3000 ;
- ID3 : titre, artiste, album, compositeur, éditeur, année, genre, contacts, producteur, label, paroles et APIC présents.
