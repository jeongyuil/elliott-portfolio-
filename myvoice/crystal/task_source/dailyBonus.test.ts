import { describe, it, expect, beforeEach } from "vitest";
import { appRouter } from "./routers";
import { getDb } from "./db";
import { users } from "../drizzle/schema";
import { eq } from "drizzle-orm";

describe("Daily Login Bonus", () => {
  let mockUser = {
    id: 0,
    openId: "test-daily-bonus-user",
    name: "Test User",
    email: "test@example.com",
    role: "user" as const,
  };

  const createCaller = () => {
    return appRouter.createCaller({
      user: mockUser,
      req: {} as any,
      res: {} as any,
    });
  };

  beforeEach(async () => {
    // Clean up test user before each test
    const db = await getDb();
    if (!db) throw new Error("Database not available");
    
    await db.delete(users).where(eq(users.openId, mockUser.openId));
    
    // Insert fresh test user
    const result = await db.insert(users).values({
      openId: mockUser.openId,
      name: mockUser.name,
      email: mockUser.email,
      role: mockUser.role,
      stars: 100,
      hearts: 3,
      maxHearts: 3,
      streak: 0,
      consecutiveLoginDays: 0,
      lastLoginBonusDate: null,
    });
    
    // Get the inserted user to get the correct ID
    const [insertedUser] = await db.select().from(users).where(eq(users.openId, mockUser.openId));
    mockUser.id = insertedUser.id;
  });

  it("should claim first day bonus successfully", async () => {
    const caller = createCaller();
    
    const result = await caller.dailyBonus.claimDailyBonus();
    
    expect(result).not.toBeNull();
    expect(result?.starsReward).toBe(5);
    expect(result?.heartsReward).toBe(1);
    expect(result?.consecutiveDays).toBe(1);
    expect(result?.newStars).toBe(105); // 100 + 5
    expect(result?.newHearts).toBe(3); // min(3 + 1, 3) = 3
  });

  it("should not allow claiming bonus twice in the same day", async () => {
    const caller = createCaller();
    
    // First claim
    const firstClaim = await caller.dailyBonus.claimDailyBonus();
    expect(firstClaim).not.toBeNull();
    
    // Second claim on same day
    const secondClaim = await caller.dailyBonus.claimDailyBonus();
    expect(secondClaim).toBeNull();
  });

  it("should increase rewards for consecutive days", async () => {
    const caller = createCaller();
    const db = await getDb();
    if (!db) throw new Error("Database not available");
    
    // Simulate day 1 bonus claimed yesterday
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    yesterday.setHours(0, 0, 0, 0);
    
    await db.update(users)
      .set({
        lastLoginBonusDate: yesterday,
        consecutiveLoginDays: 1,
        stars: 105,
      })
      .where(eq(users.openId, mockUser.openId));
    
    // Claim day 2 bonus
    const result = await caller.dailyBonus.claimDailyBonus();
    
    expect(result).not.toBeNull();
    expect(result?.starsReward).toBe(7); // Day 2 reward
    expect(result?.heartsReward).toBe(1);
    expect(result?.consecutiveDays).toBe(2);
    expect(result?.newStars).toBe(112); // 105 + 7
  });

  it("should reset streak if a day is skipped", async () => {
    const caller = createCaller();
    const db = await getDb();
    if (!db) throw new Error("Database not available");
    
    // Simulate day 3 bonus claimed 2 days ago (skipped yesterday)
    const twoDaysAgo = new Date();
    twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);
    twoDaysAgo.setHours(0, 0, 0, 0);
    
    await db.update(users)
      .set({
        lastLoginBonusDate: twoDaysAgo,
        consecutiveLoginDays: 3,
        stars: 122,
      })
      .where(eq(users.openId, mockUser.openId));
    
    // Claim today (streak should reset)
    const result = await caller.dailyBonus.claimDailyBonus();
    
    expect(result).not.toBeNull();
    expect(result?.starsReward).toBe(5); // Back to day 1 reward
    expect(result?.heartsReward).toBe(1);
    expect(result?.consecutiveDays).toBe(1); // Streak reset
  });

  it("should give maximum rewards for 7+ consecutive days", async () => {
    const caller = createCaller();
    const db = await getDb();
    if (!db) throw new Error("Database not available");
    
    // Simulate day 6 bonus claimed yesterday
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    yesterday.setHours(0, 0, 0, 0);
    
    await db.update(users)
      .set({
        lastLoginBonusDate: yesterday,
        consecutiveLoginDays: 6,
        stars: 200,
        hearts: 1, // Low hearts to test heart reward
      })
      .where(eq(users.openId, mockUser.openId));
    
    // Claim day 7 bonus
    const result = await caller.dailyBonus.claimDailyBonus();
    
    expect(result).not.toBeNull();
    expect(result?.starsReward).toBe(20); // Max reward
    expect(result?.heartsReward).toBe(3);
    expect(result?.consecutiveDays).toBe(7);
    expect(result?.newStars).toBe(220); // 200 + 20
    expect(result?.newHearts).toBe(3); // min(1 + 3, 3) = 3
  });

  it("should correctly report bonus status", async () => {
    const caller = createCaller();
    
    // Check status before claiming
    const statusBefore = await caller.dailyBonus.getBonusStatus();
    expect(statusBefore.isAvailable).toBe(true);
    expect(statusBefore.nextStarsReward).toBe(5);
    expect(statusBefore.nextHeartsReward).toBe(1);
    expect(statusBefore.nextConsecutiveDays).toBe(1);
    
    // Claim bonus
    await caller.dailyBonus.claimDailyBonus();
    
    // Check status after claiming
    const statusAfter = await caller.dailyBonus.getBonusStatus();
    expect(statusAfter.isAvailable).toBe(false);
    expect(statusAfter.currentConsecutiveDays).toBe(1);
  });
});
