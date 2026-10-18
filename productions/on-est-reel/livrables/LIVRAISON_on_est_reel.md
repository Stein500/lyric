# LIVRAISON FINALE — « On est réel » · Dsky (v5.9 — MODE PEINT)

---

## 1. Commandes Termux (copier-coller direct)

### Option A — Téléchargement unitaire direct (`curl -fL`, reproductible sur hash vérifié `7dff3b7870d30f26e430ac543f86731b2285fbec` ou sur la branche `arena/cd315c34-lyric`)

```bash
pkg install -y curl && mkdir -p ~/storage/shared/Download/OnEstReel-Dsky && cd ~/storage/shared/Download/OnEstReel-Dsky && \
HASH="7dff3b7870d30f26e430ac543f86731b2285fbec" && \
BASE="https://raw.githubusercontent.com/Stein500/lyric/${HASH}/productions/on-est-reel/livrables" && \
curl -fL "$BASE/on-est-reel-916.mp4" -o "on-est-reel-916.mp4" && \
curl -fL "$BASE/On%20est%20r%C3%A9el%20-%20master%20320k.mp3" -o "On est réel - master 320k.mp3" && \
curl -fL "$BASE/cover-1080.jpg" -o "cover-1080.jpg" && \
curl -fL "$BASE/cover-916.jpg" -o "cover-916.jpg" && \
curl -fL "$BASE/carte-accueil.jpg" -o "carte-accueil.jpg" && \
curl -fL "$BASE/carte-finale.jpg" -o "carte-finale.jpg" && \
curl -fL "$BASE/paroles_clean.txt" -o "paroles_clean.txt" && \
ls -lh ~/storage/shared/Download/OnEstReel-Dsky
```

*(Variante pointant sur le nom de branche `arena/cd315c34-lyric`)* :
```bash
mkdir -p ~/storage/shared/Download/OnEstReel-Dsky && cd ~/storage/shared/Download/OnEstReel-Dsky && \
BASE="https://raw.githubusercontent.com/Stein500/lyric/arena/cd315c34-lyric/productions/on-est-reel/livrables" && \
curl -fL "$BASE/on-est-reel-916.mp4" -o "on-est-reel-916.mp4" && \
curl -fL "$BASE/On%20est%20r%C3%A9el%20-%20master%20320k.mp3" -o "On est réel - master 320k.mp3" && \
curl -fL "$BASE/cover-1080.jpg" -o "cover-1080.jpg" && \
curl -fL "$BASE/cover-916.jpg" -o "cover-916.jpg" && \
ls -lh ~/storage/shared/Download/OnEstReel-Dsky
```

### Option B — Clone léger (`sparse-checkout`) du dossier `productions/on-est-reel`

```bash
pkg install -y git && rm -rf ~/on-est-reel-dl && \
git clone --depth 1 --filter=blob:none --sparse -b arena/cd315c34-lyric https://github.com/Stein500/lyric.git ~/on-est-reel-dl && \
cd ~/on-est-reel-dl && git sparse-checkout set productions/on-est-reel/livrables && \
mkdir -p ~/storage/shared/Download/OnEstReel-Dsky && \
cp -v productions/on-est-reel/livrables/* ~/storage/shared/Download/OnEstReel-Dsky/ && \
ls -lh ~/storage/shared/Download/OnEstReel-Dsky
```

---

## 2. Chemins exacts des livrables et tailles vérifiées (local == distant)

- **Branche** : `arena/cd315c34-lyric`
- **Commit livrables vérifié (`git ls-remote` & API GitHub)** : `7dff3b7870d30f26e430ac543f86731b2285fbec`

