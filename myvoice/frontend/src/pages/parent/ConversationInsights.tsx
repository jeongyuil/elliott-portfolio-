/**
 * Conversation Insights — Wireframe #11
 * Keywords, sentiment analysis, language mix, behavior patterns, activity timeline
 */
import { useEffect, useState } from "react";
import { parentApi } from "@/api/client";
import type {
    ChildProfile,
    KeywordItem,
    SentimentSummary,
    TimelineDay,
    LanguageMix,
    BehaviorPatterns,
} from "@/api/types";
import { MessageCircle, TrendingUp, Globe, Brain, Activity, Loader2 } from "lucide-react";

const EMOTION_EMOJI: Record<string, string> = {
    happy: "😊",
    excited: "🤩",
    neutral: "😐",
    sad: "😢",
    frustrated: "😤",
    curious: "🤔",
    shy: "😳",
    confident: "💪",
};

const EMOTION_COLOR: Record<string, string> = {
    happy: "bg-yellow-100 text-yellow-700",
    excited: "bg-orange-100 text-orange-700",
    neutral: "bg-gray-100 text-gray-700",
    sad: "bg-blue-100 text-blue-700",
    frustrated: "bg-red-100 text-red-700",
    curious: "bg-purple-100 text-purple-700",
    shy: "bg-pink-100 text-pink-700",
    confident: "bg-green-100 text-green-700",
};

