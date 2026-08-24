/**
 * MissionList Page - Mobile Optimized (No Header)
 * Design Philosophy: Grid layout with mission cards
 * - Filters integrated into main content
 * - Scrollable mission grid
 */

import { useState } from "react";
import BottomNav from "@/components/layout/BottomNav";
import MissionCard from "@/components/mission/MissionCard";
import { missions } from "@/lib/mockData";

export default function MissionList() {
  const [filter, setFilter] = useState<"전체" | "쉬움" | "보통" | "어려움">("전체");

  const filteredMissions = filter === "전체" 
    ? missions 
    : missions.filter(m => m.difficulty === filter);

  return (
    <div className="h-screen flex flex-col bg-[var(--duo-bg)] overflow-hidden">
      {/* Content - Scrollable */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        {/* Filter Tabs */}
        <div className="flex gap-2 overflow-x-auto scrollbar-hide mb-4">
          {["전체", "쉬움", "보통", "어려움"].map((level) => (
            <button
              key={level}
              onClick={() => setFilter(level as any)}
              className={`px-4 py-2 rounded-full text-sm font-semibold whitespace-nowrap transition-colors ${
                filter === level
                  ? "bg-[var(--duo-green)] text-white"
                  : "bg-gray-100 text-[var(--duo-text-secondary)]"
              }`}
            >
              {level}
            </button>
          ))}
        </div>

        {/* Mission Grid */}
        <div className="grid grid-cols-2 gap-3 mb-20">
          {filteredMissions.map((mission) => (
            <MissionCard key={mission.id} {...mission} />
          ))}
        </div>

        {filteredMissions.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <p className="text-[var(--duo-text-secondary)]">
              해당 난이도의 미션이 없습니다
            </p>
          </div>
        )}
      </div>

      <BottomNav />

      <style>{`
        .scrollbar-hide::-webkit-scrollbar {
          display: none;
        }
        .scrollbar-hide {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `}</style>
    </div>
  );
}
