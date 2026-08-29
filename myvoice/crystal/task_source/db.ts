import { eq, and, gte, lte, desc } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import * as schema from "../drizzle/schema";
import { InsertUser, users } from "../drizzle/schema";
import { ENV } from './_core/env';

let _db: ReturnType<typeof drizzle> | null = null;

// Lazily create the drizzle instance so local tooling can run without a DB.
export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get user: database not available");
    return undefined;
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);

  return result.length > 0 ? result[0] : undefined;
}

/**
 * User stats queries
 */
export async function updateUserStats(userId: number, stats: {
  stars?: number;
  hearts?: number;
  streak?: number;
  level?: number;
  xp?: number;
  onboardingCompleted?: boolean;
}) {
  const db = await getDb();
  if (!db) return;
  await db.update(users).set(stats).where(eq(users.id, userId));
}

/**
 * Weekly goals queries
 */
export async function getCurrentWeeklyGoal(userId: number) {
  const db = await getDb();
  if (!db) return undefined;
  
  const now = new Date();
  const [goal] = await db
    .select()
    .from(schema.weeklyGoals)
    .where(
      and(
        eq(schema.weeklyGoals.userId, userId),
        lte(schema.weeklyGoals.weekStartDate, now),
        gte(schema.weeklyGoals.weekEndDate, now)
      )
    )
    .orderBy(desc(schema.weeklyGoals.createdAt))
    .limit(1);
  
  return goal;
}

export async function createWeeklyGoal(data: schema.InsertWeeklyGoal) {
  const db = await getDb();
  if (!db) return 0;
  const [result] = await db.insert(schema.weeklyGoals).values(data);
  return result.insertId;
}

export async function updateWeeklyGoalProgress(goalId: number, progress: {
  xpCurrent?: number;
  missionsCurrent?: number;
  studyTimeCurrent?: number;
  wordsCurrent?: number;
}) {
  const db = await getDb();
  if (!db) return;
  await db.update(schema.weeklyGoals).set(progress).where(eq(schema.weeklyGoals.id, goalId));
}

export async function updateWeeklyGoalTargets(goalId: number, targets: {
  xpTarget?: number;
  missionsTarget?: number;
  studyTimeTarget?: number;
  wordsTarget?: number;
}) {
  const db = await getDb();
  if (!db) return;
  await db.update(schema.weeklyGoals).set(targets).where(eq(schema.weeklyGoals.id, goalId));
}

/**
 * Missions queries
 */
export async function getAllMissions() {
  const db = await getDb();
  if (!db) return [];
  return await db.select().from(schema.missions);
}

export async function getUserMissions(userId: number) {
  const db = await getDb();
  if (!db) return [];
  return await db.select().from(schema.userMissions).where(eq(schema.userMissions.userId, userId));
}

export async function updateUserMissionStatus(
  userId: number,
  missionId: number,
  status: "completed" | "in_progress" | "locked",
  score?: number
) {
  const db = await getDb();
  if (!db) return;
  
  const completedAt = status === "completed" ? new Date() : null;
  
  // Check if user mission exists
  const existing = await db
    .select()
    .from(schema.userMissions)
    .where(
      and(
        eq(schema.userMissions.userId, userId),
        eq(schema.userMissions.missionId, missionId)
      )
    );
  
  if (existing.length > 0) {
    await db
      .update(schema.userMissions)
      .set({ status, score, completedAt })
      .where(
        and(
          eq(schema.userMissions.userId, userId),
          eq(schema.userMissions.missionId, missionId)
        )
      );
  } else {
    await db.insert(schema.userMissions).values({
      userId,
      missionId,
      status,
      score,
      completedAt,
    });
  }
}

/**
 * Vocabulary queries
 */
export async function getAllVocabularyCategories() {
  const db = await getDb();
  if (!db) return [];
  return await db.select().from(schema.vocabularyCategories);
}

export async function getVocabularyWordsByCategory(categoryId: number) {
  const db = await getDb();
  if (!db) return [];
  return await db.select().from(schema.vocabularyWords).where(eq(schema.vocabularyWords.categoryId, categoryId));
}

export async function getUserVocabularyProgress(userId: number) {
  const db = await getDb();
  if (!db) return [];
  return await db.select().from(schema.userVocabulary).where(eq(schema.userVocabulary.userId, userId));
}

