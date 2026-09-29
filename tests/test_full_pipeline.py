"""Tests du montage complet sans réencoder les vidéos pendant les tests."""
from pathlib import Path
import hashlib
import io
import json
import math
import sys
import unittest
import wave

import numpy as np
from PIL import Image
from mutagen.mp3 import MP3
from fontTools.ttLib import TTFont

sys.path.insert(0,str(Path(__file__).parents[1]/'scripts'))
from analyse_chanson import load_lyrics
from render_clip import ROOT, ClipRenderer, LyricLayout
from render_ancre import badge_alpha

STATE=ROOT/'productions/concentre_sur_le_chemin'


class TimelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.timeline=json.loads((STATE/'timings_render.json').read_text())
        cls.entries=load_lyrics(ROOT/'concentré sur le chemin.txt')['entries']

    def test_all_verses_preserve_text_and_source_onsets(self):
        verses=self.timeline['verses']
        self.assertEqual(len(verses),58)
        self.assertEqual([(v['text'],v['start']) for v in verses],
                         [(v['text'],v['start']) for v in self.entries])
        self.assertEqual(sum(len(v['words']) for v in verses),389)

    def test_words_monotone_complete_and_inside_verse(self):
        for verse in self.timeline['verses']:
            with self.subTest(verse=verse['id']):
                self.assertEqual([w['text'] for w in verse['words']],verse['text'].split())
                for w in verse['words']:
                    self.assertGreaterEqual(w['start']+1e-7,verse['start'])
                    self.assertLess(w['start'],w['end'])
                    self.assertLessEqual(w['end']-1e-7,verse['end'])
                for a,b in zip(verse['words'],verse['words'][1:]):
                    self.assertLess(a['start'],b['start'])
                self.assertLess(verse['words'][-1]['start'],verse['end']-.15)

    def test_exact_single_frame_clock(self):
        t=self.timeline
        self.assertEqual(t['frames'],math.ceil(t['total']*t['fps']))
        self.assertEqual(t['frames'],6752)
        self.assertAlmostEqual(t['hook_duration']+t['duration_source']+t['padding'],225.06)
        self.assertLess(abs(t['encoded_duration']-t['total']),1/t['fps'])
        self.assertFalse(t['human_vocal_validation'])
        self.assertEqual(t['word_alignment'],'estimated_not_forced')

    def test_adlibs_do_not_extend_into_whole_instrumental_tail(self):
        last=self.timeline['verses'][-1]
        self.assertLessEqual(last['end']-last['start'],4.2+1e-6)
        self.assertLess(last['end'],200)
        for v in self.timeline['verses']:
            self.assertLessEqual(v['end'],self.timeline['duration_source'])

    def test_five_scenes_only(self):
        self.assertEqual({s['slot'] for s in self.timeline['sections']},{'s01','s02','s03','s04','s05'})
        self.assertTrue(json.loads((STATE/'production.json').read_text())['approvals']['image_series'])

    def test_pcm_duration_equals_frame_clock_when_cache_present(self):
        p=ROOT/'work/concentre_sur_le_chemin/video_audio.wav'
        if not p.exists():self.skipTest('PCM cache à régénérer avec produce_audio.py')
        with wave.open(str(p)) as f:
            self.assertEqual(f.getnchannels(),2)
            self.assertEqual(f.getframerate(),48000)
            self.assertEqual(f.getnframes(),self.timeline['frames']*1600)


class FullLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verses=json.loads((STATE/'timings_render.json').read_text())['verses']

    def test_both_formats_complete_large_and_centered(self):
        for fmt,w,h in [('portrait',1080,1920),('landscape',1920,1080)]:
            for verse in self.verses:
                with self.subTest(format=fmt,verse=verse['id']):
                    layout=LyricLayout(verse['text'],fmt)
                    self.assertEqual([e[3] for e in layout.words],verse['text'].split())
                    self.assertGreaterEqual(layout.font_size,100)
                    x1,y1,x2,y2=layout.bounds
                    self.assertEqual((x1+x2)/2,w/2)
                    self.assertLessEqual(abs((y1+y2)/2-h/2),.5)
                    if fmt=='portrait':
                        self.assertLess(x2,910);self.assertLess(y2,1574)
                        # The container includes transparent padding. Account for
                        # the 4.5 px wave and 3 px outline before testing visible ink.
                        self.assertGreater(y1+layout.pad-4.5-3,710)
                    else:
                        self.assertLess(y2,h-120)

    def test_wave_moves_without_clipping_visible_glyphs(self):
        for fmt in ['portrait','landscape']:
            layout=LyricLayout('Concentré sur le chemin, je regarde plus en arrière',fmt)
            bounds=layout.bounds
            images=[np.asarray(layout.layer(len(layout.words)-1,t)) for t in [0,.16,.37]]
            self.assertFalse(np.array_equal(images[0],images[1]))
            self.assertEqual(layout.bounds,bounds)
            for pixels in images:
                yy,xx=np.where(pixels[:,:,3]>200)
                self.assertGreaterEqual(int(xx.min()),6)
                self.assertGreaterEqual(int(yy.min()),6)
                self.assertLessEqual(int(xx.max()),layout.width-7)
                self.assertLessEqual(int(yy.max()),layout.height-7)

    def test_badge_fades_for_every_occurrence(self):
        for verse in self.verses:
            a,b=verse['start']-.03,verse['end']-.03
            self.assertEqual(badge_alpha(a,a,b),0)
            self.assertEqual(badge_alpha(b,a,b),0)
            self.assertAlmostEqual(badge_alpha(a+.2,a,b),.375)
            self.assertLessEqual(badge_alpha((a+b)/2,a,b),.75)

    def test_title_and_lyrics_fonts_cover_exact_text(self):
        fonts=[('BarlowCondensed-Bold.ttf',''.join(v['text'] for v in self.verses)),
               ('GreatVibes-Regular.ttf','Concentré sur le chemin'),('DejaVuSans-Bold.ttf','Dsky Daïsky +229 dais­kyproduction@gmail.com'.replace('\u00ad',''))]
        for filename,text in fonts:
            glyphs=TTFont(ROOT/'assets/fonts'/filename).getBestCmap()
            self.assertEqual({c for c in text if not c.isspace() and ord(c) not in glyphs},set())


class MasterAndCoverTests(unittest.TestCase):
    def test_mp3_tags_audio_properties_and_clean_lyrics(self):
        path=ROOT/'livrables/Concentre_sur_le_chemin_master_320k.mp3'
        song=MP3(path)
        self.assertEqual(song.info.sample_rate,48000)
        self.assertEqual(song.info.bitrate,320000)
        self.assertEqual(song.info.channels,2)
        self.assertEqual(song.tags.version,(2,4,0))
        self.assertEqual(str(song.tags['TIT2']),'Concentré sur le chemin')
        self.assertEqual(str(song.tags['TPE1']),'Daïsky')
        self.assertIn('TXXX:email',song.tags)
        lyrics=song.tags.getall('USLT')[0].text
        self.assertNotIn('[00:',lyrics)
        verses=json.loads((STATE/'timings_render.json').read_text())['verses']
        self.assertEqual(lyrics,'\n'.join(v['text'] for v in verses))
        data=song.tags.getall('APIC')[0].data
        self.assertEqual(data,(ROOT/'livrables/cover_concentre_sur_le_chemin_1080x1080.jpg').read_bytes())
        self.assertEqual(Image.open(io.BytesIO(data)).size,(1080,1080))

    def test_master_measurements_are_measured_and_in_range(self):
        report=json.loads((STATE/'audio_master_report.json').read_text())
        self.assertAlmostEqual(report['decoded_master_duration'],213.16,places=3)
        self.assertLessEqual(float(report['master_mp3_measurement']['input_tp']),-1.5)
        self.assertLess(abs(float(report['master_mp3_measurement']['input_i'])+14),.8)
        path=ROOT/report['file']
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),report['sha256'])

    def test_covers_title_artist_do_not_overlap_and_are_in_safe_margins(self):
        rows=json.loads((STATE/'covers_report.json').read_text())
        self.assertEqual(len(rows),3)
        for row in rows:
            self.assertEqual(row['new_ai_generations'],0)
            with Image.open(ROOT/row['file']) as image:
                self.assertEqual(list(image.size),row['size'])
                w,h=image.size
            a,b=row['title_bbox'],row['artist_bbox']
            self.assertLess(a[3],b[1])
            for box in [a,b]:
                self.assertGreaterEqual(box[0],int(.08*w))
                self.assertLessEqual(box[2],w-int(.08*w))
                self.assertGreaterEqual(box[1],int(.08*h))
                self.assertLessEqual(box[3],h-int(.08*h))


if __name__=='__main__':unittest.main()
