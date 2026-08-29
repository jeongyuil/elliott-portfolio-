/**
 * Skills Data - Based on Skill Dictionary v0.1
 * 
 * This file contains skill definitions for the language learning platform.
 * Skills are categorized into Language, Cognitive, and Emotional/Social skills.
 */

export type SkillCategory = "language" | "cognitive" | "emotional";
export type SkillMode = "receptive" | "expressive" | "both";
export type AgeBand = "4-6" | "7-9" | "10-12";
export type SkillUnit = "score_0_100" | "level_1_5" | "boolean";

export interface Skill {
    skill_id: string;
    name_kr: string;
    name_en: string;
    category: SkillCategory;
    mode: SkillMode;
    age_band: AgeBand;
    unit: SkillUnit;
    is_core_metric: boolean;
    description: string;
    can_do_examples: string[];
    emoji: string; // For visual representation
}

export interface UserSkillProgress {
    skill_id: string;
    current_value: number; // 0-100 for score, 1-5 for level, 0-1 for boolean
    last_updated: Date;
    attempts: number;
}

// Language Skills
export const languageSkills: Skill[] = [
    {
        skill_id: "LANG_VOCAB_DAILY_01",
        name_kr: "일상 어휘 이해 및 사용",
        name_en: "Daily-life Vocabulary (Basic)",
        category: "language",
        mode: "both",
        age_band: "7-9",
        unit: "score_0_100",
        is_core_metric: true,
        emoji: "📚",
        description: "일상생활과 관련된 기초 명사/동사/형용사를 듣고 이해하거나, 단어 또는 짧은 표현으로 말할 수 있는 능력",
        can_do_examples: [
            "가족, 동물, 음식, 장난감 등 20~40개의 일상 단어를 그림/상황과 매칭할 수 있다",
            "질문에 대해 단어 한 개만 말하더라도, 의미적으로 적절한 단어를 선택할 수 있다",
            "AI가 먼저 말한 단어를 따라 말하기가 가능하다"
        ]
    },
    {
        skill_id: "LANG_VOCAB_PREFERENCE_01",
        name_kr: "좋아하는 것/싫어하는 것 표현",
        name_en: "Likes & Dislikes Vocabulary",
        category: "language",
        mode: "expressive",
        age_band: "7-9",
        unit: "score_0_100",
        is_core_metric: true,
        emoji: "❤️",
        description: "동물, 음식, 놀이 등 선호 영역에서 'I like ~ / I don't like ~' 패턴을 활용해 자신의 취향을 영어로 표현하는 능력",
        can_do_examples: [
            "AI가 제시한 여러 그림 중에서 자신이 좋아하는 것을 선택하고, 'I like ___.'로 말할 수 있다",
            "조금 싫어하는 대상에 대해 'I don't like ___.'를 말해볼 수 있다",
            "한 세션 내에서 최소 1~2개의 선호 문장을 성공적으로 말할 수 있다"
        ]
    },
    {
        skill_id: "LANG_PRON_BASIC_01",
        name_kr: "기초 영어 발음 명료도",
        name_en: "Basic English Pronunciation Clarity",
        category: "language",
        mode: "expressive",
        age_band: "7-9",
        unit: "score_0_100",
        is_core_metric: false,
        emoji: "🗣️",
        description: "영어 단어/짧은 문장을 말했을 때 의미 파악이 가능한 수준으로 발음하는 능력",
        can_do_examples: [
            "기초 단어(cat, dog, pizza 등)를 발음했을 때, 올바른 단어로 인식된다",
            "문장 전체가 아닌 일부 소리만 약간 흐려져도, 전체 의미 이해에는 큰 장애가 없다"
        ]
    },
    {
        skill_id: "LANG_SENT_BASIC_SVO_01",
        name_kr: "기초 SVO 문장 구성",
        name_en: "Basic SVO Sentence",
        category: "language",
        mode: "expressive",
        age_band: "7-9",
        unit: "score_0_100",
        is_core_metric: true,
        emoji: "✍️",
        description: "'My name is ~.', 'I am ~.', 'I like ~.'처럼 간단한 주어-동사-목적어 패턴으로 된 문장을 완성하거나 말할 수 있는 능력",
        can_do_examples: [
            "'My name is [Name].'을 한 세션에서 1회 이상 스스로 말할 수 있다",
            "'I like ___.' 문장을 완전하거나 부분적으로 말할 수 있다",
            "단어만 말해도 의미를 의사소통 할 수 있다"
        ]
    },
    {
        skill_id: "LANG_WH_ANSWER_SIMPLE_01",
        name_kr: "기초 WH-질문 응답",
        name_en: "Simple WH-question Answer",
        category: "language",
        mode: "expressive",
        age_band: "7-9",
        unit: "score_0_100",
        is_core_metric: true,
        emoji: "❓",
        description: "'What do you like?', 'Who do you live with?' 등 간단한 WH-질문에 대해 최소한 단어 한 개 수준으로나마 의미 있는 응답을 할 수 있는 능력",
        can_do_examples: [
            "'What do you like?' → 'cat / pizza / drawing' 등 한 단어로 대답할 수 있다",
            "질문을 한국어로 다시 들은 뒤, 영어 단어나 혼합어로 대답하려고 한다"
        ]
    }
];

