"""
FDD-based Skill Dictionary Seed — W1-W4 (밤토리 Phase 1)

Based on:
  - Skill_Dictionary_v0.1.md (16 base skills)
  - W1-W4 Task_Activity_Skill_Mapping files (additional skills per week)
"""
import asyncio
import sys
import os

sys.path.append(os.getcwd())

from sqlalchemy import select
from app.database import async_session_maker, engine, Base
from app.models.skill import Skill

# --------------------------------------------------------------------------
# Skill Dictionary — All skills referenced across W1-W4
# --------------------------------------------------------------------------

SKILLS = [
    # ===== Language — Vocabulary =====
    {
        "skill_id": "SK_VOCAB_DAILY_GREET",
        "name": "인사 표현 (Hello, Hi, Bye)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["Hello!", "Hi!", "Bye!", "Nice to meet you!"],
    },
    {
        "skill_id": "SK_VOCAB_DAILY_FOOD",
        "name": "일상 음식 단어",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["apple", "banana", "milk", "bread"],
    },
    {
        "skill_id": "SK_VOCAB_DAILY_ROOM",
        "name": "방/집 관련 단어",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["bed", "desk", "book", "toy", "door", "window"],
    },
    {
        "skill_id": "SK_VOCAB_DAILY_ROUTINE",
        "name": "일과 관련 단어",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["wake up", "eat", "sleep", "play", "school"],
    },
    {
        "skill_id": "SK_VOCAB_ROOM_OBJECT",
        "name": "방 안 물건 단어 (W2)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["bed", "desk", "chair", "lamp", "shelf", "box"],
    },
    {
        "skill_id": "SK_VOCAB_PREPOSITION_BASIC",
        "name": "기본 전치사 (in/on/under)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["in the box", "on the desk", "under the bed"],
    },
    {
        "skill_id": "SK_VOCAB_ACTION_BASIC",
        "name": "기본 동작 동사",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["look", "find", "go", "come", "open"],
    },
    {
        "skill_id": "SK_VOCAB_EMOTION_BASIC",
        "name": "감정 단어 (happy/sad/angry 등)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["happy", "sad", "angry", "scared", "tired"],
    },
    {
        "skill_id": "SK_VOCAB_SOCIAL_TRAIT",
        "name": "친구 특성 단어 (funny/help/play 등)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["funny", "help", "play", "quiet", "friend"],
    },
    {
        "skill_id": "SK_VOCAB_CLOTHES_BASIC",
        "name": "옷 관련 단어 (shirt/dress/hat 등)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["shirt", "dress", "pants", "skirt", "shoes", "hat", "coat"],
    },
    {
        "skill_id": "SK_VOCAB_COLOR_BASIC",
        "name": "기본 색깔 단어",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["red", "blue", "yellow", "green", "pink", "black", "white"],
    },
    {
        "skill_id": "SK_VOCAB_ACTION_VERB_CLOTHES",
        "name": "옷 입기/벗기 동사 (put on/take off)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["put on your coat", "take off your shoes"],
    },
    {
        "skill_id": "SK_VOCAB_PLAY_BASIC",
        "name": "놀이 관련 단어",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["play", "game", "draw", "hide and seek"],
    },
    {
        "skill_id": "SK_VOCAB_PLACE_BASIC",
        "name": "기본 장소 단어",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["school", "home", "outside", "room"],
    },
    {
        "skill_id": "SK_VOCAB_SOCIAL_RULE",
        "name": "사회 규칙 단어 (share/turn/stop)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["share", "turn", "stop", "please"],
    },

    # ===== Language — Sentence =====
    {
        "skill_id": "SK_SENTENCE_BASIC",
        "name": "기본 문장 구성 (SVO)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["I like apple.", "This is my bed.", "I am seven."],
    },
    {
        "skill_id": "SK_SYNTAX_NEGATION",
        "name": "부정문 구성 (don't like)",
        "category": "language",
        "mode": "expressive",
        "age_band": "6-8",
        "can_do_examples": ["I don't like the black hat."],
    },

    # ===== Language — Pronunciation =====
    {
        "skill_id": "SK_PRONUN_BASIC",
        "name": "기본 발음 (단어 수준)",
        "category": "language",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["apple", "dog", "happy", "shirt"],
    },

    # ===== Language — Discourse =====
    {
        "skill_id": "SK_DISCOURSE_MINI_SEQUENCE",
        "name": "2~3문장 연속 발화",
        "category": "language",
        "mode": "expressive",
        "age_band": "6-8",
        "can_do_examples": ["My name is ___. I am seven. I like my blue hoodie."],
    },

    # ===== Cognitive =====
    {
        "skill_id": "SK_COMPREHENSION_BASIC",
        "name": "기본 이해력 (지시/질문 이해)",
        "category": "cognitive",
        "mode": "receptive",
        "age_band": "5-8",
        "can_do_examples": ["질문을 이해하고 적절히 반응", "지시를 따름"],
    },
    {
        "skill_id": "SK_COMPREHENSION_SITUATION",
        "name": "상황 이해 (상황-감정 매칭)",
        "category": "cognitive",
        "mode": "receptive",
        "age_band": "5-8",
        "can_do_examples": ["선물 받으면 happy", "비 오면 sad"],
    },

    # ===== Pragmatics (Social/Communication) =====
    {
        "skill_id": "SK_PRAG_SELF_INTRO",
        "name": "자기소개 화용 (이름/나이 말하기)",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["My name is ___.", "I am seven."],
    },
    {
        "skill_id": "SK_PRAG_PREFERENCE",
        "name": "선호 표현 (I like / I don't like)",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["I like apple.", "I like the red shirt."],
    },
    {
        "skill_id": "SK_PRAG_GAME_RULE",
        "name": "게임 규칙 이해 & 참여",
        "category": "social",
        "mode": "receptive",
        "age_band": "5-8",
        "can_do_examples": ["숨바꼭질 규칙 이해", "차례 게임 참여"],
    },
    {
        "skill_id": "SK_PRAG_SOCIAL_TALK",
        "name": "사회적 대화 참여",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["친구 이야기하기", "주변 사람 묘사"],
    },
    {
        "skill_id": "SK_PRAG_SOCIAL_PLAY",
        "name": "놀이 맥락 대화",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["I play with my friend."],
    },
    {
        "skill_id": "SK_PRAG_EMOTION_EXP",
        "name": "감정 표현 화용",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["I am happy.", "I feel sad."],
    },
    {
        "skill_id": "SK_PRAG_TURN_TAKING",
        "name": "순서 지키기 표현",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["It's my turn.", "Your turn."],
    },
    {
        "skill_id": "SK_PRAG_SHARING",
        "name": "공유하기 제안",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["Let's share."],
    },
    {
        "skill_id": "SK_PRAG_POLITE_REQUEST",
        "name": "정중한 요청 (please)",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["My turn, please.", "Can I play, please?"],
    },
    {
        "skill_id": "SK_PRAG_SET_BOUNDARY",
        "name": "경계 설정 (Stop)",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["Stop, please."],
    },
    {
        "skill_id": "SK_PRAG_CONTEXT_APPROPRIATE",
        "name": "상황에 맞는 행동/말하기",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["추우면 coat 입기", "집에서 shoes 벗기"],
    },
    {
        "skill_id": "SK_PRAG_CONFIRMATION",
        "name": "확인/동의 표현",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["Yes!", "맞아", "No"],
    },
    {
        "skill_id": "SK_PRAG_DESCRIPTION_BASIC",
        "name": "기본 묘사 화용",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["This is my dress.", "I like my blue hoodie."],
    },
    {
        "skill_id": "SK_PRAG_CORRECTION",
        "name": "실수 교정 (No, put on...)",
        "category": "social",
        "mode": "expressive",
        "age_band": "6-8",
        "can_do_examples": ["No, put on your coat."],
    },
    {
        "skill_id": "SK_PRAG_SOCIAL_RITUAL",
        "name": "사회적 의식/인사 참여",
        "category": "social",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["Earth crew, ready!", "Earth crew, mission complete!"],
    },

    # ===== Emotional =====
    {
        "skill_id": "SK_AFFECT_CONFIDENCE",
        "name": "자신감/참여 의지",
        "category": "emotional",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["미션 수락", "자발적 발화", "도전 시도"],
    },
    {
        "skill_id": "SK_EXPRESSIVE_NEGATIVE_EMOTION",
        "name": "부정적 감정의 적절한 언어적 표현",
        "category": "emotional",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["I feel sad.", "I feel angry."],
    },
    {
        "skill_id": "SK_EXPRESSIVE_POSITIVE_EMOTION",
        "name": "긍정적 감정 표현",
        "category": "emotional",
        "mode": "expressive",
        "age_band": "5-8",
        "can_do_examples": ["I feel happy.", "I feel better.", "I feel okay."],
    },
]


async def seed_skills():
    """Seed W1-W4 skill dictionary from FDD specs."""
    print(f"Seeding {len(SKILLS)} skills...")

    async with async_session_maker() as session:
        for skill_data in SKILLS:
            skill_id = skill_data["skill_id"]
            stmt = select(Skill).where(Skill.skill_id == skill_id)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                for key, value in skill_data.items():
                    if key != "skill_id" and hasattr(existing, key):
                        setattr(existing, key, value)
                print(f"  Updated: {skill_data['name']}")
            else:
                skill = Skill(**skill_data)
                session.add(skill)
                print(f"  Created: {skill_data['name']}")

        await session.commit()
        print(f"\nSkill seed complete! ({len(SKILLS)} skills)")


if __name__ == "__main__":
    asyncio.run(seed_skills())
