"use client";

import { useApp } from "../../../context/AppContext";
import MobileLayout from "../../../components/MobileLayout";
import StarryBackground from "../../../components/StarryBackground";
import { useRouter } from "next/navigation";

export default function KidHome() {
  const { childProfile, reset } = useApp();
  const router = useRouter();

  const handleReset = () => {
    reset();
    router.push('/');
  };

  return (
    <div className="bg-[--color-bamtori-dark] min-h-dvh text-white font-sans overflow-hidden">
      <StarryBackground />
      <MobileLayout className="items-center justify-center p-6 relative z-10 text-center">
        <div className="text-6xl mb-6 animate-float">🌰</div>
        <h1 className="text-3xl font-bold mb-4 text-[--color-bamtori-yellow]">
          반가워요, {childProfile?.name || '별이'}!
        </h1>
        <p className="text-[--color-bamtori-teal] text-lg mb-8">
          홈 화면 (Phase 2 준비 중)
        </p>
        
        <button 
          onClick={handleReset}
          className="px-6 py-3 rounded-full bg-[#1C2128] border border-gray-700 text-gray-400 text-sm hover:bg-[#30363D] transition-colors"
        >
          처음으로 돌아가기 (Reset)
        </button>
      </MobileLayout>
    </div>
  );
}
