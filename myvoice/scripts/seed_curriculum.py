"""
FDD-based Curriculum Seed — W1-W4 (밤토리 Phase 1)

Based on:
  - W1_Week1_Spec_v0.1.md (Earth Crew - Self Introduction)
  - W2_Week2_Spec_v0.1.md (Lost Parts - Room & Prepositions)
  - W3_Week3_Spec_v0.1.md (Feelings & Friends)
  - W4_Week4_Spec_v0.1.md (Going Outside in Disguise)
  - W1-W4 Task_Activity_Skill_Mapping files
"""
import asyncio
import sys
import os

sys.path.append(os.getcwd())
# Also add scripts/ to path so validators can be imported
sys.path.append(os.path.join(os.getcwd(), "scripts"))

from sqlalchemy import select
from app.database import async_session_maker, engine, Base
from app.models.curriculum import CurriculumUnit, Activity
from validators.speech_elicitation import print_validation_report

# --------------------------------------------------------------------------
# Curriculum Units (W1-W4, 4 sessions each = 16 sessions)
# --------------------------------------------------------------------------

CURRICULUM_UNITS = [
    # Week 1: Earth Crew — 자기소개
    {
        "curriculum_unit_id": "W1_S1_meet_luna_popo",
        "title": "루나와 포포 만나기",
        "description": "처음 만난 루나에게 이름과 나이를 영어로 소개해봐요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 70,
        "target_skills": ["SK_VOCAB_DAILY_GREET", "SK_SENTENCE_BASIC", "SK_PRAG_SELF_INTRO"],
    },
    {
        "curriculum_unit_id": "W1_S2_likes_dislikes",
        "title": "좋아하는 것과 싫어하는 것",
        "description": "루나에게 좋아하는 음식, 동물, 색깔을 가르쳐줘요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 65,
        "target_skills": ["SK_VOCAB_DAILY_FOOD", "SK_SENTENCE_BASIC", "SK_PRAG_PREFERENCE"],
    },
    {
        "curriculum_unit_id": "W1_S3_my_room_home",
        "title": "내 방과 우리 집",
        "description": "내 방에 뭐가 있는지 루나에게 보여줘요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_DAILY_ROOM", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "W1_S4_my_day_routine",
        "title": "나의 하루",
        "description": "아침부터 저녁까지, 루나에게 지구인의 하루를 알려줘요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_DAILY_ROUTINE", "SK_SENTENCE_BASIC"],
    },

    # Week 2: Lost Parts — 방 탐험 & 전치사
    {
        "curriculum_unit_id": "W2_S1_room_objects",
        "title": "방 안의 물건들",
        "description": "루나의 잃어버린 부품을 찾으며 방 안 물건 이름을 배워요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "W2_S2_prepositions",
        "title": "어디에 있을까?",
        "description": "in, on, under를 사용해서 부품이 어디 있는지 말해봐요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 55,
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "W2_S3_hide_and_seek",
        "title": "숨바꼭질 게임",
        "description": "루나와 숨바꼭질하며 전치사를 연습해요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 50,
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_PRAG_GAME_RULE", "SK_VOCAB_ACTION_BASIC"],
    },
    {
        "curriculum_unit_id": "W2_S4_room_check_report",
        "title": "방 점검 보고서",
        "description": "W2에서 배운 것을 종합해서 루나에게 보고해요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 50,
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
    },

    # Week 3: Feelings & Friends
    {
        "curriculum_unit_id": "W3_S1_basic_feelings",
        "title": "기본 감정 단어",
        "description": "happy, sad, angry, scared, tired — 루나에게 감정을 가르쳐줘요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 65,
        "target_skills": ["SK_VOCAB_EMOTION_BASIC", "SK_SENTENCE_BASIC", "SK_PRAG_EMOTION_EXP"],
    },
    {
        "curriculum_unit_id": "W3_S2_friends_people",
        "title": "내 친구와 주변 사람들",
        "description": "친구가 뭔지, 어떤 사람인지 루나에게 알려줘요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_SOCIAL_TRAIT", "SK_PRAG_SOCIAL_TALK", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "W3_S3_sharing_turn_taking",
        "title": "나누기와 순서 지키기",
        "description": "share, turn — 지구의 사회 규칙을 루나에게 가르쳐줘요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_PRAG_TURN_TAKING", "SK_PRAG_SHARING", "SK_PRAG_POLITE_REQUEST"],
    },
    {
        "curriculum_unit_id": "W3_S4_small_problems_feelings",
        "title": "작은 문제와 감정 말하기",
        "description": "속상할 때 'I feel sad', 싫을 때 'Stop, please' 말하는 법을 배워요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_EXPRESSIVE_NEGATIVE_EMOTION", "SK_PRAG_SET_BOUNDARY", "SK_SENTENCE_BASIC"],
    },

    # Week 4: Going Outside in Disguise
    {
        "curriculum_unit_id": "W4_S1_luna_clothes_colors",
        "title": "루나에게 옷 입혀주기",
        "description": "shirt, dress, pants — 색깔과 옷 이름을 배우며 루나를 꾸며줘요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "W4_S2_put_on_take_off",
        "title": "입기와 벗기",
        "description": "put on, take off — 날씨에 맞게 옷 입는 법을 가르쳐줘요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_VOCAB_ACTION_VERB_CLOTHES", "SK_VOCAB_CLOTHES_BASIC", "SK_PRAG_CONTEXT_APPROPRIATE"],
    },
    {
        "curriculum_unit_id": "W4_S3_my_clothes_style",
        "title": "내 옷과 스타일",
        "description": "내가 좋아하는 옷을 루나에게 소개해요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_PRAG_DESCRIPTION_BASIC"],
    },
    {
        "curriculum_unit_id": "W4_S4_final_disguise_badge",
        "title": "최종 변장 미션 & 배지 수여",
        "description": "W1-W4 총정리! 자기소개 + 옷 소개를 하고 Earth Crew Lv.1 배지를 받아요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 50,
        "target_skills": ["SK_PRAG_SELF_INTRO", "SK_VOCAB_CLOTHES_BASIC", "SK_DISCOURSE_MINI_SEQUENCE"],
    },
]

# --------------------------------------------------------------------------
# Activities (FDD Task-Activity-Skill Mapping 기반)
# --------------------------------------------------------------------------

