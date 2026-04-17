import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../client';
import type { DailyBonusResponse } from '../types';

export function useClaimDailyBonus() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: () => api.post<DailyBonusResponse>('/v1/kid/daily-bonus'),
        onSuccess: (_data) => {
            // Update cache for home/profile/inventory if needed
            queryClient.invalidateQueries({ queryKey: ['kidHome'] });
            queryClient.invalidateQueries({ queryKey: ['profile'] });
            queryClient.invalidateQueries({ queryKey: ['shop'] }); // for inventory
        }
    });
}
