"""Tests hors réseau : parsing des paroles et contrôles, pas de validation vocale."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("analyse", Path(__file__).parents[1] / "scripts/analyse_chanson.py")
analyse = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyse)


class LyricsTests(unittest.TestCase):
    def parse(self, text, encoding="utf-8"):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lyrics.txt"
            path.write_bytes(text.encode(encoding))
            return analyse.load_lyrics(path)

    def test_lrc_metadata_and_invisible_marks(self):
        parsed = self.parse("[length:03:33]\n[00:04.44]\u200eWolof TechStein beat wê...\n")
        self.assertEqual(parsed["metadata"], {"length": "03:33"})
        self.assertEqual(parsed["removed_direction_marks"], 1)
        self.assertEqual(parsed["entries"][0]["text"], "Wolof TechStein beat wê...")
        self.assertEqual(parsed["entries"][0]["start"], 4.44)

    def test_trailing_hyphen_timestamp(self):
        entries = self.parse("Je suis libre-1:30.6\nLa vie ! -2:47")['entries']
        self.assertEqual([e["start"] for e in entries], [90.6, 167.0])
        self.assertEqual([e["text"] for e in entries], ["Je suis libre", "La vie !"])

    def test_time_range_preserves_punctuation(self):
        e = self.parse("(Dernier vers...) 4:01-4:05")['entries'][0]
        self.assertEqual(e["text"], "(Dernier vers...)")
        self.assertEqual((e["start"], e["explicit_end"]), (241.0, 245.0))

    def test_section_is_metadata(self):
        e = self.parse("[REFRAIN - Explosif]\nSans heure !")['entries'][0]
        self.assertEqual(e["section"], "REFRAIN - Explosif")
        self.assertIsNone(e["start"])
        self.assertEqual(e["format"], "untimed")

    def test_case_punctuation_and_internal_space_are_not_normalized(self):
        entries = self.parse("[00:01]wê...\n[00:03]wê!\n[00:05]Wê!\n[00:07]moi  aussi")['entries']
        self.assertEqual(len({e["text"] for e in entries}), 4)
        self.assertEqual(entries[-1]["text"], "moi  aussi")

    def test_cp1252_has_no_replacement_characters(self):
        e = self.parse("[00:01.23]L'œuvre, je rêve !", "cp1252")
        self.assertEqual(e["encoding"], "cp1252")
        self.assertEqual(e["entries"][0]["text"], "L'œuvre, je rêve !")

    def test_multi_tag_lrc_is_expanded(self):
        e = self.parse("[00:01][00:11]Reprise\n[00:05]Suite")['entries']
        self.assertEqual([v['start'] for v in e], [1, 5, 11])

    def test_source_timing_errors_are_reported_not_rewritten(self):
        e = self.parse("[00:04]A\n[00:03]B\n[00:03.5]C\n[00:11]D")['entries']
        self.assertEqual([i['issue'] for i in analyse.audit_timings(e, 10)],
                         ['non_monotone', 'ecart_inferieur_1.2s', 'hors_audio'])
        self.assertEqual([v['start'] for v in e], [4, 3, 3.5, 11])

    def test_minimum_spacing_inclusive(self):
        e = self.parse("[00:01.1]A\n[00:02.3]B")['entries']
        self.assertEqual(analyse.audit_timings(e, 10), [])

    def test_invalid_explicit_end(self):
        e = self.parse("Texte 0:04-0:03")['entries']
        self.assertEqual(analyse.audit_timings(e, 10)[0]['issue'], 'fin_invalide')

    def test_lrc_timestamp_rounding_carries(self):
        self.assertEqual(analyse.timestamp(59.999), '01:00.00')

    def test_lrc_export_roundtrip(self):
        parsed = self.parse("[REFRAIN]\n[00:01.25]La lumière...\n[00:03.40]L'œuvre !")
        data = {"title": "Titre", "duration_decoded_seconds": 7.16,
                "lyrics": {**parsed, "issues": []}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.lrc"
            analyse.write_source_lrc(data, path)
            result = analyse.load_lyrics(path)
            self.assertEqual(result['metadata']['length'], '00:07.16')
            self.assertEqual([(e['text'], e['start'], e['section']) for e in result['entries']],
                             [(e['text'], e['start'], e['section']) for e in parsed['entries']])

    def test_lrc_export_rejects_unaligned_lyrics(self):
        parsed = self.parse("Pas encore aligné")
        data = {"title": "Titre", "duration_decoded_seconds": 7,
                "lyrics": {**parsed, "issues": []}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.lrc"
            with self.assertRaises(ValueError):
                analyse.write_source_lrc(data, path)
            self.assertFalse(path.exists())

    def test_real_song(self):
        path = Path(__file__).parents[1] / 'concentré sur le chemin.txt'
        parsed = analyse.load_lyrics(path)
        self.assertEqual(parsed['entries'][0]['start'], 4.44)
        self.assertEqual(parsed['entries'][-1]['start'], 190.90)
        self.assertEqual(analyse.audit_timings(parsed['entries'], 213.16), [])
        self.assertTrue(any(e['text'] == "J'suis concentrée, j'regarde droit devant" for e in parsed['entries']))


if __name__ == '__main__':
    unittest.main()