| Livrable | Chemin dans le dépôt | Taille exacte (octets) | Taille lisible |
|---|---|---:|---:|
| Vidéo Lyrics 9:16 (1080×1920, 30 fps, H.264 + AAC 256k) | `productions/on-est-reel/livrables/on-est-reel-916.mp4` | `71 408 712` | `68,10 Mio` |
| Master Audio 320 kb/s CBR 48 kHz + tags ID3 + cover 1080² + USLT | `productions/on-est-reel/livrables/On est réel - master 320k.mp3` | `10 166 044` | `9,70 Mio` |
| Pochette carrée 1080×1080 (JPEG Q95) | `productions/on-est-reel/livrables/cover-1080.jpg` | `346 540` | `338,4 Kio` |
| Pochette carrée 1080×1080 (PNG) | `productions/on-est-reel/livrables/cover-1080.png` | `1 519 619` | `1,45 Mio` |
| Cover verticale 9:16 1080×1920 (JPEG Q95) | `productions/on-est-reel/livrables/cover-916.jpg` | `631 022` | `616,2 Kio` |
| Carton d'accueil (JPEG) | `productions/on-est-reel/livrables/carte-accueil.jpg` | `183 827` | `179,5 Kio` |
| Carton final — Code `0405` (JPEG) | `productions/on-est-reel/livrables/carte-finale.jpg` | `243 857` | `238,1 Kio` |
| Paroles propres sans timestamps (`USLT`) | `productions/on-est-reel/livrables/paroles_clean.txt` | `2 785` | `2,7 Kio` |
| Planche de contrôle MP4 rendu (16 frames) | `productions/on-est-reel/CONTROLE-mp4-final.jpg` | `1 749 166` | `1,67 Mio` |
| Planche zoom 1:1 typo sur frames MP4 en travelling | `productions/on-est-reel/CONTROLE-typo-zoom.jpg` | `723 980` | `707,0 Kio` |

---

## 3. Contrôles mesurés (Audio, Vidéo, Cartes, Clochettes, Conformité v5.9)

| Contrôle (§12) | Outil / Méthode | Valeur mesurée | Seuil v5.9 | Statut |
|---|---|---|---|---|
| Mode de production | Verrouillé §0 | **`MODE PEINT`** | 100 % cohérent | **OK** |
| Plans distincts disponibles | `build_map.py` / `verses_map.json` | **`46 / 46`** (`0` manquant, **57 / 57** vers couverts) | `100 %` (`0` manquant) | **OK** |
| Durée audio maître décodée | `ffmpeg -i` | **`244,99 s`** (`04:04.99`) → Code **`0405`** | Décodage complet | **OK** |
| Durée vidéo MP4 décodée | `ffmpeg -i` | **`250,00 s`** (`00:04:10.00` = `7 500 frames / 30 fps`) | `= frames/fps ± 0,01 s` | **OK** |
| Frames noires | `blackdetect=d=0.05:pix_th=0.10` | **`0`** (`[]`) | `0` | **OK** |
| Freeze sur les vers | `freezedetect=n=-33dB:d=2.5` | **`0` sur les 57 vers** (uniquement cartons `0→10,77 s` et `245,33→250,00 s`, assumés) | `0` sur les vers | **OK** |
| Loudness intégré (MP3 / MP4) | `ebur128=peak=true` (double passe `loudnorm`) | **`-14,0 LUFS`** (MP3 & MP4) · `LRA = 7,5 / 7,4 LU` | `-14 LUFS ± 0,5` | **OK** |
| True Peak / Crête | `ebur128` + `astats` | **`-1,7 dBFS`** (`-1,75 dB` MP3) / **`-1,8 dBFS`** (`-1,81 dB` MP4) | `≤ -1,0 dB` | **OK** |
| Faststart (`moov` avant `mdat`) | Inspection binaire MP4 | `moov` = octet **`36`** < `mdat` = octet **`262 588`** | `moov < mdat` | **OK** |
| Typo pendant le travelling | `CONTROLE-typo-zoom.jpg` (zoom 1:1) | **Nette, 0 doublement de lettre, orthographe 100 % exacte** | Nette, 0 doublement | **OK** |
| Fenêtres clochettes (`≥ 4,0 s`) | `verses_map.json` | **4 fenêtres** : `17,15→24,48 s` (`7,33 s`), `187,35→193,01 s` (`5,66 s`), `225,11→232,32 s` (`7,21 s`), `234,67→244,99 s` (`10,32 s`) | Seuil `≥ 4,0 s` en MODE PEINT | **OK** |
| Carton final & code | `carte-finale.jpg` / `244,99→249,99 s` | **`5,00 s`** après la fin du son · Code **`0405`** en `210 px` or `#D9A441` | `5 s` + code `MMSS` | **OK** |
| Drapeaux / logos / contacts | Inspection des 46 plans | **`0` drapeau, `0` contact, `0` watermark, têtes 100 % entières** | Interdiction stricte §3/§14 | **OK** |

---

## 4. Titres YouTube / TikTok / Reels / Shorts (5 propositions)

