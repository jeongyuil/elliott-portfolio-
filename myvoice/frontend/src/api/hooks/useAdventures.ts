import { useQuery } from '@tanstack/react-query';
import { api } from '../client';
import type { Adventure } from '../types';

export function useAdventures() {
    return useQuery({
        queryKey: ['adventures'],
        queryFn: () => api.get<Adventure[]>('/v1/kid/adventures'),
        staleTime: 0,
        refetchOnMount: 'always',
    });
}
