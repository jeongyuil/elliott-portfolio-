/**
 * Intro Page - Mobile game-style title screen
 *
 * Full-screen character illustration with:
 *   1. Image covers entire viewport (object-cover)
 *   2. Logo at top with glow
 *   3. "TAP TO START" blinking at bottom
 *   4. BGM auto-plays (Pixel Heartbeat) — continues through Landing & SelectChild
 *   5. Tap anywhere → navigate to login
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Volume2, VolumeX } from 'lucide-react';
import { useBgm } from '@/contexts/BgmContext';

// Pre-generate star positions so they don't change on re-render
const STARS = Array.from({ length: 40 }, (_, i) => ({
    id: i,
    size: Math.random() * 2.5 + 1,
    x: Math.random() * 100,
    y: Math.random() * 45,
    opacity: Math.random() * 0.6 + 0.3,
    duration: Math.random() * 3 + 2,
    delay: Math.random() * 3,
}));

const FIREFLIES = Array.from({ length: 8 }, (_, i) => ({
    id: i,
    x: 10 + Math.random() * 80,
    y: 20 + Math.random() * 60,
    duration: 3 + Math.random() * 4,
    delay: Math.random() * 5,
}));

export default function Intro() {
    const navigate = useNavigate();
    const bgm = useBgm();

    const [ready, setReady] = useState(false);
    const [showTitle, setShowTitle] = useState(false);
    const [showCta, setShowCta] = useState(false);
    const [isExiting, setIsExiting] = useState(false);

    // Phase progression
    useEffect(() => {
        const t1 = setTimeout(() => setReady(true), 400);
        const t2 = setTimeout(() => setShowTitle(true), 1200);
        const t3 = setTimeout(() => setShowCta(true), 2500);
        return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); };
    }, []);

    // Try autoplay BGM
    useEffect(() => {
        bgm.play();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const handleTap = () => {
        if (isExiting) return;

        // First tap: start BGM (browser requires user gesture for audio)
        if (!bgm.isPlaying) {
            bgm.play();
            return;
        }

        if (!showCta) return;
        setIsExiting(true);

        // Navigate after exit animation — BGM keeps playing
        setTimeout(() => navigate('/landing'), 600);
    };

    return (
        <div
            className={`fixed inset-0 overflow-hidden bg-[#060618] select-none cursor-pointer transition-opacity duration-500 ${
                isExiting ? 'opacity-0' : 'opacity-100'
            }`}
            onClick={handleTap}
        >
            {/* ── Full-screen character illustration ── */}
            <div className={`absolute inset-0 transition-all duration-[2000ms] ease-out ${
                ready ? 'opacity-100 scale-100' : 'opacity-0 scale-110'
            }`}>
                <img
                    src="/assets/bamtori-intro.png"
                    alt="밤토리"
                    className="absolute inset-0 w-full h-full object-cover object-center"
                    draggable={false}
                />

                {/* Top gradient — for title readability */}
                <div className="absolute inset-x-0 top-0 h-[35%] bg-gradient-to-b from-[#060618] via-[#060618]/60 to-transparent" />

                {/* Bottom gradient — for CTA readability */}
                <div className="absolute inset-x-0 bottom-0 h-[30%] bg-gradient-to-t from-[#060618] via-[#060618]/80 to-transparent" />
            </div>

            {/* ── Stars (above gradient, behind text) ── */}
            <div className={`absolute inset-0 pointer-events-none transition-opacity duration-[2000ms] ${
                ready ? 'opacity-100' : 'opacity-0'
            }`}>
                {STARS.map((s) => (
                    <div
                        key={s.id}
                        className="absolute rounded-full bg-white"
                        style={{
                            width: `${s.size}px`,
                            height: `${s.size}px`,
                            left: `${s.x}%`,
                            top: `${s.y}%`,
                            opacity: s.opacity,
                            animation: `twinkle ${s.duration}s ease-in-out infinite`,
                            animationDelay: `${s.delay}s`,
                        }}
                    />
                ))}
            </div>

            {/* ── Fireflies ── */}
            <div className={`absolute inset-0 pointer-events-none transition-opacity duration-[2000ms] ${
                ready ? 'opacity-100' : 'opacity-0'
            }`}>
                {FIREFLIES.map((f) => (
                    <div
                        key={`ff-${f.id}`}
                        className="absolute w-2 h-2 rounded-full"
                        style={{
                            background: 'radial-gradient(circle, rgba(255,223,100,0.9) 0%, transparent 70%)',
                            left: `${f.x}%`,
                            top: `${f.y}%`,
                            animation: `firefly ${f.duration}s ease-in-out infinite`,
                            animationDelay: `${f.delay}s`,
                        }}
                    />
                ))}
            </div>

            {/* ── Title area (top) ── */}
            <div className="absolute inset-x-0 top-0 z-10 flex flex-col items-center pt-[env(safe-area-inset-top,0px)]">
                <div className={`flex flex-col items-center pt-14 transition-all duration-[1500ms] ease-out ${
                    showTitle ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-8'
                }`}>
                    <h1
                        className="text-[3.2rem] font-black text-white tracking-tight leading-none"
                        style={{
                            textShadow: '0 0 60px rgba(139,92,246,0.6), 0 0 120px rgba(139,92,246,0.3), 0 4px 20px rgba(0,0,0,0.7)',
                        }}
                    >
                        밤토리
                    </h1>

                    <p
                        className={`text-sm text-indigo-200/80 mt-2.5 font-medium tracking-widest uppercase transition-all duration-[1200ms] delay-500 ${
                            showTitle ? 'opacity-100' : 'opacity-0'
                        }`}
                        style={{ textShadow: '0 2px 12px rgba(0,0,0,0.8)' }}
                    >
                        Bamtory
                    </p>

                    <p
                        className={`text-xs text-indigo-300/60 mt-1.5 transition-all duration-[1200ms] delay-700 ${
                            showTitle ? 'opacity-100' : 'opacity-0'
                        }`}
                        style={{ textShadow: '0 2px 12px rgba(0,0,0,0.8)' }}
                    >
                        밤하늘의 친구들과 떠나는 영어 모험
                    </p>
                </div>
            </div>

            {/* ── Bottom CTA area ── */}
            <div className="absolute inset-x-0 bottom-0 z-10 flex flex-col items-center pb-[env(safe-area-inset-bottom,0px)]">
                <div className={`flex flex-col items-center pb-16 transition-all duration-[1000ms] ${
                    showCta ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
                }`}>
                    {/* Tap to Start — game style blinking text */}
                    <p
                        className="text-lg font-bold tracking-[0.3em] uppercase animate-pulse-slow"
                        style={{
                            color: 'rgba(255,255,255,0.9)',
                            textShadow: '0 0 20px rgba(255,255,255,0.4), 0 0 40px rgba(139,92,246,0.3)',
                        }}
                    >
                        Tap to Start
                    </p>

                    {/* Subtle arrow hint */}
                    <div className="mt-3 animate-bounce-gentle">
                        <svg width="24" height="14" viewBox="0 0 24 14" fill="none">
                            <path d="M2 2L12 12L22 2" stroke="rgba(255,255,255,0.4)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </div>
                </div>
            </div>

            {/* ── Mute toggle ── */}
            <button
                onClick={(e) => {
                    e.stopPropagation();
                    bgm.play();
                    bgm.toggleMute();
                }}
                className={`absolute top-12 right-4 z-30 p-2.5 rounded-full backdrop-blur-sm transition-all ${
                    showTitle ? 'opacity-100' : 'opacity-0'
                } bg-black/30 hover:bg-black/50 active:scale-90`}
                aria-label={bgm.isMuted ? '소리 켜기' : '소리 끄기'}
            >
                {bgm.isMuted ? (
                    <VolumeX size={18} className="text-white/60" />
                ) : (
                    <Volume2 size={18} className="text-white/60" />
                )}
            </button>

            {/* ── Keyframe animations ── */}
            <style>{`
                @keyframes twinkle {
                    0%, 100% { opacity: 0.3; transform: scale(1); }
                    50% { opacity: 1; transform: scale(1.4); }
                }
                @keyframes firefly {
                    0%, 100% { transform: translate(0, 0); opacity: 0.2; }
                    25% { transform: translate(12px, -18px); opacity: 0.9; }
                    50% { transform: translate(-8px, -8px); opacity: 0.3; }
                    75% { transform: translate(16px, 6px); opacity: 0.8; }
                }
                @keyframes pulse-slow {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.3; }
                }
                .animate-pulse-slow {
                    animation: pulse-slow 2.5s ease-in-out infinite;
                }
                @keyframes bounce-gentle {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(6px); }
                }
                .animate-bounce-gentle {
                    animation: bounce-gentle 2s ease-in-out infinite;
                }
            `}</style>
        </div>
    );
}
