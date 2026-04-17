import { drizzle } from "drizzle-orm/mysql2";
import * as schema from "./drizzle/schema.ts";
import dotenv from "dotenv";

dotenv.config();

const db = drizzle(process.env.DATABASE_URL);

// Mission data
const missions = [
  // Beginner missions
  {
    title: "Luna Meets Friends",
    emoji: "👋",
    duration: 5,
    stars: 15,
    difficulty: "beginner",
    category: "conversation",
    scenarioCharacter: "Luna",
    scenarioSituation: "Help Luna introduce herself to new friends",
    scenarioTargetWord: "greetings",
  },
  {
    title: "Luna is Hungry!",
    emoji: "🍎",
    duration: 3,
    stars: 10,
    difficulty: "beginner",
    category: "vocabulary",
    scenarioCharacter: "Luna",
    scenarioSituation: "Learn food vocabulary with Luna",
    scenarioTargetWord: "food",
  },
  {
    title: "Luna is Thirsty!",
    emoji: "🥤",
    duration: 4,
    stars: 15,
    difficulty: "beginner",
    category: "vocabulary",
    scenarioCharacter: "Luna",
    scenarioSituation: "Practice drink-related expressions",
    scenarioTargetWord: "drinks",
  },
  {
    title: "Luna's Family",
    emoji: "👨‍👩‍👧‍👦",
    duration: 5,
    stars: 15,
    difficulty: "beginner",
    category: "vocabulary",
    scenarioCharacter: "Luna",
    scenarioSituation: "Learn family member names and relationships",
    scenarioTargetWord: "family",
  },
  {
    title: "Colors with Luna",
    emoji: "🎨",
    duration: 4,
    stars: 10,
    difficulty: "beginner",
    category: "vocabulary",
    scenarioCharacter: "Luna",
    scenarioSituation: "Identify and name different colors",
    scenarioTargetWord: "colors",
  },
  
  // Intermediate missions
  {
    title: "Luna Goes Shopping",
    emoji: "🛒",
    duration: 8,
    stars: 25,
    difficulty: "intermediate",
    category: "conversation",
    scenarioCharacter: "Luna",
    scenarioSituation: "Practice shopping conversations and numbers",
    scenarioTargetWord: "shopping",
  },
  {
    title: "Luna's Daily Routine",
    emoji: "⏰",
    duration: 10,
    stars: 30,
    difficulty: "intermediate",
    category: "grammar",
    scenarioCharacter: "Luna",
    scenarioSituation: "Learn time expressions and daily activities",
    scenarioTargetWord: "time",
  },
  {
    title: "Weather Talk",
    emoji: "🌤️",
    duration: 7,
    stars: 20,
    difficulty: "intermediate",
    category: "conversation",
    scenarioCharacter: "Luna",
    scenarioSituation: "Describe weather conditions and seasons",
    scenarioTargetWord: "weather",
  },
  {
    title: "At the Restaurant",
    emoji: "🍽️",
    duration: 9,
    stars: 25,
    difficulty: "intermediate",
    category: "conversation",
    scenarioCharacter: "Luna",
    scenarioSituation: "Order food and practice restaurant conversations",
    scenarioTargetWord: "restaurant",
  },
  {
    title: "Luna's Hobbies",
    emoji: "🎮",
    duration: 8,
    stars: 20,
    difficulty: "intermediate",
    category: "conversation",
    scenarioCharacter: "Luna",
    scenarioSituation: "Talk about hobbies and free time activities",
    scenarioTargetWord: "hobbies",
  },
  
  // Advanced missions
  {
    title: "Job Interview",
    emoji: "💼",
    duration: 15,
    stars: 40,
    difficulty: "advanced",
    category: "conversation",
    scenarioCharacter: "Luna",
    scenarioSituation: "Practice professional conversation skills",
    scenarioTargetWord: "interview",
  },
  {
    title: "Travel Adventure",
    emoji: "✈️",
    duration: 12,
    stars: 35,
    difficulty: "advanced",
    category: "conversation",
    scenarioCharacter: "Luna",
    scenarioSituation: "Learn travel-related vocabulary and expressions",
    scenarioTargetWord: "travel",
  },
  {
    title: "Grammar Master",
    emoji: "📚",
    duration: 20,
    stars: 50,
    difficulty: "advanced",
    category: "grammar",
    scenarioCharacter: "Luna",
    scenarioSituation: "Master complex grammar structures",
    scenarioTargetWord: "grammar",
  },
  {
    title: "Storytelling",
    emoji: "📖",
    duration: 18,
    stars: 45,
    difficulty: "advanced",
    category: "writing",
    scenarioCharacter: "Luna",
    scenarioSituation: "Create and tell your own story in English",
    scenarioTargetWord: "story",
  },
  {
    title: "Debate Club",
    emoji: "💬",
    duration: 15,
    stars: 40,
    difficulty: "advanced",
    category: "conversation",
    scenarioCharacter: "Luna",
    scenarioSituation: "Express opinions and debate on various topics",
    scenarioTargetWord: "debate",
  },
];

