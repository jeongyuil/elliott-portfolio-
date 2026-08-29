import { Dialog, DialogContent, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight, X, Rocket, Target, Star, Heart, Trophy } from "lucide-react";
import { useState } from "react";

interface OnboardingTutorialProps {
  isOpen: boolean;
  onComplete: () => void;
  onSkip: () => void;
}

const tutorialSteps = [
  {
    icon: Rocket,
    title: "밤토리에 오신 것을 환영합니다!",
    description: "외계인 루나를 도와주며 재미있게 영어를 배워보세요. 게임처럼 즐기면서 자연스럽게 영어 실력이 쌓입니다!",
    emoji: "🚀",
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    icon: Target,
    title: "미션을 완료하세요",
    description: "루나가 지구에서 겪는 다양한 상황을 도와주세요. 각 미션을 완료하면 별과 경험치를 획득할 수 있어요!",
    emoji: "🎯",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    icon: Star,
    title: "별을 모아 아이템을 구매하세요",
    description: "미션과 어휘 학습으로 별을 모으고, 상점에서 파워업과 특별 아이템을 구매할 수 있어요.",
    emoji: "⭐",
    gradient: "from-yellow-500 to-orange-500",
  },
  {
    icon: Heart,
    title: "매일 로그인하고 보상을 받으세요",
    description: "매일 첫 로그인 시 별과 하트를 받을 수 있어요. 연속으로 로그인하면 보상이 점점 커집니다!",
    emoji: "❤️",
    gradient: "from-red-500 to-pink-500",
  },
  {
    icon: Trophy,
    title: "주간 목표를 달성하세요",
    description: "매주 XP, 미션, 학습 시간, 단어 목표를 설정하고 달성해보세요. 100% 달성 시 특별 보상이 기다립니다!",
    emoji: "🏆",
    gradient: "from-green-500 to-emerald-500",
  },
];

export default function OnboardingTutorial({ isOpen, onComplete, onSkip }: OnboardingTutorialProps) {
  const [currentStep, setCurrentStep] = useState(0);

  const handleNext = () => {
    if (currentStep < tutorialSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onComplete();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const step = tutorialSteps[currentStep];
  const Icon = step.icon;
  const isLastStep = currentStep === tutorialSteps.length - 1;

  return (
    <Dialog open={isOpen} onOpenChange={() => {}}>
      <DialogContent 
        className="sm:max-w-lg bg-white border-2 border-gray-200"
        onPointerDownOutside={(e) => e.preventDefault()}
        onEscapeKeyDown={(e) => e.preventDefault()}
      >
        {/* Hidden DialogTitle and DialogDescription for accessibility */}
        <DialogTitle className="sr-only">{step.title}</DialogTitle>
        <DialogDescription className="sr-only">{step.description}</DialogDescription>
        
        {/* Skip Button */}
        <button
          onClick={onSkip}
          className="absolute top-4 right-4 p-2 rounded-full hover:bg-gray-100 transition-colors z-10"
          title="건너뛰기"
        >
          <X size={20} className="text-gray-500" />
        </button>

        <div className="flex flex-col items-center gap-6 py-8 px-4">
          {/* Icon with Gradient Background */}
          <div className={`relative w-24 h-24 rounded-full bg-gradient-to-br ${step.gradient} flex items-center justify-center shadow-lg`}>
            <div className="absolute inset-0 rounded-full bg-white/20 animate-pulse"></div>
            <Icon className="w-12 h-12 text-white relative z-10" />
          </div>

          {/* Title */}
          <h2 className="text-2xl font-bold text-gray-900 text-center">
            {step.title}
          </h2>

          {/* Description */}
          <p className="text-base text-gray-600 text-center leading-relaxed max-w-md">
            {step.description}
          </p>

          {/* Emoji Illustration */}
          <div className="text-6xl animate-bounce">
            {step.emoji}
          </div>

          {/* Progress Dots */}
          <div className="flex items-center gap-2">
            {tutorialSteps.map((_, index) => (
              <div
                key={index}
                className={`h-2 rounded-full transition-all duration-300 ${
                  index === currentStep
                    ? "w-8 bg-gradient-to-r " + step.gradient
                    : "w-2 bg-gray-300"
                }`}
              />
            ))}
          </div>

          {/* Navigation Buttons */}
          <div className="flex items-center gap-3 w-full">
            {currentStep > 0 && (
              <Button
                onClick={handlePrevious}
                variant="outline"
                className="flex-1 py-6 text-base"
              >
                <ChevronLeft size={20} />
                이전
              </Button>
            )}
            <Button
              onClick={handleNext}
              className={`flex-1 py-6 text-base bg-gradient-to-r ${step.gradient} hover:opacity-90 text-white font-semibold shadow-lg`}
            >
              {isLastStep ? "시작하기" : "다음"}
              {!isLastStep && <ChevronRight size={20} />}
            </Button>
          </div>

          {/* Step Counter */}
          <p className="text-sm text-gray-500">
            {currentStep + 1} / {tutorialSteps.length}
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
}
