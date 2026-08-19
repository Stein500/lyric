import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { Background, Grain } from './components/Background';
import { LineSequence } from './components/text';
import { SCENES } from './data';
import { FPS, gradeAt } from './theme';

export const LyricVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const grade = gradeAt(t);

  return (
    <AbsoluteFill style={{ backgroundColor: '#000000' }}>
      <AbsoluteFill
        style={{
          filter: `saturate(${grade.sat}) brightness(${grade.bright})`,
        }}
      >
        <Background />
        {SCENES.flatMap((s) => s.lines).map((line, i) => (
          <LineSequence key={i} line={line} />
        ))}
      </AbsoluteFill>
      <Grain />
    </AbsoluteFill>
  );
};
