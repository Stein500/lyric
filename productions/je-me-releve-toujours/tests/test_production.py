"""Structural tests only: visual, artistic and sung-word QC still require human review."""
import hashlib
import importlib.util
import io
import json
import math
import unittest
from pathlib import Path

from mutagen.mp3 import MP3
from PIL import Image

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_module("build_map_test", PROJECT / "build_map.py")
        cls.renderer = load_module("render_test", PROJECT / "render_9x16.py")
        cls.rows = json.loads((PROJECT / "verses_map.json").read_text(encoding="utf-8"))

    def test_source_lyrics_and_timestamps_unchanged(self):
        source = self.builder.read_lyrics()
        self.assertEqual(len(source), 58)
        self.assertEqual(len(self.rows), len(source))
        for original, row in zip(source, self.rows):
            self.assertEqual(row["source_timestamp"], original["source_timestamp"])
            self.assertEqual(row["t"], original["t"])
            self.assertEqual(row["texte"], original["texte"])
            delay = math.ceil(row["t"] * 30 - 1e-9) / 30 - row["t"]
            self.assertGreaterEqual(delay, -1e-9)
            self.assertLess(delay, 1 / 30 + 1e-9)

    def test_all_artwork_exists_and_has_expected_dimensions(self):
        paths = {row["image"] for row in self.rows}
        self.assertEqual(len(paths), 47)
        self.assertTrue(all(row["disponible"] for row in self.rows))
        for path in paths:
            with self.subTest(path=path), Image.open(PROJECT / path) as image:
                self.assertEqual(image.size, (768, 1376))

    def test_translations_and_late_cta_window_are_explicit(self):
        translations = {row["texte"]: row["traduction_fr"] for row in self.rows if row["traduction_fr"]}
        self.assertEqual(translations["Yeah... I'm still standing..."], "Ouais... je suis toujours debout...")
        self.assertEqual(translations["Arigato, gracias, merci, monwê"], "Merci, merci, merci — c'est confirmé.")
        signature, next_line = self.rows[56:58]
        self.assertGreater(self.renderer.CTA_START, signature["t"] + signature["rendu_affichage_s"] + .15)
        self.assertLess(self.renderer.CTA_END, next_line["t"])
        for text in translations.values():
            layer = self.renderer.translation_layer(text, 10)
            self.assertEqual(layer.size, (740, 80))
        self.assertLessEqual(1470 + 80, 1574)

    def test_id3_and_master_provenance(self):
        audio = MP3(PROJECT / "livrables/Je_me_releve_toujours_Dsky.mp3")
        tags = audio.tags
        self.assertEqual(tags["TIT2"].text, ["Je me relève toujours"])
        self.assertEqual(tags["TPE1"].text, ["Dsky"])
        self.assertEqual(tags["TPE2"].text, ["Dsky"])
        self.assertIn("Suno", tags["TXXX:IA_AUDIO"].text[0])
        self.assertIn("made with suno", tags["TXXX:SUNO_SOURCE_COMMENT"].text[0])
        self.assertTrue(any("made with suno" in str(c.text).lower() for c in tags.getall("COMM")))
        self.assertEqual(tags.getall("USLT")[0].text, "\n".join(row["texte"] for row in self.rows))
        source_hash = hashlib.sha256((REPO / "je me relève toujours 3.mp3").read_bytes()).hexdigest()
        self.assertEqual(tags["TXXX:MASTER_SHA256"].text, [source_hash])
        self.assertFalse(tags.getall("GEOB"), "A stale master C2PA manifest must not be copied onto a derivative")
        self.assertEqual(Image.open(io.BytesIO(tags.getall("APIC")[0].data)).size, (1080, 1080))

    def test_mp4_faststart_and_frame_budget(self):
        video = (PROJECT / "livrables/Je_me_releve_toujours_9x16.mp4").read_bytes()
        self.assertLess(video.index(b"moov"), video.index(b"mdat"))
        self.assertEqual(self.renderer.N_FRAMES, 7048)
        self.assertEqual((self.renderer.WIDTH, self.renderer.HEIGHT, self.renderer.FPS), (1080, 1920, 30))


if __name__ == "__main__":
    unittest.main()
