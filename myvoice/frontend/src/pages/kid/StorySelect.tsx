/**
 * StorySelect — Story theme selection screen.
 * Shown when the child hasn't selected a story yet, or when switching stories.
 */

import { useStories, useSelectStory } from "@/api/hooks";
import type { StoryTheme } from "@/api/types";

function StoryCard({
    story,
    onSelect,
    isSelecting,
}: {
    story: StoryTheme;
    onSelect: () => void;
    isSelecting: boolean;
}) {
    const progress =
        story.totalUnits > 0
            ? Math.round((story.completedUnits / story.totalUnits) * 100)
            : 0;

    return (
        <button
            onClick={onSelect}
            disabled={isSelecting}
            className="w-full text-left active:scale-[0.97] transition-all disabled:opacity-60"
        >
            <div
                className={`bg-gradient-to-br ${story.coverColor} rounded-2xl p-5 shadow-lg text-white`}
            >
                <div className="text-4xl mb-2">{story.emoji}</div>
                <h2 className="text-lg font-extrabold leading-tight">{story.title}</h2>
                <p className="text-sm opacity-90 mt-1 leading-snug">{story.description}</p>

                {/* Progress bar */}
                {story.completedUnits > 0 && (
                    <div className="mt-3">
                        <div className="flex justify-between text-xs opacity-80 mb-1">
                            <span>진행률</span>
                            <span>{progress}%</span>
                        </div>
                        <div className="h-1.5 bg-white/30 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-white rounded-full transition-all"
                                style={{ width: `${progress}%` }}
                            />
                        </div>
                    </div>
                )}

                <div className="mt-4 bg-white/20 rounded-xl py-2 text-center text-sm font-bold">
                    {story.completedUnits > 0 ? "이어하기" : "시작하기"}
                </div>
            </div>
        </button>
    );
}

export default function StorySelect({ onSelected }: { onSelected?: () => void } = {}) {
    const { data: stories, isLoading } = useStories();
    const selectStory = useSelectStory();

    const handleSelect = (theme: string) => {
        selectStory.mutate(theme, {
            onSuccess: () => onSelected?.(),
        });
    };

    if (isLoading) {
        return (
            <div className="h-full flex items-center justify-center">
                <div className="animate-spin w-8 h-8 border-4 border-indigo-400 border-t-transparent rounded-full" />
            </div>
        );
    }

    return (
        <div className="h-full flex flex-col bg-gradient-to-b from-[#f0f4ff] to-[#e8eeff] overflow-hidden">
            <div className="flex-1 overflow-y-auto px-5 py-6 pb-28">
                {/* Header */}
                <div className="text-center mb-6">
                    <h1 className="text-xl font-bold text-[var(--bt-text)]">
                        어떤 모험을 할까요?
                    </h1>
                    <p className="text-xs text-[var(--bt-text-secondary)] mt-1">
                        원하는 이야기를 골라보세요!
                    </p>
                </div>

                {/* Story cards */}
                <div className="space-y-4">
                    {stories?.map((story) => (
                        <StoryCard
                            key={story.theme}
                            story={story}
                            onSelect={() => handleSelect(story.theme)}
                            isSelecting={selectStory.isPending}
                        />
                    ))}
                </div>

                {(!stories || stories.length === 0) && (
                    <div className="text-center py-12">
                        <div className="text-6xl mb-4">📚</div>
                        <p className="text-[var(--bt-text-secondary)]">
                            아직 이야기가 없습니다
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
