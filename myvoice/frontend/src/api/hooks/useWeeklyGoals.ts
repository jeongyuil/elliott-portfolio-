import { useQuery } from '@tanstack/react-query';
import { api } from '../client';
import type { WeeklyGoal } from '../types';

export function useWeeklyGoals() {
    return useQuery({
        queryKey: ['weeklyGoals'],
        queryFn: () => api.get<WeeklyGoal>('/v1/kid/goals'),
    });
}
