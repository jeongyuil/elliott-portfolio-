import { describe, it, expect, beforeEach } from "vitest";
import { appRouter } from "./routers";
import * as db from "./db";
import type { User } from "../drizzle/schema";

describe("Onboarding System", () => {
  let testUser: User;
  let caller: ReturnType<typeof appRouter.createCaller>;

  beforeEach(async () => {
    // Create a test user
    const openId = `test-onboarding-${Date.now()}`;
    await db.upsertUser({
      openId,
      name: "Test User",
      email: "test@example.com",
    });

    const user = await db.getUserByOpenId(openId);
    if (!user) throw new Error("Failed to create test user");
    testUser = user;

    caller = appRouter.createCaller({
      user: testUser,
    });
  });

  it("should have onboardingCompleted as false for new users", async () => {
    expect(testUser.onboardingCompleted).toBe(false);
  });

  it("should complete onboarding successfully", async () => {
    const result = await caller.user.completeOnboarding();
    expect(result.success).toBe(true);

    // Verify the user's onboarding status is updated
    const updatedUser = await db.getUserByOpenId(testUser.openId);
    expect(updatedUser?.onboardingCompleted).toBe(true);
  });

  it("should allow completing onboarding multiple times without error", async () => {
    await caller.user.completeOnboarding();
    const result = await caller.user.completeOnboarding();
    expect(result.success).toBe(true);

    const updatedUser = await db.getUserByOpenId(testUser.openId);
    expect(updatedUser?.onboardingCompleted).toBe(true);
  });
});
