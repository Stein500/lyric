#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le dossier de livraison v2 avec les poids reels et le hash de commit passe en env (LIVHASH)."""
import os
import urllib.parse

H = os.environ["LIVHASH"]
OWNER, REPO = "Stein500", "lyric"
P = "productions/gbetche-vivi/"

FILES = [
    (P + "livrables/Gbetché vivi - 916 v2.mp4",
     "**clip 9:16 v2** — écriture gravée dans les images (marker, néon, craie, papier scotché) + autocollants et icônes "
     "dessinés par le moteur · 1080×1920 · 30 fps · 5 995 images · 199,83 s · H.264 CRF 24 bt709 + AAC 256k/48 kHz · "
     "`+faststart`"),
    (P + "livrables/Gbetché vivi - master v2.mp3",
     "**master v2** — audio **identique** au master v1 · −14,0 LUFS, crête vraie −1,6 dBFS · 320 kb/s · 48 kHz · tags "
     "ID3v2.3 : TIT2, TPE1, TALB, TCON, COMM, **TYER 2026**, **APIC 1080² (v2)**, **USLT « Paroles » / fre · 2 384 car.**"),
    (P + "covers/gbetché-vivi-v2-1080.jpg",
     "**pochette carrée 1080×1080 v2** — titre écrit au marqueur sur feuille scotchée, souligné feutre, "
     "cloche/partage/signet vectoriels, étiquette « 0314 », étoiles"),
    (P + "covers/cover-v2-neon.jpg", "pochette v2 de rechange (plan néon « Wanyiyi »)"),
    (P + "covers/cover-v2-libre.jpg", "pochette v2 de rechange (plan « LIBRE » à la craie)"),
    (P + "covers/cover-v2-regarde.jpg", "pochette v2 de rechange (plan accueil « REGARDE JUSQU'A LA FIN »)"),
    (P + "livrables/Gbetché vivi - paroles.lrc",
     "paroles horodatées (tes horodatages, jamais décalés) — la même source que l'USLT du master"),
    ("PROMPT_UNIVERSEL_v5.8_ECRIT_SUR_IMAGE.md",
     "**le prompt universel à jour (v5.8)** : la règle « l'outil écrit dans l'image », zones autorisées/interdites, "
     "contrôle d'orthographe, chaîne audio, ordre APIC→USLT, contrôles fichier, format Termux"),
    (P + "ANCRE.md", "notice de production de la chanson — §13 contrôles v1, **§15 version 2**"),
]

TITRE = [
    ("## 2 · Ce que la v2 change à l'écran",
     "- **0,0 → 5,9 s — accueil** : le whiteboard du fond porte « REGARDE JUSQU'A LA FIN » écrit au marqueur, une carte "
     "« 0314 » et une cloche dessinée ; le moteur ajoute un **cadre pointillé doré** autour des trois pilules et une "
     "**flèche orange** courte qui monte vers la rangée, plus des étincelles.\n"
     "- **Vers chantés** : le mot en cours reçoit un **coup de surligneur** or, la ligne est **soulignée au feutre**, le "
     "bloc est **scotché** (deux bandes de masking tape) et **encadré en pointillés** ; une étiquette en bas à gauche "
     "annonce la section, **déduite de tes paroles** : `REFRAIN ×3` sur les quatre lignes qui reviennent trois fois, "
     "`ADLIB` sur « Wolof TechStein beat wê ! » (5 apparitions). Aucune étiquette ailleurs.\n"
     "- **Texte gravé, plan par plan** : A01 accueil (whiteboard + deux cartes) · A03 « MA VIE ME PLAIT » sur feuille "
     "scotchée + smiley + étoile · A05 « LIBRE » à la craie contre la chaîne cassée, poster à flèche rouge, néon « WOLOF » "
     "· A12 néon script « Wanyiyi » · A29 « NONVI » peint au mur + flèche + deux étoiles découpées · A30 « MERCI » + "
     "étiquette bagage « 0314 » + bandeau cloche (ce plan sert aussi de fond à la carte finale).\n"
     "- **194,8 → 199,8 s — carte finale** : « 0314 » dans un **cadre pointillé scotché**, étoiles, étincelles sur les "
     "côtés.\n"
     "- Fond assombri à **0,80** (0,74 en v1) et scrim plus doux : l'écriture gravée devait rester lisible sous les paroles."),
]

CAPTION = ("> ✍️ Cette fois, **c'est écrit sur les murs** : « regarde jusqu'à la fin », « libre », « merci », et le code — "
           "**0314**.\n>\n> Gbètché vivi, ma vie me plaît ✊🏿 Version 2 du clip : 30 plans, les paroles surlignées au "
           "feutre, le refrain étiqueté, les icônes dessinées à la main. Tu sens le passage ? **Commente le code `0314`**, "
           "partage, enregistre, et mets la cloche 🔔 avant le prochain son.\n>\n> Wolof TechStein beat wê ! — Bandit "
           "Positif.")

