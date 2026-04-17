import { useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';
import { api } from '@/api/client';
import type { LoginResponse } from '@/api/types';

type Tab = 'email' | 'sns';

// Show Apple button on iOS / Safari
const isApplePlatform =
    /iPad|iPhone|iPod/.test(navigator.userAgent) ||
    (/Macintosh/.test(navigator.userAgent) && navigator.maxTouchPoints > 1);

export default function Login() {
    const { loginAsParent } = useAuth();
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const [tab, setTab] = useState<Tab>('email');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);

    const oauthError = searchParams.get('error');
    if (oauthError) {
        const messages: Record<string, string> = {
            oauth_failed: '소셜 로그인에 실패했습니다. 다시 시도해 주세요.',
            oauth_no_user: '소셜 계정 정보를 가져오지 못했습니다.',
            apple_no_token: 'Apple 로그인에 실패했습니다.',
            apple_invalid_token: 'Apple 인증 토큰이 유효하지 않습니다.',
        };
        toast.error(messages[oauthError] ?? '로그인 중 오류가 발생했습니다.');
    }

    const resendVerification = async () => {
        if (!email) return;
        try {
            await api.post('/v1/auth/resend-verification', { email });
            toast.success('인증 이메일을 재발송했습니다.');
        } catch {
            toast.error('재발송 실패. 잠시 후 다시 시도해 주세요.');
        }
    };

    const handleEmailLogin = async (e: { preventDefault(): void }) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await api.post<LoginResponse>('/v1/auth/login', { email, password });
            loginAsParent(res.accessToken);
            navigate('/select-child');
        } catch (err: unknown) {
            const message = (err as Error)?.message ?? '';
            if (message.includes('email_not_verified')) {
                toast.error('이메일 인증이 필요합니다. 받은 편지함을 확인해 주세요.', {
                    action: { label: '재발송', onClick: resendVerification },
                });
            } else {
                toast.error('이메일 또는 비밀번호가 올바르지 않습니다.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-[var(--bt-bg)] p-4">
            <div className="w-full max-w-md">
                <Link to="/" className="block mb-6 text-center">
                    <span className="text-4xl">🐾</span>
                    <p className="text-sm text-[var(--bt-text-secondary)] mt-1">밤토리</p>
                </Link>

                <div className="bg-white rounded-2xl shadow-sm border border-[var(--bt-border)] overflow-hidden">
                    {/* Tabs */}
                    <div className="flex border-b border-[var(--bt-border)]">
                        {(['email', 'sns'] as Tab[]).map((t) => (
                            <button
                                key={t}
                                onClick={() => setTab(t)}
                                className={`flex-1 py-3 text-sm font-bold transition-colors ${
                                    tab === t
                                        ? 'text-[var(--bt-primary)] border-b-2 border-[var(--bt-primary)]'
                                        : 'text-[var(--bt-text-secondary)]'
                                }`}
                            >
                                {t === 'email' ? '이메일 로그인' : 'SNS 로그인'}
                            </button>
                        ))}
                    </div>

                    <div className="p-6">
                        {tab === 'email' ? (
                            <form onSubmit={handleEmailLogin} className="flex flex-col gap-4">
                                <input
                                    type="email"
                                    placeholder="이메일"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                    className="w-full px-4 py-3 rounded-xl border border-[var(--bt-border)] bg-[var(--bt-bg)] text-[var(--bt-text)] focus:outline-none focus:ring-2 focus:ring-[var(--bt-primary)]"
                                />
                                <input
                                    type="password"
                                    placeholder="비밀번호"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    className="w-full px-4 py-3 rounded-xl border border-[var(--bt-border)] bg-[var(--bt-bg)] text-[var(--bt-text)] focus:outline-none focus:ring-2 focus:ring-[var(--bt-primary)]"
                                />
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full bg-[var(--bt-primary)] text-white font-extrabold py-3 rounded-xl disabled:opacity-50 hover:brightness-110 active:scale-95 transition-all"
                                >
                                    {loading ? '로그인 중...' : '로그인'}
                                </button>
                                <Link
                                    to="/forgot-password"
                                    className="text-center text-sm text-[var(--bt-text-secondary)] hover:text-[var(--bt-primary)]"
                                >
                                    비밀번호를 잊으셨나요?
                                </Link>
                            </form>
                        ) : (
                            <div className="flex flex-col gap-3">
                                <SocialButton
                                    href="/v1/auth/google"
                                    icon={<GoogleIcon />}
                                    label="Google로 계속하기"
                                    className="bg-white border border-[var(--bt-border)] text-[var(--bt-text)]"
                                />
                                <SocialButton
                                    href="/v1/auth/kakao"
                                    icon={<span className="text-xl leading-none">💬</span>}
                                    label="카카오로 계속하기"
                                    className="bg-[#FEE500] text-[#3C1E1E]"
                                />
                                {isApplePlatform && (
                                    <SocialButton
                                        href="/v1/auth/apple"
                                        icon={<AppleIcon />}
                                        label="Apple로 계속하기"
                                        className="bg-black text-white"
                                    />
                                )}
                            </div>
                        )}
                    </div>
                </div>

                <p className="text-center text-sm text-[var(--bt-text-secondary)] mt-6">
                    계정이 없으신가요?{' '}
                    <Link to="/signup" className="text-[var(--bt-primary)] font-bold">
                        회원가입
                    </Link>
                </p>
            </div>
        </div>
    );
}

function SocialButton({
    href,
    icon,
    label,
    className,
}: {
    href: string;
    icon: React.ReactNode;
    label: string;
    className: string;
}) {
    return (
        <a
            href={href}
            className={`flex items-center justify-center gap-3 w-full py-3 px-4 rounded-xl font-bold shadow-sm hover:brightness-95 active:scale-95 transition-all ${className}`}
        >
            {icon}
            <span>{label}</span>
        </a>
    );
}

function GoogleIcon() {
    return (
        <svg width="20" height="20" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.3 0 24 0 14.7 0 6.7 5.4 2.8 13.3l8 6.2C12.8 13.3 17.9 9.5 24 9.5z" />
            <path fill="#4285F4" d="M46.1 24.6c0-1.6-.1-3.1-.4-4.6H24v8.7h12.4c-.5 2.8-2.2 5.2-4.6 6.8l7.2 5.6c4.2-3.9 6.7-9.6 7.1-16.5z" />
            <path fill="#FBBC05" d="M10.8 28.5c-.6-1.8-1-3.6-1-5.5s.3-3.8 1-5.5l-8-6.2C1 14.5 0 19.1 0 24s1 9.5 2.8 13.7l8-6.2c-.6-1.7-1-3.5-1-5z" />
            <path fill="#34A853" d="M24 48c6.5 0 12-2.1 16-5.7l-7.2-5.6c-2.2 1.5-5 2.3-8.8 2.3-6.1 0-11.2-3.8-13.2-9l-8 6.2C6.7 42.6 14.7 48 24 48z" />
        </svg>
    );
}

function AppleIcon() {
    return (
        <svg width="20" height="20" viewBox="0 0 814 1000" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
            <path d="M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76 0-103.7 40.8-165.9 40.8s-105-38.8-155.5-127.4C46 790.6 0 695.6 0 603.4c0-234.8 167.5-359.1 332-359.1 84 0 154 55.4 207 55.4 50.1 0 129.9-58.6 222.8-58.6 35.9 0 138.3 3.2 208.4 102.9zm-198.4-176.9c37.9-44.9 65.2-107.2 65.2-169.5 0-8.9-.6-17.9-2.2-25.5-61.7 2.2-134.9 41.2-179.3 91.7-34.1 38.5-66.4 100.8-66.4 164.1 0 9.5 1.6 18.9 2.2 22.1 3.9.6 10.3 1.6 16.6 1.6 55.4 0 123.4-37.2 163.9-84.5z" />
        </svg>
    );
}
