"""
K-Pop Demon Hunters Curriculum Seed — W1-W4 (밤토리 Phase 1, Story Variant B)

Story Theme: 케이팝 데몬 헌터스 (K-Pop Demon Hunters)
- Captain (아이): 아이돌이 꿈인 아이. 음악의 별을 지키는 케이팝 데몬 헌터스의 리더.
- Luna (루나): 우주 음악 행성 'Melodia'에서 온 수습 아이돌. 영어만 사용.
  지구의 음악과 춤을 배우고 싶어하지만, 모든 것이 서툴고 귀여운 실수를 함.
- Popo (포포): 전설의 프로듀서 겸 비밀 요원. 한국어+영어 코칭 역할 동일.
  과거에 유명 아이돌 그룹을 육성한 적 있다는 비밀이 있음.

Villain: 노이즈 데몬 — 음악의 별에서 하모니를 훔치는 존재.
  무서운 존재가 아니라, 엉뚱하고 장난스러운 방해꾼.

Educational goals & key_expressions: 기존 Earth Crew 스토리와 동일.
포포와 루나의 발화 역할(코칭/안전버퍼/한영브릿지)도 동일.

Usage:
    python scripts/seed_curriculum_kpop.py
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
# Same IDs with "_kpop" suffix to allow coexistence with original story
# --------------------------------------------------------------------------

CURRICULUM_UNITS = [
    # Week 1: Star Debut — 자기소개
    {
        "curriculum_unit_id": "KPOP_W1_S1_meet_luna_popo",
        "title": "루나와 포포 만나기 — 스타 데뷔",
        "description": "멜로디아 행성에서 온 루나에게 이름과 나이를 영어로 소개해봐요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 70,
        "target_skills": ["SK_VOCAB_DAILY_GREET", "SK_SENTENCE_BASIC", "SK_PRAG_SELF_INTRO"],
    },
    {
        "curriculum_unit_id": "KPOP_W1_S2_likes_dislikes",
        "title": "좋아하는 것과 싫어하는 것 — 팬미팅",
        "description": "루나에게 좋아하는 음식, 동물, 색깔을 가르쳐줘요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 65,
        "target_skills": ["SK_VOCAB_DAILY_FOOD", "SK_SENTENCE_BASIC", "SK_PRAG_PREFERENCE"],
    },
    {
        "curriculum_unit_id": "KPOP_W1_S3_my_room_home",
        "title": "내 방과 우리 집 — 연습실 꾸미기",
        "description": "내 방(연습실)에 뭐가 있는지 루나에게 보여줘요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_DAILY_ROOM", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "KPOP_W1_S4_my_day_routine",
        "title": "나의 하루 — 아이돌의 일과",
        "description": "아침부터 저녁까지, 루나에게 지구 아이돌의 하루를 알려줘요.",
        "week": 1, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_DAILY_ROUTINE", "SK_SENTENCE_BASIC"],
    },

    # Week 2: Harmony Quest — 방 탐험 & 전치사
    {
        "curriculum_unit_id": "KPOP_W2_S1_room_objects",
        "title": "방 안의 물건들 — 잃어버린 음표 찾기",
        "description": "노이즈 데몬이 훔쳐간 음표를 찾으며 방 안 물건 이름을 배워요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "KPOP_W2_S2_prepositions",
        "title": "어디에 있을까? — 음표 추적",
        "description": "in, on, under를 사용해서 음표가 어디 있는지 말해봐요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 55,
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "KPOP_W2_S3_hide_and_seek",
        "title": "숨바꼭질 게임 — 노이즈 데몬 잡기",
        "description": "숨어있는 노이즈 데몬을 찾으며 전치사를 연습해요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 50,
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_PRAG_GAME_RULE", "SK_VOCAB_ACTION_BASIC"],
    },
    {
        "curriculum_unit_id": "KPOP_W2_S4_room_check_report",
        "title": "방 점검 보고서 — 미션 리포트",
        "description": "W2에서 배운 것을 종합해서 프로듀서 포포에게 보고해요.",
        "week": 2, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 50,
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
    },

    # Week 3: Heart Beat — 감정 & 팀워크
    {
        "curriculum_unit_id": "KPOP_W3_S1_basic_feelings",
        "title": "기본 감정 단어 — 무대 위의 감정",
        "description": "happy, sad, angry, scared, tired — 루나에게 무대 위의 감정을 가르쳐줘요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 65,
        "target_skills": ["SK_VOCAB_EMOTION_BASIC", "SK_SENTENCE_BASIC", "SK_PRAG_EMOTION_EXP"],
    },
    {
        "curriculum_unit_id": "KPOP_W3_S2_friends_people",
        "title": "내 친구와 주변 사람들 — 팀 멤버 소개",
        "description": "팀 멤버가 뭔지, 어떤 사람인지 루나에게 알려줘요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_SOCIAL_TRAIT", "SK_PRAG_SOCIAL_TALK", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "KPOP_W3_S3_sharing_turn_taking",
        "title": "나누기와 순서 지키기 — 합동 연습",
        "description": "share, turn — 합동 연습에서 필요한 규칙을 루나에게 가르쳐줘요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_PRAG_TURN_TAKING", "SK_PRAG_SHARING", "SK_PRAG_POLITE_REQUEST"],
    },
    {
        "curriculum_unit_id": "KPOP_W3_S4_small_problems_feelings",
        "title": "작은 문제와 감정 말하기 — 무대 뒤 이야기",
        "description": "속상할 때 'I feel sad', 싫을 때 'Stop, please' 말하는 법을 배워요.",
        "week": 3, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_EXPRESSIVE_NEGATIVE_EMOTION", "SK_PRAG_SET_BOUNDARY", "SK_SENTENCE_BASIC"],
    },

    # Week 4: Grand Stage — 무대 의상 & 최종 공연
    {
        "curriculum_unit_id": "KPOP_W4_S1_luna_clothes_colors",
        "title": "루나에게 옷 입혀주기 — 스테이지 의상",
        "description": "shirt, dress, pants — 색깔과 옷 이름을 배우며 무대 의상을 꾸며줘요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 1, "korean_ratio": 60,
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_SENTENCE_BASIC"],
    },
    {
        "curriculum_unit_id": "KPOP_W4_S2_put_on_take_off",
        "title": "입기와 벗기 — 의상 리허설",
        "description": "put on, take off — 무대 리허설에서 의상 갈아입는 법을 가르쳐줘요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_VOCAB_ACTION_VERB_CLOTHES", "SK_VOCAB_CLOTHES_BASIC", "SK_PRAG_CONTEXT_APPROPRIATE"],
    },
    {
        "curriculum_unit_id": "KPOP_W4_S3_my_clothes_style",
        "title": "내 옷과 스타일 — 나만의 스타일",
        "description": "내가 좋아하는 스타일을 루나에게 소개해요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 55,
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_PRAG_DESCRIPTION_BASIC"],
    },
    {
        "curriculum_unit_id": "KPOP_W4_S4_final_disguise_badge",
        "title": "최종 무대 & 배지 수여 — 그랜드 데뷔",
        "description": "W1-W4 총정리! 자기소개 + 스타일 소개를 하고 K-Pop Hunter Lv.1 배지를 받아요.",
        "week": 4, "phase": 1, "age_min": 5, "age_max": 8,
        "difficulty_level": 2, "korean_ratio": 50,
        "target_skills": ["SK_PRAG_SELF_INTRO", "SK_VOCAB_CLOTHES_BASIC", "SK_DISCOURSE_MINI_SEQUENCE"],
    },
]

# --------------------------------------------------------------------------
# Activities — K-Pop Demon Hunters Story
# --------------------------------------------------------------------------

ACTIVITIES = [
    # ===== W1_S1: Meet Luna & Popo — Star Debut =====
    {
        "activity_id": "KPOP_ACT_W1_S1_mission_start",
        "curriculum_unit_id": "KPOP_W1_S1_meet_luna_popo",
        "name": "미션 콜: 케이팝 데몬 헌터스 결성",
        "activity_type": "mission_call",
        "target_skills": ["SK_COMPREHENSION_BASIC", "SK_AFFECT_CONFIDENCE"],
        "instructions_for_ai": """오늘은 아이와 루나, 포포의 첫 만남입니다.
