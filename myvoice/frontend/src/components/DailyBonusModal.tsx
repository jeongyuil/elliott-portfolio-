import { Dialog, DialogContent, DialogTitle, DialogDescription } from "@radix-ui/react-dialog";
import { Gift, Star, Flame, X } from "lucide-react";
import { useEffect, useState } from "react";

interface DailyBonusModalProps {
    isOpen: boolean;
    onClose: () => void;
    reward: {
        starsReward: number;
        consecutiveDays: number;
        newStars: number;
        newStreak: number;
    } | null;
}

export default function DailyBonusModal({ isOpen, onClose, reward }: DailyBonusModalProps) {
    const [showRewards, setShowRewards] = useState(false);

    useEffect(() => {
        if (isOpen && reward) {
            const timer = setTimeout(() => setShowRewards(true), 300);
            return () => clearTimeout(timer);
        } else {
            setShowRewards(false);
        }
    }, [isOpen, reward]);

    if (!reward || !isOpen) return null;

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <div className="fixed inset-0 z-50 bg-black/50" aria-hidden="true" />
            <DialogContent className="fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-0 shadow-lg duration-200 sm:rounded-lg">
                <div className="bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 border-2 border-purple-200 rounded-lg overflow-hidden">
                    <DialogTitle className="sr-only">일일 로그인 보너스</DialogTitle>
                    <DialogDescription className="sr-only">
                        {reward.consecutiveDays}일 연속 로그인 달성! 별 {reward.starsReward}개를 획득했습니다.
                    </DialogDescription>

                    <div className="flex flex-col items-center gap-6 py-6 px-6 relative">
                        <button
                            onClick={onClose}
                            className="absolute top-4 right-4 p-2 rounded-full hover:bg-black/5 transition-colors"
                        >
                            <X size={20} className="text-gray-500" />
                        </button>

                        {/* Header */}
                        <div className="text-center mt-4">
                            <div className="flex items-center justify-center gap-2 mb-2">
                                <Gift className="w-8 h-8 text-purple-600" />
                                <h2 className="text-2xl font-bold text-purple-900">일일 로그인 보너스!</h2>
                            </div>
                            <p className="text-sm text-purple-700">
                                {reward.consecutiveDays}일 연속 로그인 달성!
                            </p>
                        </div>

                        {/* Streak Display */}
                        <div className="flex items-center gap-2 bg-white/80 px-6 py-3 rounded-full shadow-lg">
                            <Flame className="w-6 h-6 text-orange-500" fill="currentColor" />
                            <span className="text-xl font-bold text-orange-600">
                                {reward.consecutiveDays}일 연속
                            </span>
                        </div>

                        {/* Stars Reward */}
                        <div className="w-full">
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
                        </div>

                        {/* Next Day Preview */}
                        <div className="w-full bg-purple-100/50 p-4 rounded-xl border border-purple-200">
                            <p className="text-center text-sm text-purple-700">
                                내일도 로그인하면 더 많은 별을 받을 수 있어요!
                            </p>
                            <p className="text-center text-xs text-purple-600 mt-1">
                                {reward.consecutiveDays < 7
                                    ? `${reward.consecutiveDays + 1}일 연속 시 별 ${Math.min(50 + (reward.consecutiveDays + 1) * 10, 100)}개`
                                    : "최대 보상을 받고 있습니다!"}
                            </p>
                        </div>

                        {/* Close Button */}
                        <button
                            onClick={onClose}
                            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold py-4 rounded-xl text-lg shadow-lg transition-transform active:scale-95"
                        >
                            확인
                        </button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    );
}
