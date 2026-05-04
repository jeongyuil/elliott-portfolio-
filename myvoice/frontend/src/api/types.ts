export interface LoginResponse {
    accessToken: string;
    familyId: string;
    tokenType: string;
}

export interface ChildStats {
    totalStudyTime: number;
    missionsCompleted: number;
    vocabularyLearned: number;
    pronunciationAccuracy: number;
}

export interface ChildUpdate {
    name?: string;
    birthDate?: string; // YYYY-MM-DD
    gender?: string;
    primaryLanguage?: string;
    developmentStageLanguage?: string;
    avatarId?: string;
    pin?: string;
}

export interface ChildCreate {
    name: string;
    birthDate: string; // YYYY-MM-DD
    gender?: string;
    primaryLanguage?: string;
    developmentStageLanguage?: string;
    avatarId?: string;
    pin?: string;
}

export interface ChildProfile {
    childId: string;
    familyId: string;
    name: string;
    birthDate: string; // Added
    gender: string;    // Added
    primaryLanguage: string; // Added
    developmentStageLanguage?: string | null; // Added
    nickname: string | null;
    avatarEmoji: string | null;
    avatarId?: string | null; // Added for 3D Avatars
    avatarUrl?: string | null;
    level: number;
    xp: number;
    streak: number;
    stats: ChildStats;
    onboardingCompleted: boolean;
    availableAvatars?: { id: string; name: string; image: string }[];
}

export interface WeeklyGoal {
    xpCurrent: number;
    xpTarget: number;
    missionsCurrent: number;
    missionsTarget: number;
    studyTimeCurrent: number;
    studyTimeTarget: number;
    wordsCurrent: number;
    wordsTarget: number;
}

export interface Adventure {
    sessionId: string;
    title: string;
    emoji: string;
    status: 'locked' | 'unlocked' | 'in_progress' | 'completed';
    difficulty: string;
    week: number;
    order: number;
    earnedStars?: number;
    earnedXp?: number;
}

export interface KidHomeResponse {
    child: ChildProfile;
    weeklyGoals: WeeklyGoal;
    recentAdventures: Adventure[];
    streak: number;
    stars: number;
    dailyBonusAvailable: boolean;
}

export interface DailyBonusResponse {
    starsReward: number;
    consecutiveDays: number;
    newStars: number;
    newStreak: number;
}

export interface VocabularyCategory {
    id: string;
    name: string;
    emoji: string;
    totalWords: number;
    wordsLearned: number;
}

export interface VocabularyWord {
    id: string;
    word: string;
    korean: string;
    emoji: string;
}

export interface ShopItem {
    id: string;
    name: string;
    description: string;
    emoji: string;
    price: number;
    itemType: string;
}

export interface Inventory {
    stars: number;
    ownedSkins: string[];
    activePopoSkin: string | null;
    activeLunaSkin: string | null;
}

export interface ShopResponse {
    items: ShopItem[];
    inventory: Inventory;
}

export interface PurchaseResponse {
    success: boolean;
    newStars: number;
    inventory: Inventory;
}

// === Voice AI & Adventure Detail Types ===
// All camelCase — api/client.ts auto-converts snake_case responses from backend.

export interface ActivityInfo {
    activityId: string;
    name: string;
    activityType: string;
    introNarratorScript: string | null;
    outroNarratorScript: string | null;
    estimatedDurationMinutes: number | null;
    imagePath: string | null;
}

export interface AdventureDetail {
    id: string;
    title: string;
    description: string;
    emoji: string;
    difficulty: string;
    duration: number;
    rewards: { stars: number; xp: number };
    languageMode: string;
    koreanRatio: number;
    activities: ActivityInfo[];
}

export interface SessionStartResponse {
    sessionId: string;
    childId: string;
    sessionType: string;
    status: string;
    startTime: string;
    curriculumUnitId: string | null;
    activities: ActivityInfo[];
}

export interface UtteranceResponse {
    utteranceId: string;
    childText: string | null;
    aiResponseText: string | null;
    aiResponseAudioBase64: string | null;
    turnIndex: number;
    speakerType: string;
    feedback?: UtteranceFeedback;
    nextPhase?: string; // "transition" | "interactive"
}

export interface UtteranceFeedback {
    type: string;
    skill: string;
    level: number;
    message: string;
}

export interface SessionEndResponse {
    durationSeconds: number;
    totalTurns: number;
    earnedXp: number;
    newLevel: number;
    levelUp: boolean;
    engagementScore?: number | null;
}

export interface ConversationTurn {
    speaker: "narrator" | "ai" | "child";
    text: string;
    audioBase64?: string;
    feedback?: UtteranceFeedback;
}

export interface SkillLevelResponse {
    skillLevelId: string;
    childId: string;
    skillId: string;
    snapshotDate: string;
    rawScore: number | null;
    level: number;
    source: string;
}

export interface SkillListResponse {
    items: SkillLevelResponse[];
}

export interface ReportSkillSummary {
    skillId: string;
    skillName?: string;
    skillNameEn?: string;
    level?: number;
    summaryForParent?: string;
    trend?: number;          // e.g. +12, -3, 0
    canDo?: string;          // CAN-DO statement
    sparkline?: number[];    // 30-day score history (last 12 points)
}

export interface Report {
    reportId: string;
    periodStartDate: string;
    periodEndDate: string;
    createdAt?: string;
    summaryText?: string;
    strengthsSummary?: string;
    areasToImprove?: string;
    recommendationsNextMonth?: string;
    skillSummaries: ReportSkillSummary[];
}

export interface DashboardStats {
    totalSessions: number;
    totalLearningTimeMinutes: number;
    dailyBreakdown: { date: string; dayName: string; minutes: number }[];
}

// === Insights Types ===

export interface KeywordItem {
    word: string;
    count: number;
}

export interface EmotionItem {
    label: string;
    count: number;
    percentage: number;
}

export interface SentimentSummary {
    emotions: EmotionItem[];
    overall: string;
}

export interface TimelineDay {
    date: string;
    sessions: number;
    totalMinutes: number;
    totalTurns: number;
}

export interface LanguageMix {
    koreanRatio: number;
    englishRatio: number;
    totalUtterances: number;
}

export interface StoryTheme {
    theme: string;
    title: string;
    description: string;
    emoji: string;
    coverColor: string;
    totalUnits: number;
    completedUnits: number;
}

export interface BehaviorPatterns {
    avgSessionMinutes: number;
    avgEngagement: number;
    sessionCount: number;
    avgPronunciation: number;
    avgFluency: number;
    avgWordsPerTurn: number;
}