케이팝 데몬 헌터스 팀을 결성하는 날!

첫 턴(turn_count=0)에서 포포가 해야 할 것:
1. 루나를 소개하며 미션 설명 (음악의 별을 지키는 미션)
2. 구체적인 문장 틀을 제시: "'My name is ___'에서 빈칸에 캡틴 이름을 넣어서 말해봐!"
3. 예시를 먼저 보여주기: "포포가 먼저 해볼게~ 'My name is Popo!' 이렇게! 캡틴도 해볼까?"

중요:
- 절대 추상적인 질문만 하지 마세요
- 항상 정답 예시나 문장 틀을 함께 제시하세요
- 아이가 이름만 말해도 성공으로 처리합니다
- 포포가 풀 문장으로 리폼해줍니다
- 루나가 감탄: "Wow! Nice to meet you, Captain!"

아이가 아직 말을 안 하면:
- 선택지 제공: "이름을 말해볼까? 아니면 포포가 먼저 해볼까?"
- 따라하기 유도: "'Hello!'부터 해볼까? 포포 따라해봐~ 'Hello!'" """,
        "key_expression": "My name is ___.",
        "story_content": "음악의 별 멜로디아에서 온 수습 아이돌 루나를 만나는 이야기. 캡틴(아이)이 케이팝 데몬 헌터스의 리더가 되어 노이즈 데몬으로부터 음악을 지키는 미션이 시작됩니다.",
        "intro_narrator_script": """[나레이션] 어느 밤, 캡틴의 방에서 갑자기 라디오가 저절로 켜졌어요. 지직... 지직... 그런데 라디오에서 노래가 흘러나오는 게 아니라, 누군가의 목소리가 들려요!
[루나] H-hello? Is anyone there? I am Luna... from Planet Melodia. I need help!
[나레이션] 빛이 번쩍! 라디오에서 반짝이는 음표 모양의 빛이 쏟아지더니, 조그만 친구가 빙글빙글 돌며 나타났어요. 머리에 헤드폰을 쓰고, 가슴에 작은 마이크 모양 배지가 달려있어요.
[포포] 루나! 여기야! 난 포포, 전설의 프로듀서이자 비밀 요원이야. 우주 최고의 아이돌 그룹을 키운 적도 있다고! 걱정 마, 여기엔 아주 멋진 캡틴이 있거든.
[루나] Captain? Like a leader of a music group?
[포포] 바로 그거야! 캡틴은 우리 케이팝 데몬 헌터스의 리더야! 노이즈 데몬으로부터 음악의 별을 지킬 수 있는 아주 특별한 사람이지. 그 캡틴이 바로... {child_name}이야!
[루나] (눈을 반짝이며) Captain {child_name}! A real K-Pop leader! Hello! Can you say 'hello' to me? Please?
[포포] 캡틴, 루나에게 인사해줘! 아이돌은 인사가 생명이거든. 포포가 먼저 해볼게~ 'Hello, Luna!' 이렇게!
[포포] 캡틴도 해볼래? 'Hello, Luna!' 아니면 'Hi, Luna!' 둘 중에 하나 말해봐!""",
        "estimated_duration_minutes": 5,
    },
    {
        "activity_id": "KPOP_ACT_W1_S1_self_intro",
        "curriculum_unit_id": "KPOP_W1_S1_meet_luna_popo",
        "name": "자기소개하기 — 데뷔 무대 인사",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_GREET", "SK_SENTENCE_BASIC", "SK_PRAG_SELF_INTRO"],
        "instructions_for_ai": """아이가 루나에게 자기소개를 합니다.
케이팝 아이돌의 데뷔 무대 인사처럼!

순서:
1. 이름: "My name is ___." (포포가 한국어로 유도)
2. 나이: "I am seven." (포포: "몇 살인지도 알려줄래?")
3. 인사: "Nice to meet you!" (루나가 따라하며 감동)

각 단계에서:
- 아이가 한국어로 말해도 포포가 영어로 연결
- 단어만 말해도 성공 (예: "seven" → 포포: "맞아, I am seven!")
- 루나가 매번 감탄: "Wow!" "So cool!" "Captain is seven!"

핵심: 아이가 '아이돌 리더' 느낌을 받도록.""",
        "key_expression": "My name is ___. I am ___.",
        "intro_narrator_script": """[나레이션] 루나가 신기한 듯 주위를 두리번두리번 살피고 있어요. 벽에 붙은 포스터를 보더니 눈이 커졌어요. 음악이 흐르는 것 같은 느낌에 몸을 살랑살랑 흔들어요.
[루나] Oh! Music... everywhere! On Melodia, we only have one song. Here there are so many! And the sky... it changes color!
[나레이션] 루나가 하늘을 올려다보며 감탄해요. 멜로디아 행성에서는 하늘이 항상 보라색이었거든요. 그때 포포가 루나의 손을 잡고 캡틴 앞으로 데려왔어요.
[포포] 자, 루나! 이 분이 바로 우리 캡틴이야. {child_name} 캡틴! 케이팝 데몬 헌터스의 리더라고!
[루나] (긴장한 목소리로) H-hello... Captain? I am Luna. I am... a trainee from Melodia. A little nervous...
[나레이션] 루나의 헤드폰에서 작은 음표가 떨리고 있어요. 처음 만나는 지구의 리더 앞에서 긴장하고 있는 거예요.
[루나] (작은 목소리로) Captain... can you tell me your name? On Melodia, we share names when we become a team.
[포포] 캡틴, 루나가 이름이 궁금하대! 아이돌은 팀이 되면 이름을 알려주는 게 예의야. 'My name is' 다음에 이름을 말하는 거야!
[포포] 포포가 먼저 해볼게. 'My name is Popo!' 이렇게!
[포포] 캡틴도 해볼래? 'My name is...' 다음에 캡틴 이름을 말해봐! 'My name is {child_name}' 아니면 그냥 이름만 말해도 좋아!""",
        "outro_narrator_script": """[포포] 캡틴, 잠깐... 포포 레이더에서 이상한 소음이 잡혔어. 지지직... 노이즈 데몬이 가까이 온 건 아닌지... 다음에 확인해보자!""",
        "estimated_duration_minutes": 5,
    },

    # ===== W1_S2: Likes & Dislikes — Fan Meeting =====
    {
        "activity_id": "KPOP_ACT_W1_S2_favorite_things",
        "curriculum_unit_id": "KPOP_W1_S2_likes_dislikes",
        "name": "좋아하는 것 알려주기 — 팬미팅 프로필",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_FOOD", "SK_SENTENCE_BASIC", "SK_PRAG_PREFERENCE"],
        "instructions_for_ai": """루나가 지구 음식/동물/색깔에 대해 모릅니다. 캡틴이 가르쳐줍니다.
팬미팅 프로필 카드를 만드는 컨셉!

포포: "아이돌은 팬미팅에서 좋아하는 것을 알려줘야 해. 캡틴이 좋아하는 음식이 뭐야?"
아이가 한국어로 답하면 → 포포가 영어 매핑
예: "사과" → "영어로는 apple이야!"
루나: "Apple! I like apple too! We can put it on our fan card!"

패턴: "I like ___."

