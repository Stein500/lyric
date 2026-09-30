#!/usr/bin/env python3
"""Écrire les commandes seulement après publication et contrôle des vrais fichiers.

Le hash référence le commit des médias/prompt ; ce document sera nécessairement
committé ensuite. Aucun lien dépendant d'une branche mutable, aucun faux média.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'productions/concentre_sur_le_chemin'
REPOSITORY = 'Stein500/lyric'
BRANCH = 'arena/01a0e931-lyric'
DESTINATION = '/storage/emulated/0/Web+'


def checked_ref(ref: str) -> str:
    if not re.fullmatch(r'[0-9a-f]{40}', ref):
        raise ValueError('Un hash Git complet et immuable de 40 caractères est obligatoire.')
    return ref


def raw_url(path: str, ref: str) -> str:
    checked_ref(ref)
    parts = Path(path).parts
    if Path(path).is_absolute() or '..' in parts or not parts:
        raise ValueError('Le chemin doit être relatif au dépôt, sans remontée.')
    return f'https://raw.githubusercontent.com/{REPOSITORY}/{ref}/{quote(path, safe="/")}'


def download_command(path: str, name: str, ref: str) -> str:
    if Path(name).name != name or name in ('', '.', '..'):
        raise ValueError('Le nom de téléchargement doit être un simple nom de fichier.')
    target = shlex.quote(f'{DESTINATION}/{name}')
    url = shlex.quote(raw_url(path, ref))
    return (f'mkdir -p {shlex.quote(DESTINATION)}; '
            f'curl -fL --retry 5 --retry-delay 3 -C - -o {target} {url}; '
            f'ls -lh {target}')


def verify_metadata(metadata: dict, blob: str, size: int) -> None:
    if metadata.get('type') != 'file' or metadata.get('sha') != blob or metadata.get('size') != size:
        raise ValueError('Le fichier GitHub ne correspond pas au blob/à la taille locaux.')


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def verify_remote(row: dict, ref: str) -> dict:
    path = row['file']
    local = ROOT / path
    if not local.is_file() or local.stat().st_size != row['size_bytes']:
        raise ValueError(f'Fichier local manquant ou taille modifiée : {path}')
    if hashlib.sha256(local.read_bytes()).hexdigest() != row['sha256']:
        raise ValueError(f'Fichier local modifié : {path}')
    blob = git('rev-parse', f'{ref}:{path}')
    if git('hash-object', '--', path) != blob:
        raise ValueError(f'Le hash fourni ne contient pas la version courante de {path}')
    endpoint = f'repos/{REPOSITORY}/contents/{quote(path, safe="/")}?ref={ref}'
    metadata = json.loads(subprocess.check_output(['gh', 'api', endpoint], cwd=ROOT, text=True))
    verify_metadata(metadata, blob, row['size_bytes'])
    # Vérifier aussi le téléchargement raw réel, pas seulement son existence API.
    url = raw_url(path, ref)
    process = subprocess.Popen(
        ['curl', '-fL', '--retry', '2', '--retry-delay', '1', '--connect-timeout', '30', '--max-time', '180', '-sS', url],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    digest = hashlib.sha256()
    count = 0
    while chunk := process.stdout.read(1024 * 1024):
        digest.update(chunk)
        count += len(chunk)
    process.stdout.close()
    error = process.stderr.read().decode('utf-8', errors='replace')
    process.stderr.close()
    code = process.wait(timeout=120)
    if code or count != row['size_bytes'] or digest.hexdigest() != row['sha256']:
        raise RuntimeError(f'Téléchargement raw invalide : {path}, code={code}, octets={count}. {error}')
    print(f'Publié et téléchargé : {row["download_name"]} ({count:,} octets)', flush=True)
    return {'file': path, 'download_name': row['download_name'], 'url': url,
            'git_blob_sha': blob, 'size_bytes': count, 'sha256': digest.hexdigest(),
            'github_contents_verified': True, 'raw_download_verified': True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ref', required=True, help='git rev-parse HEAD après commit/push des médias')
    args = parser.parse_args()
    ref = checked_ref(args.ref)
    if git('branch', '--show-current') != BRANCH:
        raise SystemExit('Rester sur la branche de cette session.')
    git('merge-base', '--is-ancestor', ref, 'HEAD')
    # Le contenu est vérifié au hash par API et raw, même si HEAD avance ensuite.
    manifest = json.loads((STATE / 'delivery_manifest.json').read_text())
    results = [verify_remote(row, ref) for row in manifest['files']]
    (STATE / 'delivery_remote_checks.json').write_text(json.dumps(
        {'date': '2026-09-30', 'repository': REPOSITORY, 'media_commit': ref,
         'files': results, 'status': 'all_files_verified_via_api_and_raw_download'},
        ensure_ascii=False, indent=2) + '\n')
    lines = [
        '# Télécharger le pack — Concentré sur le chemin', '',
        '**Daïsky · deux clips complets, master MP3, trois pochettes, dix fonds et prompts.**', '',
        'Les exports v1 sont contrôlés techniquement. Les fonds sont approuvés ; '
        'le calage mot à mot reste estimé depuis ton LRC, pas encore validé à l’écoute.', '',
        f'Commit immuable des médias et du prompt : `{ref}`. Chaque fichier a été '
        'vérifié par l’API GitHub puis réellement téléchargé et comparé en SHA-256. '
        'Ce document de commandes est enregistré dans le commit suivant.', '',
        '## 1. Préparer Termux une fois', '',
        'Copier cette ligne et accepter l’autorisation Android :', '',
        '```sh', 'pkg update -y; pkg install -y curl ca-certificates coreutils; termux-setup-storage', '```', '',
        '## 2. Télécharger — une ligne entière par fichier', '',
        'Destination : `/storage/emulated/0/Web+/`. Relancer la même ligne après une coupure : '
        '`-C -` reprend le fichier partiel. Les fichiers sont livrés séparément pour éviter '
        'une seconde grosse archive des mêmes vidéos.', '',
    ]
    for row in manifest['files']:
        lines += [f'### {row["label"]}', '',
                  f'[`{row["download_name"]}`]({raw_url(row["file"], ref)}) '
                  f'— **{row["size_bytes"]:,} octets**.', '', '```sh',
                  download_command(row['file'], row['download_name'], ref), '```', '']
    lines += [
        '## 3. Vérifier les téléchargements', '',
        'Après téléchargement du fichier des empreintes :', '', '```sh',
        f'cd {DESTINATION}; sha256sum -c Concentre_sur_le_chemin_SHA256.txt', '```', '',
        'Chaque fichier téléchargé doit afficher `OK`. Un fichier non encore téléchargé '
        'sera signalé comme manquant ; il suffit de lancer sa ligne.', '',
        '## Si Termux signale une erreur', '',
        '- Si le shell affiche seulement `>` : Ctrl+C, puis recoller une ligne complète.',
        '- Une erreur HTTP n’est pas un média : `-fL` évite d’enregistrer la page d’erreur.',
        '- Comparer la taille exacte indiquée ci-dessus. Un MP4/JPG/MP3 de quelques octets '
        'est un fichier raté : supprimer uniquement ce fichier puis relancer.',
        '- Les documents Markdown/LRC peuvent légitimement faire moins de 100 ko ; '
        'ne pas les supprimer pour cette seule raison.',
        '- Si `curl` refuse une reprise parce qu’un fichier local est déjà complet, '
        'vérifier son SHA-256 avant de le supprimer ou de le retélécharger.', '',
        '## Repères d’écoute du clip', '',
        'Le hook dure 6,90 s ; ensuite la chanson commence depuis son début. '
        'Écouter notamment **00:32,20**, **01:32,54** et **02:39,74** dans les clips. '
        'Les tests audio n’ont mesuré aucune dérive du montage sur ces trois passages ; '
        'cela ne prouve pas l’alignement phonétique de chaque mot.', '',
    ]
    output = ROOT / 'livrables/TERMUX_Concentre_sur_le_chemin_COMPLET.md'
    output.write_text('\n'.join(lines), encoding='utf-8')
    print(output.relative_to(ROOT), flush=True)


if __name__ == '__main__':
    main()
