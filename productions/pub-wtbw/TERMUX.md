# TERMUX — télécharger les livrables DSKY WTBW

Branche : `arena/9a0dd1bb-lyric` · dépôt `Stein500/lyric`

## 0. Préparer Termux (une seule fois)

```bash
pkg update -y && pkg install -y curl unzip ffmpeg
mkdir -p ~/storage/shared/DSKY-WTBW && termux-setup-storage
cd ~/storage/shared/DSKY-WTBW
```

## 1. Le plus rapide : le script qui télécharge tout (~90 Mo)

```bash
curl -L -o get.sh https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/get-livrables.sh
bash get.sh
```

> Il crée les dossiers (`films/`, `brand/`, `pochettes/`, `affiches/`, `visuels/`,
> `variations/`) et y range chaque fichier. Relançable : il reprend où il s'est arrêté
> grâce à `curl -C -`.

> Le zip du dépôt complet est déconseillé depuis le téléphone : l'historique Git pèse
> plus de 10 Go et le zip de branche embarque les 38 pistes audio.

## 2. Fichier par fichier (curl direct, sans zip)

```bash
cd ~/storage/shared/DSKY-WTBW && mkdir -p films brand pochettes affiches visuels variations
```

### Films (9:16) — 9 fichiers

```bash
curl -L -o "FILM-ANNIVERSAIRE-9x16.mp4" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/FILM-ANNIVERSAIRE-9x16.mp4    # 4.9 Mo
curl -L -o "FILM-CATALOGUE-34-9x16.mp4" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/FILM-CATALOGUE-34-9x16.mp4    # 4.9 Mo
curl -L -o "FILM-CITATIONS-9x16.mp4" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/FILM-CITATIONS-9x16.mp4    # 8.8 Mo
curl -L -o "FILM-EDUCATION-9x16.mp4" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/FILM-EDUCATION-9x16.mp4    # 5.9 Mo
curl -L -o "FILM-MARIAGE-9x16.mp4" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/FILM-MARIAGE-9x16.mp4    # 5.8 Mo
curl -L -o "FILM-MEMOIRE-9x16.mp4" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/FILM-MEMOIRE-9x16.mp4    # 7.2 Mo
curl -L -o "FILM-SERVICES-9x16.mp4" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/FILM-SERVICES-9x16.mp4    # 5.2 Mo
curl -L -o "PUB-WTBW-BUMPER-5s-9x16.mp4" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/PUB-WTBW-BUMPER-5s-9x16.mp4    # 2.5 Mo
curl -L -o "PUB-WTBW-CATALOGUE-9x16.mp4" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/PUB-WTBW-CATALOGUE-9x16.mp4    # 18.4 Mo
```

### Branding / logo — fichiers imprimeur — 8 fichiers

```bash
curl -L -o "DSKY-WTBW-badge-blanc-2000px.png" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-badge-blanc-2000px.png    # 169 ko
curl -L -o "DSKY-WTBW-lettrage-blanc-2400px.png" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lettrage-blanc-2400px.png    # 134 ko
curl -L -o "DSKY-WTBW-lockup-STEIN-blanc-2400px.png" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lockup-STEIN-blanc-2400px.png    # 268 ko
curl -L -o "DSKY-WTBW-lockup-STEIN-noir-2400px.png" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lockup-STEIN-noir-2400px.png    # 265 ko
curl -L -o "DSKY-WTBW-lockup-blanc-2400px.png" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lockup-blanc-2400px.png    # 265 ko
curl -L -o "DSKY-WTBW-lockup-noir-2400px.png" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lockup-noir-2400px.png    # 261 ko
curl -L -o "DSKY-WTBW-sigle-blanc-2000px.png" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-sigle-blanc-2000px.png    # 224 ko
curl -L -o "DSKY-WTBW-sigle.svg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-sigle.svg    # 1 ko
```

### Branding — 10 applications merch — 10 fichiers

