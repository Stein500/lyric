# LIVRAISON FINALE — « Goinfres » (Dsky · WTBW) — v6.0

- **Titre exact** : `Goinfres`
- **Artiste** : `Dsky`
- **Signature** : `Wolof TechStein beat wê !` (`WTBW`)
- **Mode** : **MODE PEINT** (47 / 47 vers sur **36 / 36 plans distincts**, dont 5 variantes d'aube dédiées pour le refrain final et l'outro §9)
- **Recette** : **STUDIO ANIME SEINEN — Noir & Blanc (`#050608` / `#FFFFFF` / `#2A2E35`), décors atténués & expressions faciales variées** (validée par l'artiste)
- **Habillage v6.0** :
  - **Zéro système de code** (aucune accroche « regarde jusqu'à la fin pour le code », aucun code à 4 chiffres sur la carte finale).
  - **Carte d'accueil WTBW en 2 temps (`0,00 s → 5,30 s → 10,60 s`)** : `SALUT · WTBW` / `Wolof TechStein beat wê` / `GOINFRES — DSKY` puis `BIENVENUE SUR WTBW` / `Soutiens le son en douceur :`, accompagnée des **3 stickers vectoriels animés en douceur** :
    1. **Cœur vectoriel** : `LIKE LA VIDÉO` (*Laisse un cœur si tu valides*)
    2. **Bouton `+` vectoriel** : `CLIQUE SUR + POUR T'ABONNER` (*Rejoins Wolof TechStein beat wê*)
    3. **Bulle de dialogue vectorielle** : `COMMENTE SI TU AIMES !` (*Dis-nous ton vers préféré*)
  - **Carte finale WTBW (`222,92 s → 227,92 s`)** : `MERCI D'AVOIR ÉCOUTÉ !` / `Wolof TechStein beat wê (WTBW)` / `GOINFRES · DSKY` + les **3 stickers vectoriels animés en douceur** (sans code).
  - **7 fenêtres Clochettes CTA `≥ 4,0 s`** (`16,89→23,41 s`, `39,87→50,26 s`, `85,65→89,76 s`, `106,04→116,32 s`, `151,48→155,96 s`, `184,25→193,71 s`, `199,98→222,92 s`).

## Contrôles obligatoires mesurés (§12)

| Contrôle | Outil / Commande | Valeur mesurée | Statut |
|---|---|---|---|
| Durée vidéo | `ffmpeg -i` | `00:03:47.93` (`227,933 s`, `6 838 frames` @ 30 fps) | **OK** |
| Taille MP4 | `os.path.getsize` | `47 823 568` octets (`45,61 Mo`) | **OK** |
| Frames noires | `blackdetect=d=0.05:pix_th=0.10` | **`0`** événement | **OK** |
| Gel d'image | `freezedetect=n=-33dB:d=2.5` | **0** pendant les vers actifs (uniquement cartes / fenêtres CTA éteintes) | **OK** |
| Loudness intégré | `ebur128` | **`-14,0 LUFS`** (`LRA = 8,3 LU`) | **OK** |
| True Peak / Max | `ebur128` / `astats` | **`-1,8 dBFS TP`** / **`-2,11 dB`** (`≤ -1,0 dB`) | **OK** |
| Faststart | Octets atomes MP4 | `moov` à l'octet `36` < `mdat` à l'octet `243 860` | **OK** |
| Typographie 1:1 | `CONTROLE-typo-zoom.jpg` | Nette à 1:1, **0 doublement de lettre (0 ghosting)** | **OK** |
| Master Audio MP3 | `Goinfres - master 320k.mp3` | `320 kbps` CBR, `48 kHz`, ID3v2.4 complet (`APIC` 1080², `USLT` propre, `TIT2`, `TPE1`, `TXXX`) | **OK** |