export async function updateUserVocabularyProgress(
  userId: number,
  wordId: number,
  data: {
    learned?: boolean;
    accuracy?: number;
    attempts?: number;
  }
) {
  const db = await getDb();
  if (!db) return;
  
  const existing = await db
    .select()
    .from(schema.userVocabulary)
    .where(
      and(
        eq(schema.userVocabulary.userId, userId),
        eq(schema.userVocabulary.wordId, wordId)
      )
    );

  if (existing.length > 0) {
    await db
      .update(schema.userVocabulary)
      .set({ ...data, lastPracticedAt: new Date() })
      .where(
        and(
          eq(schema.userVocabulary.userId, userId),
          eq(schema.userVocabulary.wordId, wordId)
        )
      );
  } else {
    await db.insert(schema.userVocabulary).values({
      userId,
      wordId,
      ...data,
      lastPracticedAt: new Date(),
    });
  }
}

/**
 * Skills queries
 */
export async function getUserSkills(userId: number) {
  const db = await getDb();
  if (!db) return [];
  return await db.select().from(schema.skills).where(eq(schema.skills.userId, userId));
}

export async function updateUserSkill(userId: number, skillId: string, data: {
  score?: number;
  level?: number;
}) {
  const db = await getDb();
  if (!db) return;
  
  const existing = await db
    .select()
    .from(schema.skills)
    .where(
      and(
        eq(schema.skills.userId, userId),
        eq(schema.skills.skillId, skillId)
      )
    );

  if (existing.length > 0) {
    await db
      .update(schema.skills)
      .set(data)
      .where(
        and(
          eq(schema.skills.userId, userId),
          eq(schema.skills.skillId, skillId)
        )
      );
  } else {
    const category = skillId.includes("vocab") || skillId.includes("pronunciation") 
      ? "language" as const
      : skillId.includes("memory") || skillId.includes("problem") 
      ? "cognitive" as const
      : "emotional" as const;
    
    await db.insert(schema.skills).values({
      userId,
      skillId,
      category,
      ...data,
    });
  }
}

/**
 * Badges queries
 */
export async function getUserBadges(userId: number) {
  const db = await getDb();
  if (!db) return [];
  return await db.select().from(schema.badges).where(eq(schema.badges.userId, userId));
}

export async function awardBadge(data: schema.InsertBadge) {
  const db = await getDb();
  if (!db) return 0;
  const [result] = await db.insert(schema.badges).values(data);
  return result.insertId;
}

/**
 * Shop queries
 */
export async function getAllShopItems() {
  const db = await getDb();
  if (!db) return [];
  return await db.select().from(schema.shopItems);
}

export async function getUserInventory(userId: number) {
  const db = await getDb();
  if (!db) return [];
  return await db.select().from(schema.userInventory).where(eq(schema.userInventory.userId, userId));
}

export async function purchaseItem(userId: number, itemId: number) {
  const db = await getDb();
  if (!db) return 0;
  const [result] = await db.insert(schema.userInventory).values({
    userId,
    itemId,
    quantity: 1,
  });
  return result.insertId;
}

/**
 * Learning history queries
 */
export async function getLearningHistory(userId: number, startDate: Date, endDate: Date) {
  const db = await getDb();
  if (!db) return [];
  return await db
    .select()
    .from(schema.learningHistory)
    .where(
      and(
        eq(schema.learningHistory.userId, userId),
        gte(schema.learningHistory.date, startDate),
        lte(schema.learningHistory.date, endDate)
      )
    )
    .orderBy(schema.learningHistory.date);
}

export async function updateLearningHistory(userId: number, date: Date, data: {
  xpEarned?: number;
  missionsCompleted?: number;
  wordsLearned?: number;
  studyTimeMinutes?: number;
}) {
  const db = await getDb();
  if (!db) return;
  
  const dateStr = date.toISOString().split('T')[0];
  const existing = await db
    .select()
    .from(schema.learningHistory)
    .where(
      and(
        eq(schema.learningHistory.userId, userId),
        eq(schema.learningHistory.date, new Date(dateStr))
      )
    );

  if (existing.length > 0) {
    await db
      .update(schema.learningHistory)
      .set(data)
      .where(
        and(
          eq(schema.learningHistory.userId, userId),
          eq(schema.learningHistory.date, new Date(dateStr))
        )
      );
  } else {
    await db.insert(schema.learningHistory).values({
      userId,
      date: new Date(dateStr),
      ...data,
    });
  }
}