export default function ConversationInsights() {
    const [children, setChildren] = useState<ChildProfile[]>([]);
    const [selectedChildId, setSelectedChildId] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const [keywords, setKeywords] = useState<KeywordItem[]>([]);
    const [sentiment, setSentiment] = useState<SentimentSummary | null>(null);
    const [timeline, setTimeline] = useState<TimelineDay[]>([]);
    const [languageMix, setLanguageMix] = useState<LanguageMix | null>(null);
    const [behavior, setBehavior] = useState<BehaviorPatterns | null>(null);

    // Fetch children
    useEffect(() => {
        (async () => {
            try {
                const data = await parentApi.listChildren();
                setChildren(data);
                if (data.length > 0) setSelectedChildId(data[0].childId);
            } catch {
                // silently fail
            }
        })();
    }, []);

    // Fetch insights data
    useEffect(() => {
        if (!selectedChildId) return;
        setIsLoading(true);

        Promise.all([
            parentApi.getKeywords(selectedChildId).catch(() => []),
            parentApi.getSentiment(selectedChildId).catch(() => null),
            parentApi.getTimeline(selectedChildId).catch(() => []),
            parentApi.getLanguageMix(selectedChildId).catch(() => null),
            parentApi.getBehavior(selectedChildId).catch(() => null),
        ]).then(([kw, sent, tl, lang, beh]) => {
            setKeywords(kw as KeywordItem[]);
            setSentiment(sent as SentimentSummary | null);
            setTimeline(tl as TimelineDay[]);
            setLanguageMix(lang as LanguageMix | null);
            setBehavior(beh as BehaviorPatterns | null);
            setIsLoading(false);
        });
    }, [selectedChildId]);

    const maxKeywordCount = keywords.length > 0 ? keywords[0].count : 1;
    const maxTimelineMinutes = Math.max(...timeline.map((d) => d.totalMinutes), 1);

    if (!selectedChildId) {
        return (
            <div className="flex items-center justify-center h-64">
                <Loader2 className="w-6 h-6 animate-spin text-[var(--bt-primary)]" />
            </div>
        );
    }

    return (
        <div className="p-4 pb-24 max-w-2xl mx-auto space-y-5">
            {/* Header */}
            <div>
                <h1 className="text-xl font-bold text-[var(--bt-text)]">대화 인사이트</h1>
                <p className="text-sm text-[var(--bt-text-secondary)] mt-0.5">
                    아이의 대화 패턴과 성장을 한눈에
                </p>
            </div>

            {/* Child selector */}
            {children.length > 1 && (
                <div className="flex gap-2 overflow-x-auto pb-1">
                    {children.map((c) => (
                        <button
                            key={c.childId}
                            onClick={() => setSelectedChildId(c.childId)}
                            className={`px-3 py-1.5 rounded-full text-sm font-semibold whitespace-nowrap transition-colors ${
                                c.childId === selectedChildId
                                    ? "bg-[var(--bt-primary)] text-white"
                                    : "bg-[var(--bt-bg)] text-[var(--bt-text-secondary)] border border-[var(--bt-border)]"
                            }`}
                        >
                            {c.name}
                        </button>
                    ))}
                </div>
            )}

            {isLoading ? (
                <div className="flex items-center justify-center h-48">
                    <Loader2 className="w-6 h-6 animate-spin text-[var(--bt-primary)]" />
                </div>
            ) : (
                <>
                    {/* Keywords Cloud */}
                    <section className="bt-card p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <MessageCircle size={18} className="text-[var(--bt-primary)]" />
                            <h2 className="font-bold text-[var(--bt-text)]">자주 사용한 단어</h2>
                        </div>
                        {keywords.length === 0 ? (
                            <p className="text-sm text-[var(--bt-text-muted)] text-center py-4">
                                아직 대화 데이터가 없습니다
                            </p>
                        ) : (
                            <div className="flex flex-wrap gap-2">
                                {keywords.map((kw) => {
                                    const ratio = kw.count / maxKeywordCount;
                                    const size =
                                        ratio > 0.7 ? "text-lg px-3 py-1.5" :
                                        ratio > 0.4 ? "text-sm px-2.5 py-1" :
                                        "text-xs px-2 py-0.5";
                                    return (
                                        <span
                                            key={kw.word}
                                            className={`bg-indigo-50 text-indigo-700 rounded-full font-semibold ${size}`}
                                        >
                                            {kw.word}
                                            <span className="text-indigo-400 ml-1 text-[10px]">{kw.count}</span>
                                        </span>
                                    );
                                })}
                            </div>
                        )}
                    </section>

                    {/* Sentiment Analysis */}
                    <section className="bt-card p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <TrendingUp size={18} className="text-[var(--bt-primary)]" />
                            <h2 className="font-bold text-[var(--bt-text)]">정서 분석</h2>
                        </div>
                        {!sentiment || sentiment.emotions.length === 0 ? (
                            <p className="text-sm text-[var(--bt-text-muted)] text-center py-4">
                                감정 데이터가 아직 없습니다
                            </p>
                        ) : (
                            <>
                                <div className="flex items-center gap-2 mb-3 p-2 bg-[var(--bt-bg)] rounded-lg">
                                    <span className="text-2xl">{EMOTION_EMOJI[sentiment.overall] || "😊"}</span>
                                    <div>
                                        <p className="text-sm font-semibold text-[var(--bt-text)]">전반적 감정</p>
                                        <p className="text-xs text-[var(--bt-text-secondary)] capitalize">
                                            {sentiment.overall}
                                        </p>
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    {sentiment.emotions.slice(0, 5).map((e) => (
                                        <div key={e.label} className="flex items-center gap-2">
                                            <span className={`text-xs font-semibold rounded-full px-2 py-0.5 ${EMOTION_COLOR[e.label] || "bg-gray-100 text-gray-600"}`}>
                                                {EMOTION_EMOJI[e.label] || "😶"} {e.label}
                                            </span>
                                            <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-[var(--bt-primary)] rounded-full transition-all"
                                                    style={{ width: `${e.percentage}%` }}
                                                />
                                            </div>
                                            <span className="text-xs text-[var(--bt-text-muted)] w-8 text-right">
                                                {e.percentage}%
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </>
                        )}
                    </section>

                    {/* Language Mix */}
                    <section className="bt-card p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <Globe size={18} className="text-[var(--bt-primary)]" />
                            <h2 className="font-bold text-[var(--bt-text)]">언어 비율</h2>
                        </div>
                        {!languageMix ? (
                            <p className="text-sm text-[var(--bt-text-muted)] text-center py-4">데이터 없음</p>
                        ) : (
                            <div>
                                <div className="flex justify-between text-sm mb-1.5">
                                    <span className="font-semibold text-blue-600">🇰🇷 한국어 {languageMix.koreanRatio}%</span>
                                    <span className="font-semibold text-red-500">🇺🇸 영어 {languageMix.englishRatio}%</span>
                                </div>
                                <div className="h-4 bg-gray-100 rounded-full overflow-hidden flex">
                                    <div
                                        className="h-full bg-blue-400 transition-all"
                                        style={{ width: `${languageMix.koreanRatio}%` }}
                                    />
                                    <div
                                        className="h-full bg-red-400 transition-all"
                                        style={{ width: `${languageMix.englishRatio}%` }}
                                    />
                                </div>
                                <p className="text-xs text-[var(--bt-text-muted)] mt-1.5 text-center">
                                    총 {languageMix.totalUtterances}회 발화 기준
                                </p>
                            </div>
                        )}
                    </section>

                    {/* Behavior Patterns */}
                    <section className="bt-card p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <Brain size={18} className="text-[var(--bt-primary)]" />
                            <h2 className="font-bold text-[var(--bt-text)]">행동 패턴</h2>
                        </div>
                        {!behavior ? (
                            <p className="text-sm text-[var(--bt-text-muted)] text-center py-4">데이터 없음</p>
                        ) : (
                            <div className="grid grid-cols-2 gap-3">
                                <StatBox label="평균 세션" value={`${behavior.avgSessionMinutes}분`} />
                                <StatBox label="참여도" value={`${behavior.avgEngagement}%`} />
                                <StatBox label="발음 점수" value={`${behavior.avgPronunciation}점`} />
                                <StatBox label="유창성" value={`${behavior.avgFluency}%`} />
                                <StatBox label="세션 횟수" value={`${behavior.sessionCount}회`} />
                                <StatBox label="턴당 단어" value={`${behavior.avgWordsPerTurn}개`} />
                            </div>
                        )}
                    </section>

                    {/* Activity Timeline */}
                    <section className="bt-card p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <Activity size={18} className="text-[var(--bt-primary)]" />
                            <h2 className="font-bold text-[var(--bt-text)]">활동 타임라인</h2>
                        </div>
                        {timeline.length === 0 ? (
                            <p className="text-sm text-[var(--bt-text-muted)] text-center py-4">
                                최근 활동 데이터가 없습니다
                            </p>
                        ) : (
                            <div className="space-y-1.5">
                                {timeline.map((day) => {
                                    const date = new Date(day.date);
                                    const dayLabel = `${date.getMonth() + 1}/${date.getDate()}`;
                                    const barWidth = Math.max((day.totalMinutes / maxTimelineMinutes) * 100, 4);
                                    return (
                                        <div key={day.date} className="flex items-center gap-2">
                                            <span className="text-xs text-[var(--bt-text-muted)] w-10 text-right">
                                                {dayLabel}
                                            </span>
                                            <div className="flex-1 h-5 bg-gray-50 rounded overflow-hidden">
                                                <div
                                                    className="h-full bg-gradient-to-r from-[var(--bt-primary)] to-indigo-400 rounded transition-all flex items-center px-1.5"
                                                    style={{ width: `${barWidth}%` }}
                                                >
                                                    {day.totalMinutes > 0 && (
                                                        <span className="text-[10px] text-white font-semibold whitespace-nowrap">
                                                            {day.totalMinutes}분
                                                        </span>
                                                    )}
                                                </div>
                                            </div>
                                            <span className="text-[10px] text-[var(--bt-text-muted)] w-12">
                                                {day.sessions}세션
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </section>
                </>
            )}
        </div>
    );
}

function StatBox({ label, value }: { label: string; value: string }) {
    return (
        <div className="bg-[var(--bt-bg)] rounded-xl p-3 text-center">
            <p className="text-lg font-bold text-[var(--bt-text)]">{value}</p>
            <p className="text-[10px] text-[var(--bt-text-muted)] mt-0.5">{label}</p>
        </div>
    );
}
