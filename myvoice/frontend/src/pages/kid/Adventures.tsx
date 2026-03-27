/**
 * Adventures Page - Adventure Map (모험 지도)
 * Sequential path layout showing curriculum progression.
 * Nodes: completed(star) → current(pulse) → locked(grey lock)
 */

import { useState, lazy, Suspense } from "react";
import { Link } from "react-router-dom";
import { useAdventures } from "@/api/hooks/useAdventures";
import { useQueryClient } from "@tanstack/react-query";
import { Lock, Check, Star, Zap, BookOpen } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/api/client";
import type { Adventure } from "@/api/types";

const StorySelect = lazy(() => import("./StorySelect"));

const SKIP_COST = 30;

const STORY_WEEK_LABELS: Record<string, Record<number, { title: string; color: string }>> = {
    earth_crew: {
        1: { title: "1주차: 루나와 첫 만남", color: "from-indigo-500 to-blue-500" },
        2: { title: "2주차: 잃어버린 부품", color: "from-emerald-500 to-teal-500" },
        3: { title: "3주차: 마음 읽기 작전", color: "from-purple-500 to-pink-500" },
        4: { title: "4주차: 완벽한 변장", color: "from-amber-500 to-orange-500" },
    },
    kpop_hunters: {
        1: { title: "1주차: 스타 데뷔", color: "from-pink-500 to-rose-500" },
        2: { title: "2주차: 하모니 퀘스트", color: "from-violet-500 to-purple-500" },
        3: { title: "3주차: 하트 비트", color: "from-red-400 to-pink-500" },
        4: { title: "4주차: 그랜드 스테이지", color: "from-amber-500 to-yellow-500" },
    },
};

function AdventureNode({ adv, index, onSkip }: { adv: Adventure; index: number; onSkip?: (id: string) => void }) {
    const isCompleted = adv.status === "completed";
    const isUnlocked = adv.status === "unlocked" || adv.status === "in_progress";
    const isLocked = adv.status === "locked";
    const isEven = index % 2 === 0;

    const node = (
        <div className={`flex items-center gap-3 ${isEven ? "flex-row" : "flex-row-reverse"}`}>
            {/* Node circle */}
            <div
                className={`
                    relative w-16 h-16 rounded-full flex items-center justify-center text-2xl
                    shadow-lg border-4 transition-all duration-300 shrink-0
                    ${isCompleted
                        ? "bg-gradient-to-br from-green-400 to-emerald-500 border-green-300 text-white"
                        : isUnlocked
                            ? "bg-gradient-to-br from-indigo-400 to-purple-500 border-indigo-300 text-white animate-pulse"
                            : "bg-gray-200 border-gray-300 text-gray-400"
                    }
                `}
            >
                {isCompleted ? (
                    <Check size={28} strokeWidth={3} />
                ) : isLocked ? (
                    <Lock size={22} />
                ) : (
                    <span>{adv.emoji}</span>
                )}
                {/* Star badge for completed */}
                {isCompleted && adv.earnedStars && (
                    <div className="absolute -top-1 -right-1 bg-yellow-400 text-yellow-900 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold shadow">
                        <Star size={12} fill="currentColor" />
                    </div>
                )}
            </div>

            {/* Label */}
            <div className={`flex-1 ${isEven ? "text-left" : "text-right"}`}>
                <p
                    className={`font-bold text-sm leading-tight ${
                        isLocked ? "text-gray-400" : "text-[var(--bt-text)]"
                    }`}
                >
                    {adv.title}
                </p>
                <p className={`text-xs mt-0.5 ${isLocked ? "text-gray-300" : "text-[var(--bt-text-secondary)]"}`}>
                    {isCompleted
                        ? "완료! ⭐"
                        : isUnlocked
                            ? "도전하기 →"
                            : `${adv.difficulty}`
                    }
                </p>
                {/* Skip button for locked or unlocked (not completed) adventures */}
                {!isCompleted && onSkip && (
                    <button
                        onClick={(e) => { e.stopPropagation(); e.preventDefault(); onSkip(adv.sessionId); }}
                        className="mt-1.5 inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-100 text-amber-700 text-[11px] font-bold hover:bg-amber-200 active:scale-95 transition-all"
                    >
                        <Zap size={12} />
                        <Star size={10} fill="currentColor" className="text-amber-500" />
                        {SKIP_COST}으로 건너뛰기
                    </button>
                )}
            </div>
        </div>
    );

    if (isLocked) {
        return <div className="opacity-70">{node}</div>;
    }

    return (
        <Link to={`/kid/adventure/${adv.sessionId}`} className="block active:scale-95 transition-transform">
            {node}
        </Link>
    );
}

function PathConnector({ index }: { index: number }) {
    const isEven = index % 2 === 0;
    return (
        <div className={`flex ${isEven ? "justify-start pl-7" : "justify-end pr-7"}`}>
            <div className="w-0.5 h-8 bg-gradient-to-b from-gray-300 to-gray-200 rounded-full" />
        </div>
    );
}

