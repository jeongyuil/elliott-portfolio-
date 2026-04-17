import { describe, it, expect, beforeAll } from "vitest";
import { appRouter } from "./routers";
import * as db from "./db";

describe("Weekly Goals API", () => {
  describe("weeklyGoals.getCurrent", () => {
    it("should auto-create weekly goal for user without one", async () => {
      const caller = appRouter.createCaller({
        user: {
          id: 999999,
          openId: "test-user-no-goal",
          name: "Test User",
          email: "test@example.com",
          loginMethod: "oauth",
          role: "user",
          nickname: "테스트",
          avatar: "🐰",
          stars: 100,
          hearts: 3,
          maxHearts: 3,
          streak: 5,
          level: 1,
          xp: 500,
          createdAt: new Date(),
          updatedAt: new Date(),
          lastSignedIn: new Date(),
        },
        req: {} as any,
        res: {} as any,
      });

      const result = await caller.weeklyGoals.getCurrent();
      expect(result).toBeDefined();
      expect(result?.userId).toBe(999999);
      expect(result?.xpTarget).toBe(1500);
      expect(result?.xpCurrent).toBe(0);
    });
  });

  describe("weeklyGoals.updateProgress", () => {
    it("should throw error when no active goal exists", async () => {
      const caller = appRouter.createCaller({
        user: {
          id: 999998,
          openId: "test-user-no-goal-2",
          name: "Test User 2",
          email: "test2@example.com",
          loginMethod: "oauth",
          role: "user",
          nickname: "테스트2",
          avatar: "🐰",
          stars: 100,
          hearts: 3,
          maxHearts: 3,
          streak: 5,
          level: 1,
          xp: 500,
          createdAt: new Date(),
          updatedAt: new Date(),
          lastSignedIn: new Date(),
        },
        req: {} as any,
        res: {} as any,
      });

      await expect(
        caller.weeklyGoals.updateProgress({
          xpCurrent: 1500,
        })
      ).rejects.toThrow("No active weekly goal found");
    });
  });

  describe("weeklyGoals.updateTargets", () => {
    it("should throw error when no active goal exists", async () => {
      const caller = appRouter.createCaller({
        user: {
          id: 999997,
          openId: "test-user-no-goal-3",
          name: "Test User 3",
          email: "test3@example.com",
          loginMethod: "oauth",
          role: "user",
          nickname: "테스트3",
          avatar: "🐰",
          stars: 100,
          hearts: 3,
          maxHearts: 3,
          streak: 5,
          level: 1,
          xp: 500,
          createdAt: new Date(),
          updatedAt: new Date(),
          lastSignedIn: new Date(),
        },
        req: {} as any,
        res: {} as any,
      });

      await expect(
        caller.weeklyGoals.updateTargets({
          xpTarget: 2000,
        })
      ).rejects.toThrow("No active weekly goal found");
    });
  });
});

describe("Database Query Helpers", () => {
  describe("getCurrentWeeklyGoal", () => {
    it("should return undefined for non-existent user", async () => {
      const result = await db.getCurrentWeeklyGoal(999996);
      expect(result).toBeUndefined();
    });
  });

  describe("getAllMissions", () => {
    it("should return an array", async () => {
      const result = await db.getAllMissions();
      expect(Array.isArray(result)).toBe(true);
    });
  });

  describe("getAllVocabularyCategories", () => {
    it("should return an array", async () => {
      const result = await db.getAllVocabularyCategories();
      expect(Array.isArray(result)).toBe(true);
    });
  });

  describe("getAllShopItems", () => {
    it("should return an array", async () => {
      const result = await db.getAllShopItems();
      expect(Array.isArray(result)).toBe(true);
    });
  });
});
