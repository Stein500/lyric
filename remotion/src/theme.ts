import '@fontsource/anton/400.css';
import '@fontsource/permanent-marker/400.css';
import '@fontsource/archivo-black/400.css';
import '@fontsource/archivo/800.css';
import '@fontsource/archivo/900.css';
import '@fontsource/inter/400.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/800.css';

export const FPS = 30;
export const TOTAL_SECONDS = 215.2;

export const FONTS = {
  brush: "'Permanent Marker', 'DejaVu Sans', sans-serif",
  display: "'Anton', 'DejaVu Sans', sans-serif",
  heavy: "'Archivo Black', 'Archivo', 'DejaVu Sans', sans-serif",
  body: "'Archivo', 'DejaVu Sans', sans-serif",
  ui: "'Inter', 'DejaVu Sans', sans-serif",
};

// Palette — couleurs du Bénin + embrasement
export const COLORS = {
  green: '#008751',
  yellow: '#FCD116',
  red: '#E8112D',
  gold: '#FFC93C',
  orange: '#FF7A1A',
  ember: '#FF8C42',
  white: '#FFFFFF',
  ink: '#050505',
};

/* ------------------------------------------------------------------ */
/*  Arc de couleur global (désaturé froid -> chaud -> explosion -> or) */
/* ------------------------------------------------------------------ */

interface GradeKey {
  t: number;
  sat: number;
  bright: number;
  tint: [number, number, number, number]; // rgba
}

const GRADE_KEYS: GradeKey[] = [
  { t: 0.0, sat: 0.35, bright: 0.9, tint: [80, 90, 110, 0.16] }, // intro sombre
  { t: 13.0, sat: 0.8, bright: 1.0, tint: [255, 120, 40, 0.13] }, // ad-lib chaud
  { t: 34.0, sat: 1.25, bright: 1.05, tint: [255, 90, 30, 0.17] }, // tag
  { t: 50.0, sat: 0.48, bright: 0.82, tint: [70, 85, 110, 0.2] }, // couplet 1 froid
  { t: 73.0, sat: 0.85, bright: 1.0, tint: [255, 130, 45, 0.17] }, // pré-refrain 1
  { t: 89.9, sat: 1.3, bright: 1.1, tint: [255, 70, 20, 0.25] }, // refrain 1
  { t: 108.8, sat: 1.0, bright: 1.0, tint: [255, 110, 35, 0.2] }, // couplet 2 chaud
  { t: 124.8, sat: 1.15, bright: 1.05, tint: [255, 120, 35, 0.23] }, // pré-refrain 2
  { t: 140.0, sat: 0.95, bright: 1.12, tint: [255, 190, 80, 0.3] }, // pont doré
  { t: 160.0, sat: 1.45, bright: 1.15, tint: [255, 90, 20, 0.28] }, // refrain final
  { t: 177.0, sat: 1.5, bright: 1.12, tint: [255, 110, 40, 0.22] }, // tag final
  { t: 195.0, sat: 0.9, bright: 1.0, tint: [255, 170, 70, 0.26] }, // outro
  { t: 215.2, sat: 0.7, bright: 0.7, tint: [110, 110, 120, 0.16] }, // extinction
];

function lerp(a: number, b: number, p: number) {
  return a + (b - a) * p;
}

export interface Grade {
  sat: number;
  bright: number;
  tint: string;
  tintA: number;
}

export function gradeAt(t: number): Grade {
  const keys = GRADE_KEYS;
  if (t <= keys[0].t) {
    return pack(keys[0]);
  }
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i];
    const b = keys[i + 1];
    if (t >= a.t && t <= b.t) {
      const p = (t - a.t) / (b.t - a.t);
      const sat = lerp(a.sat, b.sat, p);
      const bright = lerp(a.bright, b.bright, p);
      const tint = a.tint.map((c, k) => lerp(c, b.tint[k], p)) as [
        number,
        number,
        number,
        number,
      ];
      return pack({ t, sat, bright, tint });
    }
  }
  return pack(keys[keys.length - 1]);
}

function pack(k: GradeKey): Grade {
  return {
    sat: k.sat,
    bright: k.bright,
    tint: `rgb(${k.tint[0]},${k.tint[1]},${k.tint[2]})`,
    tintA: k.tint[3],
  };
}

/* ------------------------------------------------------------------ */
/*  Intensité de la flamme (0 -> ~1.3)                                  */
/* ------------------------------------------------------------------ */