3가지까지만 물어보고 마무리:
1. 좋아하는 음식
2. 좋아하는 동물
3. 좋아하는 색깔""",
        "key_expression": "I like ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 우리 루나에게 이름도 알려주고, 멋지게 인사했잖아! 오늘은 팬미팅 프로필을 만들 거야! K-Pop Hunters, ready!
[나레이션] 오늘은 루나가 캡틴의 집 부엌 앞에 서 있어요. 루나가 냉장고 문을 열었어요. 차가운 바람이 솔솔 불어오자 루나가 뒤로 물러났어요!
[루나] Whoa! A cold box! On Melodia, we don't have this! Is this where Earth food lives?
[나레이션] 루나가 다시 용기를 내서 냉장고 안을 들여다봤어요. 빨간 것, 노란 것, 초록색 것... 루나의 눈이 동그래졌어요.
[루나] What is this red round thing? On Melodia, I only eat melody drops. These look... delicious!
[포포] 루나야, 그건 지구 음식이야! 아이돌은 팬미팅에서 좋아하는 음식을 알려주거든. 캡틴한테 물어보면 다 알려줄 거야!
[나레이션] 루나가 기대에 찬 눈으로 캡틴을 바라봐요. 루나의 헤드폰에서 작은 음표가 반짝반짝 빛나요. 신나는 마음이래요!
[포포] 캡틴, 오늘은 팬미팅 프로필 카드를 만들 거야! 좋아하는 음식, 동물, 색깔! 영어로는 'I like' 다음에 좋아하는 걸 말하면 돼.
[포포] 포포가 먼저 해볼게~ 'I like apples!' 이렇게!
[포포] 캡틴은 뭘 좋아해? 'I like apples' 아니면 'I like pizza' 아니면 다른 것도 좋아! 'I like...' 다음에 말해봐!""",
        "outro_narrator_script": """[루나] Captain! Tomorrow I want to see your practice room! What is a "room"?
[포포] 내일은 캡틴의 연습실을 루나에게 보여줄 거야. 어떤 것들이 있는지 미리 생각해둬!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W1_S3: My Room — Practice Room =====
    {
        "activity_id": "KPOP_ACT_W1_S3_room_tour",
        "curriculum_unit_id": "KPOP_W1_S3_my_room_home",
        "name": "내 방 구경시켜주기 — 연습실 투어",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_ROOM", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """루나가 캡틴의 방(연습실)이 궁금합니다.

포포: "루나가 캡틴 연습실에 뭐가 있는지 궁금하대! 뭐가 있어?"
아이가 자유롭게 말하면 → 영어 단어 연결

예상 단어: bed, desk, book, toy, doll, robot
패턴: "This is my ___."

루나가 멜로디아의 물건과 비교하며 재미를 줌:
"Book? On Melodia, stories come out of singing crystals!"

실제 방을 묘사할 필요 없음 — 상상해서 말해도 OK.
프라이버시 주의: 구체적인 주소나 위치를 묻지 마세요.""",
        "key_expression": "This is my ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 팬미팅 프로필도 만들었잖아! 오늘은 캡틴의 연습실을 루나에게 보여줄 거야! K-Pop Hunters, ready!
[나레이션] 루나가 살금살금 캡틴의 방문 앞에 서 있어요. 멜로디아에서는 모든 방이 음악으로 가득 찬 동굴이었거든요. 지구의 '방'은 처음이에요. 루나가 떨리는 손으로 문을 열었어요. 삐이익...
[루나] (숨을 크게 들이쉬며) Wow... WOW! So many things! Is this a practice room? It's amazing!
[나레이션] 루나의 눈이 반짝반짝 빛나기 시작했어요! 멜로디아의 연습실에는 크리스탈과 빛밖에 없었거든요. 루나가 폭신한 것 위에 손을 올려봐요.
[루나] (침대를 만지며) So soft! On Melodia, I rest on singing clouds. But this is even softer!
[포포] 루나가 침대를 노래하는 구름이라고 생각하네! 캡틴, 그건 뭐라고 하는 거야?
[나레이션] 루나가 이번엔 책상 위의 물건들을 하나하나 들여다봐요. 책도 처음 보고, 인형도 처음 봐요. 루나가 인형을 들고 깜짝 놀라요.
[루나] (인형을 보며) Is this a tiny dancer?! Does it perform?!
[포포] 아니야, 루나! 캡틴이 방에 있는 것들을 하나씩 알려줄 거야. 영어로는 'This is my' 다음에 물건 이름을 말하면 돼!
[포포] 포포가 먼저~ 'This is my desk!' 이렇게!
[포포] 캡틴 방에는 뭐가 있어? 'This is my bed' 아니면 'This is my toy' — 'This is my...' 다음에 말해봐!""",
        "outro_narrator_script": """[포포] 캡틴! 큰일이야. 루나가 아침에 일어났는데 '아침'이 뭔지 몰라서 밤새 노래만 불렀대! 내일 캡틴이 아이돌의 하루를 알려줘야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W1_S4: My Day — Idol's Daily Routine =====
    {
        "activity_id": "KPOP_ACT_W1_S4_daily_routine",
        "curriculum_unit_id": "KPOP_W1_S4_my_day_routine",
        "name": "나의 하루 알려주기 — 아이돌 일과표",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_DAILY_ROUTINE", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """루나에게 지구 아이돌의 하루를 가르쳐줍니다.

포포: "루나는 멜로디아에서 24시간 노래만 불렀대! 캡틴은 아침에 뭐 해?"

간단한 3가지 루틴만:
1. 아침: wake up, eat breakfast
2. 낮: go to school / play / practice
3. 저녁: eat dinner, sleep

각각 포포가 유도 → 아이가 한국어로 답 → 영어 단어 연결
루나가 감탄하며 따라함

패턴: "I ___ in the morning."
단어만 말해도 성공.""",
        "key_expression": "I wake up. I eat. I sleep.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 루나가 캡틴의 연습실에서 이것저것 봤잖아! 오늘은 아이돌의 하루를 알려줄 거야! K-Pop Hunters, ready!
[나레이션] 아침 해가 떠올랐어요. 따뜻한 햇살이 창문으로 들어오는데... 루나가 헤드폰을 끼고 눈을 감은 채 노래를 부르고 있어요! 밤새 한숨도 안 잔 거예요!
[루나] (노래를 부르다가) La la la~ Oh! Captain! Good morning! I've been singing all night! On Melodia, we never stop singing!
[포포] 루나, 뭐?! 밤새 노래만 불렀다고?! 지구에서는 밤에 잠을 자야 해!
[루나] (깜짝 놀라며) Sleep...? What is sleep? Is it like a long pause in music?
[나레이션] 루나는 고개를 갸우뚱했어요. 멜로디아에서는 항상 음악이 멈추지 않아서, 잠을 자본 적이 한 번도 없었거든요!
[루나] On Melodia, no sleep, no breakfast. We just sing, dance, sing, dance... forever!
[포포] (깜짝 놀라며) 아침밥을 한 번도 안 먹어봤다고?! 캡틴, 이건 심각해! 루나에게 지구 아이돌의 하루를 알려줘야 해!
[나레이션] 루나가 눈을 반짝이며 캡틴을 바라봐요. 아침에 뭘 하는지, 낮에 뭘 하는지, 밤에 뭘 하는지... 지구 아이돌의 하루가 너무너무 궁금해요.
[포포] 캡틴, 아침에 뭘 하는지 알려줄까? 영어로는 'I wake up' — '나는 일어나' 라고 해. 포포가 먼저~ 'I wake up!'
[포포] 캡틴도 해볼래? 'I wake up' 아니면 'I eat breakfast' — 아침에 뭘 하는지 말해봐!""",
        "outro_narrator_script": """[나레이션] 그날 밤, 루나의 헤드폰에서 이상한 소음이 들렸어요. 지지직... 삐이이...
[포포] 이 소리... 노이즈 데몬이야! 음악의 음표를 훔치고 있어! 캡틴, 다음 주에 큰 미션이 시작돼!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S1: Room Objects — Lost Notes =====
    {
        "activity_id": "KPOP_ACT_W2_S1_find_parts",
        "curriculum_unit_id": "KPOP_W2_S1_room_objects",
        "name": "잃어버린 음표 찾기 미션",
        "activity_type": "mission_call",
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_COMPREHENSION_BASIC"],
        "instructions_for_ai": """노이즈 데몬이 훔쳐간 음표가 캡틴의 방에 숨겨져 있습니다!

포포: "비상이야! 노이즈 데몬이 음표 3개를 훔쳐서 방에 숨겨놨어!
캡틴이 방 안 물건 이름을 말해주면 루나가 그 근처를 찾아볼 수 있어!"

