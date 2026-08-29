/**
 * Shop Page - Mobile Optimized (No Header)
 * Design Philosophy: Clean item grid with inventory display
 * - Star count and inventory integrated into main content
 * - Scrollable item grid
 */

import { useState } from "react";
import { Star } from "lucide-react";
import { toast } from "sonner";
import BottomNav from "@/components/layout/BottomNav";
import { shopItems, userData } from "@/lib/mockData";

export default function Shop() {
  const [stars, setStars] = useState(userData.stars);
  const [inventory, setInventory] = useState(userData.inventory);

  const handlePurchase = (item: typeof shopItems[0]) => {
    if (stars >= item.price) {
      setStars(stars - item.price);
      
      // Update inventory based on item
      if (item.name === "힌트") {
        setInventory({ ...inventory, hints: inventory.hints + 1 });
      } else if (item.name === "시간 연장") {
        setInventory({ ...inventory, timeExtensions: inventory.timeExtensions + 1 });
      } else if (item.name === "하트 충전") {
        setInventory({ ...inventory, heartRefills: inventory.heartRefills + 1 });
      }
      
      toast.success(`${item.name}을(를) 구매했습니다!`, {
        description: `${item.price}개의 별을 사용했습니다`,
      });
    } else {
      toast.error("별이 부족합니다", {
        description: "미션을 완료하여 별을 모아보세요!",
      });
    }
  };

  return (
    <div className="h-screen flex flex-col bg-[var(--duo-bg)] overflow-hidden">
      {/* Items Grid - Scrollable */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        {/* Star Count */}
        <div className="flex items-center gap-2 mb-4">
          <Star size={20} className="duo-star" fill="currentColor" />
          <span className="text-lg font-bold text-[var(--duo-text)]">{stars}개 보유</span>
        </div>

        {/* Inventory Section */}
        <div className="duo-card p-4 mb-4">
          <h2 className="text-base font-bold text-[var(--duo-text)] mb-3 flex items-center gap-2">
            🎒 보유 아이템
          </h2>
          <div className="grid grid-cols-3 gap-3">
            <div className="text-center p-3 bg-yellow-50 rounded-xl">
              <div className="text-2xl mb-1">💡</div>
              <div className="text-lg font-bold text-[var(--duo-text)]">{inventory.hints}</div>
              <div className="text-xs text-[var(--duo-text-secondary)]">힌트</div>
            </div>
            <div className="text-center p-3 bg-blue-50 rounded-xl">
              <div className="text-2xl mb-1">⏱️</div>
              <div className="text-lg font-bold text-[var(--duo-text)]">{inventory.timeExtensions}</div>
              <div className="text-xs text-[var(--duo-text-secondary)]">시간 연장</div>
            </div>
            <div className="text-center p-3 bg-red-50 rounded-xl">
              <div className="text-2xl mb-1">❤️</div>
              <div className="text-lg font-bold text-[var(--duo-text)]">{inventory.heartRefills}</div>
              <div className="text-xs text-[var(--duo-text-secondary)]">하트 충전</div>
            </div>
          </div>
        </div>

        {/* Shop Items */}
        <h2 className="text-base font-bold text-[var(--duo-text)] mb-3">상점 아이템</h2>
        <div className="grid grid-cols-2 gap-3 mb-20">
          {shopItems.map((item) => {
            const canAfford = stars >= item.price;

            return (
              <div key={item.id} className="duo-card p-4 text-center">
                <div className="text-4xl mb-2">{item.emoji}</div>
                <h3 className="font-bold text-base text-[var(--duo-text)] mb-1">{item.name}</h3>
                <p className="text-xs text-[var(--duo-text-secondary)] mb-3 min-h-[32px]">
                  {item.description}
                </p>
                <button
                  onClick={() => handlePurchase(item)}
                  disabled={!canAfford}
                  className={`w-full rounded-xl py-2 font-bold text-sm transition-colors ${
                    canAfford
                      ? "bg-[var(--duo-green)] text-white hover:bg-[#4CAD02]"
                      : "bg-gray-200 text-gray-400 cursor-not-allowed"
                  }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    <Star size={14} fill="currentColor" />
                    <span>{item.price}</span>
                  </div>
                </button>
              </div>
            );
          })}
        </div>
      </div>

      <BottomNav />
    </div>
  );
}
