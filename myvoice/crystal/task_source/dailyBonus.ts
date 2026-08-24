import { z } from "zod";
import { router, protectedProcedure } from "../../_core/trpc";
import { getDb } from "../../db";
import { users } from "../../../drizzle/schema";
import { eq } from "drizzle-orm";

/**
 * Daily login bonus router
 * Handles daily login rewards with increasing bonuses for consecutive logins
 */
export const dailyBonusRouter = router({
  /**
   * Check and claim daily login bonus
   * Returns null if already claimed today, otherwise returns the bonus rewards
   */
  claimDailyBonus: protectedProcedure.mutation(async ({ ctx }) => {
    const userId = ctx.user.id;

    // Get current user data
    const db = await getDb();
    if (!db) throw new Error("Database not available");
    
    const [user] = await db.select().from(users).where(eq(users.id, userId));
    
    if (!user) {
      throw new Error("User not found");
    }

    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    
    // Check if user already claimed bonus today
    if (user.lastLoginBonusDate) {
      const lastBonusDate = new Date(user.lastLoginBonusDate);
      const lastBonusDay = new Date(
        lastBonusDate.getFullYear(),
        lastBonusDate.getMonth(),
        lastBonusDate.getDate()
      );
      
      // Already claimed today
      if (lastBonusDay.getTime() === today.getTime()) {
        return null;
      }
    }

    // Calculate consecutive login days
    let consecutiveDays = user.consecutiveLoginDays || 0;
    
    if (user.lastLoginBonusDate) {
      const lastBonusDate = new Date(user.lastLoginBonusDate);
      const lastBonusDay = new Date(
        lastBonusDate.getFullYear(),
        lastBonusDate.getMonth(),
        lastBonusDate.getDate()
      );
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      
      // Check if last bonus was claimed yesterday (consecutive)
      if (lastBonusDay.getTime() === yesterday.getTime()) {
        consecutiveDays += 1;
      } else {
        // Streak broken, reset to 1
        consecutiveDays = 1;
      }
    } else {
      // First time claiming bonus
      consecutiveDays = 1;
    }

    // Calculate bonus rewards based on consecutive days
    // Day 1: 5 stars, 1 heart
    // Day 2: 7 stars, 1 heart
    // Day 3: 10 stars, 1 heart
    // Day 4: 12 stars, 2 hearts
    // Day 5: 15 stars, 2 hearts
    // Day 6: 18 stars, 2 hearts
    // Day 7+: 20 stars, 3 hearts (max bonus)
    
    let starsReward = 5;
    let heartsReward = 1;
    
    if (consecutiveDays >= 7) {
      starsReward = 20;
      heartsReward = 3;
    } else if (consecutiveDays === 6) {
      starsReward = 18;
      heartsReward = 2;
    } else if (consecutiveDays === 5) {
      starsReward = 15;
      heartsReward = 2;
    } else if (consecutiveDays === 4) {
      starsReward = 12;
      heartsReward = 2;
    } else if (consecutiveDays === 3) {
      starsReward = 10;
      heartsReward = 1;
    } else if (consecutiveDays === 2) {
      starsReward = 7;
      heartsReward = 1;
    }

    // Update user stats
    const newStars = user.stars + starsReward;
    const newHearts = Math.min(user.hearts + heartsReward, user.maxHearts);
    const newStreak = consecutiveDays;

    await db
      .update(users)
      .set({
        stars: newStars,
        hearts: newHearts,
        streak: newStreak,
        consecutiveLoginDays: consecutiveDays,
        lastLoginBonusDate: now,
        updatedAt: now,
      })
      .where(eq(users.id, userId));

    return {
      starsReward,
      heartsReward,
      consecutiveDays,
      newStars,
      newHearts,
      newStreak,
    };
  }),

  /**
   * Get daily bonus status (without claiming)
   * Returns whether bonus is available and what the reward would be
   */
  getBonusStatus: protectedProcedure.query(async ({ ctx }) => {
    const userId = ctx.user.id;

    const db = await getDb();
    if (!db) throw new Error("Database not available");
    
    const [user] = await db.select().from(users).where(eq(users.id, userId));
    
    if (!user) {
      throw new Error("User not found");
    }

    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    
    let isAvailable = true;
    
    // Check if user already claimed bonus today
    if (user.lastLoginBonusDate) {
      const lastBonusDate = new Date(user.lastLoginBonusDate);
      const lastBonusDay = new Date(
        lastBonusDate.getFullYear(),
        lastBonusDate.getMonth(),
        lastBonusDate.getDate()
      );
      
      if (lastBonusDay.getTime() === today.getTime()) {
        isAvailable = false;
      }
    }

    // Calculate what the next bonus would be
    let nextConsecutiveDays = user.consecutiveLoginDays || 0;
    
    if (isAvailable && user.lastLoginBonusDate) {
      const lastBonusDate = new Date(user.lastLoginBonusDate);
      const lastBonusDay = new Date(
        lastBonusDate.getFullYear(),
        lastBonusDate.getMonth(),
        lastBonusDate.getDate()
      );
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      
      if (lastBonusDay.getTime() === yesterday.getTime()) {
        nextConsecutiveDays += 1;
      } else {
        nextConsecutiveDays = 1;
      }
    } else if (isAvailable) {
      nextConsecutiveDays = 1;
    }

    // Calculate next rewards
    let nextStarsReward = 5;
    let nextHeartsReward = 1;
    
    if (nextConsecutiveDays >= 7) {
      nextStarsReward = 20;
      nextHeartsReward = 3;
    } else if (nextConsecutiveDays === 6) {
      nextStarsReward = 18;
      nextHeartsReward = 2;
    } else if (nextConsecutiveDays === 5) {
      nextStarsReward = 15;
      nextHeartsReward = 2;
    } else if (nextConsecutiveDays === 4) {
      nextStarsReward = 12;
      nextHeartsReward = 2;
    } else if (nextConsecutiveDays === 3) {
      nextStarsReward = 10;
      nextHeartsReward = 1;
    } else if (nextConsecutiveDays === 2) {
      nextStarsReward = 7;
      nextHeartsReward = 1;
    }

    return {
      isAvailable,
      currentConsecutiveDays: user.consecutiveLoginDays || 0,
      nextConsecutiveDays,
      nextStarsReward,
      nextHeartsReward,
      lastClaimedDate: user.lastLoginBonusDate,
    };
  }),
});
