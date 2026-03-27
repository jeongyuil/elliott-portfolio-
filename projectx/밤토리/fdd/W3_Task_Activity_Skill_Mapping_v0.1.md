# Week 3 Task · Activity · Skill Mapping
프로젝트 밤토리 · 7세 페르소나 · W3_S1 ~ W3_S4
Topic: Feelings & Friends – Operation 'Heart Signal'

---

## 공통 규칙

- `activity_id` 형식: `ACT_W3_S[세션번호]_[핵심주제]`
- `task_attempt_id` 형식: `TASK_W3_S[세션번호]_[구체행동]` (Spec의 T_ID와 매핑)

---

## W3_S1: My Basic Feelings (기본 감정)

| Session | activity_id                      | task_attempt_id                      | Task 설명 (KR)                                             | 예시 아동 발화                          | skill_id 리스트                                                                 | 비고 |
|--------|-----------------------------------|--------------------------------------|------------------------------------------------------------|-----------------------------------------|-------------------------------------------------------------------------------|------|
| W3_S1  | ACT_W3_S1_mission_start          | TASK_W3_S1_accept_decoder_mission    | '감정 해독기(Feeling Decoder)' 가동 및 미션 수락            | "응", "도와줄게", "OK"                 | SK_COMPREHENSION_BASIC, SK_AFFECT_CONFIDENCE                                  |      |
| W3_S1  | ACT_W3_S1_emotion_labeling       | TASK_W3_S1_label_happy               | '기분 좋다(Happy)' 얼굴 카드 고르고 따라 말하기             | (Happy 카드 선택) "Happy."             | SK_VOCAB_EMOTION_BASIC, SK_COMPREHENSION_BASIC                                |      |
| W3_S1  | ACT_W3_S1_emotion_check          | TASK_W3_S1_say_current_feeling       | 현재 자신의 기분을 카드에서 골라 표현 (I am [happy])        | "I am happy.", "happy"                 | SK_VOCAB_EMOTION_BASIC, SK_SENTENCE_BASIC, SK_PRAG_EMOTION_EXP                 |      |
| W3_S1  | ACT_W3_S1_mood_matching          | TASK_W3_S1_match_situation_feeling   | (선택) 상황(선물 등)에 맞는 감정 카드 고르기                | (Happy 카드 선택)                      | SK_COMPREHENSION_SITUATION, SK_VOCAB_EMOTION_BASIC                            |      |

---

## W3_S2: My Friends & People Around Me (친구)

| Session | activity_id                      | task_attempt_id                          | Task 설명 (KR)                                                             | 예시 아동 발화                              | skill_id 리스트                                                                                | 비고 |
|--------|-----------------------------------|------------------------------------------|----------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------------------------|------|
| W3_S2  | ACT_W3_S2_friend_data            | TASK_W3_S2_provide_friend_info           | 루나의 '친구 데이터' 수집에 응답 (친구 유무/코드네임)                      | "친구 있어", "민지", "친구 없어"            | SK_PRAG_SOCIAL_TALK, SK_AFFECT_CONFIDENCE                                                      |      |
| W3_S2  | ACT_W3_S2_friend_trait           | TASK_W3_S2_describe_friend_trait_en      | 친구의 특징(play, help, funny) 중 하나 골라 영어로 표현                    | "plays", "funny"                            | SK_VOCAB_SOCIAL_TRAIT, SK_SENTENCE_BASIC                                                       |      |
| W3_S2  | ACT_W3_S2_social_sentence        | TASK_W3_S2_say_i_have_friend             | 'I have a friend.' 또는 'I have Luna.' 패턴 발화                          | "I have a friend.", "I have Luna."          | SK_SENTENCE_BASIC, SK_PRAG_SOCIAL_TALK                                                         |      |
| W3_S2  | ACT_W3_S2_play_action            | TASK_W3_S2_say_play_with_friend          | 'I play with my friend.' 패턴 따라 말하기                                 | "I play with my friend."                    | SK_SENTENCE_BASIC, SK_VOCAB_PLAY_BASIC, SK_PRAG_SOCIAL_PLAY                                    |      |

---