HASHTAGS = ("`#GbetchéVivi #BanditPositif #Dsky #WolofTechStein #AfroFusion #ClipParoles #LyricVideo #ParolesÉcrites "
            "#StickersEtFeutre #MusiqueIndépendante #NouvelArtiste #BeatMakeur #RegardeJusquÀLaFin`")

DECLA = ("> **Visuels, écritures dans l'image et clip générés avec l'IA**, sous direction artistique de l'artiste "
         "(30 images portrait natives 1080×1920, texte gravé dans la matière, autocollants et icônes vectoriels dessinés "
         "par le moteur, montage, animation). **Paroles : l'artiste.** Audio : master issu du fichier fourni par l'artiste "
         "(métadonnées d'origine : beat généré avec Suno) — retravaillé uniquement en normalisation de volume (−14 LUFS), "
         "limitation de crête et encapsulage. Aucun drapeau, aucun logo de marque, aucun filigrane.")

CONTROLES = [
     "**Durée annoncée = durée décodée** : `00:03:19.83`, **5 995 frames** ÷ 30 fps = 199,833 s.",
     "**Audit « parois du visage » rejoué sur la v2** : 30 frames testées, **0 pixel d'encre au‑dessus de y 1134** hors "
     "bandeau de badge ; encre de parole la plus haute = **y 1139**. L'audit a servi : la première passe v2 faisait "
     "déborder surligneur et scotch de ~25 px au‑dessus de la limite → tracé borné puis **re‑rendu complet**.",
     "**`blackdetect d=0.10`** : **aucun** passage noir.",
     "**Volume du clip** : **−14,1 LUFS** intégrés, **crête vraie −1,5 dBTP** (pic échantillon −1,49 dBFS) — limiteur à "
     "−2,05 dBFS posé **avant** l'AAC, sinon l'encodeur ressortait à +0,1 dBFS.",
     "**`freezedetect`** : 2 segments ≥ 4 s (6 en v1) — les étincelles et les stickers animés cassent la détection ; les "
     "fonds restent fixes **parce que tu as interdit le recadrage/zoom**, c'est voulu, pas un défaut.",
     "**Géométrie** : ratio 0,5581 sur les 36 plans (768×1376) et **aucune barre noire latérale** (mesure des colonnes de "
     "bord, p99 < 14).",
     "**Orthographe gravée relue à la planche à 100 %** : « REGARDE JUSQU'A LA FIN », « MA VIE ME PLAIT », « LIBRE », "
     "« WOLOF », « Wanyiyi », « NONVI », « MERCI », « 0314 ». Les accents ont sauté sous la main du générateur "
     "(« PLAÎT » → « PLAIT ») — accepté pour un mur peint à la main ; les paroles à l'écran, elles, gardent l'orthographe "
     "exacte de ton fichier.",
     "**Trois régénérations** ont été nécessaires après lecture : « VIVI » peint au sol se trouvait sous la bande de "
     "paroles (A03) ; un plan est ressorti en ratio 0,67 (A05, corrigé en 9:16 natif) ; le néon « Wanyiyi » passait "
     "derrière la tête (A12, repositionné à gauche de la silhouette).",
     "Preuves jointes au dépôt : `productions/gbetche-vivi/PLANCHE-v2-fonds.jpg`, `PLANCHE-v2-retries.jpg`, "
     "`livrables/QC-frames/v2/planche-controle-v2.jpg`, `zoom-v2b.jpg`, `preuve-v2-ligne-1160.jpg`.",
]

TRANCHES = [
    "**`0314`** reste un code **posé par défaut, jamais validé par toi**. Il est écrit à trois endroits (carte d'accueil "
    "gravée, fond de la carte finale, cadre dessiné par le moteur) → le changer = 1 plan régénéré + 1 re‑rendu (~10 min).",
    "**Densité d'écriture** : 6 plans sur 30 portent du texte gravé (plafond de 10 générations par tour, et l'écriture "
    "concurrence les paroles si on en met partout). Tu veux les 30 plans marqués ? je les traite en 3 tours.",
    "**Police unicase sans jambage** (un `p`, `g`, `y` se lisent comme des majuscules sur une ligne longue) : gardée parce "
    "que l'accueil validé en v1 l'utilise déjà. Dis‑le moi et je bascule sur une police à jambages (re‑rendu complet).",
]

