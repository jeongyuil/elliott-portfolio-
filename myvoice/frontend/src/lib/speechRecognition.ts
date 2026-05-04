/**
 * Speech Recognition Utility
 * Provides pronunciation evaluation using Web Speech API
 */

export interface PronunciationResult {
    recognized: string;
    expected: string;
    accuracy: number;
    feedback: string;
    isCorrect: boolean;
}

/**
 * Calculate pronunciation accuracy using Levenshtein distance
 */
function calculateSimilarity(str1: string, str2: string): number {
    const s1 = str1.toLowerCase().trim();
    const s2 = str2.toLowerCase().trim();

    // Exact match
    if (s1 === s2) return 100;

    // Calculate Levenshtein distance
    const matrix: number[][] = [];

    for (let i = 0; i <= s2.length; i++) {
        matrix[i] = [i];
    }

    for (let j = 0; j <= s1.length; j++) {
        matrix[0][j] = j;
    }

    for (let i = 1; i <= s2.length; i++) {
        for (let j = 1; j <= s1.length; j++) {
            if (s2.charAt(i - 1) === s1.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j] + 1
                );
            }
        }
    }

    const distance = matrix[s2.length][s1.length];
    const maxLength = Math.max(s1.length, s2.length);
    const similarity = ((maxLength - distance) / maxLength) * 100;

    return Math.round(similarity);
}

/**
 * Get feedback message based on accuracy
 */
function getFeedback(accuracy: number): string {
    if (accuracy >= 95) {
        return "완벽해요! 🌟";
    } else if (accuracy >= 85) {
        return "아주 잘했어요! 👏";
    } else if (accuracy >= 70) {
        return "좋아요! 조금만 더 연습해봐요 💪";
    } else if (accuracy >= 50) {
        return "괜찮아요! 다시 한 번 시도해봐요 🎯";
    } else {
        return "다시 천천히 말해볼까요? 😊";
    }
}

/**
 * Evaluate pronunciation against expected word
 */
export function evaluatePronunciation(
    recognized: string,
    expected: string
): PronunciationResult {
    const accuracy = calculateSimilarity(recognized, expected);
    const isCorrect = accuracy >= 70; // 70% threshold for correct

    return {
        recognized: recognized.trim(),
        expected: expected.trim(),
        accuracy,
        feedback: getFeedback(accuracy),
        isCorrect,
    };
}

/**
 * Start speech recognition for a specific word
 */
export function startSpeechRecognition(
    expectedWord: string,
    onResult: (result: PronunciationResult) => void,
    onError: (error: string) => void
): () => void {
    // Check browser support
    const SpeechRecognition =
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
        onError("음성 인식을 지원하지 않는 브라우저입니다. Chrome을 사용해주세요.");
        return () => { };
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.continuous = false;

    recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        const result = evaluatePronunciation(transcript, expectedWord);
        onResult(result);
    };

    recognition.onerror = (event: any) => {
        let errorMessage = "음성 인식 중 오류가 발생했습니다.";

        switch (event.error) {
            case "no-speech":
                errorMessage = "음성이 감지되지 않았습니다. 다시 시도해주세요.";
                break;
            case "audio-capture":
                errorMessage = "마이크를 찾을 수 없습니다.";
                break;
            case "not-allowed":
                errorMessage = "마이크 권한이 필요합니다.";
                break;
            case "network":
                errorMessage = "네트워크 오류가 발생했습니다.";
                break;
        }

        onError(errorMessage);
    };

    recognition.onend = () => {
        // Recognition ended
    };

    try {
        recognition.start();
    } catch (error) {
        onError("음성 인식을 시작할 수 없습니다.");
    }

    // Return stop function
    return () => {
        try {
            recognition.stop();
        } catch (error) {
            // Already stopped
        }
    };
}

/**
 * Check if speech recognition is supported
 */
export function isSpeechRecognitionSupported(): boolean {
    return !!(
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition
    );
}
