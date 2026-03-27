import { useQuery } from '@tanstack/react-query';
import { api } from '../client';

import type { ChildProfile } from '../types';

export function useProfile() {
    return useQuery({
        queryKey: ['profile'],
        queryFn: () => api.get<ChildProfile>('/v1/kid/profile'),
    });
}
