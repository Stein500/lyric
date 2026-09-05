"""Utilitaires partagés : sources, paroles, polices et mesures audio."""
from __future__ import annotations
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projets/je_maime_tellement'
WORK = ROOT / 'work/out/je_maime_tellement'
DELIVER = ROOT / 'livrables'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
FPS, WIDTH, HEIGHT = 30, 1080, 1920


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha256(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def font(size, bold=False, cursive=False):
    if cursive:
        local = PROJECT / 'assets/fonts/GreatVibes-Regular.ttf'
        if local.is_file() and local.stat().st_size:
            return ImageFont.truetype(str(local), size)
        return ImageFont.truetype(str(FONT_DIR / 'DejaVuSerif.ttf'), size)
    return ImageFont.truetype(str(FONT_DIR / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')), size)


def clean_lyric(text):
    """Uniquement indications scéniques ; aucun remplacement des mots de l'artiste."""
    text = text.strip()
    if text.startswith('Wolof TechStein beat'):
        text = re.sub(r'\([^)]*\)\s*$', '', text).strip()
    if text.startswith('(Je m\'aime tellement') and text.endswith(')'):
        text = text[1:-1]
    return text


def typography(text):
    return re.sub(r',(?=\S)', ', ', clean_lyric(text))


def compact(text):
    return re.sub(r'\s+', '', text)


def wrap(text, face, max_width=920):
    words = text.split()
    lines, current = [], ''
    for word in words:
        candidate = (current + ' ' + word).strip()
        if face.getlength(candidate) <= max_width:
            current = candidate
        else:
            if not current:
                raise ValueError('Mot trop large : ' + word)
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def lyric_lines(text):
    text = typography(text)
    face = font(58)
    prefix = "Je m'aime tellement,"
    if text.startswith(prefix):
        rest = text[len(prefix):].strip()
        result = [prefix] + wrap(rest, face)
    else:
        result = wrap(text, face)
    if len(result) > 3 or any(face.getlength(line) > 920 for line in result):
        raise ValueError(f'Paroles hors zone : {text}')
    if compact(''.join(result)) != compact(text):
        raise ValueError('Le wrap a changé les paroles')
    return result


def assets_by_slot():
    result = {}
    for path in sorted((PROJECT / 'salves').glob('portrait_*.json')):
        for item in load(path)['assets']:
            if item['slot'] in result:
                raise ValueError('Slot source dupliqué')
            result[item['slot']] = item
    return result


def resolve_asset(relative_path, expected_sha=None):
    """Récupération éventuelle depuis le commit d'archive, sans toucher aux originaux.

    Les images lourdes peuvent être sorties de l'arbre courant APRÈS sauvegarde
    Git et rendu. Elles restent disponibles intégralement dans ce commit.
    """
    relative = Path(relative_path)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Chemin de source non relatif au dépôt')
    path = ROOT / relative
    if not path.is_file():
        path = WORK / 'restored_assets' / relative
        if not path.is_file():
            archive_file = PROJECT / 'archive_visuels.json'
            if not archive_file.is_file():
                raise FileNotFoundError(relative_path)
            archive = load(archive_file)
            revision = archive['commit']
            if not re.fullmatch(r'[0-9a-f]{40}', revision):
                raise ValueError('Commit d’archive invalide')
            command = ['git', 'show', f'{revision}:{relative.as_posix()}']
            process = subprocess.run(command, cwd=ROOT, capture_output=True)
            if process.returncode:
                # Cas d'un clone/snapshot à historique partiel : ne pas changer de branche.
                subprocess.run(['git', 'fetch', 'origin', 'arena/01a072d8-lyric'], cwd=ROOT, check=True)
                process = subprocess.run(command, cwd=ROOT, capture_output=True, check=True)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(process.stdout)
    if expected_sha and sha256(path) != expected_sha:
        raise ValueError('Empreinte source invalide : ' + relative_path)
    return path


def measure_loudness(path, prefix_filters='', target_i=-14.0, target_tp=-1.8):
    af = (prefix_filters + ',' if prefix_filters else '') + f'loudnorm=I={target_i}:TP={target_tp}:LRA=11:print_format=json'
    process = subprocess.run([FFMPEG, '-hide_banner', '-nostdin', '-i', str(path), '-vn', '-af', af, '-f', 'null', '-'], capture_output=True, text=True, check=True)
    start, end = process.stderr.rfind('{'), process.stderr.rfind('}') + 1
    if start < 0:
        raise ValueError('Mesures loudnorm absentes')
    return json.loads(process.stderr[start:end]), process.stderr


def decoded_audio_info(path, sample_rate=48000, channels=2):
    # Compter tous les échantillons décodés sans charger tout le PCM en mémoire.
    process = subprocess.Popen([FFMPEG, '-hide_banner', '-nostdin', '-v', 'error', '-i', str(path), '-vn', '-ac', str(channels), '-ar', str(sample_rate), '-f', 'f32le', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    total = 0
    while True:
        part = process.stdout.read(1024 * 1024)
        if not part:
            break
        total += len(part)
    error = process.stderr.read().decode()
    if process.wait() != 0:
        raise RuntimeError(error)
    if total % (4 * channels):
        raise ValueError('PCM incomplet')
    samples = total // (4 * channels)
    return {'samples_per_channel': samples, 'duration_seconds': samples / sample_rate, 'sample_rate_hz': sample_rate, 'channels': channels}


def assert_sources_unchanged():
    config = load(PROJECT / 'cadrage.json')
    audit = load(PROJECT / 'analyse_audio.json')
    assert sha256(ROOT / config['source_audio']) == audit['sha256']
    assert sha256(ROOT / config['source_lrc']) == audit['lrc']['sha256']
    canonical = (ROOT / config['source_lrc']).read_bytes().decode('cp1252').replace('cSur', 'cœur')
    assert (PROJECT / 'paroles_utf8.lrc').read_text(encoding='utf-8') == canonical
    assert config['approved']['text_advance_seconds'] == 0
    return config, audit
