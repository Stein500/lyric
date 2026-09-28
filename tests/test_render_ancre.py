"""Géométrie, lisibilité et badges de l'ancre (aucun appel IA)."""
from pathlib import Path
import sys
import unittest

import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import analyse_chanson
import render_ancre as renderer


class CompositingTests(unittest.TestCase):
    def test_flag_exact_pixels_and_bounds(self):
        image = Image.new('RGB', (1080, 1920), (1, 2, 3))
        renderer.draw_flag(image, (0, 1866, 1080, 54))
        self.assertEqual(image.getpixel((0, 1865)), (1, 2, 3))
        self.assertEqual(image.getpixel((359, 1919)), (0, 135, 81))
        self.assertEqual(image.getpixel((360, 1866)), (252, 209, 22))
        self.assertEqual(image.getpixel((1079, 1892)), (252, 209, 22))
        self.assertEqual(image.getpixel((360, 1893)), (232, 17, 45))
        self.assertEqual(image.getpixel((1079, 1919)), (232, 17, 45))

    def test_badge_fades_on_every_verse(self):
        for start, end in [(0, 3), (3, 6), (6, 7.2)]:
            self.assertEqual(renderer.badge_alpha(start, start, end), 0)
            self.assertEqual(renderer.badge_alpha(end, start, end), 0)
            self.assertAlmostEqual(renderer.badge_alpha(start+0.2, start, end), 0.375)
            self.assertAlmostEqual(renderer.badge_alpha(end-0.2, start, end), 0.375)
            self.assertLessEqual(renderer.badge_alpha((start+end)/2, start, end), 0.75)
        self.assertEqual(renderer.badge_alpha(-0.1, 0, 3), 0)
        self.assertEqual(renderer.badge_alpha(3.1, 0, 3), 0)

    def test_all_real_verses_complete_centered_and_safe(self):
        parsed = analyse_chanson.load_lyrics(renderer.ROOT / 'concentré sur le chemin.txt')
        for entry in parsed['entries']:
            with self.subTest(verse=entry['text']):
                layout = renderer.VerseLayout(entry['text'])
                self.assertEqual([w.text for w in layout.words], entry['text'].split())
                self.assertLessEqual(len(layout.lines), 4)
                self.assertGreaterEqual(layout.size, 100)
                x1, y1, x2, y2 = layout.bounds
                self.assertEqual((x1+x2)/2, 540)
                self.assertLessEqual(abs((y1+y2)/2-960), 0.5)
                self.assertGreaterEqual(y1, 710)  # reframed face is above this
                self.assertLess(y2, 1574)
                self.assertLess(x2, 910)
                for left, right in layout.line_centers:
                    self.assertAlmostEqual((left+right)/2, layout.width/2)
                    self.assertGreaterEqual(left, 6)
                    self.assertLessEqual(right, layout.width-6)

    def test_no_missing_song_glyphs(self):
        glyphs = TTFont(renderer.LYRIC_FONT).getBestCmap()
        source = (renderer.ROOT / 'Concentré sur le chemin.lrc').read_text()
        self.assertEqual({c for c in source if not c.isspace() and ord(c) not in glyphs}, set())
        self.assertIn(ord('✓'), TTFont(renderer.UI_FONT).getBestCmap())

    def test_wave_moves_present_text_without_repositioning_verse(self):
        layout = renderer.VerseLayout('Concentré sur le chemin, je regarde plus en arrière')
        before = layout.bounds
        first = np.asarray(layout.layer(1, 0, force_all=True))
        after = np.asarray(layout.layer(1, 0.21, force_all=True))
        self.assertEqual(layout.bounds, before)
        self.assertFalse(np.array_equal(first, after))
        # High-alpha glyphs/stroke must remain within the padded sprite.
        for pixels in [first, after]:
            yy, xx = np.where(pixels[:, :, 3] > 200)
            self.assertGreaterEqual(int(xx.min()), 6)
            self.assertLessEqual(int(xx.max()), layout.width-7)
            self.assertGreaterEqual(int(yy.min()), 6)
            self.assertLessEqual(int(yy.max()), layout.height-7)

    def test_future_words_hidden_and_past_words_preserved(self):
        layout = renderer.VerseLayout('Concentré sur le chemin')
        first = np.asarray(layout.layer(0, 0))
        last = np.asarray(layout.layer(1, 0, force_all=True))
        self.assertGreater(np.count_nonzero(last[:, :, 3]), np.count_nonzero(first[:, :, 3]))
        self.assertEqual(len(layout.words), 4)


if __name__ == '__main__':
    unittest.main()
