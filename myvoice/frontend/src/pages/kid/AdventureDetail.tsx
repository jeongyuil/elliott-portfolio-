/**
 * Adventure Detail Page
 * Entry point for an adventure. Shows description and start button.
 */

import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Star, Clock, Trophy } from "lucide-react";
import { useAdventureDetail } from "@/api/hooks/useAdventureDetail";

export default function AdventureDetail() {
    const { id } = useParams();
    const navigate = useNavigate();

    const { data: adventure, isLoading, error } = useAdventureDetail(id!);

    if (isLoading) {
        return (
            <div className="h-full flex items-center justify-center bg-[var(--bt-bg)]">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--bt-primary)]"></div>
            </div>
        );
    }

    if (error || !adventure) {
        return (
            <div className="h-full flex items-center justify-center p-4 bg-[var(--bt-bg)]">
                <div className="text-center">
                    <h2 className="text-xl font-bold mb-2 text-[var(--bt-text)]">모험을 찾을 수 없습니다</h2>
                    <p className="text-[var(--bt-text-secondary)] mb-4">다시 시도해주세요.</p>
                    <button
                        onClick={() => navigate('/kid/adventures')}
                        className="text-[var(--bt-accent)] font-bold hover:underline"
                    >
                        목록으로 돌아가기
                    </button>
                </div>
            </div>
        );
    }

    const handleStartAdventure = () => {
        navigate(`/kid/adventure/${id}/play`);
    };

    // Difficulty mapping
    let difficultyClass = "medium";
    if (adventure.difficulty === "쉬움") difficultyClass = "easy";
    else if (adventure.difficulty === "어려움") difficultyClass = "hard";

    return (
        <div className="h-full flex flex-col bg-[var(--bt-bg)]">
            {/* Header */}
            <div className="bg-white shadow-sm p-4 relative z-10">
                <div className="flex items-center gap-3">
                    <button onClick={() => navigate('/kid/adventures')} className="p-1 hover:bg-gray-100 rounded-full transition-colors">
                        <ArrowLeft size={24} className="text-[var(--bt-text)]" />
                    </button>
                    <h1 className="text-lg font-bold text-[var(--bt-text)]">모험 상세</h1>
                </div>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4 pb-24">
                {/* Mission Hero */}
                <div className="bt-card p-6 mb-4 text-center">
                    <div className="text-8xl mb-4 animate-bounce">{adventure.emoji}</div>
                    <h2 className="text-2xl font-bold text-[var(--bt-text)] mb-2">{adventure.title}</h2>
                    <span className={`bt-badge ${difficultyClass} text-sm px-3 py-1`}>{adventure.difficulty}</span>
                </div>

                {/* Mission Info */}
                <div className="bt-card p-4 mb-4">
                    <h3 className="font-bold text-[var(--bt-text)] mb-3">모험 정보</h3>
                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2 text-[var(--bt-text-secondary)]">
                                <Clock size={18} />
                                <span>소요 시간</span>
                            </div>
                            <span className="font-bold text-[var(--bt-text)]">{adventure.duration ? Math.floor(adventure.duration / 60) : 5}분</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2 text-[var(--bt-text-secondary)]">
                                <Star size={18} className="text-yellow-500" fill="currentColor" />
                                <span className="text-[var(--bt-text-secondary)]">별 보상</span>
                            </div>
                            <span className="font-bold text-[var(--bt-text)]">+{adventure.rewards?.stars || 0}</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2 text-[var(--bt-text-secondary)]">
                                <Trophy size={18} className="text-blue-500" />
                                <span className="text-[var(--bt-text-secondary)]">XP 보상</span>
                            </div>
                            <span className="font-bold text-[var(--bt-text)]">+{adventure.rewards?.xp || 0}</span>
                        </div>
                    </div>
                </div>

                {/* Activities Preview (Optional) */}
                {adventure.activities && adventure.activities.length > 0 && (
                    <div className="bt-card p-4 mb-4">
                        <h3 className="font-bold text-[var(--bt-text)] mb-3">활동 목록</h3>
                        <ul className="space-y-2">
                            {adventure.activities.map((act, idx) => (
                                <li key={act.activityId} className="flex items-center gap-2 text-sm text-[var(--bt-text-secondary)]">
                                    <span className="w-5 h-5 rounded-full bg-[var(--bt-accent)] text-white flex items-center justify-center text-xs font-bold">
                                        {idx + 1}
                                    </span>
                                    <span>{act.name}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Mission Description */}
                <div className="bt-card p-4 mb-6">
                    <h3 className="font-bold text-[var(--bt-text)] mb-2">모험 설명</h3>
                    <p className="text-[var(--bt-text-secondary)] leading-relaxed">{adventure.description}</p>
                </div>

                {/* Start Button */}
                <button
                    onClick={handleStartAdventure}
                    className="w-full bg-[var(--bt-primary)] hover:bg-[#58cc02] active:translate-y-1 active:shadow-none text-white font-bold py-4 rounded-xl text-lg shadow-[0_4px_0_#58cc02] transition-all"
                >
                    모험 시작하기
                </button>
            </div>
        </div>
    );
}
