import { useState, useEffect } from 'react';
import { Link, useLocation, useSearchParams } from 'react-router-dom';
import { toast } from 'sonner';
import { api } from '@/api/client';

export default function VerifyEmail() {
    const [searchParams] = useSearchParams();
    const location = useLocation();
    const token = searchParams.get('token');
    const error = searchParams.get('error');
    const emailFromQuery = searchParams.get('email') ?? (location.state as { email?: string })?.email ?? '';

    const [email, setEmail] = useState(emailFromQuery);
    const [resending, setResending] = useState(false);
    const [resent, setResent] = useState(false);

    // If URL has ?token=..., forward through Vite proxy to backend
    // Backend verifies → sets HttpOnly cookie → redirects to /select-child
    useEffect(() => {
        if (token) {
            window.location.href = `/v1/auth/verify-email?token=${token}`;
        }
    }, [token]);

    const handleResend = async () => {
        if (!email) {
            toast.error('이메일 주소를 입력해 주세요.');
            return;
        }
        setResending(true);
        try {
            await api.post('/v1/auth/resend-verification', { email });
            setResent(true);
            toast.success('인증 이메일을 재발송했습니다. 받은 편지함을 확인해 주세요.');
        } catch {
            toast.error('재발송 실패. 잠시 후 다시 시도해 주세요.');
        } finally {
            setResending(false);
        }
    };

    // While redirecting via token
    if (token) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-[var(--bt-bg)]">
                <div className="w-8 h-8 border-4 border-[var(--bt-primary)] border-t-transparent rounded-full animate-spin mb-4" />
                <p className="text-[var(--bt-text-secondary)]">이메일 인증 중...</p>
            </div>
        );
    }

    // Error: invalid token
    if (error === 'invalid') {
        return (
            <StatusScreen
                icon="❌"
                title="유효하지 않은 링크"
                desc="인증 링크가 올바르지 않습니다. 다시 인증 이메일을 요청해 주세요."
                email={email}
                setEmail={setEmail}
                onResend={handleResend}
                resending={resending}
                resent={resent}
            />
        );
    }

    // Error: expired token
    if (error === 'expired') {
        return (
            <StatusScreen
                icon="⏰"
                title="링크가 만료되었습니다"
                desc="인증 링크가 만료되었습니다 (24시간). 새 인증 이메일을 요청해 주세요."
                email={email}
                setEmail={setEmail}
                onResend={handleResend}
                resending={resending}
                resent={resent}
            />
        );
    }

    // Default: post-signup pending state
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-[var(--bt-bg)] p-6 text-center">
            <span className="text-6xl mb-5">📬</span>
            <h1 className="text-2xl font-extrabold text-[var(--bt-text)] mb-3">
                이메일을 확인해 주세요!
            </h1>
            <p className="text-[var(--bt-text-secondary)] mb-2 max-w-xs">
                <strong>{email || '입력하신 이메일'}</strong>로 인증 링크를 보냈습니다.
            </p>
            <p className="text-sm text-[var(--bt-text-secondary)] mb-8 max-w-xs">
                링크를 클릭하면 자동으로 로그인됩니다.
                스팸 폴더도 확인해 보세요.
            </p>

            {!resent ? (
                <button
                    onClick={handleResend}
                    disabled={resending}
                    className="text-sm text-[var(--bt-primary)] font-bold hover:underline disabled:opacity-50"
                >
                    {resending ? '재발송 중...' : '이메일을 받지 못했어요 (재발송)'}
                </button>
            ) : (
                <p className="text-sm text-[var(--bt-primary)] font-bold">✓ 재발송 완료!</p>
            )}

            <Link to="/login" className="mt-6 text-sm text-[var(--bt-text-secondary)] hover:text-[var(--bt-primary)]">
                로그인으로 돌아가기
            </Link>
        </div>
    );
}

function StatusScreen({
    icon,
    title,
    desc,
    email,
    setEmail,
    onResend,
    resending,
    resent,
}: {
    icon: string;
    title: string;
    desc: string;
    email: string;
    setEmail: (v: string) => void;
    onResend: () => void;
    resending: boolean;
    resent: boolean;
}) {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-[var(--bt-bg)] p-6 text-center">
            <span className="text-6xl mb-5">{icon}</span>
            <h1 className="text-2xl font-extrabold text-[var(--bt-text)] mb-3">{title}</h1>
            <p className="text-[var(--bt-text-secondary)] mb-6 max-w-xs">{desc}</p>

            {!resent ? (
                <div className="flex flex-col gap-3 w-full max-w-xs">
                    <input
                        type="email"
                        placeholder="이메일 주소"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full px-4 py-3 rounded-xl border border-[var(--bt-border)] bg-white text-[var(--bt-text)] focus:outline-none focus:ring-2 focus:ring-[var(--bt-primary)]"
                    />
                    <button
                        onClick={onResend}
                        disabled={resending}
                        className="w-full bg-[var(--bt-primary)] text-white font-extrabold py-3 rounded-xl disabled:opacity-50 hover:brightness-110 active:scale-95 transition-all"
                    >
                        {resending ? '발송 중...' : '인증 이메일 재발송'}
                    </button>
                </div>
            ) : (
                <p className="text-[var(--bt-primary)] font-bold">✓ 이메일을 발송했습니다. 받은 편지함을 확인해 주세요.</p>
            )}

            <Link to="/login" className="mt-6 text-sm text-[var(--bt-text-secondary)] hover:text-[var(--bt-primary)]">
                로그인으로 돌아가기
            </Link>
        </div>
    );
}
