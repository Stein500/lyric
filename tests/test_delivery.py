"""Commandes Termux sûres et preuves cohérentes du pack complet, sans réseau."""
from pathlib import Path
import hashlib
import json
import re
import shlex
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from write_termux_delivery import checked_ref, raw_url, download_command, verify_metadata, download_proof, ROOT, STATE

REF = '1234567890abcdef1234567890abcdef12345678'


class TermuxCommandTests(unittest.TestCase):
    def test_only_full_immutable_git_hash_is_accepted(self):
        self.assertEqual(checked_ref(REF), REF)
        for value in ['main', 'HEAD', '1234567', REF + '/main', 'z' * 40, REF.upper()]:
            with self.subTest(ref=value), self.assertRaises(ValueError):
                checked_ref(value)

    def test_url_encodes_spaces_and_accents_without_encoding_directories(self):
        url = raw_url('Concentré sur le chemin.lrc', REF)
        self.assertEqual(url, f'https://raw.githubusercontent.com/Stein500/lyric/{REF}/Concentr%C3%A9%20sur%20le%20chemin.lrc')
        self.assertTrue(raw_url('livrables/clip.mp4', REF).endswith('/livrables/clip.mp4'))

    def test_command_is_one_line_resumable_and_uses_requested_destination(self):
        line = download_command('livrables/clip.mp4', 'clip.mp4', REF)
        self.assertNotIn('\n', line)
        self.assertNotIn('&&', line)
        self.assertNotIn('\\', line)
        self.assertEqual(line.count(';'), 2)
        self.assertIn('curl -fL --retry 5 --retry-delay 3 -C -', line)
        self.assertIn('-o /storage/emulated/0/Web+/clip.mp4', line)
        self.assertIn(f'/{REF}/livrables/clip.mp4', line)

    def test_relative_paths_and_download_basenames_only(self):
        for value in ['/etc/passwd', '../clip.mp4', 'livrables/../clip.mp4', '']:
            with self.subTest(path=value), self.assertRaises(ValueError):
                raw_url(value, REF)
        for name in ['../clip.mp4', 'nested/clip.mp4', '.', '..', '']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                download_command('livrables/clip.mp4', name, REF)

    def test_shell_quoting_preserves_a_filename_with_spaces(self):
        name = 'Concentré sur le chemin.lrc'
        line = download_command(name, name, REF)
        command = shlex.split(line.split(';')[1])
        self.assertEqual(command[command.index('-o') + 1], '/storage/emulated/0/Web+/' + name)
        self.assertNotIn(' ', command[-1])

    def test_remote_proof_requires_file_type_sha_and_exact_size(self):
        valid = {'type': 'file', 'sha': 'a' * 40, 'size': 123456}
        verify_metadata(valid, 'a' * 40, 123456)
        for field, bad in [('type', 'dir'), ('sha', 'b' * 40), ('size', 123455)]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_metadata({**valid, field: bad}, 'a' * 40, 123456)


    def test_tls_failure_uses_api_raw_without_pretending_direct_raw_succeeded(self):
        sha = 'a' * 64
        endpoint = 'repos/Stein500/lyric/contents/clip.mp4?ref=' + REF
        with patch('write_termux_delivery.stream_digest', side_effect=[
                (35, 0, 'b' * 64, 'SSL_ERROR_SYSCALL'), (0, 12345, sha, '')]) as fetch:
            proof = download_proof(raw_url('clip.mp4', REF), endpoint, 12345, sha)
        self.assertFalse(proof['raw_download_verified'])
        self.assertTrue(proof['api_raw_download_verified'])
        self.assertEqual(proof['download_verification_method'], 'github_api_raw')
        self.assertIn('SSL_ERROR_SYSCALL', proof['raw_url_check_error'])
        self.assertEqual(fetch.call_args_list[1].args[0], [
            'gh', 'api', '-H', 'Accept: application/vnd.github.raw+json', endpoint])
        self.assertNotIn('-k', fetch.call_args_list[0].args[0])
        with patch('write_termux_delivery.stream_digest', return_value=(0, 12345, 'c' * 64, '')):
            with self.assertRaises(RuntimeError):
                download_proof(raw_url('clip.mp4', REF), endpoint, 12345, sha)


