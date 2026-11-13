# PROD — MONSTER POSITIVE (config v6.5, verrouillée le 2026-11-13)

```
TITRE        : MONSTER POSITIVE
ARTISTE      : DSKY (confirmé 2026-11-11)
LANGUES      : wolof/fon + français (confirmé 2026-11-11) — VO wolof/fon peinte, pilule FR défilante
PAROLES      : EN ATTENTE — dans le dépôt GitHub de l'artiste (branche main).
               Arena n'a pas de connecteur GitHub, MAIS le sandbox a accès au réseau :
               avec l'URL du dépôt (public), on lit la branche main en direct
               (raw.githubusercontent.com + API api.github.com) et on copie les fichiers ici.
AUDIO        : EN ATTENTE — même source (dépôt GitHub, branche main) ; sera copié tel quel,
               jamais généré ni modifié.
RECETTE      : STUDIO ANIME SEINEN N&B, DÉCORS ATTÉNUÉS & EXPRESSIONS MULTIPLES (défaut = le style v6.0)
               — style et décor laissés libres par l'artiste ; on peut basculer sur WANDANCE (8.4)
               ou ENCRE & FEUILLE D'OR (8.2) si le thème « monster » le demande.
HABILLAGE    : WTBW SALUT + STICKERS DOUX (Like · Clique sur + pour t'abonner · Commente si tu aimes) — SANS CODE
SIGNATURE    : « Wolof TechStein beat 웨 ! » (WTBW)
MODE         : HYBRIDE (verrouillé) — l'artiste a choisi « peintes » + « les traductions qui défilent »
               = paroles peintes dans le visuel (VO) + pilule FR défilante §5.7 pour les passages non français.
               AUCUNE extinction : §5.4 supprimé en v6.5 (règle absolue 2026-11-13) — les paroles peintes restent nettes 100 % du temps.
               Pilule FR : cotes v6.5 §5.7 (y 1444→1556, 32 px auto-fit ≤ 620 px, tracking 6 px, masquée x 198→882).
               Badge clignotant : « DSKY » ↔ « WTBW » (§7.4).
DOSSIER      : productions/monster-positive/  (fonds/ livrables/ fonts/ + verses_map.json + CARTE-VERS.md)
```

## Arborescence

```
productions/monster-positive/
├── PROMPT-UNIVERSEL-v6.5.md     (fait — v6.4 nettoyée, correctifs 2026-11-13)
├── PROMPT-UNIVERSEL-v6.4.md     (archive)
├── PROD-CONFIG.md               (ce fichier)
├── paroles.txt                  (EN ATTENTE)
├── master audio                 (EN ATTENTE — ex. master.mp3)
├── fonds/                       (ancre + plans générés)
├── livrables/                   (clip 9:16, cover, contrôles)
├── fonts/                       (Montserrat…)
├── verses_map.json              (généré par build_map.py)
└── CARTE-VERS.md                (généré depuis verses_map.json)
```

## Prochaines étapes dès réception des fichiers

1. Lire `paroles.txt` (N lignes = N vers) → `build_map.py` → `verses_map.json` + `CARTE-VERS.md`.
2. Mesurer l'audio (`ffmpeg -map 0:a:0 -f null -`, LUFS/TP/LRA/silences) avant toute promesse.
3. Générer `fonds/scene-01-ancre.png` → contrôle → validation artiste (`ANCRE.md`).
4. Salves ≤ 8 plans (référence = ancre), QC à chaque salve (contact sheet + crops 1:1 + `CONTROLE-paroles.jpg`).
5. `lettering.py`/`bake.py` → paroles cuites · `render.py` → clip + contrôles §12 · `cover.py` → couverture TikTok §7.5.
