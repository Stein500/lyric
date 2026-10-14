#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  DSKY QUOTES 🇧🇯 — TÉLÉCHARGEMENT v5 (par API GitHub)
#  Usage Termux :
#    bash dsky-dl.sh        → TOUTES les images publiées
#    bash dsky-dl.sh 221    → seulement les numéros à partir de 221
#  · v5 : passe par api.github.com (blobs) — contourne les 404
#    de cache que raw.githubusercontent.com peut servir.
#  · Reprise : saute les fichiers déjà téléchargés.
#  · Beaucoup de fichiers ? export GITHUB_TOKEN=... avant (5000 req/h).
# ============================================================
DEST="${DSKY_DEST:-/storage/emulated/0/Web+/DSKY-QUOTES}"
API="https://api.github.com/repos/Stein500/lyric"
RAW="https://raw.githubusercontent.com/Stein500/lyric/main/dsky-quotes"
START="$1"

mkdir -p "$DEST" || { echo "!! Storage inaccessible — lance : termux-setup-storage"; exit 1; }
echo "== DSKY QUOTES v5 (API) → $DEST =="
[ -n "$START" ] && echo "   (filtre : numéros à partir de $START)"

dl() { # dl <url> <fichier-destination>  → télécharge via API/brute
  _u="$1"; _f="$2"
  if [ -n "$AUTH" ]; then
    curl -sL --retry 3 --connect-timeout 20 -H "$AUTH" -H "Accept: application/vnd.github.raw" -o "$_f" "$_u"
  else
    curl -sL --retry 3 --connect-timeout 20 -H "Accept: application/vnd.github.raw" -o "$_f" "$_u"
  fi
}

AUTH=""
[ -n "$GITHUB_TOKEN" ] && AUTH="Authorization: Bearer $GITHUB_TOKEN"

# 1) SHA du sous-arbre dsky-quotes
SHA=$(curl -sL --retry 3 --connect-timeout 20 ${AUTH:+-H "$AUTH"} "$API/git/trees/main" \
  | grep -A4 '"path": "dsky-quotes"' | grep -o '[a-f0-9]\{40\}' | head -1)
[ -n "$SHA" ] || { echo "!! Liste introuvable (réseau ou limite GitHub sans token)."
  echo "   Si ça répète : export GITHUB_TOKEN=ton_token_puis_relance."; exit 1; }

# 2) Liste (chemin + blob sha) en 1 appel API
RESP=$(curl -sL --retry 3 --connect-timeout 20 ${AUTH:+-H "$AUTH"} "$API/git/trees/$SHA?recursive=1")
LIST=$(echo "$RESP" | awk '
  /"path":/ {p=$0; sub(/.*"path": *"/,"",p); sub(/".*/,"",p)}
  /"sha":/  {s=$0; sub(/.*"sha": *"/,"",s); sub(/".*/,"",s); if (p!="") print p" "s; p=""}' \
  | grep '\.jpg' | grep -E '^(salve-0[0-9]|saison-02)/')
[ -n "$LIST" ] || { echo "!! Liste vide (réseau ?) — réessaie."; exit 1; }

total=$(echo "$LIST" | wc -l)
echo "   $total images publiées trouvées."
is_jpg() { head -c 3 "$1" | od -An -tx1 | grep -q 'ff d8 ff'; }

new=0; skip=0; out=0; fail=0
while read -r p s; do
  [ -n "$p" ] || continue
  [ -n "$s" ] || continue
  f="$DEST/$(basename "$p")"
  if [ -n "$START" ]; then
    n=$(basename "$p" | sed 's/[^0-9]//g'); [ -n "$n" ] || n=0
    if [ "$n" -lt "$START" ]; then out=$((out+1)); continue; fi
  fi
  if [ -s "$f" ]; then skip=$((skip+1)); continue; fi
  ok=""
  if dl "$API/git/blobs/$s" "$f.tmp" && [ -s "$f.tmp" ] && is_jpg "$f.tmp"; then
    mv "$f.tmp" "$f"; ok=api
  elif [ -n "$AUTH" ]; then
    curl -sL --retry 3 --connect-timeout 20 -H "$AUTH" -o "$f.tmp" "$RAW/$p" \
      && [ -s "$f.tmp" ] && is_jpg "$f.tmp" && mv "$f.tmp" "$f" && ok=raw
  else
    curl -sL --retry 3 --connect-timeout 20 -o "$f.tmp" "$RAW/$p" \
      && [ -s "$f.tmp" ] && is_jpg "$f.tmp" && mv "$f.tmp" "$f" && ok=raw
  fi
  rm -f "$f.tmp"
  if [ -n "$ok" ]; then echo "   ✔ $(basename "$f") [$ok]"; new=$((new+1))
  else echo "   !! échec : $p"; fail=$((fail+1)); fi
done <<LISTEOF
$LIST
LISTEOF

echo "== Terminé : $new nouveaux, $skip déjà présents, $fail échecs =="
[ -n "$START" ] && echo "   ($out ignorés : numéros avant $START)"
echo "   Total dans le dossier : $(ls "$DEST" | wc -l) fichiers"
if [ "$fail" -gt 0 ] && [ -z "$GITHUB_TOKEN" ]; then
  echo "   Astuce : export GITHUB_TOKEN=... puis relance (limite API 60/h sans token)."
fi
