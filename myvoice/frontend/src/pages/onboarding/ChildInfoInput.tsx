import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Sparkles } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/api/client';
import { toast } from 'sonner';

const INTERESTS = [
    { id: 'space_science', label: '우주/과학', icon: '🚀' },
    { id: 'music_song', label: '음악/노래', icon: '🎵' },
    { id: 'art_craft', label: '미술/만들기', icon: '🎨' },
    { id: 'story_reading', label: '동화/독서', icon: '📖' },
    { id: 'animal_nature', label: '동물/자연', icon: '🌿' },
    { id: 'game_play', label: '게임/놀이', icon: '🎮' },
    { id: 'photo_video', label: '사진/영상', icon: '📸' },
    { id: 'magic_fantasy', label: '마법/판타지', icon: '✨' },
    { id: 'dinosaur', label: '공룡', icon: '🦕' },
] as const;

const MAX_INTERESTS = 5;

export default function ChildInfoInput() {
    const navigate = useNavigate();
    const { loginAsChild } = useAuth();
    const [name, setName] = useState('');
    const [age, setAge] = useState(5);
    const [gender, setGender] = useState<'m' | 'f' | null>(null);
    const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);

    const toggleInterest = (id: string) => {
        setSelectedInterests((prev) => {
            if (prev.includes(id)) return prev.filter((i) => i !== id);
            if (prev.length >= MAX_INTERESTS) return prev;
            return [...prev, id];
        });
    };

    const canSubmit = name.trim().length > 0 && gender !== null;

    const handleSubmit = async () => {
        if (!canSubmit) return;
        setLoading(true);
        try {
            // Create child profile
            const child = await api.post<{ childId: string }>('/v1/parent/children', {
                name: name.trim(),
                gender,
                age,
                interests: selectedInterests,
            });

            // Auto-select child
            const { childToken } = await api.post<{ childToken: string }>('/v1/auth/select-child', {
                childId: child.childId,
            });
            loginAsChild(childToken);

            sessionStorage.setItem('onboarding_child_done', 'true');
            navigate('/onboarding/setup');
        } catch {
            toast.error('아이 정보 저장에 실패했습니다. 다시 시도해 주세요.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[var(--bt-bg)]">
            {/* Header */}
            <div className="flex items-center px-4 py-4">
                <button onClick={() => navigate('/onboarding/setup')} className="p-2 -ml-2">
                    <ChevronLeft size={24} className="text-[var(--bt-text)]" />
                </button>
                <h1 className="text-lg font-bold text-[var(--bt-text)] ml-2">아이 정보 입력</h1>
            </div>

            <div className="px-6 pb-8">
                {/* Banner */}
                <div className="bt-card p-4 flex items-center gap-3 mb-8">
                    <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center flex-shrink-0">
                        <Sparkles size={20} className="text-[var(--bt-primary)]" />
                    </div>
                    <div>
                        <p className="font-bold text-[var(--bt-text)]">밤토리와 친구가 될 시간!</p>
                        <p className="text-xs text-[var(--bt-text-secondary)]">
                            아이의 정보를 입력해주시면, 밤토리가 아이의 성향에 맞춰 더 즐거운 대화를 나눌 수 있어요.
                        </p>
                    </div>
                </div>

                {/* Name */}
                <div className="mb-6">
                    <label className="flex items-center gap-2 text-sm font-semibold text-[var(--bt-text)] mb-2">
                        <span>👤</span> 아이 이름
                    </label>
                    <input
                        type="text"
                        placeholder="아이의 이름을 입력해주세요"
                        maxLength={20}
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="w-full px-4 py-3 rounded-xl border border-[var(--bt-border)] bg-white text-[var(--bt-text)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--bt-primary)]"
                    />
                </div>

                {/* Age Slider */}
                <div className="mb-6">
                    <div className="flex items-center justify-between mb-2">
                        <label className="flex items-center gap-2 text-sm font-semibold text-[var(--bt-text)]">
                            <span>🎂</span> 아이 나이
                        </label>
                        <span className="text-lg font-bold text-[var(--bt-primary)]">{age}세</span>
                    </div>
                    <input
                        type="range"
                        min={2}
                        max={10}
                        value={age}
                        onChange={(e) => setAge(Number(e.target.value))}
                        className="w-full h-2 bg-gray-200 rounded-full appearance-none cursor-pointer accent-[var(--bt-primary)]"
                    />
                    <div className="flex justify-between text-xs text-[var(--bt-text-muted)] mt-1">
                        <span>2세</span>
                        <span>10세</span>
                    </div>
                </div>

                {/* Gender */}
                <div className="mb-6">
                    <label className="flex items-center gap-2 text-sm font-semibold text-[var(--bt-text)] mb-2">
                        <span>💜</span> 아이 성별
                    </label>
                    <div className="grid grid-cols-2 gap-3">
                        {([['m', '남자아이'], ['f', '여자아이']] as const).map(([val, label]) => (
                            <button
                                key={val}
                                onClick={() => setGender(val)}
                                className={`py-3 rounded-xl font-semibold text-sm transition-all ${
                                    gender === val
                                        ? 'bg-[var(--bt-primary)] text-white shadow-md'
                                        : 'bg-white border border-[var(--bt-border)] text-[var(--bt-text)]'
                                }`}
                            >
                                {label}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Interests */}
                <div className="mb-8">
                    <div className="flex items-center justify-between mb-2">
                        <label className="flex items-center gap-2 text-sm font-semibold text-[var(--bt-text)]">
                            <span>🎯</span> 아이 관심사
                        </label>
                        <span className="text-xs text-[var(--bt-text-muted)]">
                            {selectedInterests.length} / {MAX_INTERESTS} 선택됨
                        </span>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                        {INTERESTS.map((interest) => {
                            const isSelected = selectedInterests.includes(interest.id);
                            const isDisabled = !isSelected && selectedInterests.length >= MAX_INTERESTS;
                            return (
                                <button
                                    key={interest.id}
                                    onClick={() => toggleInterest(interest.id)}
                                    disabled={isDisabled}
                                    className={`flex flex-col items-center gap-1.5 py-3 px-2 rounded-xl transition-all text-center ${
                                        isSelected
                                            ? 'bg-indigo-50 border-2 border-[var(--bt-primary)] text-[var(--bt-primary)]'
                                            : isDisabled
                                            ? 'bg-gray-50 border border-gray-100 text-[var(--bt-text-muted)] opacity-50'
                                            : 'bg-white border border-[var(--bt-border)] text-[var(--bt-text)]'
                                    }`}
                                >
                                    <span className="text-xl">{interest.icon}</span>
                                    <span className="text-xs font-medium">{interest.label}</span>
                                </button>
                            );
                        })}
                    </div>
                </div>

                {/* Submit */}
                <button
                    onClick={handleSubmit}
                    disabled={!canSubmit || loading}
                    className="bt-btn-primary w-full"
                >
                    {loading ? '저장 중...' : '입력 완료 (다음으로)'}
                </button>
            </div>
        </div>
    );
}
