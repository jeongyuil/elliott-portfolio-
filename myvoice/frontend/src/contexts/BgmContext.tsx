import { createContext, useContext, useRef, useState, useCallback, type ReactNode } from 'react';

interface BgmContextValue {
    play: (trackUrl?: string) => void;
    stop: () => void;
    toggleMute: () => void;
    isMuted: boolean;
    isPlaying: boolean;
}

const BgmContext = createContext<BgmContextValue | null>(null);

export function BgmProvider({ children }: { children: ReactNode }) {
    const audioRef = useRef<HTMLAudioElement | null>(null);
    const trackRef = useRef<string>('');
    const [isPlaying, setIsPlaying] = useState(false);
    const [isMuted, setIsMuted] = useState(false);

    const play = useCallback((trackUrl: string = '/assets/intro-bgm.mp3') => {
        if (!audioRef.current) {
            const audio = new Audio(trackUrl);
            audio.loop = true;
            audio.volume = 0.35;
            audio.muted = isMuted;
            audioRef.current = audio;
            trackRef.current = trackUrl;
        } else if (trackRef.current !== trackUrl) {
            audioRef.current.pause();
            audioRef.current.src = trackUrl;
            audioRef.current.load();
            trackRef.current = trackUrl;
        }

        const audio = audioRef.current;
        if (audio.paused) {
            audio.volume = 0.35;
            audio.play().then(() => setIsPlaying(true)).catch(() => {});
        }
    }, [isMuted]);

    const stop = useCallback(() => {
        const audio = audioRef.current;
        if (!audio || audio.paused) {
            setIsPlaying(false);
            return;
        }

        const fadeOut = setInterval(() => {
            if (audio.volume > 0.03) {
                audio.volume = Math.max(0, audio.volume - 0.03);
            } else {
                audio.pause();
                audio.currentTime = 0;
                audio.volume = 0.35;
                clearInterval(fadeOut);
                setIsPlaying(false);
            }
        }, 40);
    }, []);

    const toggleMute = useCallback(() => {
        const audio = audioRef.current;
        setIsMuted(m => {
            const nextMuted = !m;
            if (audio) {
                audio.muted = nextMuted;
            }
            return nextMuted;
        });
    }, []);

    return (
        <BgmContext.Provider value={{ play, stop, toggleMute, isMuted, isPlaying }}>
            {children}
        </BgmContext.Provider>
    );
}

export function useBgm() {
    const ctx = useContext(BgmContext);
    if (!ctx) throw new Error('useBgm must be used within BgmProvider');
    return ctx;
}