const FLAME_KEYS: [number, number][] = [
  [0.0, 0.02],
  [4.0, 0.18],
  [12.0, 0.3],
  [13.0, 0.78],
  [18.0, 0.66],
  [24.0, 0.72],
  [30.0, 0.86],
  [34.0, 0.9],
  [40.0, 0.82],
  [50.0, 0.1],
  [54.0, 0.55],
  [55.5, 0.68],
  [58.2, 0.52],
  [60.0, 0.74],
  [64.5, 0.82],
  [68.0, 0.9],
  [73.0, 0.96],
  [80.0, 1.0],
  [89.9, 1.05],
  [100.0, 1.0],
  [108.8, 0.85],
  [114.9, 0.9],
  [119.0, 1.0],
  [124.8, 1.06],
  [132.0, 1.1],
  [140.0, 0.72],
  [152.0, 0.66],
  [160.0, 1.16],
  [170.0, 1.2],
  [177.0, 1.26],
  [195.0, 0.9],
  [205.0, 0.55],
  [215.2, 0.2],
];

export function flameAt(t: number): number {
  for (let i = 0; i < FLAME_KEYS.length - 1; i++) {
    const [t1, v1] = FLAME_KEYS[i];
    const [t2, v2] = FLAME_KEYS[i + 1];
    if (t >= t1 && t <= t2) {
      return lerp(v1, v2, (t - t1) / (t2 - t1));
    }
  }
  return FLAME_KEYS[FLAME_KEYS.length - 1][1];
}

/* ------------------------------------------------------------------ */
/*  Présence du phénix (opacité, échelle, position, image)              */
/* ------------------------------------------------------------------ */

export interface PhoenixState {
  opacity: number;
  scale: number;
  y: number; // px offset (positif = vers le bas)
  x: number; // px offset
  gold: boolean;
}

const PHOENIX_KEYS: [number, number, number, number, number, boolean][] = [
  // t, opacity, scale, y, x, gold
  [0.0, 0, 1, 0, 0, false],
  [13.0, 0, 1, 0, 0, false],
  [34.0, 0.15, 1.05, 0, 0, false],
  [50.0, 0.12, 1.02, 0, 0, false],
  [73.0, 0.35, 1.05, 120, 0, false], // plumes filigrane entrant par les bords
  [89.9, 1.0, 1.0, 0, 0, false],
  [108.8, 0.6, 0.96, 0, 0, false],
  [124.8, 0.82, 1.02, 60, 0, false],
  [140.0, 0.85, 1.0, 0, 0, true], // pont : phénix doré, vol calme
  [160.0, 1.2, 1.12, 0, 0, false],
  [177.0, 1.15, 1.08, 0, 0, false],
  [195.0, 1.0, 1.0, 0, 0, false],
  [215.2, 0.8, 0.9, -420, 0, false], // s'envole hors-cadre
];

export function phoenixAt(t: number): PhoenixState {
  const keys = PHOENIX_KEYS;
  if (t <= keys[0][0]) {
    return pk(keys[0]);
  }
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i];
    const b = keys[i + 1];
    if (t >= a[0] && t <= b[0]) {
      const p = (t - a[0]) / (b[0] - a[0]);
      return {
        opacity: lerp(a[1], b[1], p),
        scale: lerp(a[2], b[2], p),
        y: lerp(a[3], b[3], p),
        x: lerp(a[4], b[4], p),
        gold: b[5],
      };
    }
  }
  return pk(keys[keys.length - 1]);
}

function pk(k: [number, number, number, number, number, boolean]): PhoenixState {
  return { opacity: k[1], scale: k[2], y: k[3], x: k[4], gold: k[5] };
}

/* ------------------------------------------------------------------ */
/*  PRNG déterministe (pour un rendu stable entre deux exports)         */
/* ------------------------------------------------------------------ */

export function mulberry32(seed: number) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ------------------------------------------------------------------ */
/*  Easing                                                             */
/* ------------------------------------------------------------------ */

export function clamp01(v: number) {
  return Math.max(0, Math.min(1, v));
}

export function easeOutCubic(p: number) {
  return 1 - Math.pow(1 - p, 3);
}

export function easeOutBack(p: number) {
  const c1 = 1.70158;
  const c3 = c1 + 1;
  return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2);
}

export function easeInOut(p: number) {
  return p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
}
