// Rend chaque ligne de paroles en PNG transparent (une fois par ligne, via Chromium)
// → typographie brush/graffiti, mots-clés en or, icônes, stamps.
// Sortie : out/text/line_XX.png + out/text/timing.json
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import puppeteer from 'puppeteer-core';
import { SCENES } from '../src/data.ts';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'out', 'text');
fs.mkdirSync(OUT, { recursive: true });

const W = 1920; // largeur de référence pour les tailles de police

/* ---------------- Polices ---------------- */

const FONT_FILES = [
  ['PermanentMarker', 'node_modules/@fontsource/permanent-marker/files/permanent-marker-latin-400-normal.woff2'],
  ['Anton', 'node_modules/@fontsource/anton/files/anton-latin-400-normal.woff2'],
  ['ArchivoBlack', 'node_modules/@fontsource/archivo-black/files/archivo-black-latin-400-normal.woff2'],
  ['Archivo700', 'node_modules/@fontsource/archivo/files/archivo-latin-700-normal.woff2'],
  ['Archivo800', 'node_modules/@fontsource/archivo/files/archivo-latin-800-normal.woff2'],
  ['Archivo900', 'node_modules/@fontsource/archivo/files/archivo-latin-900-normal.woff2'],
  ['Inter600', 'node_modules/@fontsource/inter/files/inter-latin-600-normal.woff2'],
  ['Inter800', 'node_modules/@fontsource/inter/files/inter-latin-800-normal.woff2'],
];

function b64(file) {
  return fs.readFileSync(path.join(ROOT, file)).toString('base64');
}

const FONTS = {
  brush: "'PermanentMarker', sans-serif",
  display: "'Anton', sans-serif",
  heavy: "'ArchivoBlack', sans-serif",
  body700: "'Archivo700', sans-serif",
  body800: "'Archivo800', sans-serif",
  body900: "'Archivo900', sans-serif",
  ui600: "'Inter600', sans-serif",
  ui800: "'Inter800', sans-serif",
};

const COLORS = {
  green: '#008751',
  yellow: '#FCD116',
  red: '#E8112D',
  gold: '#FFC93C',
  orange: '#FF7A1A',
  white: '#FFFFFF',
};

/* ---------------- Icônes SVG ---------------- */

const ICONS = {
  bell: `<svg width="50" height="50" viewBox="0 0 24 24" fill="none"><path d="M12 2a6 6 0 0 0-6 6v3.2L4.4 14a1 1 0 0 0 .8 1.6h13.6a1 1 0 0 0 .8-1.6L18 11.2V8a6 6 0 0 0-6-6Z" fill="#fff"/><path d="M10 19a2 2 0 0 0 4 0" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>`,
  heart: `<svg width="50" height="50" viewBox="0 0 24 24" fill="#fff"><path d="M12 21s-7.5-4.9-9.5-9.2C1.2 8.6 2.6 5 6 5c2 0 3.2 1.2 4 2.4C10.8 6.2 12 5 14 5c3.4 0 4.8 3.6 3.5 6.8C19.5 16.1 12 21 12 21Z"/></svg>`,
  comment: `<svg width="50" height="50" viewBox="0 0 24 24" fill="#fff"><path d="M4 4h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H8l-4 4V5a1 1 0 0 1 1-1Z"/></svg>`,
  share: `<svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7"/><path d="M16 6l-4-4-4 4"/><path d="M12 2v14"/></svg>`,
  key: `<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#FFC93C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3 20 3M16 7l2 2M13 10l2 2"/></svg>`,
  flag: `<svg width="60" height="40" viewBox="0 0 60 40"><rect x="0" y="0" width="20" height="40" fill="#008751"/><rect x="20" y="0" width="40" height="20" fill="#FCD116"/><rect x="20" y="20" width="40" height="20" fill="#E8112D"/></svg>`,
};

const ICON_BG = {
  bell: '#FF7A1A',
  heart: '#E8112D',
  comment: '#FCD116',
  share: '#008751',
};

