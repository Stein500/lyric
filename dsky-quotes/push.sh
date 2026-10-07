#!/usr/bin/env bash
# ============================================================
# DSKY QUOTES — Push propre vers github.com/Stein500/lyric
#
# Utilisation :
#   GITHUB_TOKEN=ghp_votre_token ./push.sh "message du commit"
#
# Ce script fait TOUT :
#   1. lit l'arbre du projet (worktree) — les objets git vont dans /tmp,
#      le workspace ne grossit JAMAIS
#   2. met à jour le sous-dossier dsky-quotes/ de  main
#   3. met à jour la branche légère  dsky-quotes  (idéale mobile/Termux)
# Le token n'est JAMAIS stocké (variable d'environnement only).
# ============================================================
set -e
cd "$(dirname "$0")"

MSG="${1:-Mise à jour DSKY QUOTES}"
: "${GITHUB_TOKEN:?Définis GITHUB_TOKEN, ex : GITHUB_TOKEN=ghp_xxx ./push.sh \"message\"}"
REPO="Stein500/lyric"
REMOTE="https://Stein500:${GITHUB_TOKEN}@github.com/${REPO}.git"

# objets & index éphémères : le workspace ne stocke aucun blob
export GIT_OBJECT_DIRECTORY=/tmp/dsky-obj
export GIT_ALTERNATE_OBJECT_DIRECTORIES=""
IDX=/tmp/dsky-idx
export GIT_AUTHOR_NAME="Dsky"  GIT_AUTHOR_EMAIL="dsky@users.noreply.github.com"
export GIT_COMMITTER_NAME="Dsky" GIT_COMMITTER_EMAIL="dsky@users.noreply.github.com"
mkdir -p "$GIT_OBJECT_DIRECTORY"

echo "── 1. Arbre du projet depuis le worktree ──"
rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git add -A
PROJECT_TREE=$(GIT_INDEX_FILE="$IDX" git write-tree)
echo "   arbre projet : $PROJECT_TREE"

echo "── 2. Récupération de main (léger, sans l'historique musique) ──"
git fetch --depth 1 --filter=blob:none "$REMOTE" main 2>/dev/null
MAIN=$(git rev-parse FETCH_HEAD)
echo "   main         : $MAIN"

echo "── 3. Fusion : main + projet dans dsky-quotes/ ──"
rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree "$MAIN"
GIT_INDEX_FILE="$IDX" git rm -r -q --cached dsky-quotes 2>/dev/null || true
GIT_INDEX_FILE="$IDX" git read-tree --prefix=dsky-quotes/ "$PROJECT_TREE"
TREE=$(GIT_INDEX_FILE="$IDX" git write-tree)
rm -f "$IDX"
MERGE=$(git commit-tree "$TREE" -p "$MAIN" -m "$MSG")

echo "── 4. Push de main ──"
git push "$REMOTE" "$MERGE:refs/heads/main" 2>&1 | grep -E "main|rejected|error" || true

echo "── 5. Push de la branche légère dsky-quotes ──"
LIGHT=$(git commit-tree "$PROJECT_TREE" -m "$MSG — branche légère dsky-quotes")
git push -f "$REMOTE" "$LIGHT:refs/heads/dsky-quotes" 2>&1 | grep -E "dsky-quotes|rejected|error" || true

echo "✅ Terminé. Contenu vérifiable : arbre projet = $PROJECT_TREE"
echo "   (identique dans main:dsky-quotes et la branche dsky-quotes)"
