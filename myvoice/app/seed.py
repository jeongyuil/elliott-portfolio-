import asyncio
import uuid
from datetime import datetime
from sqlalchemy import select
from app.database import async_session_maker, engine, Base
from app.models import VocabularyCategory, VocabularyWord, ShopItem, CurriculumUnit, Activity
from app.models.family import FamilyAccount, Child
from app.core.security import hash_password

# Data from frontend/src/lib/mockData.ts

VOCABULARY_CATEGORIES = [
    {"id": "food", "name": "음식", "emoji": "🍎", "total_words": 10},
    {"id": "animals", "name": "동물", "emoji": "🐶", "total_words": 10},
    {"id": "colors", "name": "색깔", "emoji": "🎨", "total_words": 10},
    {"id": "numbers", "name": "숫자", "emoji": "🔢", "total_words": 10},
    {"id": "family", "name": "가족", "emoji": "👨‍👩‍👧‍👦", "total_words": 10},
    {"id": "body", "name": "신체", "emoji": "👁️", "total_words": 10},
    {"id": "weather", "name": "날씨", "emoji": "☀️", "total_words": 10},
    {"id": "clothes", "name": "옷", "emoji": "👕", "total_words": 10},
    {"id": "school", "name": "학교", "emoji": "🏫", "total_words": 10},
    {"id": "toys", "name": "장난감", "emoji": "🧸", "total_words": 10},
    {"id": "transportation", "name": "교통", "emoji": "🚗", "total_words": 10},
    {"id": "nature", "name": "자연", "emoji": "🌳", "total_words": 10},
]

# Sample words for each category
VOCABULARY_WORDS = {
    "food": [
        {"word": "Apple", "korean": "사과", "emoji": "🍎"},
        {"word": "Banana", "korean": "바나나", "emoji": "🍌"},
        {"word": "Grape", "korean": "포도", "emoji": "🍇"},
        {"word": "Bread", "korean": "빵", "emoji": "🍞"},
        {"word": "Milk", "korean": "우유", "emoji": "🥛"},
        {"word": "Water", "korean": "물", "emoji": "💧"},
        {"word": "Juice", "korean": "주스", "emoji": "🧃"},
        {"word": "Egg", "korean": "계란", "emoji": "🥚"},
        {"word": "Cheese", "korean": "치즈", "emoji": "🧀"},
        {"word": "Cookie", "korean": "쿠키", "emoji": "🍪"},
    ],
    "animals": [
        {"word": "Dog", "korean": "강아지", "emoji": "🐶"},
        {"word": "Cat", "korean": "고양이", "emoji": "🐱"},
        {"word": "Lion", "korean": "사자", "emoji": "🦁"},
        {"word": "Tiger", "korean": "호랑이", "emoji": "🐯"},
        {"word": "Bear", "korean": "곰", "emoji": "🐻"},
        {"word": "Rabbit", "korean": "토끼", "emoji": "🐰"},
        {"word": "Monkey", "korean": "원숭이", "emoji": "🐵"},
        {"word": "Pig", "korean": "돼지", "emoji": "🐷"},
        {"word": "Cow", "korean": "소", "emoji": "🐮"},
        {"word": "Horse", "korean": "말", "emoji": "🐴"},
    ],
}

SHOP_ITEMS = [
    # Character skins (price in stars)
    {"id": "skin_popo_pirate", "name": "해적 포포", "description": "바다를 누비는 해적 포포!", "emoji": "🏴‍☠️", "price": 200, "item_type": "skin"},
    {"id": "skin_popo_astronaut", "name": "우주인 포포", "description": "우주를 탐험하는 포포!", "emoji": "🧑‍🚀", "price": 300, "item_type": "skin"},
    {"id": "skin_luna_detective", "name": "탐정 루나", "description": "수수께끼를 푸는 루나!", "emoji": "🕵️‍♀️", "price": 200, "item_type": "skin"},
    {"id": "skin_luna_princess", "name": "공주 루나", "description": "반짝이는 왕관의 루나!", "emoji": "👑", "price": 300, "item_type": "skin"},
    {"id": "skin_popo_chef", "name": "요리사 포포", "description": "맛있는 요리를 하는 포포!", "emoji": "👨‍🍳", "price": 150, "item_type": "skin"},
    {"id": "skin_luna_artist", "name": "화가 루나", "description": "그림을 그리는 루나!", "emoji": "🎨", "price": 150, "item_type": "skin"},
]

