"""
공룡 탐험대 (Dinosaur Expedition) — W1-W4 Curriculum Seed

Story Theme: dino_expedition
World: 시간 여행 포털을 통해 공룡 시대에 도착한 루나, 포포, 캡틴(아이).
       루나는 탐험 일지를 기록하는 우주 과학자, 포포는 가이드 로봇,
       캡틴은 공룡 박사가 되어 Trixie(아기 트리케라톱스)를 돌보고 가르칩니다.

관통 서사: '공룡 세계 지도 완성하기'
  - W1: 초원 지역 탐험 (자기소개) → 지도 스티커 1개
  - W2: 절벽/동굴 지역 (화석 발굴, 전치사) → 지도 스티커 2개
  - W3: 숲/호수 지역 (감정, 친구) → 지도 스티커 3개
  - W4: 하늘빛 계곡 (장비, 최종) → 지도 완성!

Learning progression (same as earth_crew):
  - W1: 자기소개 (My name is, I like)
  - W2: 전치사 (in/on/under) — 공룡 화석/알 찾기
  - W3: 감정 (I feel, Stop please) — 공룡 친구 사귀기
  - W4: 옷/색깔 (I like the ___ ___) — 탐험 장비 입기
"""
import asyncio
import sys
import os

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "scripts"))

from sqlalchemy import select
from app.database import async_session_maker, engine, Base
from app.models.curriculum import CurriculumUnit, Activity
from validators.speech_elicitation import print_validation_report

# --------------------------------------------------------------------------
# Curriculum Units (W1-W4, 4 sessions each = 16 sessions)
# --------------------------------------------------------------------------

CURRICULUM_UNITS = [
    # Week 1: 공룡 세계에 도착 — 자기소개
    {
        "curriculum_unit_id": "DINO_W1_S1_arrival",
        "title": "공룡 세계에 도착!",
        "description": "시간 여행 포털을 통해 공룡 시대에 도착! 공룡 친구에게 이름과 나이를 소개해봐요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 70,
        "target_skills": ["SK_VOCAB_DAILY_GREET", "SK_SENTENCE_BASIC", "SK_PRAG_SELF_INTRO"],
    },
    {
        "curriculum_unit_id": "DINO_W1_S2_favorite_dino",
        "title": "좋아하는 공룡은?",
        "description": "어떤 공룡이 좋아? 좋아하는 음식, 동물, 색깔을 공룡 친구에게 알려줘요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 65,
        "target_skills": ["SK_VOCAB_DAILY_FOOD", "SK_SENTENCE_BASIC", "SK_PRAG_PREFERENCE"],
    },
    {
        "curriculum_unit_id": "DINO_W1_S3_dino_nest",
        "title": "공룡 둥지 탐험",
        "description": "공룡 둥지에 뭐가 있는지 루나에게 알려줘요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_DAILY_ROOM", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "DINO_W1_S4_dino_day",
        "title": "공룡의 하루",
        "description": "공룡들은 아침에 뭘 할까? 루나에게 공룡의 하루를 상상해서 알려줘요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_DAILY_ROUTINE", "SK_SENTENCE_BASIC"],
    },

    # Week 2: 공룡 알 찾기 — 전치사
    {
        "curriculum_unit_id": "DINO_W2_S1_fossil_hunt",
        "title": "화석 발굴 현장",
        "description": "공룡 화석을 찾으며 주변 물건 이름을 배워요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "DINO_W2_S2_egg_location",
        "title": "공룡 알은 어디에?",
        "description": "in, on, under를 사용해서 공룡 알이 어디 있는지 말해봐요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 55,
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "DINO_W2_S3_dino_hide_seek",
        "title": "아기 공룡 숨바꼭질",
        "description": "아기 공룡과 숨바꼭질하며 전치사를 연습해요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 50,
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_PRAG_GAME_RULE", "SK_VOCAB_ACTION_BASIC"],
    },
    {
        "curriculum_unit_id": "DINO_W2_S4_expedition_report",
        "title": "탐험 보고서",
        "description": "W2에서 발견한 것을 종합해서 탐험 보고서를 작성해요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 50,
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
    },

    # Week 3: 공룡 친구 사귀기 — 감정
    {
        "curriculum_unit_id": "DINO_W3_S1_dino_feelings",
        "title": "공룡도 감정이 있대!",
        "description": "happy, sad, angry, scared, tired — 공룡 친구의 감정을 읽어봐요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 65,
        "target_skills": ["SK_VOCAB_EMOTION_BASIC", "SK_SENTENCE_BASIC", "SK_PRAG_EMOTION_EXP"],
    },
    {
        "curriculum_unit_id": "DINO_W3_S2_dino_friends",
        "title": "공룡 무리와 친구",
        "description": "공룡 무리에서 친구를 사귀는 법을 배워요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_SOCIAL_TRAIT", "SK_PRAG_SOCIAL_TALK", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "DINO_W3_S3_share_berries",
        "title": "열매 나누기",
        "description": "share, turn — 공룡 친구와 열매를 나누며 규칙을 배워요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_PRAG_TURN_TAKING", "SK_PRAG_SHARING", "SK_PRAG_POLITE_REQUEST"],
    },
    {
        "curriculum_unit_id": "DINO_W3_S4_brave_explorer",
        "title": "용감한 탐험가",
        "description": "무서울 때 'I feel scared', 멈춰달라고 할 때 'Stop, please' 말하는 법을 배워요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_EXPRESSIVE_NEGATIVE_EMOTION", "SK_PRAG_SET_BOUNDARY", "SK_SENTENCE_BASIC"],
    },

    # Week 4: 탐험 장비 — 옷/색깔
    {
        "curriculum_unit_id": "DINO_W4_S1_explorer_gear",
        "title": "탐험 장비 고르기",
        "description": "탐험 모자, 조끼, 부츠 — 색깔과 장비 이름을 배우며 루나를 꾸며줘요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "DINO_W4_S2_gear_up",
        "title": "장비 입기!",
        "description": "put on, take off — 탐험 상황에 맞게 장비를 입고 벗어봐요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_VOCAB_ACTION_VERB_CLOTHES", "SK_VOCAB_CLOTHES_BASIC", "SK_PRAG_CONTEXT_APPROPRIATE"],
    },
    {
        "curriculum_unit_id": "DINO_W4_S3_my_explorer_style",
        "title": "나만의 탐험 스타일",
        "description": "내가 좋아하는 탐험 장비를 소개해요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_PRAG_DESCRIPTION_BASIC"],
    },
    {
        "curriculum_unit_id": "DINO_W4_S4_final_expedition",
        "title": "최종 탐험 & 탐험대장 배지",
        "description": "W1-W4 총정리! 자기소개 + 장비 소개를 하고 공룡 탐험대장 배지를 받아요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 50,
        "target_skills": ["SK_PRAG_SELF_INTRO", "SK_VOCAB_CLOTHES_BASIC", "SK_DISCOURSE_MINI_SEQUENCE"],
    },
]

# --------------------------------------------------------------------------
# Shared character guide — injected into every instructions_for_ai
# --------------------------------------------------------------------------

TRIXIE_GUIDE = """
[Trixie 캐릭터 가이드 — 아기 트리케라톱스]
Trixie는 말을 못 하므로 행동과 소리로만 표현합니다:
- 기쁠 때: 꼬리를 흔들며 "삐이익!" 기쁜 소리, 방방 뛰기
- 슬플 때: 고개를 떨구고 작게 "삐이익..." 울음
- 흥분할 때: 앞발로 땅을 콩콩, 방방 뛰기
- 무서울 때: 캡틴 뒤에 숨거나 꼬리로 캡틴 다리를 감싸기
- 고마울 때: 뺨을 비비며 킁킁
- 자랑할 때: 코로 물건을 굴려서 캡틴 앞에 가져다 놓기

[루나 역할 — 탐험 기록 과학자]
루나는 이 스토리에서 '우주 과학자'로서 공룡 세계를 관찰하고 탐험 일지에 기록하는 역할입니다.
루나는 공룡에 대해 모르지만, 과학적 호기심으로 비교 분석합니다 (예: "In space, we don't have this!").
가르침의 대상은 주로 Trixie입니다 — 캡틴이 Trixie에게 가르쳐주는 구조.
루나는 캡틴이 말한 것을 "기록"하며 영어로 반복/정리합니다.

[관통 서사: 공룡 세계 지도 완성하기]
매주 새로운 구역을 탐험하며 지도에 스티커를 붙입니다:
W1=초원, W2=절벽/동굴, W3=숲/호수, W4=하늘빛 계곡.
세션 마무리 시 "지도에 별 스티커를 하나 붙였어!" 같은 성취감 요소를 자연스럽게 포함하세요.
"""

