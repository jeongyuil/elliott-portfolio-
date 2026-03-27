import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';
import { useBgm } from '@/contexts/BgmContext';
import { api } from '@/api/client';
import type { LoginResponse } from '@/api/types';

const isApplePlatform =
    /iPad|iPhone|iPod/.test(navigator.userAgent) ||
    (/Macintosh/.test(navigator.userAgent) && navigator.maxTouchPoints > 1);

export default function Landing() {
    const { loginAsParent } = useAuth();
    const navigate = useNavigate();
    const bgm = useBgm();
    const [searchParams] = useSearchParams();
    const [showEmail, setShowEmail] = useState(false);
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

    const handleEmailLogin = async (e: { preventDefault(): void }) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await api.post<LoginResponse>('/v1/auth/login', { email, password });
            loginAsParent(res.accessToken);
            navigate('/onboarding/setup');
        } catch (err: unknown) {
            const message = (err as Error)?.message ?? '';
            if (message.includes('email_not_verified')) {
                toast.error('이메일 인증이 필요합니다. 받은 편지함을 확인해 주세요.');
            } else {
                toast.error('이메일 또는 비밀번호가 올바르지 않습니다.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col min-h-screen bg-[var(--bt-bg)]">
            {/* Hero - Night Sky */}
            <section className="flex flex-col items-center justify-center flex-1 px-6 pt-16 pb-8">
                {/* Moon Logo */}
                <div className="w-32 h-32 bg-gradient-to-br from-indigo-100 to-indigo-200 rounded-3xl flex items-center justify-center mb-6 shadow-lg overflow-hidden">
                    <img src="/assets/characters/luna.png" alt="루나" className="w-24 h-24 object-contain" />
                </div>

                <h1 className="text-xl font-bold text-center text-[var(--bt-text)] leading-relaxed mb-2">
                    밤하늘의 친구들과<br />함께하는
                </h1>

                {/* Character illustration placeholder */}
                <div className="w-full max-w-xs h-48 bg-gradient-to-b from-indigo-50 to-purple-50 rounded-2xl flex items-center justify-center my-6">
                    <div className="text-center text-[var(--bt-text-muted)]">
                        <div className="flex items-center justify-center gap-3 mb-2">
                            <img src="/assets/characters/popo.png" alt="포포" className="w-16 h-16 object-contain" />
                            <img src="/assets/characters/luna.png" alt="루나" className="w-16 h-16 object-contain" />
                        </div>
                        <p className="text-xs">포포와 루나가 기다리고 있어요</p>
                    </div>
                </div>
            </section>

            {/* Login Section */}
            <section className="px-6 pb-8">
                <div className="w-full max-w-sm mx-auto flex flex-col gap-3">
                    {/* Kakao */}
                    <a
                        href="/v1/auth/kakao"
                        className="bt-social-btn bg-[var(--bt-kakao)] text-[#3C1E1E] border-[var(--bt-kakao)]"
                    >
                        <span className="text-lg">💬</span>
                        <span>카카오로 시작하기</span>
                    </a>

                    {/* Google */}
                    <a
                        href="/v1/auth/google"
                        className="bt-social-btn bg-white text-[var(--bt-text)]"
                    >
                        <GoogleIcon />
                        <span>Google로 로그인</span>
                    </a>

                    {/* Apple */}
                    {isApplePlatform && (
                        <a
                            href="/v1/auth/apple"
                            className="bt-social-btn bg-black text-white border-black"
                        >
                            <AppleIcon />
                            <span>Apple로 로그인</span>
                        </a>
                    )}

                    {/* Email login toggle */}
                    {!showEmail ? (
                        <button
                            onClick={() => setShowEmail(true)}
                            className="text-sm text-[var(--bt-text-secondary)] hover:text-[var(--bt-primary)] transition-colors mt-2 text-center"
                        >
                            이메일로 로그인
                        </button>
                    ) : (
                        <form onSubmit={handleEmailLogin} className="flex flex-col gap-3 mt-2">
                            <input
                                type="email"
                                placeholder="이메일"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="w-full px-4 py-3 rounded-xl border border-[var(--bt-border)] bg-white text-[var(--bt-text)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--bt-primary)]"
                            />
                            <input
                                type="password"
                                placeholder="비밀번호"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                className="w-full px-4 py-3 rounded-xl border border-[var(--bt-border)] bg-white text-[var(--bt-text)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--bt-primary)]"
                            />
                            <button
                                type="submit"
                                disabled={loading}
                                className="bt-btn-primary w-full"
                            >
                                {loading ? '로그인 중...' : '로그인'}
                            </button>
                        </form>
                    )}
                </div>

                {/* Terms */}
                <p className="text-center text-xs text-[var(--bt-text-muted)] mt-6 leading-relaxed">
                    로그인 시 밤토리의{' '}
                    <span className="underline">이용약관</span> 및{' '}
                    <span className="underline">개인정보 처리방침</span>에 동의하게 됩니다.
                </p>
            </section>
        </div>
    );
}

function GoogleIcon() {
    return (
        <svg width="18" height="18" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.3 0 24 0 14.7 0 6.7 5.4 2.8 13.3l8 6.2C12.8 13.3 17.9 9.5 24 9.5z" />
            <path fill="#4285F4" d="M46.1 24.6c0-1.6-.1-3.1-.4-4.6H24v8.7h12.4c-.5 2.8-2.2 5.2-4.6 6.8l7.2 5.6c4.2-3.9 6.7-9.6 7.1-16.5z" />
            <path fill="#FBBC05" d="M10.8 28.5c-.6-1.8-1-3.6-1-5.5s.3-3.8 1-5.5l-8-6.2C1 14.5 0 19.1 0 24s1 9.5 2.8 13.7l8-6.2c-.6-1.7-1-3.5-1-5z" />
            <path fill="#34A853" d="M24 48c6.5 0 12-2.1 16-5.7l-7.2-5.6c-2.2 1.5-5 2.3-8.8 2.3-6.1 0-11.2-3.8-13.2-9l-8 6.2C6.7 42.6 14.7 48 24 48z" />
        </svg>
    );
}

function AppleIcon() {
    return (
        <svg width="18" height="18" viewBox="0 0 814 1000" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
            <path d="M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76 0-103.7 40.8-165.9 40.8s-105-38.8-155.5-127.4C46 790.6 0 695.6 0 603.4c0-234.8 167.5-359.1 332-359.1 84 0 154 55.4 207 55.4 50.1 0 129.9-58.6 222.8-58.6 35.9 0 138.3 3.2 208.4 102.9zm-198.4-176.9c37.9-44.9 65.2-107.2 65.2-169.5 0-8.9-.6-17.9-2.2-25.5-61.7 2.2-134.9 41.2-179.3 91.7-34.1 38.5-66.4 100.8-66.4 164.1 0 9.5 1.6 18.9 2.2 22.1 3.9.6 10.3 1.6 16.6 1.6 55.4 0 123.4-37.2 163.9-84.5z" />
        </svg>
    );
}