ADVENTURES = [
    {
        "unit_id": "8ca51667-9725-4122-bb0d-ad50072508a0",
        "title": "동물원 친구들 만나기",
        "description": "사자, 호랑이, 곰... 동물원에는 어떤 친구들이 살고 있을까요?",
        "age_group": "4-5",
        "difficulty_level": "beginner",
        "order": 1,
        "keywords": ["animals", "zoo"],
        "cover_image_url": "zoo.png"
    },
    {
        "unit_id": "bdd7ec94-aafe-488a-bff3-56456f56d8aa",
        "title": "맛있는 과일 가게",
        "description": "사과, 바나나, 포도... 맛있는 과일을 영어로 주문해봐요!",
        "age_group": "4-5",
        "difficulty_level": "beginner",
        "order": 2,
        "keywords": ["fruits", "market"],
        "cover_image_url": "fruits.png"
    },
    {
        "unit_id": "e5b9c139-c04c-427a-bb10-dffed131c6da",
        "title": "우리 가족 소개하기",
        "description": "엄마, 아빠, 동생... 우리 가족을 영어로 소개해볼까요?",
        "age_group": "5-6",
        "difficulty_level": "beginner",
        "order": 3,
        "keywords": ["family"],
        "cover_image_url": "family.png"
    },
]

# Activities for "Meeting Zoo Friends" (Week 1)
ACTIVITIES = [
    {
        "activity_id": "W1-A1-mission-call",
        "curriculum_unit_id": "8ca51667-9725-4122-bb0d-ad50072508a0",
        "name": "루나의 미션 콜",
        "activity_type": "mission_call",
        "instructions_for_ai": """너는 '루나'라는 이름의 친근한 AI 캐릭터야.
동물원에 갔는데 동물 친구들이 영어 이름을 까먹었어!
아이에게 도움을 요청해. 
첫 번째로 강아지(dog)를 소개해줘.
한국어 70%, 영어 30%로 말해.""",
        "intro_narrator_script": "어느 날, 루나에게서 긴급 전화가 왔어요! 동물원 친구들이 영어 이름을 까먹었대요. 우리가 도와줄까요?",
        "transition_trigger": "child_response",
        "estimated_duration_minutes": 2,
    },
    {
        "activity_id": "W1-A2-guided-conversation",
        "curriculum_unit_id": "8ca51667-9725-4122-bb0d-ad50072508a0",
        "name": "동물 친구 소개하기",
        "activity_type": "guided_conversation",
        "instructions_for_ai": """아이와 함께 동물원의 동물들을 하나씩 소개하는 대화를 해.
대상 단어: dog, cat, lion, bear, rabbit
각 동물에 대해:
1. 한국어로 "이 친구는 누구지?" 질문
2. 아이가 영어로 대답하도록 유도
3. 맞으면 칭찬, 틀리면 힌트 제공
4. 다음 동물로 자연스럽게 이동
한국어 50%, 영어 50%로 말해.""",
        "intro_narrator_script": None,
        "transition_trigger": "auto",
        "estimated_duration_minutes": 5,
    },
    {
        "activity_id": "W1-A3-pronunciation-drill",
        "curriculum_unit_id": "8ca51667-9725-4122-bb0d-ad50072508a0",
        "name": "발음 연습",
        "activity_type": "pronunciation_drill",
        "instructions_for_ai": """아이의 영어 발음을 연습시켜줘.
단어: dog, cat, lion
각 단어를 또박또박 말해보도록 유도하고,
잘 따라하면 "Perfect! 👏" 칭찬해줘.
간단한 문장도 시도: "I see a dog!" """,
        "intro_narrator_script": "이제 동물 이름을 또박또박 말해볼까요?",
        "transition_trigger": "auto",
        "estimated_duration_minutes": 3,
    },
]

