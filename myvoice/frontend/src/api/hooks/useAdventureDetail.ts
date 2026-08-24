import { useQuery } from '@tanstack/react-query';
import { api } from '../client';
import type { AdventureDetail } from '../types';

export function useAdventureDetail(id: string) {
    return useQuery({
        queryKey: ['adventure', id],
        queryFn: () => api.get<AdventureDetail>(`/v1/kid/adventures/${id}`),
        enabled: !!id,
    });
}
