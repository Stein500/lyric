#!/usr/bin/env bash
# Prépare un binaire Chromium exploitable par Remotion quand seuls les
# miroirs npm sont accessibles (pas de deb.debian.org, pas de Google, pas
# de remotion.media). À relancer après une réinstallation (node_modules
# et /tmp ne sont pas persistés entre les sessions).
set -euo pipefail

cd "$(dirname "$0")/.."

echo "→ Installation du paquet Chromium (npm)…"
npm install --no-audit --no-fund @sparticuz/chromium

echo "→ Extraction du binaire Chromium…"
node --input-type=module -e "
import Chromium from '@sparticuz/chromium';
const p = await Chromium.executablePath();
console.log('chromium =', p);
"

echo "→ Extraction des bibliothèques NSS (Amazon Linux 2023)…"
node --input-type=module -e "
import fs from 'fs';
import zlib from 'zlib';
const src = 'node_modules/@sparticuz/chromium/bin/al2023.tar.br';
const tar = zlib.brotliDecompressSync(fs.readFileSync(src));
fs.mkdirSync('/tmp/chromium-libs', { recursive: true });
fs.writeFileSync('/tmp/al2023.tar', tar);
"
mkdir -p /tmp/chromium-libs
tar -xf /tmp/al2023.tar -C /tmp/chromium-libs

echo "→ Vérification…"
LD_LIBRARY_PATH=/tmp/chromium-libs/lib /tmp/chromium --version

echo "✔ Prêt. Lance le rendu avec :"
echo "  LD_LIBRARY_PATH=/tmp/chromium-libs/lib npx remotion render src/index.tsx ImNotAfraidLyrics out/im-not-afraid.mp4 --browser-executable=/tmp/chromium"