async def seed_data():
    # Ensure tables exist
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        print("Seeding Vocabulary Categories...")
        for cat_data in VOCABULARY_CATEGORIES:
            stmt = select(VocabularyCategory).where(VocabularyCategory.id == cat_data["id"])
            result = await session.execute(stmt)
            if not result.scalar_one_or_none():
                cat = VocabularyCategory(**cat_data)
                session.add(cat)
                
                # Add words if available
                words = VOCABULARY_WORDS.get(cat_data["id"], [])
                for i, w_data in enumerate(words):
                    word = VocabularyWord(
                        category_id=cat_data["id"],
                        sort_order=i+1,
                        **w_data
                    )
                    session.add(word)
        
        print("Seeding Shop Items...")
        for item_data in SHOP_ITEMS:
            stmt = select(ShopItem).where(ShopItem.id == item_data["id"])
            result = await session.execute(stmt)
            if not result.scalar_one_or_none():
                item = ShopItem(**item_data)
                session.add(item)

        print("Seeding Adventures (CurriculumUnits)...")
        for adv_data in ADVENTURES:
            stmt = select(CurriculumUnit).where(CurriculumUnit.title == adv_data["title"])
            result = await session.execute(stmt)
            if not result.scalar_one_or_none():
                # Map difficulty string to int
                diff_map = {"beginner": 1, "intermediate": 2, "advanced": 3}
                difficulty = diff_map.get(adv_data["difficulty_level"], 1)
                
                # Parse age group
                age_min, age_max = 4, 12
                if "-" in adv_data["age_group"]:
                    parts = adv_data["age_group"].split("-")
                    age_min = int(parts[0])
                    age_max = int(parts[1])

                unit = CurriculumUnit(
                    curriculum_unit_id=str(adv_data["unit_id"]),
                    title=adv_data["title"],
                    description=adv_data["description"],
                    phase=1,
                    week=adv_data["order"],
                    age_min=age_min,
                    age_max=age_max,
                    difficulty_level=difficulty,
                    # Defaults
                    language_mode="mixed",
                    clumsiness_level=80,
                    korean_ratio=50
                )
                session.add(unit)

        print("Seeding Activities...")
        for act_data in ACTIVITIES:
            stmt = select(Activity).where(Activity.activity_id == act_data["activity_id"])
            result = await session.execute(stmt)
            if not result.scalar_one_or_none():
                activity = Activity(**act_data)
                session.add(activity)

        print("Seeding Family & Child...")
        stmt = select(FamilyAccount).where(FamilyAccount.contact_email == "test@test.com")
        result = await session.execute(stmt)
        family = result.scalar_one_or_none()
        
        if not family:
            family = FamilyAccount(
                parent_name="테스트부모",
                contact_email="test@test.com",
                hashed_password=hash_password("password"),
                email_verified=True # Allow immediate login
            )
            session.add(family)
            await session.flush() # Get ID
            
            child = Child(
                family_id=family.family_id,
                name="지수",
                gender="female",
                birth_date=datetime(2018, 1, 1),
                avatar_id="girl_1", 
                preferences_topics={"shyness": 2, "energy": 5} # Using preferences_topics as catch-all for now
            )
            session.add(child)
        else:
            # check verification
            if not family.email_verified:
                family.email_verified = True
            
            # check child
            stmt = select(Child).where(Child.family_id == family.family_id)
            result = await session.execute(stmt)
            if not result.scalar_one_or_none():
                 child = Child(
                    family_id=family.family_id,
                    name="지수",
                    gender="female",
                    birth_date=datetime(2018, 1, 1),
                    avatar_id="girl_1",
                    preferences_topics={"shyness": 2, "energy": 5}
                )
                 session.add(child)

        await session.commit()
        print("Seed complete!")

if __name__ == "__main__":
    asyncio.run(seed_data())
