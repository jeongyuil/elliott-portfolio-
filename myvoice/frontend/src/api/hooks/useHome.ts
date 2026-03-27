import { useQuery } from '@tanstack/react-query';
import { api } from '../client';
import type { KidHomeResponse } from '../types';

export function useHome() {
    return useQuery({
        queryKey: ['kidHome'],
        queryFn: () => api.get<KidHomeResponse>('/v1/kid/home'),
    });
}
