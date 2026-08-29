 * MissionResult Page
 * Design Philosophy: Encouraging feedback for both success and failure
 * - Success: Celebration with rewards display
 * - Failure: Gentle encouragement without harsh red colors
 */

import { useEffect } from "react";
import { useRoute, useLocation } from "wouter";
import { Star, TrendingUp, Home, RotateCcw } from "lucide-react";
import { missions } from "@/lib/mockData";
import { trpc } from "@/lib/trpc";
import { toast } from "sonner";

export default function MissionResult() {
  const [, params] = useRoute("/mission/:id/result");
  const [, setLocation] = useLocation();
  
  const mission = missions.find((m) => m.id === Number(params?.id));
  
  // Get URL params
  const urlParams = new URLSearchParams(window.location.search);
  const isSuccess = urlParams.get("success") === "true";
  const stars = Number(urlParams.get("stars")) || mission?.rewards.stars || 0;
  const xp = Number(urlParams.get("xp")) || mission?.rewards.xp || 0;
  
  const utils = trpc.useUtils();
  
  const completeMission = trpc.missions.updateStatus.useMutation({
    onMutate: async (variables) => {
      // Cancel any outgoing refetches
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
    
    // Update weekly goals if mission was successful
    if (isSuccess && mission) {
      completeMission.mutate({
        missionId: mission.id,
        status: "completed",
        score: 100,
        earnedXp: xp,
      });
    }
  }, [isSuccess, mission?.id]);

  if (!mission) {
    return (
      <div className="min-h-screen bg-[var(--duo-bg)] flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🔍</div>
          <p className="text-[var(--duo-text-secondary)]">미션을 찾을 수 없습니다</p>
          <button
            onClick={() => setLocation("/missions")}
            className="mt-4 duo-btn-primary"
          >
            미션 목록으로
          </button>
        </div>
      </div>
    );
  }

  if (isSuccess) {
    return (