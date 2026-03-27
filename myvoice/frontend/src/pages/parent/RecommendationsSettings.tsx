/**
 * Recommendations & Settings — Wireframe #12
 * Recommended activities, subscription management, app settings
 */
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { parentApi } from "@/api/client";
import type { ChildProfile } from "@/api/types";
import { useAuth } from "@/contexts/AuthContext";
import {
    Sparkles,
    CreditCard,
    Bell,
    Shield,
    LogOut,
    ChevronRight,
    User,
    Moon,
    Volume2,
    Clock,
    Loader2,
    ArrowRightLeft,
} from "lucide-react";

interface RecommendedActivity {
    id: string;
    emoji: string;
    title: string;
    description: string;
    tag: string;
}

const SAMPLE_ACTIVITIES: RecommendedActivity[] = [
    {
        id: "1",
        emoji: "🎨",
        title: "색깔 모험",
        description: "영어로 다양한 색깔을 배워요!",
        tag: "어휘",
    },
    {
        id: "2",
        emoji: "🐾",
        title: "동물 친구들",
        description: "동물 이름을 영어로 말해봐요",
        tag: "발음",
    },
    {
        id: "3",
        emoji: "🎵",
        title: "노래로 배우기",
        description: "영어 동요와 함께 즐겁게!",
        tag: "듣기",
    },
];

export default function RecommendationsSettings() {
    const navigate = useNavigate();
    const { logoutParent } = useAuth();
    const [children, setChildren] = useState<ChildProfile[]>([]);
    const [selectedChild, setSelectedChild] = useState<ChildProfile | null>(null);
    const [notifications, setNotifications] = useState(true);
    const [dailyReminder, setDailyReminder] = useState(true);
    const [soundEffects, setSoundEffects] = useState(true);

    useEffect(() => {
        (async () => {
            try {
                const data = await parentApi.listChildren();
                setChildren(data);
                if (data.length > 0) setSelectedChild(data[0]);
            } catch {
                // silently fail
            }
        })();
    }, []);

    const handleLogout = () => {
        logoutParent();
        navigate("/");
    };

    if (!selectedChild) {
        return (
            <div className="flex items-center justify-center h-64">
                <Loader2 className="w-6 h-6 animate-spin text-[var(--bt-primary)]" />
            </div>
        );
    }

    return (
        <div className="p-4 pb-24 max-w-2xl mx-auto space-y-5">
            {/* Header */}
            <div>
                <h1 className="text-xl font-bold text-[var(--bt-text)]">추천 & 설정</h1>
                <p className="text-sm text-[var(--bt-text-secondary)] mt-0.5">
                    맞춤 추천 활동과 앱 설정을 관리하세요
                </p>
            </div>

            {/* Recommended Activities */}
            <section>
                <div className="flex items-center gap-2 mb-3">
                    <Sparkles size={18} className="text-[var(--bt-primary)]" />
                    <h2 className="font-bold text-[var(--bt-text)]">추천 활동</h2>
                </div>
                <div className="space-y-3">
                    {SAMPLE_ACTIVITIES.map((act) => (
                        <div
                            key={act.id}
                            className="bt-card p-4 flex items-center gap-3"
                        >
                            <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center text-2xl flex-shrink-0">
                                {act.emoji}
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2">
                                    <h3 className="font-bold text-sm text-[var(--bt-text)]">{act.title}</h3>
                                    <span className="text-[10px] font-semibold bg-[var(--bt-primary)]/10 text-[var(--bt-primary)] px-1.5 py-0.5 rounded-full">
                                        {act.tag}
                                    </span>
                                </div>
                                <p className="text-xs text-[var(--bt-text-secondary)] mt-0.5">{act.description}</p>
                            </div>
                            <ChevronRight size={16} className="text-[var(--bt-text-muted)] flex-shrink-0" />
                        </div>
                    ))}
                </div>
            </section>

            {/* Child Profiles */}
            <section>
                <div className="flex items-center gap-2 mb-3">
                    <User size={18} className="text-[var(--bt-primary)]" />
                    <h2 className="font-bold text-[var(--bt-text)]">아이 프로필</h2>
                </div>
                <div className="space-y-2">
                    {children.map((child) => (
                        <button
                            key={child.childId}
                            onClick={() => navigate(`/parent/children/${child.childId}`)}
                            className="w-full bt-card p-3 flex items-center justify-between"
                        >
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center">
                                    <span className="text-lg">{child.avatarEmoji || "👧"}</span>
                                </div>
                                <div className="text-left">
                                    <p className="font-semibold text-sm text-[var(--bt-text)]">{child.name}</p>
                                    <p className="text-xs text-[var(--bt-text-secondary)]">
                                        Lv.{child.level} · {child.xp} XP
                                    </p>
                                </div>
                            </div>
                            <ChevronRight size={16} className="text-[var(--bt-text-muted)]" />
                        </button>
                    ))}
                </div>
            </section>

            {/* Subscription */}
            <section>
                <div className="flex items-center gap-2 mb-3">
                    <CreditCard size={18} className="text-[var(--bt-primary)]" />
                    <h2 className="font-bold text-[var(--bt-text)]">구독 관리</h2>
                </div>
                <div className="bt-card p-4">
                    <div className="flex items-center justify-between mb-2">
                        <div>
                            <p className="font-bold text-sm text-[var(--bt-text)]">무료 체험</p>
                            <p className="text-xs text-[var(--bt-text-secondary)]">기본 기능 이용 가능</p>
                        </div>
                        <span className="text-xs font-semibold bg-green-100 text-green-700 px-2 py-0.5 rounded-full">
                            활성
                        </span>
                    </div>
                    <button className="w-full mt-2 py-2.5 rounded-xl bg-[var(--bt-primary)] text-white font-bold text-sm">
                        프리미엄 업그레이드
                    </button>
                </div>
            </section>

            {/* App Settings */}
            <section>
                <h2 className="font-bold text-[var(--bt-text)] mb-3">앱 설정</h2>
                <div className="bt-card divide-y divide-[var(--bt-border)]">
                    <ToggleSetting
                        icon={<Bell size={18} />}
                        label="알림"
                        description="학습 알림 및 리포트 알림"
                        value={notifications}
                        onChange={setNotifications}
                    />
                    <ToggleSetting
                        icon={<Clock size={18} />}
                        label="일일 학습 리마인더"
                        description="매일 정해진 시간에 알림"
                        value={dailyReminder}
                        onChange={setDailyReminder}
                    />
                    <ToggleSetting
                        icon={<Volume2 size={18} />}
                        label="사운드 효과"
                        description="앱 내 효과음"
                        value={soundEffects}
                        onChange={setSoundEffects}
                    />
                    <NavSetting
                        icon={<Moon size={18} />}
                        label="다크 모드"
                        description="곧 지원 예정"
                    />
                    <NavSetting
                        icon={<Shield size={18} />}
                        label="개인정보 처리방침"
                        description=""
                    />
                </div>
            </section>

            {/* Mode Switch */}
            <button
                onClick={() => navigate("/mode-select")}
                className="w-full bt-card p-4 flex items-center justify-center gap-2 text-[var(--bt-primary)] font-semibold"
            >
                <ArrowRightLeft size={18} />
                아이 모드로 전환
            </button>

            {/* Logout */}
            <button
                onClick={handleLogout}
                className="w-full bt-card p-4 flex items-center justify-center gap-2 text-red-500 font-semibold"
            >
                <LogOut size={18} />
                로그아웃
            </button>
        </div>
    );
}

