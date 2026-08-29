/**
 * Home Page - Mobile Optimized with Pull-to-Refresh
 * Design Philosophy: Duolingo-style learning dashboard
 * - User info integrated into main content
 * - Scrollable content area with pull-to-refresh
 * - Bottom navigation fixed
 */

import { Heart, Flame, ArrowRight, Trophy, Target, Book, RefreshCw, LogIn } from "lucide-react";
import { Link } from "wouter";
import { getLoginUrl } from "@/const";
import { useState, useEffect } from "react";
import BottomNav from "@/components/layout/BottomNav";
import MissionCard from "@/components/mission/MissionCard";
import { userData, missions, weeklyGoals as mockWeeklyGoals } from "@/lib/mockData";
import { usePullToRefresh } from "@/hooks/usePullToRefresh";
import { toast } from "sonner";
import { trpc } from "@/lib/trpc";
import { useAuth } from "@/_core/hooks/useAuth";
import DailyBonusModal from "@/components/DailyBonusModal";
import OnboardingTutorial from "@/components/OnboardingTutorial";

export default function Home() {
  const { user, isAuthenticated } = useAuth();
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [showBonusModal, setShowBonusModal] = useState(false);
  const [bonusReward, setBonusReward] = useState<any>(null);
  const [showOnboarding, setShowOnboarding] = useState(false);
  
  // Complete onboarding mutation
  const completeOnboardingMutation = trpc.user.completeOnboarding.useMutation();
  
  // Check if user needs onboarding
  useEffect(() => {
    if (isAuthenticated && user && !user.onboardingCompleted) {
      // Show onboarding after a short delay to let daily bonus show first
      const timer = setTimeout(() => {
        setShowOnboarding(true);
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [isAuthenticated, user]);
  
  const handleCompleteOnboarding = async () => {
    setShowOnboarding(false);
    await completeOnboardingMutation.mutateAsync();
    toast.success("환영합니다! 이제 학습을 시작해보세요! 🎉");
  };
  
  const handleSkipOnboarding = async () => {
    setShowOnboarding(false);
    await completeOnboardingMutation.mutateAsync();
  };
  
  // Check and claim daily bonus
  const claimBonusMutation = trpc.dailyBonus.claimDailyBonus.useMutation({
    onSuccess: (data) => {
      if (data) {
        setBonusReward(data);
        setShowBonusModal(true);
      }
    },
  });
  
  // Auto-claim bonus on page load if authenticated
  useEffect(() => {
    if (isAuthenticated && !claimBonusMutation.isPending) {
      claimBonusMutation.mutate();
    }
  }, [isAuthenticated]);
  
  // Fetch user missions from database
  const { data: userMissionsData } = trpc.missions.getUserMissions.useQuery(
    undefined,
    { enabled: isAuthenticated }
  );
  
  // Get today's missions with completion status
  const todayMissions = missions.slice(0, 3).map(mission => {
    const userMission = userMissionsData?.find(um => um.missionId === mission.id);
    const isCompleted = userMission?.status === 'completed';
    return {
      ...mission,
      completed: isCompleted,
      earnedStars: isCompleted ? mission.rewards.stars : undefined,
      earnedXp: isCompleted ? mission.rewards.xp : undefined,
    };
  }).sort((a, b) => {
    // Sort: incomplete missions first (false < true), completed missions last
    if (a.completed === b.completed) return 0;
    return a.completed ? 1 : -1;
  });
  
  // Fetch weekly goals from database
  const { data: weeklyGoalsData, refetch: refetchGoals } = trpc.weeklyGoals.getCurrent.useQuery(
    undefined,
    { enabled: isAuthenticated }
  );
  
  // Use database data if available, otherwise fallback to mock data
  const weeklyGoals = weeklyGoalsData ? {
    xp: { current: weeklyGoalsData.xpCurrent, target: weeklyGoalsData.xpTarget },
    missions: { current: weeklyGoalsData.missionsCurrent, target: weeklyGoalsData.missionsTarget },
    studyTime: { current: weeklyGoalsData.studyTimeCurrent, target: weeklyGoalsData.studyTimeTarget },
    words: { current: weeklyGoalsData.wordsCurrent, target: weeklyGoalsData.wordsTarget },
  } : mockWeeklyGoals;
  
  // Use authenticated user data if available, otherwise fallback to mock data
  const currentUser = user || userData;

  const handleRefresh = async () => {
    if (isAuthenticated) {
      await refetchGoals();
      // Refetch user missions is automatic via React Query
    }
    setLastUpdated(new Date());
    toast.success("최신 정보로 업데이트되었습니다!");
  };

  const { containerRef, isPulling, isRefreshing, pullDistance, threshold } = usePullToRefresh({
    onRefresh: handleRefresh,
    threshold: 80,
  });

  const pullProgress = Math.min(pullDistance / threshold, 1);
  const showRefreshIcon = pullDistance > 0;

  return (
    <div className="h-screen flex flex-col bg-[var(--duo-bg)] overflow-hidden">
      {/* Pull-to-Refresh Indicator */}
      {showRefreshIcon && (
        <div 
          className="absolute top-0 left-0 right-0 flex items-center justify-center z-50 transition-all duration-200"
          style={{
            height: `${pullDistance}px`,
            opacity: pullProgress,
          }}
        >
          <div className="bg-white rounded-full p-2 shadow-lg">
            <RefreshCw 
              size={24} 
              className={`text-[var(--duo-green)] ${isRefreshing ? 'animate-spin' : ''}`}
              style={{
                transform: `rotate(${pullProgress * 360}deg)`,
              }}
            />
          </div>
        </div>
      )}

      {/* Main Content - Scrollable with Pull-to-Refresh */}
      <div 
        ref={containerRef}
        className="flex-1 overflow-y-auto px-4 py-4"
        style={{
          transform: `translateY(${isPulling || isRefreshing ? pullDistance : 0}px)`,
          transition: isPulling ? 'none' : 'transform 0.3s ease-out',
        }}
      >
        {/* User Info */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <span className="text-3xl">{currentUser.avatar || "🐰"}</span>
            <div>
              <h1 className="text-lg font-bold text-[var(--duo-text)]">
                {isAuthenticated 
                  ? `안녕, ${currentUser.nickname || ("name" in currentUser ? currentUser.name : null) || "학습자"}님! 👋`
                  : "안녕하세요! 👋"}
              </h1>
              <p className="text-sm text-[var(--duo-text-secondary)]">
                {isAuthenticated ? "Ready to help Luna?" : "로그인하고 학습을 시작하세요!"}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {isAuthenticated ? (
              <>
                {Array.from({ length: currentUser.maxHearts || 3 }).map((_, i) => (
                  <Heart
                    key={i}
                    size={18}
                    className={i < (currentUser.hearts || 3) ? "duo-heart" : "text-gray-300"}
                    fill={i < (currentUser.hearts || 3) ? "currentColor" : "none"}
                  />
                ))}
              </>
            ) : (
              <button
                onClick={() => window.location.href = getLoginUrl()}
                className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-full shadow-md transition-all"
              >
                <LogIn size={18} />
                <span>로그인</span>
              </button>
            )}
          </div>
        </div>

        {/* Weekly Goals Summary - Simplified & Emphasized */}
        <Link href="/skills">
          <div className="relative overflow-hidden rounded-2xl p-5 mb-4 cursor-pointer hover:scale-[1.02] transition-all duration-200 shadow-md hover:shadow-xl bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500">
            {/* Background Pattern */}
            <div className="absolute inset-0 opacity-10">
              <div className="absolute top-0 right-0 w-32 h-32 bg-white rounded-full -translate-y-1/2 translate-x-1/2"></div>
              <div className="absolute bottom-0 left-0 w-24 h-24 bg-white rounded-full translate-y-1/2 -translate-x-1/2"></div>
            </div>
            
            {/* Content */}
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Target size={22} className="text-white" />
                  <h2 className="text-lg font-bold text-white">이번 주 목표</h2>
                </div>
                <div className="flex items-center gap-2">
                  <div className="flex items-center gap-1.5 bg-white/20 backdrop-blur-sm rounded-full px-3 py-1">
                    <Flame size={16} className="text-yellow-300" fill="currentColor" />
                    <span className="text-sm font-bold text-white">{currentUser.streak || 7}일 연속</span>
                  </div>
                  <ArrowRight size={18} className="text-white" />
                </div>
              </div>
              
              {/* Overall Progress */}
              <div className="mb-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-white/90">주간 달성률</span>
                  <span className="text-2xl font-bold text-white">
                    {Math.round(
                      ((weeklyGoals.xp.current / weeklyGoals.xp.target) +
                      (weeklyGoals.missions.current / weeklyGoals.missions.target) +
                      (weeklyGoals.studyTime.current / weeklyGoals.studyTime.target) +
                      (weeklyGoals.words.current / weeklyGoals.words.target)) / 4 * 100
                    )}%
                  </span>
                </div>
                <div className="w-full bg-white/30 backdrop-blur-sm rounded-full h-3 shadow-inner">
                  <div 
                    className="bg-white h-3 rounded-full transition-all duration-500 shadow-lg" 
                    style={{ 
                      width: `${Math.min(
                        ((weeklyGoals.xp.current / weeklyGoals.xp.target) +
                        (weeklyGoals.missions.current / weeklyGoals.missions.target) +
                        (weeklyGoals.studyTime.current / weeklyGoals.studyTime.target) +
                        (weeklyGoals.words.current / weeklyGoals.words.target)) / 4 * 100,
                        100
                      )}%` 
                    }}
                  ></div>
                </div>
              </div>
              
              <div className="text-center mt-4">
                <span className="text-sm text-white/90 font-semibold">탭하여 자세히 보기 →</span>
              </div>
            </div>
          </div>
        </Link>

        {/* Today's Missions */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-bold text-[var(--duo-text)]">오늘의 미션</h2>
            <Link href="/missions">
              <div className="flex items-center gap-1 text-sm font-semibold text-[var(--duo-blue)] cursor-pointer">
                <span>전체보기</span>
                <ArrowRight size={14} />
              </div>
            </Link>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {todayMissions.map((mission) => (
              <MissionCard key={mission.id} {...mission} />
            ))}
          </div>
        </div>

        {/* Quick Actions - Compact */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <Link href="/vocabulary">
            <div className="duo-card p-4 text-center cursor-pointer">
              <div className="text-3xl mb-1">📚</div>
              <h3 className="font-bold text-sm text-[var(--duo-text)]">어휘 학습</h3>
              <p className="text-xs text-[var(--duo-text-secondary)] mt-1">
                {userData.stats.vocabularyLearned}개 완료
              </p>
            </div>
          </Link>
          <Link href="/shop">
            <div className="duo-card p-4 text-center cursor-pointer">
              <div className="text-3xl mb-1">🛍️</div>
              <h3 className="font-bold text-sm text-[var(--duo-text)]">상점</h3>
              <p className="text-xs text-[var(--duo-text-secondary)] mt-1">
                ⭐ {userData.stars}개 보유
              </p>
            </div>
          </Link>
        </div>

        {/* Learning Tips */}
        <div className="mb-20">
          <h2 className="text-lg font-bold text-[var(--duo-text)] mb-3">학습 팁</h2>
          <div className="duo-card p-4 mb-3 bg-gradient-to-br from-blue-50 to-cyan-50">
            <div className="flex gap-3">
              <div className="text-2xl">💡</div>
              <div>
                <h4 className="font-bold text-sm text-[var(--duo-text)] mb-1">매일 조금씩!</h4>
                <p className="text-xs text-[var(--duo-text-secondary)]">
                  하루 10분씩 꾸준히 학습하는 것이 한 번에 몰아서 하는 것보다 효과적이에요.
                </p>
              </div>
            </div>
          </div>
          <div className="duo-card p-4 bg-gradient-to-br from-green-50 to-emerald-50">
            <div className="flex gap-3">
              <div className="text-2xl">🎤</div>
              <div>
                <h4 className="font-bold text-sm text-[var(--duo-text)] mb-1">큰 소리로 따라 말해보세요!</h4>
                <p className="text-xs text-[var(--duo-text-secondary)]">
                  발음 연습은 큰 소리로 자신있게 말하는 것이 중요해요.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNav />
      
      {/* Daily Bonus Modal */}
      <DailyBonusModal
        isOpen={showBonusModal}
        onClose={() => setShowBonusModal(false)}
        reward={bonusReward}
      />
      
      {/* Onboarding Tutorial */}
      <OnboardingTutorial
        isOpen={showOnboarding}
        onComplete={handleCompleteOnboarding}
        onSkip={handleSkipOnboarding}
      />
    </div>
  );
}
