import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, Sequence } from 'remotion';
import {
  FPS,
  FONTS,
  COLORS,
  clamp01,
  easeOutCubic,
  easeOutBack,
  easeInOut,
} from '../theme';
import type { LyricLine } from '../data';
import { Icon } from '../icons';

/* ------------------------------------------------------------------ */
/*  Helpers                                                             */
/* ------------------------------------------------------------------ */

function normalize(w: string) {
  return w
    .toLowerCase()
    .replace(/[^a-z0-9àâçéèêëîïôûùüÿœæ'-]/g, '');
}

function tokenize(main: string, emphasis?: string[]) {
  const emphSet = new Set((emphasis ?? []).map(normalize));
  return main.split(' ').map((w, i) => ({
    text: w,
    key: i,
    emphasized: emphSet.has(normalize(w)),
  }));
}

/* ------------------------------------------------------------------ */
/*  Spécifications typographiques par kind                              */
/* ------------------------------------------------------------------ */

interface Spec {
  font: string;
  size: number;
  color: string;
  letterSpacing?: string;
  weight?: number;
}

function spec(kind: LyricLine['kind'], w: number, h: number): Spec {
  switch (kind) {
    case 'hook':
      return { font: FONTS.display, size: w * 0.056, color: COLORS.white, letterSpacing: '0.01em' };
    case 'final':
      return { font: FONTS.display, size: w * 0.064, color: COLORS.white, letterSpacing: '0.01em' };
    case 'verse':
      return { font: FONTS.body, size: w * 0.048, color: COLORS.white, weight: 900 };
    case 'quote':
      return { font: FONTS.body, size: w * 0.041, color: '#c3c9d4', weight: 700 };
    case 'paren':
      return { font: FONTS.body, size: w * 0.033, color: COLORS.white, weight: 700 };
    case 'bridge':
      return { font: FONTS.heavy, size: w * 0.05, color: COLORS.white };
    case 'echo':
      return { font: FONTS.body, size: w * 0.042, color: COLORS.white, weight: 800 };
    case 'title':
      return { font: FONTS.brush, size: w * 0.098, color: COLORS.white };
    case 'cta':
      return { font: FONTS.ui, size: w * 0.026, color: COLORS.white, weight: 800 };
    case 'stamp':
      return { font: FONTS.brush, size: w * 0.046, color: COLORS.white };
    case 'logo':
      return { font: FONTS.brush, size: w * 0.042, color: COLORS.white };
    default:
      return { font: FONTS.body, size: w * 0.05, color: COLORS.white };
  }
}

function subSpec(w: number): Spec {
  return { font: FONTS.ui, size: w * 0.024, color: 'rgba(255,255,255,0.72)', weight: 600 };
}

/* ------------------------------------------------------------------ */
/*  Overlay FX (fracture lumineuse, clé dorée)                          */
/* ------------------------------------------------------------------ */

const Lightning: React.FC<{ color: string }> = ({ color }) => (
  <svg
    width="100%"
    height="100%"
    viewBox="0 0 1000 400"
    preserveAspectRatio="none"
    style={{ position: 'absolute', inset: 0, mixBlendMode: 'screen' }}
  >
    <polyline
      points="60,20 240,180 180,180 340,360 520,120 470,120 620,20 760,300 700,300 940,60"
      fill="none"
      stroke={color}
      strokeWidth="6"
      strokeLinejoin="round"
      strokeLinecap="round"
      style={{ filter: `drop-shadow(0 0 18px ${color}) drop-shadow(0 0 40px ${color})` }}
    />
  </svg>
);

/* ------------------------------------------------------------------ */
/*  Texte ligne à ligne (word-by-word kinetic)                          */
/* ------------------------------------------------------------------ */

export const LyricText: React.FC<{ line: LyricLine }> = ({ line }) => {
  const frame = useCurrentFrame();
  const { width: w, height: h } = useVideoConfig();
  const dur = Math.max(1, Math.round(line.end * FPS) - Math.round(line.start * FPS));
  const local = frame;

  const s = spec(line.kind, w, h);
  const sub = line.sub ? subSpec(w) : null;
  const tokens = tokenize(line.main, line.emphasis);
  const n = tokens.length;

  const wordMode = line.kind === 'hook' || line.kind === 'final';

  /* --- entrée / sortie --- */
  let entrance = 1;
  let lineY = 0;
  let lineScale = 1;
  let lineBlur = 0;

  if (wordMode) {
    entrance = 1;
  } else if (line.kind === 'verse' || line.kind === 'quote' || line.kind === 'rise') {
    const p = clamp01(local / (dur * 0.28));
    entrance = easeOutCubic(p);
    lineY = (1 - p) * (line.fx === 'rise' ? 90 : 46);
  } else if (line.kind === 'paren') {
    const p = clamp01(local / (dur * 0.3));
    entrance = p;
    lineBlur = (1 - p) * 10;
    lineY = (1 - p) * 18;
  } else if (line.kind === 'bridge') {
    const p = clamp01(local / (dur * 0.5));
    entrance = easeInOut(p);
    lineY = Math.sin(frame / 28) * 6;
    lineScale = 0.98 + 0.02 * p;
  } else if (line.kind === 'echo') {
    const p = clamp01(local / (dur * 0.6));
    entrance = easeInOut(p);
  }

  /* sortie en fondu (sauf pour les lignes qui enchaînent sans chevauchement) */
  const exitDur = dur * 0.12;
  let exit = 0;
  if (line.kind === 'verse' || line.kind === 'quote' || line.kind === 'hook' || line.kind === 'final' || line.kind === 'bridge') {
    exit = clamp01((local - (dur - exitDur)) / exitDur);
  }
  const opacity = entrance * (1 - exit);

  /* --- découpage par mot --- */
  const gap = Math.min(dur * 0.16, (dur * 0.72) / Math.max(1, n));
  const wDur = Math.max(1, dur - gap * (n - 1));

  const yPct = line.y ?? 52;

  const renderWord = (word: string, emphasized: boolean, i: number) => {
    let scale = 1;
    let wy = 0;
    let glow = 0;
    let color = s.color;

    if (wordMode) {
      const wStart = i * gap;
      const wp = clamp01((local - wStart) / wDur);
      const back = easeOutBack(wp);
      scale = 1 + (1 - back) * 0.7;
      wy = (1 - easeOutCubic(wp)) * 10;
      glow = (1 - clamp01(wp * 2)) * 1;
      color = emphasized ? COLORS.gold : s.color;
    } else {
      color = emphasized ? COLORS.gold : s.color;
    }

    return (
      <span
        key={i}
        style={{
          display: 'inline-block',
          marginRight: '0.28em',
          transform: `translateY(${wy}px) scale(${scale})`,
          transformOrigin: '50% 60%',
          color,
          textShadow: glow > 0 ? `0 0 ${glow * 26}px rgba(255,255,255,${glow})` : emphasized ? `0 0 22px rgba(255,201,60,0.45)` : 'none',
        }}
      >
        {word}
      </span>
    );
  };

  const mainStyle: React.CSSProperties = {
    fontFamily: s.font,
    fontSize: s.size,
    color: s.color,
    fontWeight: s.weight ?? 400,
    letterSpacing: s.letterSpacing,
    lineHeight: 1.12,
    textAlign: 'center',
    maxWidth: w * 0.9,
    opacity,
    transform: `translateY(${lineY}px) scale(${lineScale})`,
    filter: lineBlur > 0 ? `blur(${lineBlur}px)` : undefined,
    fontStyle: line.kind === 'quote' ? 'italic' : 'normal',
    textShadow:
      line.kind === 'verse' ? '0 2px 18px rgba(0,0,0,0.7)' : line.kind === 'bridge' ? '0 0 34px rgba(255,190,90,0.35)' : '0 2px 14px rgba(0,0,0,0.6)',
  };

  const indent = line.kind === 'quote' || line.kind === 'paren' ? w * 0.06 : 0;

  /* --- FX clé dorée --- */
  const showKey = line.fx === 'key';
  const keyP = clamp01(local / (dur * 0.4));

  /* --- FX fracture --- */
  const showCrack = line.fx === 'crack' || line.fx === 'fracture';
  const crackP = showCrack ? 1 - clamp01(local / (dur * 0.55)) : 0;

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: `${yPct}%`,
          left: 0,
          right: 0,
          transform: 'translateY(-50%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          paddingLeft: indent,
          paddingRight: indent,
        }}
      >
        <div style={mainStyle}>
          {tokens.map((t, i) => renderWord(t.text, t.emphasized, i))}
        </div>
        {sub && (
          <div
            style={{
              fontFamily: sub.font,
              fontSize: sub.size,
              fontWeight: sub.weight,
              color: sub.color,
              lineHeight: 1.2,
              textAlign: 'center',
              maxWidth: w * 0.9,
              marginTop: h * 0.015,
              opacity: opacity * 0.92,
            }}
          >
            {sub.text}
          </div>
        )}
        {showKey && (
          <div
            style={{
              position: 'absolute',
              right: w * 0.06,
              top: '50%',
              transform: `translateY(-50%) scale(${easeOutBack(keyP)}) rotate(${Math.sin(frame / 12) * 8}deg)`,
              opacity: keyP,
              filter: 'drop-shadow(0 0 16px rgba(255,201,60,0.7))',
            }}
          >
            <Icon name="key" size={w * 0.055} color={COLORS.gold} />
          </div>
        )}
      </div>
      {showCrack && crackP > 0 && (
        <div style={{ position: 'absolute', inset: 0, opacity: crackP * 0.9 }}>
          <Lightning color={line.fx === 'fracture' ? '#ffffff' : '#FFE9A8'} />
        </div>
      )}
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/*  Tampon signature                                                    */
/* ------------------------------------------------------------------ */

const STAMP_COLORS: Record<string, string> = {
  red: COLORS.red,
  gold: COLORS.gold,
  green: COLORS.green,
};

export const Stamp: React.FC<{ line: LyricLine }> = ({ line }) => {
  const frame = useCurrentFrame();
  const { width: w } = useVideoConfig();
  const dur = Math.max(1, Math.round(line.end * FPS) - Math.round(line.start * FPS));
  const local = frame;

  const color = STAMP_COLORS[line.note ?? 'red'] ?? COLORS.red;

  const p = clamp01(local / (dur * 0.3));
  const scale = easeOutBack(p);
  const exit = clamp01((local - (dur - dur * 0.15)) / (dur * 0.15));

  /* tremblement "drop" sur la première répétition du tag final */
  let shake = 0;
  if (line.fx === 'fracture') {
    const d = local / FPS;
    const decay = Math.max(0, 1 - d / 0.7);
    shake = Math.sin(d * 70) * 6 * decay;
  }

  const pulse = 1 + 0.025 * Math.sin(frame / 4.5);

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <div
        style={{
          opacity: (1 - exit),
          transform: `translateX(${shake}px) rotate(-3deg) scale(${scale * pulse})`,
          border: `4px solid ${color}`,
          outline: `2px solid ${color}`,
          outlineOffset: 4,
          borderRadius: 14,
          padding: `${w * 0.012}px ${w * 0.03}px`,
          background: 'rgba(0,0,0,0.55)',
          boxShadow: `0 0 40px ${color}55, inset 0 0 30px ${color}33`,
        }}
      >
        <div
          style={{
            fontFamily: FONTS.brush,
            fontSize: w * 0.048,
            color,
            letterSpacing: '0.02em',
            textShadow: `0 0 24px ${color}99`,
            whiteSpace: 'nowrap',
          }}
        >
          {line.main}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/*  CTA avec icône qui "pop"                                            */
/* ------------------------------------------------------------------ */

const ICON_BG: Record<string, string> = {
  bell: '#FF7A1A',
  heart: '#E8112D',
  comment: '#FCD116',
  share: '#008751',
};

export const CtaLine: React.FC<{ line: LyricLine }> = ({ line }) => {
  const frame = useCurrentFrame();
  const { width: w, height: h } = useVideoConfig();
  const dur = Math.max(1, Math.round(line.end * FPS) - Math.round(line.start * FPS));
  const local = frame;

  const p = clamp01(local / (dur * 0.3));
  const iconPop = easeOutBack(clamp01(local / (dur * 0.35)));
  const exit = clamp01((local - (dur - dur * 0.18)) / (dur * 0.18));
  const yPct = line.y ?? 52;

  const bg = ICON_BG[line.icon ?? 'bell'] ?? COLORS.gold;

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <div
        style={{
          position: 'absolute',
          top: `${yPct}%`,
          transform: 'translateY(-50%)',
          display: 'flex',
          alignItems: 'center',
          gap: w * 0.016,
          opacity: (1 - exit),
        }}
      >
        {line.icon && (
          <div
            style={{
              width: w * 0.045,
              height: w * 0.045,
              borderRadius: '14%',
              background: bg,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transform: `scale(${iconPop})`,
              boxShadow: `0 0 26px ${bg}88`,
              flexShrink: 0,
            }}
          >
            <Icon name={line.icon as any} size={w * 0.026} color="#FFFFFF" />
          </div>
        )}
        <div
          style={{
            fontFamily: FONTS.ui,
            fontSize: w * 0.026,
            fontWeight: 800,
            color: '#FFFFFF',
            letterSpacing: '0.01em',
            transform: `translateX(${(1 - easeOutCubic(p)) * 24}px)`,
            opacity: p,
            textShadow: '0 2px 14px rgba(0,0,0,0.7)',
            maxWidth: w * 0.8,
          }}
        >
          {line.main}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/*  Titre (typographie brush graffiti)                                  */
/* ------------------------------------------------------------------ */

export const TitleCard: React.FC<{ line: LyricLine }> = ({ line }) => {
  const frame = useCurrentFrame();
  const { width: w } = useVideoConfig();
  const dur = Math.max(1, Math.round(line.end * FPS) - Math.round(line.start * FPS));
  const local = frame;

  const p = clamp01(local / (dur * 0.32));
  const scale = easeOutBack(p);
  const exit = clamp01((local - (dur - dur * 0.4)) / (dur * 0.4));

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <div
        style={{
          opacity: (1 - exit),
          transform: `scale(${scale}) rotate(-1.5deg)`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            fontFamily: FONTS.brush,
            fontSize: w * 0.098,
            color: '#FFFFFF',
            lineHeight: 1,
            textAlign: 'center',
            textShadow: [
              '3px 3px 0 #E8112D',
              '-3px -3px 0 #E8112D',
              '3px -3px 0 #E8112D',
              '-3px 3px 0 #E8112D',
              '0 0 30px rgba(255,120,20,0.85)',
              '0 0 70px rgba(255,60,10,0.5)',
            ].join(','),
            maxWidth: w * 0.92,
          }}
        >
          {line.main}
        </div>
        {line.sub && (
          <div
            style={{
              fontFamily: FONTS.ui,
              fontSize: w * 0.024,
              fontWeight: 600,
              color: 'rgba(255,255,255,0.85)',
              letterSpacing: '0.06em',
              marginTop: w * 0.01,
            }}
          >
            {line.sub}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/*  Logo de fin                                                         */
/* ------------------------------------------------------------------ */

export const LogoCard: React.FC<{ line: LyricLine }> = ({ line }) => {
  const frame = useCurrentFrame();
  const { width: w } = useVideoConfig();
  const dur = Math.max(1, Math.round(line.end * FPS) - Math.round(line.start * FPS));
  const local = frame;
  const p = clamp01(local / (dur * 0.5));
  const yPct = line.y ?? 80;

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <div
        style={{
          position: 'absolute',
          top: `${yPct}%`,
          transform: 'translateY(-50%)',
          display: 'flex',
          alignItems: 'center',
          gap: w * 0.014,
          opacity: easeInOut(p),
        }}
      >
        <Icon name="flag" size={w * 0.05} />
        <div
          style={{
            fontFamily: FONTS.brush,
            fontSize: w * 0.044,
            color: COLORS.white,
            textShadow: '0 0 26px rgba(255,201,60,0.6)',
          }}
        >
          {line.main}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/*  Dispatch                                                            */
/* ------------------------------------------------------------------ */

export const LineSequence: React.FC<{ line: LyricLine }> = ({ line }) => {
  const start = Math.round(line.start * FPS);
  const dur = Math.max(1, Math.round(line.end * FPS) - start);

  let child: React.ReactNode;
  switch (line.kind) {
    case 'stamp':
      child = <Stamp line={line} />;
      break;
    case 'cta':
      child = <CtaLine line={line} />;
      break;
    case 'title':
      child = <TitleCard line={line} />;
      break;
    case 'logo':
      child = <LogoCard line={line} />;
      break;
    default:
      child = <LyricText line={line} />;
  }

  return (
    <Sequence from={start} durationInFrames={dur}>
      {child}
    </Sequence>
  );
};
