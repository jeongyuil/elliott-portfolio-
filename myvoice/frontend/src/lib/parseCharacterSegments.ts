/** Parse [나레이션] / [포포] / [루나] tagged AI responses into segments */
export interface SpeakerSegment {
  speaker: 'narrator' | 'popo' | 'luna' | 'unknown';
  text: string;
}

const TAG_MAP: Record<string, SpeakerSegment['speaker']> = {
  '나레이션': 'narrator',
  '포포': 'popo',
  '루나': 'luna',
};

export function parseCharacterSegments(text: string): SpeakerSegment[] {
  const regex = /\[(나레이션|포포|루나)\]\s*/g;
  const segments: SpeakerSegment[] = [];
  let lastIndex = 0;
  let lastSpeaker: SpeakerSegment['speaker'] = 'unknown';
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    const before = text.slice(lastIndex, match.index).trim();
    if (before) {
      segments.push({ speaker: lastSpeaker, text: before });
    }
    lastSpeaker = TAG_MAP[match[1]] || 'unknown';
    lastIndex = regex.lastIndex;
  }

  const remaining = text.slice(lastIndex).trim();
  if (remaining) {
    segments.push({ speaker: lastSpeaker, text: remaining });
  }

  if (segments.length === 0 && text.trim()) {
    segments.push({ speaker: 'unknown', text: text.trim() });
  }

  return segments;
}

export const CHARACTER_IMAGES = {
  popo: '/assets/characters/popo.png',
  luna: '/assets/characters/luna.png',
  captain_girl: '/assets/characters/girl_captain.png',
  captain_boy: '/assets/characters/boy_captain.png',
  narrator: '',  // narrator uses 📖 emoji (no character image)
} as const;

export const SPEAKER_STYLES: Record<
  SpeakerSegment['speaker'],
  { img: string; emoji: string; label: string; bg: string; border: string; avatarBg: string }
> = {
  narrator: { img: '', emoji: '📖', label: '', bg: 'bg-gradient-to-r from-slate-50 to-gray-50', border: 'border-gray-200', avatarBg: 'bg-amber-100' },
  popo: { img: CHARACTER_IMAGES.popo, emoji: '', label: '포포', bg: 'bg-white', border: 'border-[var(--bt-border)]', avatarBg: 'bg-indigo-100' },
  luna: { img: CHARACTER_IMAGES.luna, emoji: '', label: '루나', bg: 'bg-gradient-to-r from-purple-50 to-indigo-50', border: 'border-purple-200', avatarBg: 'bg-purple-100' },
  unknown: { img: CHARACTER_IMAGES.popo, emoji: '', label: '포포', bg: 'bg-white', border: 'border-[var(--bt-border)]', avatarBg: 'bg-indigo-100' },
};