const STAMP_COLORS = { red: COLORS.red, gold: COLORS.gold, green: COLORS.green };

/* ---------------- Normalisation / tokens ---------------- */

function normalize(w) {
  return w.toLowerCase().replace(/[^a-z0-9àâçéèêëîïôûùüÿœæ'-]/g, '');
}

function htmlEscape(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function lineHtml(line) {
  const kind = line.kind;
  const emph = new Set((line.emphasis ?? []).map(normalize));
  const renderWords = (color) =>
    line.main
      .split(' ')
      .map((w) => {
        const gold = emph.has(normalize(w));
        const style = gold
          ? `color:${COLORS.gold};text-shadow:0 0 22px rgba(255,201,60,0.5)`
          : `color:${color}`;
        return `<span style="${style}">${htmlEscape(w)}</span>`;
      })
      .join(' ');

  const subHtml = line.sub
    ? `<div style="font-family:${FONTS.ui600};font-size:46px;color:rgba(255,255,255,0.78);line-height:1.2;text-align:center;margin-top:14px">${htmlEscape(line.sub)}</div>`
    : '';

  let inner = '';

  if (kind === 'hook' || kind === 'final') {
    const size = kind === 'final' ? 123 : 108;
    inner = `<div style="font-family:${FONTS.display};font-size:${size}px;color:#fff;line-height:1.12;text-align:center;letter-spacing:0.01em;text-shadow:0 2px 14px rgba(0,0,0,0.6)">${renderWords('#ffffff')}</div>${subHtml}`;
  } else if (kind === 'verse') {
    inner = `<div style="font-family:${FONTS.body900};font-size:92px;color:#fff;line-height:1.12;text-align:center;text-shadow:0 2px 18px rgba(0,0,0,0.7)">${renderWords('#ffffff')}</div>`;
    if (line.fx === 'key') inner += `<div style="text-align:center;margin-top:10px">${ICONS.key}</div>`;
    if (line.fx === 'crack' || line.fx === 'fracture') inner = `<div style="text-shadow:0 0 40px rgba(255,233,168,0.9);${line.fx==='fracture'?'':''}">${inner}</div>`;
  } else if (kind === 'quote') {
    inner = `<div style="font-family:${FONTS.body700};font-style:italic;font-size:79px;color:#c3c9d4;line-height:1.15;text-align:center;padding:0 120px">${renderWords('#c3c9d4')}</div>`;
  } else if (kind === 'paren') {
    inner = `<div style="font-family:${FONTS.body700};font-size:63px;color:#fff;line-height:1.15;text-align:center;opacity:0.92;padding:0 120px">${renderWords('#ffffff')}</div>${subHtml}`;
  } else if (kind === 'bridge') {
    inner = `<div style="font-family:${FONTS.heavy};font-size:96px;color:#fff;line-height:1.15;text-align:center;text-shadow:0 0 34px rgba(255,190,90,0.5)">${renderWords('#ffffff')}</div>${subHtml}`;
  } else if (kind === 'echo') {
    inner = `<div style="font-family:${FONTS.body800};font-size:81px;color:#fff;line-height:1.15;text-align:center;text-shadow:0 2px 14px rgba(0,0,0,0.6)">${renderWords('#ffffff')}</div>${subHtml}`;
  } else if (kind === 'title') {
    inner = `<div style="font-family:${FONTS.brush};font-size:188px;color:#fff;line-height:1;text-align:center;text-shadow:3px 3px 0 #E8112D,-3px -3px 0 #E8112D,3px -3px 0 #E8112D,-3px 3px 0 #E8112D,0 0 30px rgba(255,120,20,0.85),0 0 70px rgba(255,60,10,0.5)">${htmlEscape(line.main)}</div>${subHtml}`;
  } else if (kind === 'cta') {
    const bg = ICON_BG[line.icon ?? 'bell'] ?? COLORS.gold;
    const icon = line.icon ? `<span style="display:inline-flex;align-items:center;justify-content:center;width:86px;height:86px;border-radius:12px;background:${bg};box-shadow:0 0 26px ${bg}88;flex-shrink:0">${ICONS[line.icon] ?? ''}</span>` : '';
    inner = `<div style="display:flex;align-items:center;gap:30px"><div>${icon}</div><div style="font-family:${FONTS.ui800};font-size:50px;color:#fff;letter-spacing:0.01em;text-shadow:0 2px 14px rgba(0,0,0,0.7)">${htmlEscape(line.main)}</div></div>`;
  } else if (kind === 'stamp') {
    const color = STAMP_COLORS[line.note ?? 'red'] ?? COLORS.red;
    inner = `<div style="border:4px solid ${color};outline:2px solid ${color};outline-offset:4px;border-radius:14px;padding:22px 58px;background:rgba(0,0,0,0.55);box-shadow:0 0 40px ${color}55,inset 0 0 30px ${color}33;transform:rotate(-3deg)"><div style="font-family:${FONTS.brush};font-size:88px;color:${color};letter-spacing:0.02em;text-shadow:0 0 24px ${color}99;white-space:nowrap">${htmlEscape(line.main)}</div></div>`;
  } else if (kind === 'logo') {
    inner = `<div style="display:flex;align-items:center;gap:28px">${ICONS.flag}<div style="font-family:${FONTS.brush};font-size:81px;color:#fff;text-shadow:0 0 26px rgba(255,201,60,0.6)">${htmlEscape(line.main)}</div></div>`;
  } else {
    inner = `<div style="font-family:${FONTS.body800};font-size:92px;color:#fff;text-align:center">${renderWords('#ffffff')}</div>${subHtml}`;
  }

  return inner;
}

/* ---------------- HTML complet ---------------- */

const lines = SCENES.flatMap((s) => s.lines);

const fontFace = FONT_FILES.map(
  ([name, file]) =>
    `@font-face{font-family:'${name}';src:url(data:font/woff2;base64,${b64(file)}) format('woff2');font-weight:normal;font-style:normal;}`
).join('\n');

const divs = lines
  .map((line, i) => {
    const y = line.y ?? (line.kind === 'stamp' ? 50 : 52);
    return `<div id="l${i}" data-y="${y}" style="position:absolute;left:0;top:0;max-width:1740px;padding:60px;display:inline-block">${lineHtml(line)}</div>`;
  })
  .join('\n');

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{background:transparent}
  body{width:20000px;height:20000px}
  ${fontFace}
</style></head><body>${divs}</body></html>`;

/* ---------------- Capture ---------------- */

const chromiumPath = process.env.CHROMIUM ?? '/tmp/chromium';

const browser = await puppeteer.launch({
  executablePath: chromiumPath,
  env: { ...process.env, LD_LIBRARY_PATH: process.env.LD_LIBRARY_PATH ?? '/tmp/chromium-libs/lib' },
  args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--no-zygote'],
  defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 1 },
});

const page = await browser.newPage();
await page.setContent(html, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);

const timing = [];
for (let i = 0; i < lines.length; i++) {
  const el = await page.$(`#l${i}`);
  const file = path.join(OUT, `line_${String(i).padStart(3, '0')}.png`);
  await el.screenshot({ omitBackground: true, path: file });
  const box = await el.boundingBox();
  timing.push({
    i,
    start: lines[i].start,
    end: lines[i].end,
    kind: lines[i].kind,
    y: lines[i].y ?? (lines[i].kind === 'stamp' ? 50 : 52),
    w: Math.round(box.width),
    h: Math.round(box.height),
    file: path.basename(file),
  });
}

await browser.close();

fs.writeFileSync(path.join(OUT, 'timing.json'), JSON.stringify(timing, null, 2));
console.log(`✔ ${lines.length} overlays texte générés dans ${OUT}`);
