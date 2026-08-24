/**
 * Profile Page - Mobile Optimized (No Header)
 * Design Philosophy: Simple profile overview with progress stats
 * - Removed detailed charts (moved to Skills page)
 * - Focused on daily streak and overall progress
 */

import { Link, useNavigate } from "react-router-dom";
import { Settings, Award, Edit2, X, Check, Users, ArrowLeftRight } from "lucide-react";
import { useProfile } from "@/api/hooks/useProfile";
import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateAvatar } from "@/api/client";
import { toast } from "sonner";

export default function KidProfile() {
    const { data: profile, isLoading } = useProfile();
    const { logoutChild } = useAuth();
    const navigate = useNavigate();
    const [isEditingAvatar, setIsEditingAvatar] = useState(false);
    const queryClient = useQueryClient();

    const updateAvatarMutation = useMutation({
        mutationFn: updateAvatar,
        onSuccess: () => {
            toast.success("아바타가 변경되었어요! 🎉");
            setIsEditingAvatar(false);
            queryClient.invalidateQueries({ queryKey: ['profile'] });
            // Optimistic update or refetch
        },
        onError: () => {
            toast.error("아바타 변경에 실패했어요. 😢");
        }
    });

    if (isLoading || !profile) {
        return <div className="h-full flex items-center justify-center">Loading...</div>;
    }

    // Weekly progress mock data (last 7 days)
    const today = new Date();
    const getDayName = (date: Date) => {
        const days = ['일', '월', '화', '수', '목', '금', '토'];
        return days[date.getDay()];
    };

    const weeklyProgress = Array.from({ length: 7 }).map((_, i) => {
        const d = new Date(today);
        d.setDate(d.getDate() - (6 - i));
        return {
            day: getDayName(d),
            // Random mock minutes for visual effect
            minutes: Math.floor(Math.random() * 30) + (i === 6 ? 15 : 5),
        };
    });

    return (
        <div className="h-full flex flex-col bg-[var(--bt-bg)] overflow-hidden relative">
            {/* Top Section with Settings */}
            <div className="p-4 flex justify-between items-center bg-white shadow-sm">
                <h1 className="text-xl font-bold text-[var(--bt-text)]">내 프로필</h1>
                <Link to="/settings" className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                    <Settings className="w-6 h-6 text-gray-400" />
                </Link>
            </div>

            {/* Scrollable Content */}
            <div className="flex-1 overflow-y-auto px-4 py-6 pb-24">
                {/* Profile Header */}
                <div className="flex flex-col items-center mb-8 relative">
                    <div className="relative group">
                        <div className="w-32 h-32 bg-purple-50 rounded-full flex items-center justify-center border-4 border-white shadow-lg overflow-visible">
                            {profile.avatarUrl ? (
                                <img
                                    src={profile.avatarUrl}
                                    alt="Profile Avatar"
                                    className="w-full h-full object-contain scale-110 drop-shadow-md"
                                />
                            ) : (
                                <span className="text-6xl">{profile.avatarEmoji || "🐰"}</span>
                            )}
                        </div>
                        <button
                            onClick={() => setIsEditingAvatar(true)}
                            className="absolute bottom-0 right-0 bg-blue-500 hover:bg-blue-600 text-white p-2.5 rounded-full shadow-md transition-transform hover:scale-110"
                        >
                            <Edit2 size={16} />
                        </button>
                    </div>

                    <h2 className="text-2xl font-bold text-[var(--bt-text)] mt-3 mb-1">
                        {profile.nickname}
                    </h2>
                    <div className="flex items-center gap-2 bg-yellow-100 px-3 py-1 rounded-full">
                        <span className="text-sm font-bold text-yellow-700">Lv.{profile.level}</span>
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="bt-card p-4 mb-4">
                    <h2 className="text-lg font-bold text-[var(--bt-text)] mb-3 flex items-center gap-2">
                        🏆 학습 통계
                    </h2>
                    <div className="grid grid-cols-2 gap-3">
                        <div className="text-center p-3 bg-red-50 rounded-xl">
                            <div className="text-2xl mb-1">🔥</div>
                            <div className="text-xl font-bold text-[var(--bt-text)]">
                                {profile.streak}일
                            </div>
                            <div className="text-xs text-[var(--bt-text-secondary)] mt-1">연속 학습</div>
                        </div>
                        <div className="text-center p-3 bg-blue-50 rounded-xl">
                            <div className="text-2xl mb-1">💎</div>
                            <div className="text-xl font-bold text-[var(--bt-text)]">
                                {profile.xp}
                            </div>
                            <div className="text-xs text-[var(--bt-text-secondary)] mt-1">총 XP</div>
                        </div>
                        <div className="text-center p-3 bg-green-50 rounded-xl">
                            <div className="text-2xl mb-1">📚</div>
                            <div className="text-xl font-bold text-[var(--bt-text)]">
                                {profile.stats.vocabularyLearned}
                            </div>
                            <div className="text-xs text-[var(--bt-text-secondary)] mt-1">학습 단어</div>
                        </div>
                        <div className="text-center p-3 bg-yellow-50 rounded-xl">
                            <Award size={20} className="text-[var(--bt-accent)] mx-auto mb-1" />
                            <div className="text-xl font-bold text-[var(--bt-text)]">
                                {profile.stats.pronunciationAccuracy}%
                            </div>
                            <div className="text-xs text-[var(--bt-text-secondary)] mt-1">발음 정확도</div>
                        </div>
                    </div>
                </div>

                {/* Switch Actions */}
                <div className="bt-card p-4 mb-4">
                    <h2 className="text-lg font-bold text-[var(--bt-text)] mb-3 flex items-center gap-2">
                        <Settings size={18} /> 설정
                    </h2>
                    <div className="flex flex-col gap-2">
                        <button
                            onClick={() => { logoutChild(); navigate('/select-child'); }}
                            className="flex items-center gap-3 w-full p-3 rounded-xl hover:bg-gray-50 active:scale-[0.98] transition-all text-left"
                        >
                            <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center">
                                <Users size={18} className="text-blue-500" />
                            </div>
                            <div>
                                <div className="font-bold text-sm text-[var(--bt-text)]">프로필 전환</div>
                                <div className="text-xs text-[var(--bt-text-secondary)]">다른 아이 프로필로 전환해요</div>
                            </div>
                        </button>
                        <button
                            onClick={() => navigate('/mode-select')}
                            className="flex items-center gap-3 w-full p-3 rounded-xl hover:bg-gray-50 active:scale-[0.98] transition-all text-left"
                        >
                            <div className="w-10 h-10 rounded-full bg-purple-50 flex items-center justify-center">
                                <ArrowLeftRight size={18} className="text-purple-500" />
                            </div>
                            <div>
                                <div className="font-bold text-sm text-[var(--bt-text)]">모드 전환</div>
                                <div className="text-xs text-[var(--bt-text-secondary)]">부모 모드로 전환해요</div>
                            </div>
                        </button>
                    </div>
                </div>

                {/* Weekly Progress */}
                <div className="bt-card p-4 mb-20">
                    <h2 className="text-lg font-bold text-[var(--bt-text)] mb-3 flex items-center gap-2">
                        📈 주간 학습량
                    </h2>
                    <div className="flex items-end justify-between gap-2 h-28">
                        {weeklyProgress.map((day, index) => {
                            const maxMinutes = Math.max(...weeklyProgress.map(d => d.minutes));
                            const height = (day.minutes / maxMinutes) * 100;
                            const isToday = index === 6;

                            return (
                                <div key={day.day} className="flex-1 flex flex-col items-center gap-2">
                                    <div className="flex-1 flex items-end w-full">
                                        <div
                                            className={`w-full rounded-t-lg transition-all ${isToday ? "bg-[var(--bt-primary)]" : "bg-blue-200"
                                                }`}
                                            style={{ height: `${height}%` }}
                                        />
                                    </div>
                                    <span className="text-xs font-semibold text-[var(--bt-text-secondary)]">
                                        {day.day}
                                    </span>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* Avatar Selection Modal */}
            {isEditingAvatar && (
                <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/50 p-0 sm:p-4 animate-in fade-in duration-200">
                    <div className="bg-white rounded-t-2xl sm:rounded-2xl w-full max-w-sm max-h-[85vh] flex flex-col shadow-2xl animate-in slide-in-from-bottom duration-300">
                        <div className="p-4 border-b flex justify-between items-center">
                            <h3 className="text-lg font-bold">캐릭터 선택</h3>
                            <button onClick={() => setIsEditingAvatar(false)} className="p-2 hover:bg-gray-100 rounded-full">
                                <X size={20} />
                            </button>
                        </div>

                        <div className="p-4 overflow-y-auto grid grid-cols-2 gap-3">
                            {profile.availableAvatars?.map((avatar) => (
                                <button
                                    key={avatar.id}
                                    onClick={() => updateAvatarMutation.mutate(avatar.id)}
                                    disabled={updateAvatarMutation.isPending}
                                    className={`relative p-4 rounded-xl border-2 transition-all flex flex-col items-center gap-2 group
                                        ${profile.avatarId === avatar.id
                                            ? "border-blue-500 bg-blue-50 ring-2 ring-blue-200"
                                            : "border-gray-100 hover:border-blue-200 hover:bg-gray-50"
                                        }
                                    `}
                                >
                                    <img
                                        src={avatar.image}
                                        alt={avatar.name}
                                        className="w-20 h-20 object-contain drop-shadow transition-transform group-hover:scale-110"
                                    />
                                    <span className={`text-sm font-bold ${profile.avatarId === avatar.id ? "text-blue-600" : "text-gray-600"}`}>
                                        {avatar.name}
                                    </span>
                                    {profile.avatarId === avatar.id && (
                                        <div className="absolute top-2 right-2 bg-blue-500 text-white rounded-full p-0.5">
                                            <Check size={12} strokeWidth={3} />
                                        </div>
                                    )}
                                    {updateAvatarMutation.isPending && updateAvatarMutation.variables === avatar.id && (
                                        <div className="absolute inset-0 bg-white/50 flex items-center justify-center rounded-xl">
                                            <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                                        </div>
                                    )}
                                </button>
                            ))}
                        </div>

                        <div className="p-4 border-t bg-gray-50 rounded-b-2xl">
                            <button
                                onClick={() => setIsEditingAvatar(false)}
                                className="w-full py-3 bg-[var(--bt-bg)] hover:brightness-95 text-[var(--bt-text)] font-bold rounded-xl transition-all"
                            >
                                닫기
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
