import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import {
  FPS,
  flameAt,
  gradeAt,
  phoenixAt,
  mulberry32,
  COLORS,
} from '../theme';

/* ---------------- Braises / étincelles ---------------- */

const EMBER_COUNT = 70;

interface Ember {
  x: number;
  phase: number;
  speed: number;
  size: number;
  drift: number;
  wobble: number;
  flick: number;
  hue: number; // 0 orange -> 1 gold
}

const Embers: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const t = frame / FPS;
  const rnd = mulberry32(1234);
  const embers: Ember[] = Array.from({ length: EMBER_COUNT }, () => ({
    x: rnd(),
    phase: rnd(),
    speed: 0.06 + rnd() * 0.13,
    size: 1.5 + rnd() * 3.5,
    drift: 0.004 + rnd() * 0.02,
    wobble: 0.3 + rnd() * 1.2,
    flick: 6 + rnd() * 10,
    hue: rnd(),
  }));

  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      {embers.map((e, i) => {
        const travel = (e.phase + t * e.speed) % 1.25;
        const y = height * (1.05 - travel * 1.15);
        const x = width * (e.x + Math.sin(t * e.wobble + e.phase * 20) * e.drift);
        const flick = 0.45 + 0.55 * Math.abs(Math.sin(t * e.flick + e.phase * 40));
        const r = Math.round(255);
        const g = Math.round(140 + e.hue * 70);
        const b = Math.round(30 + e.hue * 60);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: e.size,
              height: e.size,
              borderRadius: '50%',
              background: `radial-gradient(circle, rgba(${r},${g},${b},${flick}) 0%, rgba(${r},${g},${b},0) 70%)`,
              boxShadow: `0 0 ${e.size * 3}px rgba(255,150,60,${0.6 * flick})`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

/* ---------------- Fumée ---------------- */

const Smoke: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const t = frame / FPS;
  const rnd = mulberry32(99);
  const blobs = Array.from({ length: 5 }, () => ({
    x: 0.15 + rnd() * 0.7,
    size: 0.5 + rnd() * 0.8,
    speed: 0.008 + rnd() * 0.02,
    phase: rnd(),
    op: 0.05 + rnd() * 0.08,
  }));

  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      {blobs.map((b, i) => {
        const travel = (b.phase + t * b.speed) % 1.3;
        const y = height * (1.1 - travel * 1.25);
        const x = width * (b.x + Math.sin(t * 0.2 + b.phase * 10) * 0.05);
        const s = b.size * Math.min(width, height);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x - s / 2,
              top: y - s / 2,
              width: s,
              height: s,
              borderRadius: '50%',
              background:
                'radial-gradient(circle, rgba(120,90,70,0.9) 0%, rgba(80,60,50,0.5) 40%, rgba(0,0,0,0) 70%)',
              filter: 'blur(60px)',
              opacity: b.op,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

/* ---------------- Phénix ---------------- */

const Phoenix: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const t = frame / FPS;
  const p = phoenixAt(t);
  const img = p.gold ? staticFile('assets/phoenix_gold.png') : staticFile('assets/phoenix_main.png');
  const base = Math.min(width, height);
  const size = base * (p.gold ? 0.8 : 0.95) * p.scale;

  const floatY = p.gold ? Math.sin(t * 0.7) * 12 : 0;
  const rot = p.gold ? Math.sin(t * 0.35) * 2 : 0;

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        opacity: Math.max(0, p.opacity),
        transform: `translate(${p.x}px, ${p.y + floatY}px)`,
      }}
    >
      <div
        style={{
          position: 'relative',
          width: size,
          height: size * 0.72,
          transform: `rotate(${rot}deg)`,
        }}
      >
        {/* halo / glow */}
        <Img
          src={img}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            mixBlendMode: 'screen',
            filter: 'blur(40px) saturate(1.4)',
            opacity: 0.7,
          }}
        />
        <Img
          src={img}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            mixBlendMode: 'screen',
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

/* ---------------- Flamme centrale ---------------- */

const Flame: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const t = frame / FPS;
  const intensity = flameAt(t);
  const flick = 1 + 0.08 * Math.sin(t * 13) + 0.05 * Math.sin(t * 7.3) + 0.03 * Math.sin(t * 23);
  const s = Math.min(width, height) * (0.08 + 0.28 * Math.min(1, intensity)) * flick;
  const opacity = Math.min(1, 0.12 + intensity * 0.9);

  if (intensity <= 0.03) {
    return null;
  }

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'flex-end',
        alignItems: 'center',
        paddingBottom: height * 0.03,
        opacity,
      }}
    >
      <div
        style={{
          position: 'relative',
          width: s,
          height: s * 1.35,
          filter: 'blur(1px)',
        }}
      >
        {/* halo extérieur */}
        <div
          style={{
            position: 'absolute',
            left: '-45%',
            bottom: '-8%',
            width: '190%',
            height: '190%',
            borderRadius: '50%',
            background:
              'radial-gradient(ellipse at 50% 80%, rgba(255,110,20,0.45) 0%, rgba(255,60,10,0.15) 45%, rgba(0,0,0,0) 70%)',
            filter: 'blur(30px)',
          }}
        />
        {/* flamme */}
        <div
          style={{
            position: 'absolute',
            left: '50%',
            bottom: 0,
            transform: 'translateX(-50%)',
            width: '100%',
            height: '100%',
            background:
              'radial-gradient(ellipse at 50% 100%, rgba(255,230,150,0.95) 0%, rgba(255,150,40,0.9) 30%, rgba(255,70,10,0.55) 55%, rgba(120,20,0,0) 75%)',
            borderRadius: '50% 50% 50% 50% / 72% 72% 28% 28%',
            transformOrigin: '50% 100%',
            scale: `${1 + 0.06 * Math.sin(t * 16)} 1`,
          }}
        />
        {/* noyau */}
        <div
          style={{
            position: 'absolute',
            left: '50%',
            bottom: 0,
            transform: 'translateX(-50%)',
            width: '46%',
            height: '62%',
            background:
              'radial-gradient(ellipse at 50% 100%, rgba(255,255,240,0.95) 0%, rgba(255,220,120,0.7) 45%, rgba(255,120,30,0) 75%)',
            borderRadius: '50% 50% 50% 50% / 72% 72% 28% 28%',
            transformOrigin: '50% 100%',
            scale: `${1 + 0.08 * Math.sin(t * 11 + 2)} 1`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

/* ---------------- Fond complet ---------------- */

export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const t = frame / FPS;
  const grade = gradeAt(t);
  const flame = flameAt(t);

  return (
    <AbsoluteFill style={{ backgroundColor: '#030303', overflow: 'hidden' }}>
      {/* base radiale */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `radial-gradient(ellipse at 50% ${75 + 10 * Math.sin(t * 0.5)}%, rgba(70,26,10,${
            0.35 + 0.4 * Math.min(1, flame)
          }) 0%, rgba(10,6,4,0.9) 55%, #030303 100%)`,
        }}
      />
      <Smoke />
      <Embers />
      <Phoenix />
      <Flame />
      {/* voile de teinte (arc de couleur) */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: grade.tint,
          opacity: grade.tintA,
          mixBlendMode: 'screen',
        }}
      />
      {/* vignette */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background:
            'radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};

/* ---------------- Grain cinématique ---------------- */

const NOISE_SVG = `data:image/svg+xml;utf8,${encodeURIComponent(
  `<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#n)' opacity='0.5'/></svg>`
)}`;

export const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  const jx = (frame % 3) * 40;
  const jy = (frame % 5) * 26;
  return (
    <AbsoluteFill
      style={{
        backgroundImage: `url("${NOISE_SVG}")`,
        backgroundRepeat: 'repeat',
        backgroundPosition: `${jx}px ${jy}px`,
        mixBlendMode: 'overlay',
        opacity: 0.14,
      }}
    />
  );
};

export const BENIN_BAR: React.FC<{ height: number }> = ({ height }) => (
  <div
    style={{
      position: 'absolute',
      left: 0,
      right: 0,
      bottom: 0,
      height,
      display: 'flex',
    }}
  >
    <div style={{ width: '33.3%', height: '100%', background: COLORS.green }} />
    <div style={{ width: '33.3%', height: '100%', background: COLORS.yellow }} />
    <div style={{ width: '33.4%', height: '100%', background: COLORS.red }} />
  </div>
);
