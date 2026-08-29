import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronRight, Lock } from 'lucide-react';
import { toast } from 'sonner';
import { api } from '@/api/client';
import { useBgm } from '@/contexts/BgmContext';

export default function ModeSelection() {
    const navigate = useNavigate();
    const bgm = useBgm();

    // Stop BGM when entering mode selection (post-login)
    useEffect(() => { bgm.stop(); }, []); // eslint-disable-line react-hooks/exhaustive-deps
    const [showPinInput, setShowPinInput] = useState(false);
    const [isSetupMode, setIsSetupMode] = useState(false);
    const [pin, setPin] = useState('');
    const [pinLoading, setPinLoading] = useState(false);

    const handleKidMode = () => {
        navigate('/kid/home');
    };

    const handleParentMode = async () => {
        try {
            const res = await api.get<{ hasPin: boolean }>('/v1/parent/pin/status');
            if (res.hasPin) {
                setIsSetupMode(false);
                setShowPinInput(true);
            } else {
                setIsSetupMode(true);
                setShowPinInput(true);
            }
        } catch {
            // If not authenticated or error, just navigate
            navigate('/parent/home');
        }
    };

    const handlePinSubmit = async () => {
        if (pin.length < 4) {
            toast.error('4자리 비밀번호를 입력해주세요.');
            return;
        }
        setPinLoading(true);
        try {
            if (isSetupMode) {
                await api.post('/v1/parent/pin', { pin });
                toast.success('비밀번호가 설정되었습니다.');
            } else {
                await api.post('/v1/parent/pin/verify', { pin });
            }
            navigate('/parent/home');
        } catch {
            toast.error(isSetupMode ? '비밀번호 설정에 실패했습니다.' : '비밀번호가 올바르지 않습니다.');
            setPin('');
        } finally {
            setPinLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[var(--bt-bg)] flex flex-col">
            {/* Header */}
            <div className="px-6 pt-6 pb-2">
                <p className="text-sm text-[var(--bt-text-secondary)]">누가 사용하나요?</p>
            </div>

            {/* Welcome Banner */}
            <div className="bg-gradient-to-br from-indigo-50 to-purple-50 px-6 py-8 text-center">
                <h1 className="text-2xl font-extrabold text-[var(--bt-text)] mb-2">반가워요!</h1>
                <p className="text-sm text-[var(--bt-text-secondary)]">사용할 모드를 선택해 주세요.</p>
            </div>

            {/* Mode Cards */}
            <div className="flex-1 px-6 py-6 flex flex-col gap-4">
                {/* Parent Mode */}
                <button
                    onClick={handleParentMode}
                    className="bt-card p-6 text-center w-full"
                >
                    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <span className="text-3xl">👤</span>
                    </div>
                    <h2 className="text-xl font-bold text-[var(--bt-text)] mb-2">부모 모드</h2>
                    <p className="text-sm text-[var(--bt-text-secondary)] mb-4">
                        아이의 학습 리포트와 설정을 관리할 수 있어요.
                    </p>
                    <ChevronRight size={20} className="text-[var(--bt-text-muted)] mx-auto" />
                </button>

                {/* Kid Mode */}
                <button
                    onClick={handleKidMode}
                    className="bt-card p-6 text-center w-full bg-indigo-50 border-[var(--bt-primary)] border-2"
                >
                    <div className="w-16 h-16 bg-indigo-100 rounded-full overflow-hidden mx-auto mb-4">
                        <img src="/assets/characters/popo.png" alt="포포" className="w-full h-full object-cover" />
                    </div>
                    <h2 className="text-xl font-bold text-[var(--bt-text)] mb-2">아이 모드</h2>
                    <p className="text-sm text-[var(--bt-text-secondary)] mb-4">
                        포포와 함께 즐거운 밤하늘 모험을 떠나볼까요?
                    </p>
                    <ChevronRight size={20} className="text-[var(--bt-primary)] mx-auto" />
                </button>
            </div>

            {/* Footer Info */}
            <div className="px-6 pb-6 text-center">
                <div className="flex items-center justify-center gap-2 text-[var(--bt-text-muted)] mb-4">
                    <Lock size={14} />
                    <span className="text-xs">부모 모드 진입 시 암호 확인이 필요합니다.</span>
                </div>
                <button
                    onClick={() => {
                        localStorage.clear();
                        sessionStorage.clear();
                        navigate('/');
                    }}
                    className="text-xs text-[var(--bt-text-muted)] underline"
                >
                    기기 초기화하기
                </button>
            </div>

            {/* PIN Modal */}
            {showPinInput && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-6">
                    <div className="bg-white rounded-2xl p-6 w-full max-w-sm">
                        <h3 className="text-lg font-bold text-[var(--bt-text)] text-center mb-2">
                            {isSetupMode ? '부모 모드 암호 설정' : '부모 모드 암호 입력'}
                        </h3>
                        <p className="text-sm text-[var(--bt-text-secondary)] text-center mb-6">
                            {isSetupMode
                                ? '부모 모드 보호를 위한 4자리 비밀번호를 설정해주세요.'
                                : '설정한 4자리 비밀번호를 입력해주세요.'}
                        </p>
                        <input
                            type="password"
                            inputMode="numeric"
                            maxLength={4}
                            value={pin}
                            onChange={(e) => setPin(e.target.value.replace(/\D/g, ''))}
                            placeholder="••••"
                            autoFocus
                            className="w-full text-center text-2xl tracking-[0.5em] px-4 py-3 rounded-xl border border-[var(--bt-border)] bg-white text-[var(--bt-text)] focus:outline-none focus:ring-2 focus:ring-[var(--bt-primary)]"
                        />
                        <div className="flex gap-3 mt-6">
                            <button
                                onClick={() => { setShowPinInput(false); setPin(''); }}
                                className="bt-btn-secondary flex-1"
                            >
                                취소
                            </button>
                            <button
                                onClick={handlePinSubmit}
                                disabled={pin.length < 4 || pinLoading}
                                className="bt-btn-primary flex-1"
                            >
                                {pinLoading ? '확인 중...' : isSetupMode ? '설정' : '확인'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