```bash
curl -L -o "BRAND-01-LOGO-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-01-LOGO-1080x1350.jpg    # 238 ko
curl -L -o "BRAND-02-TSHIRT-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-02-TSHIRT-1080x1350.jpg    # 384 ko
curl -L -o "BRAND-03-HOODIE-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-03-HOODIE-1080x1350.jpg    # 335 ko
curl -L -o "BRAND-04-TOTE-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-04-TOTE-1080x1350.jpg    # 469 ko
curl -L -o "BRAND-05-CAP-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-05-CAP-1080x1350.jpg    # 369 ko
curl -L -o "BRAND-06-SNEAKERS-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-06-SNEAKERS-1080x1350.jpg    # 411 ko
curl -L -o "BRAND-07-BAG-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-07-BAG-1080x1350.jpg    # 418 ko
curl -L -o "BRAND-08-STICKERS-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-08-STICKERS-1080x1350.jpg    # 571 ko
curl -L -o "BRAND-09-CARDS-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-09-CARDS-1080x1350.jpg    # 480 ko
curl -L -o "BRAND-10-VINYL-1080x1350.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/BRAND-10-VINYL-1080x1350.jpg    # 377 ko
```

### Pochettes — 34 couvertures catalogue — 34 fichiers

```bash
curl -L -o "POCHE-01-NOUKIKO-TCHE-WE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-01-NOUKIKO-TCHE-WE-1080.jpg    # 250 ko
curl -L -o "POCHE-02-AYON-DEKPE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-02-AYON-DEKPE-1080.jpg    # 246 ko
curl -L -o "POCHE-03-TU-ES-TROP-BELLE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-03-TU-ES-TROP-BELLE-1080.jpg    # 261 ko
curl -L -o "POCHE-04-MONSTER-POSITIVE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-04-MONSTER-POSITIVE-1080.jpg    # 203 ko
curl -L -o "POCHE-05-JE-ME-RELEVE-TOUJOURS-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-05-JE-ME-RELEVE-TOUJOURS-1080.jpg    # 223 ko
curl -L -o "POCHE-06-GBETCHE-VIVI-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-06-GBETCHE-VIVI-1080.jpg    # 172 ko
curl -L -o "POCHE-07-NAN-YI-A-GA-DJIN-WE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-07-NAN-YI-A-GA-DJIN-WE-1080.jpg    # 248 ko
curl -L -o "POCHE-08-CONCENTRE-SUR-LE-CHEMIN-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-08-CONCENTRE-SUR-LE-CHEMIN-1080.jpg    # 257 ko
curl -L -o "POCHE-09-SANGUIN-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-09-SANGUIN-1080.jpg    # 258 ko
curl -L -o "POCHE-10-ON-NOUS-A-VOLE-NOTRE-EDUCATION-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-10-ON-NOUS-A-VOLE-NOTRE-EDUCATION-1080.jpg    # 219 ko
curl -L -o "POCHE-11-CA-MONTE-CA-DESCEND-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-11-CA-MONTE-CA-DESCEND-1080.jpg    # 223 ko
curl -L -o "POCHE-12-LE-GOUT-BON-DE-LA-VIE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-12-LE-GOUT-BON-DE-LA-VIE-1080.jpg    # 174 ko
curl -L -o "POCHE-13-MAHU-TI-TE-GBE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-13-MAHU-TI-TE-GBE-1080.jpg    # 248 ko
curl -L -o "POCHE-14-VIVI-O-O-R-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-14-VIVI-O-O-R-1080.jpg    # 241 ko
curl -L -o "POCHE-15-GLACE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-15-GLACE-1080.jpg    # 254 ko
curl -L -o "POCHE-16-GOINFRES-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-16-GOINFRES-1080.jpg    # 199 ko
curl -L -o "POCHE-17-GRAND-MARCHEUR-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-17-GRAND-MARCHEUR-1080.jpg    # 210 ko
curl -L -o "POCHE-18-MASQUE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-18-MASQUE-1080.jpg    # 167 ko
curl -L -o "POCHE-19-GHOST-U-SEE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-19-GHOST-U-SEE-1080.jpg    # 247 ko
curl -L -o "POCHE-20-NONVI-KONOU-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-20-NONVI-KONOU-1080.jpg    # 246 ko
curl -L -o "POCHE-21-YAFOY-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-21-YAFOY-1080.jpg    # 254 ko
curl -L -o "POCHE-22-LE-SURVIVANT-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-22-LE-SURVIVANT-1080.jpg    # 201 ko
curl -L -o "POCHE-23-JE-SUIS-PAUVRE-ET-RICHE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-23-JE-SUIS-PAUVRE-ET-RICHE-1080.jpg    # 216 ko
curl -L -o "POCHE-24-TESTOSTERONE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-24-TESTOSTERONE-1080.jpg    # 174 ko
curl -L -o "POCHE-25-JE-CRACHE-LES-DEMONS-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-25-JE-CRACHE-LES-DEMONS-1080.jpg    # 259 ko
curl -L -o "POCHE-26-DES-LE-DEBUT-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-26-DES-LE-DEBUT-1080.jpg    # 244 ko
curl -L -o "POCHE-27-ENTRE-TES-MAINS-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-27-ENTRE-TES-MAINS-1080.jpg    # 263 ko
curl -L -o "POCHE-28-CALM-IN-OFF-DOWN-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-28-CALM-IN-OFF-DOWN-1080.jpg    # 201 ko
curl -L -o "POCHE-29-DRAGUE-MOI-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-29-DRAGUE-MOI-1080.jpg    # 209 ko
curl -L -o "POCHE-30-JE-M-AIME-TELLEMENT-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-30-JE-M-AIME-TELLEMENT-1080.jpg    # 183 ko
curl -L -o "POCHE-31-SEUL-DANS-MA-TETE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-31-SEUL-DANS-MA-TETE-1080.jpg    # 248 ko
curl -L -o "POCHE-32-L-AMOUR-EST-LA-REPONSE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-32-L-AMOUR-EST-LA-REPONSE-1080.jpg    # 257 ko
curl -L -o "POCHE-33-MOTIVE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-33-MOTIVE-1080.jpg    # 256 ko
curl -L -o "POCHE-34-WOLOF-TECHSTEIN-ESSAIE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/catalogue/POCHE-34-WOLOF-TECHSTEIN-ESSAIE-1080.jpg    # 212 ko
```