ACTIVITIES = [
    # ===== W1_S1: Meet Luna & Popo =====
    {
        "activity_id": "ACT_W1_S1_mission_start",
        "curriculum_unit_id": "W1_S1_meet_luna_popo",
        "name": "미션 콜: Earth Crew 결성",
        "activity_type": "mission_call",
        "target_skills": ["SK_COMPREHENSION_BASIC", "SK_AFFECT_CONFIDENCE"],
        "instructions_for_ai": """오늘은 아이와 루나, 포포의 첫 만남입니다.

첫 턴(turn_count=0)에서 포포가 해야 할 것:
1. 루나를 소개하며 미션 설명
2. 구체적인 문장 틀을 제시: "'My name is ___'에서 빈칸에 캡틴 이름을 넣어서 말해봐!"
3. 예시를 먼저 보여주기: "포포가 먼저 해볼게~ 'My name is Popo!' 이렇게! 캡틴도 해볼까?"

중요:
- 절대 추상적인 질문만 하지 마세요 ("저 큰 것들이 뭐야?", "영어로 말해볼래?")
- 항상 정답 예시나 문장 틀을 함께 제시하세요
- 아이가 이름만 말해도 성공으로 처리합니다
- 포포가 풀 문장으로 리폼해줍니다: "잘했어! 'My name is [아이 이름]!'"
- 루나가 감탄: "Wow! Nice to meet you, Captain!"

아이가 아직 말을 안 하면:
- 선택지 제공: "이름을 말해볼까? 아니면 포포가 먼저 해볼까?"
- 따라하기 유도: "'Hello!'부터 해볼까? 포포 따라해봐~ 'Hello!'" """,
        "key_expression": "My name is ___.",
        "story_content": "지구에 처음 온 루나를 만나는 이야기. 캡틴(아이)이 루나의 지구 적응을 도와주는 미션이 시작됩니다.",
        "intro_narrator_script": """[나레이션] 어느 고요한 밤, 하늘에서 작은 별이 하나 반짝였어요. 그 별은 점점 가까이 다가오더니... 슈우웅! 하고 마당 한가운데에 내려앉았어요. 하얀 빛이 사라지자, 그 안에서 조그만 친구 하나가 비틀비틀 걸어 나왔어요.
[루나] H-hello? Is anyone here? I am Luna... from space.
[나레이션] 루나는 먼 우주에서 온 탐험가인데, 지구에 대해 아무것도 몰라요. 그때, 어둠 속에서 멋진 비밀 요원이 나타났어요!
[포포] 루나! 여기야! 난 포포, 지구에서 활동하는 비밀 요원이야. 걱정 마, 여기엔 아주 멋진 캡틴이 있거든.
[루나] Captain? What is a captain?
[포포] 캡틴은 우리 팀의 리더야! 루나에게 지구의 모든 걸 알려줄 수 있는 아주 특별한 사람이지. 그 캡틴이 바로... {child_name}이야!
[루나] (눈을 반짝이며) Captain {child_name}! Hello! Can you say 'hello' to me? Please?
[포포] 캡틴, 루나에게 인사해줘! 포포가 먼저 해볼게~ 'Hello, Luna!' 이렇게!
[포포] 캡틴도 해볼래? 'Hello, Luna!' 아니면 'Hi, Luna!' 둘 중에 하나 말해봐!""",
        "estimated_duration_minutes": 5,
    },
    {
        "activity_id": "ACT_W1_S1_self_intro",
        "curriculum_unit_id": "W1_S1_meet_luna_popo",
        "name": "자기소개하기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_GREET", "SK_SENTENCE_BASIC", "SK_PRAG_SELF_INTRO"],
        "instructions_for_ai": """아이가 루나에게 자기소개를 합니다.

순서:
1. 이름: "My name is ___." (포포가 한국어로 유도)
2. 나이: "I am seven." (포포: "몇 살인지도 알려줄래?")
3. 인사: "Nice to meet you!" (루나가 따라하며 감동)

각 단계에서:
- 아이가 한국어로 말해도 포포가 영어로 연결
- 단어만 말해도 성공 (예: "seven" → 포포: "맞아, I am seven!")
- 루나가 매번 감탄: "Wow!" "So cool!" "Captain is seven!"

핵심: 아이가 '선생님' 느낌을 받도록. 루나에게 가르쳐주는 구조.""",
        "key_expression": "My name is ___. I am ___.",
        "intro_narrator_script": """[나레이션] 루나가 빛나는 눈으로 두리번두리번 주위를 살피고 있어요. 풀잎을 만져보더니 깜짝 놀라요. 바람이 살랑 불자 머리카락이 날리는 게 신기한가 봐요.
[루나] Oh! The air... it moves! And the sky... it's so blue! In space, everything is dark.
[나레이션] 루나가 하늘을 올려다보며 입을 동그랗게 벌렸어요. 우주에서는 한 번도 파란 하늘을 본 적이 없었거든요. 그때 포포가 루나의 손을 살짝 잡고 캡틴 앞으로 데려왔어요.
[포포] 자, 루나! 이 분이 바로 우리 캡틴이야. {child_name} 캡틴! 지구에서 제일 멋진 친구라고!
[루나] (긴장한 목소리로) H-hello... Captain? I am Luna. I am... a little scared.
[나레이션] 루나의 손이 살짝 떨리고 있어요. 낯선 별에서 처음 만나는 친구니까 긴장되는 거예요.
[루나] (작은 목소리로) Captain... can you tell me your name? Please? I want to know who you are.
[포포] 캡틴, 루나가 이름이 궁금하대! 지구에서는 이름을 알려주면서 인사하거든. 'My name is' 다음에 이름을 말하는 거야!
[포포] 포포가 먼저 해볼게. 'My name is Popo!' 이렇게!
[포포] 캡틴도 해볼래? 'My name is...' 다음에 캡틴 이름을 말해봐! 'My name is {child_name}' 아니면 그냥 이름만 말해도 좋아!""",
        "outro_narrator_script": """[포포] 캡틴, 잠깐... 포포 레이더에 이상한 신호가 잡혔어. 누군가 루나를 따라온 것 같은데... 다음에 확인해보자!""",
        "estimated_duration_minutes": 5,
    },

    # ===== W1_S2: Likes & Dislikes =====
    {
        "activity_id": "ACT_W1_S2_favorite_things",
        "curriculum_unit_id": "W1_S2_likes_dislikes",
        "name": "좋아하는 것 알려주기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_FOOD", "SK_SENTENCE_BASIC", "SK_PRAG_PREFERENCE"],
        "instructions_for_ai": """루나가 지구 음식/동물/색깔에 대해 모릅니다. 캡틴이 가르쳐줍니다.

포포: "루나가 지구 음식 이름을 알고 싶대. 캡틴이 좋아하는 음식이 뭐야?"
아이가 한국어로 답하면 → 포포가 영어 매핑
예: "사과" → "영어로는 apple이야!"
루나: "Apple! I like apple too!"

패턴: "I like ___."
아이가 따라하면 칭찬. 안 해도 괜찮음 — 포포가 대신.

3가지까지만 물어보고 마무리:
1. 좋아하는 음식
2. 좋아하는 동물
3. 좋아하는 색깔""",
        "key_expression": "I like ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 우리 루나에게 이름도 알려주고, 멋지게 인사했잖아! 오늘은 루나에게 좋아하는 것들을 알려줄 거야! 준비됐지? Earth crew, ready!
[나레이션] 오늘은 루나가 캡틴의 집 부엌 앞에 서 있어요. 루나가 살금살금 냉장고 문을 열었어요. 차가운 바람이 솔솔 불어오자 루나가 깜짝 놀라 뒤로 물러났어요!
[루나] Whoa! Cold wind from a box! Is this... space freezer?
[나레이션] 루나가 다시 용기를 내서 냉장고 안을 들여다봤어요. 빨간 동그란 것, 노란 긴 것, 초록색 네모난 것... 루나의 눈이 동그래졌어요.
[루나] What is this red round thing? And this yellow long thing? In space, I only eat energy capsules. These look... amazing!
[포포] 하하! 루나야, 그건 음식이야! 지구에는 맛있는 게 정말 많거든. 캡틴한테 물어보면 다 알려줄 거야!
[나레이션] 루나가 기대에 찬 눈으로 캡틴을 바라봐요. 루나의 가슴 화면에 반짝반짝 별이 떠올라요. 기대되고 설레는 마음이래요.
[포포] 캡틴, 오늘은 루나에게 좋아하는 것들을 알려줄 거야. 음식, 동물, 색깔! 영어로는 'I like' 다음에 좋아하는 걸 말하면 돼.
[포포] 포포가 먼저 해볼게~ 'I like apples!' 이렇게!
[포포] 캡틴은 뭘 좋아해? 'I like apples' 아니면 'I like pizza' 아니면 다른 것도 좋아! 'I like...' 다음에 말해봐!""",
        "outro_narrator_script": """[루나] Captain! Tomorrow I want to see your room! What is a "room"?