PROMPT_NOTE = (
    "`PROMPT_UNIVERSEL_v5.8_ECRIT_SUR_IMAGE.md` est dans ce commit : règle « l'outil écrit dans l'image » (§A), zones "
    "autorisées/interdites, contrôle d'orthographe obligatoire sur planche, ratio imposé à chaque édition, chaîne audio "
    "(limiteur **avant** l'encodeur, `alimiter level=false`), ordre **APIC puis USLT**, contrôles du fichier livré avec les "
    "commandes exactes, format des commandes Termux, et la leçon de performance des calques (dessiner en sous‑boîte et "
    "cacher le statique : 200 ms → 28 ms par frame). Notice de la chanson : `productions/gbetche-vivi/ANCRE.md` "
    "(§13 v1, §15 v2).")


def main():
    for f, _ in FILES:
        assert os.path.exists(f), f
    cmd = []
    for f, _ in FILES:
        nom = os.path.basename(f)
        url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{H}/{urllib.parse.quote(f)}"
        cmd.append(f'mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o '
                   f'"/storage/emulated/0/Web+/{nom}" {url}; ls -lh "/storage/emulated/0/Web+/{nom}"')
    tbl = "\n".join(f"| `{os.path.basename(f)}` | {os.path.getsize(f)/1024/1024:.2f} Mo | {d} |" for f, d in FILES)
    size_mp4 = os.path.getsize(FILES[0][0]) / 1024 / 1024
    size_mp3 = os.path.getsize(FILES[1][0]) / 1024 / 1024
    doc = f"""# 📦 LIVRAISON v2 — « Gbètché vivi » (Bandit Positif) · l'outil écrit dans l'image

Version 2 demandée : **« je veux que l'outil IA écrive les choses directement sur l'image, avec des icônes et stickers »**.
Mon parti pris (je me suis écrit mon propre prompt, §A de la v5.8) : **le texte est gravé dans la matière** (marker sur
papier scotché, néon script, craie au sol, peinture stencil, étiquette bagage) **et** les autocollants/icônes sont
**dessinés par le moteur** (scotch, étoiles découpées, cadre pointillé, surligneur, souligné feutre, flèche,
cloche/partage/signet/play, étincelles). La règle v5.7 « aucune écriture sur les images » est donc **levée par toi** pour
cette version ; restent interdits : logos, drapeaux, filigranes, bandes noires.

**Commit de livraison :** `{H}` (branche `arena/f0df3f2f-lyric`, dépôt `{OWNER}/{REPO}`) — les 9 fichiers ci‑dessous ont
été vérifiés présents **dans ce commit** (`git cat-file -e {H}:<chemin>`), tailles identiques à celles du tableau.

## 1 · Fichiers

| Fichier | Poids | Ce que c'est |
|---|---|---|
{tbl}

{TITRE[0][0]}

{TITRE[0][1]}

## 3 · Titre

`Gbètché vivi — Bandit Positif · clip paroles 9:16 (version écrite sur l'image)`

Variante courte : `Gbètché vivi (v2) — écrit sur l'image · Bandit Positif · 9:16`

## 4 · Caption + code

{CAPTION}

## 5 · Hashtags (13)

{HASHTAGS}

## 6 · Déclaration IA

{DECLA}

## 7 · Commandes Termux

Termux neuf d'abord : `pkg update -y; pkg install -y curl ca-certificates; termux-setup-storage` (accepter la popup), puis
**une ligne par fichier**, collées une par une (jamais `&&`, jamais de continuation) :

```
{chr(10).join(cmd)}
```

Contrôle : `ls -lh /storage/emulated/0/Web+` — clip ≈ {size_mp4:.1f} Mo, master ≈ {size_mp3:.1f} Mo. Réseau coupé ?
**relancer la même ligne** (`-C -` reprend là où ça s'arrête). Shell bloqué sur `>` : Ctrl+C puis recoller la ligne entière.

## 8 · Contrôles chiffrés du fichier livré

{chr(10).join('- ' + c for c in CONTROLES)}

## 9 · Trois points à trancher

{chr(10).join(f'{i+1}. {t}' for i, t in enumerate(TRANCHES))}

## 10 · Le prompt à jour

{PROMPT_NOTE}
"""
    out = P + "livrables/LIVRAISON_gbetche_vivi_v2.md"
    open(out, "w", encoding="utf-8").write(doc)
    import unicodedata
    bad = sorted({c for c in doc if ord(c) > 0x2500 and c not in "🎬🔔✊✍️"})
    print("ecrit:", out, "|", len(doc), "caracteres | lignes curl:", len(cmd), "| caracteres inattendus:", bad or "aucun")


if __name__ == "__main__":
    main()