### Pochettes — 10 héros — 11 fichiers

```bash
curl -L -o "PLANCHE-10.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/PLANCHE-10.jpg    # 166 ko
curl -L -o "POCHE-01-NOUKIKO-TCHE-WE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-01-NOUKIKO-TCHE-WE-1080.jpg    # 256 ko
curl -L -o "POCHE-02-MONSTER-POSITIVE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-02-MONSTER-POSITIVE-1080.jpg    # 258 ko
curl -L -o "POCHE-03-NAN-YI-A-GA-DJIN-WE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-03-NAN-YI-A-GA-DJIN-WE-1080.jpg    # 265 ko
curl -L -o "POCHE-04-GBETCHE-VIVI-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-04-GBETCHE-VIVI-1080.jpg    # 211 ko
curl -L -o "POCHE-05-MAHU-TI-TE-GBE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-05-MAHU-TI-TE-GBE-1080.jpg    # 215 ko
curl -L -o "POCHE-06-TU-ES-TROP-BELLE-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-06-TU-ES-TROP-BELLE-1080.jpg    # 209 ko
curl -L -o "POCHE-07-SANGUIN-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-07-SANGUIN-1080.jpg    # 249 ko
curl -L -o "POCHE-08-ON-NOUS-A-VOLE-NOTRE-EDUCATION-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-08-ON-NOUS-A-VOLE-NOTRE-EDUCATION-1080.jpg    # 281 ko
curl -L -o "POCHE-09-CONCENTRE-SUR-LE-CHEMIN-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-09-CONCENTRE-SUR-LE-CHEMIN-1080.jpg    # 266 ko
curl -L -o "POCHE-10-LE-SURVIVANT-1080.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/pochettes/POCHE-10-LE-SURVIVANT-1080.jpg    # 176 ko
```

