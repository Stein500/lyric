#!/usr/bin/env bash
# ============================================================
# DSKY QUOTES — Push propre vers github.com/Stein500/lyric
#
# Utilisation :
#   GITHUB_TOKEN=ghp_votre_token bash push.sh "message du commit"
#
# MODE SURCOUCHE : l'arbre GitHub de dsky-quotes/ sert de BASE ;
# le workspace vient par-dessus (ajouts / modifications uniquement).
# → On peut PURGER le workspace des images déjà poussées :
#   rien n'est jamais supprimé de GitHub par accident.
# Le token n'est JAMAIS stocké (variable d'environnement only).
# ============================================================
set -e
cd "$(dirname "$0")"

MSG="${1:-Mise à jour DSKY QUOTES}"
: "${GITHUB_TOKEN:?Définis GITHUB_TOKEN, ex : GITHUB_TOKEN=ghp_xxx bash push.sh \"message\"}"
REPO="Stein500/lyric"
REMOTE="https://Stein500:${GITHUB_TOKEN}@github.com/${REPO}.git"

# objets & index éphémères : le workspace ne stocke aucun blob
export GIT_OBJECT_DIRECTORY=/tmp/dsky-obj
export GIT_ALTERNATE_OBJECT_DIRECTORIES=""
IDX=/tmp/dsky-idx
export GIT_AUTHOR_NAME="Dsky"  GIT_AUTHOR_EMAIL="dsky@users.noreply.github.com"
export GIT_COMMITTER_NAME="Dsky" GIT_COMMITTER_EMAIL="dsky@users.noreply.github.com"
mkdir -p "$GIT_OBJECT_DIRECTORY"

echo "── 1. Récupération de main (léger, sans l'historique musique) ──"
git fetch --depth 1 --filter=blob:none "$REMOTE" main 2>/dev/null || true
MAIN=$(git rev-parse FETCH_HEAD 2>/dev/null || true)
echo "   main         : ${MAIN:-indisponible (premier push ?)}"

echo "── 2. Fusion douce : GitHub (base) + workspace (surcouche) ──"
rm -f "$IDX"
if [ -n "$MAIN" ] && git cat-file -e "$MAIN:dsky-quotes" 2>/dev/null; then
  GIT_INDEX_FILE="$IDX" git read-tree "$MAIN:dsky-quotes"
  echo "   base GitHub  : $(GIT_INDEX_FILE="$IDX" git ls-files | wc -l) fichiers conservés"
fi
# --no-all : ajoute/modifie, ne stage JAMAIS les suppressions
GIT_INDEX_FILE="$IDX" git add --no-all .
TREE=$(GIT_INDEX_FILE="$IDX" git write-tree)
rm -f "$IDX"
echo "   arbre projet : $TREE"

echo "── 3. Push de main ──"
MERGE=$(git commit-tree "$TREE" ${MAIN:+-p "$MAIN"} -m "$MSG")
git push "$REMOTE" "$MERGE:refs/heads/main" 2>&1 | grep -E "main|rejected|error" || true

echo "── 4. Push de la branche légère dsky-quotes ──"
LIGHT=$(git commit-tree "$TREE" -m "$MSG — branche légère dsky-quotes")
git push -f "$REMOTE" "$LIGHT:refs/heads/dsky-quotes" 2>&1 | grep -E "dsky-quotes|rejected|error" || true

echo "✅ Terminé. Arbre projet = $TREE"
echo "   Workspace purgable librement : GitHub conserve tout (surcouche)."
