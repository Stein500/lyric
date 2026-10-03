#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  DSKY QUOTES 🇧🇯 — TOUT TÉLÉCHARGER DANS UN SEUL DOSSIER
#  Usage Termux :  bash dsky-dl.sh
#  · Récupère TOUTES les images publiées (salves 01-05, saison 2 :
#    story + tiktok + post + couvertures) dans UN dossier unique.
#  · Relançable à volonté : ne télécharge que les nouveautés.
# ============================================================
DEST="/storage/emulated/0/Web+/DSKY-QUOTES"
BASE="https://raw.githubusercontent.com/Stein500/lyric/main/dsky-quotes"
API="https://api.github.com/repos/Stein500/lyric"

mkdir -p "$DEST" || { echo "!! Storage inaccessible — lance d'abord : termux-setup-storage"; exit 1; }
echo "== DSKY QUOTES 🇧🇯 → $DEST =="

# 1) SHA du sous-arbre dsky-quotes (petit, jamais tronqué)
SHA=$(curl -sL "$API/git/trees/main" | grep -A4 '"path": "dsky-quotes"' \
  | grep -o '"sha": *"[a-f0-9]*"' | head -1 | grep -o '[a-f0-9]\{40\}')
[ -n "$SHA" ] || { echo "!! SHA introuvable (réseau ?) — réessaie."; exit 1; }

# 2) Liste complète des .jpg des dossiers publiés (1 appel API)
RESP=$(curl -sL "$API/git/trees/$SHA?recursive=1")
echo "$RESP" | grep -q '"truncated": *true' && echo "   (arbre tronqué — relance une 2e fois)"
LIST=$(echo "$RESP" \
  | grep -o '"path": *"[^"]*\.jpg"' \
  | sed 's/"path": *"//;s/"$//' \
  | grep -E '^(salve-0[0-9]|saison-02)/')

[ -n "$LIST" ] || { echo "!! Liste vide (réseau ?) — réessaie."; exit 1; }

total=$(echo "$LIST" | wc -l)
echo "   $total images publiées trouvées en ligne."
new=0; skip=0
for p in $LIST; do
  f="$DEST/$(basename "$p")"
  if [ -s "$f" ]; then skip=$((skip+1)); continue; fi
  curl -sL --fail -o "$f" "$BASE/$p" && new=$((new+1)) \
    || { echo "   !! échec : $p"; rm -f "$f"; }
done

echo "== Terminé : $new nouveaux, $skip déjà présents =="
echo "   Total dans le dossier : $(ls "$DEST" | wc -l) fichiers"