### Affiches services — 10 — 22 fichiers

```bash
curl -L -o "AFFICHE-01-MARIAGE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-01-MARIAGE-STORY.jpg    # 435 ko
curl -L -o "AFFICHE-01-MARIAGE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-01-MARIAGE.jpg    # 334 ko
curl -L -o "AFFICHE-02-ANNIVERSAIRE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-02-ANNIVERSAIRE-STORY.jpg    # 393 ko
curl -L -o "AFFICHE-02-ANNIVERSAIRE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-02-ANNIVERSAIRE.jpg    # 308 ko
curl -L -o "AFFICHE-03-MÉMOIRE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-03-MÉMOIRE-STORY.jpg    # 356 ko
curl -L -o "AFFICHE-03-MÉMOIRE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-03-MÉMOIRE.jpg    # 270 ko
curl -L -o "AFFICHE-04-FÊTE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-04-FÊTE-STORY.jpg    # 423 ko
curl -L -o "AFFICHE-04-FÊTE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-04-FÊTE.jpg    # 339 ko
curl -L -o "AFFICHE-05-CLIP-916-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-05-CLIP-916-STORY.jpg    # 347 ko
curl -L -o "AFFICHE-05-CLIP-916.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-05-CLIP-916.jpg    # 255 ko
curl -L -o "AFFICHE-06-ÉCRITURE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-06-ÉCRITURE-STORY.jpg    # 366 ko
curl -L -o "AFFICHE-06-ÉCRITURE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-06-ÉCRITURE.jpg    # 284 ko
curl -L -o "AFFICHE-07-ÉDUCATION-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-07-ÉDUCATION-STORY.jpg    # 436 ko
curl -L -o "AFFICHE-07-ÉDUCATION.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-07-ÉDUCATION.jpg    # 345 ko
curl -L -o "AFFICHE-08-ÉVÉNEMENT-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-08-ÉVÉNEMENT-STORY.jpg    # 410 ko
curl -L -o "AFFICHE-08-ÉVÉNEMENT.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-08-ÉVÉNEMENT.jpg    # 324 ko
curl -L -o "AFFICHE-09-ÉGLISE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-09-ÉGLISE-STORY.jpg    # 388 ko
curl -L -o "AFFICHE-09-ÉGLISE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-09-ÉGLISE.jpg    # 319 ko
curl -L -o "AFFICHE-10-PARTOUT-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-10-PARTOUT-STORY.jpg    # 497 ko
curl -L -o "AFFICHE-10-PARTOUT.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/AFFICHE-10-PARTOUT.jpg    # 410 ko
curl -L -o "PLANCHE-10-FEED.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/PLANCHE-10-FEED.jpg    # 263 ko
curl -L -o "PLANCHE-AFFICHES.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/affiches/PLANCHE-AFFICHES.jpg    # 338 ko
```

### Visuels universels — 10 — 21 fichiers

