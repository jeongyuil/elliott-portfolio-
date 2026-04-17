/**
 * Shop Page - Passive star regen info + character skins
 * Stars regenerate over time (5/hour) and via daily login bonus.
 */

import { useState, useEffect } from "react";
import { Star, Clock, Flame, Check } from "lucide-react";
import { toast } from "sonner";
import { useShop } from "@/api/hooks/useShop";
import { api } from "@/api/client";
import type { ShopItem, PurchaseResponse } from "@/api/types";

export default function KidShop() {
    const { data: shopData, isLoading, refetch } = useShop();
    const [stars, setStars] = useState(0);
    const [ownedSkins, setOwnedSkins] = useState<string[]>([]);
    const [purchasing, setPurchasing] = useState<string | null>(null);
    const [regenInfo, setRegenInfo] = useState<{ ratePerHour: number; maxBalance: number } | null>(null);

    useEffect(() => {
        if (shopData) {
            setStars(shopData.inventory.stars);
            setOwnedSkins((shopData.inventory as any).ownedSkins || []);
            if ((shopData as any).starRegen) {
                setRegenInfo((shopData as any).starRegen);
            }
        }
    }, [shopData]);

    const handlePurchase = async (item: ShopItem) => {
        if (ownedSkins.includes(item.id)) {
            toast.info("이미 보유한 스킨이에요!");
            return;
        }
        if (stars < item.price) {
            toast.error("별이 부족해요!", { description: "시간이 지나면 별이 자동으로 충전돼요." });
            return;
        }
        setPurchasing(item.id);
        try {
            const res = await api.post<PurchaseResponse>('/v1/kid/shop/purchase', { itemId: item.id });
            toast.success(`${item.name} 스킨을 구매했어요!`);
            if (res?.newStars !== undefined) setStars(res.newStars);
            if (res?.inventory) {
                setOwnedSkins((res.inventory as any).ownedSkins || []);
            }
            refetch();
        } catch {
            toast.error("구매에 실패했어요.");
        } finally {
            setPurchasing(null);
        }
    };

    if (isLoading) {
        return (
            <div className="h-full flex items-center justify-center">
                <div className="animate-spin w-8 h-8 border-4 border-[var(--bt-primary)] border-t-transparent rounded-full" />
            </div>
        );
    }

    const skinItems = (shopData?.items || []).filter(i => i.itemType === "skin");
    const popoSkins = skinItems.filter(i => i.id.includes("popo"));
    const lunaSkins = skinItems.filter(i => i.id.includes("luna"));

    return (
        <div className="h-full flex flex-col bg-[var(--bt-bg)] overflow-hidden">
            <div className="flex-1 overflow-y-auto px-5 py-5 pb-28">
                {/* Header */}
                <div className="flex items-center justify-between mb-5">
                    <h1 className="text-xl font-bold text-[var(--bt-text)]">상점</h1>
                    <div className="flex items-center gap-1.5 bg-amber-50 border border-amber-200 rounded-full px-3 py-1.5">
                        <Star size={16} fill="currentColor" className="text-amber-500" />
                        <span className="text-sm font-bold text-amber-700">{stars}</span>
                    </div>
                </div>

                {/* Star Regen Info Card */}
                <div className="bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-50 border-2 border-amber-200 rounded-2xl p-4 mb-6">
                    <h2 className="text-base font-bold text-[var(--bt-text)] mb-3 flex items-center gap-2">
                        <Star size={18} className="text-amber-500" fill="currentColor" />
                        별 자동 충전
                    </h2>
                    <div className="grid grid-cols-2 gap-3">
                        <div className="flex items-center gap-2 bg-white/70 rounded-xl p-3">
                            <Clock size={20} className="text-amber-500 flex-shrink-0" />
                            <div>
                                <div className="text-sm font-bold text-[var(--bt-text)]">
                                    {regenInfo?.ratePerHour ?? 5}별 / 시간
                                </div>
                                <div className="text-[11px] text-[var(--bt-text-secondary)]">자동 충전 중</div>
                            </div>
                        </div>
                        <div className="flex items-center gap-2 bg-white/70 rounded-xl p-3">
                            <Flame size={20} className="text-orange-500 flex-shrink-0" />
                            <div>
                                <div className="text-sm font-bold text-[var(--bt-text)]">매일 접속 보너스</div>
                                <div className="text-[11px] text-[var(--bt-text-secondary)]">
                                    연속 접속 시 더 많이!
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="mt-3 bg-white/50 rounded-lg px-3 py-2">
                        <div className="flex items-center justify-between text-xs text-[var(--bt-text-secondary)]">
                            <span>현재 별</span>
                            <span className="font-bold text-amber-700">{stars} / {regenInfo?.maxBalance ?? 500}</span>
                        </div>
                        <div className="mt-1.5 h-2 bg-gray-200 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-gradient-to-r from-amber-400 to-yellow-400 rounded-full transition-all"
                                style={{ width: `${Math.min((stars / (regenInfo?.maxBalance ?? 500)) * 100, 100)}%` }}
                            />
                        </div>
                    </div>
                </div>

                {/* Popo Skins */}
                {popoSkins.length > 0 && (
                    <div className="mb-6">
                        <h2 className="text-base font-bold text-[var(--bt-text)] mb-3">포포 스킨</h2>
                        <div className="grid grid-cols-2 gap-3">
                            {popoSkins.map((item) => {
                                const owned = ownedSkins.includes(item.id);
                                const canAfford = stars >= item.price;
                                const isPurchasing = purchasing === item.id;

                                return (
                                    <SkinCard
                                        key={item.id}
                                        item={item}
                                        owned={owned}
                                        canAfford={canAfford}
                                        isPurchasing={isPurchasing}
                                        onPurchase={handlePurchase}
                                    />
                                );
                            })}
                        </div>
                    </div>
                )}

                {/* Luna Skins */}
                {lunaSkins.length > 0 && (
                    <div className="mb-6">
                        <h2 className="text-base font-bold text-[var(--bt-text)] mb-3">루나 스킨</h2>
                        <div className="grid grid-cols-2 gap-3">
                            {lunaSkins.map((item) => {
                                const owned = ownedSkins.includes(item.id);
                                const canAfford = stars >= item.price;
                                const isPurchasing = purchasing === item.id;

                                return (
                                    <SkinCard
                                        key={item.id}
                                        item={item}
                                        owned={owned}
                                        canAfford={canAfford}
                                        isPurchasing={isPurchasing}
                                        onPurchase={handlePurchase}
                                    />
                                );
                            })}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

function SkinCard({
    item,
    owned,
    canAfford,
    isPurchasing,
    onPurchase,
}: {
    item: ShopItem;
    owned: boolean;
    canAfford: boolean;
    isPurchasing: boolean;
    onPurchase: (item: ShopItem) => void;
}) {
    return (
        <div className={`bg-white rounded-2xl border ${owned ? "border-green-300 bg-green-50/30" : "border-gray-100"} p-4 text-center shadow-sm`}>
            <div className="text-4xl mb-2">{item.emoji}</div>
            <h3 className="font-bold text-sm text-[var(--bt-text)] mb-1">{item.name}</h3>
            <p className="text-[11px] text-[var(--bt-text-secondary)] mb-3 min-h-[28px]">
                {item.description}
            </p>
            {owned ? (
                <div className="w-full rounded-xl py-2 font-bold text-sm bg-green-100 text-green-700 flex items-center justify-center gap-1.5">
                    <Check size={14} />
                    <span>보유 중</span>
                </div>
            ) : (
                <button
                    onClick={() => onPurchase(item)}
                    disabled={!canAfford || isPurchasing}
                    className={`w-full rounded-xl py-2 font-bold text-sm transition-all active:scale-95 ${
                        canAfford
                            ? "bg-[var(--bt-primary)] text-white shadow-[0_2px_0_#58cc02]"
                            : "bg-gray-100 text-gray-400 cursor-not-allowed"
                    }`}
                >
                    <div className="flex items-center justify-center gap-1.5">
                        <Star size={14} fill="currentColor" className={canAfford ? "text-yellow-300" : ""} />
                        <span>{isPurchasing ? "..." : item.price}</span>
                    </div>
                </button>
            )}
        </div>
    );
}
