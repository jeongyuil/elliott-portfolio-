import { useState, useEffect } from 'react';

interface TypingTextProps {
    text: string;
    /** Characters per second (default: 30) */
    speed?: number;
    /** Called when typing animation completes */
    onComplete?: () => void;
    className?: string;
}

export default function TypingText({ text, speed = 30, onComplete, className }: TypingTextProps) {
    const [displayedLen, setDisplayedLen] = useState(0);

    useEffect(() => {
        setDisplayedLen(0);
    }, [text]);

    useEffect(() => {
        if (displayedLen >= text.length) {
            onComplete?.();
            return;
        }
        const timeout = setTimeout(() => {
            setDisplayedLen(prev => prev + 1);
        }, 1000 / speed);
        return () => clearTimeout(timeout);
    }, [displayedLen, text, speed, onComplete]);

    return (
        <p className={className}>
            {text.slice(0, displayedLen)}
            {displayedLen < text.length && (
                <span className="inline-block w-0.5 h-4 bg-current ml-0.5 animate-blink align-text-bottom" />
            )}
        </p>
    );
}