# --------------------------------------------------------------------------
# Activities
# --------------------------------------------------------------------------

ACTIVITIES = [
    # ===== W1_S1: 공룡 세계에 도착! =====
    {
        "activity_id": "ACT_DINO_W1_S1_mission_start",
        "curriculum_unit_id": "DINO_W1_S1_arrival",
        "name": "미션 콜: 공룡 탐험대 출동",
        "activity_type": "mission_call",
        "target_skills": ["SK_COMPREHENSION_BASIC", "SK_AFFECT_CONFIDENCE"],
        "instructions_for_ai": TRIXIE_GUIDE + """오늘은 시간 여행 포털을 통해 공룡 세계에 도착한 첫날입니다.

첫 턴(turn_count=0)에서 포포가 해야 할 것:
1. 아기 트리케라톱스(영어 이름: Trixie)를 소개하며 미션 설명
2. 구체적인 문장 틀을 제시: "'My name is ___'에서 빈칸에 캡틴 이름을 넣어서 말해봐!"
3. 예시를 먼저 보여주기: "포포가 먼저 해볼게~ 'My name is Popo!' 이렇게! 캡틴도 해볼까?"

중요:
- 절대 추상적인 질문만 하지 마세요
- 항상 정답 예시나 문장 틀을 함께 제시하세요
- 아이가 이름만 말해도 성공으로 처리합니다
- 포포가 풀 문장으로 리폼해줍니다: "잘했어! 'My name is [아이 이름]!'"
- 루나가 감탄: "Wow! Nice to meet you, Captain!"

아이가 아직 말을 안 하면:
- 선택지 제공: "이름을 말해볼까? 아니면 포포가 먼저 해볼까?"
- 따라하기 유도: "'Hello!'부터 해볼까? 포포 따라해봐~ 'Hello!'" """,
        "key_expression": "My name is ___.",
        "story_content": "시간 여행 포털을 통해 6천만 년 전 공룡 세계에 도착한 이야기. 아기 트리케라톱스 Trixie를 만나 공룡 탐험대가 결성됩니다.",
        "intro_narrator_script": """[나레이션] 어느 날, 포포의 레이더에서 이상한 신호가 잡혔어요. 삐삐삐! 시간 여행 포털이 열린 거예요! 번쩍이는 초록빛 소용돌이가 나타나더니... 슈우웅! 루나와 포포, 그리고 캡틴을 빨아들였어요!
[루나] (두리번거리며) W-where are we? These trees are SO big! And... what is THAT huge thing moving over there?!
[나레이션] 거대한 나뭇잎 사이로 어마어마하게 큰 동물이 느릿느릿 걸어가고 있어요. 길다란 목, 거대한 몸, 쿵쿵쿵 발소리! 공룡이에요!
[포포] (깜짝 놀라며) 세상에! 여긴... 공룡 시대야! 우리가 6천만 년 전으로 온 거야!
[루나] Di-no-saur? What is a dinosaur?!
[나레이션] 그때, 덤불 뒤에서 작은 울음소리가 들렸어요. 삐이익... 삐이익... 조심스럽게 고개를 내민 건 아기 트리케라톱스! 뿔이 세 개 달린 귀여운 아기 공룡이에요.
[포포] 와, 아기 공룡이야! 탐험을 좋아하는 호기심쟁이인가 봐. 이름이... (레이더를 확인하며) Trixie! 이 아기 공룡 이름이 Trixie래! 무리는 저 언덕 너머에 있나 봐. 엄마 공룡이 가끔 보러 오는 것 같아!
[루나] (눈을 반짝이며) Trixie! So cute! Hello, little dinosaur!
[포포] 캡틴, Trixie가 우리를 도와줄 수 있을 것 같아. 근데 먼저 인사를 해야지! 'My name is' 다음에 이름을 말하는 거야!
[포포] 포포가 먼저 해볼게~ 'My name is Popo!' 이렇게!
[포포] 캡틴도 해볼래? 'My name is...' 다음에 캡틴 이름을 말해봐! 'Hello, Trixie!' 아니면 이름만 말해도 좋아!""",
        "estimated_duration_minutes": 5,
    },
    {
        "activity_id": "ACT_DINO_W1_S1_self_intro",
        "curriculum_unit_id": "DINO_W1_S1_arrival",
        "name": "자기소개하기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_GREET", "SK_SENTENCE_BASIC", "SK_PRAG_SELF_INTRO"],
        "instructions_for_ai": TRIXIE_GUIDE + """아이가 아기 공룡 Trixie에게 자기소개를 합니다.

순서:
1. 이름: "My name is ___." (포포가 한국어로 유도)
2. 나이: "I am seven." (포포: "몇 살인지도 알려줄래?")
3. 인사: "Nice to meet you!" (루나가 따라하며 감동)

각 단계에서:
- 아이가 한국어로 말해도 포포가 영어로 연결
- 단어만 말해도 성공 (예: "seven" → 포포: "맞아, I am seven!")
- 루나가 매번 감탄: "Wow!" "So cool!" "Captain is seven!"

핵심: 아이가 '공룡 박사' 느낌을 받도록. Trixie에게 가르쳐주는 구조.""",
        "key_expression": "My name is ___. I am ___.",
        "intro_narrator_script": """[나레이션] 아기 공룡 Trixie가 호기심 가득한 눈으로 캡틴을 바라보고 있어요. 짧은 꼬리를 살랑살랑 흔들며 킁킁 냄새를 맡아요. 캡틴이 신기한가 봐요!
[루나] (Trixie를 쓰다듬으며) Oh! Trixie's skin is so bumpy! Like little rocks! And the three horns... so cool!
[나레이션] Trixie가 루나의 손을 꼬리로 톡톡 건드렸어요. 친해지고 싶은 거예요! 그런데 Trixie가 캡틴 앞에 쪼그려 앉으며 고개를 갸웃했어요.
[포포] Trixie가 캡틴이 궁금한가 봐! 공룡 세계에서는 이름을 알려주면서 인사하거든. 'My name is' 다음에 이름을 말하는 거야!
[포포] 포포가 먼저 해볼게. 'My name is Popo!' 이렇게!
[루나] (따라하며) My name is Luna!
[나레이션] Trixie가 삐이익! 하고 기뻐해요. 이제 캡틴 차례예요!
[포포] 캡틴도 해볼래? 'My name is...' 다음에 캡틴 이름을 말해봐! 'My name is {child_name}' 아니면 그냥 이름만 말해도 좋아!""",
        "outro_narrator_script": """[포포] 캡틴, 잠깐... 저 멀리서 쿵쿵쿵 소리가 들려! 큰 공룡이 오고 있는 것 같아... 다음에 확인해보자!""",
        "estimated_duration_minutes": 5,
    },

    # ===== W1_S2: 좋아하는 공룡은? =====
    {
        "activity_id": "ACT_DINO_W1_S2_favorites",
        "curriculum_unit_id": "DINO_W1_S2_favorite_dino",
        "name": "좋아하는 것 알려주기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_FOOD", "SK_SENTENCE_BASIC", "SK_PRAG_PREFERENCE"],
        "instructions_for_ai": TRIXIE_GUIDE + """루나가 공룡 세계의 음식/동물/색깔에 대해 모릅니다. 캡틴이 가르쳐줍니다.

포포: "루나가 공룡들이 뭘 먹는지 알고 싶대. 캡틴이 좋아하는 음식이 뭐야?"
아이가 한국어로 답하면 → 포포가 영어 매핑
예: "사과" → "영어로는 apple이야!"
루나: "Apple! I like apple too! Do dinosaurs eat apples?"

패턴: "I like ___."
아이가 따라하면 칭찬. 안 해도 괜찮음 — 포포가 대신.

3가지까지만 물어보고 마무리:
1. 좋아하는 음식
2. 좋아하는 동물 (or 공룡)
3. 좋아하는 색깔""",
        "key_expression": "I like ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 Trixie에게 이름도 알려주고, 멋지게 인사했잖아! 오늘은 좋아하는 것들을 알려줄 거야! 공룡 탐험대, 출동!
