/**
 * Vocabulary List Page - Mobile Optimized (No Header)
 * Design Philosophy: Mission card style for vocabulary categories
 * - Grid layout with mission-style cards
 * - Progress indicators for each category
 */

import { Link } from "wouter";
import BottomNav from "@/components/layout/BottomNav";
import { vocabularyCategories } from "@/lib/mockData";
import { CheckCircle2, Clock } from "lucide-react";

export default function VocabularyList() {
  return (
    <div className="h-screen flex flex-col bg-[var(--duo-bg)] overflow-hidden">
      {/* Main Content - Scrollable */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        {/* Category Grid - Mission Card Style */}
        <div className="grid grid-cols-2 gap-3 mb-20">
          {vocabularyCategories.map((category) => {
            const isCompleted = category.wordsLearned === category.totalWords;
            const isStarted = category.wordsLearned > 0;
            const progress = Math.round((category.wordsLearned / category.totalWords) * 100);

            return (
              <Link key={category.id} href={`/vocabulary/${category.id}`}>
                <div className="duo-card p-4 cursor-pointer hover:shadow-lg transition-all min-h-[160px] flex flex-col">
                  {/* Emoji and Status Badge */}
                  <div className="flex items-start justify-between mb-2">
                    <div className="text-4xl">{category.emoji}</div>
                    {isCompleted && (
                      <div className="flex items-center gap-1 px-2 py-1 bg-[var(--duo-green)] text-white rounded-full text-xs font-bold">
                        <CheckCircle2 size={12} />
                        완료
                      </div>
                    )}
                    {!isCompleted && isStarted && (
                      <div className="flex items-center gap-1 px-2 py-1 bg-[var(--duo-blue)] text-white rounded-full text-xs font-bold">
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
                  <h3 className="text-base font-bold text-[var(--duo-text)] mb-2">
                    {category.name}
                  </h3>

                  {/* Progress Info */}
                  <div className="mt-auto">
                    <div className="flex items-center justify-between text-xs text-[var(--duo-text-secondary)] mb-1">
                      <span>{category.wordsLearned}/{category.totalWords} 단어</span>
                      <span>{progress}%</span>
                    </div>
                    <div className="duo-progress">
                      <div 
                        className="duo-progress-bar" 
                        style={{ 
                          width: `${progress}%`,
                          backgroundColor: isCompleted ? 'var(--duo-green)' : 'var(--duo-blue)'
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

      {/* Bottom Navigation */}
      <BottomNav />
    </div>
  );
}
