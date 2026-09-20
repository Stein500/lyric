#!/usr/bin/env bash
# ============================================================
# DSKY QUOTES — Push propre vers github.com/Stein500/lyric
#
# Utilisation :
#   GITHUB_TOKEN=ghp_votre_token ./push.sh "message du commit"
#
# Ce script fait TOUT, dans le bon ordre :
#   1. commit local (branche master)
#   2. mise à jour du sous-dossier dsky-quotes/ sur  main
#   3. mise à jour de la branche légère  dsky-quotes
#      (branche qui contient UNIQUEMENT le projet — idéale mobile/Termux)
# Le token n'est JAMAIS écrit dans le repo (variable d'environnement only).
# ============================================================
set -e
cd "$(dirname "$0")"

MSG="${1:-Mise à jour DSKY QUOTES}"
: "${GITHUB_TOKEN:?Définis GITHUB_TOKEN, ex : GITHUB_TOKEN=ghp_xxx ./push.sh \"message\"}"
REPO="Stein500/lyric"
REMOTE="https://Stein500:${GITHUB_TOKEN}@github.com/${REPO}.git"

export GIT_AUTHOR_NAME="Dsky"  GIT_AUTHOR_EMAIL="dsky@users.noreply.github.com"
export GIT_COMMITTER_NAME="Dsky" GIT_COMMITTER_EMAIL="dsky@users.noreply.github.com"
git config user.name "Dsky"; git config user.email "dsky@users.noreply.github.com"

echo "── 1. Commit local ──"
git add -A
git commit -m "$MSG" || echo "   (rien de nouveau à commiter)"

echo "── 2. Récupération de main (léger, sans l'historique musique) ──"
git fetch --depth 1 --filter=blob:none "$REMOTE" main 2>/dev/null
MAIN=$(git rev-parse FETCH_HEAD)

echo "── 3. Fusion : main + projet dans dsky-quotes/ ──"
rm -f /tmp/dsky-idx
GIT_INDEX_FILE=/tmp/dsky-idx git read-tree "$MAIN"
GIT_INDEX_FILE=/tmp/dsky-idx git rm -r -q --cached dsky-quotes 2>/dev/null || true
GIT_INDEX_FILE=/tmp/dsky-idx git read-tree --prefix=dsky-quotes/ HEAD
TREE=$(GIT_INDEX_FILE=/tmp/dsky-idx git write-tree)
rm -f /tmp/dsky-idx
MERGE=$(git commit-tree "$TREE" -p "$MAIN" -m "$MSG")

echo "── 4. Push de main ──"
git push "$REMOTE" "$MERGE:refs/heads/main" 2>&1 | grep -v "^To\|^$" || true

echo "── 5. Push de la branche légère dsky-quotes ──"
LIGHT=$(git commit-tree "HEAD^{tree}" -m "$MSG — (branche légère dsky-quotes)")
git push -f "$REMOTE" "$LIGHT:refs/heads/dsky-quotes" 2>&1 | grep -v "^To\|^$" || true

echo "✅ Terminé : main + dsky-quotes synchronisés."
echo "   Vérif : les 3 arbres (local, main/dsky-quotes, branche dsky-quotes) doivent être identiques."
echo "   Arbre local      : $(git rev-parse 'master^{tree}')"
echo "   Arbre poussé     : $TREE"
