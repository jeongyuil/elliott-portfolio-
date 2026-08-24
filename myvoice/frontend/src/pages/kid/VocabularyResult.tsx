/**
 * VocabularyResult Page
 * Design Philosophy: Encouraging feedback for vocabulary learning completion
 */

import { useEffect } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { Star, TrendingUp, Home, BookOpen } from "lucide-react";
import { vocabularyCategories } from "@/lib/mockData";

export default function VocabularyResult() {
    const { category: categoryId } = useParams();
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();

    const category = vocabularyCategories.find((c) => c.id === categoryId);

    // Get URL params
    const wordsLearned = Number(searchParams.get("wordsLearned")) || 10;
    const stars = Number(searchParams.get("stars")) || 5;
    const xp = Number(searchParams.get("xp")) || 25;

    // Create mock API hooks or call logic here if needed
    // For Phase 2, we just simulate the completeCategory mutation

    useEffect(() => {
        // Prevent back navigation
        window.history.pushState(null, "", window.location.href);
        window.addEventListener("popstate", () => {
            window.history.pushState(null, "", window.location.href);
        });

        // Update weekly goals
        if (category) {
            // Mock API call simulation
            if (import.meta.env.DEV) console.log(`Completed category ${category.name}, +${xp} XP, +${wordsLearned} words`);
            // toast.success("학습 완료!"); // Already implied by the screen
        }
    }, [category, xp, wordsLearned]);

    if (!category) {
        return (
            <div className="h-full flex items-center justify-center bg-[var(--bt-bg)]">
                <div className="text-center">
                    <div className="text-6xl mb-4">🔍</div>
                    <p className="text-[var(--bt-text-secondary)]">카테고리를 찾을 수 없습니다</p>
                    <button
                        onClick={() => navigate("/kid/vocabulary")}
                        className="mt-4 px-6 py-3 bg-[var(--bt-primary)] text-white font-bold rounded-xl shadow-[0_4px_0_#58cc02] active:shadow-none active:translate-y-1 transition-all"
                    >
                        어휘 목록으로
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="h-full bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex items-center justify-center p-4 overflow-y-auto pb-24">
            <div className="max-w-md w-full">
                {/* Success Animation */}
                <div className="text-center mb-8 animate-in zoom-in duration-500">
                    <div className="text-8xl mb-4 animate-bounce">{category.emoji}</div>
                    <h1 className="text-3xl font-black text-[var(--bt-text)] mb-2">
                        완벽해요! 🎉
                    </h1>
                    <p className="text-lg text-[var(--bt-text-secondary)]">
                        {category.name} 카테고리 완료!
                    </p>
                </div>

                {/* Rewards Card */}
                <div className="bt-card p-6 mb-6 animate-in slide-in-from-bottom duration-700 bg-white">
                    <div className="text-center mb-6">
                        <h2 className="text-xl font-bold text-[var(--bt-text)] mb-4">획득한 보상</h2>

                        {/* Words Learned */}
                        <div className="mb-4 p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl border border-blue-100">
                            <div className="flex items-center justify-center gap-2 mb-2">
                                <BookOpen size={24} className="text-blue-500" />
                                <span className="text-2xl font-black text-blue-600">+{wordsLearned}</span>
                            </div>
                            <p className="text-sm text-[var(--bt-text-secondary)]">단어 학습 완료</p>
                        </div>

                        {/* Stars */}
                        <div className="mb-4 p-4 bg-gradient-to-r from-yellow-50 to-amber-50 rounded-xl border border-yellow-100">
                            <div className="flex items-center justify-center gap-2 mb-2">
                                <Star size={24} className="text-yellow-500" fill="currentColor" />
                                <span className="text-2xl font-black text-yellow-600">+{stars}</span>
                            </div>
                            <p className="text-sm text-[var(--bt-text-secondary)]">별 획득</p>
                        </div>

                        {/* XP */}
                        <div className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border border-purple-100">
                            <div className="flex items-center justify-center gap-2 mb-2">
                                <TrendingUp size={24} className="text-purple-500" />
                                <span className="text-2xl font-black text-purple-600">+{xp} XP</span>
                            </div>
                            <p className="text-sm text-[var(--bt-text-secondary)]">경험치 획득</p>
                        </div>
                    </div>

                    {/* Progress Message */}
                    <div className="text-center p-4 bg-green-50 rounded-xl border border-green-100">
                        <p className="text-sm font-semibold text-green-700">
                            🎯 주간 목표에 {wordsLearned}개 단어가 추가되었어요!
                        </p>
                    </div>
                </div>

                {/* Action Buttons */}
                <div className="grid grid-cols-2 gap-3 animate-in slide-in-from-bottom duration-1000">
                    <button
                        onClick={() => navigate("/kid/home")}
                        className="w-full bg-white hover:bg-gray-50 text-[var(--bt-text-secondary)] font-bold py-4 rounded-xl text-lg border-2 border-gray-200 transition-colors flex items-center justify-center gap-2"
                    >
                        <Home size={20} />
                        <span>홈으로</span>
                    </button>
                    <button
                        onClick={() => navigate("/kid/vocabulary")}
                        className="w-full bg-[var(--bt-accent)] hover:bg-[#1cb0f6] text-white font-bold py-4 rounded-xl text-lg shadow-[0_4px_0_#1899d6] active:shadow-none active:translate-y-1 transition-all flex items-center justify-center gap-2"
                    >
                        <BookOpen size={20} />
                        <span>다음 학습</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
