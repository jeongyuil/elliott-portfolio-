import { useQuery } from '@tanstack/react-query';
import { api } from '../client';

import type { ShopResponse } from '../types';

export function useShop() {
    return useQuery({
        queryKey: ['shop'],
        queryFn: () => api.get<ShopResponse>('/v1/kid/shop'),
    });
}
