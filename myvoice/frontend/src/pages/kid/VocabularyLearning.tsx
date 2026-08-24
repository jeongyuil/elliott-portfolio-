/**
 * VocabularyLearning Page
 * Flashcard-style word learning with TTS pronunciation and speech recognition
 */

import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Volume2, Mic, ArrowLeft, ArrowRight, CheckCircle, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/api/client";
import { AudioPlayer } from "@/lib/audioPlayer";
import {
    startSpeechRecognition,
    isSpeechRecognitionSupported,
    type PronunciationResult,
} from "@/lib/speechRecognition";
import type { VocabularyCategory, VocabularyWord } from "@/api/types";

export default function VocabularyLearning() {
    const { category: categoryId } = useParams();
    const navigate = useNavigate();
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isListening, setIsListening] = useState(false);
    const [isTtsLoading, setIsTtsLoading] = useState(false);
    const [pronunciationResult, setPronunciationResult] = useState<PronunciationResult | null>(null);
    const [stopRecognition, setStopRecognition] = useState<(() => void) | null>(null);
    const audioPlayerRef = useRef<AudioPlayer>(new AudioPlayer());

    // Load category info and words from API
    const [category, setCategory] = useState<VocabularyCategory | null>(null);
    const [words, setWords] = useState<VocabularyWord[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (!categoryId) return;
        let cancelled = false;

        (async () => {
            try {
                const [categories, wordList] = await Promise.all([
                    api.get<VocabularyCategory[]>('/v1/kid/vocabulary'),
                    api.get<VocabularyWord[]>(`/v1/kid/vocabulary/${categoryId}/words`),
                ]);
                if (cancelled) return;
                const cat = categories.find((c) => c.id === categoryId) || null;
                setCategory(cat);
                setWords(wordList);
            } catch {
                toast.error('단어를 불러올 수 없습니다.');
            } finally {
                if (!cancelled) setIsLoading(false);
            }
        })();

        return () => { cancelled = true; };
    }, [categoryId]);

    const currentWord = words[currentIndex];

    if (isLoading) {
        return (
            <div className="h-full flex items-center justify-center bg-[var(--bt-bg)]">
                <Loader2 size={32} className="text-[var(--bt-primary)] animate-spin" />
            </div>
        );
    }

    if (!category || words.length === 0) {
        return (
            <div className="h-full flex items-center justify-center bg-[var(--bt-bg)]">
                <div className="text-center">
                    <div className="text-6xl mb-4">🔍</div>
                    <p className="text-[var(--bt-text-secondary)]">단어가 아직 준비되지 않았어요</p>
                    <button
                        onClick={() => navigate('/kid/vocabulary')}
                        className="mt-4 px-4 py-2 bg-[var(--bt-primary)] text-white rounded-lg"
                    >
                        돌아가기
                    </button>
                </div>
            </div>
        );
    }

    const handleNext = () => {
        setPronunciationResult(null);
        if (currentIndex < words.length - 1) {
            setCurrentIndex(currentIndex + 1);
        } else {
            const wordsLearned = words.length;
            const stars = Math.floor(wordsLearned / 2);
            const xp = wordsLearned * 5;
            navigate(`/kid/vocabulary/${categoryId}/result?wordsLearned=${wordsLearned}&stars=${stars}&xp=${xp}`);
        }
    };

    const handlePrevious = () => {
        setPronunciationResult(null);
        if (currentIndex > 0) {
            setCurrentIndex(currentIndex - 1);
        }
    };

    const handleListen = async () => {
        if (isTtsLoading) return;
        setIsTtsLoading(true);

        try {
            const res = await api.post<{ audioBase64: string }>(
                '/v1/kid/vocabulary/tts',
                { text: currentWord.word },
            );
            if (res.audioBase64) {
                audioPlayerRef.current.playBase64(res.audioBase64);
            }
        } catch {
            // Fallback to browser TTS
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(currentWord.word);
                utterance.lang = 'en-US';
                utterance.rate = 0.8;
                window.speechSynthesis.speak(utterance);
            } else {
                toast.error("음성을 재생할 수 없습니다.");
            }
        } finally {
            setIsTtsLoading(false);
        }
    };

    const handleSpeak = () => {
        if (!isSpeechRecognitionSupported()) {
            toast.error("음성 인식 미지원", {
                description: "Chrome 브라우저를 사용해주세요.",
            });
            return;
        }

        setIsListening(true);
        setPronunciationResult(null);

        const stop = startSpeechRecognition(
            currentWord.word,
            (result) => {
                setIsListening(false);
                setPronunciationResult(result);

                if (result.isCorrect) {
                    toast.success(result.feedback, {
                        description: `정확도: ${result.accuracy}%`,
                    });
                } else {
                    toast.error(result.feedback, {
                        description: `들린 단어: "${result.recognized}"`,
                    });
                }
            },
            (error) => {
                setIsListening(false);
                toast.error("음성 인식 오류", {
                    description: error,
                });
            }
        );

        setStopRecognition(() => stop);
    };

    const handleStopListening = () => {
        if (stopRecognition) {
            stopRecognition();
            setStopRecognition(null);
        }
        setIsListening(false);
    };

    const progress = Math.round(((currentIndex + 1) / words.length) * 100);

    return (
        <div className="h-full flex flex-col bg-[var(--bt-bg)] overflow-hidden">
            <div className="flex-1 flex flex-col overflow-y-auto px-4 py-4 pb-24">
                {/* Top Navigation */}
                <div className="flex items-center justify-between mb-3">
                    <button onClick={() => navigate("/kid/vocabulary")} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                        <ArrowLeft size={20} className="text-[var(--bt-text)]" />
                    </button>
                    <div className="flex-1 mx-3">
                        <div className="flex items-center justify-between text-sm mb-1">
                            <span className="font-semibold text-[var(--bt-text)]">{category.name}</span>
                            <span className="font-semibold text-[var(--bt-text-secondary)]">
                                {currentIndex + 1}/{words.length}
                            </span>
                        </div>
                        <div className="bt-progress">
                            <div className="bt-progress-bar" style={{ width: `${progress}%` }} />
                        </div>
                    </div>
                </div>

                {/* Word Card */}
                <div className="flex-1 flex items-center justify-center">
                    <div className="w-full max-w-md">
                        <div className="bt-card p-6 text-center">
                            <div className="text-8xl mb-4 animate-bounce-in">{currentWord.emoji}</div>

                            <h2 className="text-3xl font-bold text-[var(--bt-text)] mb-2">
                                {currentWord.word}
                            </h2>

                            <p className="text-lg text-[var(--bt-text-secondary)] mb-4">
                                {currentWord.korean}
                            </p>

                            {/* Action Buttons */}
                            <div className="flex gap-3 justify-center mb-4">
                                <button
                                    onClick={handleListen}
                                    disabled={isTtsLoading}
                                    className="flex flex-col items-center gap-1 p-3 hover:bg-blue-50 rounded-xl transition-colors"
                                >
                                    <div className="w-14 h-14 rounded-full bg-blue-100 flex items-center justify-center shadow-sm active:translate-y-0.5 active:shadow-none transition-all">
                                        {isTtsLoading ? (
                                            <Loader2 size={24} className="text-[var(--bt-accent)] animate-spin" />
                                        ) : (
                                            <Volume2 size={24} className="text-[var(--bt-accent)]" />
                                        )}
                                    </div>
                                    <span className="text-xs font-semibold text-[var(--bt-text-secondary)]">듣기</span>
                                </button>

                                <button
                                    onClick={isListening ? handleStopListening : handleSpeak}
                                    className={`flex flex-col items-center gap-1 p-3 rounded-xl transition-colors group ${isListening
                                        ? "bg-red-50 hover:bg-red-100"
                                        : "hover:bg-green-50"
                                        }`}
                                >
                                    <div className={`w-14 h-14 rounded-full flex items-center justify-center shadow-sm active:translate-y-0.5 active:shadow-none transition-all ${isListening
                                        ? "bg-red-100 animate-pulse"
                                        : "bg-green-100 group-hover:bg-green-200"
                                        }`}>
                                        <Mic size={24} className={isListening ? "text-red-500" : "text-[var(--bt-primary)]"} />
                                    </div>
                                    <span className="text-xs font-semibold text-[var(--bt-text-secondary)]">
                                        {isListening ? "듣는 중" : "말하기"}
                                    </span>
                                </button>
                            </div>

                            {/* Pronunciation Result */}
                            {pronunciationResult && (
                                <div className={`rounded-xl p-3 mb-2 animate-scale-in ${pronunciationResult.isCorrect
                                    ? "bg-green-50 border-2 border-green-200"
                                    : "bg-orange-50 border-2 border-orange-200"
                                    }`}>
                                    <div className="flex items-center justify-between mb-1">
                                        <span className={`text-sm font-bold ${pronunciationResult.isCorrect ? "text-[var(--bt-primary)]" : "text-orange-600"
                                            }`}>
                                            {pronunciationResult.feedback}
                                        </span>
                                        <span className={`text-base font-bold ${pronunciationResult.isCorrect ? "text-[var(--bt-primary)]" : "text-orange-600"
                                            }`}>
                                            {pronunciationResult.accuracy}%
                                        </span>
                                    </div>
                                    {!pronunciationResult.isCorrect && (
                                        <div className="text-xs text-[var(--bt-text-secondary)] text-left">
                                            <p>들린 단어: <span className="font-semibold">"{pronunciationResult.recognized}"</span></p>
                                        </div>
                                    )}
                                </div>
                            )}

                            {isListening && (
                                <div className="bg-blue-50 rounded-xl p-2 animate-pulse">
                                    <p className="text-sm text-[var(--bt-accent)] font-semibold">
                                        🎤 "{currentWord.word}" 라고 말해보세요
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Navigation Buttons */}
                <div className="flex items-center justify-between pt-3 mt-auto">
                    <button
                        onClick={handlePrevious}
                        disabled={currentIndex === 0}
                        className={`bt-btn-secondary flex items-center gap-2 ${currentIndex === 0 ? "opacity-50 cursor-not-allowed" : ""
                            }`}
                    >
                        <ArrowLeft size={18} />
                        <span>이전</span>
                    </button>

                    <button
                        onClick={handleNext}
                        className="bt-btn-primary flex items-center gap-2"
                    >
                        <span>{currentIndex === words.length - 1 ? "완료" : "다음"}</span>
                        {currentIndex === words.length - 1 ? (
                            <CheckCircle size={18} />
                        ) : (
                            <ArrowRight size={18} />
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
