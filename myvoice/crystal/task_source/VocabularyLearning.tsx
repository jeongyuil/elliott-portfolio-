/**
 * VocabularyLearning Page - Mobile Optimized (No Header)
 * Design Philosophy: Flashcard-style word learning with pronunciation evaluation
 * - Navigation integrated into main content
 * - Fixed navigation buttons at bottom
 */

import { useState } from "react";
import { useRoute, useLocation } from "wouter";
import { Volume2, Mic, ArrowLeft, ArrowRight, CheckCircle } from "lucide-react";
import { toast } from "sonner";
import { vocabularyCategories } from "@/lib/mockData";
import {
  startSpeechRecognition,
  isSpeechRecognitionSupported,
  PronunciationResult,
} from "@/lib/speechRecognition";

// Sample vocabulary data
const vocabularyData: Record<string, Array<{ word: string; korean: string; emoji: string }>> = {
  food: [
    { word: "Apple", korean: "사과", emoji: "🍎" },
    { word: "Banana", korean: "바나나", emoji: "🍌" },
    { word: "Orange", korean: "오렌지", emoji: "🍊" },
    { word: "Bread", korean: "빵", emoji: "🍞" },
    { word: "Milk", korean: "우유", emoji: "🥛" },
    { word: "Water", korean: "물", emoji: "💧" },
    { word: "Rice", korean: "쌀", emoji: "🍚" },
    { word: "Egg", korean: "달걀", emoji: "🥚" },
    { word: "Fish", korean: "물고기", emoji: "🐟" },
    { word: "Chicken", korean: "닭고기", emoji: "🍗" },
  ],
  animals: [
    { word: "Dog", korean: "개", emoji: "🐶" },
    { word: "Cat", korean: "고양이", emoji: "🐱" },
    { word: "Bird", korean: "새", emoji: "🐦" },
    { word: "Fish", korean: "물고기", emoji: "🐟" },
    { word: "Rabbit", korean: "토끼", emoji: "🐰" },
    { word: "Bear", korean: "곰", emoji: "🐻" },
    { word: "Lion", korean: "사자", emoji: "🦁" },
    { word: "Elephant", korean: "코끼리", emoji: "🐘" },
    { word: "Monkey", korean: "원숭이", emoji: "🐵" },
    { word: "Tiger", korean: "호랑이", emoji: "🐯" },
  ],
  colors: [
    { word: "Red", korean: "빨강", emoji: "🔴" },
    { word: "Blue", korean: "파랑", emoji: "🔵" },
    { word: "Green", korean: "초록", emoji: "🟢" },
    { word: "Yellow", korean: "노랑", emoji: "🟡" },
    { word: "Orange", korean: "주황", emoji: "🟠" },
    { word: "Purple", korean: "보라", emoji: "🟣" },
    { word: "Pink", korean: "분홍", emoji: "🩷" },
    { word: "Brown", korean: "갈색", emoji: "🟤" },
    { word: "Black", korean: "검정", emoji: "⚫" },
    { word: "White", korean: "하양", emoji: "⚪" },
  ],
};

