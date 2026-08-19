import React from 'react';
import { AbsoluteFill, Audio, staticFile } from 'remotion';
import { LyricVideo } from './LyricVideo';

export const Root: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#000000' }}>
      <Audio src={staticFile('not afraid.mp3')} />
      <LyricVideo />
    </AbsoluteFill>
  );
};
