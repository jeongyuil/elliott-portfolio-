/**
 * Adventure Play Page - Wireframe #8
 * 3-Phase curriculum flow:
 *   Phase 1: narrator_intro - Show narrator script + TTS, auto-advance
 *   Phase 2: transition - Show trigger word prompt ("Go!" button)
 *   Phase 3: interactive - Full voice conversation with AI
 */
import { useCallback, useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Clock, X, Mic, Loader2, Volume2, VolumeX, Play } from 'lucide-react';
import { toast } from 'sonner';
import { api } from '@/api/client';
import { useAdventureDetail } from '@/api/hooks/useAdventureDetail';
import { useAuth } from '@/contexts/AuthContext';
import { useBgm } from '@/contexts/BgmContext';
import { useVoiceWebSocket, type VoiceMessage } from '@/hooks/useVoiceWebSocket';
import { AudioPlayer } from '@/lib/audioPlayer';
import type { ActivityInfo, SessionStartResponse, SessionEndResponse } from '@/api/types';

import { parseCharacterSegments, SPEAKER_STYLES } from '@/lib/parseCharacterSegments';
import TypingText from '@/components/TypingText';

// Scene backgrounds based on adventure theme
const SCENE_BACKGROUNDS: Record<string, { from: string; via: string; to: string }> = {
    forest: { from: '#1a3a2a', via: '#1e4d3a', to: '#f1f5f9' },
    ocean: { from: '#0c2d4a', via: '#1a4b6e', to: '#f1f5f9' },
    space: { from: '#0a0a2e', via: '#1a1a4e', to: '#f1f5f9' },
    cave: { from: '#1a1a1a', via: '#2d2d3d', to: '#f1f5f9' },
    village: { from: '#4a3728', via: '#6b4f3a', to: '#f1f5f9' },
    default: { from: '#312e81', via: '#3730a3', to: '#f1f5f9' },
};

type Phase = 'narrator_intro' | 'transition' | 'interactive';

interface NarratorMessage {
    id: string;
    speaker: 'narrator' | 'user';
    /** Original character key for avatar/style mapping in intro */
    character?: 'narrator' | 'popo' | 'luna';
    text: string;
}

