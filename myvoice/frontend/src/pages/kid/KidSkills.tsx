/**
 * Skills Page
 * Detailed skills analysis and goal setting
 */

import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { ChevronLeft, TrendingUp, Users, Target, Edit3, Activity } from "lucide-react";
import {
    LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from "recharts";
import { allSkills, type SkillCategory } from "@/lib/skillsData";
import SkillProgress from "@/components/SkillProgress";
import { learningProgressData, peerComparisonData, weeklyGoals, historicalLearningData } from "@/lib/mockData";
import { recommendWeeklyGoals, validateGoal } from "@/lib/goalRecommendation";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { getKidSkills } from "@/api/client";

// Mock Data for Radar Chart (will need endpoint for this later)
const radarData = [
    { subject: '어휘', A: 80, fullMark: 100 },
    { subject: '표현', A: 65, fullMark: 100 },
    { subject: '발음', A: 90, fullMark: 100 },
    { subject: '유창성', A: 70, fullMark: 100 },
    { subject: '자신감', A: 85, fullMark: 100 },
    { subject: '미션', A: 60, fullMark: 100 },
];

export default function KidSkills() {
    const [userSkills, setUserSkills] = useState<Record<string, number>>({});
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function fetchSkills() {
            try {
                const response = await getKidSkills();
                const skillMap: Record<string, number> = {};
                response.items.forEach(item => {
                    // Use raw score if available (0-100), otherwise map level 1-5 to something?
                    // Frontend skill unit logic:
                    // if unit == score_0_100 (e.g. vocab): use rawScore or 0.
                    // if unit == level_1_5 (e.g. attention): use level.

                    // Actually, let's look at how mockUserSkillProgress was used.
                    // It had values like 65, 4, etc.

                    // Ideally we should look up the skill definition to know if we should use level or rawScore.
                    // But for simplicity, let's prefer rawScore if > 5 (likely a score), else level?
                    // Better: use rawScore if not null, else level.
                    skillMap[item.skillId] = item.rawScore ?? item.level;
                });
                setUserSkills(skillMap);
            } catch (err) {
                console.error("Failed to fetch skills", err);
            } finally {
                setIsLoading(false);
            }
        }
        fetchSkills();
    }, []);

    const [selectedCategory, setSelectedCategory] = useState<SkillCategory | "all">("all");
    const [chartPeriod, setChartPeriod] = useState<"week" | "month">("week");
    const [isGoalModalOpen, setIsGoalModalOpen] = useState(false);
    const [goalValues, setGoalValues] = useState({
        xp: weeklyGoals.xp.target,
        missions: weeklyGoals.missions.target,
        studyTime: weeklyGoals.studyTime.target,
        words: weeklyGoals.words.target,
    });
    const [showRecommendation, setShowRecommendation] = useState(false);
    const [validationMessages, setValidationMessages] = useState<Record<string, string>>({});

    // Get recommended goals
    const recommendedGoals = recommendWeeklyGoals(historicalLearningData);

    const categories: Array<{ value: SkillCategory | "all"; label: string; emoji: string }> = [
        { value: "all", label: "전체", emoji: "📊" },
        { value: "language", label: "언어", emoji: "📚" },
        { value: "cognitive", label: "인지", emoji: "🧠" },
        { value: "emotional", label: "정서", emoji: "💝" },
    ];

    const filteredSkills = selectedCategory === "all"
        ? allSkills
        : allSkills.filter(skill => skill.category === selectedCategory);

    // Calculate overall progress
    const totalSkills = allSkills.length;

    // Correct calculation for completed skills
    const actualCompletedSkills = allSkills.filter(skill => {
        const val = userSkills[skill.skill_id];
        if (val === undefined) return false;
        if (skill.unit === "score_0_100") return val >= 80;
        return val >= 4;
    }).length;


    // Weekly goals data
    const goals = [
        {
            id: "xp",
            emoji: "⚡",
            label: "획득 XP",
            current: weeklyGoals.xp.current,
            target: weeklyGoals.xp.target,
            unit: "XP",
            color: "var(--bt-accent)"
        },
        {
            id: "missions",
            emoji: "🎯",
            label: "완료 모험",
            current: weeklyGoals.missions.current,
            target: weeklyGoals.missions.target,
            unit: "개",
            color: "var(--bt-primary)"
        },
        {
            id: "studyTime",
            emoji: "⏰",
            label: "학습 시간",
            current: weeklyGoals.studyTime.current,
            target: weeklyGoals.studyTime.target,
            unit: "시간",
            color: "var(--bt-accent)"
        },
        {
            id: "words",
            emoji: "📚",
            label: "학습 단어",
            current: weeklyGoals.words.current,
            target: weeklyGoals.words.target,
            unit: "개",
            color: "#9333ea"
        },
    ];

    return (
        <div className="h-full flex flex-col bg-[var(--bt-bg)] overflow-hidden">
            {/* Top Section with Back Button */}
            <div className="p-4 bg-white shadow-sm flex-none">
                <div className="flex items-center gap-3">
                    <Link to="/kid/home">
                        <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                            <ChevronLeft className="w-5 h-5 text-gray-600" />
                        </button>
                    </Link>
                    <div>
                        <h1 className="text-xl font-bold text-[var(--bt-text)]">나의 스킬</h1>
                        <p className="text-xs text-[var(--bt-text-secondary)]">학습 진행 상황을 확인하세요</p>
                    </div>
                </div>
            </div>

            {/* Scrollable Content */}
            <div className="flex-1 overflow-y-auto p-4 pb-24">

                {/* Radar Chart Section (New) */}
                <div className="bt-card p-4 mb-4 bg-gradient-to-br from-indigo-50 to-purple-50">
                    <h2 className="text-base font-bold text-[var(--bt-text)] mb-3 flex items-center gap-2">
                        <Activity size={18} className="text-[var(--bt-accent)]" />
                        스킬 분석 (Radar)
                    </h2>
                    <div className="h-[250px] w-full relative">
                        <ResponsiveContainer width="100%" height="100%">
                            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                                <PolarGrid stroke="#e5e7eb" />
                                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 12, fill: '#4b5563' }} />
                                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                                <Radar
                                    name="My Skills"
                                    dataKey="A"
                                    stroke="var(--bt-accent)"
                                    fill="var(--bt-accent)"
                                    fillOpacity={0.4}
                                />
                            </RadarChart>
                        </ResponsiveContainer>
                        <div className="absolute top-2 right-2 p-2 bg-white/80 rounded-lg shadow-sm text-xs">
                            <span className="font-bold text-[var(--bt-accent)]">종합 점수: 75점</span>
                        </div>
                    </div>
                </div>

                {/* Weekly Goals Section */}
                <div className="bt-card p-4 mb-4">
                    <div className="flex items-center justify-between mb-3">
                        <h2 className="text-base font-bold text-[var(--bt-text)] flex items-center gap-2">
                            <Target size={18} className="text-[var(--bt-accent)]" />
                            이번 주 목표
                        </h2>
                        <Dialog open={isGoalModalOpen} onOpenChange={setIsGoalModalOpen}>
                            <DialogTrigger asChild>
                                <button className="flex items-center gap-1 text-xs font-semibold text-[var(--bt-accent)] hover:underline">
                                    <Edit3 size={14} />
                                    목표 수정
                                </button>
                            </DialogTrigger>
                            <DialogContent className="max-w-sm max-h-[80vh] overflow-y-auto">
                                <DialogHeader>
                                    <DialogTitle>주간 목표 설정</DialogTitle>
                                </DialogHeader>
                                <div className="space-y-4 py-4">
                                    {/* Recommendation Banner */}
                                    <div className="p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border-2 border-blue-200">
                                        <div className="flex items-center justify-between mb-2">
                                            <p className="text-sm font-bold text-[var(--bt-text)] flex items-center gap-1">
                                                🎯 AI 추천 목표
                                            </p>
                                            <button
                                                onClick={() => setShowRecommendation(!showRecommendation)}
                                                className="text-xs font-semibold text-[var(--bt-accent)] hover:underline"
                                            >
                                                {showRecommendation ? "숨기기" : "자세히 보기"}
                                            </button>
                                        </div>
                                        <p className="text-xs text-gray-600 mb-2">
                                            과거 학습 기록을 분석하여 최적의 목표를 추천합니다
                                        </p>
                                        {showRecommendation && (
                                            <div className="space-y-2 mt-3 pt-3 border-t border-blue-200">
                                                {goals.map((goal) => {
                                                    const goalKey = goal.id as 'xp' | 'missions' | 'studyTime' | 'words';
                                                    const recommendedValue = typeof recommendedGoals[goalKey] === 'number' ? recommendedGoals[goalKey] : 0;
                                                    const reasoning = recommendedGoals.reasoning[goalKey];
                                                    return (
                                                        <div key={goal.id} className="text-xs">
                                                            <p className="font-semibold text-[var(--bt-text)]">
                                                                {goal.emoji} {goal.label}: <span className="text-[var(--bt-accent)]">{recommendedValue}{goal.unit}</span>
                                                            </p>
                                                            <p className="text-gray-600 mt-1">{reasoning}</p>
                                                        </div>
                                                    );
                                                })}
                                                <button
                                                    onClick={() => {
                                                        setGoalValues({
                                                            xp: recommendedGoals.xp,
                                                            missions: recommendedGoals.missions,
                                                            studyTime: recommendedGoals.studyTime,
                                                            words: recommendedGoals.words,
                                                        });
                                                        setValidationMessages({});
                                                    }}
                                                    className="w-full mt-2 px-3 py-2 bg-[var(--bt-accent)] text-white text-xs font-bold rounded-lg hover:bg-blue-600 transition-colors"
                                                >
                                                    ✨ 추천 목표 적용하기
                                                </button>
                                            </div>
                                        )}
                                    </div>

                                    {/* Goal Input Fields */}
                                    {goals.map((goal) => {
                                        const goalKey = goal.id as keyof typeof goalValues;
                                        return (
                                            <div key={goal.id} className="space-y-2">
                                                <label className="text-sm font-semibold text-[var(--bt-text)] flex items-center gap-2">
                                                    <span>{goal.emoji}</span>
                                                    {goal.label}
                                                </label>
                                                <div className="flex items-center gap-2">
                                                    <input
                                                        type="number"
                                                        value={goalValues[goalKey]}
                                                        onChange={(e) => {
                                                            const value = parseFloat(e.target.value) || 0;
                                                            setGoalValues({ ...goalValues, [goalKey]: value });

                                                            // Validate on change
                                                            const validation = validateGoal(goalKey, value, historicalLearningData);
                                                            if (!validation.valid && validation.message) {
                                                                setValidationMessages({ ...validationMessages, [goalKey]: validation.message });
                                                            } else {
                                                                const newMessages = { ...validationMessages };
                                                                delete newMessages[goalKey];
                                                                setValidationMessages(newMessages);
                                                            }
                                                        }}
                                                        className="flex-1 px-3 py-2 border-2 border-gray-200 rounded-lg focus:border-[var(--bt-accent)] focus:outline-none"
                                                    />
                                                    <span className="text-sm text-gray-500">{goal.unit}</span>
                                                </div>
                                                {validationMessages[goalKey] && (
                                                    <p className="text-xs text-orange-600 flex items-center gap-1">
                                                        ⚠️ {validationMessages[goalKey]}
                                                    </p>
                                                )}
                                            </div>
                                        );
                                    })}
                                    <Button
                                        onClick={() => {
                                            // Save goals (in real app, save to LocalStorage)
                                            setIsGoalModalOpen(false);
                                        }}
                                        className="w-full bg-[var(--bt-primary)] hover:bg-green-500 text-white font-bold"
                                    >
                                        저장하기
                                    </Button>
                                </div>
                            </DialogContent>
                        </Dialog>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                        {goals.map((goal) => {
                            const progress = Math.round((goal.current / goal.target) * 100);
                            const isCompleted = progress >= 100;

                            return (
                                <div key={goal.id} className="p-3 bg-gradient-to-br from-gray-50 to-white rounded-xl border-2 border-gray-100">
                                    <div className="flex items-center gap-2 mb-2">
                                        <span className="text-xl">{goal.emoji}</span>
                                        <p className="text-xs font-semibold text-[var(--bt-text)]">{goal.label}</p>
                                    </div>
                                    <div className="mb-2">
                                        <div className="flex items-baseline gap-1">
                                            <span className="text-lg font-bold" style={{ color: goal.color }}>
                                                {goal.current}
                                            </span>
                                            <span className="text-xs text-gray-500">/ {goal.target}{goal.unit}</span>
                                        </div>
                                    </div>
                                    <div className="bt-progress h-1.5">
                                        <div
                                            className="bt-progress-bar transition-all duration-500"
                                            style={{
                                                width: `${Math.min(progress, 100)}%`,
                                                backgroundColor: goal.color
                                            }}
                                        />
                                    </div>
                                    {isCompleted && (
                                        <p className="text-[10px] text-green-600 font-bold mt-1">✓ 목표 달성!</p>
                                    )}
                                    {!isCompleted && (
                                        <p className="text-[10px] text-gray-500 mt-1">{progress}% 달성</p>
                                    )}
                                </div>
                            );
                        })}
                    </div>

                    {/* Overall Progress - Integrated */}
                    <div className="mt-4 pt-4 border-t-2 border-gray-100">
                        <div className="p-3 bg-gradient-to-r from-[var(--bt-primary)] to-green-400 text-white rounded-xl">
                            <div className="flex items-center justify-between mb-2">
                                <div>
                                    <p className="text-xs opacity-90">전체 진행률</p>
                                    <p className="text-2xl font-bold">{Math.round((actualCompletedSkills / totalSkills) * 100)}%</p>
                                </div>
                                <div className="text-right">
                                    <p className="text-xs opacity-90">완료한 스킬</p>
                                    <p className="text-xl font-bold">{actualCompletedSkills} / {totalSkills}</p>
                                </div>
                            </div>
                            <div className="h-2 bg-white/30 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-white transition-all duration-500"
                                    style={{ width: `${(actualCompletedSkills / totalSkills) * 100}%` }}
                                />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Learning Progress Chart */}
                <div className="bt-card p-4 mb-4">
                    <div className="flex items-center justify-between mb-3">
                        <h2 className="text-base font-bold text-[var(--bt-text)] flex items-center gap-2">
                            <TrendingUp size={18} className="text-[var(--bt-accent)]" />
                            학습 진행 상황
                        </h2>
                        <div className="flex gap-1">
                            <button
                                onClick={() => setChartPeriod("week")}
                                className={`px-3 py-1 text-xs font-semibold rounded-full transition-all ${chartPeriod === "week"
                                    ? "bg-[var(--bt-accent)] text-white"
                                    : "bg-gray-100 text-gray-600"
                                    }`}
                            >
                                주간
                            </button>
                            <button
                                onClick={() => setChartPeriod("month")}
                                className={`px-3 py-1 text-xs font-semibold rounded-full transition-all ${chartPeriod === "month"
                                    ? "bg-[var(--bt-accent)] text-white"
                                    : "bg-gray-100 text-gray-600"
                                    }`}
                            >
                                월간
                            </button>
                        </div>
                    </div>
                    <div className="h-[200px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={learningProgressData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                <XAxis
                                    dataKey="date"
                                    tick={{ fontSize: 11 }}
                                    stroke="#999"
                                />
                                <YAxis
                                    tick={{ fontSize: 11 }}
                                    stroke="#999"
                                />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: 'white',
                                        border: '2px solid var(--bt-border)',
                                        borderRadius: '12px',
                                        fontSize: '12px'
                                    }}
                                />
                                <Legend
                                    wrapperStyle={{ fontSize: '11px' }}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="xp"
                                    stroke="var(--bt-accent)"
                                    strokeWidth={2}
                                    name="획득 XP"
                                    dot={{ fill: 'var(--bt-accent)', r: 4 }}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="words"
                                    stroke="var(--bt-primary)"
                                    strokeWidth={2}
                                    name="학습 단어"
                                    dot={{ fill: 'var(--bt-primary)', r: 4 }}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Peer Comparison Chart */}
                <div className="bt-card p-4 mb-4">
                    <h2 className="text-base font-bold text-[var(--bt-text)] mb-3 flex items-center gap-2">
                        <Users size={18} className="text-[var(--bt-accent)]" />
                        또래 평균 비교
                    </h2>
                    <div className="h-[250px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={peerComparisonData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                <XAxis
                                    dataKey="category"
                                    tick={{ fontSize: 10 }}
                                    stroke="#999"
                                />
                                <YAxis
                                    tick={{ fontSize: 11 }}
                                    stroke="#999"
                                />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: 'white',
                                        border: '2px solid var(--bt-border)',
                                        borderRadius: '12px',
                                        fontSize: '12px'
                                    }}
                                    formatter={((value: number, name: string, props: any) => {
                                        return [`${value}${props.payload.unit || ''}`, name];
                                    }) as any}
                                />
                                <Legend
                                    wrapperStyle={{ fontSize: '11px' }}
                                />
                                <Bar
                                    dataKey="myValue"
                                    fill="var(--bt-primary)"
                                    name="나의 기록"
                                    radius={[4, 4, 0, 0]}
                                />
                                <Bar
                                    dataKey="peerAverage"
                                    fill="#e0e0e0"
                                    name="또래 평균"
                                    radius={[4, 4, 0, 0]}
                                />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="mt-3 p-3 bg-green-50 rounded-lg">
                        <p className="text-xs text-green-700 font-semibold">
                            🎉 축하해요! 또래 평균보다 24% 더 열심히 학습하고 있어요!
                        </p>
                    </div>
                </div>

                {/* Category Filter */}
                <div className="flex gap-2 mb-4 overflow-x-auto pb-2 scrollbar-hide">
                    {categories.map((cat) => (
                        <button
                            key={cat.value}
                            onClick={() => setSelectedCategory(cat.value)}
                            className={`px-4 py-2 rounded-full font-semibold whitespace-nowrap transition-all text-sm ${selectedCategory === cat.value
                                ? "bg-[var(--bt-primary)] text-white shadow-lg scale-105"
                                : "bg-white text-gray-600 hover:bg-gray-100 bt-card"
                                }`}
                        >
                            {cat.emoji} {cat.label}
                        </button>
                    ))}
                </div>

                {/* Skills List */}
                <div className="space-y-3">
                    {isLoading ? (
                        <div className="text-center py-12">
                            <p className="text-gray-500">스킬 정보를 불러오는 중...</p>
                        </div>
                    ) : filteredSkills.length === 0 ? (
                        <div className="text-center py-12">
                            <p className="text-gray-500">스킬이 없습니다</p>
                        </div>
                    ) : (
                        filteredSkills.map((skill) => (
                            <SkillProgress
                                key={skill.skill_id}
                                skill={skill}
                                currentValue={userSkills[skill.skill_id] || 0}
                                showDetails={true}
                            />
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}
