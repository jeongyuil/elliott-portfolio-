import { useState } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'sonner';
import { api } from '@/api/client';

export default function ForgotPassword() {
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const [sent, setSent] = useState(false);

    const handleSubmit = async (e: { preventDefault(): void }) => {
        e.preventDefault();
        setLoading(true);
        try {
            await api.post('/v1/auth/forgot-password', { email });
            setSent(true);
        } catch {
            toast.error('요청 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.');
        } finally {
            setLoading(false);
        }
    };

    if (sent) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-[var(--bt-bg)] p-6 text-center">
                <span className="text-6xl mb-5">📩</span>
                <h1 className="text-2xl font-extrabold text-[var(--bt-text)] mb-3">
                    이메일을 확인해 주세요
                </h1>
                <p className="text-[var(--bt-text-secondary)] mb-8 max-w-xs">
                    비밀번호 재설정 링크를 <strong>{email}</strong>로 발송했습니다.
                    링크는 1시간 동안 유효합니다.
                </p>
                <Link to="/login" className="text-[var(--bt-primary)] font-bold hover:underline">
                    로그인으로 돌아가기
                </Link>
            </div>
        );
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-[var(--bt-bg)] p-4">
            <div className="w-full max-w-md">
                <Link to="/" className="block mb-6 text-center">
                    <span className="text-4xl">🐾</span>
                    <p className="text-sm text-[var(--bt-text-secondary)] mt-1">밤토리</p>
                </Link>

                <div className="bg-white rounded-2xl shadow-sm border border-[var(--bt-border)] p-6">
                    <h2 className="text-xl font-extrabold text-[var(--bt-text)] mb-2 text-center">
                        비밀번호 찾기
                    </h2>
                    <p className="text-sm text-[var(--bt-text-secondary)] text-center mb-6">
                        가입하신 이메일을 입력하면 재설정 링크를 보내드립니다.
                    </p>

                    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                        <input
                            type="email"
                            placeholder="이메일 주소"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full px-4 py-3 rounded-xl border border-[var(--bt-border)] bg-[var(--bt-bg)] text-[var(--bt-text)] focus:outline-none focus:ring-2 focus:ring-[var(--bt-primary)]"
                        />
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-[var(--bt-primary)] text-white font-extrabold py-3 rounded-xl disabled:opacity-50 hover:brightness-110 active:scale-95 transition-all"
                        >
                            {loading ? '발송 중...' : '재설정 링크 보내기'}
                        </button>
                    </form>
                </div>

                <p className="text-center text-sm text-[var(--bt-text-secondary)] mt-6">
                    <Link to="/login" className="text-[var(--bt-primary)] font-bold">
                        로그인으로 돌아가기
                    </Link>
                </p>
            </div>
        </div>
    );
}