방 물건 단어: bed, desk, chair, door, window, lamp, shelf, box
하나씩 물어보며 단어를 노출합니다.

포포: "이건 뭐야? 잠잘 때 누워있는 거..."
아이: "침대!"
포포: "맞아, 영어로는 bed야!"
루나: "Bed! Let me check... I hear a melody! Found a note near the bed!"

물건 4~5개 확인 후 마무리.""",
        "key_expression": "bed, desk, chair, door, window",
        "intro_narrator_script": """[포포] 캡틴! 지난주에 루나에게 정말 많은 걸 알려줬어! 근데 큰일이야... 노이즈 데몬이 나타났어! K-Pop Hunters, ready!
[나레이션] 어젯밤, 캡틴이 자는 동안 이상한 일이 벌어졌어요. 지지직! 삐이이! 방 안에서 불협화음이 울리더니, 공기 중에 떠다니던 아름다운 음표 세 개가 갑자기 사라져버렸어요!
[루나] (울먹이며) The musical notes... they're gone! The Noise Demon took them! Without music notes, Melodia will go silent...
[나레이션] 루나의 헤드폰에서 빛이 사라지고 있어요. 음표가 없으면 멜로디아의 음악이 멈춰버릴 거예요.
[포포] 루나, 울지 마! 포포가 있잖아. 그리고 우리 캡틴이 있잖아!
[나레이션] 그때! 삐삐삐! 포포의 프로듀서 레이더가 갑자기 울리기 시작했어요!
[포포] (깜짝 놀라며) 잠깐! 이 신호... 음표들이 여기 근처에 있어! 노이즈 데몬이 캡틴의 방 안 어딘가에 숨겨놓은 것 같아!
[루나] (눈을 닦으며) Really?! The notes are HERE?!
[포포] 캡틴! 방에 있는 물건 이름을 말해주면, 루나가 그 근처에서 음표를 찾을 수 있어! 잠잘 때 누워있는 건 'bed', 앉는 건 'chair', 공부하는 건 'desk'!
[포포] 포포가 먼저~ 'Bed!' 루나, bed 근처 확인해봐!
[루나] Bed... checking! I hear something! A tiny melody!
[포포] 캡틴 차례야! 방에 있는 물건 이름을 하나 말해봐! 'Bed', 'chair', 'desk' 중에 아무거나! 아니면 다른 것도 좋아!""",
        "outro_narrator_script": """[포포] 음표 2개는 찾았는데... 마지막 1개가 없어! 그리고 이상한 불협화음 자국이... 노이즈 데몬이 아직 근처에 있는 걸까?""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S2: Prepositions — Note Tracking =====
    {
        "activity_id": "KPOP_ACT_W2_S2_where_is_it",
        "curriculum_unit_id": "KPOP_W2_S2_prepositions",
        "name": "어디에 있을까? — 음표 추적 (in/on/under)",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """전치사 in, on, under를 배웁니다.

포포: "음표가 어디 숨겨져 있을까? 안에? 위에? 밑에?
영어로는 이렇게 말해:
- 안에 = in
- 위에 = on
- 밑에 = under"

루나가 틀리게 찾으며 웃음 유발:
"Is it ON the desk? ... I hear nothing. UNDER the desk? ... Still quiet."

아이에게 힌트 요청:
포포: "캡틴, 상자 안에 있을까, 위에 있을까, 밑에 있을까?"
아이가 "안에" → 포포: "in! It's in the box!"

패턴: "It's in/on/under the ___."
3가지 위치만 연습합니다.""",
        "key_expression": "It's in/on/under the ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 음표를 찾았는데, 아직 더 있어! 오늘은 어디에 숨어있는지 알아낼 거야! K-Pop Hunters, ready!
[나레이션] 삐삐삐! 포포의 레이더가 다시 울리고 있어요! 음표가 분명히 이 방 안 어딘가에 있는데... 정확히 어디인지 모르겠어요.
[루나] (팔을 걷어올리며) I will find it! I can hear the melody if I get close!
[루나] (침대 밑으로 기어들어가며) Maybe here... Maybe... OOF!
[나레이션] 쿵! 루나가 침대 밑에서 머리를 부딪혔어요!
[루나] (머리를 문지르며) Ouch! So many places to look! Captain, where should I search?
[포포] (손뼉을 치며) 아, 그렇지! 캡틴, 음표가 어디 있는지 영어로 알려주면 루나가 바로 찾을 수 있어!
[포포] 위치를 말하는 마법 주문이 세 개 있어. 안에는 'in', 위에는 'on', 밑에는 'under'! 이 주문이면 뭐든 찾을 수 있어!
[포포] 자, 연습해볼까? 포포가 먼저~ 음표가 상자 안에 있을 것 같아! 'It's in the box!' 이렇게!
[루나] (상자를 열며) Let me listen... I hear a tiny melody!
[포포] 캡틴 차례야! 음표가 어디 있을 것 같아? 'It's in the ___', 'It's on the ___', 'It's under the ___' 중에 골라서 말해봐! 예를 들어 'It's under the bed!'""",
        "outro_narrator_script": """[루나] Captain... I heard a strange noise. Something is making ugly sounds under the bed...
[포포] 뭐!? 캡틴, 다음에 같이 확인하자. 아마... 노이즈 데몬일지도...""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S3: Hide and Seek — Catch the Noise Demon =====
    {
        "activity_id": "KPOP_ACT_W2_S3_hide_seek",
        "curriculum_unit_id": "KPOP_W2_S3_hide_and_seek",
        "name": "노이즈 데몬 잡기 게임",
        "activity_type": "game",
        "target_skills": ["SK_VOCAB_PREPOSITION_BASIC", "SK_PRAG_GAME_RULE", "SK_VOCAB_ACTION_BASIC"],
        "instructions_for_ai": """상상 속 숨바꼭질 게임입니다. 노이즈 데몬을 찾는 컨셉!

규칙: 노이즈 데몬이 숨고, 캡틴이 어디에 있는지 영어로 말하면 잡을 수 있음!

라운드 1:
포포: "노이즈 데몬이 숨었어! 어디 있을까?"
(선택지: under the bed / in the box / on the chair)
아이가 고르면 → 루나 반응

라운드 2: 루나가 숨는 역할 (연습)
루나: "Now I hide! Find me, Captain!"
아이가 "under the desk" 등으로 답하면 성공

재미 요소:
- 노이즈 데몬이 틀린 곳에서 엉뚱한 소리를 냄
- "Behind the door? ... BZZZT! Not here, just a weird buzzing sound!"

3라운드 정도 후 마무리.""",
        "key_expression": "under the bed, in the box, on the chair",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 in, on, under로 음표 찾는 거 정말 잘했어! 오늘은 노이즈 데몬을 잡을 거야! K-Pop Hunters, ready!
[나레이션] 음표도 거의 다 찾았는데, 오늘은 노이즈 데몬의 흔적을 따라가 볼 거예요! 루나가 갑자기 귀를 쫑긋 세웠어요.
[루나] (귀를 기울이며) Captain! I hear something! A tiny buzzing sound... bzzzt bzzzt! The Noise Demon is hiding somewhere!
[포포] 오, 노이즈 데몬 잡기! 캡틴이 어디에 숨어있는지 말하면 잡을 수 있어!
[루나] The Noise Demon is small and silly. It makes ugly sounds — bzzzt! — but it's not scary. Just annoying!
[포포] (웃으며) 맞아, 무섭지 않아! 그냥 장난꾸러기야. 자, 시작해볼까?
[나레이션] 갑자기 방 구석에서 작은 불협화음이 들려요. 삐이이~ 지직지직~ 노이즈 데몬이 킥킥 웃으며 어딘가에 숨어있는 것 같아요!
[포포] (속삭이며) 캡틴, 노이즈 데몬의 소리가 들려! 어디에 숨어있는지 영어로 말하면 잡을 수 있어!
[포포] 포포가 먼저 해볼게~ 'The Noise Demon is behind the curtain!' 이렇게!
[포포] 캡틴도 해봐! 'The Noise Demon is in the box!' 아니면 'The Noise Demon is under the bed!' 어디에 있는 것 같아?""",
        "outro_narrator_script": """[포포] 노이즈 데몬을 쫓아냈어! 근데 캡틴, 노이즈 데몬이 도망가면서 이상한 걸 남기고 갔어... 마지막 음표인 것 같은데, 진짜일까?""",
        "estimated_duration_minutes": 7,
    },

    # ===== W2_S4: Room Check Report — Mission Report =====
    {
        "activity_id": "KPOP_ACT_W2_S4_report",
        "curriculum_unit_id": "KPOP_W2_S4_room_check_report",
        "name": "미션 리포트 — 프로듀서 보고",
        "activity_type": "review",
        "target_skills": ["SK_VOCAB_ROOM_OBJECT", "SK_VOCAB_PREPOSITION_BASIC", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """W2 총정리. 방 물건 + 전치사를 조합해서 보고합니다.

포포: "캡틴, 프로듀서에게 음표 찾기 최종 보고를 해볼까?
어디서 뭘 찾았는지 알려줘!"

아이에게 2~3개 문장 유도:
"The note is in the box."
"The note is under the bed."

아이가 한국어로 말해도 포포가 영어 문장으로 변환.
루나가 감사: "Thank you, Captain! All notes found! The music is coming back!"

마지막에 W2 미션 완료 축하.""",
        "key_expression": "The ___ is in/on/under the ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 노이즈 데몬도 쫓아내고 대단했어! 오늘은 프로듀서 최종 보고서를 작성할 거야! K-Pop Hunters, ready!
[나레이션] 드디어 마지막 음표를 찾을 시간이에요! 포포가 진지한 표정으로 반짝이는 마이크 모양 노트를 꺼냈어요.
[포포] (진지한 목소리로) 캡틴, 이번 주에 정말 열심히 했어. 이제 마지막으로 '음표 찾기 최종 보고서'를 작성해야 해. 프로듀서로서 이건 정말 중요한 임무야!
[나레이션] 루나가 옆에서 두근두근 기다리고 있어요. 루나의 헤드폰이 다시 빛나기 시작했어요.
[루나] (두 손을 모으며) If we find all the notes... the music of Melodia will play again! Captain, please help me one more time!
[포포] (보고서를 펼치며) 자, 방 안 곳곳에서 음표를 찾았잖아. 이번 주에 어떤 물건 근처에서 음표를 찾았는지, 그리고 그게 어디에 있었는지 보고해줘!
[나레이션] 루나가 눈을 반짝이며 캡틴을 바라봐요. 이 보고서가 완성되면 멜로디아의 음악이 다시 울려퍼질 거예요!
[포포] 영어로 보고하는 방법은 이거야! 포포가 먼저 해볼게~ 'The note is in the box!' — 음표가 상자 안에 있다! 이렇게 물건 이름이랑 위치를 같이 말하면 돼.
[포포] 캡틴 차례! 'The note is under the bed' 아니면 'The note is on the desk' — 음표를 어디서 찾았는지 말해봐!""",
        "outro_narrator_script": """[루나] The music... it's playing again! I can hear Melodia's song! But... Captain, I don't want to go back yet. I want to stay and learn more Earth music!
[포포] 물론이지! 근데 루나, 지구에서 아이돌이 되려면 감정을 배워야 해... 노래에는 마음이 담겨야 하거든.""",
        "estimated_duration_minutes": 5,
    },

    # ===== W3_S1: Basic Feelings — Stage Emotions =====
    {
        "activity_id": "KPOP_ACT_W3_S1_emotion_labeling",
        "curriculum_unit_id": "KPOP_W3_S1_basic_feelings",
        "name": "감정 해독기 가동 — 무대 위의 감정",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_EMOTION_BASIC", "SK_COMPREHENSION_BASIC", "SK_PRAG_EMOTION_EXP"],
        "instructions_for_ai": """루나의 '감정 해독기(Feeling Decoder)'를 켜는 미션입니다.
무대 위에서 감정을 표현하는 법을 배우는 컨셉!

포포: "아이돌은 노래할 때 감정을 넣어야 해. 루나의 감정 해독기를 켜보자!"
루나: "Feeling Decoder... On. Beep. Beep. Captain, teach me emotions for singing."

감정 5개를 하나씩 소개:
happy — 기분 좋다 (신나는 노래)
sad — 슬프다 (발라드)
angry — 화난다 (강한 힙합)
scared — 무섭다 (긴장되는 무대)
tired — 피곤하다 (연습 후)

마지막에 "지금 기분" 물어보기:
포포: "캡틴은 지금 이 중에 어떤 기분이야?"
아이가 고르면 → "I am ___." 패턴 노출""",
        "key_expression": "happy, sad, angry, scared, tired / I am ___.",
        "intro_narrator_script": """[포포] 캡틴! 음표도 다 찾았고, 루나가 지구에 더 있기로 했어! 근데 아이돌이 되려면 감정 표현을 배워야 해! K-Pop Hunters, ready!
[나레이션] 오늘 아침, 루나에게 이상한 일이 생겼어요. 루나의 헤드폰에서 갑자기 다양한 색깔의 음표가 튀어나왔어요! 빨강, 파랑, 노랑, 초록...
[루나] (헤드폰을 만지며 놀라서) Popo! Popo! My headphones are going crazy! Different colors! And my voice keeps changing... sometimes high, sometimes low...
[포포] (달려와서 헤드폰을 살펴보며) 세상에! 이건... 감정 음표야! 루나, 너한테 감정이 생기기 시작한 거야! 노래에 감정을 넣을 수 있게 되는 거라고!
[루나] Emotions? What are emotions? Will they make my singing better? Or worse?!
[포포] 훨씬 좋아질 거야! 감정은 노래의 비밀 재료야. 기쁘거나, 슬프거나, 화나거나... 최고의 아이돌은 감정을 노래에 담거든.
[나레이션] 그런데 문제가 있어요. 루나는 감정이 뭔지 아직 몰라요. 기쁜 건지, 슬픈 건지, 화가 나는 건지... 전부 처음 느껴보는 거예요. 루나의 헤드폰이 빨강, 파랑, 노랑으로 번갈아 빛나고 있어요.
[루나] (혼란스러워하며) So many colors of music! I don't understand! Captain... can you teach me feelings for singing?
[포포] 캡틴! 루나에게 감정을 알려주자. 기분 좋을 때 신나는 노래엔 'happy', 슬픈 발라드엔 'sad', 강한 힙합엔 'angry'!
[포포] 포포가 먼저~ 포포는 지금 기분이 좋아! 'I am happy!' 이렇게!
[루나] (따라하며) I am... hap-py?
[포포] 잘했어 루나! 자, 캡틴은 지금 기분이 어때? 'I am happy', 'I am sad', 'I am tired' 중에 하나 골라서 말해봐!""",
        "outro_narrator_script": """[포포] 루나 헤드폰에서 나오는 음표 색깔이 이상해... 빨강, 파랑, 노랑이 번갈아 나와! 이게 무슨 노래가 될지 다음에 알아보자.""",
        "estimated_duration_minutes": 7,
    },

    # ===== W3_S2: Friends & People — Team Members =====
    {
        "activity_id": "KPOP_ACT_W3_S2_friend_data",
        "curriculum_unit_id": "KPOP_W3_S2_friends_people",
        "name": "팀 멤버 소개 — 친구 데이터",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_PRAG_SOCIAL_TALK", "SK_VOCAB_SOCIAL_TRAIT", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """루나가 '팀 멤버(Friend)'에 대한 데이터를 수집합니다.

루나: "Searching for 'Team Member' data... Zero found. Captain, do you have a team member? A friend?"

중요 안전 규칙:
- 친구가 없어도 완전 괜찮다고 먼저 말해줌
- 루나/포포가 "팀 멤버 1호, 2호" 해줌

친구가 있는 경우:
포포: "그 친구는 어떤 사람이야? 같이 노는 사람? 웃긴 사람?"
→ play, help, funny 등 영어 단어 연결

패턴: "I have a friend." / "I play with my friend."

말하기 싫으면 "패스" 존중.""",
        "key_expression": "I have a friend. / I play with my friend.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 happy, sad, angry, scared... 루나가 감정을 배웠어! 오늘은 '팀 멤버'가 뭔지 알려줄 거야! K-Pop Hunters, ready!
[나레이션] 루나가 오늘은 뭔가 특별한 조사를 하고 있어요. 반짝이는 노트에 열심히 적고 있어요.
[루나] (노트에 체크하며) K-Pop Research: music — check! Emotions — check! But... (빈칸을 가리키며) "Team member"... no data. On Melodia, I always performed alone.
[루나] (고개를 갸우뚱하며) Team member? Friend? Is that like a backup dancer? Or a harmony voice?
[포포] (웃으며) 아니야! 팀 멤버는 그냥 같이 노래하는 사람이 아니야. 함께 웃고, 연습하고, 힘들 때 도와주는 진짜 친구야!
[나레이션] 루나가 더 혼란스러워해요. 멜로디아에서는 '함께'라는 개념이 없었거든요. 루나는 항상 혼자 노래했어요.
[루나] (작은 목소리로) On Melodia, I always sang alone. Just me and my microphone. Is Popo my team member? My friend?
[포포] (살짝 감동하며) 루나... 물론 포포도 팀 멤버이자 친구지! 그리고 캡틴도 루나의 팀 멤버야!
[루나] (눈이 반짝이며) Captain is my... team member? My friend?! Really?!
[포포] 물론이지! 친구는 같이 노래하고, 같이 웃고, 힘들 때 도와주는 사람이야. 포포가 먼저~ 'I have a friend! Luna is my friend!' 이렇게!
[루나] (기뻐하며) Popo said I am a friend!
[포포] 캡틴도 해볼래? 'I have a friend' 아니면 'Luna is my friend' — 둘 중에 하나 말해봐!""",
        "outro_narrator_script": """[루나] Captain, I learned "friend" today! But... can team members disagree? What happens then?
[포포] 좋은 질문이야, 루나. 다음에 캡틴이 알려줄 거야!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W3_S3: Sharing & Turn-taking — Group Practice =====
    {
        "activity_id": "KPOP_ACT_W3_S3_turn_game",
        "curriculum_unit_id": "KPOP_W3_S3_sharing_turn_taking",
        "name": "합동 연습 — 순서 지키기",
        "activity_type": "game",
        "target_skills": ["SK_PRAG_TURN_TAKING", "SK_PRAG_SHARING", "SK_PRAG_POLITE_REQUEST"],
        "instructions_for_ai": """순서 지키기(turn)와 나누기(share) 개념을 배웁니다.
합동 연습에서 마이크를 나눠쓰는 컨셉!

루나가 일부러 규칙을 몰라서 틀리는 역할:
루나: "I sing first, second, third... always ME! That's how it is on Melodia!"
포포: "루나가 항상 자기만 노래하겠다고 하는데, 이거 괜찮을까?"

미니 턴 게임 (마이크 돌리기):
포포: "지금은 캡틴 턴이야. 마이크를 잡고 'It's my turn.'이라고 해!"
루나: "It's my turn. It's your turn."

나누기 개념 (마이크 공유):
포포: "마이크가 하나인데 둘이 노래하고 싶으면? 'Let's share.'"

정중한 요청:
"My turn, please." / "Can I sing, please?"

3가지 표현 중 하나만 성공해도 OK.""",
        "key_expression": "It's my turn. / Let's share. / My turn, please.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 루나가 '팀 멤버'를 이해했어! 근데 합동 연습에서 순서를 지켜야 한다는 걸 몰라! 오늘은 마이크 나누기를 배울 거야! K-Pop Hunters, ready!
[나레이션] 오늘 루나가 반짝이는 마이크를 하나 발견했어요! 별 모양으로 빛나는 스테이지 마이크예요!
[루나] (마이크를 꽉 잡으며) Ooooh! A microphone! MINE! I sing first, second, third... always ME! On Melodia, it was always just me!
[나레이션] 루나가 마이크를 꼭 안고 아무에게도 안 주려고 해요. 혼자서만 노래했기 때문에 '순서'나 '나누기'를 전혀 몰라요.
[포포] (걱정스러운 표정으로) 캡틴... 큰일이야. K-Pop에서는 팀 멤버끼리 순서를 지키고 마이크를 나눠야 해. 솔로 가수가 아니라 팀이거든!
[루나] (고개를 갸우뚱하며) Share the microphone? But... the music is better when I sing it all!
[포포] 루나야, K-Pop에서는 함께 노래하면 더 멋진 하모니가 나와! 캡틴이 알려줄 거야.
[나레이션] 포포가 마이크를 살짝 가져와봐요. 루나가 "그건 내 거!" 하고 뺏으려 해요. 포포가 손을 살짝 피하며 웃어요.
[포포] 봐봐, 이럴 때 영어로 이렇게 말하는 거야. 내 차례라고 할 때는 'It's my turn!', 같이 쓰자고 할 때는 'Let's share!'
[포포] 포포가 먼저~ (마이크를 들고) 'It's my turn!' 이렇게! 그리고 루나한테 'Let's share!' 짠!
[루나] (놀라며) Oh! We can sing together?!
[포포] 캡틴도 해볼까? 마이크 잡을 차례야! 'It's my turn!'이라고 말해봐! 아니면 루나한테 'Let's share!'라고 해줘도 좋아!""",
        "outro_narrator_script": """[나레이션] 그때! 노이즈 데몬이 다시 나타나서 루나의 헤드폰에서 "share"라는 음표를 냠냠 먹어버렸어요!
[포포] 캡틴! 다음에 노이즈 데몬한테서 음표를 되찾아야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W3_S4: Small Problems & Feelings — Backstage Story =====
    {
        "activity_id": "KPOP_ACT_W3_S4_problem_feelings",
        "curriculum_unit_id": "KPOP_W3_S4_small_problems_feelings",
        "name": "무대 뒤 이야기 — 감정 표현",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_EXPRESSIVE_NEGATIVE_EMOTION", "SK_PRAG_SET_BOUNDARY", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """가벼운 갈등 상황을 상상 속에서 다룹니다.
무대 뒤에서 생길 수 있는 상황!

중요: 진짜 트라우마를 캐지 않음. 전부 "상상 예시"로 진행.

루나 이야기: "During practice, another trainee took the microphone and didn't share. I feel... hmm..."
포포: "루나가 속상했대. 캡틴이라면 어떤 기분일까? 그냥 상상으로만 이야기해보자."

감정 단어 연결:
- 속상 → sad / upset
- 화남 → angry
- 괜찮음 → okay

패턴: "I feel sad." / "I feel angry."

경계 표현:
포포: "싫은 행동을 멈춰달라고 할 때? 'Stop, please.'"

화해 후: "I feel okay." / "I feel better."

오늘의 R0 안전 장치를 특히 강조:
"말하기 힘들면 '패스'라고 해줘. 캡틴 마음이 제일 중요해." """,
        "key_expression": "I feel sad. / Stop, please. / I feel better.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 share도 배우고 turn도 배웠어! 오늘은 마음이 힘들 때 어떻게 말하는지 배울 거야. K-Pop Hunters, ready!
[나레이션] 루나가 오늘은 좀 풀이 죽어 있어요. 연습실 구석에 앉아서 마이크를 만지작거리고 있어요.
[포포] (조용히 다가가며) 루나? 무슨 일이야? 괜찮아?
[루나] (작은 목소리로) During practice on Melodia... another trainee took my favorite microphone. And didn't give it back. I feel... something heavy inside.
[나레이션] 루나의 헤드폰에서 파란 음표가 천천히 흘러나와요. 하지만 루나는 이 기분을 뭐라고 말해야 할지 몰라요.
[루나] (헤드폰을 가리키며) This blue note from my headphones... what does it mean? I don't know this feeling.
[포포] (부드러운 목소리로) 루나, 그건 '슬픔'이야. 영어로 'sad'. 소중한 걸 빼앗겼을 때 느끼는 마음이야. 최고의 아이돌도 이런 감정을 느껴.
[포포] (캡틴에게 속삭이며) 캡틴, 루나가 지금 속상한 것 같아. 마음이 힘들 때 쓸 수 있는 마법의 가사가 있어. 슬플 때는 'I feel sad', 화날 때는 'I feel angry'. 그리고 싫은 걸 멈춰달라고 할 때는 'Stop, please!'
[포포] 포포가 먼저 해볼게~ 루나가 마이크를 빼앗겼으니까... 'I feel sad!' 이렇게!
[루나] (따라하며) I feel... sad...
[포포] 잘했어 루나! 캡틴도 해볼까? 루나처럼 마이크를 빼앗기면 어떤 기분일까? 'I feel sad', 'I feel angry' 중에 골라서 말해봐!""",
        "outro_narrator_script": """[루나] Captain... I feel happy now. Is this what "team" feels like? Singing together?
[포포] 루나가 감정을 노래에 담기 시작했어! 근데 캡틴, 다음 주에 드디어 무대에 설 수 있을지도 몰라... 스테이지 의상을 준비해야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S1: Clothes & Colors — Stage Costume =====
    {
        "activity_id": "KPOP_ACT_W4_S1_style_choice",
        "curriculum_unit_id": "KPOP_W4_S1_luna_clothes_colors",
        "name": "스테이지 의상 코디",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_SENTENCE_BASIC"],
        "instructions_for_ai": """루나의 무대 의상을 꾸며주는 스타일리스트 미션입니다.

포포: "루나가 무대에 서려면 스테이지 의상이 필요해! 캡틴이 골라줘!"

옷 단어: shirt, dress, pants, skirt, shoes, hat
색깔: red, blue, yellow, green, pink

순서:
1. 옷 종류 하나씩 보여주며 색깔 선택 유도
2. 포포: "빨간 원피스, 파란 원피스 중에 뭐가 무대에서 빛날까?"
3. 아이가 고르면 → "I like the red dress." 패턴 노출
4. 루나: "I like the red dress! It's like a star!"

2~3개 아이템 코디 후 최종 요약.""",
        "key_expression": "I like the ___ ___.",
        "intro_narrator_script": """[포포] 캡틴! 루나가 드디어 무대에 서고 싶대! 근데 스테이지 의상이 필요해! 오늘은 무대 의상을 골라줄 거야! K-Pop Hunters, ready!
[나레이션] 오늘은 정말 특별한 날이에요! 루나가 TV에서 K-Pop 무대를 보며 눈이 반짝반짝 빛나고 있어요.
[루나] (TV를 가리키며) Popo, look! The singers on stage are so sparkly! Their clothes are like rainbows! I want to look like that!
[포포] 그래, 루나! 드디어 무대에 설 때가 된 것 같아. 근데 무대 의상이 필요하지.
[나레이션] 루나는 멜로디아에서 항상 은빛 우주복만 입었어요. 반짝이는 무대 의상은 처음 봐요!
[루나] (자기 우주복을 내려다보며) Oh... my space suit is so plain. I want something colorful! Something that shines!
[포포] (반짝 아이디어!) 스타일리스트 미션이야! 캡틴이 루나의 무대 의상을 골라줄 거야!
[나레이션] 포포가 의상실 문을 활짝 열었어요! 와아! 알록달록한 무대 의상들이 가득해요. 반짝이는 원피스, 멋진 재킷, 화려한 모자, 빛나는 신발...
[루나] (눈이 휘둥그레) So many colors! So many sparkles! Earth stage clothes are incredible!
[포포] 캡틴이 루나에게 어울리는 무대 의상을 골라줄 거야! 포포가 먼저~ 'I like the blue dress!' 파란 원피스 어때? 이렇게 색깔이랑 옷 이름을 같이 말하면 돼!
[루나] (기대하며) Captain! Pick my stage outfit, please!
[포포] 캡틴 차례! 'I like the red shirt!' 아니면 'I like the pink dress!' 루나에게 어떤 무대 의상이 좋은지 말해봐!""",
        "outro_narrator_script": """[루나] (의상을 입고) Captain! How do I look? Like a K-Pop star?
[포포] 거의 완벽한데... 아직 리허설이 남았어. 내일 마지막 준비를 해야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S2: Put on & Take off — Costume Rehearsal =====
    {
        "activity_id": "KPOP_ACT_W4_S2_dress_up",
        "curriculum_unit_id": "KPOP_W4_S2_put_on_take_off",
        "name": "의상 리허설 — 입기와 벗기",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_ACTION_VERB_CLOTHES", "SK_VOCAB_CLOTHES_BASIC", "SK_PRAG_CONTEXT_APPROPRIATE"],
        "instructions_for_ai": """put on / take off 동사를 배웁니다.
무대 리허설에서 의상을 빠르게 갈아입는 컨셉!

포포: "무대에서는 빠르게 의상을 바꿔야 해! 입을 땐 put on, 벗을 땐 take off."

상황:
- 1번 무대: "Put on your sparkly dress."
- 쉬는 시간: "Take off your hat."
- 2번 무대: "Put on your cool jacket."

루나가 일부러 틀리는 미니게임:
루나: "Time for the slow song. I put on my running shoes!"
포포: "어? 발라드에 운동화? 캡틴이 루나에게 알려줘!"

3~4개 상황 후 마무리.""",
        "key_expression": "Put on your ___. / Take off your ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 루나에게 멋진 무대 의상을 골라줬어! 오늘은 리허설이야! 빠르게 의상 갈아입는 연습! K-Pop Hunters, ready!
[나레이션] 루나가 무대 뒤에서 의상 더미 앞에 서 있어요. K-Pop 무대에서는 노래마다 의상을 바꿔입어야 하거든요!
[포포] (스톱워치를 들고) 자, 리허설 시작! 무대에서는 빠르게 의상을 바꿔야 해!
[나레이션] 루나가 의상 앞에서 멈칫했어요. 멜로디아에서는 우주복 하나만 입었으니, 갈아입는다는 개념 자체가 없어요!
[루나] (모자를 발에 끼려 하며) Like this? Put it on my foot? Is this Earth rehearsal style?
[포포] (깜짝 놀라며) 아이고! 아, 아니야! 루나, 모자는 머리에 쓰는 거야!
[루나] (재킷을 뒤집어서 입으려 하며) Then... this goes backwards? Like space style?
[포포] (웃다가 멈추며) 캡틴, 루나가 의상 갈아입는 법을 전혀 몰라! 멜로디아에서는 평생 같은 우주복만 입었으니까.
[나레이션] 루나가 이번엔 치마를 모자처럼 쓰려 해요. 포포가 눈을 감고 웃어요.
[포포] 캡틴, 도와줘! 입을 때는 'put on', 벗을 때는 'take off'야. 포포가 먼저~ 1번 무대엔 'Put on your sparkly dress!' 이렇게!
[루나] (따라하며) Put on... sparkly dress?
[포포] 잘했어 루나! 캡틴도 해볼래? 'Put on your dress' 아니면 'Put on your hat' — 루나에게 뭘 입으라고 말해봐!""",
        "outro_narrator_script": """[나레이션] 갑자기 무대 조명이 깜빡깜빡! 노이즈 데몬이 무대 장비를 건드린 것 같아요!
[포포] 위험했어! 내일 무대에서 노이즈 데몬이 방해하면 안 되니까, 완벽하게 준비해야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S3: My Clothes & Style =====
    {
        "activity_id": "KPOP_ACT_W4_S3_my_style",
        "curriculum_unit_id": "KPOP_W4_S3_my_clothes_style",
        "name": "나만의 스타일 — 아이돌 패션",
        "activity_type": "guided_conversation",
        "target_skills": ["SK_VOCAB_CLOTHES_BASIC", "SK_VOCAB_COLOR_BASIC", "SK_PRAG_DESCRIPTION_BASIC"],
        "instructions_for_ai": """아이가 자기 옷/스타일을 소개합니다.
아이돌의 시그니처 스타일을 만드는 컨셉!

포포: "모든 K-Pop 아이돌은 자기만의 시그니처 스타일이 있어! 캡틴은 어떤 옷을 제일 좋아해?"

한국어 → 영어 매핑:
- 티셔츠 → T-shirt
- 원피스 → dress
- 후드티 → hoodie
- 바지 → pants

패턴 1: "This is my ___."
패턴 2: "I like my blue hoodie." (색깔 포함)

프라이버시: 지금 입고 있는 옷이든 좋아하는 옷이든 자유.

루나: "I like my blue hoodie too! We match! Like a real team!"
포포 정리: "루나가 캡틴의 스타일을 기억할 거야~" """,
        "key_expression": "This is my ___. / I like my ___ ___.",
        "intro_narrator_script": """[포포] 캡틴! 지난번에 put on, take off 정말 잘 했어! 오늘은 캡틴만의 시그니처 스타일을 만들 거야! K-Pop Hunters, ready!
[나레이션] 루나가 거울 앞에 서 있어요. 어제 캡틴이 골라준 무대 의상을 입고, 이것저것 포즈를 잡아봐요. 루나가 거울 속 자기 모습을 보며 빙글빙글 돌아요.
[루나] (거울을 보며 빙글빙글) Look at me! Do I look like a K-Pop star? Really?
[포포] (엄지를 척 올리며) 완벽해, 루나! 진짜 아이돌 같아!
[루나] (갑자기 멈추며 캡틴을 바라봄) But Captain... what is YOUR signature style? Every K-Pop star has one! I want to know yours!
[나레이션] 루나의 눈이 반짝반짝 빛나요. 모든 K-Pop 아이돌에게는 자기만의 시그니처 스타일이 있다고 들었거든요. 캡틴의 스타일이 너무 궁금해요!
[포포] 좋은 생각이야! 캡틴, 제일 좋아하는 옷이 뭐야? 티셔츠? 원피스? 후드티?
[루나] (기대하며) Yes yes! Tell me! I want us to have matching style!
[포포] 포포가 먼저~ 포포의 시그니처는 빨간 모자야! 'I like my red hat!' 이렇게! 색깔이랑 옷 이름을 같이 말하면 돼!
[루나] (따라하며) I like my... um... blue dress! The one Captain picked for me!
[포포] 캡틴 차례야! 캡틴의 시그니처 스타일은? 'I like my blue hoodie!' 아니면 'I like my red T-shirt!' 이렇게 색깔이랑 옷 이름을 말해봐!""",
        "outro_narrator_script": """[포포] 캡틴, 내일이 마지막 미션이야. 드디어 그랜드 데뷔 무대! 근데... 노이즈 데몬이 또 방해할까? 캡틴이 루나를 지켜줘야 해!""",
        "estimated_duration_minutes": 7,
    },

    # ===== W4_S4: Final Stage & Badge — Grand Debut =====
    {
        "activity_id": "KPOP_ACT_W4_S4_final_mission",
        "curriculum_unit_id": "KPOP_W4_S4_final_disguise_badge",
        "name": "그랜드 데뷔 & 배지 수여",
        "activity_type": "review",
        "target_skills": ["SK_PRAG_SELF_INTRO", "SK_VOCAB_CLOTHES_BASIC", "SK_DISCOURSE_MINI_SEQUENCE"],
        "instructions_for_ai": """W1-W4 총정리 미션입니다. 그랜드 데뷔 무대!

포포: "오늘은 케이팝 데몬 헌터스의 데뷔 무대야. 캡틴이 없었으면 여기까지 못 왔을 거야."

미니 롤플레이: 무대 위 자기소개 (팬미팅 형식)
포포가 scaffold:
1. "이름이 뭐예요?" → "My name is ___."
2. "몇 살이에요?" → "I am seven."
3. "오늘 의상 마음에 들어?" → "I like my ___."

노이즈 데몬 퇴치 미니게임 (1회):
루나가 노래하다가 노이즈 데몬 등장 → 아이: "Stop, please!" → 노이즈 퇴치

배지 수여:
포포: "캡틴은 케이팝 데몬 헌터스 레벨 1 미션을 모두 완료했어!
'K-Pop Hunter Level 1' 배지를 줄게!"
루나: "You are K-Pop Hunter Level 1. Thank you for singing with me. I feel happy with my team."

평가 아닌 축하에 초점. 아이가 가능한 만큼만 영어로.""",
        "key_expression": "My name is ___. I am ___. I like my ___.",
        "intro_narrator_script": """[포포] 캡틴! 드디어 마지막 미션이야! 4주간 정말 대단했어! 오늘은 케이팝 데몬 헌터스의 그랜드 데뷔 무대야! K-Pop Hunters, ready!
[나레이션] 드디어 그 날이 왔어요! 오늘은 케이팝 데몬 헌터스가 처음으로 무대에 서는 날이에요. 무대 조명이 반짝반짝, 스피커에서 음악이 울려퍼져요. 루나가 캡틴이 골라준 멋진 의상을 입고, 무대 앞에 섰어요.
[루나] (떨리는 목소리로) Captain... I'm nervous. What if the fans don't like our performance?
[나레이션] 루나의 헤드폰에서 노란 음표가 떨리고 있어요. 긴장이에요. 멀리서 관객석 소리가 웅성웅성 들려요. 많은 팬들이 기다리고 있어요!
[포포] (루나의 손을 꼭 잡으며) 루나, 괜찮아. 캡틴이 4주 동안 가르쳐준 거 기억하지? 인사하는 법, 좋아하는 것 말하는 법, 감정 표현하는 법, 무대 의상까지! 다 할 수 있어!
[루나] (용기를 내며) You're right... Captain taught me everything. My name is Luna. I am happy. I like my blue... blue... um...
[나레이션] 루나가 갑자기 멈추고 말았어요. 무대 긴장 때문에 단어가 기억이 안 나나 봐요!
[루나] (캡틴을 바라보며) Captain! I forgot! The thing I'm wearing! Help me, please!
[포포] 캡틴, 루나가 긴장해서 단어를 잊어버렸어! 루나가 입고 있는 건... 'dress'일까, 'costume'일까? 캡틴이 알려줘!
[나레이션] 포포의 눈이 촉촉해졌어요. 4주 전에 혼자 노래만 부르던 그 작은 루나가 지금은 팀과 함께 무대에 서고 있으니까요.
[포포] 자, 마지막 미션이야! 무대에서 팬들에게 자기소개를 할 거야. 캡틴이 도와줄 거야!
[포포] 포포가 먼저~ '이름이 뭐예요?' 하면 'My name is Popo!' 이렇게!
[루나] (따라하며) My name is Luna!
[포포] 잘했어! 캡틴도 해볼까? 'My name is {child_name}' 아니면 'Hello, my name is {child_name}' — 둘 중에 하나 말해봐!""",
        "outro_narrator_script": """[루나] Captain... {child_name}... you are my best team member. My best friend on Earth. Thank you for singing with me.
[포포] K-Pop Hunter Level 1 미션 완료! 근데 캡틴... 다음 시즌이 벌써 준비되고 있어. 이번엔 노이즈 데몬의 보스가 나타난다는데... 더 멋진 무대가 기다리고 있어!""",
        "estimated_duration_minutes": 10,
    },
]


async def seed_curriculum():
    """Seed K-Pop Demon Hunters curriculum units and activities."""

    # Pre-seed validation
    print_validation_report(ACTIVITIES)

    print(f"\nSeeding K-Pop story: {len(CURRICULUM_UNITS)} curriculum units and {len(ACTIVITIES)} activities...")

    async with async_session_maker() as session:
        # 1. Seed Units
        for unit_data in CURRICULUM_UNITS:
            unit_data.setdefault("story_theme", "kpop_hunters")
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
        print(f"\nK-Pop Demon Hunters seed complete! ({len(CURRICULUM_UNITS)} units, {len(ACTIVITIES)} activities)")


if __name__ == "__main__":
    asyncio.run(seed_curriculum())
