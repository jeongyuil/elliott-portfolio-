# Week 1 Task · Activity · Skill Mapping
프로젝트 밤토리 · 7세 페르소나 · W1_S1 ~ W1_S4

> 참고: `activity_id`, `task_attempt_id`, `skill_id` 네이밍은 제안안입니다.  
> 실제 구현 시 VOICE AI 온톨로지의 `Activity`, `TaskAttempt`, `Skill` 엔티티에 맞게 등록·조정하면 됩니다.

---

## 공통 규칙

- `activity_id` 형식: `ACT_W1_S[세션번호]_[핵심주제]`
- `task_attempt_id` 형식: `TASK_W1_S[세션번호]_[구체행동]`
- `skill_id`는 아래와 같이 추천된 도메인별 ID를 사용 (예시):
  - `SK_VOCAB_BASIC` · 기초 어휘
  - `SK_SENTENCE_BASIC` · 기초 문장 구성
  - `SK_PRAG_SELF_INTRO` · 자기소개 화용 능력
  - `SK_PRAG_PREFERENCE` · 선호/비선호 표현
  - `SK_PRAG_ROUTINE` · 일상 루틴 설명
  - `SK_COMPREHENSION_BASIC` · 기초 듣기 이해
  - `SK_AFFECT_CONFIDENCE` · 말하기 자신감/정서
  - 등등 (아래 표에 상세 기입)

---

## W1_S1: Meet Luna & Popo / My Name & Age

### Activity · Task · Skill 매핑

| Session | activity_id                      | task_attempt_id                      | Task 설명 (KR)                                             | 예시 아동 발화                          | skill_id 리스트                                                                 | 비고 |
|--------|-----------------------------------|--------------------------------------|------------------------------------------------------------|-----------------------------------------|-------------------------------------------------------------------------------|------|
| W1_S1  | ACT_W1_S1_intro_characters       | TASK_W1_S1_listen_intro              | 루나의 '지구 대원(Captain)' 임명 제안을 듣고 수락 (Mission Start)          | (고개 끄덕이기, “응”, “알겠어”)        | SK_COMPREHENSION_BASIC, SK_AFFECT_CONFIDENCE                                  | Mission Hook 수락 |
| W1_S1  | ACT_W1_S1_my_name                | TASK_W1_S1_name_korean               | 자신의 이름/별명을 한국어로 말하기                        | “유일”, “엘리엇이에요”                 | SK_PRAG_SELF_INTRO, SK_AFFECT_CONFIDENCE                                      | 기본 자기표현 |
| W1_S1  | ACT_W1_S1_my_name                | TASK_W1_S1_name_english              | ‘My name is ~’ 패턴으로 이름 말하기 시도                  | “My name is Eliot.”                    | SK_VOCAB_BASIC, SK_SENTENCE_BASIC, SK_PRAG_SELF_INTRO                          | 부분 발화도 `partial` 허용 |
| W1_S1  | ACT_W1_S1_my_age                 | TASK_W1_S1_age_korean                | 자신의 나이를 한국어로 말하기                             | “일곱 살”, “7살이요”                   | SK_PRAG_SELF_INTRO, SK_NUMERIC_BASIC                                          |      |
| W1_S1  | ACT_W1_S1_my_age                 | TASK_W1_S1_age_english               | ‘I am seven.’ 형식으로 나이 말하기                        | “I am seven.”                          | SK_VOCAB_BASIC, SK_SENTENCE_BASIC, SK_PRAG_SELF_INTRO, SK_NUMERIC_BASIC       |      |
| W1_S1  | ACT_W1_S1_secret_code            | TASK_W1_S1_choose_secret_code        | '우주 친구 비밀 코드' 정하기 (예: 뿅뿅, 에너지부족 등)                    | “뿅뿅!”, “에너지 부족!”               | SK_PRAG_EMOTION_EXP, SK_AFFECT_CONFIDENCE                                     | 이후 세션에서 재사용 |

