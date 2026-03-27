# Week 2 Task · Activity · Skill Mapping
프로젝트 밤토리 · 7세 페르소나 · W2_S1 ~ W2_S4
Topic: Lost Parts – Room Mission

---

## 공통 규칙

- `activity_id` 형식: `ACT_W2_S[세션번호]_[핵심주제]`
- `task_attempt_id` 형식: `TASK_W2_S[세션번호]_[구체행동]` (Spec의 T_ID와 매핑)

---

## W2_S1: Where is the Shiny Part? (기본 위치 표현)

| Session | activity_id                      | task_attempt_id                      | Task 설명 (KR)                                             | 예시 아동 발화                          | skill_id 리스트                                                                 | 비고 |
|--------|-----------------------------------|--------------------------------------|------------------------------------------------------------|-----------------------------------------|-------------------------------------------------------------------------------|------|
| W2_S1  | ACT_W2_S1_mission_briefing       | TASK_W2_S1_accept_mission            | '에너지 조각 찾기' 미션 수락 및 수색 시작 (Mission Hook)    | (끄덕임, "응", "찾아볼게")             | SK_COMPREHENSION_BASIC, SK_AFFECT_CONFIDENCE                                  |      |
| W2_S1  | ACT_W2_S1_location_guess         | TASK_W2_S1_guess_location_ko         | 에너지 조각 위치를 한국어로 추측 (침대 위/상자 안 등)       | "상자 안에 있어", "침대 위"            | SK_PRAG_DESCRIPTION_BASIC, SK_AFFECT_CONFIDENCE                               |      |
| W2_S1  | ACT_W2_S1_location_guess         | TASK_W2_S1_say_location_en           | 'On the bed', 'In the box' 등 위치 전치사구 영어 표현       | "In the box.", "On the bed."           | SK_VOCAB_PREPOSITION_BASIC, SK_VOCAB_ROOM_BASIC, SK_SENTENCE_BASIC            | 전치사+명사 조합 |
| W2_S1  | ACT_W2_S1_room_bridge            | TASK_W2_S1_describe_my_room_item_en  | (선택) 내 방의 물건 위치를 영어로 표현 시도                 | "My doll is on the bed."               | SK_VOCAB_ROOM_BASIC, SK_VOCAB_PREPOSITION_BASIC, SK_SENTENCE_BASIC            | 심화 Task |

---

## W2_S2: Furniture & Fixing Station (가구 단어)

| Session | activity_id                      | task_attempt_id                          | Task 설명 (KR)                                                             | 예시 아동 발화                              | skill_id 리스트                                                                                | 비고 |
|--------|-----------------------------------|------------------------------------------|----------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------------------------|------|
| W2_S2  | ACT_W2_S2_base_setup             | TASK_W2_S2_designate_repair_base         | 방을 'Secret Repair Base'로 임명하는데 동의 (Role Play)                    | "응", "좋아", "수리 기지!"                 | SK_COMPREHENSION_BASIC, SK_AFFECT_CONFIDENCE                                                   |      |
| W2_S2  | ACT_W2_S2_furniture_vocab        | TASK_W2_S2_repeat_furniture_words        | 주요 가구 단어(bed, desk, chair) 따라 말하기                               | "bed", "desk", "chair"                      | SK_VOCAB_ROOM_BASIC, SK_PRONUN_BASIC                                                           |      |
| W2_S2  | ACT_W2_S2_furniture_vocab        | TASK_W2_S2_say_this_is_my_item           | 'This is my [bed].' 패턴으로 가구 소개                                     | "This is my bed."                           | SK_VOCAB_ROOM_BASIC, SK_SENTENCE_BASIC, SK_PRAG_OWNERSHIP                                      |      |
| W2_S2  | ACT_W2_S2_action_verb            | TASK_W2_S2_say_sit_action                | 'I sit on the chair.' 문장 또는 'sit' 동사 표현                            | "I sit on the chair.", "sit"                | SK_VOCAB_ACTION_BASIC, SK_VOCAB_PREPOSITION_BASIC, SK_SENTENCE_BASIC                           |      |
| W2_S2  | ACT_W2_S2_room_check             | TASK_W2_S2_confirm_furniture_placement   | 방 가구 배치 질문에 대답 확인 (영어 라벨링 듣기)                           | "네, 책상은 침대 옆에 있어요."             | SK_COMPREHENSION_BASIC, SK_PRAG_DESCRIPTION_BASIC                                              |      |

