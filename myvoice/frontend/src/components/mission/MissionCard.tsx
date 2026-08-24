/**
 * MissionCard Component - Fully Responsive
 */

import { Link } from "react-router-dom";
import { Star, Clock } from "lucide-react";

interface MissionCardProps {
    id: number;
    title: string;
    emoji: string;
    difficulty: "쉬움" | "보통" | "어려움";
    duration: number;
    rewards: {
        stars: number;
        xp: number;
    };
    completed?: boolean;
    earnedStars?: number;
    earnedXp?: number;
}

export default function MissionCard({ id, title, emoji, difficulty, duration, rewards, completed = false, earnedStars }: MissionCardProps) {
    const difficultyClass = difficulty === "쉬움" ? "easy" : difficulty === "보통" ? "medium" : "hard";

    return (
        <Link to={`/kid/adventure/${id}`}>
            <div className={`bt-mission-card w-full hover:scale-[1.02] transition-transform duration-200 ${completed ? 'grayscale opacity-60' : ''}`}>
                <div className="relative">
                    <div className="flex items-center justify-center h-24 bg-gradient-to-br from-blue-50 to-purple-50">
                        <span className="text-5xl">{emoji}</span>
                    </div>
                    <div className="absolute top-2 right-2">
                        {completed ? (
                            <span className="bg-gray-700 text-white text-[14px] px-2 py-1 rounded font-medium shadow-sm">모험완료</span>
                        ) : (
                            <span className={`bt-badge ${difficultyClass} text-xs px-2 py-1`}>{difficulty}</span>
                        )}
                    </div>
                </div>
                <div className="p-3">
                    <h3 className="font-bold text-sm mb-2 text-[var(--bt-text)] line-clamp-2">{title}</h3>
                    <div className="flex items-center justify-between text-xs text-[var(--bt-text-secondary)]">
                        <div className="flex items-center gap-1">
                            <Clock size={12} />
                            <span>{Math.floor(duration / 60)}분</span>
                        </div>
                        <div className="flex items-center gap-2">
                            {completed && earnedStars !== undefined ? (
                                <div className="flex items-center gap-1 bg-gradient-to-r from-green-500 to-emerald-500 text-white px-2 py-1 rounded-full font-bold text-xs shadow-lg animate-in slide-in-from-right duration-300">
                                    <Star size={12} fill="currentColor" className="animate-pulse" />
                                    <span>+{earnedStars}</span>
                                </div>
                            ) : (
                                <div className="flex items-center gap-1">
                                    <Star size={12} className="bt-star" fill="currentColor" />
                                    <span className="font-bold">+{rewards.stars}</span>
                                </div>
                            )}
                        </div>
                    </div>

                </div>
            </div>
        </Link>
    );
}
