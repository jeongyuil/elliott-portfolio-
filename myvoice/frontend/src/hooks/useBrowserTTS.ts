
import { useState, useEffect, useRef } from "react";

interface SpeakOptions {
    onEnd?: () => void;
    rate?: number;
    pitch?: number;
    voiceName?: string; // 'Google US English', 'Google 한국의' etc.
}

export function useBrowserTTS() {
    const [speaking, setSpeaking] = useState(false);
    const synth = useRef<SpeechSynthesis>(window.speechSynthesis);

    useEffect(() => {
        // Ensure voices are loaded
        if (synth.current.onvoiceschanged !== undefined) {
            synth.current.onvoiceschanged = () => {
                // Voices loaded
            };
        }
    }, []);

    const speak = (text: string, options?: SpeakOptions) => {
        // Cancel previous
        cancel();

        const utterance = new SpeechSynthesisUtterance(text);

        // Pick voice
        const voices = synth.current.getVoices();
        let voice = null;
        if (options?.voiceName) {
            voice = voices.find(v => v.name === options.voiceName);
        }
        // Fallback: If Korean text
        if (!voice && /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(text)) {
            voice = voices.find(v => v.lang.includes("ko")) || null;
        }
        // Fallback: English
        if (!voice) {
            voice = voices.find(v => v.lang.includes("en-US")) || null;
        }
        if (voice) {
            utterance.voice = voice;
        }

        utterance.rate = options?.rate || 0.9;
        utterance.pitch = options?.pitch || 1.0;

        utterance.onstart = () => setSpeaking(true);
        utterance.onend = () => {
            setSpeaking(false);
            options?.onEnd?.();
        };
        utterance.onerror = (e) => {
            console.error("TTS Error:", e);
            setSpeaking(false);
        };

        synth.current.speak(utterance);
    };

    const cancel = () => {
        synth.current.cancel();
        setSpeaking(false);
    };

    return { speak, cancel, speaking };
}
