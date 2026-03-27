# Week 4 Task · Activity · Skill Mapping
프로젝트 밤토리 · 7세 페르소나 · W4_S1 ~ W4_S4
Topic: Going Outside in Disguise – Operation 'Disguise'

---

## 공통 규칙

- `activity_id` 형식: `ACT_W4_S[세션번호]_[핵심주제]`
- `task_attempt_id` 형식: `TASK_W4_S[세션번호]_[구체행동]` (Spec의 T_ID와 매핑)

---

## W4_S1: Clothes & Colors (루나 변장 코디)

| Session | activity_id                      | task_attempt_id                      | Task 설명 (KR)                                             | 예시 아동 발화                          | skill_id 리스트                                                                 | 비고 |
|--------|-----------------------------------|--------------------------------------|------------------------------------------------------------|-----------------------------------------|-------------------------------------------------------------------------------|------|
| W4_S1  | ACT_W4_S1_mission_start          | TASK_W4_S1_accept_stylist_mission    | 루나를 지구인처럼 꾸며주는 '스타일리스트' 미션 수락         | (끄덕임, "응, 도와줄게")               | SK_COMPREHENSION_BASIC, SK_AFFECT_CONFIDENCE                                  |      |
| W4_S1  | ACT_W4_S1_clothes_vocab          | TASK_W4_S1_repeat_clothes_words      | 옷 단어(shirt, dress, pants 등) 따라 말하기 (선택적)        | "shirt", "dress"                       | SK_VOCAB_CLOTHES_BASIC, SK_PRONUN_BASIC                                       |      |
| W4_S1  | ACT_W4_S1_style_choice           | TASK_W4_S1_clothes_like_color        | 'I like the [red shirt].' 패턴으로 색깔+옷 조합 선택        | "I like the red shirt."                | SK_VOCAB_CLOTHES_BASIC, SK_VOCAB_COLOR_BASIC, SK_SENTENCE_BASIC               | 중요 |
| W4_S1  | ACT_W4_S1_style_dislike          | TASK_W4_S1_clothes_dislike_optional  | (선택) 'I don’t like ~.' 패턴으로 비선호 스타일 표현        | "I don’t like the black hat."          | SK_SENTENCE_BASIC, SK_PRAG_PREFERENCE, SK_SYNTAX_NEGATION                     |      |
| W4_S1  | ACT_W4_S1_coordi_summary         | TASK_W4_S1_confirm_outfit            | 루나의 최종 코디 요약을 듣고 맞는지 확인/수정               | "응, 맞아."                             | SK_COMPREHENSION_BASIC, SK_PRAG_CONFIRMATION                                  |      |

---

## W4_S2: Put on & Take off (입기 / 벗기)

| Session | activity_id                      | task_attempt_id                          | Task 설명 (KR)                                                             | 예시 아동 발화                              | skill_id 리스트                                                                                | 비고 |
|--------|-----------------------------------|------------------------------------------|----------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------------------------|------|
| W4_S2  | ACT_W4_S2_verb_intro             | TASK_W4_S2_repeat_verbs                  | Put on / Take off 동작 동사 따라 말하기                                    | "Put on", "Take off"                        | SK_VOCAB_ACTION_VERB_CLOTHES, SK_PRONUN_BASIC                                                  |      |
| W4_S2  | ACT_W4_S2_weather_context        | TASK_W4_S2_put_on_cold                   | 추운 날씨 상황에서 'Put on your coat.' 말하기                              | "Put on your coat."                         | SK_VOCAB_ACTION_VERB_CLOTHES, SK_VOCAB_CLOTHES_BASIC, SK_PRAG_CONTEXT_APPROPRIATE              |      |
| W4_S2  | ACT_W4_S2_home_context           | TASK_W4_S2_take_off_home                 | 집에 들어온 상황에서 'Take off your shoes.' 말하기                         | "Take off your shoes."                      | SK_VOCAB_ACTION_VERB_CLOTHES, SK_VOCAB_CLOTHES_BASIC, SK_PRAG_CONTEXT_APPROPRIATE              |      |
| W4_S2  | ACT_W4_S2_mistake_fix            | TASK_W4_S2_fix_luna_mistake              | 루나의 실수(추운날 옷 벗기 등)를 보고 올바른 행동(Put on) 지시하기         | "No, put on your coat."                     | SK_PRAG_CORRECTION, SK_VOCAB_ACTION_VERB_CLOTHES, SK_AFFECT_CONFIDENCE                         |      |

