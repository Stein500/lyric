// Assemble la lyric video rapidement avec un ffmpeg complet (zoompan/overlay/concat)
// - Arrière-plans IA en Ken Burns, fondus entre sections
// - Overlays texte PNG (pré-rendus) synchronisés sur les paroles
// - Audio d'origine + étalonnage léger (vignette + grain)
// Usage : node --experimental-strip-types scripts/build-video.mjs [MAX_T]
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawnSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'out');
const FFMPEG = path.join(ROOT, 'node_modules', '@ffmpeg-installer', 'linux-x64', 'ffmpeg');

const W = 1920;
const H = 1080;
const FPS = 30;
const TOTAL = 215.2;
const MAX_T = process.argv[2] ? parseFloat(process.argv[2]) : null;

/* ---------------- Segments d'arrière-plan (mood → image) ---------------- */

const SEGMENTS = [
  { start: 0, end: 34, bg: 'bg-intro', rate: 0.10 },
  { start: 34, end: 50, bg: 'bg-verse2', rate: 0.13 },
  { start: 50, end: 73, bg: 'bg-verse1', rate: 0.09 },
  { start: 73, end: 89.9, bg: 'bg-prerefrain', rate: 0.13 },
  { start: 89.9, end: 108.8, bg: 'bg-chorus', rate: 0.15 },
  { start: 108.8, end: 124.8, bg: 'bg-verse2', rate: 0.13 },
  { start: 124.8, end: 140, bg: 'bg-prerefrain', rate: 0.14 },
  { start: 140, end: 160, bg: 'bg-bridge', rate: 0.06 },
  { start: 160, end: 195, bg: 'bg-final', rate: 0.16 },
  { start: 195, end: 215.2, bg: 'bg-bridge', rate: 0.06 },
];

/* ---------------- Overlays texte ---------------- */

const timing = JSON.parse(fs.readFileSync(path.join(OUT, 'text', 'timing.json'), 'utf8'));

/* ---------------- Construction des entrées ---------------- */

const args = ['-y', '-hide_banner', '-loglevel', 'warning', '-stats'];

// 1) arrière-plans (images fixes)
let segs = SEGMENTS;
if (MAX_T) {
  segs = SEGMENTS.filter((s) => s.start < MAX_T).map((s, idx, arr) => {
    if (idx === arr.length - 1) return { ...s, end: Math.min(s.end, MAX_T) };
    return s;
  });
}
const inputIndex = {};
let idx = 0;
for (const s of segs) {
  args.push('-i', path.join(ROOT, 'public', 'bg', `${s.bg}.png`));
  inputIndex[`bg_${s.start}`] = idx++;
}

// 2) audio
args.push('-i', path.join(ROOT, 'public', 'not afraid.mp3'));
inputIndex.audio = idx++;

// 3) overlays texte
let texts = timing;
if (MAX_T) {
  texts = timing.filter((t) => t.start < MAX_T);
}
for (const t of texts) {
  const dur = t.end - t.start;
  args.push(
    '-loop', '1',
    '-framerate', String(FPS),
    '-t', String(dur),
    '-i', path.join(OUT, 'text', t.file)
  );
  inputIndex[`t_${t.i}`] = idx++;
}

/* ---------------- Filtergraph ---------------- */

const filter = [];
const FAD = 0.4; // fondu entre sections

segs.forEach((s, i) => {
  const D = s.end - s.start;
  const DURF = Math.round(D * FPS);
  const z = `min(1.0+${s.rate}*on/${DURF},1.18)`;
  filter.push(
    `[${i}:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},` +
      `zoompan=z='${z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${DURF}:s=${W}x${H}:fps=${FPS},` +
      `fade=t=in:st=0:d=${FAD},fade=t=out:st=${Math.max(0, D - FAD)}:d=${FAD},` +
      `setsar=1,settb=AVTB,format=yuv420p[bg${i}]`
  );
});

filter.push(
  segs.map((_, i) => `[bg${i}]`).join('') + `concat=n=${segs.length}:v=1:a=0[bgcat]`
);

// étalonnage global
filter.push(`[bgcat]eq=saturation=1.06:contrast=1.03,vignette=angle=PI/4,noise=alls=4:allf=t,format=yuv420p[bgdone]`);

// overlays texte
let prev = 'bgdone';
for (const t of texts) {
  const dur = t.end - t.start;
  const x = Math.round((W - t.w) / 2);
  const y = Math.round((t.y / 100) * H - t.h / 2);
  const src = inputIndex[`t_${t.i}`];
  const label = `t${t.i}`;
  const fout = Math.max(0.15, dur - 0.25);
  filter.push(
    `[${src}:v]format=rgba,fade=t=in:st=0:d=0.15:alpha=1,fade=t=out:st=${fout}:d=0.25:alpha=1,setpts=PTS+${t.start}/TB[${label}]`
  );
  filter.push(
    `[${prev}][${label}]overlay=x=${x}:y=${y}:eof_action=pass:repeatlast=0[${label}_o]`
  );
  prev = `${label}_o`;
}

filter.push(`[${prev}]format=yuv420p[vout]`);

/* ---------------- Encodage ---------------- */

args.push(
  '-filter_complex', filter.join(';'),
  '-map', '[vout]',
  '-map', `${inputIndex.audio}:a`,
  '-c:v', 'libx264',
  '-preset', 'veryfast',
  '-crf', '19',
  '-pix_fmt', 'yuv420p',
  '-r', String(FPS),
  '-c:a', 'aac',
  '-b:a', '192k',
  '-movflags', '+faststart',
  '-shortest'
);

if (MAX_T) {
  args.push('-t', String(MAX_T));
}

const outFile = path.join(OUT, MAX_T ? 'test-fast.mp4' : 'im-not-afraid.mp4');
args.push(outFile);

console.log(`→ ${segs.length} sections bg, ${texts.length} overlays texte`);
console.log('→ commande ffmpeg…');
const res = spawnSync(FFMPEG, args, { stdio: 'inherit' });
if (res.status !== 0) {
  console.error('✗ ffmpeg a échoué (code ' + res.status + ')');
  process.exit(1);
}
console.log('✔ ' + outFile);
