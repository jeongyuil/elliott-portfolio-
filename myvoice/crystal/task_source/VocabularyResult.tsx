/**
 * VocabularyResult Page
 * Design Philosophy: Encouraging feedback for vocabulary learning completion
 * - Celebration with rewards display
 * - Similar to MissionResult but for vocabulary categories
 */

import { useEffect } from "react";
import { useRoute, useLocation } from "wouter";
import { Star, TrendingUp, Home, BookOpen } from "lucide-react";
import { vocabularyCategories } from "@/lib/mockData";
import { trpc } from "@/lib/trpc";
import { toast } from "sonner";

export default function VocabularyResult() {
  const [, params] = useRoute("/vocabulary/:category/result");
  const [, setLocation] = useLocation();
  
  const category = vocabularyCategories.find((c) => c.id === params?.category);
  
  // Get URL params
  const urlParams = new URLSearchParams(window.location.search);
  const wordsLearned = Number(urlParams.get("wordsLearned")) || 10;
  const stars = Number(urlParams.get("stars")) || 5;
  const xp = Number(urlParams.get("xp")) || 25;
  
  const utils = trpc.useUtils();
  
  const completeCategory = trpc.vocabulary.completeCategory.useMutation({
    onMutate: async (variables) => {
      // Cancel any outgoing refetches
      await utils.weeklyGoals.getCurrent.cancel();
      
      // Snapshot the previous value
      const previousGoals = utils.weeklyGoals.getCurrent.getData();
      
      // Optimistically update weekly goals
      if (previousGoals) {
        utils.weeklyGoals.getCurrent.setData(undefined, {
          ...previousGoals,
          xpCurrent: previousGoals.xpCurrent + variables.earnedXp,
          wordsCurrent: previousGoals.wordsCurrent + variables.wordsLearned,
        });
      }
      
      return { previousGoals };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousGoals) {
        utils.weeklyGoals.getCurrent.setData(undefined, context.previousGoals);
      }
      toast.error("어휘 학습 완료 처리에 실패했습니다.");
    },
    onSuccess: () => {
      console.log("🎉 주간 목표가 업데이트되었습니다!");
    },
    onSettled: () => {
      // Refetch to ensure data is in sync with server
      utils.weeklyGoals.getCurrent.invalidate();
    },
  });

  useEffect(() => {
    // Prevent back navigation
    window.history.pushState(null, "", window.location.href);
    window.addEventListener("popstate", () => {
      window.history.pushState(null, "", window.location.href);
    });
    
    // Update weekly goals
    if (category) {
      // For mock data, use a placeholder categoryId (will be replaced with real DB id later)
      const categoryId = typeof category.id === 'string' ? 1 : category.id;
      completeCategory.mutate({
        categoryId,
        wordsLearned,
        earnedStars: stars,
        earnedXp: xp,
      });
    }
  }, [category?.id]);

  if (!category) {
    return (
      <div className="min-h-screen bg-[var(--duo-bg)] flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🔍</div>
          <p className="text-[var(--duo-text-secondary)]">카테고리를 찾을 수 없습니다</p>
          <button
            onClick={() => setLocation("/vocabulary")}
            className="mt-4 duo-btn-primary"
          >
            어휘 목록으로
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Success Animation */}
        <div className="text-center mb-8 animate-in zoom-in duration-500">
          <div className="text-8xl mb-4 animate-bounce">{category.emoji}</div>
          <h1 className="text-3xl font-black text-[var(--duo-text)] mb-2">
            완벽해요! 🎉
          </h1>
          <p className="text-lg text-[var(--duo-text-secondary)]">
            {category.name} 카테고리 완료!
          </p>
        </div>

        {/* Rewards Card */}
        <div className="duo-card p-6 mb-6 animate-in slide-in-from-bottom duration-700">
          <div className="text-center mb-6">
            <h2 className="text-xl font-bold text-[var(--duo-text)] mb-4">획득한 보상</h2>
            
            {/* Words Learned */}
            <div className="mb-4 p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl">
              <div className="flex items-center justify-center gap-2 mb-2">
                <BookOpen size={24} className="text-blue-500" />
                <span className="text-2xl font-black text-blue-600">+{wordsLearned}</span>
              </div>
              <p className="text-sm text-[var(--duo-text-secondary)]">단어 학습 완료</p>
            </div>

            {/* Stars */}
            <div className="mb-4 p-4 bg-gradient-to-r from-yellow-50 to-amber-50 rounded-xl">
              <div className="flex items-center justify-center gap-2 mb-2">
                <Star size={24} className="text-yellow-500" fill="currentColor" />
                <span className="text-2xl font-black text-yellow-600">+{stars}</span>
              </div>
              <p className="text-sm text-[var(--duo-text-secondary)]">별 획득</p>
            </div>

            {/* XP */}
            <div className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
              <div className="flex items-center justify-center gap-2 mb-2">
                <TrendingUp size={24} className="text-purple-500" />
                <span className="text-2xl font-black text-purple-600">+{xp} XP</span>
              </div>
              <p className="text-sm text-[var(--duo-text-secondary)]">경험치 획득</p>
            </div>
          </div>

          {/* Progress Message */}
          <div className="text-center p-4 bg-green-50 rounded-xl">
            <p className="text-sm font-semibold text-green-700">
              🎯 주간 목표에 {wordsLearned}개 단어가 추가되었어요!
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-3 animate-in slide-in-from-bottom duration-1000">
          <button
            onClick={() => setLocation("/")}
            className="duo-btn-secondary flex items-center justify-center gap-2"
          >
            <Home size={18} />
            <span>홈으로</span>
          </button>
          <button
            onClick={() => setLocation("/vocabulary")}
            className="duo-btn-primary flex items-center justify-center gap-2"
          >
            <BookOpen size={18} />
            <span>다음 학습</span>
          </button>
        </div>
      </div>
    </div>
  );
}
