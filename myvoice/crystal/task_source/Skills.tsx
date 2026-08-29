import { useState } from "react";
import { Link } from "wouter";
import { ChevronLeft, TrendingUp, Users, Target, Edit3 } from "lucide-react";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { allSkills, SkillCategory } from "@/lib/skillsData";
import SkillProgress from "@/components/skills/SkillProgress";
import { learningProgressData, peerComparisonData, weeklyGoals, historicalLearningData } from "@/lib/mockData";
import { recommendWeeklyGoals, validateGoal } from "@/lib/goalRecommendation";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

// Mock user skill progress - in a real app, this would come from LocalStorage or backend
const mockUserSkillProgress = {
  "LANG_VOCAB_DAILY_01": 65,
  "LANG_VOCAB_PREFERENCE_01": 45,
  "LANG_PRON_BASIC_01": 70,
  "LANG_SENT_BASIC_SVO_01": 50,
  "LANG_WH_ANSWER_SIMPLE_01": 40,
  "COGN_ATTENTION_SESSION_01": 4,
  "COGN_WORKINGMEM_2STEP_01": 3,
  "COGN_FLEXIBILITY_TOPIC_01": 3,
  "EMO_SELFREPORT_3POINT_01": 4,
  "EMO_RESPONSE_PRAISE_01": 5,
  "EMO_EXPRESS_PREFERENCE_01": 55,
};