---

## W1_S2: My Likes & Dislikes (취향 탐색)

### Activity · Task · Skill 매핑

| Session | activity_id                      | task_attempt_id                          | Task 설명 (KR)                                                             | 예시 아동 발화                              | skill_id 리스트                                                                                | 비고 |
|--------|-----------------------------------|------------------------------------------|----------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------------------------|------|
| W1_S2  | ACT_W1_S2_animals_preference     | TASK_W1_S2_choose_favorite_animal        | 카드/이미지 중 좋아하는 동물 선택                                         | (선택 동작) “고양이요”                     | SK_PRAG_PREFERENCE, SK_AFFECT_CONFIDENCE                                                     | 한국어 선택도 OK |
| W1_S2  | ACT_W1_S2_animals_preference     | TASK_W1_S2_say_like_animal_en            | ‘I like ___.’ 패턴으로 좋아하는 동물 말하기                               | “I like cat.” / “cat.”                    | SK_VOCAB_BASIC, SK_SENTENCE_BASIC, SK_PRAG_PREFERENCE, SK_PRONUN_BASIC                       | 단어만 말해도 partial |
| W1_S2  | ACT_W1_S2_animals_dislike        | TASK_W1_S2_say_dislike_animal_en         | (선택) ‘I don’t like ___.’로 무서운/싫은 동물 표현                         | “I don’t like snakes.”                    | SK_SENTENCE_BASIC, SK_PRAG_PREFERENCE, SK_SYNTAX_NEGATION                                     | 기분/컨디션에 따라 생략 가능 |
| W1_S2  | ACT_W1_S2_food_preference        | TASK_W1_S2_choose_favorite_food          | 좋아하는 음식 선택                                                         | “피자요”, “아이스크림”                     | SK_PRAG_PREFERENCE, SK_AFFECT_CONFIDENCE                                                     |      |
| W1_S2  | ACT_W1_S2_food_preference        | TASK_W1_S2_say_like_food_en              | ‘I like ___.’ 패턴으로 좋아하는 음식 말하기                               | “I like pizza.”                           | SK_VOCAB_FOOD_BASIC, SK_SENTENCE_BASIC, SK_PRAG_PREFERENCE, SK_PRONUN_BASIC                   |      |
| W1_S2  | ACT_W1_S2_food_dislike           | TASK_W1_S2_say_dislike_food_en           | (선택) ‘I don’t like ___.’로 싫어하는 음식 표현                            | “I don’t like milk.”                      | SK_SENTENCE_BASIC, SK_PRAG_PREFERENCE, SK_SYNTAX_NEGATION                                     |      |
| W1_S2  | ACT_W1_S2_hobby_preference       | TASK_W1_S2_choose_favorite_hobby         | 좋아하는 놀이/취미 선택                                                    | “그림 그리기”, “레고”                      | SK_PRAG_PREFERENCE, SK_AFFECT_CONFIDENCE                                                     |      |
| W1_S2  | ACT_W1_S2_hobby_preference       | TASK_W1_S2_say_like_hobby_en             | ‘I like drawing.’ / ‘I like games.’ 등으로 취미 영어 표현                  | “I like drawing.”                         | SK_VOCAB_ACTIVITY_BASIC, SK_SENTENCE_BASIC, SK_PRAG_PREFERENCE, SK_PRONUN_BASIC               |      |
| W1_S2  | ACT_W1_S2_summary_memory         | TASK_W1_S2_confirm_luna_memory           | 루나가 기록한 "대원 취향 데이터"가 맞는지 확인 (Mission Check)            | “응”, “맞아”, “아니, 게임도 좋아해요”     | SK_COMPREHENSION_BASIC, SK_PRAG_CONFIRMATION, SK_AFFECT_CONFIDENCE                            | follow-up로 정보 보정 |

---

## W1_S3: My Room & My Home

