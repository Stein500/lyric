#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  DSKY QUOTES 🇧🇯 — TOUT TÉLÉCHARGER DANS UN SEUL DOSSIER (v4)
#  Usage Termux :
#    bash dsky-dl.sh        → TOUTES les images publiées
#    bash dsky-dl.sh 221    → seulement les numéros à partir de 221
#  · Relançable à volonté : ne télécharge que les nouveautés.
#  · v4 : argument numéro de départ + réessais auto (réseau faible).
# ============================================================
DEST="/storage/emulated/0/Web+/DSKY-QUOTES"
BASE="https://raw.githubusercontent.com/Stein500/lyric/main/dsky-quotes"
API="https://api.github.com/repos/Stein500/lyric"
START="$1"   # optionnel : numéro de départ (ex : 221)

mkdir -p "$DEST" || { echo "!! Storage inaccessible — lance d'abord : termux-setup-storage"; exit 1; }
echo "== DSKY QUOTES 🇧🇯 → $DEST =="
[ -n "$START" ] && echo "   (filtre : numéros à partir de $START)"

# 1) SHA du sous-arbre dsky-quotes (petit, jamais tronqué)
SHA=$(curl -sL --retry 3 --conn-timeout 15 "$API/git/trees/main" \
  | grep -A4 '"path": "dsky-quotes"' \
  | grep -o '"sha": *"[a-f0-9]*"' | head -1 | grep -o '[a-f0-9]\{40\}')
[ -n "$SHA" ] || { echo "!! SHA introuvable (réseau ?) — réessaie."; exit 1; }

# 2) Liste complète des .jpg des dossiers publiés (1 appel API)
RESP=$(curl -sL --retry 3 --conn-timeout 15 "$API/git/trees/$SHA?recursive=1")
echo "$RESP" | grep -q '"truncated": *true' && echo "   (arbre tronqué — relance une 2e fois)"
LIST=$(echo "$RESP" \
  | grep -o '"path": *"[^"]*\.jpg"' \
  | sed 's/"path": *"//;s/"$//' \
  | grep -E '^(salve-0[0-9]|saison-02)/')

[ -n "$LIST" ] || { echo "!! Liste vide (réseau ?) — réessaie."; exit 1; }

total=$(echo "$LIST" | wc -l)
echo "   $total images publiées trouvées en ligne."
new=0; skip=0; out=0
for p in $LIST; do
  f="$DEST/$(basename "$p")"
  if [ -n "$START" ]; then
    n=$(basename "$p" | sed 's/[^0-9]//g')
    [ -n "$n" ] || n=0
    if [ "$n" -lt "$START" ]; then out=$((out+1)); continue; fi
  fi
  if [ -s "$f" ]; then skip=$((skip+1)); continue; fi
  curl -sL --fail --retry 3 --conn-timeout 15 -o "$f" "$BASE/$p" \
    && new=$((new+1)) || { echo "   !! échec : $p"; rm -f "$f"; }
done

echo "== Terminé : $new nouveaux, $skip déjà présents =="
if [ -n "$START" ]; then echo "   ($out fichiers ignorés : numéros avant $START)"; fi
echo "   Total dans le dossier : $(ls "$DEST" | wc -l) fichiers"
