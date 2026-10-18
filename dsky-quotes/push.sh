#!/usr/bin/env bash
# ============================================================
# DSKY QUOTES — Push v2 : par API GitHub (OVERLAY, sans risque)
#
# Utilisation :
#   GITHUB_TOKEN=ghp_votre_token bash push.sh "message du commit"
#
# Différence capitale avec la v1 :
#   la v1 reconstruisait dsky-quotes/ à partir du workspace et
#   SUPPRIMAIT du dépôt tout fichier absent du workspace (c'est
#   ainsi que 355 images ont été effacées le 14/10).
#   La v2 FUSIONNE : elle ajoute/met à jour les fichiers du
#   workspace, et NE TOUCHE À AUCUN fichier existant du dépôt.
#   Aucune suppression possible ⇒ aucun effacement accidentel.
#
# Principe :
#   1. arbre du workspace → objets dans /tmp (workspace léger)
#   2. blobs manquants créés via POST /git/blobs (base64)
#   3. arbre construit par morceaux via POST /git/trees
#      (base_tree = arbre distant actuel → fusion garantie)
#   4. commits + refs mises à jour (branche dsky-quotes ET main)
# ============================================================
set -e
cd "$(dirname "$0")"

MSG="${1:-Mise à jour DSKY QUOTES}"
: "${GITHUB_TOKEN:?Définis GITHUB_TOKEN, ex : GITHUB_TOKEN=ghp_xxx bash push.sh \"message\"}"
REPO="Stein500/lyric"
API="https://api.github.com/repos/$REPO"
AUTH="Authorization: Bearer $GITHUB_TOKEN"

# objets éphémères : le workspace ne stocke aucun blob
export GIT_OBJECT_DIRECTORY=/tmp/dsky-obj
export GIT_ALTERNATE_OBJECT_DIRECTORIES=""
export GIT_AUTHOR_NAME="Dsky"  GIT_AUTHOR_EMAIL="dsky@users.noreply.github.com"
export GIT_COMMITTER_NAME="Dsky" GIT_COMMITTER_EMAIL="dsky@users.noreply.github.com"
mkdir -p "$GIT_OBJECT_DIRECTORY"

echo "── 1. Arbre du projet depuis le worktree ──"
IDX=/tmp/dsky-idx
rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git add -A
PROJECT_TREE=$(GIT_INDEX_FILE="$IDX" git write-tree)
echo "   arbre projet : $PROJECT_TREE"
GIT_INDEX_FILE="$IDX" git ls-tree -r "$PROJECT_TREE" > /tmp/dsky-entries.tsv
N_LOC=$(wc -l < /tmp/dsky-entries.tsv)
echo "   $N_LOC fichiers dans le projet."

api() { # api <méthode> <url> [json | @fichier.json] → corps 2xx, sinon 3 essais puis abort
  local m="$1" u="$2" d="$3" try out code body
  local dargs=()
  if [ -n "$d" ]; then
    if [ "${d#@}" != "$d" ]; then dargs=(--data-binary "@${d#@}"); else dargs=(--data "$d"); fi
  fi
  for try in 1 2 3; do
    out=$(curl -s --retry 2 -X "$m" -H "$AUTH" -H "Accept: application/vnd.github+json" \
      -H "Content-Type: application/json" "${dargs[@]}" -w "\n%{http_code}" "$u")
    code=$(printf '%s' "$out" | tail -n1)
    body=$(printf '%s' "$out" | sed '$d')
    case "$code" in 2*) printf '%s' "$body"; return 0 ;; esac
    sleep 3
  done
  echo "!! API $code sur $u"; printf '%s' "$body" | head -c 300; echo; exit 1
}

echo "── 2. État distant (branche dsky-quotes) ──"
BR_TIP=$(api GET "$API/branches/dsky-quotes" | python3 -c "import json,sys; print(json.load(sys.stdin)['commit']['sha'])")
REMOTE_SUB=$(api GET "$API/git/commits/$BR_TIP" | python3 -c "import json,sys; print(json.load(sys.stdin)['tree']['sha'])")
echo "   branche : $BR_TIP"
echo "   arbre distant : $REMOTE_SUB"

api GET "$API/git/trees/$REMOTE_SUB?recursive=1" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for t in d['tree']:
    if t['type']=='blob': print(t['sha'], t['path'])