### Activity · Task · Skill 매핑

| Session | activity_id                      | task_attempt_id                          | Task 설명 (KR)                                                                      | 예시 아동 발화                                   | skill_id 리스트                                                                                         | 비고 |
|--------|-----------------------------------|------------------------------------------|-------------------------------------------------------------------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------|------|
| W1_S3  | ACT_W1_S3_list_room_items        | TASK_W1_S3_list_room_items_ko            | 'Captain Base Camp' (방)에 있는 보급품/장비 한국어로 나열                | “침대, 인형이랑 책 있어요.”                    | SK_PRAG_DESCRIPTION_BASIC, SK_AFFECT_CONFIDENCE                                                       |      |
| W1_S3  | ACT_W1_S3_list_room_items        | TASK_W1_S3_say_i_have_item_en            | ‘I have a ___.’ 패턴으로 방의 물건 1개 이상 영어로 표현                            | “I have a doll.” / “doll.”                   | SK_VOCAB_ROOM_BASIC, SK_SENTENCE_BASIC, SK_PRAG_OWNERSHIP, SK_PRONUN_BASIC                            |      |
| W1_S3  | ACT_W1_S3_favorite_room_item     | TASK_W1_S3_choose_favorite_room_item     | 방에서 가장 좋아하는 물건 1개 선택                                                 | “인형이요”                                     | SK_PRAG_PREFERENCE, SK_AFFECT_CONFIDENCE                                                             |      |
| W1_S3  | ACT_W1_S3_favorite_room_item     | TASK_W1_S3_say_this_is_my_item_en        | ‘This is my [doll].’ 또는 ‘I like my [doll].’ 시도                                 | “This is my doll.”                           | SK_VOCAB_ROOM_BASIC, SK_SENTENCE_BASIC, SK_PRAG_OWNERSHIP, SK_PRAG_PREFERENCE                          | 선택 |
| W1_S3  | ACT_W1_S3_family_members         | TASK_W1_S3_list_family_ko                | 함께 사는 가족 구성원을 한국어로 말하기                                            | “엄마, 아빠, 아기 동생이랑 살아요.”            | SK_PRAG_FAMILY, SK_AFFECT_CONFIDENCE                                                                  |      |
| W1_S3  | ACT_W1_S3_family_members         | TASK_W1_S3_say_live_with_family_en       | ‘I live with my mom and dad.’ 또는 가족 단어만 일부 말하기                         | “mom, dad”, “I live with my mom.”             | SK_VOCAB_FAMILY_BASIC, SK_SENTENCE_BASIC, SK_PRAG_FAMILY, SK_PRONUN_BASIC                              | 부분 문장 허용 |
| W1_S3  | ACT_W1_S3_home_type              | TASK_W1_S3_say_home_type_ko              | 집 유형을 한국어로 말하기 (아파트/집 등)                                           | “아파트”, “단독주택”                            | SK_PRAG_DESCRIPTION_BASIC                                                                            | 민감정보 제외 |
| W1_S3  | ACT_W1_S3_home_type              | TASK_W1_S3_say_home_type_en (선택)       | ‘apartment/house’ 등 단어 노출 또는 간단 표현                                       | “apartment”                                   | SK_VOCAB_HOME_BASIC, SK_COMPREHENSION_BASIC                                                           | 상태 따라 생략 가능 |
| W1_S3  | ACT_W1_S3_luna_imagination       | TASK_W1_S3_confirm_luna_imagination      | 루나가 상상한 '기지(Room)' 도면 설명을 듣고 맞는지 확인                    | “맞아요”, “아니요, 인형은 침대 옆이에요.”       | SK_COMPREHENSION_BASIC, SK_PRAG_CORRECTION, SK_AFFECT_CONFIDENCE                                      | 실제 레이아웃까지 요구 X |

---

## W1_S4: My Day / What I Do (일상 루틴)

### Activity · Task · Skill 매핑