1. **Dsky — On est réel (Clip Lyrics Officiel) | L'Abandon n'est pas une option 🔥**
2. **Dsky — On est réel | Hommage à Sankara, Béhanzin, Bio Guéra, Lumumba & aux Lions d'Afrique 🦁**
3. **« Aujourd'hui je suis debout » — Dsky · On est réel (Lyrics Video 9:16)**
4. **Dsky — On est réel (Wolof TechStein beat wê !) | Rap Conscient & Résilience Africaine**
5. **Pour ceux qui voulaient tout lâcher… Écoute ça jusqu'à la fin (Code à 04:05) — Dsky · On est réel**

---

## 5. Description prête à coller (Chapitres + Paroles intégrales + Crédits + Déclaration IA + Hashtags)

```text
Dsky — On est réel (Lyrics Video Officiel)
Prod. signature : Wolof TechStein beat wê !

Un hymne de résilience pour chaque frère, chaque sœur, chaque père et chaque mère qui traverse la tempête en silence. Quand tout pèse et que la tentation de baisser les bras apparaît, souviens-toi d'où tu viens : l'abandon n'est pas une option. On est réels, on est vivants, on est debout.

Regarde jusqu'à la toute fin de la vidéo et commente le code à 4 chiffres affiché sur l'écran final !

⏱️ CHAPITRES :
00:00 Carton d'accueil & Signature (Wolof TechStein beat wê !)
00:10 Intro — T'es là… tu m'écoutes ?
00:24 Couplet 1 — La rue, la faim, les cicatrices et la dignité du père
00:49 Refrain 1 — Aujourd'hui je suis debout, je suis né pour chanter
01:10 Couplet 2 — Le feu des ancêtres (Béhanzin, Sankara, Bio Guéra) & la famille debout
01:41 Refrain 2 — On a serré les poings, on a crié sous le ciel
02:02 Pont & Couplet 3 — L'Afrique debout, justice, unité et souveraineté
03:13 Refrain Final (Aube dorée) — On est réels, on est vivants, on est debout
04:05 Carton final — Commente le code !

📜 PAROLES OFFICIELLES — ON EST RÉEL (DSKY) :

Wolof TechStein beat wê!
T'es là... Tu m'écoutes ?
Y a des nuits où le silence fait plus de bruit que les balles
J'ai marché dans la boue avec des rêves en étoile
J'ai vu mes frères tomber pour des billets qui brûlent
J'ai vu l'espoir mourir au fond d'une cellule
La rue m'a dit : « Petit, ici personne te pardonne »
Mais j'avais la foi d'un roi même sans la couronne
J'ai connu la faim qui te tord le ventre en deux
J'ai connu le froid qui te gèle jusqu'aux yeux
J'ai vu ma mère prier avec les mains qui tremblent
Elle disait : « Mon fils, tant qu'on est debout, on tient ensemble »
J'ai vu mon père se briser sans faire de bruit
Un homme qui pleure en cachette au milieu de la nuit
Chaque cicatrice sur ma peau, c'est une leçon
Chaque trahison m'a appris à bâtir ma maison
Ils ont voulu m'éteindre, ils ont soufflé sur ma flamme
Mais ils savaient pas que le feu, c'était mon âme

Aujourd'hui je suis debout, je suis né pour chanter
On a pleuré dans l'ombre, mais on a fini par briller
On a serré les poings, on a crié sous le ciel
Pour ceux qui n'ont pas de voix, pour ceux qui n'ont plus rien
On est réels... On est vivants...

Dans mes veines coule l'histoire de ceux qu'on a voulu effacer
Le feu de mes ancêtres, le feu de mes dieux
On porte la douleur, mais on porte aussi la terre
Ils ont pillé nos sols, ils ont volé nos saisons
Mais ils n'ont jamais pu acheter notre raison
Un combattant, un survivant, plus fort que toi
Je parle pour le gamin qui dort le ventre creux
Qui regarde le plafond en demandant pourquoi Dieu
Je parle pour la daronne qui porte le monde sur son dos
Qui sourit à ses gosses alors qu'elle coule sous l'eau
On n'est pas nés pour ramper, on n'est pas nés pour subir
Même quand tout s'écroule, on refuse de mourir

Aujourd'hui je suis debout, je suis né pour chanter
On a pleuré dans l'ombre, mais on a fini par briller
On a serré les poings, on a crié sous le ciel
Pour ceux qui n'ont pas de voix, pour ceux qui n'ont plus rien
On est réels... On est vivants...

Regarde-nous dans les yeux, on n'a plus peur du noir
C'est dans la nuit la plus sombre qu'on écrit l'histoire
Ils ont voulu nous diviser, frère contre frère
Mais le même sang rouge nourrit la même terre
J'ai vu des rois sans palais, des soldats sans armure
Qui tiennent leur famille à bout de bras contre le mur
Mais nos cœurs sont des volcans, nos âmes sont des épées
J'ai vu des traîtres vendre leur sang pour du blé
Mais j'ai vu tout un peuple se lever pour sa dignité
La vérité finit toujours par traverser le béton
Même si tu l'enterres profond, elle repousse au printemps
J'ai besoin de la justice, j'ai besoin de mon destin
On ne mendie plus sa place, on la prend de nos mains
Mes mots sont des missiles, mes rimes sont des boucliers
Pour chaque âme blessée qu'on a voulu oublier
Si tu m'écoutes ce soir et que tu veux tout lâcher
Pose ta main sur ton cœur, sens-le encore frapper
Tant que tu respires, frère, le combat continue
La victoire appartient à ceux qui ont tenu

Pour ma mère, pour mon père, pour mes frères tombés
Pour l'Afrique qui se lève et qui refuse de plier
Pour chaque larme versée dans le secret de la nuit
Pour les héros d'hier, pour les lions d'aujourd'hui
On a traversé l'enfer les pieds nus sur les braises
Aujourd'hui notre voix résonne et rien ne l'apaise
On est le cri du silence, on est la force du pardon
On est la génération qui relève le front

Aujourd'hui je suis debout, je suis né pour chanter
On a pleuré dans l'ombre, mais on a fini par briller
On a serré les poings, on a crié sous le ciel
Pour ceux qui n'ont pas de voix, pour ceux qui n'ont plus rien
On est réels... On est vivants...

On est réels...
Même dans la tempête, on reste debout
Tant qu'il reste un souffle, l'histoire continue
Pour ceux qui tiennent bon quand tout vacille
On n'a jamais baissé les yeux
On est réels... On est debout...

🎙️ CRÉDITS :
Artiste : Dsky
Titre : On est réel
Signature : Wolof TechStein beat wê !
Master Audio : -14,0 LUFS / -1,7 dBTP / 48 kHz / 320 kbps
Direction visuelle : Gouache cinématographique 9:16 (v5.9 — MODE PEINT)

🤖 DÉCLARATION IA :
- Visuels : OUI (illustrations peintes générées par IA selon la charte artistique v5.9).
- Audio : NON (enregistrement et interprétation vocale/musicale d'origine de l'artiste Dsky, masterisé à -14 LUFS).

#Dsky #OnEstReel #RapConscient #AfriqueDebout #Resilience #Sankara #Behanzin #BioGuera #AES #Lumumba #LyricsVideo #WolofTechStein
```

