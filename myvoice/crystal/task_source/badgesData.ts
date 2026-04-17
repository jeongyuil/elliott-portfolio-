/**
 * Badge System Data
 * Contains badge definitions and user badge progress
 */

export interface Badge {
  id: string;
  name: string;
  emoji: string;
  description: string;
  category: "learning" | "achievement" | "streak" | "skill";
  requirement: string;
  unlocked: boolean;
  unlockedDate?: string;
}

export const allBadges: Badge[] = [
  // Learning Badges
  {
    id: "first_mission",
    name: "첫 미션 완료",
    emoji: "🎯",
    description: "첫 번째 미션을 성공적으로 완료했어요!",
    category: "learning",
    requirement: "미션 1개 완료",
    unlocked: true,
    unlockedDate: "2026-02-01",
  },
  {
    id: "mission_master_10",
    name: "미션 마스터",
    emoji: "🏆",
    description: "10개의 미션을 완료했어요!",
    category: "learning",
    requirement: "미션 10개 완료",
    unlocked: true,
    unlockedDate: "2026-02-05",
  },
  {
    id: "vocab_explorer",
    name: "단어 탐험가",
    emoji: "📚",
    description: "100개 이상의 단어를 학습했어요!",
    category: "learning",
    requirement: "단어 100개 학습",
    unlocked: true,
    unlockedDate: "2026-02-03",
  },
  {
    id: "pronunciation_pro",
    name: "발음 달인",
    emoji: "🎤",
    description: "발음 정확도 90% 이상을 달성했어요!",
    category: "achievement",
    requirement: "발음 정확도 90% 이상",
    unlocked: false,
  },
  {
    id: "perfect_score",
    name: "완벽한 점수",
    emoji: "💯",
    description: "미션에서 만점을 받았어요!",
    category: "achievement",
    requirement: "미션 만점 달성",
    unlocked: true,
    unlockedDate: "2026-02-02",
  },
  {
    id: "speed_learner",
    name: "빠른 학습자",
    emoji: "⚡",
    description: "하루에 5개 이상의 미션을 완료했어요!",
    category: "achievement",
    requirement: "하루 미션 5개 완료",
    unlocked: false,
  },
  // Streak Badges
  {
    id: "streak_3",
    name: "3일 연속",
    emoji: "🔥",
    description: "3일 연속으로 학습했어요!",
    category: "streak",
    requirement: "3일 연속 학습",
    unlocked: true,
    unlockedDate: "2026-01-30",
  },
  {
    id: "streak_7",
    name: "일주일 연속",
    emoji: "🌟",
    description: "7일 연속으로 학습했어요!",
    category: "streak",
    requirement: "7일 연속 학습",
    unlocked: true,
    unlockedDate: "2026-02-06",
  },
  {
    id: "streak_30",
    name: "한 달 연속",
    emoji: "👑",
    description: "30일 연속으로 학습했어요!",
    category: "streak",
    requirement: "30일 연속 학습",
    unlocked: false,
  },
  // Skill Badges
  {
    id: "vocab_master",
    name: "어휘 마스터",
    emoji: "📖",
    description: "일상 어휘 스킬을 완성했어요!",
    category: "skill",
    requirement: "일상 어휘 스킬 레벨 5",
    unlocked: false,
  },
  {
    id: "pronunciation_expert",
    name: "발음 전문가",
    emoji: "🗣️",
    description: "발음 스킬을 완성했어요!",
    category: "skill",
    requirement: "발음 스킬 레벨 5",
    unlocked: false,
  },
  {
    id: "sentence_builder",
    name: "문장 제작자",
    emoji: "✍️",
    description: "문장 구성 스킬을 완성했어요!",
    category: "skill",
    requirement: "문장 구성 스킬 레벨 5",
    unlocked: false,
  },
  {
    id: "attention_champion",
    name: "집중력 챔피언",
    emoji: "🎯",
    description: "주의 집중 스킬을 완성했어요!",
    category: "skill",
    requirement: "주의 집중 스킬 레벨 5",
    unlocked: false,
  },
  {
    id: "emotion_expert",
    name: "감정 표현가",
    emoji: "💝",
    description: "정서 표현 스킬을 완성했어요!",
    category: "skill",
    requirement: "정서 표현 스킬 레벨 5",
    unlocked: false,
  },
  {
    id: "all_rounder",
    name: "올라운더",
    emoji: "🌈",
    description: "모든 카테고리의 스킬을 레벨 3 이상 달성했어요!",
    category: "skill",
    requirement: "모든 스킬 레벨 3 이상",
    unlocked: false,
  },
];

export function getUnlockedBadges(): Badge[] {
  return allBadges.filter((badge) => badge.unlocked);
}

export function getLockedBadges(): Badge[] {
  return allBadges.filter((badge) => !badge.unlocked);
}

export function getBadgesByCategory(category: Badge["category"]): Badge[] {
  return allBadges.filter((badge) => badge.category === category);
}

export function getRecentBadges(count: number = 6): Badge[] {
  return allBadges
    .filter((badge) => badge.unlocked && badge.unlockedDate)
    .sort((a, b) => {
      if (!a.unlockedDate || !b.unlockedDate) return 0;
      return new Date(b.unlockedDate).getTime() - new Date(a.unlockedDate).getTime();
    })
    .slice(0, count);
}