export default function AdventurePlay() {
    const { id } = useParams();
    const navigate = useNavigate();
    const { childToken, user } = useAuth();
    const bgm = useBgm();
    const { data: adventure, isLoading: isAdventureLoading } = useAdventureDetail(id!);

    // Fade out BGM when entering adventure
    useEffect(() => { bgm.stop(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

    // Sync narrator TTS mute state with global mute toggle
    useEffect(() => {
        narratorPlayerRef.current.muted = bgm.isMuted;
    }, [bgm.isMuted]);

    // Session State
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [activities, setActivities] = useState<ActivityInfo[]>([]);
    const [currentActivityIndex] = useState(0);
    const [timeLeft, setTimeLeft] = useState(600); // 10 minutes
    const [showQuitConfirm, setShowQuitConfirm] = useState(false);
    const [isQuitting, setIsQuitting] = useState(false);
    const [sessionEnded, setSessionEnded] = useState(false);

    // 3-Phase state
    const [phase, setPhase] = useState<Phase>('narrator_intro');
    const [narratorMessages, setNarratorMessages] = useState<NarratorMessage[]>([]);
    const [isNarratorSpeaking, setIsNarratorSpeaking] = useState(false);
    const narratorPlayerRef = useRef<AudioPlayer>(new AudioPlayer());
    const narratorMsgId = useRef(0);

    const scrollRef = useRef<HTMLDivElement>(null);
    const cancelledRef = useRef(false);
    const currentActivity = activities[currentActivityIndex];
    const [typedMessageIds, setTypedMessageIds] = useState<Set<string>>(new Set());
    const markTyped = useCallback((id: string) => {
        setTypedMessageIds(prev => new Set(prev).add(id));
    }, []);

    // WebSocket voice - only connect when in interactive phase
    const {
        messages,
        isRecording,
        isAiSpeaking,
        connectionState,
        goalAchieved,
        toggleRecording,
        sendMood,
        sendEnd,
    } = useVoiceWebSocket({
        sessionId: phase === 'interactive' ? sessionId : null,
        childToken,
        muted: bgm.isMuted,
    });

    // Goal achievement celebration banner
    const [showGoalBanner, setShowGoalBanner] = useState(false);
    useEffect(() => {
        if (goalAchieved && !showGoalBanner) {
            setShowGoalBanner(true);
        }
    }, [goalAchieved]); // eslint-disable-line react-hooks/exhaustive-deps

    // Auto-scroll on new messages
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, narratorMessages]);

    // Init Session
    useEffect(() => {
        if (!childToken || !id || sessionId) return;
        let cancelled = false;

        (async () => {
            try {
                const session = await api.post<SessionStartResponse>('/v1/kid/sessions', {
                    sessionType: 'curriculum',
                    curriculumUnitId: id,
                });
                if (!cancelled && session.sessionId) {
                    setSessionId(session.sessionId);
                    setActivities(session.activities || []);

                    // Start Phase 1: Narrator Intro
                    const firstActivity = (session.activities || [])[0];
                    if (firstActivity?.introNarratorScript) {
                        startNarratorIntro(session.sessionId, firstActivity);
                    } else {
                        // No narrator script - skip to interactive
                        setPhase('interactive');
                    }
                }
            } catch {
                toast.error('세션을 시작할 수 없습니다.');
                navigate('/kid/adventures');
            }
        })();

        return () => { cancelled = true; cancelledRef.current = true; };
    }, [childToken, id, sessionId, navigate]); // eslint-disable-line react-hooks/exhaustive-deps

    // Phase 1: Show narrator intro segment-by-segment with per-segment TTS
    const startNarratorIntro = async (sid: string, activity: ActivityInfo) => {
        setPhase('narrator_intro');
        let script = activity.introNarratorScript!;

        // Substitute {child_name} with actual child name
        const childName = user?.name || '캡틴';
        script = script.replace(/\{child_name\}/g, childName);

        // Parse segments using shared parser
        const segments = parseCharacterSegments(script);

        if (segments.length === 0) {
            setPhase('transition');
            return;
        }

        // Map speaker to TTS character and UI label
        const speakerToCharacter: Record<string, string> = {
            narrator: 'narrator', popo: 'popo', luna: 'luna', unknown: 'narrator',
        };
        const speakerToLabel: Record<string, string> = {
            narrator: '', popo: '🐾 포포: ', luna: '🌙 루나: ', unknown: '',
        };
        const speakerToUiRole = (_s: string): 'narrator' => 'narrator';

        setIsNarratorSpeaking(true);

        for (const seg of segments) {
            if (cancelledRef.current) return;
            const msgId = `narrator-${++narratorMsgId.current}`;
            const label = speakerToLabel[seg.speaker] || '';
            const charKey = (seg.speaker === 'popo' || seg.speaker === 'luna' || seg.speaker === 'narrator')
                ? seg.speaker : 'narrator' as const;
            const uiMsg: NarratorMessage = {
                id: msgId,
                speaker: speakerToUiRole(seg.speaker),
                character: charKey,
                text: label + seg.text,
            };

            // Show this segment's text
            setNarratorMessages(prev => [...prev, uiMsg]);

            // Request TTS for this segment
            const character = speakerToCharacter[seg.speaker] || 'narrator';
            try {
                const ttsRes = await api.post<{ audioBase64: string }>(
                    `/v1/kid/sessions/${sid}/tts`,
                    { text: seg.text, character },
                );
                if (ttsRes.audioBase64) {
                    // Play and wait for completion before showing next segment
                    await new Promise<void>((resolve) => {
                        narratorPlayerRef.current.playBase64(ttsRes.audioBase64, resolve);
                    });
                }
            } catch {
                // If TTS fails, pause briefly then continue to next segment
                await new Promise(r => setTimeout(r, 1500));
            }
        }

        setIsNarratorSpeaking(false);
        // Skip transition — go straight to interactive after intro
        setPhase('interactive');
    };

    // Phase 2: Handle "Go!" trigger
    const handleTriggerWord = () => {
        setNarratorMessages((prev) => [
            ...prev,
            { id: `narrator-${++narratorMsgId.current}`, speaker: 'user', text: 'Go!' },
        ]);
        setPhase('interactive');
    };

    // Timer — only counts down during interactive phase
    useEffect(() => {
        if (sessionEnded || phase !== 'interactive') return;
        const timer = setInterval(() => {
            setTimeLeft((prev) => {
                if (prev <= 1) {
                    clearInterval(timer);
                    endSessionAndNavigate(true, 0, 10);
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, [sessionEnded, phase]); // eslint-disable-line react-hooks/exhaustive-deps

    const endSessionAndNavigate = async (isSuccess: boolean, defaultXp = 0, defaultStars = 0) => {
        if (sessionEnded) return;
        setSessionEnded(true);
        narratorPlayerRef.current.stop();

        // Trigger R4 Closing Ritual via WebSocket if connected
        if (phase === 'interactive' && connectionState === 'connected') {
            sendEnd();
            // Brief delay to let closing ritual messages arrive
            await new Promise((r) => setTimeout(r, 3000));
        }

        let earnedXp = defaultXp;
        const earnedStars = defaultStars;
        if (sessionId) {
            try {
                const result = await api.post<SessionEndResponse>(`/v1/kid/sessions/${sessionId}/end`);
                earnedXp = result?.earnedXp ?? defaultXp;
            } catch {
                // Non-critical
            }
        }
        navigate(`/kid/adventure/${id}/result?success=${isSuccess}&stars=${earnedStars}&xp=${earnedXp}`);
    };

    const handleConfirmQuit = useCallback(async () => {
        setIsQuitting(true);
        await endSessionAndNavigate(false, 0, 0);
    }, [sessionEnded, sessionId, phase, connectionState]); // eslint-disable-line react-hooks/exhaustive-deps

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    const isConnected = connectionState === 'connected';
    const isConnecting = connectionState === 'connecting';

    if (isAdventureLoading || !adventure) {
        return (
            <div className="fixed inset-0 bg-[var(--bt-bg)] flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-[var(--bt-primary)] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    // Determine scene background from adventure title keywords
    const titleLower = (adventure?.title || '').toLowerCase();
    const sceneKey = titleLower.includes('forest') || titleLower.includes('숲') ? 'forest'
        : titleLower.includes('ocean') || titleLower.includes('바다') ? 'ocean'
        : titleLower.includes('space') || titleLower.includes('우주') ? 'space'
        : titleLower.includes('cave') || titleLower.includes('동굴') ? 'cave'
        : titleLower.includes('village') || titleLower.includes('마을') ? 'village'
        : 'default';
    const sceneBg = SCENE_BACKGROUNDS[sceneKey];

    return (
        <div
            className="fixed inset-0 flex flex-col z-50 transition-colors duration-1000"
            style={{ background: `linear-gradient(to bottom, ${sceneBg.from}, ${sceneBg.via}, ${sceneBg.to})` }}
        >
            {/* Stage Header */}
            <div className="flex-none px-4 py-3 flex items-center justify-between bg-indigo-900/80 backdrop-blur-sm">
                <div className="flex items-center gap-2 text-white font-bold text-sm">
                    <Clock size={16} />
                    {formatTime(timeLeft)}
                </div>

                {/* Progress */}
                <div className="flex-1 mx-3">
                    <div className="bg-white/20 h-2 rounded-full overflow-hidden">
                        <div
                            className="bg-[var(--bt-accent)] h-full transition-all duration-500 rounded-full"
                            style={{ width: `${phase === 'narrator_intro' ? 10 : phase === 'transition' ? 30 : activities.length ? ((currentActivityIndex + 1) / activities.length) * 100 : 50}%` }}
                        />
                    </div>
                    <p className="text-[10px] text-white/70 text-center mt-1">
                        {currentActivity
                            ? `STAGE ${currentActivityIndex + 1} — ${currentActivity.name}`
                            : phase === 'narrator_intro' ? '이야기 듣기' : phase === 'transition' ? '준비!' : '대화 중'}
                    </p>
                </div>

                <div className="flex items-center gap-1">
                    <button
                        onClick={bgm.toggleMute}
                        className="p-2 hover:bg-white/10 rounded-full transition-colors"
                        aria-label={bgm.isMuted ? '소리 켜기' : '소리 끄기'}
                    >
                        {bgm.isMuted
                            ? <VolumeX size={18} className="text-white/60" />
                            : <Volume2 size={18} className="text-white/80" />
                        }
                    </button>
                    <button
                        onClick={() => setShowQuitConfirm(true)}
                        className="p-2 hover:bg-white/10 rounded-full transition-colors"
                        aria-label="그만하기"
                    >
                        <X size={20} className="text-white/80" />
                    </button>
                </div>
            </div>

            {/* Avatar Area */}
            <div className="flex-none flex items-center justify-center gap-6 py-4 px-4">
                {/* Popo Avatar */}
                <div className={`flex flex-col items-center gap-1 transition-transform duration-300 ${
                    (phase === 'narrator_intro' && isNarratorSpeaking) || (phase === 'interactive' && isAiSpeaking) ? 'animate-avatar-speak' : ''
                }`}>
                    <div className={`w-16 h-16 rounded-full overflow-hidden shadow-lg border-2 transition-all ${
                        (phase === 'narrator_intro' && isNarratorSpeaking) || (phase === 'interactive' && isAiSpeaking)
                            ? 'border-[var(--bt-accent)] shadow-[var(--bt-accent)]/30 shadow-xl'
                            : 'border-white/40'
                    }`}>
                        <img src="/assets/characters/popo.png" alt="포포" className="w-full h-full object-cover" />
                    </div>
                    <span className="text-[10px] font-bold text-white/80">포포</span>
                    {((phase === 'narrator_intro' && isNarratorSpeaking) || (phase === 'interactive' && isAiSpeaking)) && (
                        <Volume2 size={10} className="text-[var(--bt-accent)] animate-pulse" />
                    )}
                </div>

                {/* Luna Avatar */}
                <div className="flex flex-col items-center gap-1">
                    <div className="w-16 h-16 rounded-full overflow-hidden shadow-lg border-2 border-purple-300">
                        <img src="/assets/characters/luna.png" alt="루나" className="w-full h-full object-cover" />
                    </div>
                    <span className="text-[10px] font-bold text-white/80">루나</span>
                </div>

                {/* Child Avatar */}
                <div className={`flex flex-col items-center gap-1 transition-transform duration-300 ${
                    isRecording ? 'animate-avatar-speak' : ''
                }`}>
                    <div className={`w-16 h-16 rounded-full overflow-hidden shadow-lg border-2 transition-all ${
                        isRecording ? 'border-red-400 shadow-red-400/30 shadow-xl' : 'border-white/40'
                    }`}>
                        <img src="/assets/characters/girl_captain.png" alt="캡틴" className="w-full h-full object-cover" />
                    </div>
                    <span className="text-[10px] font-bold text-white/80">나</span>
                </div>
            </div>

            {/* Conversation Area */}
            <div
                ref={scrollRef}
                className="flex-1 bg-[var(--bt-bg)] rounded-t-3xl overflow-y-auto px-4 pt-4 pb-36"
            >
                {/* Phase 1 & 2: Narrator messages */}
                {narratorMessages.length > 0 && (
                    <div className="flex flex-col gap-3 mb-4">
                        {narratorMessages.map((msg) => {
                            // Determine avatar and bubble style based on character
                            const char = msg.character || 'narrator';
                            const avatarConfig = {
                                narrator: { img: '', emoji: '📖', bg: 'bg-amber-100', bubble: 'bg-gradient-to-r from-slate-50 to-gray-50 border border-gray-200' },
                                popo: { img: '/assets/characters/popo.png', emoji: '', bg: 'bg-indigo-100', bubble: 'bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200' },
                                luna: { img: '/assets/characters/luna.png', emoji: '', bg: 'bg-purple-100', bubble: 'bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200' },
                            }[char];

                            return (
                                <div
                                    key={msg.id}
                                    className={`flex ${msg.speaker === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    {msg.speaker === 'narrator' && (
                                        <div className={`w-8 h-8 rounded-full overflow-hidden mr-2 flex-shrink-0 self-end flex items-center justify-center ${avatarConfig.bg}`}>
                                            {avatarConfig.img
                                                ? <img src={avatarConfig.img} alt={char} className="w-full h-full object-cover" />
                                                : <span className="text-sm">{avatarConfig.emoji}</span>
                                            }
                                        </div>
                                    )}
                                    <div
                                        className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                                            msg.speaker === 'narrator'
                                                ? `${avatarConfig.bubble} shadow-sm rounded-bl-md text-[var(--bt-text)]`
                                                : 'bg-[var(--bt-primary)] text-white rounded-br-md'
                                        }`}
                                    >
                                        {msg.speaker === 'narrator' && !typedMessageIds.has(msg.id) ? (
                                            <TypingText text={msg.text} speed={25} onComplete={() => markTyped(msg.id)} />
                                        ) : (
                                            <p>{msg.text}</p>
                                        )}
                                    </div>
                                    {msg.speaker === 'user' && (
                                        <div className="w-8 h-8 rounded-full overflow-hidden ml-2 flex-shrink-0 self-end">
                                            <img src="/assets/characters/girl_captain.png" alt="캡틴" className="w-full h-full object-cover" />
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                )}

                {/* Phase 2: Transition prompt */}
                {phase === 'transition' && (
                    <div className="flex flex-col items-center justify-center py-8 text-center">
                        <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-300 rounded-2xl p-6 mx-4 shadow-lg">
                            <span className="text-5xl block mb-3">🌟</span>
                            <h3 className="text-lg font-extrabold text-[var(--bt-text)] mb-2">
                                준비됐나요?
                            </h3>
                            <p className="text-sm text-[var(--bt-text-secondary)] mb-4">
                                포포와 대화를 시작하려면 아래 버튼을 눌러주세요!
                            </p>
                            <button
                                onClick={handleTriggerWord}
                                className="bg-[var(--bt-primary)] text-white font-extrabold py-3 px-8 rounded-xl text-lg hover:brightness-110 active:scale-95 transition-all flex items-center gap-2 mx-auto"
                            >
                                <Play size={20} fill="white" />
                                Go!
                            </button>
                        </div>
                    </div>
                )}

                {/* Phase 3: Interactive - WebSocket voice messages */}
                {phase === 'interactive' && (
                    <>
                        {messages.length === 0 && !isConnecting && (
                            <div className="flex flex-col items-center justify-center py-8 text-center">
                                <span className="text-4xl mb-3">🎙</span>
                                <p className="text-sm font-semibold text-[var(--bt-text-muted)]">
                                    마이크 버튼을 눌러 포포와 대화하세요!
                                </p>
                            </div>
                        )}

                        {isConnecting && messages.length === 0 && (
                            <div className="flex flex-col items-center justify-center py-8 text-center">
                                <Loader2 size={32} className="text-[var(--bt-primary)] animate-spin mb-3" />
                                <p className="text-sm text-[var(--bt-text-muted)]">포포와 연결하는 중...</p>
                            </div>
                        )}

                        <div className="flex flex-col gap-3">
                            {messages.map((msg: VoiceMessage) => {
                                // R3: Mood Check-in
                                if (msg.uiType === 'mood_checkin') {
                                    return (
                                        <div key={msg.id} className="flex justify-center">
                                            <div className="w-full max-w-[90%] bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 rounded-2xl p-4 text-center">
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

                                // R0: Mission Call
                                if (msg.uiType === 'mission_call') {
                                    return (
                                        <div key={msg.id} className="flex justify-center">
                                            <div className="w-full max-w-[90%] bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-300 rounded-2xl p-4 text-center">
                                                <span className="text-3xl block mb-2">🚀</span>
                                                <p className="text-sm font-bold text-[var(--bt-text)] leading-relaxed">{msg.text}</p>
                                            </div>
                                        </div>
                                    );
                                }

                                // Safety Pass
                                if (msg.uiType === 'safety_pass') {
                                    return (
                                        <div key={msg.id} className="flex justify-start">
                                            <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-sm mr-2 flex-shrink-0 self-end">
                                                🛡️
                                            </div>
                                            <div className="max-w-[75%] bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300 rounded-2xl px-4 py-3 rounded-bl-md">
                                                <div className="flex items-center gap-1 mb-1">
                                                    <span className="text-[10px] font-bold text-green-700">포포가 도와줄게!</span>
                                                </div>
                                                <p className="text-sm leading-relaxed text-[var(--bt-text)]">{msg.text}</p>
                                            </div>
                                        </div>
                                    );
                                }

                                // R4: Closing Ritual
                                if (msg.uiType === 'closing_ritual') {
                                    return (
                                        <div key={msg.id} className="flex justify-center">
                                            <div className="w-full max-w-[90%] bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-300 rounded-2xl p-4 text-center">
                                                <span className="text-3xl block mb-2">✊</span>
                                                <p className="text-lg font-extrabold text-[var(--bt-text)]">{msg.text}</p>
                                                <p className="text-xs text-[var(--bt-text-secondary)] mt-2">오늘도 멋진 모험이었어!</p>
                                            </div>
                                        </div>
                                    );
                                }

                                // Goal Achieved
                                if (msg.uiType === 'goal_achieved') {
                                    return (
                                        <div key={msg.id} className="flex justify-center">
                                            <div className="w-full max-w-[90%] bg-gradient-to-r from-yellow-50 to-amber-50 border-2 border-yellow-300 rounded-2xl p-4 text-center">
                                                <span className="text-3xl block mb-2">🎉</span>
                                                <p className="text-lg font-extrabold text-[var(--bt-text)]">{msg.text}</p>
                                            </div>
                                        </div>
                                    );
                                }

                                // User messages
                                if (msg.role === 'user') {
                                    return (
                                        <div key={msg.id} className="flex justify-end">
                                            <div className="max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed bg-[var(--bt-primary)] text-white rounded-br-md">
                                                <p>{msg.text}</p>
                                            </div>
                                            <div className="w-8 h-8 rounded-full overflow-hidden ml-2 flex-shrink-0 self-end">
                                                <img src="/assets/characters/girl_captain.png" alt="캡틴" className="w-full h-full object-cover" />
                                            </div>
                                        </div>
                                    );
                                }

                                // Assistant messages — parse [나레이션]/[포포]/[루나] tags
                                const segments = parseCharacterSegments(msg.text);
                                return (
                                    <div key={msg.id} className="flex flex-col gap-2">
                                        {segments.map((seg, idx) => {
                                            const style = SPEAKER_STYLES[seg.speaker];
                                            return (
                                                <div key={`${msg.id}-${idx}`} className="flex justify-start">
                                                    <div className={`w-8 h-8 rounded-full ${style.avatarBg} overflow-hidden flex items-center justify-center text-sm mr-2 flex-shrink-0 self-end`}>
                                                        {style.img ? <img src={style.img} alt={style.label} className="w-full h-full object-cover" /> : style.emoji}
                                                    </div>
                                                    <div className="max-w-[75%]">
                                                        {style.label && <p className="text-[10px] font-semibold text-[var(--bt-text-muted)] mb-0.5 ml-1">{style.label}</p>}
                                                        <div className={`px-4 py-3 rounded-2xl rounded-bl-md text-sm leading-relaxed border shadow-sm ${style.bg} ${style.border} text-[var(--bt-text)]`}>
                                                        {!typedMessageIds.has(`${msg.id}-${idx}`) ? (
                                                            <TypingText text={seg.text} speed={30} onComplete={() => markTyped(`${msg.id}-${idx}`)} />
                                                        ) : (
                                                            <p>{seg.text}</p>
                                                        )}
                                                        </div>
                                                    </div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                );
                            })}
                        </div>
                    </>
                )}
            </div>

            {/* Bottom Controls */}
            <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-t from-[var(--bt-bg)] via-[var(--bt-bg)] to-transparent pt-8 pb-8 flex flex-col items-center gap-2 z-10">
                {phase === 'narrator_intro' && (
                    <p className="text-xs text-[var(--bt-text-muted)]">
                        {isNarratorSpeaking ? '나레이션을 듣고 있어요...' : '잠시만 기다려 주세요...'}
                    </p>
                )}
                {phase === 'transition' && (
                    <p className="text-xs text-[var(--bt-text-muted)]">
                        위의 Go! 버튼을 눌러 시작하세요
                    </p>
                )}
                {phase === 'interactive' && (
                    <>
                        <p className="text-xs text-[var(--bt-text-muted)]">
                            {isRecording ? '녹음 중... 다시 누르면 전송돼요' : isAiSpeaking ? '포포가 말하고 있어요...' : '버튼을 눌러 말해보세요'}
                        </p>
                        <button
                            onClick={toggleRecording}
                            disabled={(!isConnected && !isRecording) || isAiSpeaking}
                            className={`w-20 h-20 rounded-full flex items-center justify-center shadow-lg transition-all disabled:opacity-40 ${
                                isRecording
                                    ? 'bg-red-500 scale-110 animate-pulse shadow-red-300/50'
                                    : isAiSpeaking
                                      ? 'bg-amber-400 cursor-not-allowed'
                                      : 'bg-[var(--bt-primary)] hover:scale-105 active:scale-95'
                            }`}
                            aria-label={isRecording ? '녹음 중지' : '녹음 시작'}
                        >
                            {isConnecting ? (
                                <Loader2 size={32} className="text-white animate-spin" />
                            ) : (
                                <Mic size={32} className="text-white" />
                            )}
                        </button>
                    </>
                )}
            </div>

            {/* Goal Achievement Celebration Overlay */}
            {showGoalBanner && (
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center z-30 animate-fade-in">
                    <div className="bg-white rounded-3xl p-8 mx-6 text-center shadow-2xl animate-bounce-in">
                        <div className="text-6xl mb-4">🎉</div>
                        <h2 className="text-2xl font-extrabold text-indigo-600 mb-2">미션 성공!</h2>
                        <p className="text-sm text-gray-500 mb-6">목표 표현을 잘 말했어요!</p>
                        <div className="space-y-3">
                            <button
                                onClick={() => setShowGoalBanner(false)}
                                className="w-full py-3 bg-indigo-500 text-white rounded-xl font-bold active:scale-95 transition-all"
                            >
                                계속 놀기 🎮
                            </button>
                            <button
                                onClick={() => { setShowGoalBanner(false); endSessionAndNavigate(true, 50, 10); }}
                                className="w-full py-3 bg-gray-100 text-gray-700 rounded-xl font-bold active:scale-95 transition-all"
                            >
                                미션 끝내기 ✨
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Quit Confirmation Overlay */}
            {showQuitConfirm && (
                <div className="absolute inset-0 bg-black/50 flex items-center justify-center z-20">
                    <div className="bg-white rounded-2xl p-6 mx-6 text-center shadow-2xl">
                        <p className="text-4xl mb-3">😢</p>
                        <h3 className="text-lg font-extrabold text-[var(--bt-text)] mb-2">그만할까요?</h3>
                        <p className="text-sm text-[var(--bt-text-secondary)] mb-5">
                            지금까지 한 대화는 저장돼요!
                        </p>
                        <div className="flex gap-3">
                            <button
                                onClick={() => setShowQuitConfirm(false)}
                                className="flex-1 py-3 rounded-xl border-2 border-gray-200 font-bold text-[var(--bt-text-secondary)]"
                            >
                                계속하기
                            </button>
                            <button
                                onClick={handleConfirmQuit}
                                disabled={isQuitting}
                                className="flex-1 py-3 rounded-xl bg-red-500 text-white font-bold disabled:opacity-50"
                            >
                                {isQuitting ? '저장 중...' : '그만하기'}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Animations */}
            <style>{`
                @keyframes avatar-speak {
                    0%, 100% { transform: translateY(0); }
                    25% { transform: translateY(-4px); }
                    50% { transform: translateY(0); }
                    75% { transform: translateY(-2px); }
                }
                .animate-avatar-speak {
                    animation: avatar-speak 0.8s ease-in-out infinite;
                }
                @keyframes blink {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0; }
                }
                .animate-blink {
                    animation: blink 0.8s step-end infinite;
                }
                @keyframes bounce-in {
                    0% { transform: scale(0.3); opacity: 0; }
                    50% { transform: scale(1.05); }
                    70% { transform: scale(0.95); }
                    100% { transform: scale(1); opacity: 1; }
                }
                .animate-bounce-in {
                    animation: bounce-in 0.5s ease-out;
                }
                @keyframes fade-in {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                .animate-fade-in {
                    animation: fade-in 0.3s ease-out;
                }
            `}</style>
        </div>
    );
}
