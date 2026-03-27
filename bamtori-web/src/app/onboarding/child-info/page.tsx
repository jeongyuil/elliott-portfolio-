"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useApp } from "../../../context/AppContext";
import MobileLayout from "../../../components/MobileLayout";
import StarryBackground from "../../../components/StarryBackground";

const INTERESTS_OPTIONS = [
  "동물", "우주", "공룡", "요리", 
  "그림그리기", "음악", "스포츠", "과학", 
  "로봇", "자동차", "공주", "바다"
];

const AGES = [4, 5, 6, 7, 8, 9, 10, 11, 12];

export default function ChildInfoPage() {
  const router = useRouter();
  const { setChildProfileData } = useApp();
  
  const [name, setName] = useState("");
  const [age, setAge] = useState<number | null>(null);
  const [gender, setGender] = useState<'male' | 'female' | ''>('');
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);

  const toggleInterest = (interest: string) => {
    if (selectedInterests.includes(interest)) {
      setSelectedInterests(prev => prev.filter(i => i !== interest));
    } else {
      if (selectedInterests.length < 5) {
        setSelectedInterests(prev => [...prev, interest]);
      }
    }
  };

  const isFormValid = name.trim().length > 0 && age !== null && gender !== '';

  const handleSubmit = () => {
    if (!isFormValid) return;
    
    setChildProfileData({
      name,
      age: age!,
      gender,
      interests: selectedInterests
    });
    
    router.push('/onboarding/subscription');
  };

  return (
    <div className="bg-[--color-bamtori-dark] min-h-dvh text-white font-sans overflow-x-hidden">
        {/* Subtle background for depth */}
        <div className="fixed inset-0 bg-gradient-to-b from-transparent via-[rgba(13,17,23,0.5)] to-[--color-bamtori-dark] pointer-events-none z-0" />
        <StarryBackground />
        
        <MobileLayout className="p-6 pb-24 relative z-10">
            <header className="mt-8 mb-8 text-center animate-float">
                <div className="text-4xl mb-2">🌟</div>
                <h1 className="text-2xl font-bold text-white mb-2">아이의 정보를 알려주세요</h1>
                <p className="text-gray-400 text-sm font-medium">
                    밤토리가 아이에게 맞는 모험을<br/>준비할 수 있도록 도와주세요
                </p>
            </header>

            <div className="space-y-8 animate-pulse-soft" style={{ animationDuration: '4s' }}>
                {/* Name Input */}
                <div className="space-y-3">
                    <label className="text-[--color-bamtori-yellow] font-bold text-sm ml-1">이름</label>
                    <input 
                        type="text" 
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="아이 이름을 입력하세요"
                        className="w-full h-14 bg-[#1C2128] border-2 border-[#30363D] rounded-2xl px-5 text-lg text-white placeholder-gray-600 focus:border-[--color-bamtori-purple] focus:outline-none transition-all"
                    />
                </div>

                {/* Age Selection */}
                <div className="space-y-3">
                    <label className="text-[--color-bamtori-coral] font-bold text-sm ml-1">나이</label>
                    <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide -mx-6 px-6">
                        {AGES.map((a) => (
                            <button
                                key={a}
                                onClick={() => setAge(a)}
                                className={`flex-shrink-0 w-14 h-14 rounded-full flex items-center justify-center text-lg font-bold border-2 transition-all ${
                                    age === a 
                                    ? 'bg-[--color-bamtori-coral] border-[--color-bamtori-coral] text-[#0D1117] scale-110 shadow-[0_0_10px_rgba(249,168,212,0.5)]' 
                                    : 'bg-[#1C2128] border-[#30363D] text-gray-400'
                                }`}
                            >
                                {a}세
                            </button>
                        ))}
                    </div>
                </div>

                {/* Gender Selection */}
                <div className="space-y-3">
                    <label className="text-[--color-bamtori-teal] font-bold text-sm ml-1">성별</label>
                    <div className="flex gap-4">
                        <button
                            onClick={() => setGender('male')}
                            className={`flex-1 h-16 rounded-2xl flex items-center justify-center gap-2 border-2 transition-all ${
                                gender === 'male'
                                ? 'bg-[--color-bamtori-teal] border-[--color-bamtori-teal] text-[#0D1117] shadow-[0_0_10px_rgba(94,234,212,0.5)]'
                                : 'bg-[#1C2128] border-[#30363D] text-gray-400'
                            }`}
                        >
                            <span className="text-2xl">👦</span>
                            <span className="font-bold">남자</span>
                        </button>
                        <button
                            onClick={() => setGender('female')}
                            className={`flex-1 h-16 rounded-2xl flex items-center justify-center gap-2 border-2 transition-all ${
                                gender === 'female'
                                ? 'bg-[--color-bamtori-teal] border-[--color-bamtori-teal] text-[#0D1117] shadow-[0_0_10px_rgba(94,234,212,0.5)]'
                                : 'bg-[#1C2128] border-[#30363D] text-gray-400'
                            }`}
                        >
                            <span className="text-2xl">👧</span>
                            <span className="font-bold">여자</span>
                        </button>
                    </div>
                </div>

                {/* Interests Selection */}
                <div className="space-y-3">
                    <div className="flex justify-between items-end">
                        <label className="text-[--color-bamtori-purple] font-bold text-sm ml-1">관심사</label>
                        <span className="text-xs text-gray-500 font-mono">{selectedInterests.length}/5 선택됨</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                        {INTERESTS_OPTIONS.map((interest) => {
                            const isSelected = selectedInterests.includes(interest);
                            return (
                                <button
                                    key={interest}
                                    onClick={() => toggleInterest(interest)}
                                    className={`py-3 rounded-xl text-sm font-medium border-2 transition-all active:scale-95 ${
                                        isSelected
                                        ? 'bg-[rgba(167,139,250,0.2)] border-[--color-bamtori-purple] text-[--color-bamtori-purple] shadow-[0_0_8px_rgba(167,139,250,0.3)]'
                                        : 'bg-[#1C2128] border-[#30363D] text-gray-400 hover:border-gray-600'
                                    }`}
                                >
                                    {interest}
                                </button>
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* Bottom Button */}
            <div className="fixed bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-[--color-bamtori-dark] via-[--color-bamtori-dark] to-transparent z-50 max-w-md mx-auto">
                <button
                    onClick={handleSubmit}
                    disabled={!isFormValid}
                    className={`w-full h-14 rounded-full font-bold text-lg shadow-lg transition-all ${
                        isFormValid
                        ? 'bg-gradient-to-r from-[--color-bamtori-purple] to-[--color-bamtori-coral] text-white hover:scale-[1.02] hover:shadow-xl shadow-[rgba(167,139,250,0.4)]'
                        : 'bg-[#30363D] text-gray-500 cursor-not-allowed'
                    }`}
                >
                    다음으로
                </button>
            </div>
        </MobileLayout>
    </div>
  );
}
