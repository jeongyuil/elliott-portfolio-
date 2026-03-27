import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, protectedProcedure, router } from "./_core/trpc";
import { z } from "zod";
import * as db from "./db";
import { dailyBonusRouter } from "./trpc/routers/dailyBonus";

export const appRouter = router({
    // if you need to use socket.io, read and register route in server/_core/index.ts, all api should start with '/api/' so that the gateway can route correctly
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  // Learning data routers
  weeklyGoals: router({
    getCurrent: protectedProcedure.query(async ({ ctx }) => {
      let goal = await db.getCurrentWeeklyGoal(ctx.user.id);
      
      // Auto-create weekly goal if not exists
      if (!goal) {
        const now = new Date();
        const weekStart = new Date(now);
        weekStart.setDate(now.getDate() - now.getDay()); // Start of week (Sunday)
        weekStart.setHours(0, 0, 0, 0);
        
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekStart.getDate() + 6); // End of week (Saturday)
        weekEnd.setHours(23, 59, 59, 999);
        
        const goalId = await db.createWeeklyGoal({
          userId: ctx.user.id,
          xpTarget: 1500,
          xpCurrent: 0,
          missionsTarget: 25,
          missionsCurrent: 0,
          studyTimeTarget: 15,
          studyTimeCurrent: 0,
          wordsTarget: 200,
          wordsCurrent: 0,
          weekStartDate: weekStart,
          weekEndDate: weekEnd,
        });
        
        goal = await db.getCurrentWeeklyGoal(ctx.user.id);
      }
      
      return goal;
    }),
    
    updateProgress: protectedProcedure
      .input(z.object({
        xpCurrent: z.number().optional(),
        missionsCurrent: z.number().optional(),
        studyTimeCurrent: z.number().optional(),
        wordsCurrent: z.number().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        const goal = await db.getCurrentWeeklyGoal(ctx.user.id);
        if (!goal) {
          throw new Error("No active weekly goal found");
        }
        await db.updateWeeklyGoalProgress(goal.id, input);
        return { success: true };
      }),
    
    updateTargets: protectedProcedure
      .input(z.object({
        xpTarget: z.number().optional(),
        missionsTarget: z.number().optional(),
        studyTimeTarget: z.number().optional(),
        wordsTarget: z.number().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        const goal = await db.getCurrentWeeklyGoal(ctx.user.id);
        if (!goal) {
          throw new Error("No active weekly goal found");
        }
        await db.updateWeeklyGoalTargets(goal.id, input);
        return { success: true };
      }),
  }),
  
  missions: router({
    getAll: publicProcedure.query(async () => {
      return await db.getAllMissions();
    }),
    
    getUserMissions: protectedProcedure.query(async ({ ctx }) => {
      return await db.getUserMissions(ctx.user.id);
    }),
    
    updateStatus: protectedProcedure
      .input(z.object({
        missionId: z.number(),
        status: z.enum(["completed", "in_progress", "locked"]),
        score: z.number().optional(),
        earnedXp: z.number().optional(), // XP earned from completing the mission
      }))
      .mutation(async ({ ctx, input }) => {
        const wasCompleted = input.status === "completed";
        
        // Update mission status
        await db.updateUserMissionStatus(ctx.user.id, input.missionId, input.status, input.score);
        
        // If mission was completed, update weekly goals
        if (wasCompleted) {
          const currentGoal = await db.getCurrentWeeklyGoal(ctx.user.id);
          if (currentGoal) {
            const xpToAdd = input.earnedXp || 0;
            await db.updateWeeklyGoalProgress(
              currentGoal.id,
              {
                xpCurrent: currentGoal.xpCurrent + xpToAdd,
                missionsCurrent: currentGoal.missionsCurrent + 1,
              }
            );
          }
        }
        
        return { success: true };
      }),
  }),
  
  vocabulary: router({
    getCategories: publicProcedure.query(async () => {
      return await db.getAllVocabularyCategories();
    }),
    
    getWordsByCategory: publicProcedure
      .input(z.object({ categoryId: z.number() }))
      .query(async ({ input }) => {
        return await db.getVocabularyWordsByCategory(input.categoryId);
      }),
    
    getUserProgress: protectedProcedure.query(async ({ ctx }) => {
      return await db.getUserVocabularyProgress(ctx.user.id);
    }),
    
    updateProgress: protectedProcedure
      .input(z.object({
        wordId: z.number(),
        learned: z.boolean().optional(),
        accuracy: z.number().optional(),
        attempts: z.number().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        const { wordId, ...data } = input;
        await db.updateUserVocabularyProgress(ctx.user.id, wordId, data);
        return { success: true };
      }),
    
    completeCategory: protectedProcedure
      .input(z.object({
        categoryId: z.number(),
        wordsLearned: z.number(),
        earnedStars: z.number(),
        earnedXp: z.number(),
      }))
      .mutation(async ({ ctx, input }) => {
        // Update user stats (stars and XP)
        await db.updateUserStats(ctx.user.id, {
          stars: input.earnedStars,
          xp: input.earnedXp,
        });
        
        // Get current weekly goal
        const goal = await db.getCurrentWeeklyGoal(ctx.user.id);
        if (goal) {
          // Update weekly goals (words learned and XP)
          await db.updateWeeklyGoalProgress(goal.id, {
            wordsCurrent: goal.wordsCurrent + input.wordsLearned,
            xpCurrent: goal.xpCurrent + input.earnedXp,
          });
        }
        
        return { success: true };
      }),
  }),
  
  skills: router({
    getUserSkills: protectedProcedure.query(async ({ ctx }) => {
      return await db.getUserSkills(ctx.user.id);
    }),
    
    updateSkill: protectedProcedure
      .input(z.object({
        skillId: z.string(),
        score: z.number().optional(),
        level: z.number().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        const { skillId, ...data } = input;
        await db.updateUserSkill(ctx.user.id, skillId, data);
        return { success: true };
      }),
  }),
  
  badges: router({
    getUserBadges: protectedProcedure.query(async ({ ctx }) => {
      return await db.getUserBadges(ctx.user.id);
    }),
  }),
  
  shop: router({
    getItems: publicProcedure.query(async () => {
      return await db.getAllShopItems();
    }),
    
    getUserInventory: protectedProcedure.query(async ({ ctx }) => {
      return await db.getUserInventory(ctx.user.id);
    }),
    
    purchaseItem: protectedProcedure
      .input(z.object({ itemId: z.number() }))
      .mutation(async ({ ctx, input }) => {
        await db.purchaseItem(ctx.user.id, input.itemId);
        return { success: true };
      }),
  }),
  
  learningHistory: router({
    getHistory: protectedProcedure
      .input(z.object({
        startDate: z.date(),
        endDate: z.date(),
      }))
      .query(async ({ ctx, input }) => {
        return await db.getLearningHistory(ctx.user.id, input.startDate, input.endDate);
      }),
    
    updateHistory: protectedProcedure
      .input(z.object({
        date: z.date(),
        xpEarned: z.number().optional(),
        missionsCompleted: z.number().optional(),
        wordsLearned: z.number().optional(),
        studyTimeMinutes: z.number().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        const { date, ...data } = input;
        await db.updateLearningHistory(ctx.user.id, date, data);
        return { success: true };
      }),
  }),
  
  dailyBonus: dailyBonusRouter,
  
  user: router({
    getStats: protectedProcedure.query(async ({ ctx }) => {
      return ctx.user;
    }),
    
    updateStats: protectedProcedure
      .input(z.object({
        stars: z.number().optional(),
        hearts: z.number().optional(),
        streak: z.number().optional(),
        level: z.number().optional(),
        xp: z.number().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        await db.updateUserStats(ctx.user.id, input);
        return { success: true };
      }),
    
    completeOnboarding: protectedProcedure.mutation(async ({ ctx }) => {
      await db.updateUserStats(ctx.user.id, { onboardingCompleted: true });
      return { success: true };
    }),
  }),
});

export type AppRouter = typeof appRouter;