| Session | activity_id                      | task_attempt_id                              | Task 설명 (KR)                                                                 | 예시 아동 발화                                   | skill_id 리스트                                                                                               | 비고 |
|--------|-----------------------------------|----------------------------------------------|--------------------------------------------------------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------|------|
| W1_S4  | ACT_W1_S4_morning_routine        | TASK_W1_S4_morning_korean                    | 아침에 하는 일을 한국어로 설명                                                 | “일어나서 세수하고 밥 먹어요.”                  | SK_PRAG_ROUTINE, SK_AFFECT_CONFIDENCE                                                                        |      |
| W1_S4  | ACT_W1_S4_morning_routine        | TASK_W1_S4_say_i_wake_up_en                  | ‘I wake up.’ 발화 시도                                                         | “I wake up.”                                   | SK_VOCAB_ROUTINE_BASIC, SK_SENTENCE_BASIC, SK_PRAG_ROUTINE, SK_PRONUN_BASIC                                    |      |
| W1_S4  | ACT_W1_S4_morning_routine        | TASK_W1_S4_say_i_eat_breakfast_en            | ‘I eat breakfast.’ 발화 시도                                                   | “I eat breakfast.”                             | SK_VOCAB_FOOD_BASIC, SK_SENTENCE_BASIC, SK_PRAG_ROUTINE                                                        | 택1만 성공해도 OK |
| W1_S4  | ACT_W1_S4_school_or_home         | TASK_W1_S4_say_where_go_ko                   | 아침 이후 어디 가는지 한국어로 말하기 (학교/유치원/집 등)                     | “학교 가요”, “유치원 가요”, “집에 있어요.”       | SK_PRAG_ROUTINE, SK_PRAG_FAMILY                                                                                |      |
| W1_S4  | ACT_W1_S4_school_or_home         | TASK_W1_S4_say_i_go_to_school_en             | ‘I go to school.’ 또는 ‘I stay home.’ 등 발화                                   | “I go to school.” / “I stay home.”            | SK_VOCAB_PLACE_BASIC, SK_SENTENCE_BASIC, SK_PRAG_ROUTINE                                                       |      |
| W1_S4  | ACT_W1_S4_afternoon_activity     | TASK_W1_S4_choose_afternoon_activity_ko      | 오후에 주로 하는 놀이를 한국어로 선택/말하기                                   | “레고해요”, “그림 그려요”, “게임해요”           | SK_PRAG_PREFERENCE, SK_PRAG_ROUTINE, SK_AFFECT_CONFIDENCE                                                     |      |
| W1_S4  | ACT_W1_S4_afternoon_activity     | TASK_W1_S4_say_afternoon_activity_en         | ‘I play.’, ‘I draw.’, ‘I watch TV.’ 등으로 오후 활동 영어 표현                 | “I play.” / “I draw.”                          | SK_VOCAB_ACTIVITY_BASIC, SK_SENTENCE_BASIC, SK_PRAG_ROUTINE, SK_PRAG_PREFERENCE                                 |      |
| W1_S4  | ACT_W1_S4_evening_dinner_sleep   | TASK_W1_S4_say_i_eat_dinner_en               | ‘I eat dinner.’ 발화 시도                                                      | “I eat dinner.”                               | SK_VOCAB_FOOD_BASIC, SK_SENTENCE_BASIC, SK_PRAG_ROUTINE                                                        |      |
| W1_S4  | ACT_W1_S4_evening_dinner_sleep   | TASK_W1_S4_say_i_sleep_en                    | ‘I sleep.’ 또는 ‘I go to bed.’ 발화 시도                                       | “I sleep.” / “I go to bed.”                   | SK_VOCAB_ROUTINE_BASIC, SK_SENTENCE_BASIC, SK_PRAG_ROUTINE                                                     | 둘 중 하나면 성공 |
| W1_S4  | ACT_W1_S4_timeline_game          | TASK_W1_S4_fix_timeline_error_en             | 'Earth Time vs Space Time' 동기화 오류 수정 (Time Sync Mission)                | “No… I wake up in the morning.” / “I sleep.”   | SK_COMPREHENSION_BASIC, SK_PRAG_CORRECTION, SK_PRAG_ROUTINE, SK_AFFECT_CONFIDENCE                               | 선택적 게임형 Task |
| W1_S4  | ACT_W1_S4_summary                | TASK_W1_S4_confirm_day_summary_ko            | 포포의 '지구 대원 하루 리포트' 최종본 확인                                     | “맞아요”, “아니요, 저는 TV도 봐요.”             | SK_COMPREHENSION_BASIC, SK_PRAG_CONFIRMATION, SK_AFFECT_CONFIDENCE                                             |      |

