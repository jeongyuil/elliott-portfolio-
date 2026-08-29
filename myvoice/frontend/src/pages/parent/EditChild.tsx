/**
 * Edit Child — Wireframe 03: 아이 프로필 수정
 * 아바타 섹션, 기본 정보 폼, 학습 언어 태그, 발달 단계
 */
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { parentApi } from "@/api/client";
import type { ChildProfile, ChildUpdate } from "@/api/types";
import { ChevronLeft, Save } from "lucide-react";
import { toast } from "sonner";

const LANG_OPTIONS = [
    { label: '🇰🇷 한국어 → 🇬🇧 영어', value: 'ko-en' },
    { label: '🇰🇷 한국어 → 🇯🇵 일본어', value: 'ko-ja' },
];

const STAGE_OPTIONS = [
    { label: '초급 (4~5세, 첫 노출)', value: 'beginner' },
    { label: '중급 (5~6세, 기초 어휘 보유)', value: 'intermediate' },
    { label: '고급 (6~7세, 문장 구사 가능)', value: 'advanced' },
];

export default function EditChild() {
    const { childId } = useParams<{ childId: string }>();
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);
    const [child, setChild] = useState<ChildProfile | null>(null);
    const [formData, setFormData] = useState<ChildUpdate>({
        name: "",
        birthDate: "",
        gender: "m",
        primaryLanguage: "ko-en",
        developmentStageLanguage: "intermediate",
    });

    useEffect(() => {
        if (childId && childId !== 'new') {
            (async () => {
                try {
                    const children = await parentApi.listChildren();
                    const found = children.find(c => c.childId === childId);
                    if (found) {
                        setChild(found);
                        setFormData({
                            name: found.name,
                            birthDate: found.birthDate.split('T')[0],
                            gender: found.gender,
                            primaryLanguage: found.primaryLanguage || 'ko-en',
                            developmentStageLanguage: found.developmentStageLanguage || 'intermediate',
                        });
                    } else {
                        toast.error("아이 정보를 찾을 수 없습니다.");
                        navigate("/parent/home");
                    }
                } catch {
                    toast.error("정보를 불러오지 못했습니다.");
                }
            })();
        }
    }, [childId, navigate]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            if (childId === 'new') {
                await parentApi.createChild({
                    name: formData.name!,
                    birthDate: formData.birthDate!,
                    gender: formData.gender,
                    primaryLanguage: formData.primaryLanguage,
                    developmentStageLanguage: formData.developmentStageLanguage,
                });
                toast.success("아이 프로필이 생성되었습니다.");
            } else if (childId) {
                await parentApi.updateChild(childId, formData);
                toast.success("아이 프로필이 수정되었습니다.");
            }
            navigate("/parent/home");
        } catch {
            toast.error("저장에 실패했습니다.");
        } finally {
            setIsLoading(false);
        }
    };

    const isNew = childId === 'new';

    return (
        <div className="min-h-screen bg-[#f8f9fa]">
            <div className="max-w-[640px] mx-auto px-6 py-8">

                {/* Header */}
                <div className="flex items-center gap-3.5 mb-8">
                    <button
                        onClick={() => navigate("/parent/home")}
                        className="w-10 h-10 rounded-lg border border-[#e5e7eb] bg-white flex items-center justify-center text-[#6b7280] hover:bg-gray-50 transition-colors"
                    >
                        <ChevronLeft size={18} />
                    </button>
                    <h1 className="text-2xl font-extrabold text-[#1a1a2e]">
                        {isNew ? '아이 등록' : '아이 프로필 수정'}
                    </h1>
                </div>

                {/* Card */}
                <div className="bg-white rounded-xl border border-[#e5e7eb] overflow-hidden">
                    <div className="px-6 pt-6">
                        <h2 className="text-lg font-bold text-[#1a1a2e]">기본 정보</h2>
                        <p className="text-[13px] text-[#6b7280] mt-1">
                            아이의 학습 맞춤형 콘텐츠를 위해 정확한 정보를 입력해주세요.
                        </p>
                    </div>

                    <div className="p-6">
                        {/* Avatar Section (only for edit mode) */}
                        {!isNew && child && (
                            <div className="flex items-center gap-5 mb-6 pb-6 border-b border-[#f3f4f6]">
                                <div className="w-20 h-20 rounded-full bg-[#dbeafe] flex items-center justify-center text-4xl">
                                    {child.avatarEmoji || '👦'}
                                </div>
                                <div className="flex-1">
                                    <div className="text-lg font-bold text-[#1a1a2e]">{child.name}</div>
                                    <div className="text-[13px] text-[#6b7280] mt-0.5">
                                        Level {child.level} · XP {child.xp}
                                    </div>
                                    <button className="mt-2 px-3.5 py-1.5 border border-[#d1d5db] rounded-md bg-white text-xs hover:bg-gray-50 transition-colors">
                                        아바타 변경
                                    </button>
                                </div>
                            </div>
                        )}

                        {/* Form */}
                        <form onSubmit={handleSubmit} className="space-y-5">
                            {/* Name */}
                            <div>
                                <label className="block text-sm font-semibold text-[#374151] mb-1.5">이름 (별명)</label>
                                <input
                                    type="text"
                                    className="w-full px-3.5 py-2.5 border border-[#d1d5db] rounded-lg text-sm bg-white focus:border-[#3b82f6] focus:ring-[3px] focus:ring-[rgba(59,130,246,0.1)] outline-none transition"
                                    value={formData.name || ''}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    required
                                />
                            </div>

                            {/* Birth Date */}
                            <div>
                                <label className="block text-sm font-semibold text-[#374151] mb-1.5">생년월일</label>
                                <input
                                    type="date"
                                    className="w-full px-3.5 py-2.5 border border-[#d1d5db] rounded-lg text-sm bg-white focus:border-[#3b82f6] focus:ring-[3px] focus:ring-[rgba(59,130,246,0.1)] outline-none transition"
                                    value={formData.birthDate || ''}
                                    onChange={(e) => setFormData({ ...formData, birthDate: e.target.value })}
                                    required
                                />
                            </div>

                            {/* Gender */}
                            <div>
                                <label className="block text-sm font-semibold text-[#374151] mb-1.5">성별</label>
                                <select
                                    className="w-full px-3.5 py-2.5 border border-[#d1d5db] rounded-lg text-sm bg-white"
                                    value={formData.gender || 'm'}
                                    onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                                >
                                    <option value="m">남자</option>
                                    <option value="f">여자</option>
                                    <option value="other">기타</option>
                                </select>
                            </div>

                            {/* Learning Language (Tag Selection) */}
                            <div>
                                <label className="block text-sm font-semibold text-[#374151] mb-1.5">학습 언어</label>
                                <div className="flex gap-2 mt-2">
                                    {LANG_OPTIONS.map((opt) => (
                                        <button
                                            key={opt.value}
                                            type="button"
                                            onClick={() => setFormData({ ...formData, primaryLanguage: opt.value })}
                                            className={`px-3.5 py-1.5 border-2 rounded-full text-[13px] font-medium transition-colors ${
                                                formData.primaryLanguage === opt.value
                                                    ? 'border-[#3b82f6] bg-[#eff6ff] text-[#3b82f6]'
                                                    : 'border-[#e5e7eb] bg-white text-[#374151] hover:border-gray-300'
                                            }`}
                                        >
                                            {opt.label}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {/* Development Stage */}
                            <div>
                                <label className="block text-sm font-semibold text-[#374151] mb-1.5">발달 단계</label>
                                <select
                                    className="w-full px-3.5 py-2.5 border border-[#d1d5db] rounded-lg text-sm bg-white"
                                    value={formData.developmentStageLanguage || 'intermediate'}
                                    onChange={(e) => setFormData({ ...formData, developmentStageLanguage: e.target.value })}
                                >
                                    {STAGE_OPTIONS.map((opt) => (
                                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                                    ))}
                                </select>
                            </div>

                            {/* Actions */}
                            <div className="flex justify-end gap-2.5 pt-5 border-t border-[#f3f4f6]">
                                <button
                                    type="button"
                                    onClick={() => navigate("/parent/home")}
                                    className="px-6 py-2.5 border border-[#d1d5db] rounded-lg bg-white text-sm hover:bg-gray-50 transition-colors"
                                >
                                    취소
                                </button>
                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className="px-6 py-2.5 border-none rounded-lg bg-[#3b82f6] text-white text-sm font-semibold hover:bg-[#2563eb] transition-colors flex items-center gap-1.5 disabled:opacity-40"
                                >
                                    <Save size={14} />
                                    {isLoading ? '저장 중...' : '저장하기'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}