class FinalExportTests(unittest.TestCase):
    def load(self, name):
        path = STATE / name
        if not path.is_file():
            self.skipTest(f'À exécuter après production de {name}')
        return json.loads(path.read_text())

    def test_both_clips_match_checked_hash_frames_and_streams(self):
        for fmt, resolution in [('portrait', '1080x1920'), ('landscape', '1920x1080')]:
            report = self.load(f'qa_{fmt}.json')
            path = ROOT / report['file']
            with self.subTest(format=fmt):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), report['sha256'])
                self.assertEqual(path.stat().st_size, report['size_bytes'])
                self.assertEqual(report['status'], 'technical_checks_passed')
                self.assertEqual(report['frames'], 6752)
                self.assertEqual(report['fps'], 30)
                self.assertAlmostEqual(report['duration'], 6752 / 30, places=5)
                video, audio = report['streams']
                self.assertIn(resolution, video)
                self.assertIn('h264', video)
                self.assertIn('bt709', video)
                self.assertIn('yuv420p', video)
                self.assertIn('aac', audio)
                self.assertIn('48000 Hz, stereo', audio)
                self.assertEqual(report['freeze_intervals'], [])
                self.assertTrue(all(t >= report['black_allowed_only_after'] - .05 for t in report['black_starts']))

    def test_three_measured_audio_checks_in_both_clips_are_not_vocal_approval(self):
        for fmt in ['portrait', 'landscape']:
            report = self.load(f'qa_{fmt}.json')
            checks = report['audio_sync_checks']
            self.assertEqual([r['source_start'] for r in checks], [25.3, 85.64, 152.84])
            for row in checks:
                self.assertLessEqual(abs(row['measured_lag_seconds']), .02)
                self.assertAlmostEqual(row['video_start'] - row['source_start'], 6.9)
            self.assertIn('not forced', report['word_alignment'])
        state = self.load('production.json')
        self.assertFalse(state['approvals']['vocal_sync'])
        self.assertTrue(state['approvals']['image_series'])

    def test_manifest_has_existing_files_matching_hashes_and_no_duplicate_names(self):
        report = self.load('delivery_manifest.json')
        self.assertFalse(report['vocal_word_alignment_human_validated'])
        self.assertTrue(report['images_artist_approved'])
        self.assertEqual(report['new_ai_images_this_step'], 0)
        names = [row['download_name'] for row in report['files']]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(names), 13)
        for row in report['files']:
            path = ROOT / row['file']
            with self.subTest(file=row['file']):
                self.assertTrue(path.is_file())
                self.assertEqual(path.stat().st_size, row['size_bytes'])
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row['sha256'])

    def test_sha256_list_uses_android_names_and_matches_manifest(self):
        report = self.load('delivery_manifest.json')
        fingerprint = ROOT / 'livrables/Concentre_sur_le_chemin_SHA256.txt'
        expected = {row['download_name']: row['sha256'] for row in report['files'] if row['file'] != str(fingerprint.relative_to(ROOT))}
        actual = {}
        for line in fingerprint.read_text().splitlines():
            digest, name = line.split('  ', 1)
            self.assertRegex(digest, r'^[0-9a-f]{64}$')
            actual[name] = digest
        self.assertEqual(actual, expected)

    def test_remote_proofs_and_termux_doc_use_one_verified_media_commit(self):
        report = self.load('delivery_remote_checks.json')
        manifest = self.load('delivery_manifest.json')
        self.assertEqual(len(report['files']), len(manifest['files']))
        ref = checked_ref(report['media_commit'])
        doc = (ROOT / 'livrables/TERMUX_Concentre_sur_le_chemin_COMPLET.md').read_text()
        commands = [line for line in doc.splitlines() if line.startswith('mkdir -p ')]
        self.assertEqual(len(commands), len(report['files']))
        for row, command, source in zip(report['files'], commands, manifest['files']):
            with self.subTest(file=row['file']):
                self.assertTrue(row['github_contents_verified'])
                self.assertTrue(row['raw_download_verified'] or row['api_raw_download_verified'])
                self.assertNotEqual(row['raw_download_verified'], row['api_raw_download_verified'])
                self.assertEqual(row['sha256'], source['sha256'])
                self.assertEqual(row['size_bytes'], source['size_bytes'])
                self.assertEqual(row['url'], raw_url(row['file'], ref))
                self.assertEqual(command, download_command(row['file'], row['download_name'], ref))
                self.assertNotIn('&&', command)
                self.assertNotIn('\\', command)
                self.assertEqual(command.count(';'), 2)


if __name__ == '__main__':
    unittest.main()
