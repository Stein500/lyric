# VIVI OOR — Télécharger les 10 images

**10 PNG en 1080 × 1920, sans texte.** Le ZIP contient uniquement les dix compositions finales, pas les décors seuls.

- Fichier : `VIVI_OOR_10_images_9x16.zip`
- Taille exacte : **20 222 558 octets** (environ 20 Mo).
- Commit des images, déjà poussé : `d086aed69b3ea636f36768b65feb5d2accb6abe6`.
- SHA-256 du ZIP : `96c87d78fc52d9b9a125fe2f59cb09086ae88e3a92726cbca45caf6fb4889be3`.
- Le dépôt est public ; aucun jeton ni mot de passe n’est nécessaire.

[Téléchargement direct du ZIP](https://raw.githubusercontent.com/Stein500/lyric/d086aed69b3ea636f36768b65feb5d2accb6abe6/vivi-oor/VIVI_OOR_10_images_9x16.zip)

Le fichier existe à ce commit : nom, taille et URL confirmés via l’API GitHub. La connexion TLS à `raw.githubusercontent.com` est bloquée depuis la sandbox ; le téléchargement HTTP complet n’a donc pas pu être testé ici. Le ZIP local, lui, a été ouvert et ses dix entrées vérifiées sans erreur.

## 1. Préparer Termux (seulement si nécessaire)

Copier chaque commande en **une seule ligne**. Après `termux-setup-storage`, accepter l’autorisation Android.

```bash
pkg update -y; pkg install -y curl ca-certificates unzip; termux-setup-storage
```

## 2. Télécharger le pack

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_10_images_9x16.zip https://raw.githubusercontent.com/Stein500/lyric/d086aed69b3ea636f36768b65feb5d2accb6abe6/vivi-oor/VIVI_OOR_10_images_9x16.zip; ls -lh /storage/emulated/0/Web+/VIVI_OOR_10_images_9x16.zip
```

En cas de coupure, relancer la **même ligne**, qui reprend le fichier partiel. Le ZIP terminé doit faire 20 222 558 octets. Ne pas tenter de décompresser un téléchargement interrompu.

Vérification facultative :

```bash
sha256sum /storage/emulated/0/Web+/VIVI_OOR_10_images_9x16.zip
```

## 3. Extraire, une fois le téléchargement terminé

```bash
unzip -o /storage/emulated/0/Web+/VIVI_OOR_10_images_9x16.zip -d /storage/emulated/0/Web+/VIVI_OOR; ls -lh /storage/emulated/0/Web+/VIVI_OOR
```

Les dix images sont ensuite dans **Stockage interne → Web+ → VIVI_OOR**.

## 4. Prompts de référence (facultatif)

Catalogue des dix décors et correspondances avec les paroles :

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/PROMPTS_IMAGES_VIVI_OOR.md https://raw.githubusercontent.com/Stein500/lyric/d086aed69b3ea636f36768b65feb5d2accb6abe6/vivi-oor/PROMPTS_IMAGES_VIVI_OOR.md
```

Prompt universel v5.3 comprenant l’addendum v5.3.1 :

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.3_FINAL.md https://raw.githubusercontent.com/Stein500/lyric/d086aed69b3ea636f36768b65feb5d2accb6abe6/PROMPT_UNIVERSEL_v5.3_FINAL.md
```

Un petit fichier Markdown est normal ; le contrôle de taille de 20 Mo concerne le ZIP, pas les textes. Si Termux affiche un simple `>` en attendant la suite d’une commande, faire Ctrl+C et recoller la ligne entière.
