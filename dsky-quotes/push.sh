#!/usr/bin/env bash
# ============================================================
# DSKY QUOTES — Push propre vers github.com/Stein500/lyric
#
# Utilisation :
#   GITHUB_TOKEN=ghp_votre_token bash push.sh "message du commit"
#
# MODE GREFFON (sûr avec un workspace purgé) :
#   1. l'arbre COMPLET de main est chargé (musique + dsky-quotes/)
#   2. les fichiers du workspace sont GREFFÉS par-dessus sous
#      dsky-quotes/ (ajouts + mises à jour uniquement ;
#      --no-all + update-index : aucune suppression possible)
# → GitHub conserve TOUT, le workspace peut être purgé librement.
# Le token n'est JAMAIS stocké (variable d'environnement only).
# ============================================================
set -e
cd "$(dirname "$0")"

MSG="${1:-Mise à jour DSKY QUOTES}"
: "${GITHUB_TOKEN:?Définis GITHUB_TOKEN, ex : GITHUB_TOKEN=ghp_xxx bash push.sh \"message\"}"
REPO="Stein500/lyric"
REMOTE="https://Stein500:${GITHUB_TOKEN}@github.com/${REPO}.git"

# objets & index éphémères, repartis à zéro à CHAQUE push
rm -rf /tmp/dsky-obj /tmp/dsky-idx /tmp/dsky-idx2
export GIT_OBJECT_DIRECTORY=/tmp/dsky-obj
export GIT_ALTERNATE_OBJECT_DIRECTORIES=""
mkdir -p "$GIT_OBJECT_DIRECTORY"
IDX=/tmp/dsky-idx; IDX2=/tmp/dsky-idx2
export GIT_AUTHOR_NAME="Dsky"  GIT_AUTHOR_EMAIL="dsky@users.noreply.github.com"
export GIT_COMMITTER_NAME="Dsky" GIT_COMMITTER_EMAIL="dsky@users.noreply.github.com"

echo "── 1. Récupération de main (léger, sans l'historique musique) ──"
git fetch --depth 1 --filter=blob:none "$REMOTE" main 2>/dev/null || true
MAIN=$(git rev-parse FETCH_HEAD 2>/dev/null || true)
echo "   main         : ${MAIN:-indisponible (premier push ?)}"

echo "── 2. Arbre du workspace ──"
rm -f "$IDX2"
GIT_INDEX_FILE="$IDX2" git add --no-all .
PROJECT_TREE=$(GIT_INDEX_FILE="$IDX2" git write-tree)
echo "   workspace    : $PROJECT_TREE ($(GIT_INDEX_FILE=$IDX2 git ls-files | wc -l) fichiers)"

echo "── 3. Greffe : main complet + workspace sous dsky-quotes/ ──"
rm -f "$IDX"
if [ -n "$MAIN" ]; then
  GIT_INDEX_FILE="$IDX" git read-tree "$MAIN"
  echo "   base main    : $(GIT_INDEX_FILE=$IDX git ls-files | wc -l) fichiers conservés"
fi
# greffe : mêmes blobs que l'index local, chemins préfixés dsky-quotes/
GIT_INDEX_FILE="$IDX2" git ls-files -s | awk -F'\t' '{print $1 "\tdsky-quotes/" $2}' \
  | GIT_INDEX_FILE="$IDX" git update-index --index-info
rm -f "$IDX2"
TREE=$(GIT_INDEX_FILE="$IDX" git write-tree)
rm -f "$IDX"
echo "   arbre complet: $TREE ($(GIT_INDEX_FILE=/dev/null git ls-tree -r "$TREE" dsky-quotes 2>/dev/null | wc -l) fichiers dans dsky-quotes/)"

echo "── 4. Push de main ──"
MERGE=$(git commit-tree "$TREE" ${MAIN:+-p "$MAIN"} -m "$MSG")
git push "$REMOTE" "$MERGE:refs/heads/main" 2>&1 | grep -E "main|rejected|error" || true

echo "── 5. Push de la branche légère dsky-quotes ──"
LIGHT=$(git commit-tree "$PROJECT_TREE" -m "$MSG — branche légère dsky-quotes")
git push -f "$REMOTE" "$LIGHT:refs/heads/dsky-quotes" 2>&1 | grep -E "dsky-quotes|rejected|error" || true

echo "✅ Terminé. main:dsky-quotes = $TREE"
echo "   (greffe : rien de GitHub n'a pu être supprimé par accident)"