---

## W4_S3: My Clothes & My Style (내 스타일)

| Session | activity_id                      | task_attempt_id                          | Task 설명 (KR)                                                                      | 예시 아동 발화                                   | skill_id 리스트                                                                                         | 비고 |
|--------|-----------------------------------|------------------------------------------|-------------------------------------------------------------------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------|------|
| W4_S3  | ACT_W4_S3_my_choice              | TASK_W4_S3_this_is_my_clothes            | 자신이 입은/좋아하는 옷을 'This is my [dress].'로 소개                               | "This is my dress."                              | SK_VOCAB_CLOTHES_BASIC, SK_SENTENCE_BASIC, SK_PRAG_DESCRIPTION_BASIC                                    |      |
| W4_S3  | ACT_W4_S3_my_choice              | TASK_W4_S3_like_my_color_clothes         | 색깔을 포함하여 'I like my [blue hoodie].' 패턴 시도                                 | "I like my blue hoodie."                         | SK_VOCAB_CLOTHES_BASIC, SK_VOCAB_COLOR_BASIC, SK_SENTENCE_BASIC                                         |      |
| W4_S3  | ACT_W4_S3_usage_context          | TASK_W4_S3_say_when_wear_en              | (선택) 언제 입는지(school/home) 간단한 단어로 표현                                   | "school", "home"                                 | SK_VOCAB_PLACE_BASIC, SK_PRAG_DESCRIPTION_BASIC                                                         |      |

---

## W4_S4: Final Disguise & Badge (최종 미션 & 배지)

| Session | activity_id                      | task_attempt_id                              | Task 설명 (KR)                                                                 | 예시 아동 발화                                   | skill_id 리스트                                                                                               | 비고 |
|--------|-----------------------------------|----------------------------------------------|--------------------------------------------------------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------|------|
| W4_S4  | ACT_W4_S4_final_check            | TASK_W4_S4_fix_disguise_context              | 최종 리허설 중 루나의 복장 실수를 발견하고 수정해주기                           | "Put on your coat."                              | SK_PRAG_CORRECTION, SK_VOCAB_ACTION_VERB_CLOTHES, SK_AFFECT_CONFIDENCE                                         |      |
| W4_S4  | ACT_W4_S4_role_play_intro        | TASK_W4_S4_mini_self_intro_clothes           | 지구인 친구에게 자기소개(이름/나이) + 내 옷 소개(I like my~)                    | "My name is [Name]. I like my [shirt]."          | SK_PRAG_SELF_INTRO, SK_VOCAB_CLOTHES_BASIC, SK_DISCOURSE_MINI_SEQUENCE                                         | 종합 과제 |
| W4_S4  | ACT_W4_S4_badge_ceremony         | TASK_W4_S4_receive_badge                     | Level 1 Badge 수여 축하 및 다음 단계(외부 세계) 미션 예고 수락                  | "와!", "Yes, Captain!"                           | SK_AFFECT_CONFIDENCE, SK_PRAG_SOCIAL_RITUAL                                                                    |      |

---

## Skill ID 추가 (W4 전용)

| skill_id                       | 설명 (KR)                                      | 카테고리 | mode       |
|--------------------------------|-----------------------------------------------|----------|------------|
| SK_VOCAB_CLOTHES_BASIC         | 옷 관련 단어 (shirt, dress, hat 등)           | language | expressive |
| SK_VOCAB_COLOR_BASIC           | 기본 색깔 단어 (red, blue, yellow 등)         | language | expressive |
| SK_VOCAB_ACTION_VERB_CLOTHES   | 옷 입기/벗기 동사 (put on, take off)          | language | expressive |
| SK_PRAG_CONTEXT_APPROPRIATE    | 상황(날씨/장소)에 맞는 행동/말하기             | social   | expressive |
| SK_DISCOURSE_MINI_SEQUENCE     | 2~3문장 연속 발화 (이름+나이+옷)              | language | expressive |
