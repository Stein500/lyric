# Télécharger la maquette — Concentré sur le chemin

**Maquette de validation de 14,5 s, pas le clip final.** Un seul fond a été généré. Ressemblance, ancre et calage vocal restent à approuver avant la suite.

Hash immuable des médias, obtenu après commit/push et vérifié via Git + API GitHub :

`0970913c998c4aca5523917f31e9963e1d9cdbcb`

## 1. Préparer Termux (une fois)

Copier la ligne entière, accepter l'autorisation d'accès au stockage :

```sh
pkg update -y; pkg install -y curl ca-certificates; termux-setup-storage
```

## 2. Aperçu vidéo — 1080×1920, 14,5 s, environ 4,55 Mo

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Concentre_sur_le_chemin_maquette_9x16_v1.mp4 https://raw.githubusercontent.com/Stein500/lyric/0970913c998c4aca5523917f31e9963e1d9cdbcb/livrables/Concentre_sur_le_chemin_maquette_9x16_v1.mp4; ls -lh /storage/emulated/0/Web+/Concentre_sur_le_chemin_maquette_9x16_v1.mp4
```

Taille attendue : **4 553 267 octets**.

## 3. Ancre fixe — JPG, environ 506 ko

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Concentre_sur_le_chemin_ancre_9x16_v1.jpg https://raw.githubusercontent.com/Stein500/lyric/0970913c998c4aca5523917f31e9963e1d9cdbcb/livrables/Concentre_sur_le_chemin_ancre_9x16_v1.jpg; ls -lh /storage/emulated/0/Web+/Concentre_sur_le_chemin_ancre_9x16_v1.jpg
```

Taille attendue : **506 412 octets**.

## 4. Prompt universel à jour — Markdown

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md https://raw.githubusercontent.com/Stein500/lyric/0970913c998c4aca5523917f31e9963e1d9cdbcb/PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md; ls -lh /storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md
```

Taille attendue : **37 771 octets**. Ce document texte fait normalement moins de 100 ko : ne pas le supprimer pour cette seule raison.

## Si la connexion coupe

- Relancer la même ligne : `-C -` reprend le téléchargement interrompu.
- `-fL` fait échouer les erreurs HTTP au lieu d'enregistrer une page d'erreur comme média.
- Si le MP4 ou le JPG ne fait que quelques octets ou moins de 100 ko à cause d'une erreur, supprimer ce fichier partiel puis relancer sa ligne. Comparer aux tailles attendues ci-dessus.
- Si Termux affiche seulement `>` : Ctrl+C, puis recoller la ligne entière.
- Les commandes des **clips complets, du master MP3 et des covers** seront produites au nouveau hash de leur livraison réelle. Aucun lien fictif vers ces fichiers non encore créés n'est fourni ici.
