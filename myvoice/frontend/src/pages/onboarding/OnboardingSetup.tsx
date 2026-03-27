import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Sparkles, CreditCard, Info } from 'lucide-react';

export default function OnboardingSetup() {
    const navigate = useNavigate();
    const [childDone, setChildDone] = useState(false);
    const [subDone, setSubDone] = useState(false);

    // Check if returning from child info or subscription
    useEffect(() => {
        const childComplete = sessionStorage.getItem('onboarding_child_done');
        const subComplete = sessionStorage.getItem('onboarding_sub_done');
        if (childComplete) setChildDone(true);
        if (subComplete) setSubDone(true);
    }, []);

    const allDone = childDone && subDone;

    return (
        <div className="min-h-screen bg-[var(--bt-bg)]">
            {/* Header */}
            <div className="flex items-center px-4 py-4">
                <button onClick={() => navigate('/')} className="p-2 -ml-2">
                    <ChevronLeft size={24} className="text-[var(--bt-text)]" />
                </button>
                <h1 className="text-lg font-bold text-[var(--bt-text)] ml-2">시작하기</h1>
            </div>

            <div className="px-6 pb-8">
                {/* Step Indicator */}
                <div className="inline-flex items-center px-3 py-1 rounded-full border border-[var(--bt-border)] bg-white text-xs font-semibold text-[var(--bt-text-secondary)] mb-4">
                    Step 1 of 2
                </div>

                {/* Title */}
                <h2 className="text-2xl font-extrabold text-[var(--bt-text)] leading-tight mb-2">
                    우리 아이를 위한<br />맞춤 환경을<br />만들어요
                </h2>
                <p className="text-sm text-[var(--bt-text-secondary)] leading-relaxed mb-8">
                    밤토리와 함께할 아이의 정보와 구독 서비스를 선택하여 신비로운 밤의 모험을 준비하세요.
                </p>

                {/* Cards */}
                <div className="flex flex-col gap-4 mb-8">
                    {/* Child Info Card */}
                    <button
                        onClick={() => navigate('/onboarding/child-info')}
                        className="bt-card p-5 flex items-center gap-4 text-left w-full"
                    >
                        <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center flex-shrink-0">
                            <Sparkles size={24} className="text-[var(--bt-primary)]" />
                        </div>
                        <div className="flex-1">
                            <p className="font-bold text-[var(--bt-text)]">아이 정보 입력</p>
                            <p className="text-sm text-[var(--bt-text-secondary)]">이름, 나이, 관심사 설정</p>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className={`bt-badge text-xs ${childDone ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-[var(--bt-text-muted)]'}`}>
                                {childDone ? '완료' : '미완료'}
                            </span>
                            <ChevronRight size={20} className="text-[var(--bt-text-muted)]" />
                        </div>
                    </button>

                    {/* Subscription Card */}
                    <button
                        onClick={() => navigate('/onboarding/subscription')}
                        className="bt-card p-5 flex items-center gap-4 text-left w-full border-[var(--bt-primary)] border-opacity-30"
                    >
                        <div className="w-12 h-12 rounded-xl bg-purple-50 flex items-center justify-center flex-shrink-0">
                            <CreditCard size={24} className="text-[var(--bt-accent)]" />
                        </div>
                        <div className="flex-1">
                            <p className="font-bold text-[var(--bt-text)]">구독 모델 선택</p>
                            <p className="text-sm text-[var(--bt-text-secondary)]">밤토리 프리미엄 혜택 확인</p>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className={`bt-badge text-xs ${subDone ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-600'}`}>
                                {subDone ? '선택됨' : '미선택'}
                            </span>
                            <ChevronRight size={20} className="text-[var(--bt-text-muted)]" />
                        </div>
                    </button>
                </div>

                {/* Help Box */}
                <div className="bg-indigo-50 rounded-xl p-4 mb-8">
                    <div className="flex items-start gap-3">
                        <Info size={18} className="text-[var(--bt-primary)] mt-0.5 flex-shrink-0" />
                        <div>
                            <p className="text-sm font-semibold text-[var(--bt-text)] mb-1">도움말</p>
                            <p className="text-xs text-[var(--bt-text-secondary)] leading-relaxed">
                                입력하신 아이 정보는 인공지능 아바타 '포포'와 '루나'가 아이의 관심사에 맞춰 대화를 이끌어가는 데 사용됩니다.
                            </p>
                        </div>
                    </div>
                </div>

                {/* CTA */}
                <button
                    onClick={() => {
                        sessionStorage.removeItem('onboarding_child_done');
                        sessionStorage.removeItem('onboarding_sub_done');
                        navigate('/mode-select');
                    }}
                    disabled={!allDone}
                    className="bt-btn-primary w-full"
                >
                    모든 설정 완료하기
                </button>

                <p className="text-center text-xs text-[var(--bt-text-muted)] mt-4 leading-relaxed">
                    SNS 계정으로 로그인되어 별도의 회원가입 절차 없이<br />
                    추가 정보만 입력하면 밤토리를 시작할 수 있습니다.
                </p>
            </div>
        </div>
    );
}
