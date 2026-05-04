import { describe, it, expect } from "vitest";
import { appRouter } from "./routers";
import * as db from "./db";

describe("Vocabulary Completion with Weekly Goals Update", () => {
  const mockUser = {
    id: 1,
    openId: "test-user",
    name: "Test User",
    email: "test@example.com",
    loginMethod: "google",
    role: "user" as const,
    nickname: "Tester",
    avatar: "🐰",
    stars: 100,
    hearts: 3,
    maxHearts: 3,
    streak: 5,
    level: 3,
    xp: 500,
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  const mockContext = {
    user: mockUser,
    req: {} as any,
    res: {} as any,
  };

  const caller = appRouter.createCaller(mockContext);

  it("should update weekly goals when vocabulary category is completed", async () => {
    const initialGoal = await db.getCurrentWeeklyGoal(mockUser.id);
    expect(initialGoal).toBeTruthy();

    const wordsLearned = 10;
    const earnedStars = 5;
    const earnedXp = 50;

    const initialXp = initialGoal!.xpCurrent;
    const initialWords = initialGoal!.wordsCurrent;

    await caller.vocabulary.completeCategory({
      categoryId: 1,
      wordsLearned,
      earnedStars,
      earnedXp,
    });

    const updatedGoal = await db.getCurrentWeeklyGoal(mockUser.id);
    expect(updatedGoal?.xpCurrent).toBe(initialXp + earnedXp);
    expect(updatedGoal?.wordsCurrent).toBe(initialWords + wordsLearned);
  });

  it("should successfully complete vocabulary category", async () => {
    const result = await caller.vocabulary.completeCategory({
      categoryId: 1,
      wordsLearned: 10,
      earnedStars: 5,
      earnedXp: 50,
    });

    expect(result.success).toBe(true);
  });
});
