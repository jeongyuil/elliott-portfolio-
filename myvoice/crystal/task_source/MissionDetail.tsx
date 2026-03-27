/**
 * Mission Detail Page - With Optimistic Weekly Goals Update
 * When user completes a mission, weekly goals are updated immediately
 */

import { useParams, useLocation } from "wouter";
import { ArrowLeft, Star, Clock, Trophy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { trpc } from "@/lib/trpc";
import { toast } from "sonner";
import { useState } from "react";

export default function MissionDetail() {
  const params = useParams();
  const [, setLocation] = useLocation();
  const missionId = params.id ? parseInt(params.id) : 0;
  const [isCompleting, setIsCompleting] = useState(false);
  
  const utils = trpc.useUtils();
  
  // Fetch mission details (mock for now, can be replaced with real API)
  const mission = {
    id: missionId,
    title: "Luna is Hungry!",
    emoji: "🍎",
    difficulty: "쉬움",
    duration: 180, // 3 minutes in seconds
    rewards: {
      stars: 10,
      xp: 50,
    },
    description: "Help Luna order food at a restaurant. Practice basic food vocabulary and ordering phrases.",
  };
  
  const completeMission = trpc.missions.updateStatus.useMutation({
    onMutate: async (variables) => {
      // Cancel any outgoing refetches to avoid overwriting optimistic update
      await utils.weeklyGoals.getCurrent.cancel();
      
      // Snapshot the previous value
      const previousGoals = utils.weeklyGoals.getCurrent.getData();
      
      // Optimistically update weekly goals
      if (previousGoals && variables.status === "completed") {
        utils.weeklyGoals.getCurrent.setData(undefined, {
          ...previousGoals,
          xpCurrent: previousGoals.xpCurrent + (variables.earnedXp || 0),
          missionsCurrent: previousGoals.missionsCurrent + 1,
        });
      }
      
      return { previousGoals };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousGoals) {
        utils.weeklyGoals.getCurrent.setData(undefined, context.previousGoals);
      }
      toast.error("미션 완료 처리에 실패했습니다.");
    },
    onSuccess: () => {
      toast.success("🎉 미션 완료! 주간 목표가 업데이트되었습니다!");
      setIsCompleting(false);
      
      // Navigate back to home after a short delay
      setTimeout(() => {
        setLocation("/");
      }, 1500);
    },
    onSettled: () => {
      // Refetch to ensure data is in sync with server
      utils.weeklyGoals.getCurrent.invalidate();
    },
  });
  
  const handleCompleteMission = () => {
    setIsCompleting(true);
    completeMission.mutate({
      missionId: mission.id,
      status: "completed",
      score: 100,
      earnedXp: mission.rewards.xp,
    });
  };
  
  return (
    <div className="h-screen flex flex-col bg-[var(--duo-bg)]">
      {/* Header */}
      <div className="bg-white shadow-sm p-4">
        <div className="flex items-center gap-3">
          <button onClick={() => setLocation("/")} className="p-1">
            <ArrowLeft size={24} className="text-[var(--duo-text)]" />
          </button>
          <h1 className="text-lg font-bold text-[var(--duo-text)]">미션 상세</h1>
        </div>
      </div>
      
      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        {/* Mission Hero */}
        <div className="duo-card p-6 mb-4 text-center">
          <div className="text-8xl mb-4">{mission.emoji}</div>
          <h2 className="text-2xl font-bold text-[var(--duo-text)] mb-2">{mission.title}</h2>
          <span className="duo-badge easy text-sm px-3 py-1">{mission.difficulty}</span>
        </div>
        
        {/* Mission Info */}
        <div className="duo-card p-4 mb-4">
          <h3 className="font-bold text-[var(--duo-text)] mb-3">미션 정보</h3>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-[var(--duo-text-secondary)]">
                <Clock size={18} />
                <span>소요 시간</span>
              </div>
              <span className="font-bold text-[var(--duo-text)]">{Math.floor(mission.duration / 60)}분</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-[var(--duo-text-secondary)]">
                <Star size={18} className="text-yellow-500" fill="currentColor" />
                <span>별 보상</span>
              </div>
              <span className="font-bold text-[var(--duo-text)]">+{mission.rewards.stars}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-[var(--duo-text-secondary)]">
                <Trophy size={18} className="text-blue-500" />
                <span>XP 보상</span>
              </div>
              <span className="font-bold text-[var(--duo-text)]">+{mission.rewards.xp}</span>
            </div>
          </div>
        </div>
        
        {/* Mission Description */}
        <div className="duo-card p-4 mb-4">
          <h3 className="font-bold text-[var(--duo-text)] mb-2">미션 설명</h3>
          <p className="text-[var(--duo-text-secondary)]">{mission.description}</p>
        </div>
        
        {/* Complete Button */}
        <Button
          onClick={handleCompleteMission}
          disabled={isCompleting}
          className="w-full bg-[var(--duo-green)] hover:bg-[var(--duo-green)]/90 text-white font-bold py-6 text-lg"
        >
          {isCompleting ? "완료 처리 중..." : "미션 완료하기"}
        </Button>
      </div>
    </div>
  );
}
