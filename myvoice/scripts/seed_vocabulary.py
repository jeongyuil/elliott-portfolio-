"""
Seed vocabulary words for 10 empty categories.

Existing categories with data: food (10 words), animals (10 words)
This script adds 10 words each for: colors, numbers, family, body,
weather, clothes, school, toys, transportation, nature.

Usage:
    python scripts/seed_vocabulary.py
"""
import asyncio
import sys
import os

sys.path.append(os.getcwd())

from sqlalchemy import select, and_
from app.database import async_session_maker, engine, Base
from app.models.vocabulary import VocabularyCategory, VocabularyWord

# ── Word data per category (10 words each) ──────────────────────────

VOCABULARY_WORDS = {
    "colors": [
        {"word": "Red", "korean": "빨강", "emoji": "🔴"},
        {"word": "Blue", "korean": "파랑", "emoji": "🔵"},
        {"word": "Green", "korean": "초록", "emoji": "🟢"},
        {"word": "Yellow", "korean": "노랑", "emoji": "🟡"},
        {"word": "Orange", "korean": "주황", "emoji": "🟠"},
        {"word": "Purple", "korean": "보라", "emoji": "🟣"},
        {"word": "Pink", "korean": "분홍", "emoji": "🩷"},
        {"word": "Brown", "korean": "갈색", "emoji": "🟤"},
        {"word": "Black", "korean": "검정", "emoji": "⚫"},
        {"word": "White", "korean": "하양", "emoji": "⚪"},
    ],
    "numbers": [
        {"word": "One", "korean": "하나", "emoji": "1️⃣"},
        {"word": "Two", "korean": "둘", "emoji": "2️⃣"},
        {"word": "Three", "korean": "셋", "emoji": "3️⃣"},
        {"word": "Four", "korean": "넷", "emoji": "4️⃣"},
        {"word": "Five", "korean": "다섯", "emoji": "5️⃣"},
        {"word": "Six", "korean": "여섯", "emoji": "6️⃣"},
        {"word": "Seven", "korean": "일곱", "emoji": "7️⃣"},
        {"word": "Eight", "korean": "여덟", "emoji": "8️⃣"},
        {"word": "Nine", "korean": "아홉", "emoji": "9️⃣"},
        {"word": "Ten", "korean": "열", "emoji": "🔟"},
    ],
    "family": [
        {"word": "Mom", "korean": "엄마", "emoji": "👩"},
        {"word": "Dad", "korean": "아빠", "emoji": "👨"},
        {"word": "Sister", "korean": "언니·누나", "emoji": "👧"},
        {"word": "Brother", "korean": "형·오빠", "emoji": "👦"},
        {"word": "Baby", "korean": "아기", "emoji": "👶"},
        {"word": "Grandma", "korean": "할머니", "emoji": "👵"},
        {"word": "Grandpa", "korean": "할아버지", "emoji": "👴"},
        {"word": "Aunt", "korean": "이모·고모", "emoji": "👩\u200d🦰"},
        {"word": "Uncle", "korean": "삼촌", "emoji": "👨\u200d🦱"},
        {"word": "Friend", "korean": "친구", "emoji": "🧒"},
    ],
    "body": [
        {"word": "Head", "korean": "머리", "emoji": "🗣️"},
        {"word": "Eye", "korean": "눈", "emoji": "👁️"},
        {"word": "Nose", "korean": "코", "emoji": "👃"},
        {"word": "Mouth", "korean": "입", "emoji": "👄"},
        {"word": "Ear", "korean": "귀", "emoji": "👂"},
        {"word": "Hand", "korean": "손", "emoji": "🤚"},
        {"word": "Foot", "korean": "발", "emoji": "🦶"},
        {"word": "Arm", "korean": "팔", "emoji": "💪"},
        {"word": "Leg", "korean": "다리", "emoji": "🦵"},
        {"word": "Finger", "korean": "손가락", "emoji": "☝️"},
    ],
    "weather": [
        {"word": "Sunny", "korean": "맑음", "emoji": "☀️"},
        {"word": "Rainy", "korean": "비", "emoji": "🌧️"},
        {"word": "Cloudy", "korean": "흐림", "emoji": "☁️"},
        {"word": "Snowy", "korean": "눈", "emoji": "❄️"},
        {"word": "Windy", "korean": "바람", "emoji": "💨"},
        {"word": "Hot", "korean": "더움", "emoji": "🌡️"},
        {"word": "Cold", "korean": "추움", "emoji": "🥶"},
        {"word": "Rainbow", "korean": "무지개", "emoji": "🌈"},
        {"word": "Storm", "korean": "폭풍", "emoji": "⛈️"},
        {"word": "Foggy", "korean": "안개", "emoji": "🌫️"},
    ],
    "clothes": [
        {"word": "Shirt", "korean": "셔츠", "emoji": "👕"},
        {"word": "Pants", "korean": "바지", "emoji": "👖"},
        {"word": "Dress", "korean": "원피스", "emoji": "👗"},
        {"word": "Shoes", "korean": "신발", "emoji": "👟"},
        {"word": "Hat", "korean": "모자", "emoji": "🧢"},
        {"word": "Socks", "korean": "양말", "emoji": "🧦"},
        {"word": "Jacket", "korean": "재킷", "emoji": "🧥"},
        {"word": "Scarf", "korean": "목도리", "emoji": "🧣"},
        {"word": "Gloves", "korean": "장갑", "emoji": "🧤"},
        {"word": "Bag", "korean": "가방", "emoji": "🎒"},
    ],
    "school": [
        {"word": "Book", "korean": "책", "emoji": "📚"},
        {"word": "Pencil", "korean": "연필", "emoji": "✏️"},
        {"word": "Eraser", "korean": "지우개", "emoji": "🗑️"},
        {"word": "Desk", "korean": "책상", "emoji": "🪑"},
        {"word": "Teacher", "korean": "선생님", "emoji": "👩\u200d🏫"},
        {"word": "Backpack", "korean": "가방", "emoji": "🎒"},
        {"word": "Crayon", "korean": "크레파스", "emoji": "🖍️"},
        {"word": "Paper", "korean": "종이", "emoji": "📝"},
        {"word": "Clock", "korean": "시계", "emoji": "🕐"},
        {"word": "Ruler", "korean": "자", "emoji": "📏"},
    ],
    "toys": [
        {"word": "Ball", "korean": "공", "emoji": "⚽"},
        {"word": "Doll", "korean": "인형", "emoji": "🧸"},
        {"word": "Car", "korean": "자동차", "emoji": "🚗"},
        {"word": "Blocks", "korean": "블록", "emoji": "🧱"},
        {"word": "Robot", "korean": "로봇", "emoji": "🤖"},
        {"word": "Puzzle", "korean": "퍼즐", "emoji": "🧩"},
        {"word": "Kite", "korean": "연", "emoji": "🪁"},
        {"word": "Drum", "korean": "드럼", "emoji": "🥁"},
        {"word": "Teddy", "korean": "곰인형", "emoji": "🧸"},
        {"word": "Train", "korean": "기차", "emoji": "🚂"},
    ],
    "transportation": [
        {"word": "Car", "korean": "자동차", "emoji": "🚗"},
        {"word": "Bus", "korean": "버스", "emoji": "🚌"},
        {"word": "Train", "korean": "기차", "emoji": "🚆"},
        {"word": "Airplane", "korean": "비행기", "emoji": "✈️"},
        {"word": "Bicycle", "korean": "자전거", "emoji": "🚲"},
        {"word": "Ship", "korean": "배", "emoji": "🚢"},
        {"word": "Taxi", "korean": "택시", "emoji": "🚕"},
        {"word": "Subway", "korean": "지하철", "emoji": "🚇"},
        {"word": "Helicopter", "korean": "헬리콥터", "emoji": "🚁"},
        {"word": "Truck", "korean": "트럭", "emoji": "🚚"},
    ],
    "nature": [
        {"word": "Tree", "korean": "나무", "emoji": "🌳"},
        {"word": "Flower", "korean": "꽃", "emoji": "🌸"},
        {"word": "River", "korean": "강", "emoji": "🏞️"},
        {"word": "Mountain", "korean": "산", "emoji": "⛰️"},
        {"word": "Sun", "korean": "해", "emoji": "☀️"},
        {"word": "Moon", "korean": "달", "emoji": "🌙"},
        {"word": "Star", "korean": "별", "emoji": "⭐"},
        {"word": "Cloud", "korean": "구름", "emoji": "☁️"},
        {"word": "Rain", "korean": "비", "emoji": "🌧️"},
        {"word": "Ocean", "korean": "바다", "emoji": "🌊"},
    ],
}


