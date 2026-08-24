import { int, mysqlEnum, mysqlTable, text, timestamp, varchar, float, boolean } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  
  // User profile data
  nickname: varchar("nickname", { length: 100 }),
  avatar: varchar("avatar", { length: 10 }).default("🐰"),
  
  // Game stats
  stars: int("stars").default(120).notNull(),
  hearts: int("hearts").default(3).notNull(),
  maxHearts: int("maxHearts").default(3).notNull(),
  streak: int("streak").default(7).notNull(),
  level: int("level").default(5).notNull(),
  xp: int("xp").default(1220).notNull(),
  
  // Daily login bonus tracking
  lastLoginBonusDate: timestamp("lastLoginBonusDate"),
  consecutiveLoginDays: int("consecutiveLoginDays").default(0).notNull(),
  
  // Onboarding
  onboardingCompleted: boolean("onboardingCompleted").default(false).notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * Weekly goals table - tracks user's weekly learning goals
 */
export const weeklyGoals = mysqlTable("weekly_goals", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  
  // XP goal
  xpTarget: int("xpTarget").default(1500).notNull(),
  xpCurrent: int("xpCurrent").default(1220).notNull(),
  
  // Mission goal
  missionsTarget: int("missionsTarget").default(25).notNull(),
  missionsCurrent: int("missionsCurrent").default(21).notNull(),
  
  // Study time goal (in hours)
  studyTimeTarget: float("studyTimeTarget").default(15).notNull(),
  studyTimeCurrent: float("studyTimeCurrent").default(12.5).notNull(),
  
  // Words goal
  wordsTarget: int("wordsTarget").default(200).notNull(),
  wordsCurrent: int("wordsCurrent").default(152).notNull(),
  
  weekStartDate: timestamp("weekStartDate").notNull(),
  weekEndDate: timestamp("weekEndDate").notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type WeeklyGoal = typeof weeklyGoals.$inferSelect;
export type InsertWeeklyGoal = typeof weeklyGoals.$inferInsert;

/**
 * Missions table - tracks available missions
 */
export const missions = mysqlTable("missions", {
  id: int("id").autoincrement().primaryKey(),
  title: varchar("title", { length: 255 }).notNull(),
  emoji: varchar("emoji", { length: 10 }).notNull(),
  duration: int("duration").notNull(), // in minutes
  stars: int("stars").notNull(),
  difficulty: mysqlEnum("difficulty", ["beginner", "intermediate", "advanced"]).notNull(),
  category: varchar("category", { length: 100 }).notNull(),
  status: mysqlEnum("status", ["completed", "in_progress", "locked"]).default("locked").notNull(),
  
  // Mission scenario
  scenarioCharacter: varchar("scenarioCharacter", { length: 255 }),
  scenarioSituation: text("scenarioSituation"),
  scenarioTargetWord: varchar("scenarioTargetWord", { length: 100 }),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Mission = typeof missions.$inferSelect;
export type InsertMission = typeof missions.$inferInsert;

/**
 * User missions table - tracks user progress on missions
 */
export const userMissions = mysqlTable("user_missions", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  missionId: int("missionId").notNull(),
  status: mysqlEnum("status", ["completed", "in_progress", "locked"]).default("locked").notNull(),
  score: int("score"), // pronunciation accuracy score
  completedAt: timestamp("completedAt"),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type UserMission = typeof userMissions.$inferSelect;
export type InsertUserMission = typeof userMissions.$inferInsert;

/**
 * Vocabulary categories table
 */
export const vocabularyCategories = mysqlTable("vocabulary_categories", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 100 }).notNull(),
  emoji: varchar("emoji", { length: 10 }).notNull(),
  wordCount: int("wordCount").notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type VocabularyCategory = typeof vocabularyCategories.$inferSelect;
export type InsertVocabularyCategory = typeof vocabularyCategories.$inferInsert;

/**
 * Vocabulary words table
 */
export const vocabularyWords = mysqlTable("vocabulary_words", {
  id: int("id").autoincrement().primaryKey(),
  categoryId: int("categoryId").notNull(),
  word: varchar("word", { length: 100 }).notNull(),
  translation: varchar("translation", { length: 100 }).notNull(),
  emoji: varchar("emoji", { length: 10 }).notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type VocabularyWord = typeof vocabularyWords.$inferSelect;
export type InsertVocabularyWord = typeof vocabularyWords.$inferInsert;

/**
 * User vocabulary progress table
 */
export const userVocabulary = mysqlTable("user_vocabulary", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  wordId: int("wordId").notNull(),
  learned: boolean("learned").default(false).notNull(),
  accuracy: int("accuracy"), // pronunciation accuracy percentage
  attempts: int("attempts").default(0).notNull(),
  lastPracticedAt: timestamp("lastPracticedAt"),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type UserVocabulary = typeof userVocabulary.$inferSelect;
export type InsertUserVocabulary = typeof userVocabulary.$inferInsert;

/**
 * Skills table - tracks user's skill progress
 */
export const skills = mysqlTable("skills", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  skillId: varchar("skillId", { length: 100 }).notNull(), // e.g., "daily_vocab"
  category: mysqlEnum("category", ["language", "cognitive", "emotional"]).notNull(),
  score: int("score").default(0).notNull(),
  level: int("level").default(1).notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Skill = typeof skills.$inferSelect;
export type InsertSkill = typeof skills.$inferInsert;

/**
 * Badges table - tracks user's earned badges
 */
export const badges = mysqlTable("badges", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  badgeId: varchar("badgeId", { length: 100 }).notNull(), // e.g., "first_mission"
  name: varchar("name", { length: 255 }).notNull(),
  description: text("description"),
  emoji: varchar("emoji", { length: 10 }).notNull(),
  earnedAt: timestamp("earnedAt").defaultNow().notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type Badge = typeof badges.$inferSelect;
export type InsertBadge = typeof badges.$inferInsert;

/**
 * Shop items table
 */
export const shopItems = mysqlTable("shop_items", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 255 }).notNull(),
  emoji: varchar("emoji", { length: 10 }).notNull(),
  price: int("price").notNull(),
  category: varchar("category", { length: 100 }).notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type ShopItem = typeof shopItems.$inferSelect;
export type InsertShopItem = typeof shopItems.$inferInsert;

/**
 * User inventory table
 */
export const userInventory = mysqlTable("user_inventory", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  itemId: int("itemId").notNull(),
  quantity: int("quantity").default(1).notNull(),
  purchasedAt: timestamp("purchasedAt").defaultNow().notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type UserInventoryItem = typeof userInventory.$inferSelect;
export type InsertUserInventoryItem = typeof userInventory.$inferInsert;

/**
 * Learning history table - tracks daily learning activity
 */
export const learningHistory = mysqlTable("learning_history", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  date: timestamp("date").notNull(),
  xpEarned: int("xpEarned").default(0).notNull(),
  missionsCompleted: int("missionsCompleted").default(0).notNull(),
  wordsLearned: int("wordsLearned").default(0).notNull(),
  studyTimeMinutes: int("studyTimeMinutes").default(0).notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type LearningHistory = typeof learningHistory.$inferSelect;
export type InsertLearningHistory = typeof learningHistory.$inferInsert;
