"""Contrôles reproductibles des dix fonds et de leurs corrections locales."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
import zipfile

import numpy as np
from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import prepare_backgrounds as backgrounds
from render_ancre import reframe_background, draw_flag


class BackgroundTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = backgrounds.ROOT
        cls.records = json.loads((cls.root/'productions/concentre_sur_le_chemin/backgrounds_manifest.json').read_text())
        cls.jobs = json.loads(backgrounds.PLAN.read_text())

    def test_exactly_five_scenes_in_each_format(self):
        self.assertEqual(len(self.records), 10)
        for fmt in ('portrait', 'landscape'):
            rows = [r for r in self.records if r['format'] == fmt]
            self.assertEqual({r['slot'] for r in rows}, set(backgrounds.NAMES))
            self.assertEqual(len(rows), 5)
            self.assertEqual(len(list((backgrounds.RAW/fmt).glob('s*.png'))), 5)

    def test_exports_have_correct_dimensions_colors_and_hashes(self):
        for row in self.records:
            with self.subTest(format=row['format'], scene=row['slot']):
                path = self.root/row['export']
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row['export_sha256'])
                with Image.open(path) as image:
                    self.assertEqual(image.size, (1080, 1920) if row['format']=='portrait' else (1920, 1080))
                    backgrounds.verify_flag(image.convert('RGB'), row['flag_height'], tolerance=5)
                self.assertEqual(row['technical_status'], 'ready_for_artist_review')
                self.assertFalse(row['badge_baked_in'])

    def test_review_status_does_not_invent_artist_approval(self):
        approved = [(r['format'], r['slot']) for r in self.records if r['artist_approved']]
        self.assertEqual(approved, [('portrait', 's01')])

    def test_raw_images_match_recorded_generations(self):
        jobs = {j['slot']: j for j in self.jobs}
        for row in self.records:
            actual = hashlib.sha256((self.root/row['raw']).read_bytes()).hexdigest()
            self.assertEqual(row['raw_sha256'], actual)
            if row['format'] == 'landscape':
                self.assertEqual(actual, jobs[row['slot']]['generated_sha256'])
                self.assertNotEqual(actual, jobs[row['slot']]['replaced_sha256'])
                self.assertEqual(row['generation_revision'], 2)

    def test_original_references_plus_approved_anchor_in_every_correction(self):
        expected = ['Samu/Snapchat-1835992965.jpg', 'Samu/Snapchat-1275781156.jpg',
                    'Samu/Snapchat-959878741.jpg',
                    'assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png']
        self.assertEqual(len(self.jobs), 5)
        for job in self.jobs:
            self.assertEqual(job['images'], expected)
            self.assertIn('3 — HERO.', job['prompt'])
            self.assertIn('7 — ANATOMY.', job['prompt'])
            for path in job['images']:
                self.assertTrue((self.root/path).is_file())

    def test_portrait_caption_cleanup_does_not_touch_person(self):
        original = np.asarray(Image.open(backgrounds.RAW/'portrait/s02_dans_le_bruit.png').convert('RGB'))
        corrected = backgrounds.clean_ceiling_caption(original)
        self.assertTrue(np.array_equal(corrected[210:], original[210:]))
        self.assertFalse(np.array_equal(corrected, original))

    def test_landscape_cleanup_does_not_touch_person(self):
        original = np.asarray(Image.open(backgrounds.RAW/'landscape/s03_tenir_le_cap.png').convert('RGB'))
        corrected = backgrounds.clean_reference_stickers(original)
        self.assertTrue(np.array_equal(corrected[:, :600], original[:, :600]))
        self.assertTrue(np.array_equal(corrected[:122], original[:122]))
        self.assertFalse(np.array_equal(corrected, original))

    def test_landscape_reframe_is_translation_not_body_stretch(self):
        source = Image.open(backgrounds.RAW/'landscape/s01_tete_lourde.png').convert('RGB')
        fitted = np.asarray(ImageOps.fit(source, (1920, 1080), method=Image.Resampling.LANCZOS))
        prepared = np.asarray(backgrounds.fit_landscape(source))
        self.assertEqual(prepared.shape, (1080, 1920, 3))
        self.assertTrue(np.array_equal(prepared[:-80], fitted[80:]))

    def test_approved_anchor_composition_unchanged(self):
        path = backgrounds.RAW/'portrait/s01_tete_lourde.png'
        self.assertTrue(np.array_equal(np.asarray(backgrounds.fit_portrait(path, 's01')),
                                       np.asarray(reframe_background(path))))

    def test_flag_geometry_for_both_resolutions(self):
        for width, height, flag_height in [(1080, 1920, 54), (1920, 1080, 30)]:
            image = Image.new('RGB', (width, height), (11, 22, 33))
            draw_flag(image, (0, height-flag_height, width, flag_height))
            backgrounds.verify_flag(image, flag_height)
            self.assertEqual(image.getpixel((0, height-flag_height-1)), (11, 22, 33))
            self.assertEqual(image.getpixel((width//3-1, height-1)), (0, 135, 81))
            self.assertEqual(image.getpixel((width//3, height-flag_height)), (252, 209, 22))
            self.assertEqual(image.getpixel((width-1, height-1)), (232, 17, 45))

    def test_zip_contains_the_ten_current_images(self):
        archive = self.root/'livrables/Concentre_sur_le_chemin_10_images_v2.zip'
        with zipfile.ZipFile(archive) as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(len([p for p in z.namelist() if p.endswith('.jpg')]), 10)
            self.assertIn('LISEZ_MOI.txt', z.namelist())
            for row in self.records:
                name = f"{row['format']}/{Path(row['export']).name}"
                self.assertEqual(hashlib.sha256(z.read(name)).hexdigest(), row['export_sha256'])


if __name__ == '__main__':
    unittest.main()
