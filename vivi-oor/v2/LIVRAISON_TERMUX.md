# Vivi OOR V2 — les 10 retouches IA

Archive : **VIVI_OOR_V2_10_images_9x16.zip**, 19 802 273 octets, exactement dix PNG en 1080 × 1920.

Commit des images poussé : `eaec1480a8a5875f30681ee270d70dcb12e335cd`.

SHA-256 du ZIP : `cfc80ce40af8308a65f9f770295880a90fce95ab669801cb374a81543093f5cd`.

[Télécharger directement les dix images](https://raw.githubusercontent.com/Stein500/lyric/eaec1480a8a5875f30681ee270d70dcb12e335cd/vivi-oor/v2/VIVI_OOR_V2_10_images_9x16.zip)

## Termux

Installation si nécessaire, puis accepter la permission de stockage Android :

```bash
pkg update -y; pkg install -y curl ca-certificates unzip; termux-setup-storage
```

Téléchargement reprenable, **une seule ligne** :

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_V2; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_V2_10_images_9x16.zip https://raw.githubusercontent.com/Stein500/lyric/eaec1480a8a5875f30681ee270d70dcb12e335cd/vivi-oor/v2/VIVI_OOR_V2_10_images_9x16.zip; ls -lh /storage/emulated/0/Web+/VIVI_OOR_V2_10_images_9x16.zip
```

Relancer la même ligne après une coupure. Une fois le téléchargement terminé :

```bash
unzip -o /storage/emulated/0/Web+/VIVI_OOR_V2_10_images_9x16.zip -d /storage/emulated/0/Web+/VIVI_OOR_V2
```

Vérification facultative :

```bash
sha256sum /storage/emulated/0/Web+/VIVI_OOR_V2_10_images_9x16.zip
```

Catalogue des dix prompts de retouche :

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/PROMPTS_IMAGES_VIVI_OOR_V2.md https://raw.githubusercontent.com/Stein500/lyric/eaec1480a8a5875f30681ee270d70dcb12e335cd/vivi-oor/v2/PROMPTS_IMAGES_VIVI_OOR_V2.md
```

Le ZIP local est vérifié et les fichiers sont enregistrés dans le dépôt public au commit ci-dessus. L’affichage et le téléchargement depuis la galerie locale ont été contrôlés ; la commande Termux reste à exécuter sur le téléphone. Aucun identifiant GitHub n’est requis.