function ToggleSetting({
    icon,
    label,
    description,
    value,
    onChange,
}: {
    icon: React.ReactNode;
    label: string;
    description: string;
    value: boolean;
    onChange: (v: boolean) => void;
}) {
    return (
        <div className="flex items-center justify-between p-4">
            <div className="flex items-center gap-3">
                <span className="text-[var(--bt-text-muted)]">{icon}</span>
                <div>
                    <p className="text-sm font-semibold text-[var(--bt-text)]">{label}</p>
                    {description && (
                        <p className="text-xs text-[var(--bt-text-secondary)]">{description}</p>
                    )}
                </div>
            </div>
            <button
                onClick={() => onChange(!value)}
                className={`w-11 h-6 rounded-full transition-colors relative ${
                    value ? "bg-[var(--bt-primary)]" : "bg-gray-300"
                }`}
            >
                <span
                    className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${
                        value ? "translate-x-5" : "translate-x-0.5"
                    }`}
                />
            </button>
        </div>
    );
}

function NavSetting({
    icon,
    label,
    description,
}: {
    icon: React.ReactNode;
    label: string;
    description: string;
}) {
    return (
        <div className="flex items-center justify-between p-4">
            <div className="flex items-center gap-3">
                <span className="text-[var(--bt-text-muted)]">{icon}</span>
                <div>
                    <p className="text-sm font-semibold text-[var(--bt-text)]">{label}</p>
                    {description && (
                        <p className="text-xs text-[var(--bt-text-secondary)]">{description}</p>
                    )}
                </div>
            </div>
            <ChevronRight size={16} className="text-[var(--bt-text-muted)]" />
        </div>
    );
}