[나레이션] 오늘은 공룡 세계의 넓은 초원이에요! 알록달록한 열매가 달린 나무들이 있고, 여기저기 공룡들이 한가롭게 풀을 뜯고 있어요. Trixie가 큰 나무 아래에서 뭔가를 열심히 먹고 있어요.
[루나] (Trixie를 보며) What is Trixie eating? That red thing on the tree! Is it... food?
[나레이션] Trixie가 빨간 열매를 입에 물고 와서 캡틴 발 앞에 톡! 하고 내려놨어요. 선물인 것 같아요!
[루나] Trixie brought us a gift! But... what is this? In space, I only eat energy capsules. And dinosaur food looks so... different!
[포포] 하하! Trixie가 좋아하는 열매를 선물로 준 거야! 캡틴, 캡틴은 뭘 좋아해? 루나에게 알려주자!
[나레이션] 루나가 기대에 찬 눈으로 캡틴을 바라봐요. Trixie도 꼬리를 흔들며 기다리고 있어요.
[포포] 캡틴, 좋아하는 것을 말할 때는 'I like' 다음에 좋아하는 걸 말하면 돼. 포포가 먼저~ 'I like apples!' 이렇게!
[포포] 캡틴은 뭘 좋아해? 'I like apples' 아니면 'I like pizza' 아니면 다른 것도 좋아! 'I like...' 다음에 말해봐!""",
        "outro_narrator_script": """[루나] Captain! Tomorrow Trixie wants to show us the dinosaur nest! What is a "nest"?
