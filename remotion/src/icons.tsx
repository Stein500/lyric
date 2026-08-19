import React from 'react';

export type IconName = 'bell' | 'heart' | 'comment' | 'share' | 'play' | 'key' | 'fire' | 'flag';

export const Icon: React.FC<{
  name: IconName;
  size: number;
  color?: string;
}> = ({ name, size, color = '#FFFFFF' }) => {
  switch (name) {
    case 'bell':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <path
            d="M12 2a6 6 0 0 0-6 6v3.2L4.4 14a1 1 0 0 0 .8 1.6h13.6a1 1 0 0 0 .8-1.6L18 11.2V8a6 6 0 0 0-6-6Z"
            fill={color}
          />
          <path d="M10 19a2 2 0 0 0 4 0" stroke={color} strokeWidth="2" strokeLinecap="round" />
        </svg>
      );
    case 'heart':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
          <path d="M12 21s-7.5-4.9-9.5-9.2C1.2 8.6 2.6 5 6 5c2 0 3.2 1.2 4 2.4C10.8 6.2 12 5 14 5c3.4 0 4.8 3.6 3.5 6.8C19.5 16.1 12 21 12 21Z" />
        </svg>
      );
    case 'comment':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <path
            d="M4 4h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H8l-4 4V5a1 1 0 0 1 1-1Z"
            fill={color}
          />
        </svg>
      );
    case 'share':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7" />
          <path d="M16 6l-4-4-4 4" />
          <path d="M12 2v14" />
        </svg>
      );
    case 'play':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
          <path d="M8 5v14l11-7Z" />
        </svg>
      );
    case 'key':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="7.5" cy="15.5" r="4.5" />
          <path d="M10.7 12.3 20 3M16 7l2 2M13 10l2 2" />
        </svg>
      );
    case 'fire':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
          <path d="M12 22c-4.4 0-7-2.8-7-6.5 0-2.4 1.3-4.2 2.4-5.6.3 1.1 1 2 1.6 2.6.4-2.5 2.3-4.3 3-6.5 1.6 1.2 2.6 2.9 3 4.5.9 1.2 2 2.7 2 5 0 3.7-2.4 6.5-7 6.5Z" />
        </svg>
      );
    case 'flag':
      return (
        <svg width={size} height={size} viewBox="0 0 60 40">
          <rect x="0" y="0" width="20" height="40" fill="#008751" />
          <rect x="20" y="0" width="40" height="20" fill="#FCD116" />
          <rect x="20" y="20" width="40" height="20" fill="#E8112D" />
        </svg>
      );
    default:
      return null;
  }
};
