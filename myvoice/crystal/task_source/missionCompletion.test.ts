import { describe, it, expect, beforeEach } from 'vitest';
import { appRouter } from './routers';
import type { Context } from './_core/context';

describe('Mission Completion with Weekly Goals Update', () => {
  const createTestContext = (): Context => ({
    user: {
      id: 1,
      openId: 'test-user',
      name: 'Test User',
      email: 'test@example.com',
      loginMethod: 'google',
      role: 'user',
      nickname: null,
      avatar: '🐰',
      stars: 120,
      hearts: 3,
      maxHearts: 3,
      streak: 7,
      level: 5,
      xp: 1220,
      createdAt: new Date(),
      updatedAt: new Date(),
      lastSignedIn: new Date(),
    },
  });

  let caller: ReturnType<typeof appRouter.createCaller>;

  beforeEach(() => {
    caller = appRouter.createCaller(createTestContext());
  });

  it('should update weekly goals when mission is completed', async () => {
    // Get current weekly goals
    const initialGoals = await caller.weeklyGoals.getCurrent();
    expect(initialGoals).toBeDefined();
    
    const initialXp = initialGoals!.xpCurrent;
    const initialMissions = initialGoals!.missionsCurrent;
    
    // Complete a mission with 50 XP
    const result = await caller.missions.updateStatus({
      missionId: 1,
      status: 'completed',
      score: 100,
      earnedXp: 50,
    });
    
    expect(result.success).toBe(true);
    
    // Verify weekly goals were updated
    const updatedGoals = await caller.weeklyGoals.getCurrent();
    expect(updatedGoals).toBeDefined();
    expect(updatedGoals!.xpCurrent).toBe(initialXp + 50);
    expect(updatedGoals!.missionsCurrent).toBe(initialMissions + 1);
  });

  it('should not update weekly goals when mission status is not completed', async () => {
    const initialGoals = await caller.weeklyGoals.getCurrent();
    expect(initialGoals).toBeDefined();
    
    const initialXp = initialGoals!.xpCurrent;
    const initialMissions = initialGoals!.missionsCurrent;
    
    // Update mission to in_progress (not completed)
    await caller.missions.updateStatus({
      missionId: 1,
      status: 'in_progress',
      score: 50,
      earnedXp: 0,
    });
    
    // Verify weekly goals were NOT updated
    const updatedGoals = await caller.weeklyGoals.getCurrent();
    expect(updatedGoals).toBeDefined();
    expect(updatedGoals!.xpCurrent).toBe(initialXp);
    expect(updatedGoals!.missionsCurrent).toBe(initialMissions);
  });

  it('should handle multiple mission completions correctly', async () => {
    const initialGoals = await caller.weeklyGoals.getCurrent();
    expect(initialGoals).toBeDefined();
    
    const initialXp = initialGoals!.xpCurrent;
    const initialMissions = initialGoals!.missionsCurrent;
    
    // Complete first mission
    await caller.missions.updateStatus({
      missionId: 1,
      status: 'completed',
      score: 100,
      earnedXp: 30,
    });
    
    // Complete second mission
    await caller.missions.updateStatus({
      missionId: 2,
      status: 'completed',
      score: 100,
      earnedXp: 40,
    });
    
    // Verify cumulative updates
    const updatedGoals = await caller.weeklyGoals.getCurrent();
    expect(updatedGoals).toBeDefined();
    expect(updatedGoals!.xpCurrent).toBe(initialXp + 30 + 40);
    expect(updatedGoals!.missionsCurrent).toBe(initialMissions + 2);
  });
});
