import { Dialog, DialogContent, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Gift, Star, Heart, Flame } from "lucide-react";
import { useEffect, useState } from "react";

interface DailyBonusModalProps {
  isOpen: boolean;
  onClose: () => void;
  reward: {
    starsReward: number;
    heartsReward: number;
    consecutiveDays: number;
    newStars: number;
    newHearts: number;
    newStreak: number;
  } | null;
}

export default function DailyBonusModal({ isOpen, onClose, reward }: DailyBonusModalProps) {
  const [showRewards, setShowRewards] = useState(false);

  useEffect(() => {
    if (isOpen && reward) {
      // Delay showing rewards for animation effect
      const timer = setTimeout(() => setShowRewards(true), 300);
      return () => clearTimeout(timer);
    } else {
      setShowRewards(false);
    }
  }, [isOpen, reward]);

  if (!reward) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 border-2 border-purple-200">
        {/* Hidden DialogTitle and DialogDescription for accessibility */}
        <DialogTitle className="sr-only">일일 로그인 보너스</DialogTitle>
        <DialogDescription className="sr-only">
          {reward.consecutiveDays}일 연속 로그인 달성! 별 {reward.starsReward}개와 하트 {reward.heartsReward}개를 획득했습니다.
        </DialogDescription>
        
        <div className="flex flex-col items-center gap-6 py-6">
          {/* Header */}
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              <Gift className="w-8 h-8 text-purple-600" />
              <h2 className="text-2xl font-bold text-purple-900">일일 로그인 보너스!</h2>
            </div>
            <p className="text-sm text-purple-700">
              {reward.consecutiveDays}일 연속 로그인 달성! 🎉
            </p>
          </div>

          {/* Streak Display */}
          <div className="flex items-center gap-2 bg-white/80 px-6 py-3 rounded-full shadow-lg">
            <Flame className="w-6 h-6 text-orange-500" fill="currentColor" />
            <span className="text-xl font-bold text-orange-600">
              {reward.consecutiveDays}일 연속
            </span>
          </div>

          {/* Rewards Display */}
          <div className="w-full space-y-4">
            {/* Stars Reward */}
            <div
              className={`
                flex items-center justify-between bg-white/90 p-4 rounded-xl shadow-md
                transition-all duration-500 transform
                ${showRewards ? "translate-x-0 opacity-100" : "-translate-x-full opacity-0"}
              `}
            >
              <div className="flex items-center gap-3">
                <div className="bg-yellow-100 p-2 rounded-lg">
                  <Star className="w-6 h-6 text-yellow-500" fill="currentColor" />
                </div>
                <span className="font-semibold text-gray-700">별 획득</span>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-yellow-600">+{reward.starsReward}</div>
                <div className="text-xs text-gray-500">총 {reward.newStars}개</div>
              </div>
            </div>

            {/* Hearts Reward */}
            <div
              className={`
                flex items-center justify-between bg-white/90 p-4 rounded-xl shadow-md
                transition-all duration-500 transform delay-100
                ${showRewards ? "translate-x-0 opacity-100" : "-translate-x-full opacity-0"}
              `}
            >
              <div className="flex items-center gap-3">
                <div className="bg-red-100 p-2 rounded-lg">
                  <Heart className="w-6 h-6 text-red-500" fill="currentColor" />
                </div>
                <span className="font-semibold text-gray-700">하트 회복</span>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-red-600">+{reward.heartsReward}</div>
                <div className="text-xs text-gray-500">총 {reward.newHearts}개</div>
              </div>
            </div>
          </div>

          {/* Next Day Preview */}
          <div className="w-full bg-purple-100/50 p-4 rounded-xl border border-purple-200">
            <p className="text-center text-sm text-purple-700">
              내일도 로그인하면 더 많은 보상을 받을 수 있어요! 🎁
            </p>
            <p className="text-center text-xs text-purple-600 mt-1">
              {reward.consecutiveDays < 7 
                ? `${reward.consecutiveDays + 1}일 연속 로그인 시 보상이 증가합니다`
                : "최대 보상을 받고 있습니다!"}
            </p>
          </div>

          {/* Close Button */}
          <Button
            onClick={onClose}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold py-6 text-lg shadow-lg"
          >
            확인
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
