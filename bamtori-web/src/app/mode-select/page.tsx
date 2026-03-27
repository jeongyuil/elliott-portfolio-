"use client";

import { useRouter } from "next/navigation";
import { useApp } from "../../context/AppContext";
import MobileLayout from "../../components/MobileLayout";
import StarryBackground from "../../components/StarryBackground";

export default function ModeSelectPage() {
  const router = useRouter();
  const { setAppMode } = useApp();

  const handleParentMode = () => {
    alert("학부모 모드는 준비 중이에요!");
  };

  const handleChildMode = () => {
    setAppMode('child');
    router.push('/kid/home');
  };

  return (
    <div className="bg-[--color-bamtori-dark] min-h-dvh text-white font-sans overflow-x-hidden">
        <StarryBackground />
        
        <MobileLayout className="p-6 justify-center relative z-10">
            <header className="mb-10 text-center animate-float">
                <h1 className="text-3xl font-bold text-white mb-2">누가 사용하나요?</h1>
                <p className="text-gray-400 text-sm font-medium">
                    사용자에 맞는 화면으로 이동합니다
                </p>
            </header>

            <div className="space-y-6">
                {/* Child Mode Card */}
                <button 
                    onClick={handleChildMode}
                    className="w-full relative group overflow-hidden rounded-3xl p-1"
                >
                    <div className="absolute inset-0 bg-gradient-to-r from-[--color-bamtori-purple] to-[--color-bamtori-teal] opacity-70 blur-sm group-hover:opacity-100 transition-opacity" />
                    <div className="relative bg-[#1C2128] rounded-[22px] p-6 flex flex-col items-center text-center h-48 justify-center gap-3 transition-transform group-hover:scale-[0.98]">
                        <div className="text-5xl mb-2 animate-pulse-soft">🚀</div>
                        <div>
                            <h2 className="text-2xl font-bold text-white mb-1">아이 모드</h2>
                            <p className="text-[--color-bamtori-teal] text-sm">별이의 모험을 시작해요!</p>
                        </div>
                    </div>
                </button>

                {/* Parent Mode Card */}
                <button 
                    onClick={handleParentMode}
                    className="w-full relative group overflow-hidden rounded-3xl p-1"
                >
                    <div className="absolute inset-0 bg-gray-700 opacity-30 group-hover:opacity-50 transition-opacity" />
                    <div className="relative bg-[#0D1117] border border-[#30363D] rounded-[22px] p-6 flex flex-col items-center text-center h-48 justify-center gap-3 transition-transform group-hover:scale-[0.98]">
                        <div className="text-5xl mb-2 grayscale opacity-70">👨‍👩‍👧</div>
                        <div>
                            <h2 className="text-2xl font-bold text-gray-300 mb-1">학부모 모드</h2>
                            <p className="text-gray-500 text-sm">아이의 성장 리포트를 확인해요</p>
                        </div>
                    </div>
                </button>
            </div>

            <p className="text-center text-xs text-gray-500 mt-10">
                나중에 설정에서 변경할 수 있어요
            </p>
        </MobileLayout>
    </div>
  );
}