// Vocabulary categories and words
const vocabularyData = [
  {
    category: {
      name: "Animals",
      emoji: "🐾",
      wordCount: 10,
    },
    words: [
      { word: "dog", translation: "개", emoji: "🐶" },
      { word: "cat", translation: "고양이", emoji: "🐱" },
      { word: "bird", translation: "새", emoji: "🐦" },
      { word: "fish", translation: "물고기", emoji: "🐟" },
      { word: "rabbit", translation: "토끼", emoji: "🐰" },
      { word: "elephant", translation: "코끼리", emoji: "🐘" },
      { word: "lion", translation: "사자", emoji: "🦁" },
      { word: "tiger", translation: "호랑이", emoji: "🐯" },
      { word: "bear", translation: "곰", emoji: "🐻" },
      { word: "monkey", translation: "원숭이", emoji: "🐵" },
    ],
  },
  {
    category: {
      name: "Food & Drinks",
      emoji: "🍕",
      wordCount: 10,
    },
    words: [
      { word: "apple", translation: "사과", emoji: "🍎" },
      { word: "banana", translation: "바나나", emoji: "🍌" },
      { word: "orange", translation: "오렌지", emoji: "🍊" },
      { word: "bread", translation: "빵", emoji: "🍞" },
      { word: "rice", translation: "밥", emoji: "🍚" },
      { word: "milk", translation: "우유", emoji: "🥛" },
      { word: "water", translation: "물", emoji: "💧" },
      { word: "juice", translation: "주스", emoji: "🧃" },
      { word: "coffee", translation: "커피", emoji: "☕" },
      { word: "tea", translation: "차", emoji: "🍵" },
    ],
  },
  {
    category: {
      name: "Numbers",
      emoji: "🔢",
      wordCount: 10,
    },
    words: [
      { word: "one", translation: "하나", emoji: "1️⃣" },
      { word: "two", translation: "둘", emoji: "2️⃣" },
      { word: "three", translation: "셋", emoji: "3️⃣" },
      { word: "four", translation: "넷", emoji: "4️⃣" },
      { word: "five", translation: "다섯", emoji: "5️⃣" },
      { word: "six", translation: "여섯", emoji: "6️⃣" },
      { word: "seven", translation: "일곱", emoji: "7️⃣" },
      { word: "eight", translation: "여덟", emoji: "8️⃣" },
      { word: "nine", translation: "아홉", emoji: "9️⃣" },
      { word: "ten", translation: "열", emoji: "🔟" },
    ],
  },
  {
    category: {
      name: "Colors",
      emoji: "🎨",
      wordCount: 8,
    },
    words: [
      { word: "red", translation: "빨강", emoji: "🔴" },
      { word: "blue", translation: "파랑", emoji: "🔵" },
      { word: "yellow", translation: "노랑", emoji: "🟡" },
      { word: "green", translation: "초록", emoji: "🟢" },
      { word: "orange", translation: "주황", emoji: "🟠" },
      { word: "purple", translation: "보라", emoji: "🟣" },
      { word: "pink", translation: "분홍", emoji: "🩷" },
      { word: "brown", translation: "갈색", emoji: "🟤" },
    ],
  },
  {
    category: {
      name: "Family",
      emoji: "👨‍👩‍👧‍👦",
      wordCount: 8,
    },
    words: [
      { word: "mother", translation: "어머니", emoji: "👩" },
      { word: "father", translation: "아버지", emoji: "👨" },
      { word: "sister", translation: "자매", emoji: "👧" },
      { word: "brother", translation: "형제", emoji: "👦" },
      { word: "grandmother", translation: "할머니", emoji: "👵" },
      { word: "grandfather", translation: "할아버지", emoji: "👴" },
      { word: "daughter", translation: "딸", emoji: "👧" },
      { word: "son", translation: "아들", emoji: "👦" },
    ],
  },
];

// Shop items
const shopItems = [
  // Power-ups
  {
    name: "Heart Refill",
    emoji: "❤️",
    price: 50,
    category: "powerup",
  },
  {
    name: "Double XP",
    emoji: "⚡",
    price: 100,
    category: "powerup",
  },
  {
    name: "Streak Freeze",
    emoji: "🧊",
    price: 75,
    category: "powerup",
  },
  
  // Cosmetics
  {
    name: "Luna's Hat",
    emoji: "🎭",
    price: 200,
    category: "cosmetic",
  },
  {
    name: "Luna's Glasses",
    emoji: "👓",
    price: 150,
    category: "cosmetic",
  },
  {
    name: "Luna's Bow",
    emoji: "🎀",
    price: 180,
    category: "cosmetic",
  },
  
  // Themes
  {
    name: "Ocean Theme",
    emoji: "🌊",
    price: 300,
    category: "theme",
  },
  {
    name: "Forest Theme",
    emoji: "🌲",
    price: 300,
    category: "theme",
  },
  {
    name: "Space Theme",
    emoji: "🌌",
    price: 350,
    category: "theme",
  },
  
  // Special items
  {
    name: "Lucky Charm",
    emoji: "🍀",
    price: 500,
    category: "special",
  },
];

async function seedDatabase() {
  console.log("🌱 Starting database seeding...\n");

  try {
    // Seed missions
    console.log("📝 Seeding missions...");
    for (const mission of missions) {
      await db.insert(schema.missions).values(mission);
    }
    console.log(`✅ Inserted ${missions.length} missions\n`);

    // Seed vocabulary categories and words
    console.log("📚 Seeding vocabulary data...");
    for (const vocabData of vocabularyData) {
      // Insert category
      const [result] = await db.insert(schema.vocabularyCategories).values(vocabData.category);
      const categoryId = result.insertId;
      
      // Insert words for this category
      for (const word of vocabData.words) {
        await db.insert(schema.vocabularyWords).values({
          ...word,
          categoryId,
        });
      }
      console.log(`  ✅ Inserted category "${vocabData.category.name}" with ${vocabData.words.length} words`);
    }
    console.log(`✅ Inserted ${vocabularyData.length} vocabulary categories\n`);

    // Seed shop items
    console.log("🛍️ Seeding shop items...");
    for (const item of shopItems) {
      await db.insert(schema.shopItems).values(item);
    }
    console.log(`✅ Inserted ${shopItems.length} shop items\n`);

    console.log("🎉 Database seeding completed successfully!");
  } catch (error) {
    console.error("❌ Error seeding database:", error);
    process.exit(1);
  }
}

seedDatabase();
