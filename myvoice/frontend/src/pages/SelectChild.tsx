import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useBgm } from '@/contexts/BgmContext';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { toast } from 'sonner';
import { api } from '@/api/client';

interface Child {
    childId: string;
    name: string;
    avatarId?: string;
    gender?: string;
}

type View = 'select' | 'onboard-gender' | 'onboard-name';

export default function SelectChild() {
    const { loginAsParent, loginAsChild } = useAuth();
    const navigate = useNavigate();
    const bgm = useBgm();
    const [searchParams] = useSearchParams();
    const [children, setChildren] = useState<Child[]>([]);
    const [loading, setLoading] = useState(true);

    // Onboarding state
    const [view, setView] = useState<View>('select');
    const [selectedGender, setSelectedGender] = useState<'male' | 'female' | null>(null);
    const [childName, setChildName] = useState('');
    const [creating, setCreating] = useState(false);

    // Pick up OAuth token from URL params (e.g. after Kakao/Google redirect)
    useEffect(() => {
        const token = searchParams.get('token');
        const familyId = searchParams.get('family_id');
        if (token) {
            loginAsParent(token);
            // Clean URL params
            window.history.replaceState({}, '', '/select-child');
        }
        if (familyId) {
            localStorage.setItem('family_id', familyId);
        }
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        api.get<Child[]>('/v1/parent/children')
            .then((list) => {
                setChildren(list);
                if (list.length === 0) setView('onboard-gender');
            })
            .catch(() => toast.error('아이 목록을 불러오는데 실패했습니다.'))
            .finally(() => setLoading(false));
    }, []);

    const handleSelect = async (childId: string) => {
        try {
            const res = await api.post<{ childToken: string }>('/v1/auth/select-child', { childId });
            loginAsChild(res.childToken);
            navigate('/kid/home');
        } catch {
            toast.error('프로필 선택에 실패했습니다. 다시 시도해 주세요.');
        }
    };

    const handleCreateChild = async () => {
        const name = childName.trim();
        if (!name) {
            toast.error('이름을 입력해 주세요.');
            return;
        }
        setCreating(true);
        try {
            const newChild = await api.post<Child>('/v1/parent/children', {
                name,
                gender: selectedGender === 'female' ? 'female' : 'male',
                avatarId: selectedGender === 'female' ? 'girl_1' : 'boy_1',
            });
            await handleSelect(newChild.childId);
        } catch {
            toast.error('프로필 생성에 실패했습니다. 다시 시도해 주세요.');
        } finally {
            setCreating(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-[var(--bt-primary)] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    // ── Onboarding: Step 1 — Gender ────────────────────────────────
    if (view === 'onboard-gender') {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-[var(--bt-bg)] p-6 text-center">
                <span className="text-5xl mb-4">🐾</span>
                <h1 className="text-2xl font-extrabold text-[var(--bt-text)] mb-2">
                    어떤 아이인가요?
                </h1>
                <p className="text-[var(--bt-text-secondary)] mb-10">
                    루나가 맞춤 친구가 되어줄 거예요!
                </p>

                <div className="flex gap-6">
                    <button
                        onClick={() => { setSelectedGender('male'); setView('onboard-name'); }}
                        className="flex flex-col items-center gap-3 w-36 h-40 rounded-2xl border-2 border-[var(--bt-border)] bg-white hover:border-blue-400 hover:bg-blue-50 active:scale-95 transition-all"
                    >
                        <img src="/assets/characters/boy_captain.png" alt="남자아이" className="w-20 h-20 object-contain mt-2" />
                        <span className="font-bold text-[var(--bt-text)]">남자아이</span>
                    </button>

                    <button
                        onClick={() => { setSelectedGender('female'); setView('onboard-name'); }}
                        className="flex flex-col items-center gap-3 w-36 h-40 rounded-2xl border-2 border-[var(--bt-border)] bg-white hover:border-pink-400 hover:bg-pink-50 active:scale-95 transition-all"
                    >
                        <img src="/assets/characters/girl_captain.png" alt="여자아이" className="w-20 h-20 object-contain mt-2" />
                        <span className="font-bold text-[var(--bt-text)]">여자아이</span>
                    </button>
                </div>
            </div>
        );
    }

    // ── Onboarding: Step 2 — Name ───────────────────────────────────
    if (view === 'onboard-name') {
        const isFemale = selectedGender === 'female';
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-[var(--bt-bg)] p-6 text-center">
                <button
                    onClick={() => setView('onboard-gender')}
                    className="absolute top-6 left-6 text-[var(--bt-text-secondary)] hover:text-[var(--bt-text)] text-sm"
                >
                    ← 뒤로
                </button>

                <img
                    src={isFemale ? '/assets/characters/girl_captain.png' : '/assets/characters/boy_captain.png'}
                    alt={isFemale ? '여자아이' : '남자아이'}
                    className="w-24 h-24 object-contain mb-4"
                />
                <h1 className="text-2xl font-extrabold text-[var(--bt-text)] mb-2">
                    이름이 뭐예요?
                </h1>
                <p className="text-[var(--bt-text-secondary)] mb-8">
                    루나가 이름으로 불러줄 거예요!
                </p>

                <div className="w-full max-w-xs flex flex-col gap-4">
                    <input
                        type="text"
                        placeholder="아이 이름"
                        value={childName}
                        onChange={(e) => setChildName(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleCreateChild()}
                        maxLength={20}
                        autoFocus
                        className="w-full px-4 py-3 rounded-xl border border-[var(--bt-border)] bg-white text-[var(--bt-text)] text-center text-lg font-bold focus:outline-none focus:ring-2 focus:ring-[var(--bt-primary)]"
                    />
                    <button
                        onClick={handleCreateChild}
                        disabled={creating || !childName.trim()}
                        className="w-full bg-[var(--bt-primary)] text-white font-extrabold py-3 rounded-xl disabled:opacity-50 hover:brightness-110 active:scale-95 transition-all"
                    >
                        {creating ? '생성 중...' : '시작하기 🚀'}
                    </button>
                </div>
            </div>
        );
    }

    // ── Select child (existing children) ───────────────────────────
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-[var(--bt-bg)] p-4">
            <h1 className="text-2xl font-bold mb-8 text-[var(--bt-text)]">누가 학습하나요?</h1>

            <div className="grid grid-cols-2 gap-6 max-w-md w-full">
                {children.map((child) => (
                    <button
                        key={child.childId}
                        onClick={() => handleSelect(child.childId)}
                        className="flex flex-col items-center gap-4 p-6 bg-white rounded-2xl hover:bg-gray-50 active:scale-95 transition-all border border-[var(--bt-border)]"
                    >
                        <div className={`w-24 h-24 rounded-full flex items-center justify-center overflow-hidden ${
                            child.gender === 'female' || child.avatarId === 'girl_1' ? 'bg-pink-100' : 'bg-blue-100'
                        }`}>
                            <img
                                src={child.gender === 'female' || child.avatarId === 'girl_1' ? '/assets/characters/girl_captain.png' : '/assets/characters/boy_captain.png'}
                                alt={child.name}
                                className="w-20 h-20 object-contain"
                            />
                        </div>
                        <span className="font-bold text-lg">{child.name}</span>
                    </button>
                ))}

                {/* Add child button */}
                <button
                    onClick={() => setView('onboard-gender')}
                    className="flex flex-col items-center gap-4 p-6 bg-white rounded-2xl hover:bg-gray-50 active:scale-95 transition-all border-2 border-dashed border-[var(--bt-border)]"
                >
                    <div className="w-24 h-24 rounded-full flex items-center justify-center text-4xl bg-gray-100">
                        ➕
                    </div>
                    <span className="font-bold text-lg text-[var(--bt-text-secondary)]">아이 추가</span>
                </button>
            </div>
        </div>
    );
}