---

## W2_S3: Hide & Seek (숨바꼭질 & 전치사 심화)

| Session | activity_id                      | task_attempt_id                          | Task 설명 (KR)                                                                      | 예시 아동 발화                                   | skill_id 리스트                                                                                         | 비고 |
|--------|-----------------------------------|------------------------------------------|-------------------------------------------------------------------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------|------|
| W2_S3  | ACT_W2_S3_hide_seek_round1       | TASK_W2_S3_guess_hidden_spot_ko          | 숨겨진 조각 위치 맞추기 (Korean/English)                                            | "책상 아래!", "Under the desk!"                  | SK_COMPREHENSION_BASIC, SK_PRAG_GAME_RULE                                                               |      |
| W2_S3  | ACT_W2_S3_hide_seek_round1       | TASK_W2_S3_say_hidden_spot_en            | 위치 정답을 'Under the desk' 형태로 영어 발화                                       | "Under the desk."                                | SK_VOCAB_PREPOSITION_BASIC, SK_VOCAB_ROOM_BASIC                                                         |      |
| W2_S3  | ACT_W2_S3_hide_seek_active       | TASK_W2_S3_hide_item_and_say_en          | 아이가 직접 위치를 정하고 루나에게 영어로 힌트 주기                                 | "It is in the box."                              | SK_VOCAB_PREPOSITION_BASIC, SK_SENTENCE_BASIC, SK_PRAG_GAME_RULE, SK_AFFECT_CONFIDENCE                 | 주도적 Task |
| W2_S3  | ACT_W2_S3_real_room_link         | TASK_W2_S3_describe_real_item_loc        | (선택) 실제 방의 물건 위치 묘사 시도                                                | "My toy is in the box."                          | SK_VOCAB_ROOM_BASIC, SK_VOCAB_PREPOSITION_BASIC, SK_SENTENCE_BASIC                                      |      |

---

## W2_S4: Room Check Report (방 구조 리포팅)

| Session | activity_id                      | task_attempt_id                              | Task 설명 (KR)                                                                 | 예시 아동 발화                                   | skill_id 리스트                                                                                               | 비고 |
|--------|-----------------------------------|----------------------------------------------|--------------------------------------------------------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------|------|
| W2_S4  | ACT_W2_S4_report_draft           | TASK_W2_S4_say_room_item_en                  | 리포트 작성: 방에 있는 물건 1개 이상 말하기                                    | "I have a bed." / "bed"                          | SK_VOCAB_ROOM_BASIC, SK_SENTENCE_BASIC, SK_PRAG_DESCRIPTION_BASIC                                              |      |
| W2_S4  | ACT_W2_S4_report_draft           | TASK_W2_S4_say_item_location_en              | 리포트 작성: 물건의 위치 1개 이상 말하기                                       | "My toy is on the bed."                          | SK_VOCAB_PREPOSITION_BASIC, SK_SENTENCE_BASIC, SK_PRAG_DESCRIPTION_BASIC                                       |      |
| W2_S4  | ACT_W2_S4_report_review          | TASK_W2_S4_confirm_report_summary            | 포포가 정리한 'Room Report' 내용이 맞는지 최종 확인                            | "응, 맞아."                                      | SK_COMPREHENSION_BASIC, SK_PRAG_CONFIRMATION, SK_AFFECT_CONFIDENCE                                             |      |
| W2_S4  | ACT_W2_S4_mission_complete       | TASK_W2_S4_celebrate_repair                  | 루나 수리 완료 축하 및 다음 미션(W3) 예고 확인                                 | "와!", "Mission Complete!"                       | SK_AFFECT_CONFIDENCE, SK_PRAG_SOCIAL_RITUAL                                                                    |      |

---

## Skill ID 추가 (W2 전용)

| skill_id                   | 설명 (KR)                                      | 카테고리 | mode       |
|----------------------------|-----------------------------------------------|----------|------------|
| SK_VOCAB_PREPOSITION_BASIC | 위치 전치사 (in, on, under)                   | language | expressive |
| SK_VOCAB_ACTION_BASIC      | 기초 동작 동사 (sit, stand 등)                | language | expressive |
| SK_PRAG_GAME_RULE          | 게임 규칙(숨바꼭질 등) 이해 및 참여            | cognitive| both       |
| SK_PRAG_DESCRIPTION_BASIC  | 사물/위치 묘사 화용 능력                       | language | expressive |
