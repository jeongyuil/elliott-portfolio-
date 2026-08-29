/**
 * MissionPlay Page
 * Design Philosophy: Video call style interface with pronunciation evaluation
 * - Large character display (Luna)
 * - Scenario text with target word
 * - Real-time pronunciation feedback
 * - Timer and progress tracking
 */

import { useState, useEffect } from "react";
import { useRoute, useLocation } from "wouter";
import { X, Lightbulb, Mic, Clock, Timer } from "lucide-react";
import { toast } from "sonner";
import { missions } from "@/lib/mockData";
import {
  startSpeechRecognition,
  isSpeechRecognitionSupported,
  PronunciationResult,
} from "@/lib/speechRecognition";

export default function MissionPlay() {
  const [, params] = useRoute("/mission/:id/play");
  const [, setLocation] = useLocation();
  const [timeLeft, setTimeLeft] = useState(180); // 3 minutes
  const [isListening, setIsListening] = useState(false);
  const [pronunciationResult, setPronunciationResult] = useState<PronunciationResult | null>(null);
  const [attempts, setAttempts] = useState(0);
  const [stopRecognition, setStopRecognition] = useState<(() => void) | null>(null);

  const mission = missions.find((m) => m.id === Number(params?.id));

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          handleTimeout();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  if (!mission) {
    return (
      <div className="min-h-screen bg-[var(--duo-bg)] flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🔍</div>
          <p className="text-[var(--duo-text-secondary)]">미션을 찾을 수 없습니다</p>
        </div>
      </div>
    );
  }

  const handleTimeout = () => {
    toast.error("시간 초과!", {
      description: "다시 도전해보세요",
    });
    setTimeout(() => {
      setLocation(`/mission/${mission.id}/result?success=false`);
    }, 1000);
  };

  const handleGiveUp = () => {
    if (window.confirm("정말 포기하시겠어요?")) {
      setLocation("/home");
    }
  };

  const handleHint = () => {
    toast.info("힌트", {
      description: `"${mission.scenario.targetWord}" 라고 말해보세요!`,
    });
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
      mission.scenario.targetWord,
      (result) => {
        setIsListening(false);
        setPronunciationResult(result);
        setAttempts((prev) => prev + 1);

        if (result.isCorrect) {
          toast.success("성공! 🎉", {
            description: result.feedback,
          });
          
          // Wait a bit to show the result, then navigate
          setTimeout(() => {
            setLocation(`/mission/${mission.id}/result?success=true&stars=${mission.rewards.stars}&xp=${mission.rewards.xp}`);
          }, 1500);
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

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const difficultyClass = mission.difficulty === "쉬움" ? "easy" : mission.difficulty === "보통" ? "medium" : "hard";

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-purple-100 via-blue-50 to-pink-50 flex flex-col">
      {/* Top Bar */}
      <div className="bg-white/90 backdrop-blur-sm px-6 py-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-3">
          <Clock size={20} className="text-[var(--duo-blue)]" />
          <span className={`font-bold text-lg ${timeLeft < 30 ? "text-red-500 animate-pulse" : "text-[var(--duo-text)]"}`}>
            {formatTime(timeLeft)}
          </span>
        </div>
        <span className={`duo-badge ${difficultyClass}`}>{mission.difficulty}</span>
        <div className="flex items-center gap-2">
          <button onClick={handleHint} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <Lightbulb size={20} className="text-[var(--duo-yellow)]" />
          </button>
          <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <Timer size={20} className="text-[var(--duo-blue)]" />
          </button>
        </div>
      </div>

      {/* Main Content - Luna Video Area */}
      <div className="flex-1 relative flex items-center justify-center p-6 overflow-y-auto">
        <div className="text-center max-w-2xl w-full">
          {/* Luna Character */}
          <div className="text-9xl mb-4 animate-bounce-in">{mission.emoji}</div>
          
          {/* Scenario */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 mb-6">
            <p className="text-lg font-semibold text-[var(--duo-text)]">
              {mission.scenario.situation}
            </p>
          </div>

          {/* Pronunciation Result */}
          {pronunciationResult && (
            <div className={`rounded-xl p-4 mb-6 ${
              pronunciationResult.isCorrect 
                ? "bg-green-50 border-2 border-green-200" 
                : "bg-orange-50 border-2 border-orange-200"
            }`}>
              <div className="flex items-center justify-between mb-2">
                <span className={`text-sm font-bold ${
                  pronunciationResult.isCorrect ? "text-[var(--duo-green)]" : "text-orange-600"
                }`}>
                  {pronunciationResult.feedback}
                </span>
                <span className={`text-lg font-bold ${
                  pronunciationResult.isCorrect ? "text-[var(--duo-green)]" : "text-orange-600"
                }`}>
                  {pronunciationResult.accuracy}%
                </span>
              </div>
              {!pronunciationResult.isCorrect && (
                <div className="text-xs text-[var(--duo-text-secondary)] text-left">
                  <p>들린 단어: <span className="font-semibold">"{pronunciationResult.recognized}"</span></p>
                  <p>정답: <span className="font-semibold">"{pronunciationResult.expected}"</span></p>
                  <p className="mt-2 text-[var(--duo-text)]">💡 다시 시도해보세요! (시도: {attempts}회)</p>
                </div>
              )}
            </div>
          )}

          {isListening && (
            <div className="bg-blue-50 rounded-xl p-4 mb-6">
              <p className="text-sm text-[var(--duo-blue)] font-semibold">
                🎤 "{mission.scenario.targetWord}" 라고 말해보세요
              </p>
            </div>
          )}

          {/* Popo Speech Bubble */}
          <div className="duo-speech-bubble inline-block">
            <div className="flex items-start gap-3">
              <span className="text-3xl">🤖</span>
              <div>
                <p className="font-bold text-sm text-[var(--duo-text)] mb-1">포포</p>
                <p className="text-sm text-[var(--duo-text-secondary)]">
                  {mission.scenario.popoGuide}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Controls */}
      <div className="bg-white/90 backdrop-blur-sm px-6 py-6 flex items-center justify-center gap-6">
        <button
          onClick={handleGiveUp}
          className="flex flex-col items-center gap-2 p-4 hover:bg-red-50 rounded-2xl transition-colors"
        >
          <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
            <X size={24} className="text-[var(--duo-red)]" />
          </div>
          <span className="text-xs font-semibold text-[var(--duo-text-secondary)]">포기</span>
        </button>

        <button
          onClick={isListening ? handleStopListening : handleSpeak}
          className={`duo-mic-button ${isListening ? "animate-pulse-scale" : ""}`}
          disabled={isListening && !stopRecognition}
        >
          <Mic size={32} strokeWidth={2.5} />
        </button>

        <button 
          onClick={handleHint}
          className="flex flex-col items-center gap-2 p-4 hover:bg-yellow-50 rounded-2xl transition-colors"
        >
          <div className="w-12 h-12 rounded-full bg-yellow-100 flex items-center justify-center">
            <Lightbulb size={24} className="text-[var(--duo-yellow)]" />
          </div>
          <span className="text-xs font-semibold text-[var(--duo-text-secondary)]">힌트</span>
        </button>
      </div>

      {/* Listening Indicator */}
      {isListening && (
        <div className="absolute inset-0 bg-black/20 flex items-center justify-center pointer-events-none">
          <div className="bg-white rounded-3xl px-8 py-6 shadow-2xl">
            <div className="flex items-center gap-4">
              <div className="w-4 h-4 bg-[var(--duo-red)] rounded-full animate-pulse" />
              <span className="text-lg font-bold text-[var(--duo-text)]">듣고 있어요...</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