[포포] 내일은 Trixie의 둥지를 구경할 거야. 어떤 게 있을지 상상해봐!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W1_S3: 공룡 둥지 탐험 =====
    {
        "activity_id": "ACT_DINO_W1_S3_nest_tour",
        "curriculum_unit_id": "DINO_W1_S3_dino_nest",
        "name": "공룡 둥지 구경시켜주기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_ROOM", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """Trixie의 공룡 둥지를 탐험합니다.

포포: "Trixie가 둥지에 뭐가 있는지 보여주고 싶대! 뭐가 있어?"
아이가 자유롭게 말하면 → 영어 단어 연결

예상 단어: egg, rock, leaf, stick, bone, nest
패턴: "This is a ___."

루나가 우주 물건과 비교하며 재미를 줌:
"Egg? We don't have eggs in space! These are so round and warm!"

상상해서 말해도 OK.""",
        "key_expression": "This is a ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 좋아하는 것도 알려주고 멋졌어! 오늘은 Trixie의 둥지를 탐험할 거야! 공룡 탐험대, 출동!
[나레이션] Trixie가 꼬리를 흔들며 앞장서서 걸어가요. 큰 나뭇잎 사이를 지나고, 작은 시내를 건너고... 드디어 Trixie의 둥지에 도착했어요! 커다란 나뭇잎과 가지로 만든 아늑한 둥지예요.
[루나] (숨을 크게 들이쉬며) Wow... WOW! So many things! What is EVERYTHING?!
[나레이션] 둥지 안에는 둥글둥글한 알, 반짝이는 돌, 큰 나뭇잎, 나뭇가지... 신기한 것들이 가득해요!
[루나] (공룡 알을 만지며) So warm! So round! In space, everything is cold and square. This is like... a warm ball!
[포포] 하하! 루나가 공룡 알을 따뜻한 공이라고 생각하네! 캡틴, 이건 뭐라고 하는 거야?
[나레이션] Trixie가 이번엔 반짝이는 돌을 코로 굴려서 캡틴 앞에 갖다 놨어요. 자랑하고 싶은 거예요!
[루나] (돌을 보며) Ooh, shiny! Is this a space crystal?!
[포포] 아니야, 루나. 캡틴이 둥지에 있는 것들을 하나씩 알려줄 거야. 영어로는 'This is a' 다음에 물건 이름을 말하면 돼!
[포포] 포포가 먼저~ 'This is a rock!' 이렇게!
[포포] 캡틴 둥지에는 뭐가 있어? 'This is an egg' 아니면 'This is a leaf' — 'This is a...' 다음에 말해봐!""",
        "outro_narrator_script": """[포포] 캡틴! 큰일이야. Trixie가 아침에 일어났는데 다른 공룡들이 벌써 다 일어나서 밥을 먹고 있대! 공룡들의 하루를 알아봐야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W1_S4: 공룡의 하루 =====
    {
        "activity_id": "ACT_DINO_W1_S4_daily_routine",
        "curriculum_unit_id": "DINO_W1_S4_dino_day",
        "name": "공룡의 하루 알려주기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_ROUTINE", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """공룡들의 하루를 상상하며 일상 단어를 배웁니다.

포포: "공룡들은 아침에 뭘 할까? 캡틴은 아침에 뭐 해?"

간단한 3가지 루틴만:
1. 아침: wake up, eat breakfast (열매, 풀)
2. 낮: play, walk (탐험, 놀기)
3. 저녁: eat dinner, sleep (둥지로 돌아가서 잠)

각각 포포가 유도 → 아이가 한국어로 답 → 영어 단어 연결
루나가 감탄하며 따라함

패턴: "I ___ in the morning."
단어만 말해도 성공.

TPR 활동 (몸으로 표현하기):
- 포포: "공룡들은 아침에 기지개를 켜면서 '으아앙~' 하고 소리를 내! 캡틴도 같이 해볼까? 으아앙~!"
- 루나: "ROAR! Like a dinosaur! Captain, can you do it?"
- 아이가 소리를 내면 대성공! 안 해도 괜찮음.""",
        "key_expression": "I wake up. I eat. I sleep.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 Trixie의 둥지에서 알도 보고 돌도 봤잖아! 오늘은 공룡들의 하루를 알아볼 거야! 공룡 탐험대, 출동!
[나레이션] 아침 해가 떠오르자 공룡 세계가 깨어나기 시작했어요. 멀리서 긴 목 공룡이 으아앙~ 하고 하품하고, Trixie가 둥지에서 삐이익! 하고 기지개를 켜요.
[루나] (눈을 비비며) Why is it so bright? And Trixie is making sounds! Is she... waking up?
[포포] 맞아! 아침이야! 태양이 뜨면 공룡들도 일어나는 거야.
[루나] (깜짝 놀라며) Morning! Just like Earth humans! But... what do dinosaurs do in the morning? Do they eat energy capsules too?
[나레이션] Trixie가 벌떡 일어나서 풀밭으로 뛰어갔어요. 큰 나뭇잎을 물고 와서 우적우적 씹고 있어요!
[루나] Trixie is eating leaves?! For breakfast?!
[포포] (깜짝 놀라며) 하하! 공룡들은 풀이나 열매를 먹어! 캡틴, 캡틴은 아침에 뭐 해? 루나에게 알려줘!
[나레이션] Trixie가 다 먹고 나서 킁킁 캡틴 옆에 와서 눈을 반짝여요. 캡틴의 아침이 궁금한 거예요!
[포포] 아침에 뭘 하는지 알려줄까? 영어로는 'I wake up' — '나는 일어나' 라고 해. 포포가 먼저~ 'I wake up!'
[포포] 캡틴도 해볼래? 'I wake up' 아니면 'I eat breakfast' — 아침에 뭘 하는지 말해봐!""",
        "outro_narrator_script": """[나레이션] 그날 밤, 공룡 세계에서 쿵쿵쿵 이상한 소리가 들렸어요...
[포포] 이 소리... 땅속에서 뭔가 올라오고 있어! 캡틴, 다음 주에 공룡 화석을 찾아야 할지도 몰라!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S1: 화석 발굴 현장 =====
    {
        "activity_id": "ACT_DINO_W2_S1_fossil",
        "curriculum_unit_id": "DINO_W2_S1_fossil_hunt",
        "name": "화석 발굴 미션",
        "activity_type": "mission_call",
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_COMPREHENSION_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """공룡 화석 발굴 현장에서 도구와 물건 이름을 배웁니다!

포포: "비상이야! 절벽에서 신비한 공룡 화석이 발견됐대.
캡틴이 발굴 도구 이름을 알려주면 루나가 파낼 수 있어!"

물건 단어: rock, bone, egg, leaf, stick, dirt, hole, stone
하나씩 물어보며 단어를 노출합니다.

포포: "이건 뭐야? 딱딱하고 둥근 거..."
아이: "돌!"
포포: "맞아, 영어로는 rock이야!"
루나: "Rock! Let me dig here... No fossil under this rock."

물건 4~5개 확인 후 마무리.

TPR 활동: 발굴할 때 "Dig, dig, dig!" 하며 파는 동작을 유도.
포포: "캡틴, 같이 파보자! 'Dig!' 하면서 파는 거야! Dig, dig, dig!"
아이가 따라하면 칭찬. 안 해도 OK.""",
        "key_expression": "rock, bone, egg, leaf, stick",
        "intro_narrator_script": """[포포] 캡틴! 지난주에 공룡 세계에서 정말 많은 걸 배웠어! 근데 큰 발견이야... 공룡 화석을 찾아야 해! 공룡 탐험대, 출동!
[나레이션] 쿠르릉! 어젯밤에 땅이 흔들렸어요. 그런데 그 덕분에 절벽 한쪽이 무너지면서 신비한 것들이 드러났어요! 반짝이는 뼈, 거대한 이빨 자국, 동그란 알 모양의 돌...
[루나] (입이 떡 벌어지며) Popo! LOOK! Something shiny is sticking out of the ground! What IS that?!
[나레이션] 루나가 달려가서 흙을 파보려 하는데... 손으로는 안 돼요! 너무 딱딱해요.
[포포] (깜짝 놀라며) 이건... 공룡 화석이야! 땅 속에 오래오래 묻혀 있던 공룡의 뼈야!
[루나] (눈을 반짝이며) Fossil?! A real dinosaur fossil?! We need to dig it out!
[나레이션] Trixie도 신이 나서 앞발로 땅을 콩콩 치고 있어요!
[포포] 캡틴! 발굴하려면 주변 물건 이름을 알아야 해! 돌은 'rock', 뼈는 'bone', 흙은 'dirt'!
[포포] 포포가 먼저~ 'Rock!' 루나, rock 근처를 파봐!
[루나] Rock... digging! Found something!
[포포] 캡틴 차례야! 주변에 뭐가 있는 것 같아? 'Rock', 'bone', 'egg' 중에 아무거나! 아니면 다른 것도 좋아!""",
        "outro_narrator_script": """[포포] 화석 2개는 찾았는데... 마지막 뼈가 없어! 어딘가에 숨겨져 있을 텐데... 어디일까?""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S2: 공룡 알은 어디에? =====
    {
        "activity_id": "ACT_DINO_W2_S2_egg_hunt",
        "curriculum_unit_id": "DINO_W2_S2_egg_location",
        "name": "공룡 알 찾기 (in/on/under)",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """전치사 in, on, under를 배웁니다.

포포: "Trixie의 알이 바람에 굴러갔어! 어디 숨겨져 있을까?
영어로는 이렇게 말해:
- 안에 = in
- 위에 = on
- 밑에 = under"

루나가 틀리게 찾으며 웃음 유발:
"Is it ON the rock? ... No. UNDER the leaf? ... No."

아이에게 힌트 요청:
포포: "캡틴, 알이 바위 안에 있을까, 위에 있을까, 밑에 있을까?"
아이가 "밑에" → 포포: "under! It's under the rock!"

패턴: "It's in/on/under the ___."
3가지 위치만 연습합니다.""",
        "key_expression": "It's in/on/under the ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 화석을 찾았는데, 오늘은 더 중요한 미션이야! Trixie의 알을 찾아야 해! 공룡 탐험대, 출동!
[나레이션] 삐이익! 삐이익! Trixie가 슬프게 울고 있어요! 어젯밤 바람이 세게 불어서 둥지에 있던 알 세 개가 굴러가 버렸어요!
[루나] (Trixie를 쓰다듬으며) Oh no! Trixie is crying! Her eggs are lost!
[나레이션] Trixie가 눈물을 글썽이며 캡틴을 바라봐요.
[포포] 캡틴! 알을 찾아줘야 해! 근데 어디에 있는지 영어로 알려주면 루나가 바로 찾을 수 있어!
[포포] 위치를 말하는 마법 단어가 세 개 있어. 안에는 'in', 위에는 'on', 밑에는 'under'! 이거면 뭐든 찾을 수 있어!
[루나] (주변을 두리번거리며) I see rocks, leaves, trees... But where are the eggs?!
[포포] 자, 연습해볼까? 포포가 먼저~ 알이 바위 밑에 있을 것 같아! 'It's under the rock!' 이렇게!
[루나] (바위를 들어보며) Let me check... OH! Found one! It WAS under the rock!
[포포] 캡틴 차례야! 나머지 알은 어디 있을 것 같아? 'It's in the ___', 'It's on the ___', 'It's under the ___' 중에 골라서 말해봐!""",
        "outro_narrator_script": """[나레이션] Trixie가 알을 다 찾고 기뻐서 캡틴에게 뺨을 비비고 있어요!
[포포] 잠깐... 저 덤불 뒤에서 뭔가 움직이고 있어! 다음에 확인해보자!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S3: 아기 공룡 숨바꼭질 =====
    {
        "activity_id": "ACT_DINO_W2_S3_hide_seek",
        "curriculum_unit_id": "DINO_W2_S3_dino_hide_seek",
        "name": "아기 공룡 숨바꼭질",
        "activity_type": "game",
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_PRAG_GAME_RULE", "SK_VOCAB_ACTION_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """상상 속 숨바꼭질 게임입니다.

규칙: Trixie가 숨고, 캡틴이 어디에 있는지 영어로 말하면 찾은 것!

라운드 1:
포포: "Trixie가 숨었어! 어디 있을까?"
(선택지: under the leaf / in the hole / on the rock)
아이가 고르면 → Trixie 반응

라운드 2: 아이가 숨는 역할 (상상)
루나: "Where is Captain?"
아이가 "under the rock" 등으로 답하면 성공

재미 요소:
- Trixie가 꼬리가 보이는데 숨었다고 생각하는 코믹 리액션
- 루나가 엉뚱한 곳을 찾는 웃음 유발
- 공룡 흉내: "Trixie처럼 발소리 내볼까? Stomp, stomp!" TPR 활동

참고: 'behind'는 이번 주 학습 목표(in/on/under)에 포함되지 않는 보너스 단어입니다.
아이가 behind를 사용하면 칭찬하되, 적극적으로 가르치지는 마세요.
핵심 전치사 in/on/under에 집중하세요.

3라운드 정도 후 마무리.""",
        "key_expression": "under the leaf, in the hole, on the rock",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 in, on, under로 알 찾는 거 정말 잘했어! 오늘은 Trixie랑 숨바꼭질 할 거야! 공룡 탐험대, 출동!
[나레이션] 알도 다 찾았겠다, 오늘은 좀 쉬면서 놀기로 했어요! Trixie가 갑자기 신이 나서 방방 뛰어요.
[루나] (신나서) Trixie wants to play! I think she knows a game!
[나레이션] Trixie가 킥킥(삐익삐익) 웃으며 벌써 숨을 곳을 찾아 두리번거려요. 큰 나뭇잎 뒤? 바위 밑? 구덩이 안?
[포포] 오, 숨바꼭질이야! Trixie가 숨고, 캡틴이 찾는 놀이야!
[나레이션] Trixie가 쪼르르 달려가서 큰 나뭇잎 뒤에 숨으려 하는데... 꼬리가 삐죽 나와 있어요! 꼬리가 나뭇잎 밖으로 살랑살랑~
[포포] (속삭이며) 캡틴, Trixie 꼬리가 보여! 어디에 숨어있는지 영어로 말하면 찾을 수 있어!
[포포] 포포가 먼저 해볼게~ 'Trixie is behind the leaf!' 이렇게!
[포포] 캡틴도 해봐! 'Trixie is in the hole!' 아니면 'Trixie is under the rock!' Trixie가 어디에 있는 것 같아?""",
        "outro_narrator_script": """[포포] 숨바꼭질 너무 재미있었지? 근데 캡틴, 저 멀리 큰 발자국이 있어... 이건 Trixie 발자국이 아닌데? 내일 확인해봐야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S4: 탐험 보고서 =====
    {
        "activity_id": "ACT_DINO_W2_S4_report",
        "curriculum_unit_id": "DINO_W2_S4_expedition_report",
        "name": "탐험 보고서",
        "activity_type": "review",
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """W2 총정리. 공룡 세계 물건 + 전치사를 조합해서 보고합니다.

포포: "캡틴, 이번 주 탐험 최종 보고를 해볼까?
뭘 찾았는지, 어디서 찾았는지 알려줘!"

아이에게 2~3개 문장 유도:
"The egg is under the rock."
"The bone is in the dirt."

아이가 한국어로 말해도 포포가 영어 문장으로 변환.
루나가 감사: "Thank you, Captain Explorer!"

마지막에 W2 미션 완료 축하.""",
        "key_expression": "The ___ is in/on/under the ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 숨바꼭질도 하고, 큰 발자국도 봤지? 오늘은 최종 탐험 보고서를 작성할 거야! 공룡 탐험대, 출동!
[나레이션] 드디어 이번 주 탐험의 마무리예요! Trixie가 캡틴 앞에 엎드리며 등에 타라는 듯 꼬리를 흔들어요. 캡틴과 루나가 Trixie 등에 올라타자, Trixie가 절벽 위 전망대로 데려가요!
[나레이션] 와! 높은 곳에서 보니 이번 주에 탐험한 곳이 다 보여요. 화석 발굴 현장, Trixie 알이 숨겨져 있던 바위들, 숨바꼭질하던 나뭇잎 숲...
[포포] (공룡 세계 지도를 펼치며) 캡틴, 이번 주 탐험한 곳에 별 스티커를 붙이자! 근데 먼저 '공룡 탐험 최종 보고서'를 작성해야 해.
[루나] (탐험 일지를 펼치며) I've been recording everything! Captain found eggs, bones, rocks... Let me write the final report!
[나레이션] Trixie가 옆에서 두근두근 기다리고 있어요. 꼬리를 흔들며 캡틴을 바라보고 있어요.
[포포] 자, 이번 주에 뭘 찾았는지, 그게 어디에 있었는지 보고해줘!
[포포] 영어로 보고하는 방법은 이거야! 포포가 먼저~ 'The egg is under the rock!' — 알이 바위 밑에 있다! 이렇게 물건 이름이랑 위치를 같이 말하면 돼.
[포포] 캡틴 차례! 'The bone is in the dirt' 아니면 'The egg is on the leaf' — 뭘 어디서 찾았는지 말해봐!""",
        "outro_narrator_script": """[나레이션] Trixie가 캡틴에게 뺨을 비비며 기뻐해요. 알도 찾고, 화석도 찾고, 최고의 탐험이었어요!
[포포] 근데 캡틴... 다음 주에는 공룡 세계에서 더 신기한 일이 벌어질 것 같아!""",
        "estimated_duration_minutes": 5,
    },

    # ===== W3_S1: 공룡도 감정이 있대! =====
    {
        "activity_id": "ACT_DINO_W3_S1_feelings",
        "curriculum_unit_id": "DINO_W3_S1_dino_feelings",
        "name": "공룡 감정 읽기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_EMOTION_BASIC", "SK_COMPREHENSION_BASIC", "SK_PRAG_EMOTION_EXP"],
        "instructions_for_ai": TRIXIE_GUIDE + """공룡들의 감정을 읽는 미션입니다.

포포: "공룡들도 감정이 있대! Trixie의 표정을 보고 어떤 기분인지 알려줘."

감정 5개를 하나씩 소개:
happy — 기분 좋다 (Trixie가 꼬리 흔들 때)
sad — 슬프다 (Trixie가 고개 숙일 때)
angry — 화난다 (큰 공룡이 으르렁할 때)
scared — 무섭다 (천둥이 칠 때)
tired — 피곤하다 (Trixie가 하품할 때)

각 감정에 대해:
1. 포포가 한국어로 설명
2. 영어 단어 알려줌
3. 루나가 따라함
4. 아이에게 따라하도록 유도 (안 해도 OK)

마지막에 "지금 기분" 물어보기:
포포: "캡틴은 지금 이 중에 어떤 기분이야?"
아이가 고르면 → "I am ___." 패턴 노출""",
        "key_expression": "happy, sad, angry, scared, tired / I am ___.",
        "intro_narrator_script": """[포포] 캡틴! 공룡 알도 찾고, 보고서도 썼고, 지도 스티커도 2개나 붙였어! 오늘은 공룡들의 감정을 배울 거야! 공룡 탐험대, 출동!
[나레이션] 오늘 아침, 포포의 레이더에서 새로운 기능이 켜졌어요! 삐비빅! 화면에 '공룡 감정 스캐너' 라고 떠요!
[포포] (레이더를 보며 깜짝 놀라) 세상에! 공룡 감정 스캐너가 활성화됐어! 이걸로 공룡의 기분을 읽을 수 있어!
[나레이션] 그런데 Trixie에게 이상한 일이 생겼어요. 평소에 밝던 Trixie가 갑자기 고개를 떨구고 삐이익... 작은 소리를 내고 있어요. 포포의 스캐너에 파란 물방울 모양이 떠올랐어요!
[루나] (걱정하며) Popo! The scanner shows a blue drop! And Trixie looks... different today. What does it mean?
[포포] (달려와서 살펴보며) 파란 물방울은... 슬픔이야! Trixie가 슬픈 거야! 영어로는 'sad'.
[나레이션] 그런데 갑자기 Trixie의 엄마 공룡이 나타났어요! 큰 트리케라톱스가 쿵쿵쿵 걸어오더니 Trixie를 코로 쓱~ 안아줬어요. 그러자 Trixie가 꼬리를 흔들기 시작했어요!
[루나] (깜짝 놀라며) Oh! Trixie is moving her tail again! And her eyes are bright! What happened?
[포포] 이제 기분이 좋아진 거야! 'happy'! 엄마가 와서 기분이 좋아진 거지.
[포포] 캡틴, 공룡 감정을 알려주자. 기분 좋을 때는 'happy', 슬플 때는 'sad', 화날 때는 'angry'!
[포포] 포포가 먼저~ 포포는 지금 기분이 좋아! 'I am happy!' 이렇게!
[루나] (따라하며) I am... hap-py?
[포포] 잘했어! 캡틴은 지금 기분이 어때? 'I am happy', 'I am sad', 'I am tired' 중에 하나 골라서 말해봐!""",
        "outro_narrator_script": """[포포] Trixie가 다른 아기 공룡 무리를 발견했어! 근데... 어떻게 인사해야 할지 모르는 것 같아. 다음에 캡틴이 도와줘!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W3_S2: 공룡 무리와 친구 =====
    {
        "activity_id": "ACT_DINO_W3_S2_dino_friends",
        "curriculum_unit_id": "DINO_W3_S2_dino_friends",
        "name": "공룡 친구 사귀기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_PRAG_SOCIAL_TALK", "SK_VOCAB_SOCIAL_TRAIT", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """Trixie가 다른 아기 공룡들과 친구가 되는 것을 도와줍니다.

루나: "Trixie found other baby dinosaurs! But she doesn't know how to say 'friend'."

중요 안전 규칙:
- 친구가 없어도 완전 괜찮다고 먼저 말해줌
- 이름 대신 "A 친구" 코드네임 사용 가능
- 친구 없으면 Trixie/루나/포포가 "탐험대 친구 1호, 2호" 해줌

친구가 있는 경우:
포포: "그 친구는 어떤 사람이야? 같이 노는 사람? 웃긴 사람?"
→ play, help, funny 등 영어 단어 연결

패턴: "I have a friend." / "Trixie is my friend."
"I play with my friend."

말하기 싫으면 "패스" 존중.""",
        "key_expression": "I have a friend. / I play with my friend.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 happy, sad, angry, scared... 공룡 감정을 배웠어! 오늘은 공룡 친구를 사귀는 법을 알려줄 거야! 공룡 탐험대, 출동!
[나레이션] Trixie가 오늘은 뭔가 특별한 걸 발견했어요. 저 언덕 너머에서 다른 아기 공룡들이 같이 놀고 있거든요! 긴 목의 아기 브라키오사우루스, 등에 뾰족한 판이 달린 아기 스테고사우루스, 빠르게 달리는 작은 벨로시랩터... 다같이 뛰어놀고 있어요! 하늘에서는 프테라노돈이 빙글빙글 날고 있어요.
[루나] (가리키며) Look! Little dinosaurs! They are playing together! Trixie, do you want to play with them?
[나레이션] Trixie가 가고 싶은데 주저하고 있어요. 발을 동동 구르면서도 한 발짝도 못 나가요.
[포포] Trixie가 무리에 끼고 싶은데 어떻게 해야 할지 모르는 거야. '친구'라는 개념을 모르니까!
[루나] (고개를 갸우뚱하며) Friend? In space, I was always alone too. Popo was with me, but... Is Popo my friend?
[포포] (살짝 감동하며) 물론이지! 포포도 친구, 루나도 친구, 캡틴도 친구, 그리고 Trixie도 친구야!
[루나] (눈이 반짝이며) We are ALL friends?! Really?!
[포포] 물론이지! 친구는 같이 놀고, 같이 웃고, 힘들 때 도와주는 사람이야. 포포가 먼저~ 'I have a friend! Trixie is my friend!' 이렇게!
[포포] 캡틴도 해볼래? 'I have a friend' 아니면 'Trixie is my friend' — 둘 중에 하나 말해봐!""",
        "outro_narrator_script": """[루나] Captain, Trixie made new friends! But... the big dinosaur over there looks angry. What do we do?
[포포] 좋은 질문이야. 다음에 캡틴이 알려줄 거야!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W3_S3: 열매 나누기 =====
    {
        "activity_id": "ACT_DINO_W3_S3_share_game",
        "curriculum_unit_id": "DINO_W3_S3_share_berries",
        "name": "열매 나누기 게임",
        "activity_type": "game",
        "target_skills": ["SK_PRAG_TURN_TAKING", "SK_PRAG_SHARING", "SK_PRAG_POLITE_REQUEST"],
        "instructions_for_ai": TRIXIE_GUIDE + """순서 지키기(turn)와 나누기(share) 개념을 배웁니다.

Trixie가 일부러 규칙을 몰라서 틀리는 역할:
Trixie가 열매를 다 자기가 먹으려 함
포포: "Trixie가 열매를 다 혼자 먹으려 하는데, 이거 괜찮을까?"

미니 턴 게임:
포포: "지금은 캡틴 턴이야. 영어로 'It's my turn.'이라고 할 수 있어."

나누기 개념:
포포: "열매가 세 개인데 셋이 먹고 싶으면? 'Let's share.'"

정중한 요청:
"My turn, please." / "Can I have one, please?"

3가지 표현 중 하나만 성공해도 OK.""",
        "key_expression": "It's my turn. / Let's share. / My turn, please.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 공룡 친구를 사귀었어! 근데 친구끼리 나눠 먹는 법을 배워야 해! 공룡 탐험대, 출동!
[나레이션] 오늘 공룡 세계의 큰 나무에 맛있는 열매가 잔뜩 열렸어요! 빨갛고, 노랗고, 보라색... 알록달록한 열매들!
[나레이션] 그런데 Trixie가 열매를 다 자기 앞에 쓸어 모으고 있어요! 하나, 둘, 셋, 넷, 다섯... 전부 자기 거래요!
[루나] (깜짝 놀라며) Trixie! You took ALL the berries! But... I want some too!
[나레이션] Trixie가 열매를 꼭 안고 아무에게도 안 주려고 해요. 공룡은 원래 혼자 먹으니까 '나누기'를 모르는 거예요.
[포포] (걱정스러운 표정으로) 캡틴... Trixie가 나누는 법을 모르네! 같이 먹으면 더 맛있다는 걸 알려줘야 해.
[루나] (손을 내밀며) Trixie, can I have one? Please?
[나레이션] 포포가 열매를 하나 들어올렸어요. Trixie가 "그건 내 거!" 하고 뺏으려 해요.
[포포] 이럴 때 영어로 이렇게 말해. 내 차례라고 할 때는 'It's my turn!', 같이 나눠 먹자고 할 때는 'Let's share!'
[포포] 포포가 먼저~ (열매를 하나 들고) 'It's my turn!' 이렇게! 그리고 Trixie한테 'Let's share!' 짠!
[포포] 캡틴도 해볼까? 'It's my turn!'이라고 말해봐! 아니면 Trixie한테 'Let's share!'라고 해줘도 좋아!""",
        "outro_narrator_script": """[나레이션] Trixie가 열매를 나눠주며 삐이익! 기뻐했어요! 나누면 더 맛있다는 걸 알게 된 거예요.
[포포] 캡틴, 근데 저 큰 공룡이 또 으르렁거리고 있어... 다음에 용감하게 대처하는 법을 배우자!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W3_S4: 용감한 탐험가 =====
    {
        "activity_id": "ACT_DINO_W3_S4_brave",
        "curriculum_unit_id": "DINO_W3_S4_brave_explorer",
        "name": "용감한 탐험가",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_EXPRESSIVE_NEGATIVE_EMOTION", "SK_PRAG_SET_BOUNDARY", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """가벼운 무서운 상황을 상상 속에서 다룹니다.

중요: 진짜 트라우마를 캐지 않음. 전부 "상상 예시"로 진행.

상황: 큰 티라노사우루스가 멀리서 으르렁거림 (위험하지 않지만 무서움)
포포: "캡틴, 무서워도 괜찮아. 무서울 때는 어떻게 말하는지 알려줄게."

감정 단어 연결:
- 무서움 → scared
- 속상 → sad / upset
- 괜찮음 → okay

패턴: "I feel scared." / "I feel brave."

경계 표현:
포포: "싫은 행동을 멈춰달라고 할 때? 'Stop, please.'"

용기를 낸 후: "I feel brave." / "I feel better."

오늘의 안전 장치를 특히 강조:
"말하기 힘들면 '패스'라고 해줘. 캡틴 마음이 제일 중요해." """,
        "key_expression": "I feel scared. / Stop, please. / I feel brave.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 share도 배우고 turn도 배웠어! 오늘은 무서울 때 어떻게 말하는지 배울 거야. 공룡 탐험대, 출동!
[나레이션] 오늘은 좀 어두운 숲을 지나가야 해요. 나뭇잎 사이로 햇빛이 조금만 들어와요. 그런데...
[나레이션] 쿵... 쿵... 쿵... 멀리서 무거운 발소리가 들려요. 나무가 흔들리고, 새들이 푸드덕 날아가요.
[루나] (떨리는 목소리로) P-Popo... what is that sound? Something BIG is coming!
[나레이션] 나무 사이로 커다란 그림자가 보였어요. 큰 머리, 작은 앞발... 티라노사우루스예요! 하지만 아주 멀리 있으니까 위험하지는 않아요.
[나레이션] Trixie가 재빨리 캡틴 뒤에 숨으며 꼬리로 캡틴의 다리를 살살 감쌌어요. 그리고 포포가 바로 캡틴과 루나 앞에 서서 팔을 벌렸어요.
[포포] (차분하고 단단한 목소리로) 캡틴, 괜찮아. 포포가 여기 있잖아. 티라노사우루스는 우리를 안 봤어. 아주 멀리서 지나가고 있을 뿐이야. 우리는 안전해.
[루나] (Trixie를 쓰다듬으며) It's okay, Trixie. We are safe. Captain is here. But... I feel something inside. My heart is going fast! What is this feeling?
[포포] (부드러운 목소리로) 그건 '무서움'이야. 영어로 'scared'. 무서울 때 느끼는 마음이야. 무서워도 괜찮아! 용감한 건 안 무서운 게 아니라, 무서워도 앞으로 가는 거야!
[포포] 슬플 때는 'I feel sad', 무서울 때는 'I feel scared'. 그리고 싫은 걸 멈춰달라고 할 때는 'Stop, please!'
[포포] 포포가 먼저~ 저 큰 공룡이 좀 무서워... 'I feel scared!' 이렇게!
[루나] (따라하며) I feel... scared...
[포포] 잘했어! 캡틴도 해볼까? 큰 공룡을 보면 어떤 기분이야? 'I feel scared', 'I feel brave' 중에 골라서 말해봐!""",
        "outro_narrator_script": """[나레이션] 티라노사우루스가 멀리 지나가고, 다시 평화로운 숲이 됐어요. Trixie가 캡틴에게 고마운 듯 뺨을 비비고 있어요.
[포포] 캡틴이 정말 용감했어! 다음 주에는 진짜 탐험 장비를 갖추고 더 멋진 모험을 할 거야!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S1: 탐험 장비 고르기 =====
    {
        "activity_id": "ACT_DINO_W4_S1_gear_choice",
        "curriculum_unit_id": "DINO_W4_S1_explorer_gear",
        "name": "탐험 장비 코디",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """탐험 장비를 골라 루나를 꾸며주는 미션입니다.

포포: "본격 탐험을 하려면 장비가 필요해! 캡틴이 골라줘!"

장비 단어: hat, vest, boots, gloves, pants, shirt
색깔: red, blue, yellow, green, brown

순서:
1. 장비 종류 하나씩 보여주며 색깔 선택 유도
2. 포포: "빨간 모자, 파란 모자 중에 뭐가 멋져 보여?"
3. 아이가 고르면 → "I like the red hat." 패턴 노출
4. 루나: "I like the red hat! Like a real explorer!"

2~3개 아이템 코디 후 최종 요약.
아이가 단어만 말해도 partial 성공.""",
        "key_expression": "I like the ___ ___.",
        "intro_narrator_script": """[포포] 캡틴! 이번 주 탐험은 정말 특별해! 진짜 탐험 장비를 갖출 거야! 공룡 탐험대, 출동!
[나레이션] 오늘은 포포가 시간 포털에서 특별한 상자를 하나 꺼냈어요. 상자를 열자... 와아! 알록달록한 탐험 장비가 가득해요!
[루나] (눈이 휘둥그레) SO many things! Hats, vests, boots... What are these?!
[포포] 이건 탐험 장비야! 공룡 세계를 안전하게 탐험하려면 이걸 입어야 해!
[나레이션] 루나가 탐험 모자를 들어봐요. 빨간 거, 파란 거, 초록 거... Trixie가 모자 냄새를 맡으며 킁킁거려요.
[루나] (모자를 머리에 올려보며) Look at me! Am I an explorer now? Like the dinosaur hunters?
[포포] 아직! 캡틴이 골라줘야 제대로 된 탐험가가 되지. 색깔이랑 장비 이름을 같이 말하면 돼!
[포포] 포포가 먼저~ 'I like the brown hat!' 갈색 모자 어때? 이렇게!
[루나] (기대하며) Captain! Pick for me, please!
[포포] 캡틴 차례! 'I like the red hat!' 아니면 'I like the blue vest!' 루나에게 어떤 장비가 좋은지 말해봐!""",
        "outro_narrator_script": """[루나] (장비를 보며) Captain! Do I look like a real explorer now?
[포포] 거의 완벽한데... 장비를 입는 법을 배워야 해! 내일 마무리하자!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S2: 장비 입기! =====
    {
        "activity_id": "ACT_DINO_W4_S2_gear_up",
        "curriculum_unit_id": "DINO_W4_S2_gear_up",
        "name": "장비 입고 벗기 연습",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_ACTION_VERB_CLOTHES", "SK_VOCAB_CLOTHES_BASIC", "SK_PRAG_CONTEXT_APPROPRIATE"],
        "instructions_for_ai": TRIXIE_GUIDE + """put on / take off 동사를 배웁니다.

포포: "입을 땐 put on, 벗을 땐 take off."
루나: "P.u.t.. o.n.. hat. Is this right, Captain?"

탐험 상황:
- 숲 속 탐험: "Put on your hat." (해가 뜨거움)
- 강을 건넌 후: "Take off your boots." (젖어서)
- 덤불을 지날 때: "Put on your gloves." (가시가 있어서)

루나가 일부러 틀리는 미니게임:
루나: "It is very hot. I put on my coat!"
포포: "어? 이거 맞을까? 캡틴이 루나에게 알려줘!"
아이: "Take off your coat!" (또는 "take off"만 해도 OK)

3~4개 상황 후 마무리.""",
        "key_expression": "Put on your ___. / Take off your ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 멋진 장비를 골랐어! 오늘은 입고 벗는 법을 배울 거야! 공룡 탐험대, 출동!
[나레이션] 오늘은 본격적인 탐험이에요! 숲을 지나고, 강을 건너고, 언덕을 넘어야 해요.
[포포] (하늘을 보며) 오늘 해가 뜨겁네! 모자를 써야 해.
[나레이션] 루나가 장비 앞에서 멈칫했어요. 어떻게 입는 거지?
[루나] (부츠를 머리에 올리며) Like this? Boots go on my head?
[포포] (깜짝 놀라며) 하하하! 아니야! 부츠는 발에 신는 거야!
[루나] (장갑을 발에 끼며) Then... gloves go on my feet? Like dinosaur claws?
[포포] (웃다가 멈추며) 캡틴, 루나가 장비 입는 법을 전혀 모르네! 우주에서는 장비를 안 입었으니까.
[나레이션] Trixie가 루나를 보며 고개를 갸웃거려요. 공룡은 옷을 안 입으니까 이해가 안 되나 봐요!
[포포] 캡틴, 도와줘! 입을 때는 'put on', 벗을 때는 'take off'야. 포포가 먼저~ 해가 뜨거우니까 'Put on your hat!' 이렇게!
[루나] (따라하며) Put on... my hat?
[포포] 잘했어! 캡틴도 해볼래? 'Put on your hat' 아니면 'Put on your boots' — 루나에게 뭘 입으라고 말해봐!""",
        "outro_narrator_script": """[나레이션] 갑자기 비가 오기 시작했어요! Trixie가 나뭇잎 밑으로 쏙 숨어요.
[포포] 비다! 다음에는 날씨에 맞게 장비 입는 법을 완벽하게 연습해야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S3: 나만의 탐험 스타일 =====
    {
        "activity_id": "ACT_DINO_W4_S3_my_style",
        "curriculum_unit_id": "DINO_W4_S3_my_explorer_style",
        "name": "나만의 탐험 스타일",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_PRAG_DESCRIPTION_BASIC"],
        "instructions_for_ai": TRIXIE_GUIDE + """아이가 자기만의 탐험 스타일을 소개합니다.

포포: "캡틴은 어떤 탐험 장비를 제일 좋아해? 모자, 조끼, 부츠?"

한국어 → 영어 매핑:
- 모자 → hat
- 조끼 → vest
- 부츠 → boots
- 바지 → pants
- 장갑 → gloves

패턴 1: "This is my ___."
패턴 2: "I like my brown boots." (색깔 포함)

프라이버시: 상상의 장비든 진짜 옷이든 자유.

루나: "I like my brown boots too! Explorer twins!"
포포 정리: "루나가 캡틴의 탐험 스타일을 기억할 거야~" """,
        "key_expression": "This is my ___. / I like my ___ ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 put on, take off 정말 잘 했어! 오늘은 캡틴만의 탐험 스타일을 알려줄 거야! 공룡 탐험대, 출동!
[나레이션] 루나가 장비를 다 갖춰 입고 거울 같은 호수 앞에 서 있어요. 물에 비친 자기 모습을 보며 빙글빙글 돌아요.
[루나] (호수를 보며 빙글빙글) Look at me! Brown hat, green vest, big boots! Am I a real explorer?
[포포] (엄지를 척 올리며) 완벽해, 루나! 진짜 탐험가 같아!
[루나] (갑자기 캡틴을 바라보며) But Captain... what is YOUR explorer style? I want to know!
[나레이션] 루나의 눈이 반짝반짝 빛나요. 캡틴처럼 멋진 탐험가가 되고 싶은 거예요!
[포포] 좋은 생각이야! 캡틴, 제일 좋아하는 탐험 장비가 뭐야? 모자? 조끼? 부츠?
[루나] (기대하며) Yes yes! Tell me! I want to be like Captain!
[포포] 포포가 먼저~ 포포는 빨간 벨트가 좋아! 'I like my red belt!' 이렇게! 색깔이랑 장비 이름을 같이 말하면 돼!
[포포] 캡틴 차례야! 캡틴은 어떤 장비를 좋아해? 'I like my brown hat!' 아니면 'I like my blue boots!' 이렇게 말해봐!""",
        "outro_narrator_script": """[포포] 캡틴, 내일이 마지막 미션이야. 공룡 세계에서의 마지막 대탐험! Trixie도 우리와 함께 갈 거야. 최고의 탐험이 될 거야!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S4: 최종 탐험 & 배지 =====
    {
        "activity_id": "ACT_DINO_W4_S4_final_mission",
        "curriculum_unit_id": "DINO_W4_S4_final_expedition",
        "name": "최종 탐험 미션 & 배지",
        "activity_type": "review",
        "target_skills": ["SK_PRAG_SELF_INTRO", "SK_VOCAB_CLOTHES_BASIC", "SK_DISCOURSE_MINI_SEQUENCE"],
        "instructions_for_ai": TRIXIE_GUIDE + """W1-W4 총정리 미션입니다.

포포: "오늘은 공룡 탐험대 마지막 미션이야. 캡틴이 없었으면 여기까지 못 왔을 거야."

미니 롤플레이: 새로 만난 공룡에게 자기소개
포포가 scaffold:
1. "이름이 뭐예요?" → "My name is ___."
2. "몇 살이에요?" → "I am seven."
3. "이 장비 마음에 들어?" → "I like my ___."

루나가 틀린 장비 수정 미니게임 (1회):
루나가 뜨거운 날 두꺼운 조끼 입음 → 아이: "Take off your vest!"

배지 수여:
포포: "캡틴은 공룡 탐험대 1단계 미션을 모두 완료했어!
'Dino Explorer Level 1' 배지를 줄게!"
루나: "You are Dino Explorer Level 1. Thank you for helping Trixie. She loves you."

평가 아닌 축하에 초점. 아이가 가능한 만큼만 영어로.
전혀 못 해도 포포가 대신 말해주고 "Yes/No" 정도만 반응해도 성공.""",
        "key_expression": "My name is ___. I am ___. I like my ___.",
        "intro_narrator_script": """[포포] 캡틴! 드디어 마지막 미션이야! 4주간 정말 대단했어! 오늘은 최종 탐험과 탐험대장 배지 수여식이야! 공룡 탐험대, 출동!
[나레이션] 드디어 그 날이 왔어요! 오늘은 공룡 세계의 가장 아름다운 곳, '하늘빛 계곡'으로 가는 날이에요. 거기에는 아직 아무도 만나보지 못한 새로운 공룡이 살고 있대요!
[루나] (떨리는 목소리로) Captain... I'm a little scared. What if the new dinosaur doesn't like us?
[나레이션] Trixie가 캡틴 옆에 바짝 붙어서 꼬리로 캡틴의 다리를 살살 감싸요. 걱정하지 말라는 거예요.
[포포] (루나의 손을 꼭 잡으며) 괜찮아! 캡틴이 4주 동안 배운 거 기억하지? 인사하는 법, 좋아하는 것 말하는 법, 감정 표현하는 법, 장비 이름까지! 다 할 수 있어!
[루나] (용기를 내며) You're right... Captain taught me so much. My name is Luna. I am happy. I like my blue... blue... um...
[나레이션] 루나가 갑자기 멈추고 말았어요. 긴장해서 단어가 기억이 안 나나 봐요!
[루나] (캡틴을 바라보며) Captain! What was it? The thing I'm wearing? Help me!
[포포] 캡틴, 루나가 긴장해서 단어를 잊어버렸어! 루나가 입고 있는 건... 'jacket'일까, 'helmet'일까? 캡틴이 알려줘!
[나레이션] 하늘빛 계곡에서 부드러운 울음소리가 들려요. 새로운 공룡 친구가 기다리고 있어요!
[포포] 자, 마지막 미션이야! 새로운 공룡에게 인사해야 해. 캡틴이 도와줄 거야!
[포포] 포포가 먼저~ '이름이 뭐예요?' 하면 'My name is Popo!' 이렇게!
[루나] (따라하며) My name is Luna!
[포포] 잘했어! 캡틴도 해볼까? 'My name is {child_name}' 아니면 'Hello, my name is {child_name}' — 둘 중에 하나 말해봐!""",
        "outro_narrator_script": """[나레이션] Trixie가 캡틴에게 달려와서 뺨을 비비고 있어요. 삐이익! 삐이익! '고마워, 사랑해' 라는 뜻이에요.
[나레이션] 그때, Trixie의 엄마 공룡이 쿵쿵쿵 걸어왔어요. Trixie가 엄마한테 달려가서 품에 쏙 안겼어요. 엄마 공룡이 캡틴에게 고개를 끄덕여요. '고마워요' 라는 뜻이에요.
[나레이션] Trixie가 다시 캡틴한테 뛰어오더니, 반짝이는 작은 공룡 알 하나를 코로 굴려서 캡틴 앞에 놓았어요!
[포포] (감동하며) Trixie가 캡틴에게 선물을 줬어! 이건 '우정의 알'이야. 이걸 가지고 있으면 언제든 다시 공룡 세계에 올 수 있대!
[루나] (눈물을 글썽이며) Captain... {child_name}... you are the best explorer I've ever met. Trixie will always remember you. And we can come back anytime!
[포포] 공룡 탐험대 Level 1 미션 완료! 공룡 세계 지도도 완성! 근데 캡틴... 시간 포털에서 또 새로운 신호가 잡혔어. 다음 모험이 벌써 기다리고 있어!""",
        "estimated_duration_minutes": 10,
    },
]


async def seed_curriculum():
    """Seed Dinosaur Expedition W1-W4 curriculum units and activities."""

    # Pre-seed validation
    print_validation_report(ACTIVITIES)

    print(f"\nSeeding {len(CURRICULUM_UNITS)} curriculum units and {len(ACTIVITIES)} activities (Dino Expedition)...")

    async with async_session_maker() as session:
        # 1. Seed Units
        for unit_data in CURRICULUM_UNITS:
            unit_data.setdefault("story_theme", "dino_expedition")
            unit_id = unit_data["curriculum_unit_id"]
            stmt = select(CurriculumUnit).where(CurriculumUnit.curriculum_unit_id == unit_id)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
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
        print(f"\nDino Expedition seed complete! ({len(CURRICULUM_UNITS)} units, {len(ACTIVITIES)} activities)")


if __name__ == "__main__":
    asyncio.run(seed_curriculum())
