#!/usr/bin/env python3
"""Un seul référentiel temporel, basé sur le LRC de l'artiste.

Départs de vers conservés. Les mots utilisent une estimation syllabique guidée
par les pics proches, et non un alignement vocal prétendument validé. L'accès
aux poids du modèle vocal est indisponible ; aucun texte n'est transcrit ou réécrit.
"""
from pathlib import Path
import json
import math
import re
import unicodedata

import numpy as np

from analyse_chanson import load_lyrics, audit_timings

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT/'productions/concentre_sur_le_chemin'
DURATION = 213.16
HOOK_START, HOOK_END = 113.28, 120.18
HOOK = round(HOOK_END-HOOK_START, 2)
PADDING = 5.0
FPS = 30
LEAD = 0.03
SECTIONS = [
    (0.0, 'intro', 's01'), (25.30, 'refrain_1', 's03'),
    (38.96, 'couplet_1', 's02'), (59.32, 'pre_refrain_1', 's04'),
    (66.71, 'refrain_2', 's03'), (81.30, 'interlude_1', 's01'),
    (85.64, 'couplet_2', 's02'), (106.60, 'pre_refrain_2', 's04'),
    (113.28, 'refrain_3', 's03'), (127.70, 'interlude_2', 's05'),
    (140.00, 'pont', 's04'), (152.84, 'refrain_final', 's03'),
    (168.10, 'outro', 's05'),
]


def syllable_weight(word):
    plain = ''.join(c for c in unicodedata.normalize('NFD', word.casefold())
                    if not unicodedata.combining(c)).replace('œ', 'oe')
    groups = re.findall('[aeiouy]+', plain)
    # Keep short function words visible without giving them the duration of a noun.
    return max(0.65, len(groups) + 0.035*len(re.sub('[^a-z]', '', plain)))


def end_cap(text, start, next_start):
    """Explicit display caps prevent an ad-lib staying through an instrumental."""
    gap = next_start-start
    if gap <= 4.8:
        return next_start-0.055, 'next_source_verse_minus_55ms'
    if text.startswith('Wolof TechStein'):
        cap = 3.1 if start < 20 else (4.0 if start > 170 else 2.45)
    elif text == 'Wassého...':
        cap = 2.25
    elif text.startswith('Yeah...'):
        cap = 4.5
    elif text.startswith('Concentré...'):
        cap = 5.3
    elif text.startswith('(Toujours'):
        cap = 4.2
    else:
        cap = min(gap-0.1, max(2.2, sum(syllable_weight(w) for w in text.split())*.27+0.65))
    return min(next_start-0.055, start+cap), 'bounded_adlib_display_estimate'


def build():
    parsed = load_lyrics(ROOT/'concentré sur le chemin.txt')
    entries = parsed['entries']
    if audit_timings(entries, DURATION):
        raise AssertionError('Les heures source doivent être corrigées avant rendu.')
    analysis_path = ROOT/'work/concentre_sur_le_chemin/analyse.json'
    analysis = json.loads(analysis_path.read_text()) if analysis_path.exists() else {}
    onsets = np.array(analysis.get('features', {}).get('onsets', []))
    verses = []
    for i, source in enumerate(entries):
        start = source['start']
        following = entries[i+1]['start'] if i+1 < len(entries) else DURATION
        end, end_method = end_cap(source['text'], start, following)
        words = source['text'].split()
        weights = np.array([syllable_weight(word) for word in words])
        available = max(0.35, end-start-0.28)
        targets = start+np.r_[0, np.cumsum(weights[:-1])/weights.sum()*available]
        starts = [start]
        for j, target in enumerate(targets[1:], 1):
            suggestion = float(target)
            if len(onsets):
                candidate = float(onsets[np.argmin(np.abs(onsets-target))])
                if abs(candidate-target) <= 0.065:
                    suggestion = candidate
            latest = end-0.12-0.055*(len(words)-j)
            starts.append(round(max(starts[-1]+0.055, min(latest, suggestion)), 5))
        timed_words = [{'text': word, 'start': round(starts[j], 5),
                        'end': round(starts[j+1] if j+1 < len(words) else end, 5)}
                       for j, word in enumerate(words)]
        name, slot = next((name, slot) for time, name, slot in reversed(SECTIONS) if start >= time)
        verses.append({'id': i+1, 'text': source['text'], 'start': start,
                       'end': round(end, 5), 'source_line': source['line'],
                       'section': name, 'slot': slot, 'end_method': end_method,
                       'words_method': 'syllable_weighted_nearby_onsets_not_forced_vocal_alignment',
                       'words': timed_words})
    sections = [{'start': start, 'end': SECTIONS[i+1][0] if i+1 < len(SECTIONS) else DURATION,
                 'name': name, 'slot': slot} for i, (start, name, slot) in enumerate(SECTIONS)]
    total = round(HOOK+DURATION+PADDING, 5)
    frames = math.ceil(total*FPS)
    report = {'title': 'Concentré sur le chemin', 'artist': 'Daïsky',
              'duration_source': DURATION, 'hook_start': HOOK_START, 'hook_end': HOOK_END,
              'hook_duration': HOOK, 'padding': PADDING, 'fps': FPS, 'total': total,
              'frames': frames, 'encoded_duration': frames/FPS, 'lyrics_lead': LEAD,
              'endcard_start': round(HOOK+DURATION-3, 5),
              'verse_starts': 'source_LRC_unchanged',
              'word_alignment': 'estimated_not_forced', 'human_vocal_validation': False,
              'alignment_fallback_reason': 'model weights unavailable: TLS failures on model hosts; use artist LRC without changing the words',
              'sections': sections, 'verses': verses}
    assert len(verses) == 58
    for verse in verses:
        assert 0 <= verse['start'] < verse['end'] <= DURATION
        assert [w['text'] for w in verse['words']] == verse['text'].split()
        assert all(w['start'] < w['end'] for w in verse['words'])
    destination = PRODUCTION/'timings_render.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    (ROOT/'work/concentre_sur_le_chemin/timings_render.json').write_text(destination.read_text())
    print(f'{len(verses)} vers, {sum(len(v["words"]) for v in verses)} mots, {frames} frames, durée {frames/FPS:.6f} s')
    return report


if __name__ == '__main__':
    build()