export default function Skills() {
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
  const completedSkills = Object.values(mockUserSkillProgress).filter(
    (value, index) => {
      const skill = allSkills[index];
      if (skill.unit === "score_0_100") {
        return value >= 80;
      } else {
        return value >= 4;
      }
    }
  ).length;

  // Weekly goals data
  const goals = [
    { 
      id: "xp", 
      emoji: "⚡", 
      label: "획득 XP", 
      current: weeklyGoals.xp.current, 
      target: weeklyGoals.xp.target,
      unit: "XP",
      color: "var(--duo-blue)"
    },
    { 
      id: "missions", 
      emoji: "🎯", 
      label: "완료 미션", 
      current: weeklyGoals.missions.current, 
      target: weeklyGoals.missions.target,
      unit: "개",
      color: "var(--duo-green)"
    },
    { 
      id: "studyTime", 
      emoji: "⏰", 
      label: "학습 시간", 
      current: weeklyGoals.studyTime.current, 
      target: weeklyGoals.studyTime.target,
      unit: "시간",
      color: "var(--duo-yellow)"
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
    <div className="h-screen flex flex-col bg-[var(--duo-bg)] overflow-hidden">
      {/* Top Section with Back Button */}
      <div className="p-4 bg-white shadow-sm">
        <div className="flex items-center gap-3">
          <Link href="/profile">
            <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
              <ChevronLeft className="w-5 h-5 text-gray-600" />
            </button>
          </Link>
          <div>
            <h1 className="text-xl font-bold text-[var(--duo-text)]">나의 스킬</h1>
            <p className="text-xs text-[var(--duo-text-secondary)]">학습 진행 상황을 확인하세요</p>
          </div>
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto p-4 pb-20">
        {/* Weekly Goals Section */}
        <div className="duo-card p-4 mb-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-base font-bold text-[var(--duo-text)] flex items-center gap-2">
              <Target size={18} className="text-[var(--duo-yellow)]" />
              이번 주 목표
            </h2>
            <Dialog open={isGoalModalOpen} onOpenChange={setIsGoalModalOpen}>
              <DialogTrigger asChild>
                <button className="flex items-center gap-1 text-xs font-semibold text-[var(--duo-blue)] hover:underline">
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
                      <p className="text-sm font-bold text-[var(--duo-text)] flex items-center gap-1">
                        🎯 AI 추천 목표
                      </p>
                      <button
                        onClick={() => setShowRecommendation(!showRecommendation)}
                        className="text-xs font-semibold text-[var(--duo-blue)] hover:underline"
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
                              <p className="font-semibold text-[var(--duo-text)]">
                                {goal.emoji} {goal.label}: <span className="text-[var(--duo-blue)]">{recommendedValue}{goal.unit}</span>
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
                          className="w-full mt-2 px-3 py-2 bg-[var(--duo-blue)] text-white text-xs font-bold rounded-lg hover:bg-blue-600 transition-colors"
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
                        <label className="text-sm font-semibold text-[var(--duo-text)] flex items-center gap-2">
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
                            className="flex-1 px-3 py-2 border-2 border-gray-200 rounded-lg focus:border-[var(--duo-blue)] focus:outline-none"
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
                    className="w-full bg-[var(--duo-green)] hover:bg-green-500 text-white font-bold"
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
                    <p className="text-xs font-semibold text-[var(--duo-text)]">{goal.label}</p>
                  </div>
                  <div className="mb-2">
                    <div className="flex items-baseline gap-1">
                      <span className="text-lg font-bold" style={{ color: goal.color }}>
                        {goal.current}
                      </span>
                      <span className="text-xs text-gray-500">/ {goal.target}{goal.unit}</span>
                    </div>
                  </div>
                  <div className="duo-progress h-1.5">
                    <div 
                      className="duo-progress-bar transition-all duration-500" 
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
            <div className="p-3 bg-gradient-to-r from-[var(--duo-green)] to-green-400 text-white rounded-xl">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <p className="text-xs opacity-90">전체 진행률</p>
                  <p className="text-2xl font-bold">{Math.round((completedSkills / totalSkills) * 100)}%</p>
                </div>
                <div className="text-right">
                  <p className="text-xs opacity-90">완료한 스킬</p>
                  <p className="text-xl font-bold">{completedSkills} / {totalSkills}</p>
                </div>
              </div>
              <div className="h-2 bg-white/30 rounded-full overflow-hidden">
                <div
                  className="h-full bg-white transition-all duration-500"
                  style={{ width: `${(completedSkills / totalSkills) * 100}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Learning Progress Chart */}
        <div className="duo-card p-4 mb-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-base font-bold text-[var(--duo-text)] flex items-center gap-2">
              <TrendingUp size={18} className="text-[var(--duo-blue)]" />
              학습 진행 상황
            </h2>
            <div className="flex gap-1">
              <button
                onClick={() => setChartPeriod("week")}
                className={`px-3 py-1 text-xs font-semibold rounded-full transition-all ${
                  chartPeriod === "week"
                    ? "bg-[var(--duo-blue)] text-white"
                    : "bg-gray-100 text-gray-600"
                }`}
              >
                주간
              </button>
              <button
                onClick={() => setChartPeriod("month")}
                className={`px-3 py-1 text-xs font-semibold rounded-full transition-all ${
                  chartPeriod === "month"
                    ? "bg-[var(--duo-blue)] text-white"
                    : "bg-gray-100 text-gray-600"
                }`}
              >
                월간
              </button>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
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
                  border: '2px solid var(--duo-border)',
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
                stroke="var(--duo-blue)" 
                strokeWidth={2}
                name="획득 XP"
                dot={{ fill: 'var(--duo-blue)', r: 4 }}
              />
              <Line 
                type="monotone" 
                dataKey="words" 
                stroke="var(--duo-green)" 
                strokeWidth={2}
                name="학습 단어"
                dot={{ fill: 'var(--duo-green)', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Peer Comparison Chart */}
        <div className="duo-card p-4 mb-4">
          <h2 className="text-base font-bold text-[var(--duo-text)] mb-3 flex items-center gap-2">
            <Users size={18} className="text-[var(--duo-yellow)]" />
            또래 평균 비교
          </h2>
          <ResponsiveContainer width="100%" height={250}>
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
                  border: '2px solid var(--duo-border)',
                  borderRadius: '12px',
                  fontSize: '12px'
                }}
                formatter={(value: number, name: string, props: any) => {
                  return [`${value}${props.payload.unit}`, name];
                }}
              />
              <Legend 
                wrapperStyle={{ fontSize: '11px' }}
              />
              <Bar 
                dataKey="myValue" 
                fill="var(--duo-green)" 
                name="나의 기록"
                radius={[0, 8, 8, 0]}
              />
              <Bar 
                dataKey="peerAverage" 
                fill="#e0e0e0" 
                name="또래 평균"
                radius={[0, 8, 8, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-3 p-3 bg-green-50 rounded-lg">
            <p className="text-xs text-green-700 font-semibold">
              🎉 축하해요! 또래 평균보다 24% 더 열심히 학습하고 있어요!
            </p>
          </div>
        </div>

        {/* Category Filter */}
        <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
          {categories.map((cat) => (
            <button
              key={cat.value}
              onClick={() => setSelectedCategory(cat.value)}
              className={`px-4 py-2 rounded-full font-semibold whitespace-nowrap transition-all text-sm ${
                selectedCategory === cat.value
                  ? "bg-[var(--duo-green)] text-white shadow-lg scale-105"
                  : "bg-white text-gray-600 hover:bg-gray-100 duo-card"
              }`}
            >
              {cat.emoji} {cat.label}
            </button>
          ))}
        </div>

        {/* Skills List */}
        <div className="space-y-3">
          {filteredSkills.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">스킬이 없습니다</p>
            </div>
          ) : (
            filteredSkills.map((skill) => (
              <SkillProgress
                key={skill.skill_id}
                skill={skill}
                currentValue={mockUserSkillProgress[skill.skill_id as keyof typeof mockUserSkillProgress] || 0}
                showDetails={true}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
}
