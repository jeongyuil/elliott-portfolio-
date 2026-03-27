import { useQuery } from '@tanstack/react-query';
import { api } from '../client';

import type { VocabularyCategory } from '../types';

export function useVocabularyCategories() {
    return useQuery({
        queryKey: ['vocabulary', 'categories'],
        queryFn: () => api.get<VocabularyCategory[]>('/v1/kid/vocabulary'),
    });
}
