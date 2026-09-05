#!/usr/bin/env python3
"""Verrouille la timeline complète : 30 fonds, 49 vers, réutilisation autorisée."""
from je_maime_common import *

# Les répétitions restent des événements de texte indépendants sur l'horloge musique.
REUSE = {
    30:22, 31:17, 32:20, 33:23, 34:17, 35:18, 36:19, 37:20,
    38:21, 39:18, 40:15, 41:21, 42:4, 43:22, 44:23, 45:24,
    46:3, 47:8, 48:25, 49:21,
}


def main():
    config, audit = assert_sources_unchanged()
    assert config['approved']['image_reuse_allowed']
    assets = assets_by_slot()
    if sorted(assets) != list(range(30)):
        raise ValueError('Il faut exactement les trente fonds S00 à S29')
    if len({asset['sha256'] for asset in assets.values()}) != 30:
        raise ValueError('Les trente sources générées doivent être distinctes')
    source_samples = audit['decoded_samples_per_channel']
    sr = audit['sample_rate_hz']
    total_samples_target = source_samples + 5 * sr
    total_frames = (total_samples_target * FPS + sr - 1) // sr
    total_duration = total_frames / FPS
    endcard_cs = 18950  # Chute RMS mesurée entre 189,25 et 189,50 s, début du fondu final.
    endcard_frame = (endcard_cs * FPS + 99) // 100
    cues = audit['lrc']['lyrics']
    segments = [{
        'kind':'intro','slot':0,'asset_slot':0,'start_centiseconds':0,
        'end_centiseconds':cues[0]['start_centiseconds'],'first_frame':0,
        'end_frame':cues[0]['first_frame_30fps'],'display_text':config['approved']['title'],
    }]
    for i, cue in enumerate(cues):
        slot = cue['slot']
        source_slot = slot if slot < 30 else REUSE[slot]
        asset = assets[source_slot]
        text = typography(cue['source_text'])
        lines = lyric_lines(text)
        if compact(text) == compact(typography(asset['display_text'])) and asset.get('display_lines'):
            lines = asset['display_lines']
        assert compact(''.join(lines)) == compact(text)
        assert len(lines) <= 3 and all(font(58).getlength(line) <= 920 for line in lines)
        end_cs = cues[i+1]['start_centiseconds'] if i+1 < len(cues) else endcard_cs
        end_frame = (end_cs * FPS + 99) // 100
        segments.append({
            'kind':'lyric','slot':slot,'asset_slot':source_slot,
            'source_timestamp':cue['timestamp'],'source_text':cue['source_text'],
            'start_centiseconds':cue['start_centiseconds'],'end_centiseconds':end_cs,
            'first_frame':cue['first_frame_30fps'],'end_frame':end_frame,
            'display_text':text,'display_lines':lines,'reused_image':source_slot != slot,
        })
    segments.append({
        'kind':'endcard','slot':50,'asset_slot':0,'start_centiseconds':endcard_cs,
        'end_centiseconds':total_duration * 100,'first_frame':endcard_frame,
        'end_frame':total_frames,'reused_image':True,
    })
    for left, right in zip(segments, segments[1:]):
        assert left['end_frame'] == right['first_frame']
    assert segments[0]['first_frame'] == 0 and segments[-1]['end_frame'] == total_frames
    assert sum(s['end_frame']-s['first_frame'] for s in segments) == total_frames
    backgrounds = {}
    for slot, asset in assets.items():
        path = resolve_asset(asset['render_source'])
        backgrounds[str(slot)] = {'path':asset['render_source'],'sha256':sha256(path),'style':asset['style']}
    plan = {
        'version':1, 'title':config['approved']['title'], 'artist':config['approved']['artist'],
        'album':config['approved']['album'], 'genre':'Rap','year':'2026',
        'width':WIDTH,'height':HEIGHT,'fps':FPS,'text_advance_seconds':0.0,
        'source_audio':config['source_audio'],'source_audio_sha256':audit['sha256'],
        'source_duration_seconds':audit['decoded_duration_seconds'],
        'source_samples_per_channel':source_samples,'sample_rate_hz':sr,
        'apad_requested_seconds':5,'total_frames':total_frames,'total_duration_seconds':total_duration,
        'actual_padding_seconds':total_duration-audit['decoded_duration_seconds'],
        'endcard_start_seconds':endcard_cs/100,'endcard_first_frame':endcard_frame,
        'endcard_basis':'Fondu audio final : RMS source de −10,66 à −25,67 dBFS entre les fenêtres 189,25 et 189,50 s.',
        'fade_out_first_frame':total_frames-90,'fade_out_duration_seconds':3,
        'distinct_scene_images':30,'lyric_events':49,
        'reuse_authorized_by_user':True,'new_image_generation_stopped':True,
        'wave':{'amplitude_px':6,'frequency_hz':.9,'letter_phase_radians':.42,'max_entry_seconds':.9,'max_exit_seconds':.45},
        'text':{'font':'DejaVuSans','size':58,'max_width':920,'first_line_top':HEIGHT-300,'line_height':80},
        'badge':{'x':36,'y':36,'width':332,'height':94,'rendered_last':True,'same_rgba_every_frame':True},
        'ken_burns':{'canvas':[1188,2112],'zoom_min':1.02,'zoom_max':1.08,'resample':'OpenCV INTER_CUBIC fractional affine, LANCZOS canvas'},
        'encoding':{'codec':'libx264','preset':'veryfast','crf':19,'pixel_format':'yuv420p','maxrate':'3500k','bufsize':'7000k','aac_bitrate':'192k','faststart':True},
        'video_output':'livrables/Je_maime_tellement_9x16_v1.mp4',
        'mp3_output':'livrables/Je_maime_tellement_master_v1.mp3',
        'backgrounds':backgrounds,'segments':segments,
        'notes':['Aucun recalage des timestamps. Quantification de première frame par plafond, jamais en avance.',
                 'Entrées/sorties des lettres raccourcies sur les fenêtres brèves pour préserver un maintien lisible, sans modifier les fenêtres.',
                 'Les fonds réutilisés sont autorisés explicitement ; aucune concaténation de clips.',
                 'Contrôle utilisateur des mots chantés/onsets demandé après téléchargement ; ne pas prétendre à une écoute indépendante.'],
    }
    dump(PROJECT / 'montage_v1.json', plan)
    config['pending'].pop('endcard_start_seconds',None)
    config['approved']['endcard_start_seconds'] = endcard_cs / 100
    config['approved']['immediate_genre_from_source'] = 'Rap'
    dump(PROJECT / 'cadrage.json', config)
    print(f'Timeline : {total_frames} frames, {total_duration:.6f} s, 49 vers, 30 fonds, endcard à {endcard_cs/100:.2f} s.')


if __name__ == '__main__':
    main()
