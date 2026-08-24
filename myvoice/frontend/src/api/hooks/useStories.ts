import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../client';
import type { StoryTheme } from '../types';

export function useStories() {
    return useQuery({
        queryKey: ['stories'],
        queryFn: () => api.get<StoryTheme[]>('/v1/kid/adventures/stories'),
    });
}

export function useSelectStory() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (theme: string) =>
            api.post<{ status: string; selectedStoryTheme: string }>(
                '/v1/kid/adventures/stories/select',
                { theme },
            ),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['adventures'] });
            queryClient.invalidateQueries({ queryKey: ['stories'] });
        },
    });
}