async def seed_vocabulary():
    """Seed vocabulary words for categories that are currently empty."""
    total_created = 0
    total_skipped = 0

    async with async_session_maker() as session:
        for category_id, words in VOCABULARY_WORDS.items():
            # Verify category exists
            stmt = select(VocabularyCategory).where(VocabularyCategory.id == category_id)
            result = await session.execute(stmt)
            category = result.scalar_one_or_none()

            if not category:
                print(f"  [SKIP] Category '{category_id}' not found in DB. Run app/seed.py first.")
                continue

            print(f"  [{category_id}] Seeding words...")

            for i, w_data in enumerate(words):
                # Upsert: skip if word already exists in this category
                stmt = select(VocabularyWord).where(
                    and_(
                        VocabularyWord.category_id == category_id,
                        VocabularyWord.word == w_data["word"],
                    )
                )
                result = await session.execute(stmt)
                existing = result.scalar_one_or_none()

                if existing:
                    total_skipped += 1
                    continue

                word = VocabularyWord(
                    category_id=category_id,
                    word=w_data["word"],
                    korean=w_data["korean"],
                    emoji=w_data["emoji"],
                    sort_order=i + 1,
                )
                session.add(word)
                total_created += 1

        await session.commit()

    print(f"\nVocabulary seed complete! Created: {total_created}, Skipped (already exist): {total_skipped}")


if __name__ == "__main__":
    asyncio.run(seed_vocabulary())