export default function Adventures() {
    const { data: adventures, isLoading } = useAdventures();
    const queryClient = useQueryClient();
    const [skipTarget, setSkipTarget] = useState<{ id: string; title: string } | null>(null);
    const [isSkipping, setIsSkipping] = useState(false);
    const [showStorySelect, setShowStorySelect] = useState(false);

    const handleSkipRequest = (unitId: string) => {
        const adv = adventures?.find(a => a.sessionId === unitId);
        if (adv) setSkipTarget({ id: unitId, title: adv.title });
    };

    const handleSkipConfirm = async () => {
        if (!skipTarget) return;
        setIsSkipping(true);
        try {
            await api.post(`/v1/kid/adventures/${skipTarget.id}/skip`, {});
            toast.success("모험을 건너뛰었어요!");
            queryClient.invalidateQueries({ queryKey: ['adventures'] });
            setSkipTarget(null);
        } catch (err: unknown) {
            const msg = (err as { message?: string })?.message || "";
            if (msg.includes("Not enough stars")) {
                toast.error(`별이 부족해요! ${SKIP_COST}개가 필요합니다.`);
            } else {
                toast.error("건너뛰기에 실패했어요.");
            }
        } finally {
            setIsSkipping(false);
        }
    };

    if (isLoading) {
        return (
            <div className="h-full flex items-center justify-center">
                <div className="animate-spin w-8 h-8 border-4 border-indigo-400 border-t-transparent rounded-full" />
            </div>
        );
    }

    // No adventures = no story selected yet → show story selection
    const noStorySelected = !adventures || adventures.length === 0;
    if (noStorySelected || showStorySelect) {
        return (
            <Suspense fallback={<div className="h-full flex items-center justify-center"><div className="animate-spin w-8 h-8 border-4 border-indigo-400 border-t-transparent rounded-full" /></div>}>
                <StorySelect onSelected={() => {
                    setShowStorySelect(false);
                    queryClient.invalidateQueries({ queryKey: ['adventures'] });
                }} />
            </Suspense>
        );
    }

    const sorted = [...adventures].sort((a, b) => a.order - b.order);

    // Detect story theme from unit IDs (KPOP_ prefix = kpop_hunters)
    const storyTheme = sorted[0]?.sessionId?.startsWith("KPOP_") ? "kpop_hunters" : "earth_crew";
    const WEEK_LABELS = STORY_WEEK_LABELS[storyTheme] || STORY_WEEK_LABELS.earth_crew;

    // Group by week
    const weeks = new Map<number, Adventure[]>();
    for (const adv of sorted) {
        const w = adv.week || 1;
        if (!weeks.has(w)) weeks.set(w, []);
        weeks.get(w)!.push(adv);
    }

    return (
        <div className="h-full flex flex-col bg-gradient-to-b from-[#f0f4ff] to-[#e8eeff] overflow-hidden">
            <div className="flex-1 overflow-y-auto px-5 py-5 pb-28">
                {/* Header */}
                <div className="text-center mb-6">
                    <h1 className="text-xl font-bold text-[var(--bt-text)]">🗺️ 모험 지도</h1>
                    <p className="text-xs text-[var(--bt-text-secondary)] mt-1">
                        순서대로 모험을 완료하면 다음 모험이 열려요!
                    </p>
                    {/* Story switch button */}
                    <button
                        onClick={() => setShowStorySelect(true)}
                        className="mt-2 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/80 border border-gray-200 text-xs font-bold text-[var(--bt-text-secondary)] hover:bg-white active:scale-95 transition-all shadow-sm"
                    >
                        <BookOpen size={14} />
                        스토리 변경
                    </button>
                </div>

                {/* Adventure path per week */}
                {Array.from(weeks.entries()).map(([weekNum, weekAdvs]) => {
                    const weekInfo = WEEK_LABELS[weekNum] || { title: `${weekNum}주차`, color: "from-gray-500 to-gray-600" };
                    return (
                        <div key={weekNum} className="mb-8">
                            {/* Week header */}
                            <div className={`bg-gradient-to-r ${weekInfo.color} text-white rounded-xl px-4 py-2 mb-4 shadow-md`}>
                                <h2 className="text-sm font-bold">{weekInfo.title}</h2>
                            </div>

                            {/* Path nodes */}
                            <div className="space-y-0">
                                {weekAdvs.map((adv, idx) => (
                                    <div key={adv.sessionId}>
                                        <AdventureNode adv={adv} index={idx} onSkip={handleSkipRequest} />
                                        {idx < weekAdvs.length - 1 && <PathConnector index={idx} />}
                                    </div>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Skip Confirmation Dialog */}
            {skipTarget && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-2xl p-6 mx-6 max-w-sm w-full text-center shadow-2xl">
                        <div className="text-4xl mb-3">⚡</div>
                        <h3 className="text-lg font-extrabold text-[var(--bt-text)] mb-1">모험 건너뛰기</h3>
                        <p className="text-sm text-[var(--bt-text-secondary)] mb-4">
                            <strong>"{skipTarget.title}"</strong>을(를) 건너뛸까요?
                        </p>
                        <div className="flex items-center justify-center gap-1 mb-5 bg-amber-50 rounded-xl py-2">
                            <Star size={16} fill="currentColor" className="text-amber-500" />
                            <span className="text-sm font-bold text-amber-700">{SKIP_COST}개 별 사용</span>
                        </div>
                        <div className="flex gap-3">
                            <button
                                onClick={() => setSkipTarget(null)}
                                className="flex-1 py-3 rounded-xl border-2 border-gray-200 font-bold text-[var(--bt-text-secondary)]"
                            >
                                취소
                            </button>
                            <button
                                onClick={handleSkipConfirm}
                                disabled={isSkipping}
                                className="flex-1 py-3 rounded-xl bg-amber-500 text-white font-bold disabled:opacity-50 active:scale-95 transition-all"
                            >
                                {isSkipping ? "처리 중..." : "건너뛰기"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