---

## Skill ID 요약 (제안안)

| skill_id                   | 설명 (KR)                                      | 카테고리 (언어/인지/정서) | mode (receptive/expressive/both) |
|----------------------------|-----------------------------------------------|---------------------------|----------------------------------|
| SK_VOCAB_BASIC             | 기초 어휘 (이름, 나이, 간단 사물)            | language                  | expressive                       |
| SK_VOCAB_FOOD_BASIC        | 음식 관련 기초 어휘                          | language                  | expressive                       |
| SK_VOCAB_ACTIVITY_BASIC    | 놀이/활동 관련 기초 어휘                     | language                  | expressive                       |
| SK_VOCAB_ROOM_BASIC        | 방/집 관련 기초 어휘                         | language                  | expressive                       |
| SK_VOCAB_FAMILY_BASIC      | 가족 구성원 관련 어휘                        | language                  | expressive                       |
| SK_VOCAB_ROUTINE_BASIC     | 일상 루틴 관련 동사 어휘(wake up, sleep 등) | language                  | expressive                       |
| SK_SENTENCE_BASIC          | 단순 SVO 구조 문장 만들기                    | language                  | expressive                       |
| SK_SYNTAX_NEGATION         | 부정문 형태(“don’t”) 사용                    | language                  | expressive                       |
| SK_PRAG_SELF_INTRO         | 자기소개 상황에 적절한 표현 사용             | language                  | expressive                       |
| SK_PRAG_PREFERENCE         | 좋아함/싫어함을 상황에 맞게 표현             | language                  | expressive                       |
| SK_PRAG_ROUTINE            | 하루 일과를 시간 순서대로 설명               | language                  | expressive                       |
| SK_PRAG_FAMILY             | 가족 구성에 대해 자연스럽게 설명             | language                  | expressive                       |
| SK_PRAG_OWNERSHIP          | ‘내 것’을 나타내는 표현 사용                 | language                  | expressive                       |
| SK_PRAG_EMOTION_EXP        | 기분/감정 상태를 단어/코드로 표현            | emotional                 | expressive                       |
| SK_PRAG_CONFIRMATION       | “맞다/아니다”를 적절히 피드백                | language                  | expressive                       |
| SK_PRAG_CORRECTION         | 상대 발화 오류를 부드럽게 수정               | language                  | expressive                       |
| SK_COMPREHENSION_BASIC     | 간단한 영어/한국어 안내 이해                 | language                  | receptive                        |
| SK_AFFECT_CONFIDENCE       | 짧은 발화라도 시도하는 자신감                | emotional                 | both                             |
| SK_NUMERIC_BASIC           | 기본 숫자(나이 등) 표현                      | cognitive                 | expressive                       |

---

> 이 문서는 **엔지니어링 구현·분석(Feature flag, TaskAttempt 로그, SkillLevel 업데이트)**에서  
> 공통 기준으로 사용할 수 있는 W1 전용 Task 매핑 초안입니다.  
> 이후 W2~W4도 동일한 패턴으로 확장하면, 온톨로지 기반 데이터가 일관되게 쌓이게 됩니다.