---

## 6. Trois commentaires épinglés prêts à poster

### Commentaire épinglé 1 — Le Code de fin (`0405`)
> 🔥 **LA FAMILLE, QUI EST RESTÉ JUSQU'À LA FIN ?**  
> Commente le **code à 4 chiffres** qui s'affiche à la fin de la vidéo pour prouver que tu fais partie des vrais qui ne lâchent rien ! 🦁✊  
> *(Et dis-moi si tu as un son ou des paroles que tu aimerais voir réalisés en clip lyrics !)*

### Commentaire épinglé 2 — Le Vers qui te parle le plus
> 💬 **Quel vers de « On est réel » résonne le plus dans ta vie aujourd'hui ?**  
> 1️⃣ *« Tant qu'on est debout, on tient ensemble »*  
> 2️⃣ *« Tant que tu respires, frère, le combat continue — la victoire appartient à ceux qui ont tenu »*  
> 3️⃣ *« Pour les héros d'hier, pour les lions d'aujourd'hui »*  
> Écris ton numéro ou ta phrase en commentaire et **partage la vidéo** à un frère ou une sœur qui a besoin de force ce soir ! 🙏🔥

### Commentaire épinglé 3 — Hommage aux Héros & aux Familles
> 🌍 **De Béhanzin, Bio Guéra, Thomas Sankara, Patrice Lumumba, Cheikh Anta Diop, Nelson Mandela jusqu'aux lions d'aujourd'hui et à nos parents qui se battent en silence :**  
> Ce son est dédié à tous ceux qui refusent de plier. **Abonne-toi**, active la cloche 🔔 et écris de quel pays ou de quelle ville tu écoutes **Dsky** !