" > /tmp/dsky-remote.tsv
N_REM=$(wc -l < /tmp/dsky-remote.tsv)
echo "   $N_REM fichiers déjà en ligne."

echo "── 3. Blobs manquants → POST /git/blobs ──"
new_blobs=0
while read -r mode type sha path; do
  [ "$type" = "blob" ] || continue
  if grep -q "^$sha $path\$" /tmp/dsky-remote.tsv; then continue; fi
  if cut -d' ' -f1 /tmp/dsky-remote.tsv | grep -q "^$sha\$"; then continue; fi
  python3 -c "
import base64, json
data = open('$path','rb').read()
open('/tmp/dsky-blob.json','w').write(json.dumps({'content': base64.b64encode(data).decode(), 'encoding': 'base64'}))
"
  RSHA=$(api POST "$API/git/blobs" "@/tmp/dsky-blob.json" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['sha'])")
  if [ "$RSHA" != "$sha" ]; then echo "   !! sha différent pour $path ($RSHA ≠ $sha)"; exit 1; fi
  new_blobs=$((new_blobs+1))
done < /tmp/dsky-entries.tsv
echo "   $new_blobs nouveau(x) blob(s) envoyé(s)."

echo "── 4. Fusion (base_tree = arbre distant) par paquets de 40 ──"
python3 - <<'PYEOF'
import json
entries=[]
for line in open('/tmp/dsky-entries.tsv'):
    mode,typ,sha,path=line.rstrip('\n').split(None,3)
    entries.append({"path":path,"mode":mode,"type":typ,"sha":sha})
CH=40; n=0
for i in range(0,len(entries),CH):
    n+=1
    json.dump({"tree":entries[i:i+CH]}, open(f'/tmp/dsky-chunk-{n:02d}.json','w'))
open('/tmp/dsky-nchunks.txt','w').write(str(n))
PYEOF
BASE="$REMOTE_SUB"
NC=$(cat /tmp/dsky-nchunks.txt)
k=1
while [ "$k" -le "$NC" ]; do
  CK=$(printf '%02d' "$k")
  PAYLOAD=$(python3 -c "
import json
d=json.load(open('/tmp/dsky-chunk-$CK.json')); d['base_tree']='$BASE'
print(json.dumps(d))")
  BASE=$(api POST "$API/git/trees" "$PAYLOAD" | python3 -c "import json,sys; print(json.load(sys.stdin)['sha'])")
  echo "   paquet $k/$NC → $BASE"
  k=$((k+1))
done
NEWSUB="$BASE"

if [ "$NEWSUB" = "$REMOTE_SUB" ]; then
  echo "✅ Rien de nouveau à pousser (arbre identique)."
  exit 0
fi

echo "── 5. Commit + branche dsky-quotes ──"
C1=$(api POST "$API/git/commits" "{\"message\":\"$MSG\",\"tree\":\"$NEWSUB\",\"parents\":[\"$BR_TIP\"]}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['sha'])")
api PATCH "$API/git/refs/heads/dsky-quotes" "{\"sha\":\"$C1\",\"force\":true}" > /dev/null
echo "   dsky-quotes : $BR_TIP → $C1"

echo "── 6. main (racine + pointeur dsky-quotes) ──"
MAIN_TIP=$(api GET "$API/branches/main" | python3 -c "import json,sys; print(json.load(sys.stdin)['commit']['sha'])")
MAIN_TREE=$(api GET "$API/git/commits/$MAIN_TIP" | python3 -c "import json,sys; print(json.load(sys.stdin)['tree']['sha'])")
NEWROOT=$(api POST "$API/git/trees" "{\"base_tree\":\"$MAIN_TREE\",\"tree\":[{\"path\":\"dsky-quotes\",\"mode\":\"040000\",\"type\":\"tree\",\"sha\":\"$NEWSUB\"}]}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['sha'])")
C2=$(api POST "$API/git/commits" "{\"message\":\"$MSG\",\"tree\":\"$NEWROOT\",\"parents\":[\"$MAIN_TIP\"]}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['sha'])")
api PATCH "$API/git/refs/heads/main" "{\"sha\":\"$C2\",\"force\":true}" > /dev/null
echo "   main : $MAIN_TIP → $C2"

echo "✅ Push terminé (overlay — aucun fichier distant supprimé)."
echo "   Arbre projet : $NEWSUB  ($((N_REM + new_blobs)) fichiers en ligne au total)"