## W3_S3: Sharing & Turn-taking (나누기 & 순서)

| Session | activity_id                      | task_attempt_id                          | Task 설명 (KR)                                                                      | 예시 아동 발화                                   | skill_id 리스트                                                                                         | 비고 |
|--------|-----------------------------------|------------------------------------------|-------------------------------------------------------------------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------|------|
| W3_S3  | ACT_W3_S3_turn_game              | TASK_W3_S3_say_my_turn_en                | 미니 게임 중 자기 차례일 때 'It’s my turn.' 말하기                                  | "It’s my turn."                                  | SK_PRAG_TURN_TAKING, SK_SENTENCE_BASIC                                                                  |      |
| W3_S3  | ACT_W3_S3_sharing_concept        | TASK_W3_S3_suggest_share_en              | 장난감 하나일 때 'Let’s share.' 제안하기 (또는 단어 share)                          | "Let’s share.", "share"                          | SK_PRAG_SHARING, SK_VOCAB_SOCIAL_RULE                                                                   |      |
| W3_S3  | ACT_W3_S3_polite_request         | TASK_W3_S3_say_polite_request_en         | 정중하게 요청하기 ('My turn, please' / 'Can I play, please?')                       | "My turn, please."                               | SK_PRAG_POLITE_REQUEST, SK_SENTENCE_BASIC                                                               |      |

---

## W3_S4: Small Problems & Feelings (갈등 해결 기초)

| Session | activity_id                      | task_attempt_id                              | Task 설명 (KR)                                                                 | 예시 아동 발화                                   | skill_id 리스트                                                                                               | 비고 |
|--------|-----------------------------------|----------------------------------------------|--------------------------------------------------------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------|------|
| W3_S4  | ACT_W3_S4_problem_reaction       | TASK_W3_S4_identify_negative_feeling         | 문제 상황(장난감 뺏김 등)에서 감정(sad/angry) 식별                             | "속상해", "sad"                                  | SK_COMPREHENSION_SITUATION, SK_VOCAB_EMOTION_BASIC                                                             |      |
| W3_S4  | ACT_W3_S4_feeling_expression     | TASK_W3_S4_say_feeling_sentence_en           | 부정적 감정을 'I feel sad/angry.' 패턴으로 표현                                | "I feel sad.", "sad"                             | SK_EXPRESSIVE_NEGATIVE_EMOTION, SK_SENTENCE_BASIC                                                              |      |
| W3_S4  | ACT_W3_S4_boundary_setting       | TASK_W3_S4_say_stop_en                       | 싫은 행동에 대해 'Stop, please.'라고 말하기 연습                               | "Stop, please."                                  | SK_PRAG_SET_BOUNDARY, SK_VOCAB_SOCIAL_RULE                                                                     |      |
| W3_S4  | ACT_W3_S4_resolution_imagination | TASK_W3_S4_say_feel_better_en                | 화해 후 기분 나아짐('I feel better / okay') 표현                               | "I feel okay.", "better"                         | SK_EXPRESSIVE_POSITIVE_EMOTION, SK_SENTENCE_BASIC                                                              |      |

---

## Skill ID 추가 (W3 전용)

| skill_id                       | 설명 (KR)                                      | 카테고리 | mode       |
|--------------------------------|-----------------------------------------------|----------|------------|
| SK_VOCAB_EMOTION_BASIC         | 감정 단어 (happy, sad, angry 등)              | language | expressive |
| SK_VOCAB_SOCIAL_TRAIT          | 친구 특성 단어 (funny, help, play 등)         | language | expressive |
| SK_PRAG_TURN_TAKING            | 순서 지키기 관련 화용 표현 (my turn)          | social   | expressive |
| SK_PRAG_SHARING                | 공유하기 제안 (Let's share)                   | social   | expressive |
| SK_PRAG_POLITE_REQUEST         | 정중한 요청 (Please usage)                    | social   | expressive |
| SK_PRAG_SET_BOUNDARY           | 거절/중단 요청 (Stop)                         | social   | expressive |
| SK_EXPRESSIVE_NEGATIVE_EMOTION | 부정적 감정의 적절한 언어적 표현               | emotional| expressive |
