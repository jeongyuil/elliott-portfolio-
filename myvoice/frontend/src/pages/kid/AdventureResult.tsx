/**
 * Adventure Result Page
 * Shows the result of an adventure completion.
 */

import { useEffect } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";
import { Star, TrendingUp, Home, RotateCcw } from "lucide-react";

export default function AdventureResult() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const queryClient = useQueryClient();

    const isSuccess = searchParams.get("success") === "true";
    const stars = Number(searchParams.get("stars")) || 0;
    const xp = Number(searchParams.get("xp")) || 0;

    useEffect(() => {
        // Prevent back navigation to the play page
        window.history.pushState(null, "", window.location.href);
        const handler = () => {
            window.history.pushState(null, "", window.location.href);
        };
        window.addEventListener("popstate", handler);
        return () => window.removeEventListener("popstate", handler);
    }, []);

    // Success Screen
    if (isSuccess) {
        return (
            <div className="min-h-screen bg-[var(--bt-bg)] flex flex-col items-center justify-center p-6 relative overflow-hidden">
                {/* Background Effects */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob" />
                    <div className="absolute top-1/4 right-1/4 w-32 h-32 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000" />
                    <div className="absolute bottom-1/4 left-1/2 w-32 h-32 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000" />
                </div>

                <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full text-center relative z-10">
                    <div className="text-6xl mb-6 animate-bounce">🎉</div>

                    <h1 className="text-2xl font-bold text-[var(--bt-text)] mb-2">모험 성공!</h1>
                    <p className="text-[var(--bt-text-secondary)] mb-8">
                        참 잘했어요! 루나가 기뻐하고 있어요.
                    </p>

                    {/* Rewards */}
                    <div className="grid grid-cols-2 gap-4 mb-8">
                        <div className="bg-yellow-50 rounded-2xl p-4 border-2 border-yellow-200">
                            <div className="flex justify-center mb-2">
                                <Star size={32} className="text-yellow-500 fill-current animate-pulse" />
                            </div>
                            <div className="text-2xl font-bold text-yellow-600">+{stars}</div>
                            <div className="text-xs font-bold text-yellow-400 uppercase">Stars</div>
                        </div>

                        <div className="bg-blue-50 rounded-2xl p-4 border-2 border-blue-200">
                            <div className="flex justify-center mb-2">
                                <TrendingUp size={32} className="text-blue-500" />
                            </div>
                            <div className="text-2xl font-bold text-blue-600">+{xp}</div>
                            <div className="text-xs font-bold text-blue-400 uppercase">XP</div>
                        </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="space-y-3">
                        <button
                            onClick={() => {
                                queryClient.invalidateQueries({ queryKey: ['adventures'] });
                                navigate("/kid/adventures");
                            }}
                            className="w-full bg-[var(--bt-primary)] hover:bg-[#58cc02] text-white font-bold py-4 rounded-xl text-lg shadow-[0_4px_0_#58cc02] active:shadow-none active:translate-y-1 transition-all"
                        >
                            모험 목록으로
                        </button>

                        <button
                            onClick={() => navigate("/kid/home")}
                            className="w-full bg-white hover:bg-gray-50 text-[var(--bt-text-secondary)] font-bold py-4 rounded-xl text-lg border-2 border-gray-200 transition-colors flex items-center justify-center gap-2"
                        >
                            <Home size={20} />
                            <span>홈으로 돌아가기</span>
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    // Failure / Quit Screen
    return (
        <div className="min-h-screen bg-[var(--bt-bg)] flex flex-col items-center justify-center p-6">
            <div className="bg-white rounded-3xl shadow-xl p-8 max-w-md w-full text-center">
                <div className="text-6xl mb-6">😢</div>

                <h1 className="text-2xl font-bold text-[var(--bt-text)] mb-2">아쉬워요!</h1>
                <p className="text-[var(--bt-text-secondary)] mb-8">
                    다시 한 번 도전해볼까요?
                </p>

                {/* Action Buttons */}
                <div className="space-y-3">
                    <button
                        onClick={() => navigate(`/kid/adventure/${id}/play`)}
                        className="w-full bg-[var(--bt-accent)] hover:bg-[#1cb0f6] text-white font-bold py-4 rounded-xl text-lg shadow-[0_4px_0_#1899d6] active:shadow-none active:translate-y-1 transition-all flex items-center justify-center gap-2"
                    >
                        <RotateCcw size={20} />
                        <span>재도전하기</span>
                    </button>

                    <button
                        onClick={() => navigate("/kid/home")}
                        className="w-full bg-white hover:bg-gray-50 text-[var(--bt-text-secondary)] font-bold py-4 rounded-xl text-lg border-2 border-gray-200 transition-colors flex items-center justify-center gap-2"
                    >
                        <Home size={20} />
                        <span>홈으로 가기</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
