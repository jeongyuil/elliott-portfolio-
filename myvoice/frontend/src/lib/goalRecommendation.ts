/**
 * Goal Recommendation System
 * Analyzes historical learning data to recommend weekly goals
 */

export interface HistoricalWeek {
    week: number;
    xp: number;
    missions: number;
    studyTime: number;
    words: number;
    date?: string; // Added date for chart compatibility
}

export interface RecommendedGoals {
    xp: number;
    missions: number;
    studyTime: number;
    words: number;
    reasoning: {
        xp: string;
        missions: string;
        studyTime: string;
        words: string;
    };
}

/**
 * Calculate recommended goals based on historical data
 * Strategy:
 * 1. Calculate average of past performance
 * 2. Identify trend (improving, stable, declining)
 * 3. Set goal 10-15% above recent average for growth
 * 4. Cap at reasonable limits to avoid burnout
 */
export function recommendWeeklyGoals(historicalData: HistoricalWeek[]): RecommendedGoals {
    if (historicalData.length === 0) {
        // Default goals for new users
        return {
            xp: 1000,
            missions: 15,
            studyTime: 10,
            words: 120,
            reasoning: {
                xp: "새로운 학습자를 위한 기본 목표입니다",
                missions: "새로운 학습자를 위한 기본 목표입니다",
                studyTime: "새로운 학습자를 위한 기본 목표입니다",
                words: "새로운 학습자를 위한 기본 목표입니다",
            },
        };
    }

    // Calculate averages
    /* eslint-disable @typescript-eslint/no-unused-vars */
    // Calculate averages (unused for now but good for reference)
    // const avgXp = Math.round(historicalData.reduce((sum, w) => sum + w.xp, 0) / historicalData.length);
    // const avgMissions = Math.round(historicalData.reduce((sum, w) => sum + w.missions, 0) / historicalData.length);
    // const avgStudyTime = parseFloat((historicalData.reduce((sum, w) => sum + w.studyTime, 0) / historicalData.length).toFixed(1));
    // const avgWords = Math.round(historicalData.reduce((sum, w) => sum + w.words, 0) / historicalData.length);
    /* eslint-enable @typescript-eslint/no-unused-vars */

    // Get recent performance (last 2 weeks)
    const recentData = historicalData.slice(-2);
    const recentAvgXp = Math.round(recentData.reduce((sum, w) => sum + w.xp, 0) / recentData.length);
    const recentAvgMissions = Math.round(recentData.reduce((sum, w) => sum + w.missions, 0) / recentData.length);
    const recentAvgStudyTime = parseFloat((recentData.reduce((sum, w) => sum + w.studyTime, 0) / recentData.length).toFixed(1));
    const recentAvgWords = Math.round(recentData.reduce((sum, w) => sum + w.words, 0) / recentData.length);

    // Detect trend
    const isImproving = (metric: keyof Omit<HistoricalWeek, 'week' | 'date'>) => {
        if (historicalData.length < 2) return false;
        const recent = historicalData[historicalData.length - 1][metric];
        const previous = historicalData[historicalData.length - 2][metric];
        return recent > previous;
    };

    // Calculate growth factor based on trend
    const getGrowthFactor = (metric: keyof Omit<HistoricalWeek, 'week' | 'date'>) => {
        if (isImproving(metric)) {
            return 1.15; // 15% increase for improving trend
        } else {
            return 1.10; // 10% increase for stable/declining trend (gentler push)
        }
    };

    // Calculate recommended goals
    const recommendedXp = Math.min(
        Math.round(recentAvgXp * getGrowthFactor('xp')),
        2500 // Cap at reasonable limit
    );

    const recommendedMissions = Math.min(
        Math.round(recentAvgMissions * getGrowthFactor('missions')),
        35 // Cap at reasonable limit
    );

    const recommendedStudyTime = Math.min(
        parseFloat((recentAvgStudyTime * getGrowthFactor('studyTime')).toFixed(1)),
        25 // Cap at reasonable limit (hours per week)
    );

    const recommendedWords = Math.min(
        Math.round(recentAvgWords * getGrowthFactor('words')),
        300 // Cap at reasonable limit
    );

    // Generate reasoning
    const reasoning = {
        xp: isImproving('xp')
            ? `최근 XP 획득이 증가 추세입니다! 지난 주 평균(${recentAvgXp}XP)보다 15% 높은 목표를 추천합니다.`
            : `지난 주 평균(${recentAvgXp}XP)을 기준으로 10% 성장 목표를 설정했습니다.`,
        missions: isImproving('missions')
            ? `미션 완료가 꾸준히 늘고 있어요! 지난 주 평균(${recentAvgMissions}개)보다 15% 높은 목표를 추천합니다.`
            : `지난 주 평균(${recentAvgMissions}개)을 기준으로 10% 성장 목표를 설정했습니다.`,
        studyTime: isImproving('studyTime')
            ? `학습 시간이 증가 중입니다! 지난 주 평균(${recentAvgStudyTime}시간)보다 15% 높은 목표를 추천합니다.`
            : `지난 주 평균(${recentAvgStudyTime}시간)을 기준으로 10% 성장 목표를 설정했습니다.`,
        words: isImproving('words')
            ? `어휘 학습이 활발합니다! 지난 주 평균(${recentAvgWords}개)보다 15% 높은 목표를 추천합니다.`
            : `지난 주 평균(${recentAvgWords}개)을 기준으로 10% 성장 목표를 설정했습니다.`,
    };

    return {
        xp: recommendedXp,
        missions: recommendedMissions,
        studyTime: recommendedStudyTime,
        words: recommendedWords,
        reasoning,
    };
}

/**
 * Validate if user-set goal is within reasonable range
 * Returns warning message if goal is too high or too low
 */
export function validateGoal(
    goalType: 'xp' | 'missions' | 'studyTime' | 'words',
    value: number,
    historicalData: HistoricalWeek[]
): { valid: boolean; message?: string } {
    if (historicalData.length === 0) {
        return { valid: true };
    }

    // Calculate recent average for validation reference
    const recentAvg = historicalData.slice(-2).reduce((sum, w) => sum + (w[goalType] as number), 0) / Math.min(historicalData.length, 2);

    const limits = {
        xp: { min: 500, max: 3000, minRatio: 0.5, maxRatio: 2.5 },
        missions: { min: 5, max: 40, minRatio: 0.5, maxRatio: 2.5 },
        studyTime: { min: 3, max: 30, minRatio: 0.5, maxRatio: 2.5 },
        words: { min: 50, max: 400, minRatio: 0.5, maxRatio: 2.5 },
    };

    const limit = limits[goalType];

    // Check absolute limits
    if (value < limit.min) {
        return {
            valid: false,
            message: `목표가 너무 낮습니다. 최소 ${limit.min} 이상을 추천합니다.`,
        };
    }

    if (value > limit.max) {
        return {
            valid: false,
            message: `목표가 너무 높습니다. 최대 ${limit.max} 이하를 추천합니다.`,
        };
    }

    // Check relative to recent performance
    if (value < recentAvg * limit.minRatio) {
        return {
            valid: false,
            message: `최근 평균(${Math.round(recentAvg)})보다 너무 낮습니다. 조금 더 도전해보세요!`,
        };
    }

    if (value > recentAvg * limit.maxRatio) {
        return {
            valid: false,
            message: `최근 평균(${Math.round(recentAvg)})보다 너무 높습니다. 무리하지 마세요!`,
        };
    }

    return { valid: true };
}
