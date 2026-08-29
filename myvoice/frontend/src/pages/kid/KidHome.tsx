/**
 * Kid Home - Wireframe #7
 * 포포 캐릭터 + 실시간 대화 + 마이크 버튼 + 모험 떠나기
 */
import { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, Mic, MicOff, ChevronRight, Loader2, Volume2, VolumeX } from 'lucide-react';
import { useHome } from '@/api/hooks/useHome';
import { useAuth } from '@/contexts/AuthContext';
import { useBgm } from '@/contexts/BgmContext';
import { useVoiceWebSocket } from '@/hooks/useVoiceWebSocket';
import { api } from '@/api/client';
import { parseCharacterSegments, SPEAKER_STYLES } from '@/lib/parseCharacterSegments';

export default function KidHome() {
    const navigate = useNavigate();
    const { data: homeData, isLoading } = useHome();
    const { childToken } = useAuth();
    const bgm = useBgm();
    const logEndRef = useRef<HTMLDivElement>(null);

    const [sessionId, setSessionId] = useState<string | null>(null);
    const [statusText, setStatusText] = useState('');

    const profile = homeData?.child;
    const level = profile?.level || 1;
    const intimacy = 85; // TODO: from API

    // Play post-login BGM on mount
    useEffect(() => { bgm.play('/assets/audio/bgm.mp3'); }, []); // eslint-disable-line react-hooks/exhaustive-deps

    // Create a free_talk session on mount
    useEffect(() => {
        if (!childToken || sessionId) return;
        let cancelled = false;
        (async () => {
            try {
                const res = await api.post<{ sessionId: string }>('/v1/kid/sessions', {
                    sessionType: 'free_talk',
                });
                if (!cancelled && res.sessionId) {
                    setSessionId(res.sessionId);
                }
            } catch {
                // Session creation failed — mic will show as disconnected
            }
        })();
        return () => { cancelled = true; };
    }, [childToken, sessionId]);

    const handleStatus = useCallback((message: string) => {
        setStatusText(message);
    }, []);

    const {
        messages,
        isRecording,
        isAiSpeaking,
        connectionState,
        toggleRecording,
        sendMood,
    } = useVoiceWebSocket({
        sessionId,
        childToken,
        muted: bgm.isMuted,
        onStatusMessage: handleStatus,
    });

    // Auto-scroll when messages change
    useEffect(() => {
        logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const isConnected = connectionState === 'connected';
    const isConnecting = connectionState === 'connecting';

    if (isLoading) {
        return (
            <div className="h-full flex items-center justify-center bg-gradient-to-b from-indigo-900 to-[var(--bt-bg)]">
                <div className="w-8 h-8 border-4 border-white border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    return (
        <div className="h-full flex flex-col bg-gradient-to-b from-indigo-900 via-indigo-800 to-[var(--bt-bg)]">
            {/* Status Bar Area (dark) */}
            <div className="h-2 bg-indigo-900" />

            {/* Header - 포포 info + 친밀도 */}
            <div className="px-4 pt-3 pb-4">
                <div className="bt-card p-3 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center overflow-hidden">
                            <img src="/assets/characters/popo.png" alt="포포" className="w-full h-full object-cover" />
                        </div>
                        <div>
                            <div className="flex items-center gap-2">
                                <span className="font-bold text-[var(--bt-text)]">포포</span>
                                <span className="text-[10px] font-bold bg-[var(--bt-primary)] text-white px-1.5 py-0.5 rounded-full">
                                    Lv.{level}
                                </span>
                            </div>
                            <p className="text-xs text-[var(--bt-text-secondary)]">
                                {statusText || '오늘 기분: 최고!'}
                            </p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={bgm.toggleMute}
                            className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center transition-all active:scale-90"
                            aria-label={bgm.isMuted ? '소리 켜기' : '소리 끄기'}
                        >
                            {bgm.isMuted
                                ? <VolumeX size={16} className="text-gray-400" />
                                : <Volume2 size={16} className="text-[var(--bt-primary)]" />
                            }
                        </button>
                        <div className="flex items-center gap-1.5">
                            <Heart size={14} className="text-[var(--bt-heart)]" fill="currentColor" />
                            <span className="text-sm font-bold text-[var(--bt-text)]">친밀도 {intimacy}%</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Character Display */}
            <div className="flex-shrink-0 flex items-center justify-center py-6">
                <div className="w-64 h-48 bg-gradient-to-b from-indigo-50 to-purple-50 rounded-3xl flex flex-col items-center justify-center shadow-inner">
                    <img src="/assets/characters/popo.png" alt="포포" className={`w-28 h-28 object-contain mb-2 ${isAiSpeaking ? 'animate-bounce' : ''}`} />
                    <div className="bg-white/80 backdrop-blur-sm rounded-full px-4 py-1.5 shadow-sm">
                        <div className="flex items-center gap-1.5">
                            <span className="text-xs">💬</span>
                            <span className="text-xs font-semibold text-[var(--bt-text)]">
                                {isAiSpeaking ? '말하는 중...' : isRecording ? '듣고 있어!' : '나랑 대화하자!'}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Conversation Log */}
            <div className="flex-1 bg-[var(--bt-bg)] rounded-t-3xl px-4 pt-4 pb-32 overflow-y-auto">
                <p className="text-[10px] font-semibold text-[var(--bt-text-muted)] text-center tracking-widest uppercase mb-4">
                    Conversation Log
                </p>

                <div className="flex flex-col gap-3">
                    {messages.length === 0 && (
                        <p className="text-sm text-[var(--bt-text-muted)] text-center py-8">
                            마이크 버튼을 눌러 포포와 대화해보세요!
                        </p>
                    )}

                    {messages.map((msg) => {
                        // R3: Mood Check-in UI
                        if (msg.uiType === 'mood_checkin') {
                            return (
                                <div key={msg.id} className="self-center w-full max-w-[90%]">
                                    <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 rounded-2xl p-4 text-center">
                                        <p className="text-sm font-bold text-[var(--bt-text)] mb-3 whitespace-pre-line">{msg.text}</p>
                                        <div className="flex gap-2 justify-center">
                                            {([1, 2, 3] as const).map((score) => (
                                                <button
                                                    key={score}
                                                    onClick={() => sendMood(score)}
                                                    className="flex-1 py-3 rounded-xl font-bold text-lg transition-all active:scale-95 hover:brightness-110 shadow-sm"
                                                    style={{
                                                        background: score === 1 ? '#e0e7ff' : score === 2 ? '#fef3c7' : '#d1fae5',
                                                        color: score === 1 ? '#4338ca' : score === 2 ? '#92400e' : '#065f46',
                                                    }}
                                                >
                                                    {score === 1 ? '😔 1' : score === 2 ? '😊 2' : '🤩 3'}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            );
                        }

                        // R0: Mission Call UI
                        if (msg.uiType === 'mission_call') {
                            return (
                                <div key={msg.id} className="self-center w-full max-w-[90%]">
                                    <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-300 rounded-2xl p-4 text-center">
                                        <span className="text-3xl block mb-2">🚀</span>
                                        <p className="text-sm font-bold text-[var(--bt-text)] leading-relaxed">{msg.text}</p>
                                    </div>
                                </div>
                            );
                        }

                        // Safety Pass UI
                        if (msg.uiType === 'safety_pass') {
                            return (
                                <div key={msg.id} className="self-start max-w-[85%]">
                                    <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300 rounded-2xl px-4 py-3 rounded-tl-md">
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className="text-lg">🛡️</span>
                                            <span className="text-[10px] font-bold text-green-700">포포가 도와줄게!</span>
                                        </div>
                                        <p className="text-sm leading-relaxed text-[var(--bt-text)]">{msg.text}</p>
                                    </div>
                                </div>
                            );
                        }

                        // R4: Closing Ritual UI
                        if (msg.uiType === 'closing_ritual') {
                            return (
                                <div key={msg.id} className="self-center w-full max-w-[90%]">
                                    <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-300 rounded-2xl p-4 text-center">
                                        <span className="text-3xl block mb-2">✊</span>
                                        <p className="text-lg font-extrabold text-[var(--bt-text)]">{msg.text}</p>
                                        <p className="text-xs text-[var(--bt-text-secondary)] mt-2">오늘도 멋진 모험이었어!</p>
                                    </div>
                                </div>
                            );
                        }

                        // User messages
                        if (msg.role === 'user') {
                            return (
                                <div key={msg.id} className="max-w-[85%] self-end">
                                    <p className="text-[10px] font-semibold text-[var(--bt-text-muted)] mb-1 mr-1 text-right">나</p>
                                    <div className="rounded-2xl px-4 py-3 bg-[var(--bt-primary)] text-white rounded-tr-md">
                                        <p className="text-sm leading-relaxed">{msg.text}</p>
                                    </div>
                                </div>
                            );
                        }

                        // Assistant messages — parse character tags
                        const segments = parseCharacterSegments(msg.text);
                        return (
                            <div key={msg.id} className="self-start max-w-[85%] flex flex-col gap-2">
                                {segments.map((seg, idx) => {
                                    const style = SPEAKER_STYLES[seg.speaker];
                                    return (
                                        <div key={`${msg.id}-${idx}`} className="flex items-end gap-2">
                                            <div className={`w-7 h-7 rounded-full ${style.avatarBg} flex items-center justify-center text-xs flex-shrink-0 overflow-hidden`}>
                                                {style.img ? <img src={style.img} alt={style.label} className="w-full h-full object-cover" /> : style.emoji}
                                            </div>
                                            <div>
                                                {style.label && <p className="text-[10px] font-semibold text-[var(--bt-text-muted)] mb-0.5 ml-1">{style.label}</p>}
                                                <div className={`rounded-2xl rounded-tl-md px-4 py-3 border ${style.bg} ${style.border} text-[var(--bt-text)]`}>
                                                    <p className="text-sm leading-relaxed">{seg.text}</p>
                                                </div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        );
                    })}
                    <div ref={logEndRef} />
                </div>

                {/* Adventure CTA */}
                <button
                    onClick={() => navigate('/kid/adventures')}
                    className="w-full mt-6 bt-card p-4 flex items-center justify-between"
                >
                    <div className="flex items-center gap-2">
                        <span className="text-lg">✨</span>
                        <span className="font-bold text-[var(--bt-text)]">모험 떠나기</span>
                    </div>
                    <ChevronRight size={20} className="text-[var(--bt-text-muted)]" />
                </button>
            </div>

            {/* Floating Mic Button — above BottomNav (80px) */}
            <div className="fixed bottom-[100px] left-1/2 -translate-x-1/2 z-30 flex flex-col items-center gap-2">
                {isConnecting && (
                    <span className="text-xs text-[var(--bt-text-muted)] bg-white/90 rounded-full px-3 py-1 shadow">
                        연결 중...
                    </span>
                )}
                <button
                    onClick={toggleRecording}
                    disabled={!isConnected && !isRecording}
                    className={`w-16 h-16 rounded-full flex items-center justify-center shadow-lg transition-all disabled:opacity-40 ${
                        isRecording
                            ? 'bg-red-500 scale-110 animate-pulse'
                            : isAiSpeaking
                              ? 'bg-amber-400 border-2 border-amber-500'
                              : 'bg-white border-2 border-[var(--bt-border)]'
                    }`}
                >
                    {isConnecting ? (
                        <Loader2 size={28} className="text-[var(--bt-primary)] animate-spin" />
                    ) : !isConnected ? (
                        <MicOff size={28} className="text-gray-400" />
                    ) : isRecording ? (
                        <Mic size={28} className="text-white" />
                    ) : (
                        <Mic size={28} className="text-[var(--bt-primary)]" />
                    )}
                </button>
            </div>
        </div>
    );
}
