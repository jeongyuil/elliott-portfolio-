export const userData = {
    id: "user_1",
    name: "User",
    nickname: "루나",
    avatar: "🐰",
    level: 5,
    xp: 1250,
    stars: 350,
    streak: 7,
    onboardingCompleted: true,
    stats: {
        totalStudyTime: 750,
        missionsCompleted: 45,
        vocabularyLearned: 230,
        pronunciationAccuracy: 85,
    },
};

export interface Mission {
    id: number;
    title: string;
    description: string;
    emoji: string;
    difficulty: "쉬움" | "보통" | "어려움";
    duration: number;
    rewards: {
        stars: number;
        xp: number;
    };
}

export const missions: Mission[] = [
    {
        id: 1,
        title: "동물원 친구들 만나기",
        description: "동물 친구들의 이름을 영어로 배워봐요!",
        emoji: "🦁",
        difficulty: "쉬움",
        duration: 180,
        rewards: { stars: 10, xp: 50 },
    },
    {
        id: 2,
        title: "맛있는 과일 가게",
        description: "사과, 바나나, 포도... 맛있는 과일들을 영어로 말해볼까요?",
        emoji: "🍎",
        difficulty: "쉬움",
        duration: 180,
        rewards: { stars: 10, xp: 50 },
    },
    {
        id: 3,
        title: "우리 가족 소개하기",
        description: "엄마, 아빠, 동생을 영어로 어떻게 부를까요?",
        emoji: "👨‍👩‍👧‍👦",
        difficulty: "보통",
        duration: 300,
        rewards: { stars: 20, xp: 100 },
    },
    {
        id: 4,
        title: "학교 가는 길",
        description: "학교에서 볼 수 있는 물건들을 찾아봐요.",
        emoji: "🏫",
        difficulty: "보통",
        duration: 300,
        rewards: { stars: 20, xp: 100 },
    },
    {
        id: 5,
        title: "신비한 우주 여행",
        description: "우주선, 별, 달... 우주에는 무엇이 있을까요?",
        emoji: "🚀",
        difficulty: "어려움",
        duration: 420,
        rewards: { stars: 30, xp: 150 },
    },
    {
        id: 6,
        title: "알록달록 색깔 놀이",
        description: "빨강, 파랑, 노랑... 세상의 모든 색깔들을 영어로!",
        emoji: "🎨",
        difficulty: "쉬움",
        duration: 180,
        rewards: { stars: 10, xp: 50 },
    }
];

export const weeklyGoals = {
    xp: { current: 850, target: 1000 },
    missions: { current: 4, target: 7 },
    studyTime: { current: 45, target: 60 },
    words: { current: 15, target: 20 },
};

export interface VocabularyCategory {
    id: string;
    name: string;
    emoji: string;
    wordsLearned: number;
    totalWords: number;
}

export const vocabularyCategories: VocabularyCategory[] = [
    {
        id: "food",
        name: "음식",
        emoji: "🍎",
        wordsLearned: 10,
        totalWords: 10,
    },
    {
        id: "animals",
        name: "동물",
        emoji: "🐶",
        wordsLearned: 7,
        totalWords: 10,
    },
    {
        id: "colors",
        name: "색깔",
        emoji: "🎨",
        wordsLearned: 0,
        totalWords: 10,
    },
    {
        id: "numbers",
        name: "숫자",
        emoji: "🔢",
        wordsLearned: 10,
        totalWords: 10,
    },
    {
        id: "family",
        name: "가족",
        emoji: "👨‍👩‍👧‍👦",
        wordsLearned: 5,
        totalWords: 10,
    },
    {
        id: "body",
        name: "신체",
        emoji: "👁️",
        wordsLearned: 8,
        totalWords: 10,
    },
    {
        id: "weather",
        name: "날씨",
        emoji: "☀️",
        wordsLearned: 3,
        totalWords: 10,
    },
    {
        id: "clothes",
        name: "옷",
        emoji: "👕",
        wordsLearned: 0,
        totalWords: 10,
    },
    {
        id: "school",
        name: "학교",
        emoji: "🏫",
        wordsLearned: 6,
        totalWords: 10,
    },
    {
        id: "toys",
        name: "장난감",
        emoji: "🧸",
        wordsLearned: 4,
        totalWords: 10,
    },
    {
        id: "transportation",
        name: "교통",
        emoji: "🚗",
        wordsLearned: 2,
        totalWords: 10,
    },
    {
        id: "nature",
        name: "자연",
        emoji: "🌳",
        wordsLearned: 0,
        totalWords: 10,
    },
];

export const shopItems = [
    { id: 'skin_popo_pirate', name: '해적 포포', description: '바다를 누비는 해적 포포!', emoji: '🏴‍☠️', price: 200 },
    { id: 'skin_luna_detective', name: '탐정 루나', description: '수수께끼를 푸는 루나!', emoji: '🕵️‍♀️', price: 200 },
    { id: 'skin_popo_chef', name: '요리사 포포', description: '맛있는 요리를 하는 포포!', emoji: '👨‍🍳', price: 150 },
    { id: 'skin_luna_artist', name: '화가 루나', description: '그림을 그리는 루나!', emoji: '🎨', price: 150 },
];

export const learningProgressData = [
    { date: 'Mon', xp: 50, words: 10 },
    { date: 'Tue', xp: 80, words: 15 },
    { date: 'Wed', xp: 40, words: 8 },
    { date: 'Thu', xp: 100, words: 20 },
    { date: 'Fri', xp: 60, words: 12 },
    { date: 'Sat', xp: 120, words: 25 },
    { date: 'Sun', xp: 90, words: 18 },
];

export const peerComparisonData = [
    { category: '언어', myValue: 85, peerAverage: 70, unit: '점' },
    { category: '인지', myValue: 75, peerAverage: 65, unit: '점' },
    { category: '정서', myValue: 90, peerAverage: 80, unit: '점' },
];

export const historicalLearningData = [
    { week: 1, xp: 500, missions: 5, studyTime: 5, words: 50, date: '2024-01-01' },
    { week: 2, xp: 600, missions: 6, studyTime: 6, words: 60, date: '2024-01-08' },
    { week: 3, xp: 700, missions: 7, studyTime: 7, words: 70, date: '2024-01-15' },
    { week: 4, xp: 850, missions: 8, studyTime: 8, words: 85, date: '2024-01-22' },
];