// Cognitive Skills
export const cognitiveSkills: Skill[] = [
    {
        skill_id: "COGN_ATTENTION_SESSION_01",
        name_kr: "세션 내 지속 주의 집중",
        name_en: "Sustained Attention within Session",
        category: "cognitive",
        mode: "receptive",
        age_band: "7-9",
        unit: "level_1_5",
        is_core_metric: true,
        emoji: "🎯",
        description: "약 10~15분 길이의 세션 동안, 과제 수행 및 대화에 지속적으로 참여하는 능력",
        can_do_examples: [
            "세션 중 최소 3~4개의 과제에 응답한다",
            "세션 끝까지 이탈하지 않고 함께한다"
        ]
    },
    {
        skill_id: "COGN_WORKINGMEM_2STEP_01",
        name_kr: "두 단계 지시 따르기",
        name_en: "Following 2-step Instructions",
        category: "cognitive",
        mode: "receptive",
        age_band: "7-9",
        unit: "level_1_5",
        is_core_metric: false,
        emoji: "🧩",
        description: "'먼저 ~~ 하고, 그다음에 ~~ 해줘.' 형태의 2단계 지시를 이해하고 수행하는 능력",
        can_do_examples: [
            "먼저 좋아하는 동물을 말하고, 그다음에 좋아하는 음식을 말해줘.' 요청에 대해 두 항목 모두를 순서대로 말할 수 있다",
            "한 번에 기억하기 힘들어도, 다시 상기시켰을 때 수행을 마무리할 수 있다"
        ]
    },
    {
        skill_id: "COGN_FLEXIBILITY_TOPIC_01",
        name_kr: "주제 전환 유연성",
        name_en: "Topic-switching Flexibility",
        category: "cognitive",
        mode: "both",
        age_band: "7-9",
        unit: "level_1_5",
        is_core_metric: false,
        emoji: "🔄",
        description: "한 주제에서 다른 주제로 대화가 넘어갈 때, 과도한 저항 없이 새로운 질문에 응답하려는 유연성",
        can_do_examples: [
            "동물 이야기에서 음식 이야기로 넘어갈 때, 새로운 질문에 대해 최소한 한 단어 수준의 응답을 시도한다",
            "주제 전환에 대해 '그만할래요' 신호가 반복적으로 나타나지 않는다"
        ]
    }
];