export default function VocabularyLearning() {
  const [, params] = useRoute("/vocabulary/:category");
  const [, setLocation] = useLocation();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isListening, setIsListening] = useState(false);
  const [pronunciationResult, setPronunciationResult] = useState<PronunciationResult | null>(null);
  const [stopRecognition, setStopRecognition] = useState<(() => void) | null>(null);

  const category = vocabularyCategories.find((c) => c.id === params?.category);
  const words = vocabularyData[params?.category || "food"] || [];
  const currentWord = words[currentIndex];

  if (!category || words.length === 0) {
    return (
      <div className="h-screen flex items-center justify-center bg-[var(--duo-bg)]">
        <div className="text-center">
          <div className="text-6xl mb-4">🔍</div>
          <p className="text-[var(--duo-text-secondary)]">카테고리를 찾을 수 없습니다</p>
        </div>
      </div>
    );
  }

  const handleNext = () => {
    setPronunciationResult(null);
    if (currentIndex < words.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // Navigate to result page with rewards
      const wordsLearned = words.length;
      const stars = Math.floor(wordsLearned / 2); // 2 words = 1 star
      const xp = wordsLearned * 5; // 5 XP per word
      setLocation(`/vocabulary/${params?.category}/result?wordsLearned=${wordsLearned}&stars=${stars}&xp=${xp}`);
    }
  };

  const handlePrevious = () => {
    setPronunciationResult(null);
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleListen = () => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(currentWord.word);
      utterance.lang = 'en-US';
      utterance.rate = 0.8;
      window.speechSynthesis.speak(utterance);
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
    <div className="h-screen flex flex-col bg-[var(--duo-bg)] overflow-hidden">
      {/* Word Card - Centered with scrollable content */}
      <div className="flex-1 flex flex-col overflow-y-auto px-4 py-4">
        {/* Top Navigation */}
        <div className="flex items-center justify-between mb-3">
          <button onClick={() => setLocation("/vocabulary")} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <ArrowLeft size={20} className="text-[var(--duo-text)]" />
          </button>
          <div className="flex-1 mx-3">
            <div className="flex items-center justify-between text-sm mb-1">
              <span className="font-semibold text-[var(--duo-text)]">{category.name}</span>
              <span className="font-semibold text-[var(--duo-text-secondary)]">
                {currentIndex + 1}/{words.length}
              </span>
            </div>
            <div className="duo-progress">
              <div className="duo-progress-bar" style={{ width: `${progress}%` }} />
            </div>
          </div>
        </div>

        {/* Word Card */}
        <div className="flex-1 flex items-center justify-center">
          <div className="w-full max-w-md">
            <div className="duo-card p-6 text-center">
              {/* Emoji */}
              <div className="text-8xl mb-4">{currentWord.emoji}</div>
              
              {/* English Word */}
              <h2 className="text-3xl font-bold text-[var(--duo-text)] mb-2">
                {currentWord.word}
              </h2>
              
              {/* Korean Meaning */}
              <p className="text-lg text-[var(--duo-text-secondary)] mb-4">
                {currentWord.korean}
              </p>

              {/* Action Buttons */}
              <div className="flex gap-3 justify-center mb-4">
                <button
                  onClick={handleListen}
                  className="flex flex-col items-center gap-1 p-3 hover:bg-blue-50 rounded-xl transition-colors"
                >
                  <div className="w-14 h-14 rounded-full bg-blue-100 flex items-center justify-center">
                    <Volume2 size={24} className="text-[var(--duo-blue)]" />
                  </div>
                  <span className="text-xs font-semibold text-[var(--duo-text-secondary)]">듣기</span>
                </button>

                <button
                  onClick={isListening ? handleStopListening : handleSpeak}
                  className={`flex flex-col items-center gap-1 p-3 rounded-xl transition-colors ${
                    isListening 
                      ? "bg-red-50 hover:bg-red-100" 
                      : "hover:bg-green-50"
                  }`}
                >
                  <div className={`w-14 h-14 rounded-full flex items-center justify-center ${
                    isListening 
                      ? "bg-red-100 animate-pulse" 
                      : "bg-green-100"
                  }`}>
                    <Mic size={24} className={isListening ? "text-red-500" : "text-[var(--duo-green)]"} />
                  </div>
                  <span className="text-xs font-semibold text-[var(--duo-text-secondary)]">
                    {isListening ? "듣는 중" : "말하기"}
                  </span>
                </button>
              </div>

              {/* Pronunciation Result */}
              {pronunciationResult && (
                <div className={`rounded-xl p-3 mb-2 ${
                  pronunciationResult.isCorrect 
                    ? "bg-green-50 border-2 border-green-200" 
                    : "bg-orange-50 border-2 border-orange-200"
                }`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-sm font-bold ${
                      pronunciationResult.isCorrect ? "text-[var(--duo-green)]" : "text-orange-600"
                    }`}>
                      {pronunciationResult.feedback}
                    </span>
                    <span className={`text-base font-bold ${
                      pronunciationResult.isCorrect ? "text-[var(--duo-green)]" : "text-orange-600"
                    }`}>
                      {pronunciationResult.accuracy}%
                    </span>
                  </div>
                  {!pronunciationResult.isCorrect && (
                    <div className="text-xs text-[var(--duo-text-secondary)] text-left">
                      <p>들린 단어: <span className="font-semibold">"{pronunciationResult.recognized}"</span></p>
                    </div>
                  )}
                </div>
              )}

              {isListening && (
                <div className="bg-blue-50 rounded-xl p-2">
                  <p className="text-sm text-[var(--duo-blue)] font-semibold">
                    🎤 "{currentWord.word}" 라고 말해보세요
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between pt-3">
          <button
            onClick={handlePrevious}
            disabled={currentIndex === 0}
            className={`duo-btn-secondary flex items-center gap-2 ${
              currentIndex === 0 ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            <ArrowLeft size={18} />
            <span>이전</span>
          </button>

          <button
            onClick={handleNext}
            className="duo-btn-primary flex items-center gap-2"
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
