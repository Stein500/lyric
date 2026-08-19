import { registerRoot } from 'remotion';
import React from 'react';
import { Composition } from 'remotion';
import { Root } from './Root';
import { FPS, TOTAL_SECONDS } from './theme';

const duration = Math.round(TOTAL_SECONDS * FPS);

registerRoot(() => {
  return (
    <>
      <Composition
        id="ImNotAfraidLyrics"
        component={Root}
        durationInFrames={duration}
        fps={FPS}
        width={1920}
        height={1080}
      />
      <Composition
        id="ImNotAfraidVertical"
        component={Root}
        durationInFrames={duration}
        fps={FPS}
        width={1080}
        height={1920}
      />
    </>
  );
});
