import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Check, Zap, Star, Crown, Calendar } from 'lucide-react';

interface Plan {
    id: string;
    name: string;
    subtitle: string;
    price: number;
    priceLabel: string;
    icon: React.ReactNode;
    features: string[];
    recommended?: boolean;
}

const PLANS: Plan[] = [
    {
        id: 'basic',
        name: '포포 베이직',
        subtitle: '밤토리와 친해지는 첫걸음',
        price: 0,
        priceLabel: '₩0',
        icon: <Star size={20} className="text-[var(--bt-primary-light)]" />,
        features: [
            '일일 대화 10분 제공',
            '기본 아바타 1종 (포포)',
            '최근 대화 기록 3일 저장',
            '기본 모험 스테이지 제공',
        ],
    },
    {
        id: 'premium',
        name: '루나 프리미엄',
        subtitle: '가장 풍부한 학습과 모험',
        price: 9900,
        priceLabel: '₩9,900',
        icon: <Zap size={20} className="text-[var(--bt-accent)]" />,
        features: [
            '무제한 음성 대화',
            '모든 아바타 선택 가능',
            '모든 모험 스테이지 오픈',
            '실시간 친밀도 리포트',
            '대화 기록 영구 보관',
        ],
        recommended: true,
    },
    {
        id: 'family',
        name: '은하수 패밀리',
        subtitle: '온 가족이 함께 즐기는 밤토리',
        price: 15900,
        priceLabel: '₩15,900',
        icon: <Crown size={20} className="text-amber-500" />,
        features: [
            '최대 3인 프로필 등록',
            '동시 접속 가능',
            '프리미엄 모든 혜택 포함',
            '아이별 맞춤 성장 리포트',
            '부모 전용 대시보드',
        ],
    },
];

export default function SubscriptionSelect() {
    const navigate = useNavigate();
    const [selected, setSelected] = useState<string>('premium');

    const handleComplete = () => {
        sessionStorage.setItem('onboarding_sub_done', 'true');
        sessionStorage.setItem('onboarding_plan', selected);
        navigate('/onboarding/setup');
    };

    return (
        <div className="min-h-screen bg-[var(--bt-bg)]">
            {/* Header */}
            <div className="flex items-center px-4 py-4">
                <button onClick={() => navigate('/onboarding/setup')} className="p-2 -ml-2">
                    <ChevronLeft size={24} className="text-[var(--bt-text)]" />
                </button>
                <h1 className="text-lg font-bold text-[var(--bt-text)] ml-2">구독 모델 선택</h1>
            </div>

            <div className="px-6 pb-8">
                {/* Title */}
                <h2 className="text-xl font-extrabold text-[var(--bt-text)] leading-tight mb-1">
                    아이의 성장을<br />함께할
                    <br />플랜을 선택해주세요
                </h2>
                <p className="text-sm text-[var(--bt-text-secondary)] mb-6">
                    7일간 모든 기능을 무료로 체험할 수 있습니다.
                    <br />무료 체험 종료 전까지는 결제되지 않습니다.
                </p>

                {/* Plan Cards */}
                <div className="flex flex-col gap-4 mb-6">
                    {PLANS.map((plan) => {
                        const isSelected = selected === plan.id;
                        return (
                            <button
                                key={plan.id}
                                onClick={() => setSelected(plan.id)}
                                className={`bt-card p-5 text-left transition-all relative ${
                                    isSelected
                                        ? 'border-[var(--bt-primary)] border-2 shadow-md'
                                        : ''
                                }`}
                            >
                                {plan.recommended && (
                                    <span className="absolute -top-2 right-4 bg-[var(--bt-accent)] text-white text-xs font-bold px-3 py-0.5 rounded-full">
                                        추천
                                    </span>
                                )}
                                <div className="flex items-center gap-2 mb-1">
                                    {plan.icon}
                                    <span className="font-bold text-[var(--bt-text)]">{plan.name}</span>
                                </div>
                                <p className="text-xs text-[var(--bt-text-secondary)] mb-3">{plan.subtitle}</p>

                                <p className="text-2xl font-extrabold text-[var(--bt-text)] mb-3">
                                    {plan.priceLabel}
                                    <span className="text-sm font-normal text-[var(--bt-text-secondary)]">/ 월</span>
                                </p>

                                <div className="flex flex-col gap-1.5">
                                    {plan.features.map((f) => (
                                        <div key={f} className="flex items-center gap-2">
                                            <Check size={14} className="text-[var(--bt-success)] flex-shrink-0" />
                                            <span className="text-sm text-[var(--bt-text-secondary)]">{f}</span>
                                        </div>
                                    ))}
                                </div>

                                <div className="mt-4">
                                    <span className={`bt-btn-secondary text-center block text-sm py-2 ${
                                        isSelected ? 'bg-[var(--bt-primary)] text-white border-[var(--bt-primary)]' : ''
                                    }`}>
                                        {isSelected ? '선택됨' : '플랜 선택하기'}
                                    </span>
                                </div>
                            </button>
                        );
                    })}
                </div>

                {/* Payment Notice */}
                <div className="bg-gray-50 rounded-xl p-4 mb-6">
                    <div className="flex items-start gap-3">
                        <Calendar size={18} className="text-[var(--bt-text-muted)] mt-0.5 flex-shrink-0" />
                        <div>
                            <p className="text-sm font-semibold text-[var(--bt-text)] mb-1">결제 정보 등록 안내</p>
                            <p className="text-xs text-[var(--bt-text-secondary)] leading-relaxed">
                                카드 결제 정보는 7일간의 무료 체험 기간이 끝난 후에 등록하시면 됩니다. 지금 바로 밤토리를 시작해보세요!
                            </p>
                        </div>
                    </div>
                </div>

                <p className="text-center text-xs text-[var(--bt-text-muted)] mb-4">
                    언제든지 해지가 가능합니다.
                </p>

                {/* CTA */}
                <button onClick={handleComplete} className="bt-btn-primary w-full flex items-center justify-center gap-2">
                    <Zap size={18} />
                    무료 체험 시작하기
                </button>
            </div>
        </div>
    );
}
