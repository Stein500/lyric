#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère TERMUX.md : commandes curl de téléchargement de tous les livrables.
Usage : python3 make_termux.py
"""
import os
import subprocess

BRANCH = "arena/9a0dd1bb-lyric"
REPO = "Stein500/lyric"
BASE = f"productions/pub-wtbw"
OUT = "/home/user/lyric/productions/pub-wtbw"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{BASE}"

GROUPS = [
    ("Films (9:16)", "livrables", (".mp4",)),
    ("Branding / logo — fichiers imprimeur", "livrables/brand/print", (".png", ".svg")),
    ("Branding — 10 applications merch", "livrables/brand", (".jpg",)),
    ("Pochettes — 34 couvertures catalogue", "livrables/pochettes/catalogue", (".jpg",)),
    ("Pochettes — 10 héros", "livrables/pochettes", (".jpg",)),
    ("Affiches services — 10", "livrables/affiches", (".jpg",)),
    ("Visuels universels — 10", "livrables/universel", (".jpg",)),
    ("Variations laiton — 10", "livrables/variations", (".jpg",)),
]


def files(d, ext):
    p = f"{OUT}/{d}"
    if not os.path.isdir(p):
        return []
    out = [f for f in sorted(os.listdir(p)) if f.lower().endswith(ext) and os.path.isfile(f"{p}/{f}")]
    return out


def human(n):
    return f"{n/1e6:.1f} Mo" if n > 1e6 else f"{n/1e3:.0f} ko"


def main():
    L = []
    A = L.append
    A("# TERMUX — télécharger les livrables DSKY WTBW")
    A("")
    A(f"Branche : `{BRANCH}` · dépôt `{REPO}`")
    A("")
    A("## 0. Préparer Termux (une seule fois)")
    A("")
    A("```bash")
    A("pkg update -y && pkg install -y curl unzip ffmpeg")
    A("mkdir -p ~/storage/shared/DSKY-WTBW && termux-setup-storage")
    A("cd ~/storage/shared/DSKY-WTBW")
    A("```")
    A("")
    A("## 1. Le plus rapide : le script qui télécharge tout (~90 Mo)")
    A("")
    A("```bash")
    A(f"curl -L -o get.sh {RAW}/get-livrables.sh")
    A("bash get.sh")
    A("```")
    A("")
    A("> Il crée les dossiers (`films/`, `brand/`, `pochettes/`, `affiches/`, `visuels/`,")
    A("> `variations/`) et y range chaque fichier. Relançable : il reprend où il s'est arrêté")
    A("> grâce à `curl -C -`.")
    A("")
    A("> Le zip du dépôt complet est déconseillé depuis le téléphone : l'historique Git pèse")
    A("> plus de 10 Go et le zip de branche embarque les 38 pistes audio.")
    A("")
    A("## 2. Fichier par fichier (curl direct, sans zip)")
    A("")
    A("```bash")
    A("cd ~/storage/shared/DSKY-WTBW && mkdir -p films brand pochettes affiches visuels variations")
    A("```")
    A("")
    total = 0
    for title, d, exts in GROUPS:
        rows = []
        for e in exts:
            for f in files(d, e):
                rows.append(f)
        if not rows:
            continue
        A(f"### {title} — {len(rows)} fichiers")
        A("")
        A("```bash")
        for f in rows:
            src = f"{OUT}/{d}/{f}"
            size = os.path.getsize(src)
            total += size
            A(f"curl -L -o \"{f}\" \\")
            A(f"  {RAW}/{d}/{f}    # {human(size)}")
        A("```")
        A("")
    A(f"Total des fichiers ci-dessus : **{human(total)}**.")
    A("")
    A("## 3. Vérifier après téléchargement")
    A("")
    A("```bash")
    A("# durées et poids des films")
    A('for f in films/*.mp4; do echo -n "$f  "; ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"; done')
    A("")
    A("# nombre d'images récupérées")
    A("ls pochettes | wc -l      # attendu : 34")
    A("ls affiches  | wc -l      # attendu : 10")
    A("```")
    A("")
    A("## 4. Publier depuis le téléphone")
    A("")
    A("| Production | Où | Format |")
    A("|---|---|---|")
    A("| Films mariage / mémoire / anniversaire / éducation | TikTok, Reels, Statut WhatsApp, YouTube Shorts | 9:16, 16–24 s |")
    A("| Film catalogue 34 | YouTube (non répertorié), bio TikTok | 9:16, 29 s |")
    A("| Pochettes | IG / FB (carrousel), YouTube (miniature) | 1080×1080 |")
    A("| Affiches services | Statut WhatsApp, Facebook | 1080×1350 |")
    A("| Fichiers imprimeur | flocage, broderie, cartes | PNG transparent / SVG |")
    A("")
    A("> Astuce Termux : `termux-open --content-type video/mp4 films/FILM-MARIAGE-9x16.mp4`")
    A("> ouvre directement le film dans le lecteur du téléphone.")
    open(f"{OUT}/TERMUX.md", "w").write("\n".join(L) + "\n")

    # script de téléchargement direct (Termux / Linux / macOS)
    SH = ["#!/bin/sh",
          "# get-livrables.sh — DSKY WTBW : télécharge tous les livrables (repris possible)",
          "set -u",
          'DEST="${1:-$HOME/storage/shared/DSKY-WTBW}"',
          'mkdir -p "$DEST/films" "$DEST/brand" "$DEST/brand-print" "$DEST/pochettes" \\',
          '         "$DEST/affiches" "$DEST/visuels" "$DEST/variations" || exit 1',
          'cd "$DEST" || exit 1',
          ""]
    FOLD = {"livrables": "films", "livrables/brand/print": "brand-print",
            "livrables/brand": "brand", "livrables/pochettes/catalogue": "pochettes",
            "livrables/pochettes": "pochettes", "livrables/affiches": "affiches",
            "livrables/universel": "visuels", "livrables/variations": "variations"}
    n = 0
    for title, d, exts in GROUPS:
        for e in exts:
            for f in files(d, e):
                n += 1
                SH.append(f'echo "[{n}] {f}"')
                SH.append(f'curl -L -C - --retry 4 -sS -o "{FOLD[d]}/{f}" "{RAW}/{d}/{f}"')
    SH += ["", 'echo', 'echo "Terminé : $DEST"', 'ls -1 films']
    open(f"{OUT}/get-livrables.sh", "w").write("\n".join(SH) + "\n")
    os.chmod(f"{OUT}/get-livrables.sh", 0o755)
    print("get-livrables.sh", n, "fichiers")
    print("TERMUX.md", human(total))


if __name__ == "__main__":
    main()