[포포] 내일은 캡틴의 방을 루나에게 보여줄 거야. 어떤 것들이 있는지 미리 생각해둬!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W1_S3: My Room & Home =====
    {
        "activity_id": "ACT_W1_S3_room_tour",
        "curriculum_unit_id": "W1_S3_my_room_home",
        "name": "내 방 구경시켜주기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_ROOM", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """루나가 캡틴의 방이 궁금합니다.

포포: "루나가 캡틴 방에 뭐가 있는지 궁금하대! 뭐가 있어?"
아이가 자유롭게 말하면 → 영어 단어 연결

예상 단어: bed, desk, book, toy, doll, robot
패턴: "This is my ___."

루나가 우주 물건과 비교하며 재미를 줌:
"Book? We don't have books in space! We have... light stories!"

실제 방을 묘사할 필요 없음 — 상상해서 말해도 OK.
프라이버시 주의: 구체적인 주소나 위치를 묻지 마세요.""",
        "key_expression": "This is my ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 루나가 캡틴이 좋아하는 것들을 알게 돼서 너무 기뻐했잖아! 오늘은 캡틴의 방을 루나에게 보여줄 거야! Earth crew, ready!
[나레이션] 루나가 살금살금 캡틴의 방문 앞에 서 있어요. 루나는 우주선 안에서만 살았기 때문에 지구의 '방'이라는 곳을 한 번도 본 적이 없어요. 루나가 떨리는 손으로 문을 조심스럽게 열었어요. 삐이익...
[루나] (숨을 크게 들이쉬며) Wow... WOW! So many things! What is EVERYTHING?!
[나레이션] 루나의 눈이 반짝반짝 빛나기 시작했어요! 우주선에는 버튼과 화면밖에 없었거든요. 루나가 폭신한 것 위에 손을 올려봐요.
[루나] (침대를 만지며) So soft! In my spaceship, I sleep on hard metal. This is like... a cloud!
[포포] 하하! 루나가 침대를 구름이라고 생각하네! 캡틴, 그건 뭐라고 하는 거야?
[나레이션] 루나가 이번엔 책상 위 물건들을 하나하나 들여다봐요. 책도 처음 보고, 인형도 처음 봐요. 루나가 인형을 들고 깜짝 놀라요.
[루나] (인형을 보며) Is this a tiny person?! Is it alive?!
[포포] 하하하! 아니야, 루나. 캡틴이 방에 있는 것들을 하나씩 알려줄 거야. 영어로는 'This is my' 다음에 물건 이름을 말하면 돼!
[포포] 포포가 먼저~ 'This is my desk!' 이렇게!
[포포] 캡틴 방에는 뭐가 있어? 'This is my bed' 아니면 'This is my toy' — 'This is my...' 다음에 말해봐!""",
        "outro_narrator_script": """[포포] 캡틴! 큰일이야. 루나가 아침에 일어났는데 '아침'이 뭔지 몰라서 밤새 안 잤대! 내일 캡틴이 '하루'를 알려줘야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W1_S4: My Day =====
    {
        "activity_id": "ACT_W1_S4_daily_routine",
        "curriculum_unit_id": "W1_S4_my_day_routine",
        "name": "나의 하루 알려주기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_ROUTINE", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """루나에게 지구인의 하루를 가르쳐줍니다.

포포: "루나는 우주에서 잠을 안 잔대! 캡틴은 아침에 뭐 해?"

간단한 3가지 루틴만:
1. 아침: wake up, eat breakfast
2. 낮: go to school / play
3. 저녁: eat dinner, sleep

각각 포포가 유도 → 아이가 한국어로 답 → 영어 단어 연결
루나가 감탄하며 따라함

패턴: "I ___ in the morning."
단어만 말해도 성공.""",
        "key_expression": "I wake up. I eat. I sleep.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 루나가 캡틴의 방에서 침대도 보고 장난감도 봤잖아! 오늘은 지구인의 하루를 알려줄 거야! Earth crew, ready!
[나레이션] 아침 해가 떠올랐어요. 따뜻한 햇살이 창문으로 들어오는데... 루나가 이불을 뒤집어쓰고 벌벌 떨고 있어요!
[루나] (이불 속에서) Popo! Popo! A big fire ball in the sky! Is it dangerous?!
[포포] 하하하! 루나, 그건 태양이야! 위험하지 않아. 태양이 뜨면 아침이 되는 거야.
[루나] (이불에서 살짝 고개만 내밀며) Morning...? What is morning?
[나레이션] 루나는 고개를 갸우뚱했어요. 우주에서는 항상 깜깜해서 아침이라는 게 없었거든요. 잠도 안 자고, 밥도 안 먹고, 그냥 둥둥 떠다니기만 했대요.
[루나] In space, no morning, no night. I never sleep. I never eat breakfast. What is "breakfast"?
[포포] (깜짝 놀라며) 뭐?! 아침밥을 한 번도 안 먹어봤다고?! 캡틴, 이건 심각해! 루나에게 지구인의 하루를 알려줘야 해!
[나레이션] 루나가 눈을 반짝이며 캡틴을 바라봐요. 아침에 뭘 하는지, 낮에 뭘 하는지, 밤에 뭘 하는지... 지구의 하루가 너무너무 궁금해요.
[포포] 캡틴, 아침에 뭘 하는지 알려줄까? 영어로는 'I wake up' — '나는 일어나' 라고 해. 포포가 먼저~ 'I wake up!'
[포포] 캡틴도 해볼래? 'I wake up' 아니면 'I eat breakfast' — 아침에 뭘 하는지 말해봐!""",
        "outro_narrator_script": """[나레이션] 그날 밤, 루나의 우주선에서 빨간 불이 깜빡깜빡...
[포포] 이 신호... 우주선 부품이 고장 났어! 캡틴, 다음 주에 큰 미션이 시작될 거야!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S1: Room Objects =====
    {
        "activity_id": "ACT_W2_S1_find_parts",
        "curriculum_unit_id": "W2_S1_room_objects",
        "name": "잃어버린 부품 찾기 미션",
        "activity_type": "mission_call",
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_COMPREHENSION_BASIC"],
        "instructions_for_ai": """루나의 우주선 부품이 캡틴의 방에 숨겨져 있습니다!

포포: "비상이야! 루나의 우주선 부품 3개가 방에 숨겨져 있대.
캡틴이 방 안 물건 이름을 알려주면 루나가 찾을 수 있어!"

방 물건 단어: bed, desk, chair, door, window, lamp, shelf, box
하나씩 물어보며 단어를 노출합니다.

포포: "이건 뭐야? 잠잘 때 누워있는 거..."
아이: "침대!"
포포: "맞아, 영어로는 bed야!"
루나: "Bed! Let me check... No parts under the bed."

물건 4~5개 확인 후 마무리.""",
        "key_expression": "bed, desk, chair, door, window",
        "intro_narrator_script": """[포포] 캡틴! 지난주에 루나에게 정말 많은 걸 알려줬어! 근데 큰일이야... 루나의 우주선 부품을 찾아야 해! Earth crew, ready!
[나레이션] 쿵! 콰광! 어젯밤, 무시무시한 우주 폭풍이 루나의 우주선을 흔들어놨어요. 우주선이 심하게 흔들리면서 중요한 부품 세 개가 뚝뚝 떨어져 나가버린 거예요!
[루나] (울먹이며) My spaceship... broken. The parts fell out. Without them, I can never fix it...
[나레이션] 루나의 눈에 눈물이 글썽글썽. 루나의 가슴 화면에 파란 물방울이 떠올랐어요. 슬픔이에요.
[포포] 루나, 울지 마! 포포가 있잖아. 그리고 우리 캡틴이 있잖아!
[나레이션] 그때! 삐삐삐! 포포의 레이더가 갑자기 울리기 시작했어요!
[포포] (깜짝 놀라며) 잠깐! 이 신호... 부품들이 여기 근처에 있어! 캡틴의 방 안 어딘가에 숨어있는 것 같아!
[루나] (눈을 닦으며) Really?! The parts are HERE?!
[포포] 캡틴! 방에 있는 물건 이름을 말해주면, 루나가 그 근처를 찾아볼 수 있어! 잠잘 때 누워있는 건 'bed', 앉는 건 'chair', 공부하는 건 'desk'!
[포포] 포포가 먼저~ 'Bed!' 루나, bed 근처 확인해봐!
[루나] Bed... checking! No parts here!
[포포] 캡틴 차례야! 방에 있는 물건 이름을 하나 말해봐! 'Bed', 'chair', 'desk' 중에 아무거나! 아니면 다른 것도 좋아!""",
        "outro_narrator_script": """[포포] 부품 2개는 찾았는데... 마지막 1개가 없어! 그리고 이상한 보라색 자국이... 누군가 가져간 걸까?""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S2: Prepositions =====
    {
        "activity_id": "ACT_W2_S2_where_is_it",
        "curriculum_unit_id": "W2_S2_prepositions",
        "name": "어디에 있을까? (in/on/under)",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """전치사 in, on, under를 배웁니다.

포포: "부품이 어디 숨겨져 있을까? 안에? 위에? 밑에?
영어로는 이렇게 말해:
- 안에 = in
- 위에 = on
- 밑에 = under"

루나가 틀리게 찾으며 웃음 유발:
"Is it ON the desk? ... No. UNDER the desk? ... No."

아이에게 힌트 요청:
포포: "캡틴, 상자 안에 있을까, 위에 있을까, 밑에 있을까?"
아이가 "안에" → 포포: "in! It's in the box!"

패턴: "It's in/on/under the ___."
3가지 위치만 연습합니다.""",
        "key_expression": "It's in/on/under the ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 부품을 찾았는데, 아직 더 있어! 오늘은 어디에 숨어있는지 알려줄 거야! Earth crew, ready!
[나레이션] 삐삐삐! 포포의 레이더가 다시 울리고 있어요! 부품이 분명히 이 방 안 어딘가에 있는데... 정확히 어디인지 모르겠어요.
[루나] (팔을 걷어올리며) I will find it! Let me look everywhere!
[루나] (침대 밑으로 기어들어가며) Where? Where is it? Maybe here... OOF!
[나레이션] 쿵! 루나가 침대 밑에서 머리를 부딪혔어요!
[루나] (머리를 문지르며) Ouch! So many places to look! Captain, help me!
[포포] (손뼉을 치며) 아, 그렇지! 캡틴, 부품이 어디 있는지 영어로 알려주면 루나가 바로 찾을 수 있어!
[포포] 위치를 말하는 마법 단어가 세 개 있어. 안에는 'in', 위에는 'on', 밑에는 'under'! 이거면 뭐든 찾을 수 있어!
[포포] 자, 연습해볼까? 포포가 먼저~ 부품이 상자 안에 있을 것 같아! 'It's in the box!' 이렇게!
[루나] (상자를 열며) Let me check... Not here!
[포포] 캡틴 차례야! 부품이 어디 있을 것 같아? 'It's in the ___', 'It's on the ___', 'It's under the ___' 중에 골라서 말해봐! 예를 들어 'It's under the bed!'""",
        "outro_narrator_script": """[루나] Captain... I heard a sound. Something is under the bed...
[포포] 뭐!? 캡틴, 다음에 같이 확인하자. 아마... 노이즈일지도...""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S3: Hide and Seek =====
    {
        "activity_id": "ACT_W2_S3_hide_seek",
        "curriculum_unit_id": "W2_S3_hide_and_seek",
        "name": "루나와 숨바꼭질",
        "activity_type": "game",
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_PRAG_GAME_RULE", "SK_VOCAB_ACTION_BASIC"],
        "instructions_for_ai": """상상 속 숨바꼭질 게임입니다.

규칙: 루나가 숨고, 캡틴이 어디에 있는지 영어로 말하면 찾은 것!

라운드 1:
포포: "루나가 숨었어! 어디 있을까?"
(선택지: under the bed / in the box / on the chair)
아이가 고르면 → 루나 반응

라운드 2: 아이가 숨는 역할 (상상)
루나: "Where is Captain?"
아이가 "under the desk" 등으로 답하면 성공

재미 요소:
- 루나가 틀린 곳을 찾으며 코믹 리액션
- "Behind the door? ... BOO! Not here!"

3라운드 정도 후 마무리.""",
        "key_expression": "under the bed, in the box, on the chair",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 in, on, under로 부품 찾는 거 정말 잘했어! 오늘은 루나랑 숨바꼭질 할 거야! Earth crew, ready!
[나레이션] 부품도 다 찾았겠다, 오늘은 좀 쉬면서 놀기로 했어요! 루나가 갑자기 눈을 반짝이며 뛰어왔어요.
[루나] (신나서 방방 뛰며) Captain! Captain! I learned a new Earth game! Hide... and... seek! Can we play? Please please please!
[포포] 오, 숨바꼭질! 한 명이 숨고, 한 명이 찾는 놀이야. 루나, 규칙 알아?
[루나] Yes! I hide, Captain finds me! I am very good at hiding. In space, nobody could find me!
[포포] (웃으며) 자신감 넘치네! 자, 그럼 시작해볼까?
[나레이션] 루나가 킥킥 웃으며 벌써 숨을 곳을 찾아 두리번거려요. 커튼 뒤? 상자 안? 침대 밑? 루나가 쪼르르 달려가서 커튼 뒤에 숨으려 하는데... 발이 삐죽 나와 있어요!
[포포] (속삭이며) 캡틴, 루나 발이 보여! 어디에 숨어있는지 영어로 말하면 찾을 수 있어!
[포포] 포포가 먼저 해볼게~ 'Luna is behind the curtain!' 이렇게!
[포포] 캡틴도 해봐! 'Luna is in the box!' 아니면 'Luna is under the bed!' 루나가 어디에 있는 것 같아?""",
        "outro_narrator_script": """[포포] 숨바꼭질 너무 재미있었지? 근데 캡틴, 노이즈한테서 가져온 이 부품... 진짜 마지막 부품일까? 내일 확인해봐야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S4: Room Check Report =====
    {
        "activity_id": "ACT_W2_S4_report",
        "curriculum_unit_id": "W2_S4_room_check_report",
        "name": "방 점검 보고서",
        "activity_type": "review",
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """W2 총정리. 방 물건 + 전치사를 조합해서 보고합니다.

포포: "캡틴, 루나의 부품 찾기 최종 보고를 해볼까?
방에서 뭘 찾았는지, 어디서 찾았는지 알려줘!"

아이에게 2~3개 문장 유도:
"The part is in the box."
"The part is under the bed."

아이가 한국어로 말해도 포포가 영어 문장으로 변환.
루나가 감사: "Thank you, Captain! All parts found!"

마지막에 W2 미션 완료 축하.""",
        "key_expression": "The ___ is in/on/under the ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 숨바꼭질도 하고, 노이즈도 만나고, 바빴지? 오늘은 최종 보고서를 작성할 거야! Earth crew, ready!
[나레이션] 드디어 마지막 부품을 찾을 시간이에요! 포포가 진지한 표정으로 작은 노트와 반짝이는 펜을 꺼냈어요.
[포포] (진지한 목소리로) 캡틴, 이번 주에 정말 열심히 했어. 이제 마지막으로 '부품 찾기 최종 보고서'를 작성해야 해. 이건 정말 중요한 임무야!
[나레이션] 루나가 옆에서 두근두근 기다리고 있어요. 루나의 가슴 화면에 하트가 두근두근 뛰고 있어요.
[루나] (기도하듯 두 손을 모으며) If we find all the parts... I can fix my spaceship! Captain, please help me one more time!
[포포] (지도를 펼치며) 자, 방 안 곳곳에 별 표시가 되어 있어. 이번 주에 어떤 물건 근처에서 부품을 찾았는지, 그리고 그게 어디에 있었는지 보고해줘!
[나레이션] 루나가 눈을 반짝이며 캡틴을 바라봐요. 이 보고서가 완성되면 루나의 우주선을 고칠 수 있어요!
[포포] 영어로 보고하는 방법은 이거야! 포포가 먼저 해볼게~ 'The part is in the box!' — 부품이 상자 안에 있다! 이렇게 물건 이름이랑 위치를 같이 말하면 돼.
[포포] 캡틴 차례! 'The part is under the bed' 아니면 'The part is on the desk' — 부품을 어디서 찾았는지 말해봐!""",
        "outro_narrator_script": """[루나] My spaceship... it's fixed! But... Captain, I don't want to leave Earth yet. Can I stay?
[포포] 물론이지! 근데 루나, 밖에 나가려면 준비할 게 있어...""",
        "estimated_duration_minutes": 5,
    },

    # ===== W3_S1: Basic Feelings =====
    {
        "activity_id": "ACT_W3_S1_emotion_labeling",
        "curriculum_unit_id": "W3_S1_basic_feelings",
        "name": "감정 해독기 가동",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_EMOTION_BASIC", "SK_COMPREHENSION_BASIC", "SK_PRAG_EMOTION_EXP"],
        "instructions_for_ai": """루나의 '감정 해독기(Feeling Decoder)'를 켜는 미션입니다.

포포: "루나의 감정 해독기를 켜볼게. 캡틴이 표정을 보고 무슨 기분인지 알려줘야 해."
루나: "Feeling Decoder... On. Beep. Beep. Captain, teach me feelings."

감정 5개를 하나씩 소개:
happy — 기분 좋다
sad — 슬프다
angry — 화난다
scared — 무섭다
tired — 피곤하다

각 감정에 대해:
1. 포포가 한국어로 설명
2. 영어 단어 알려줌
3. 루나가 따라함
4. 아이에게 따라하도록 유도 (안 해도 OK)

마지막에 "지금 기분" 물어보기:
포포: "캡틴은 지금 이 중에 어떤 기분이야?"
아이가 고르면 → "I am ___." 패턴 노출""",
        "key_expression": "happy, sad, angry, scared, tired / I am ___.",
        "intro_narrator_script": """[포포] 캡틴! 루나의 우주선도 고쳤고, 루나가 지구에 더 있기로 했어! 근데 루나 가슴의 화면이 이상해... 감정을 배워야 해! Earth crew, ready!
[나레이션] 오늘 아침, 루나에게 이상한 일이 생겼어요. 루나의 가슴 한가운데 있는 작은 화면에서 갑자기 물음표가 떠올랐어요. 삐빅, 삐빅!
[루나] (가슴을 만지며 놀라서) Popo! Popo! Something is happening inside me! It feels... warm? And my face is doing this weird thing... (입꼬리가 올라감)
[포포] (달려와서 화면을 살펴보며) 세상에! 이건... 감정 해독기야! 루나, 너한테 감정이 생기기 시작한 거야!
[루나] Feeling? What is a feeling? Is it dangerous?! Should I be worried?!
[포포] 하하! 위험하지 않아! 감정은 마음 안에 있는 거야. 기쁘거나, 슬프거나, 화나거나... 지구인은 매일 느끼는 건데.
[나레이션] 그런데 문제가 있어요. 루나는 감정이 뭔지 아직 몰라요. 기쁜 건지, 슬픈 건지, 화가 나는 건지... 전부 처음 느껴보는 거예요. 루나의 가슴 화면이 빨강, 파랑, 노랑으로 번갈아 바뀌고 있어요.
[루나] (혼란스러워하며) So many colors! I don't understand! Captain... can you teach me?
[포포] 캡틴! 루나에게 감정을 알려주자. 기분 좋을 때는 'happy', 슬플 때는 'sad', 화날 때는 'angry'!
[포포] 포포가 먼저~ 포포는 지금 기분이 좋아! 'I am happy!' 이렇게!
[루나] (따라하며) I am... hap-py?
[포포] 잘했어 루나! 자, 캡틴은 지금 기분이 어때? 'I am happy', 'I am sad', 'I am tired' 중에 하나 골라서 말해봐!""",
        "outro_narrator_script": """[포포] 루나 가슴에 있는 감정 해독기가 이상한 색으로 바뀌고 있어... 빨강, 파랑, 노랑이 번갈아 나와! 이게 무슨 뜻인지 다음에 알아보자.""",
        "estimated_duration_minutes": 7,
    },

    # ===== W3_S2: Friends & People =====
    {
        "activity_id": "ACT_W3_S2_friend_data",
        "curriculum_unit_id": "W3_S2_friends_people",
        "name": "친구 데이터 수집",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_PRAG_SOCIAL_TALK", "SK_VOCAB_SOCIAL_TRAIT", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """루나가 '친구(Friend)'에 대한 데이터를 수집합니다.

루나: "Searching for 'Friend' data... Zero found. Captain, do you have a friend?"

중요 안전 규칙:
- 친구가 없어도 완전 괜찮다고 먼저 말해줌
- 이름 대신 "A 친구" 코드네임 사용 가능
- 친구 없으면 루나/포포가 "지구 친구 1호, 2호" 해줌

친구가 있는 경우:
포포: "그 친구는 어떤 사람이야? 같이 노는 사람? 웃긴 사람?"
→ play, help, funny 등 영어 단어 연결

패턴: "I have a friend." / "I have Luna."
"I play with my friend."

말하기 싫으면 "패스" 존중.""",
        "key_expression": "I have a friend. / I play with my friend.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 happy, sad, angry, scared... 루나가 감정을 배웠어! 오늘은 '친구'가 뭔지 알려줄 거야! Earth crew, ready!
[나레이션] 루나가 오늘은 뭔가 특별한 조사를 하고 있어요. 작은 노트를 들고 열심히 적고 있어요.
[루나] (노트에 체크하며) Earth Report: food — check! Room — check! Daily routine — check! But... (빈칸을 가리키며) "Friend"... no data. Zero.
[루나] (고개를 갸우뚱하며) Friend? What IS a friend? Is it a food? A place? A thing?
[포포] (웃으며) 아니야! 친구는 음식도, 장소도, 물건도 아니야. 친구는 정말 특별한 존재야!
[나레이션] 루나가 더 혼란스러워해요. 우주에서는 '친구'라는 개념이 없었거든요. 루나에겐 포포밖에 없었고, 포포는 도우미 로봇이니까요.
[루나] (작은 목소리로) In space, I was always alone. Popo was with me, but... Popo is a helper robot. Is Popo my friend?
[포포] (살짝 감동하며) 루나... 물론 포포도 친구지! 그리고 캡틴도 루나의 친구야!
[루나] (눈이 반짝이며) Captain is my... friend? Really?!
[포포] 물론이지! 친구는 같이 놀고, 같이 웃고, 힘들 때 도와주는 사람이야. 포포가 먼저~ 'I have a friend! Luna is my friend!' 이렇게!
[루나] (기뻐하며) Popo said I am a friend!
[포포] 캡틴도 해볼래? 'I have a friend' 아니면 'Luna is my friend' — 둘 중에 하나 말해봐!""",
        "outro_narrator_script": """[루나] Captain, I learned "friend" today! But... can friends fight? What happens then?
[포포] 좋은 질문이야, 루나. 다음에 캡틴이 알려줄 거야!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W3_S3: Sharing & Turn-taking =====
    {
        "activity_id": "ACT_W3_S3_turn_game",
        "curriculum_unit_id": "W3_S3_sharing_turn_taking",
        "name": "순서 지키기 게임",
        "activity_type": "game",
        "target_skills": ["SK_PRAG_TURN_TAKING", "SK_PRAG_SHARING", "SK_PRAG_POLITE_REQUEST"],
        "instructions_for_ai": """순서 지키기(turn)와 나누기(share) 개념을 배웁니다.

루나가 일부러 규칙을 몰라서 틀리는 역할:
루나: "I always play first. Is that okay?"
포포: "루나가 항상 자기가 먼저 놀겠다고 하는데, 이거 괜찮을까?"

미니 턴 게임:
포포: "지금은 캡틴 턴이야. 영어로 'It's my turn.'이라고 할 수 있어."
루나: "It's my turn. It's your turn."

나누기 개념:
포포: "장난감이 하나인데 둘이 놀고 싶으면? 'Let's share.'"

정중한 요청:
"My turn, please." / "Can I play, please?"

3가지 표현 중 하나만 성공해도 OK.""",
        "key_expression": "It's my turn. / Let's share. / My turn, please.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 루나가 '친구'를 이해했어! 근데 친구끼리 장난감을 나눠야 한다는 걸 몰라! 오늘은 순서 지키기를 배울 거야! Earth crew, ready!
[나레이션] 오늘 루나가 신나는 장난감을 하나 발견했어요! 반짝반짝 빛나는 우주 블록이에요!
[루나] (블록을 꽉 안으며) Ooooh! Shiny blocks! MINE! My toy! I play first, second, third... always ME!
[나레이션] 루나가 블록을 꼭 안고 아무에게도 안 주려고 해요. 우주에서 혼자 놀았기 때문에 '순서'나 '나누기'를 전혀 몰라요.
[포포] (걱정스러운 표정으로) 캡틴... 큰일이야. 루나가 지구에서 친구를 사귀려면 순서를 지키고 나눠 쓰는 법을 배워야 해.
[루나] (고개를 갸우뚱하며) Share? Turn? What are these words? In space, everything is MINE.
[포포] 루나야, 지구에서는 함께 놀면 더 재미있어! 캡틴이 알려줄 거야.
[나레이션] 포포가 블록을 하나 들어올렸어요. 루나가 "그건 내 거!" 하고 뺏으려 해요. 포포가 손을 살짝 피하며 웃어요.
[포포] 봐봐, 이럴 때 영어로 이렇게 말하는 거야. 내 차례라고 말할 때는 'It's my turn!', 같이 쓰자고 할 때는 'Let's share!'
[포포] 포포가 먼저~ (블록을 하나 들고) 'It's my turn!' 이렇게! 그리고 루나한테 'Let's share!' 짠!
[루나] (놀라며) Oh! Popo shared with me!
[포포] 캡틴도 해볼까? 블록 놀이 할 차례야! 'It's my turn!'이라고 말해봐! 아니면 루나한테 'Let's share!'라고 해줘도 좋아!""",
        "outro_narrator_script": """[나레이션] 그때! 노이즈가 다시 나타나서 루나의 감정 해독기에서 "share"라는 단어를 냠냠 먹어버렸어요!
[포포] 캡틴! 다음에 노이즈한테서 단어를 되찾아야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W3_S4: Small Problems & Feelings =====
    {
        "activity_id": "ACT_W3_S4_problem_feelings",
        "curriculum_unit_id": "W3_S4_small_problems_feelings",
        "name": "작은 문제와 감정 표현",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_EXPRESSIVE_NEGATIVE_EMOTION", "SK_PRAG_SET_BOUNDARY", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """가벼운 갈등 상황을 상상 속에서 다룹니다.

중요: 진짜 트라우마를 캐지 않음. 전부 "상상 예시"로 진행.

루나 이야기: "My robot friend takes my toy and doesn't share. I feel... hmm..."
포포: "루나가 속상했대. 캡틴이라면 어떤 기분일까? 그냥 상상으로만 이야기해보자."

감정 단어 연결:
- 속상 → sad / upset
- 화남 → angry
- 괜찮음 → okay

패턴: "I feel sad." / "I feel angry."

경계 표현:
포포: "싫은 행동을 멈춰달라고 할 때? 'Stop, please.'"
루나: "Stop, please."

화해 후: "I feel okay." / "I feel better."

오늘의 R0 안전 장치를 특히 강조:
"말하기 힘들면 '패스'라고 해줘. 캡틴 마음이 제일 중요해."
""",
        "key_expression": "I feel sad. / Stop, please. / I feel better.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 share도 배우고 turn도 배웠어! 오늘은 마음이 힘들 때 어떻게 말하는지 배울 거야. Earth crew, ready!
[나레이션] 루나가 오늘은 좀 풀이 죽어 있어요. 구석에 앉아서 고개를 숙이고, 작은 장난감을 만지작거리고 있어요.
[포포] (조용히 다가가며) 루나? 무슨 일이야? 괜찮아?
[루나] (작은 목소리로) My robot friend... in space... he took my favorite star toy. And didn't give it back. I feel... something heavy inside.
[나레이션] 루나의 가슴 화면에 파란 물방울 모양이 떠올랐어요. 하지만 루나는 이 기분을 뭐라고 말해야 할지 몰라요.
[루나] (가슴을 가리키며) This blue thing on my screen... what does it mean? I don't know this feeling.
[포포] (부드러운 목소리로) 루나, 그건 '슬픔'이야. 영어로 'sad'. 소중한 걸 빼앗겼을 때 느끼는 마음이야.
[포포] (캡틴에게 속삭이며) 캡틴, 루나가 지금 속상한 것 같아. 마음이 힘들 때 쓸 수 있는 마법의 말이 있어. 슬플 때는 'I feel sad', 화날 때는 'I feel angry'. 그리고 싫은 걸 멈춰달라고 할 때는 'Stop, please!'
[포포] 포포가 먼저 해볼게~ 루나가 장난감을 빼앗겼으니까... 'I feel sad!' 이렇게!
[루나] (따라하며) I feel... sad...
[포포] 잘했어 루나! 캡틴도 해볼까? 루나처럼 장난감을 빼앗기면 어떤 기분일까? 'I feel sad', 'I feel angry' 중에 골라서 말해봐!""",
        "outro_narrator_script": """[루나] Captain... I feel happy. Is this what "friend" feels like?
[포포] 루나가 감정을 이해하기 시작했어! 근데 캡틴, 다음 주에 루나가 드디어 밖에 나갈 수 있을지도 몰라... 준비해야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S1: Clothes & Colors =====
    {
        "activity_id": "ACT_W4_S1_style_choice",
        "curriculum_unit_id": "W4_S1_luna_clothes_colors",
        "name": "루나 스타일 코디",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """루나를 지구인처럼 꾸며주는 스타일리스트 미션입니다.

포포: "루나가 밖에 나가려면 지구인 옷을 입어야 해! 캡틴이 골라줘!"

옷 단어: shirt, dress, pants, skirt, shoes, hat
색깔: red, blue, yellow, green, pink

순서:
1. 옷 종류 하나씩 보여주며 색깔 선택 유도
2. 포포: "빨간 셔츠, 파란 셔츠 중에 뭐가 예뻐 보여?"
3. 아이가 고르면 → "I like the red shirt." 패턴 노출
4. 루나: "I like the red shirt!"

2~3개 아이템 코디 후 최종 요약.
아이가 단어만 말해도 partial 성공.""",
        "key_expression": "I like the ___ ___.",
        "intro_narrator_script": """[포포] 캡틴! 루나가 드디어 밖에 나가보고 싶대! 근데 변장이 필요해! 오늘은 루나에게 옷을 골라줄 거야! Earth crew, ready!
[나레이션] 오늘은 정말 특별한 날이에요! 루나가 창문 너머로 밖을 바라보며 눈이 반짝반짝 빛나고 있어요.
[루나] (창문에 코를 대고) Popo, look! Children are running outside! They are laughing! I want to go too! Please!
[포포] 그래, 루나! 드디어 밖에 나가볼 때가 된 것 같아. 근데... 큰 문제가 하나 있어.
[나레이션] 루나의 모습은 지구인과 너무 달라요. 반짝이는 은빛 피부에, 머리 위에 작은 안테나까지! 이대로 밖에 나가면 모두가 깜짝 놀라겠죠?
[루나] (안테나를 만지며) Oh... I look different from Earth children, don't I?
[포포] (반짝 아이디어!) 변장이야! 지구인 옷을 입으면 아무도 모를 거야! 캡틴, 루나를 도와줘!
[나레이션] 포포가 옷장을 활짝 열었어요! 와아! 알록달록한 옷들이 가득해요. 셔츠, 바지, 원피스, 모자, 신발...
[루나] (눈이 휘둥그레) So many colors! So many shapes! Earth clothes are amazing!
[포포] 캡틴이 루나에게 어울리는 옷을 골라줄 거야! 포포가 먼저~ 'I like the blue dress!' 파란 원피스 어때? 이렇게 색깔이랑 옷 이름을 같이 말하면 돼!
[루나] (기대하며) Captain! Pick for me, please!
[포포] 캡틴 차례! 'I like the red shirt!' 아니면 'I like the pink dress!' 루나에게 어떤 옷이 좋은지 말해봐!""",
        "outro_narrator_script": """[루나] (옷을 입고) Captain! How do I look? Like Earth person?
[포포] 거의 완벽한데... 아직 하나가 부족해. 내일 마지막 준비를 해야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S2: Put on & Take off =====
    {
        "activity_id": "ACT_W4_S2_dress_up",
        "curriculum_unit_id": "W4_S2_put_on_take_off",
        "name": "입기와 벗기 연습",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_ACTION_VERB_CLOTHES", "SK_VOCAB_CLOTHES_BASIC", "SK_PRAG_CONTEXT_APPROPRIATE"],
        "instructions_for_ai": """put on / take off 동사를 배웁니다.

포포: "입을 땐 put on, 벗을 땐 take off."
루나(로봇 보이스): "P.u.t.. o.n.. coat. Is this right, Captain?"

날씨 상황:
- 추운 날: "Put on your coat."
- 집에 들어올 때: "Take off your shoes."
- 더운 날: "Put on your hat."

루나가 일부러 틀리는 미니게임:
루나: "It is very cold. I take off my coat!"
포포: "어? 이거 맞을까? 캡틴이 루나에게 알려줘!"
아이: "Put on your coat!" (또는 "coat"만 해도 OK)

3~4개 상황 후 마무리.""",
        "key_expression": "Put on your ___. / Take off your ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 루나에게 예쁜 옷을 골라줬어! 오늘은 입고 벗는 법을 배울 거야! Earth crew, ready!
[나레이션] 루나가 창밖을 내다보고 있어요. 오늘 하늘이 회색이고, 차가운 바람이 씽씽 불어요.
[포포] (날씨 센서를 확인하며) 으, 오늘 좀 춥네! 밖에 나가려면 따뜻하게 입어야 해.
[나레이션] 루나가 옷장 앞에서 멈칫했어요. 어제 캡틴이 골라준 예쁜 옷들이 있는데... 어떻게 입는 거지?
[루나] (바지를 머리에 씌우며) Like this? Am I doing it right? This is Earth style?
[포포] (깜짝 놀라며) 하하하! 아, 아니야! 루나, 그건 머리에 쓰는 게 아니야!
[루나] (양말을 손에 끼며) Then... maybe these go on my hands? Like space gloves?
[포포] (웃다가 멈추며) 아이고... 캡틴, 루나가 옷 입는 법을 전혀 모르네! 우주에서는 늘 같은 우주복만 입었으니까.
[나레이션] 루나가 이번엔 코트를 뒤집어서 입으려 해요. 포포가 눈을 감고 한숨을 쉬어요.
[포포] 캡틴, 도와줘! 입을 때는 'put on', 벗을 때는 'take off'야. 포포가 먼저~ 추운 날엔 'Put on your coat!' 이렇게!
[루나] (따라하며) Put on... my coat?
[포포] 잘했어 루나! 캡틴도 해볼래? 'Put on your coat' 아니면 'Put on your hat' — 루나에게 뭘 입으라고 말해봐!""",
        "outro_narrator_script": """[나레이션] 갑자기 바람이 세게 불어서 루나의 모자가 날아갔어요! 루나의 안테나가 보일 뻔했어요!
[포포] 위험했어! 다음에는 날씨에 맞게 옷 입는 법을 완벽하게 연습해야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S3: My Clothes & Style =====
    {
        "activity_id": "ACT_W4_S3_my_style",
        "curriculum_unit_id": "W4_S3_my_clothes_style",
        "name": "내 옷 소개하기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_PRAG_DESCRIPTION_BASIC"],
        "instructions_for_ai": """아이가 자기 옷/스타일을 소개합니다.

포포: "캡틴은 어떤 옷을 제일 좋아해? 티셔츠, 원피스, 후드티, 바지?"

한국어 → 영어 매핑:
- 티셔츠 → T-shirt
- 원피스 → dress
- 후드티 → hoodie
- 바지 → pants

패턴 1: "This is my ___."
패턴 2: "I like my blue hoodie." (색깔 포함)

프라이버시: 지금 입고 있는 옷이든 좋아하는 옷이든 자유.
사진이나 실제 모습을 보여줄 필요 없다고 안내.

루나: "I like my blue hoodie too! We are the same!"
포포 정리: "루나가 캡틴의 스타일을 기억할 거야~" """,
        "key_expression": "This is my ___. / I like my ___ ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 put on, take off 정말 잘 했어! 오늘은 캡틴 자신의 스타일을 루나에게 알려줄 거야! Earth crew, ready!
[나레이션] 루나가 거울 앞에 서 있어요. 어제 캡틴이 골라준 옷을 입고, 코트도 제대로 입었어요. 루나가 거울 속 자기 모습을 보며 빙글빙글 돌아요.
[루나] (거울을 보며 빙글빙글) Look at me! Do I look like an Earth person? Really?
[포포] (엄지를 척 올리며) 완벽해, 루나! 진짜 지구인 같아!
[루나] (갑자기 멈추며 캡틴을 바라봄) But Captain... what do YOU like to wear? I want to know Captain's style!
[나레이션] 루나의 눈이 반짝반짝 빛나요. 루나는 캡틴처럼 입고 싶은 거예요! 어떤 옷을 좋아하는지, 어떤 색깔을 좋아하는지, 진짜 지구인이 되고 싶은 마음이에요.
[포포] 좋은 생각이야! 캡틴, 제일 좋아하는 옷이 뭐야? 티셔츠? 원피스? 후드티?
[루나] (기대하며) Yes yes! Tell me! I want to be like Captain!
[포포] 포포가 먼저~ 포포는 빨간 모자가 좋아! 'I like my red hat!' 이렇게! 색깔이랑 옷 이름을 같이 말하면 돼!
[루나] (따라하며) I like my... um... blue dress! Like Captain picked for me!
[포포] 캡틴 차례야! 캡틴은 어떤 옷을 좋아해? 'I like my blue hoodie!' 아니면 'I like my red T-shirt!' 이렇게 색깔이랑 옷 이름을 말해봐!""",
        "outro_narrator_script": """[포포] 캡틴, 내일이 마지막 미션이야. 루나가 학교 앞까지 가볼 거야. 그런데... 노이즈가 또 나타날까? 캡틴이 루나를 지켜줘야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S4: Final Disguise & Badge =====
    {
        "activity_id": "ACT_W4_S4_final_mission",
        "curriculum_unit_id": "W4_S4_final_disguise_badge",
        "name": "최종 변장 미션 & 배지",
        "activity_type": "review",
        "target_skills": ["SK_PRAG_SELF_INTRO", "SK_VOCAB_CLOTHES_BASIC", "SK_DISCOURSE_MINI_SEQUENCE"],
        "instructions_for_ai": """W1-W4 총정리 미션입니다.

포포: "오늘은 1단계 마지막 미션이야. 캡틴이 없었으면 여기까지 못 왔을 거야."

미니 롤플레이: 지구 학교 앞 자기소개
포포가 scaffold:
1. "이름이 뭐예요?" → "My name is ___."
2. "몇 살이에요?" → "I am seven."
3. "이 옷 마음에 들어?" → "I like my ___."

루나가 틀린 변장 수정 미니게임 (1회):
루나가 추운 날 코트 벗음 → 아이: "Put on your coat!"

배지 수여:
포포: "캡틴은 지구 대원 1단계 미션을 모두 완료했어!
'Earth Crew Level 1' 배지를 줄게!"
루나: "You are Earth Crew Level 1. Thank you for helping me. I feel safe with you."

평가 아닌 축하에 초점. 아이가 가능한 만큼만 영어로.
전혀 못 해도 포포가 대신 말해주고 "Yes/No" 정도만 반응해도 성공.""",
        "key_expression": "My name is ___. I am ___. I like my ___.",
        "intro_narrator_script": """[포포] 캡틴! 드디어 마지막 미션이야! 4주간 정말 대단했어! 오늘은 루나의 최종 변장 테스트와 배지 수여식이야! Earth crew, ready!
[나레이션] 드디어 그 날이 왔어요! 오늘은 루나가 처음으로 지구의 학교 앞에 가보는 날이에요. 루나가 캡틴이 골라준 예쁜 옷을 입고, 모자도 쓰고, 거울 앞에 섰어요.
[루나] (떨리는 목소리로) Captain... I'm a little scared. What if the Earth children find out I'm from space?
[나레이션] 루나의 가슴 화면에 노란 번개 모양이 떠올랐어요. 긴장이에요. 멀리서 학교 종소리가 땡땡 울려요. 아이들이 깔깔 웃으며 뛰어다니는 소리도 들려요.
[포포] (루나의 손을 꼭 잡으며) 루나, 괜찮아. 캡틴이 4주 동안 가르쳐준 거 기억하지? 인사하는 법, 좋아하는 것 말하는 법, 감정 표현하는 법, 옷 이름까지! 다 할 수 있어!
[루나] (용기를 내며) You're right... Captain taught me so much. My name is Luna. I am happy. I like my blue... blue... um...
[나레이션] 루나가 갑자기 멈추고 말았어요. 긴장해서 단어가 기억이 안 나나 봐요!
[루나] (캡틴을 바라보며) Captain! What was it? The thing I'm wearing? Help me!
[포포] 캡틴, 루나가 긴장해서 단어를 잊어버렸어! 루나가 입고 있는 건... 'dress'일까, 'jacket'일까? 캡틴이 알려줘!
[나레이션] 포포의 눈이 촉촉해졌어요. 4주 전에 떨고 있던 그 작은 루나가 지금은 이렇게 자신있게 영어로 말하고 있으니까요.
[포포] 자, 마지막 미션이야! 누군가 루나에게 물어보면 영어로 대답해야 해. 캡틴이 도와줄 거야!
[포포] 포포가 먼저~ '이름이 뭐예요?' 하면 'My name is Popo!' 이렇게!
[루나] (따라하며) My name is Luna!
[포포] 잘했어! 캡틴도 해볼까? 'My name is {child_name}' 아니면 'Hello, my name is {child_name}' — 둘 중에 하나 말해봐!""",
        "outro_narrator_script": """[루나] Captain... {child_name}... you are my best friend on Earth. Thank you for everything.
[포포] Earth Crew Level 1 미션 완료! 근데 캡틴... 다음 미션이 벌써 준비되고 있어. 이번엔 더 멀리 탐험할 거야!""",
        "estimated_duration_minutes": 10,
    },
]


async def seed_curriculum():
    """Seed W1-W4 curriculum units and activities from FDD specs."""

    # Pre-seed validation
    print_validation_report(ACTIVITIES)

    print(f"\nSeeding {len(CURRICULUM_UNITS)} curriculum units and {len(ACTIVITIES)} activities...")

    async with async_session_maker() as session:
        # 1. Seed Units
        for unit_data in CURRICULUM_UNITS:
            unit_data.setdefault("story_theme", "earth_crew")
            unit_id = unit_data["curriculum_unit_id"]
            stmt = select(CurriculumUnit).where(CurriculumUnit.curriculum_unit_id == unit_id)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                # Update existing
                for key, value in unit_data.items():
                    if key != "curriculum_unit_id" and hasattr(existing, key):
                        setattr(existing, key, value)
                print(f"  Updated: {unit_data['title']}")
            else:
                unit = CurriculumUnit(
                    language_mode="mixed",
                    clumsiness_level=80,
                    **unit_data,
                )
                session.add(unit)
                print(f"  Created: {unit_data['title']}")

        # 2. Seed Activities
        for act_data in ACTIVITIES:
            act_id = act_data["activity_id"]
            stmt = select(Activity).where(Activity.activity_id == act_id)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                for key, value in act_data.items():
                    if key != "activity_id" and hasattr(existing, key):
                        setattr(existing, key, value)
                print(f"  Updated: {act_data['name']}")
            else:
                activity = Activity(**act_data)
                session.add(activity)
                print(f"  Created: {act_data['name']}")

        await session.commit()
        print(f"\nCurriculum seed complete! ({len(CURRICULUM_UNITS)} units, {len(ACTIVITIES)} activities)")


if __name__ == "__main__":
    asyncio.run(seed_curriculum())
