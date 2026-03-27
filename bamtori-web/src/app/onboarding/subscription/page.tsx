"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useApp } from "../../../context/AppContext";
import MobileLayout from "../../../components/MobileLayout";
import StarryBackground from "../../../components/StarryBackground";

type PlanType = 'basic' | 'standard' | 'premium';

export default function SubscriptionPage() {
  const router = useRouter();
  const { setSubscriptionPlan } = useApp();
  const [selectedPlan, setSelectedPlan] = useState<PlanType | null>('standard');

  const handleSelect = (plan: PlanType) => {
    setSelectedPlan(plan);
  };

  const handleSubmit = () => {
    if (selectedPlan) {
      setSubscriptionPlan(selectedPlan);
      router.push('/mode-select');
    }
  };

  return (
    <div className="bg-[--color-bamtori-dark] min-h-dvh text-white font-sans overflow-x-hidden">
        <StarryBackground />
        
        <MobileLayout className="p-6 pb-24 relative z-10">
            <header className="mt-8 mb-8 text-center animate-float">
                <div className="text-4xl mb-2">✨</div>
                <h1 className="text-2xl font-bold text-white mb-2">모험을 시작할 준비가 됐어요!</h1>
                <p className="text-gray-400 text-sm font-medium">
                    아이에게 맞는 플랜을 선택해주세요.<br/>
                    <span className="text-[--color-bamtori-yellow]">7일간 무료로 체험</span>할 수 있어요!
                </p>
            </header>

            <div className="space-y-4">
                {/* Basic Plan */}
                <div 
                    onClick={() => handleSelect('basic')}
                    className={`relative p-5 rounded-2xl border-2 transition-all cursor-pointer ${
                        selectedPlan === 'basic' 
                        ? 'bg-[#1C2128] border-gray-400 shadow-lg' 
                        : 'bg-[#0D1117] border-[#30363D] opacity-80'
                    }`}
                >
                    <div className="flex justify-between items-center mb-3">
                        <h3 className="text-xl font-bold text-gray-300">Basic</h3>
                        <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                            selectedPlan === 'basic' ? 'border-[--color-bamtori-teal] bg-[--color-bamtori-teal]' : 'border-gray-600'
                        }`}>
                            {selectedPlan === 'basic' && <span className="text-[#0D1117] text-sm">✓</span>}
                        </div>
                    </div>
                    <div className="text-2xl font-bold mb-4">₩9,900<span className="text-sm font-normal text-gray-500"> /월</span></div>
                    <ul className="space-y-2 text-sm text-gray-400">
                        <li className="flex items-center gap-2"><span className="text-gray-500">✓</span> 주 3회 세션</li>
                        <li className="flex items-center gap-2"><span className="text-gray-500">✓</span> 기본 리포트 제공</li>
                    </ul>
                </div>

                {/* Standard Plan (Recommended) */}
                <div 
                    onClick={() => handleSelect('standard')}
                    className={`relative p-5 rounded-2xl border-2 transition-all cursor-pointer ${
                        selectedPlan === 'standard' 
                        ? 'bg-[rgba(249,168,212,0.1)] border-[--color-bamtori-coral] shadow-[0_0_15px_rgba(249,168,212,0.3)] scale-[1.02] z-10' 
                        : 'bg-[#0D1117] border-[#30363D]'
                    }`}
                >
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-[--color-bamtori-coral] text-[#0D1117] text-xs font-bold px-3 py-1 rounded-full shadow-md">
                        추천
                    </div>
                    <div className="flex justify-between items-center mb-3">
                        <h3 className="text-xl font-bold text-[--color-bamtori-coral]">Standard</h3>
                        <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                            selectedPlan === 'standard' ? 'border-[--color-bamtori-coral] bg-[--color-bamtori-coral]' : 'border-gray-600'
                        }`}>
                            {selectedPlan === 'standard' && <span className="text-[#0D1117] text-sm">✓</span>}
                        </div>
                    </div>
                    <div className="text-2xl font-bold mb-4 text-white">₩14,900<span className="text-sm font-normal text-gray-400"> /월</span></div>
                    <ul className="space-y-2 text-sm text-gray-300">
                        <li className="flex items-center gap-2"><span className="text-[--color-bamtori-coral]">✓</span> 주 5회 세션</li>
                        <li className="flex items-center gap-2"><span className="text-[--color-bamtori-coral]">✓</span> AI 리포트 제공</li>
                        <li className="flex items-center gap-2"><span className="text-[--color-bamtori-coral]">✓</span> 프리토킹 3회/주</li>
                    </ul>
                </div>

                {/* Premium Plan */}
                <div 
                    onClick={() => handleSelect('premium')}
                    className={`relative p-5 rounded-2xl border-2 transition-all cursor-pointer ${
                        selectedPlan === 'premium' 
                        ? 'bg-[rgba(253,230,138,0.1)] border-[--color-bamtori-yellow] shadow-[0_0_15px_rgba(253,230,138,0.3)]' 
                        : 'bg-[#0D1117] border-[#30363D] opacity-80'
                    }`}
                >
                    <div className="flex justify-between items-center mb-3">
                        <h3 className="text-xl font-bold text-[--color-bamtori-yellow]">Premium</h3>
                        <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                            selectedPlan === 'premium' ? 'border-[--color-bamtori-yellow] bg-[--color-bamtori-yellow]' : 'border-gray-600'
                        }`}>
                            {selectedPlan === 'premium' && <span className="text-[#0D1117] text-sm">✓</span>}
                        </div>
                    </div>
                    <div className="text-2xl font-bold mb-4">₩19,900<span className="text-sm font-normal text-gray-500"> /월</span></div>
                    <ul className="space-y-2 text-sm text-gray-400">
                        <li className="flex items-center gap-2"><span className="text-[--color-bamtori-yellow]">✓</span> 무제한 세션</li>
                        <li className="flex items-center gap-2"><span className="text-[--color-bamtori-yellow]">✓</span> 전문가 리포트 제공</li>
                        <li className="flex items-center gap-2"><span className="text-[--color-bamtori-yellow]">✓</span> 무제한 프리토킹</li>
                    </ul>
                </div>
            </div>

            {/* Bottom Button */}
            <div className="fixed bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-[--color-bamtori-dark] via-[--color-bamtori-dark] to-transparent z-50 max-w-md mx-auto">
                <button
                    onClick={handleSubmit}
                    className="w-full h-14 rounded-full font-bold text-lg shadow-lg transition-all bg-white text-[#0D1117] hover:scale-[1.02] hover:shadow-xl hover:bg-gray-100"
                >
                    무료 체험 시작하기
                </button>
            </div>
        </MobileLayout>
    </div>
  );
}
