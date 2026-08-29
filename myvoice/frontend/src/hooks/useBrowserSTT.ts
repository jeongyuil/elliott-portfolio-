
import { useState, useRef, useEffect } from 'react';

// Extend window interface for webkitSpeechRecognition
declare global {
    interface Window {
        webkitSpeechRecognition: any;
    }
}

export function useBrowserSTT() {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState("");
    const [error, setError] = useState<string | null>(null);
    const recognitionRef = useRef<any>(null);

    useEffect(() => {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new window.webkitSpeechRecognition();
            recognition.continuous = false; // Stop after one sentence
            recognition.interimResults = false;
            recognition.lang = 'en-US'; // Default to English for learning

            recognition.onstart = () => {
                setIsListening(true);
                setError(null);
            };

            recognition.onend = () => {
                setIsListening(false);
            };

            recognition.onresult = (event: any) => {
                const text = event.results[0][0].transcript;
                setTranscript(text);
            };

            recognition.onerror = (event: any) => {
                console.error("STT Error:", event.error);
                setError(event.error);
                setIsListening(false);
            };

            recognitionRef.current = recognition;
        } else {
            setError("Browser not supported");
        }
    }, []);

    const startListening = (lang: string = 'en-US') => {
        if (recognitionRef.current) {
            recognitionRef.current.lang = lang;
            try {
                recognitionRef.current.start();
            } catch (e) {
                // Already started
                recognitionRef.current.stop();
                setTimeout(() => recognitionRef.current.start(), 100);
            }
        }
    };

    const stopListening = () => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
        }
    };

    return { isListening, transcript, startListening, stopListening, error, setTranscript };
}
