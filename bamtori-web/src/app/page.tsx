"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useApp } from "../context/AppContext";
import StarryBackground from "../components/StarryBackground";
import MobileLayout from "../components/MobileLayout";

export default function LandingPage() {
  const { isLoggedIn, childProfile, subscription, mode, login } = useApp();
  const router = useRouter();

  useEffect(() => {
    if (isLoggedIn && childProfile && subscription && mode) {
        if (mode === 'child') {
            router.push('/kid/home');
        }
    }
  }, [isLoggedIn, childProfile, subscription, mode, router]);

  const handleLogin = () => {
    login();
    router.push('/onboarding/child-info');
  };

  return (
    <div className="bg-[--color-bamtori-dark] min-h-dvh text-white font-sans overflow-hidden">
      <StarryBackground />
      <MobileLayout className="justify-center p-6 relative z-10">
        <div className="flex-1 flex flex-col items-center justify-center animate-float mt-20">
          <div className="text-8xl mb-6 animate-pulse-soft relative">
            🌰
            <div className="absolute top-0 right-0 text-4xl animate-twinkle">✨</div>
          </div>
          <h1 className="text-5xl font-bold mb-4 text-[--color-bamtori-yellow] tracking-tight drop-shadow-[0_0_15px_rgba(253,230,138,0.5)]">밤토리</h1>
          <p className="text-[--color-bamtori-teal] text-xl font-medium opacity-90 tracking-wide">
            별이의 영어 모험이 시작돼요!
          </p>
        </div>

        <div className="w-full space-y-4 mb-10 z-20">
          <button
            onClick={handleLogin}
            className="w-full h-14 rounded-full bg-[#FEE500] text-[#191919] font-bold text-lg flex items-center justify-center gap-3 shadow-lg hover:scale-[1.02] transition-all active:scale-95 hover:shadow-xl"
          >
            <span className="text-xl">💬</span> 카카오로 시작하기
          </button>
          
          <button
            onClick={handleLogin}
            className="w-full h-14 rounded-full bg-white text-gray-900 font-bold text-lg flex items-center justify-center gap-3 shadow-lg hover:scale-[1.02] transition-all active:scale-95 hover:shadow-xl"
          >
             <span className="text-xl">G</span> Google로 시작하기
          </button>
          
          <button
            onClick={handleLogin}
            className="w-full h-14 rounded-full bg-black text-white font-bold text-lg flex items-center justify-center gap-3 shadow-lg hover:scale-[1.02] transition-all active:scale-95 hover:shadow-xl border border-gray-800"
          >
             <span className="text-xl">🍎</span> Apple로 시작하기
          </button>

          <p className="text-xs text-center text-gray-400 mt-6 leading-relaxed opacity-70">
            로그인 시 이용약관 및 개인정보 처리방침에<br/>동의하게 됩니다
          </p>
        </div>
      </MobileLayout>
    </div>
  );
}
