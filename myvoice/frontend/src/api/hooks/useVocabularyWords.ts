import { useQuery } from '@tanstack/react-query';
import { api } from '../client';
import type { VocabularyWord } from '../types';

export function useVocabularyWords(categoryId: string) {
    return useQuery({
        queryKey: ['vocabulary', categoryId, 'words'],
        queryFn: () => api.get<VocabularyWord[]>(`/v1/kid/vocabulary/${categoryId}/words`),
        enabled: !!categoryId,
    });
}