// Emotional & Social Skills
export const emotionalSkills: Skill[] = [
    {
        skill_id: "EMO_SELFREPORT_3POINT_01",
        name_kr: "3단계 기분 자기 보고",
        name_en: "3-point Mood Self-report",
        category: "emotional",
        mode: "expressive",
        age_band: "7-9",
        unit: "level_1_5",
        is_core_metric: true,
        emoji: "😊",
        description: "'1: 피곤, 2: 보통, 3: 신남'과 같은 간단한 척도 중에서 자신의 현재 기분을 선택·표현하는 능력",
        can_do_examples: [
            "1/2/3 중 하나를 선택해 말하거나 손가락/버튼으로 고를 수 있다",
            "여러 세션을 거치며, 기분 변화가 있을 때 다른 값을 선택하는 모습이 관찰된다"
        ]
    },
    {
        skill_id: "EMO_RESPONSE_PRAISE_01",
        name_kr: "칭찬/격려에 대한 정서적 반응",
        name_en: "Emotional Response to Praise",
        category: "emotional",
        mode: "receptive",
        age_band: "7-9",
        unit: "level_1_5",
        is_core_metric: false,
        emoji: "🌟",
        description: "'잘했어!', '굉장히 용감했어.'와 같은 칭찬/격려 메시지를 들었을 때, 표정/목소리/행동으로 긍정적인 반응을 보이는 정도",
        can_do_examples: [
            "칭찬 이후, 목소리 톤이 밝아지거나 추가 시도를 하려는 모습이 늘어난다",
            "'또 해볼래요.', '한 번 더요.' 등 긍정적인 반응을 보일 수 있다"
        ]
    },
    {
        skill_id: "EMO_EXPRESS_PREFERENCE_01",
        name_kr: "선호/비선호 정서 표현",
        name_en: "Emotional Valence in Preferences",
        category: "emotional",
        mode: "expressive",
        age_band: "7-9",
        unit: "score_0_100",
        is_core_metric: true,
        emoji: "💝",
        description: "'좋아해요 / 싫어해요'와 같은 정서적 태도를 언어·표정·제스처로 표현하는 능력",
        can_do_examples: [
            "좋아하는 것에 대해 이야기할 때 목소리와 표정이 밝아지며, '좋아요', '재밌어요' 등의 표현을 사용할 수 있다",
            "조금 무섭거나 싫어하는 대상에 대해 '무서워요', '싫어요' 등을 말해볼 수 있다"
        ]
    }
];

// Combined all skills
export const allSkills: Skill[] = [
    ...languageSkills,
    ...cognitiveSkills,
    ...emotionalSkills
];

// Get skill by ID
export function getSkillById(skillId: string): Skill | undefined {
    return allSkills.find(skill => skill.skill_id === skillId);
}

// Get skills by category
export function getSkillsByCategory(category: SkillCategory): Skill[] {
    return allSkills.filter(skill => skill.category === category);
}

// Get core metric skills
export function getCoreMetricSkills(): Skill[] {
    return allSkills.filter(skill => skill.is_core_metric);
}

// Calculate skill level from score (0-100 to 1-5)
export function calculateSkillLevel(score: number): number {
    if (score < 20) return 1;
    if (score < 40) return 2;
    if (score < 60) return 3;
    if (score < 80) return 4;
    return 5;
}

// Get level description
export function getSkillLevelDescription(level: number): string {
    const descriptions = [
        "시작 단계",
        "기초 단계",
        "발전 단계",
        "숙달 단계",
        "완성 단계"
    ];
    return descriptions[level - 1] || "시작 단계";
}

// Get category color
export function getCategoryColor(category: SkillCategory): string {
    switch (category) {
        case "language":
            return "bg-blue-100 text-blue-700";
        case "cognitive":
            return "bg-purple-100 text-purple-700";
        case "emotional":
            return "bg-pink-100 text-pink-700";
        default:
            return "bg-gray-100 text-gray-700";
    }
}

// Get category name in Korean
export function getCategoryNameKr(category: SkillCategory): string {
    switch (category) {
        case "language":
            return "언어";
        case "cognitive":
            return "인지";
        case "emotional":
            return "정서/사회";
        default:
            return "기타";
    }
}
