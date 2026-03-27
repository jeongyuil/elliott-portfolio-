/**
 * Vocabulary List Page - Mobile Optimized (No Header)
 * Design Philosophy: Mission card style for vocabulary categories
 * - Grid layout with mission-style cards
 * - Progress indicators for each command
 */

import { Link } from "react-router-dom";
import { CheckCircle2, Clock } from "lucide-react";
import { useVocabularyCategories } from "@/api/hooks/useVocabulary";

export default function Vocabulary() {
    const { data: categories, isLoading } = useVocabularyCategories();

    if (isLoading) {
        return <div className="h-full flex items-center justify-center">Loading...</div>;
    }

    return (
        <div className="h-full flex flex-col bg-[var(--bt-bg)] overflow-hidden">
            {/* Main Content - Scrollable */}
            <div className="flex-1 overflow-y-auto px-4 py-4 pb-24">
                {/* Title */}
                <h1 className="text-xl font-bold text-[var(--bt-text)] mb-4">어휘 학습</h1>

                {/* Category Grid - Mission Card Style */}
                <div className="grid grid-cols-2 gap-3">
                    {(categories || []).map((category) => {
                        const isCompleted = category.wordsLearned === category.totalWords;
                        const isStarted = category.wordsLearned > 0;
                        const progress = category.totalWords > 0 ? Math.round((category.wordsLearned / category.totalWords) * 100) : 0;

                        return (
                            <Link key={category.id} to={`/kid/vocabulary/${category.id}`}>
                                <div className="bt-card p-4 cursor-pointer hover:shadow-lg transition-all min-h-[160px] flex flex-col bg-white hover:bg-gray-50">
                                    {/* Emoji and Status Badge */}
                                    <div className="flex items-start justify-between mb-2">
                                        <div className="text-4xl">{category.emoji}</div>
                                        {isCompleted && (
                                            <div className="flex items-center gap-1 px-2 py-1 bg-[var(--bt-primary)] text-white rounded-full text-xs font-bold">
                                                <CheckCircle2 size={12} />
                                                완료
                                            </div>
                                        )}
                                        {!isCompleted && isStarted && (
                                            <div className="flex items-center gap-1 px-2 py-1 bg-[var(--bt-accent)] text-white rounded-full text-xs font-bold">
                                                <Clock size={12} />
                                                진행중
                                            </div>
                                        )}
                                        {!isStarted && (
                                            <div className="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs font-bold">
                                                새로운
                                            </div>
                                        )}
                                    </div>

                                    {/* Category Name */}
                                    <h3 className="text-base font-bold text-[var(--bt-text)] mb-2">
                                        {category.name}
                                    </h3>

                                    {/* Progress Info */}
                                    <div className="mt-auto">
                                        <div className="flex items-center justify-between text-xs text-[var(--bt-text-secondary)] mb-1">
                                            <span>{category.wordsLearned}/{category.totalWords} 단어</span>
                                            <span>{progress}%</span>
                                        </div>
                                        <div className="bt-progress">
                                            <div
                                                className="bt-progress-bar"
                                                style={{
                                                    width: `${progress}%`,
                                                    backgroundColor: isCompleted ? 'var(--bt-primary)' : 'var(--bt-accent)'
                                                }}
                                            />
                                        </div>
                                    </div>
                                </div>
                            </Link>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