```bash
curl -L -o "PLANCHE-10.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/PLANCHE-10.jpg    # 241 ko
curl -L -o "UNI-01-CITATION-HISTOIRE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-01-CITATION-HISTOIRE-STORY.jpg    # 304 ko
curl -L -o "UNI-01-CITATION-HISTOIRE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-01-CITATION-HISTOIRE.jpg    # 304 ko
curl -L -o "UNI-02-CITATION-MEMOIRE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-02-CITATION-MEMOIRE-STORY.jpg    # 330 ko
curl -L -o "UNI-02-CITATION-MEMOIRE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-02-CITATION-MEMOIRE.jpg    # 330 ko
curl -L -o "UNI-03-CITATION-COEUR-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-03-CITATION-COEUR-STORY.jpg    # 349 ko
curl -L -o "UNI-03-CITATION-COEUR.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-03-CITATION-COEUR.jpg    # 349 ko
curl -L -o "UNI-04-UNIVERSEL-EMOTION-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-04-UNIVERSEL-EMOTION-STORY.jpg    # 407 ko
curl -L -o "UNI-04-UNIVERSEL-EMOTION.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-04-UNIVERSEL-EMOTION.jpg    # 407 ko
curl -L -o "UNI-05-UNIVERSEL-AGES-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-05-UNIVERSEL-AGES-STORY.jpg    # 346 ko
curl -L -o "UNI-05-UNIVERSEL-AGES.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-05-UNIVERSEL-AGES.jpg    # 346 ko
curl -L -o "UNI-06-SERVICE-CLIP-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-06-SERVICE-CLIP-STORY.jpg    # 326 ko
curl -L -o "UNI-06-SERVICE-CLIP.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-06-SERVICE-CLIP.jpg    # 326 ko
curl -L -o "UNI-07-SERVICE-POCHE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-07-SERVICE-POCHE-STORY.jpg    # 342 ko
curl -L -o "UNI-07-SERVICE-POCHE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-07-SERVICE-POCHE.jpg    # 342 ko
curl -L -o "UNI-08-METIER-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-08-METIER-STORY.jpg    # 299 ko
curl -L -o "UNI-08-METIER.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-08-METIER.jpg    # 299 ko
curl -L -o "UNI-09-BADGE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-09-BADGE-STORY.jpg    # 339 ko
curl -L -o "UNI-09-BADGE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-09-BADGE.jpg    # 339 ko
curl -L -o "UNI-10-MANIFESTE-STORY.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-10-MANIFESTE-STORY.jpg    # 282 ko
curl -L -o "UNI-10-MANIFESTE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/universel/UNI-10-MANIFESTE.jpg    # 282 ko
```

### Variations laiton — 10 — 11 fichiers

```bash
curl -L -o "PLANCHE-10.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/PLANCHE-10.jpg    # 266 ko
curl -L -o "VAR-01-ALBUM.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-01-ALBUM.jpg    # 312 ko
curl -L -o "VAR-02-DANSE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-02-DANSE.jpg    # 297 ko
curl -L -o "VAR-03-ENFANTS.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-03-ENFANTS.jpg    # 379 ko
curl -L -o "VAR-04-GUITARE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-04-GUITARE.jpg    # 285 ko
curl -L -o "VAR-05-SALLE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-05-SALLE.jpg    # 359 ko
curl -L -o "VAR-06-34.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-06-34.jpg    # 197 ko
curl -L -o "VAR-07-CITATION.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-07-CITATION.jpg    # 294 ko
curl -L -o "VAR-08-FRISE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-08-FRISE.jpg    # 223 ko
curl -L -o "VAR-09-MERCI.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-09-MERCI.jpg    # 261 ko
curl -L -o "VAR-10-ANNONCE.jpg" \
  https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/variations/VAR-10-ANNONCE.jpg    # 195 ko
```

Total des fichiers ci-dessus : **97.5 Mo**.

## 3. Vérifier après téléchargement

```bash
# durées et poids des films
for f in films/*.mp4; do echo -n "$f  "; ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"; done

# nombre d'images récupérées
ls pochettes | wc -l      # attendu : 34
ls affiches  | wc -l      # attendu : 10
```

## 4. Publier depuis le téléphone

| Production | Où | Format |
|---|---|---|
| Films mariage / mémoire / anniversaire / éducation | TikTok, Reels, Statut WhatsApp, YouTube Shorts | 9:16, 16–24 s |
| Film catalogue 34 | YouTube (non répertorié), bio TikTok | 9:16, 29 s |
| Pochettes | IG / FB (carrousel), YouTube (miniature) | 1080×1080 |
| Affiches services | Statut WhatsApp, Facebook | 1080×1350 |
| Fichiers imprimeur | flocage, broderie, cartes | PNG transparent / SVG |

> Astuce Termux : `termux-open --content-type video/mp4 films/FILM-MARIAGE-9x16.mp4`
> ouvre directement le film dans le lecteur du téléphone.
