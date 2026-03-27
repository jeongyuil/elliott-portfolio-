# Skill_Dictionary_v0.1

VOICE AI 교육 플랫폼에서 사용하는 **Skill 엔티티 인스턴스(초안)** 정의서입니다.  
Phase 1 (MVP: 6–8세, 특히 7세) 범위를 우선 대상으로 합니다.

- 이 문서는 **도메인 온톨로지의 `Skill` 엔티티**를 구체화한 인스턴스 목록입니다.
- FDD에서는 “Skill 인스턴스는 `Skill_Dictionary_v0.1`을 따른다”라고만 명시하고,
  실제 스킬 목록/설명/레벨 정의는 이 문서에서 유지보수합니다.

---

## 1. 필드 스키마 규칙

각 Skill 인스턴스는 도메인 온톨로지의 `Skill` 엔티티 스키마를 따릅니다.

- `skill_id` (string, PK)  
  - 전역 유니크 ID  
  - 네이밍 규칙 예: `LANG_VOCAB_DAILY_01`, `COGN_ATTENTION_SESSION_01`
- `name_kr` (string)  
  - 한국어 표시 이름
- `name_en` (string)  
  - 영문 표시 이름 (내부/국제 협업용)
- `category` (enum)  
  - `language`, `cognitive`, `emotional`
- `mode` (enum)  
  - `receptive`, `expressive`, `both`
- `age_band` (enum)  
  - 예: `4-6`, `7-9`, `10-12`
- `unit` (string)  
  - 예: `score_0_100`, `level_1_5`, `boolean`
- `is_core_metric` (bool)  
  - 월간 리포트/대시보드에서 1차적으로 노출하는 핵심 지표 여부
- `description` (text)  
  - 스킬의 정의 및 관찰 기준
- `can_do_examples` (text/JSON)  
  - “이 스킬 레벨에서 아이가 할 수 있는 일”을 **can-do 문장**으로 서술

> 주의: **Level(레벨 체계)**는 `SkillLevel` 엔티티에서 정의되며,  
> 이 문서는 “스킬의 타입/정의”를 담당합니다.

---

## 2. Phase 1 전체 개요

Phase 1 (W1~W4)에서 실제로 사용되는 스킬들을 아래와 같이 정의합니다.

- Language (언어) 스킬
  - 일상 어휘, 기본 문장, 자기소개, 선호 표현, WH-질문 응답, 순서 말하기, 대화 규칙 등
- Cognitive (인지) 스킬
  - 주의 집중, 간단한 작업 기억, 두 단계 지시 따르기 등
- Emotional (정서/사회) 스킬
  - 기분 자기 보고, 칭찬/피드백 반응, 선호·비선호 정서 표현 등

각 스킬은 **MVP 대상 연령대(6–8세, 기본 7–9 밴드)**에 맞추어 설계했습니다.

---

## 3. Language Skills (언어 스킬)

### 3.1 LANG_VOCAB_DAILY_01

- `skill_id`: `LANG_VOCAB_DAILY_01`
- `name_kr`: 일상 어휘 이해 및 사용 (기초)
- `name_en`: Daily-life Vocabulary (Basic)
- `category`: `language`
- `mode`: `both`
- `age_band`: `7-9`
- `unit`: `score_0_100`
- `is_core_metric`: `true`
- `description`:
  - 일상생활과 관련된 **기초 명사/동사/형용사**(예: 가족, 동물, 음식, 놀이, 방 안 사물)를 듣고 이해하거나, 단어 또는 짧은 표현으로 말할 수 있는 능력.
- `can_do_examples`:
  - “가족, 동물, 음식, 장난감 등 20~40개의 일상 단어를 그림/상황과 매칭할 수 있다.”
  - “질문에 대해 단어 한 개만 말하더라도, 의미적으로 적절한 단어를 선택할 수 있다. (예: ‘좋아하는 동물은 뭐야?’ → ‘cat’).”
  - “AI가 먼저 말한 단어를 따라 말하기(shadowing)가 가능하다.”

---

### 3.2 LANG_VOCAB_PREFERENCE_01

- `skill_id`: `LANG_VOCAB_PREFERENCE_01`
- `name_kr`: 좋아하는 것/싫어하는 것 어휘 및 표현
- `name_en`: Likes & Dislikes Vocabulary
- `category`: `language`
- `mode`: `expressive`
- `age_band`: `7-9`
- `unit`: `score_0_100`
- `is_core_metric`: `true`
- `description`:
  - 동물, 음식, 놀이/취미 등 선호 영역에서 **“I like ~ / I don’t like ~”** 패턴을 활용해 자신의 취향을 영어로 표현하는 능력.
- `can_do_examples`:
  - “AI가 제시한 여러 그림(동물, 음식 등) 중에서 자신이 좋아하는 것을 선택하고, ‘I like ___.’로 말할 수 있다.”
  - “조금 싫어하는 대상에 대해 ‘I don’t like ___.’를 말해볼 수 있다 (문장 혹은 단어 수준).”
  - “한 세션 내에서 최소 1~2개의 선호 문장을 성공적으로 말할 수 있다.”

---

### 3.3 LANG_PRON_BASIC_01

- `skill_id`: `LANG_PRON_BASIC_01`
- `name_kr`: 기초 영어 발음 명료도
- `name_en`: Basic English Pronunciation Clarity
- `category`: `language`
- `mode`: `expressive`
- `age_band`: `7-9`
- `unit`: `score_0_100`
- `is_core_metric`: `false`  (백엔드/전문가용 세부 지표)
- `description`:
  - STT와 모델 평가 기준으로, 영어 단어/짧은 문장을 말했을 때 **의미 파악이 가능한 수준으로 발음하는 능력**.
- `can_do_examples`:
  - “기초 단어(cat, dog, pizza 등)를 발음했을 때, STT가 대체로 올바른 단어로 인식한다.”
  - “문장 전체가 아닌 일부 소리만 약간 흐려져도, 전체 의미 이해에는 큰 장애가 없다.”

---

### 3.4 LANG_SENT_BASIC_SVO_01

- `skill_id`: `LANG_SENT_BASIC_SVO_01`
- `name_kr`: 기초 SVO 문장 구성 (자기소개/선호)
- `name_en`: Basic SVO Sentence (Self-intro & Preferences)
- `category`: `language`
- `mode`: `expressive`
- `age_band`: `7-9`
- `unit`: `score_0_100`
- `is_core_metric`: `true`
- `description`:
  - “My name is ~.”, “I am ~.”, “I like ~.”처럼 간단한 **주어-동사-목적어(SVO) 패턴**으로 된 문장을 완성하거나, 일부라도 해당 패턴과 유사하게 말할 수 있는 능력.
- `can_do_examples`:
  - “My name is [Name].”을 한 세션에서 1회 이상 스스로 말할 수 있다 (Popo의 코칭/모델링 포함).”
  - “‘I like ___.’ 문장을 완전하거나 부분적으로(‘like pizza’) 말할 수 있다.”
  - “문장 길이가 부담스러울 때, 단어만 말해도 Popo의 리폼(reformulation)을 통해 의미를 의사소통 할 수 있다.”

---

### 3.5 LANG_SENT_AGE_01

- `skill_id`: `LANG_SENT_AGE_01`
- `name_kr`: 나이 표현 문장 (“I am seven.”)
- `name_en`: Age Expression (“I am seven.”)
- `category`: `language`
- `mode`: `expressive`
- `age_band`: `7-9`
- `unit`: `score_0_100`
- `is_core_metric`: `false` (세부 항목, 자기소개 전체는 상위 지표에서 커버)
- `description`:
  - 숫자와 함께 자신의 나이를 영어로 표현하는 능력.
- `can_do_examples`:
  - “I am seven.” 또는 “seven”으로 나이를 말할 수 있다.”
  - “질문 ‘How old are you?’에 대해 숫자만 대답해도, 의도된 의미를 전달할 수 있다.”

---

### 3.6 LANG_PRAG_GREETING_INTRO_01

- `skill_id`: `LANG_PRAG_GREETING_INTRO_01`
- `name_kr`: 인사 및 기본 자기소개 화용 능력
- `name_en`: Greeting & Basic Self-introduction Pragmatics
- `category`: `language`
- `mode`: `both`
- `age_band`: `7-9`
- `unit`: `level_1_5`
- `is_core_metric`: `true`
- `description`:
  - 인사, 이름·나이 소개와 관련된 **사회적/화용적 능력**.  
    (예: 인사에 적절히 응답, 자기차례가 왔을 때 최소한 이름 말하기 등)
- `can_do_examples`:
  - “AI가 ‘Hello / Hi’라고 인사했을 때, 한국어나 영어로라도 응답할 수 있다.”
  - “자기소개 타이밍에 전혀 침묵만 하지 않고, 최소한 이름이나 별명 등 한 단어를 말해볼 수 있다.”
  - “한 세션에서 인사 → 이름 → 나이 흐름을 큰 거부 없이 따라갈 수 있다.”

---

### 3.7 LANG_PRAG_TURNTAKING_01

- `skill_id`: `LANG_PRAG_TURNTAKING_01`
- `name_kr`: 차례 지키기 및 응답 타이밍
- `name_en`: Turn-taking & Response Timing
- `category`: `language`
- `mode`: `both`
- `age_band`: `7-9`
- `unit`: `level_1_5`
- `is_core_metric`: `false`
- `description`:
  - AI가 말하는 동안 끼어들지 않고, 질문 후 **적절한 시간 안에** 대답을 시도할 수 있는지에 대한 화용적 능력.
- `can_do_examples`:
  - “AI 발화가 끝난 뒤 5초 이내에 대답을 시도하는 경우가 세션 내에 여러 번 나타난다.”
  - “AI가 ‘지금은 루나 차례야’처럼 안내했을 때, 대체로 가만히 기다릴 수 있다.”

---

### 3.8 LANG_DISC_SEQUENCE_01

- `skill_id`: `LANG_DISC_SEQUENCE_01`
- `name_kr`: 간단한 순서/루틴 서술
- `name_en`: Simple Daily Sequence Description
- `category`: `language`
- `mode`: `expressive`
- `age_band`: `7-9`
- `unit`: `score_0_100`
- `is_core_metric`: `true`
- `description`:
  - “아침 → 낮 → 저녁”처럼 **3단계 정도의 순서를 자신의 말로 표현**하는 능력.  
    (문장 단위가 아니더라도, 활동 어휘를 순서대로 나열하는 수준 포함)
- `can_do_examples`:
  - “아침에 하는 일, 오후에 하는 일, 밤에 하는 일을 각각 한 단어 또는 한 문장 수준으로 말할 수 있다.”
  - “AI가 순서를 일부러 틀렸을 때(예: ‘first sleep, then breakfast’), 그것이 이상함을 인지하고 부분적으로라도 수정하려고 시도한다.”

---

### 3.9 LANG_WH_ANSWER_SIMPLE_01

- `skill_id`: `LANG_WH_ANSWER_SIMPLE_01`
- `name_kr`: 기초 WH-질문에 대한 단어 수준 응답
- `name_en`: Simple WH-question Answer (Word-level)
- `category`: `language`
- `mode`: `expressive`
- `age_band`: `7-9`
- `unit`: `score_0_100`
- `is_core_metric`: `true`
- `description`:
  - “What do you like?”, “Who do you live with?” 등 **간단한 WH-질문**에 대해, 최소한 단어 한 개 수준으로나마 의미 있는 응답을 할 수 있는 능력.
- `can_do_examples`:
  - “What do you like?” → “cat / pizza / drawing” 등 한 단어로 대답할 수 있다.”
  - “질문을 한국어로 다시 들은 뒤, 영어 단어나 혼합어(예: ‘pizza요’)로 대답하려고 한다.”

---

### 3.10 LANG_ROOM_HOME_01

- `skill_id`: `LANG_ROOM_HOME_01`
- `name_kr`: 내 방/우리 집 관련 어휘 및 표현
- `name_en`: My Room & Home Vocabulary
- `category`: `language`
- `mode`: `both`
- `age_band`: `7-9`
- `unit`: `score_0_100`
- `is_core_metric`: `false`
- `description`:
  - 방 안의 물건(침대, 책상, 인형 등)과 가족 구성/집 형태와 관련된 영어 단어와 간단한 표현(“I have a doll.”, “I live with my mom and dad.”) 사용 능력.
- `can_do_examples`:
  - “자신의 방에 있는 물건 1~2개를 선택해서, ‘I have a [toy/bed/doll].’ 형태로 말하거나 단어만 말할 수 있다.”
  - “누구와 함께 사는지에 대해 ‘mom, dad, baby’ 등 단어 또는 ‘I live with my mom and dad.’와 같은 문장으로 표현할 수 있다.”

---

## 4. Cognitive Skills (인지 스킬)

### 4.1 COGN_ATTENTION_SESSION_01

- `skill_id`: `COGN_ATTENTION_SESSION_01`
- `name_kr`: 세션 내 지속 주의 집중
- `name_en`: Sustained Attention within Session
- `category`: `cognitive`
- `mode`: `receptive`
- `age_band`: `7-9`
- `unit`: `level_1_5`
- `is_core_metric`: `true`
- `description`:
  - 약 10~15분 길이의 세션 동안, 과제 수행 및 대화에 **지속적으로 참여**하는 능력.  
    (장시간 침묵, 과도한 이탈, 반복적인 “하기 싫어요” 신호 등은 낮은 레벨로 반영)
- `can_do_examples`:
  - “세션 중 최소 3~4개의 TaskAttempt에 응답한다.”
  - “관계 블록(R0~R4) 이후에도, 도중에 이탈하지 않고 세션 끝까지 함께한다.”

---

### 4.2 COGN_WORKINGMEM_2STEP_01

- `skill_id`: `COGN_WORKINGMEM_2STEP_01`
- `name_kr`: 두 단계 지시 따르기
- `name_en`: Following 2-step Instructions
- `category`: `cognitive`
- `mode`: `receptive`
- `age_band`: `7-9`
- `unit`: `level_1_5`
- `is_core_metric`: `false`
- `description`:
  - “먼저 ~~ 하고, 그다음에 ~~ 해줘.” 형태의 **2단계 지시**를 이해하고 수행하는 능력. (언어/놀이 상황 모두 포함)
- `can_do_examples`:
  - “예: ‘먼저 좋아하는 동물을 말하고, 그다음에 좋아하는 음식을 말해줘.’ 요청에 대해 두 항목 모두를 순서대로 말할 수 있다.”
  - “한 번에 기억하기 힘들어도, Popo가 다시 상기시켰을 때 수행을 마무리할 수 있다.”

---

### 4.3 COGN_FLEXIBILITY_TOPIC_01

- `skill_id`: `COGN_FLEXIBILITY_TOPIC_01`
- `name_kr`: 주제 전환 유연성
- `name_en`: Topic-switching Flexibility
- `category`: `cognitive`
- `mode`: `both`
- `age_band`: `7-9`
- `unit`: `level_1_5`
- `is_core_metric`: `false`
- `description`:
  - 한 주제(동물)에서 다른 주제(음식, 놀이 등)로 대화가 넘어갈 때, **과도한 저항 없이** 새로운 질문에 응답하려는 유연성.
- `can_do_examples`:
  - “동물 이야기에서 음식 이야기로 넘어갈 때, 새로운 질문에 대해 최소한 한 단어 수준의 응답을 시도한다.”
  - “주제 전환에 대해 ‘그만할래요’ 신호가 반복적으로 나타나지 않는다.”

---

## 5. Emotional & Social Skills (정서/사회성 스킬)

### 5.1 EMO_SELFREPORT_3POINT_01

- `skill_id`: `EMO_SELFREPORT_3POINT_01`
- `name_kr`: 3단계 기분 자기 보고
- `name_en`: 3-point Mood Self-report
- `category`: `emotional`
- `mode`: `expressive`
- `age_band`: `7-9`
- `unit`: `level_1_5`
- `is_core_metric`: `true`
- `description`:
  - “1: 피곤, 2: 보통, 3: 신남”과 같은 **간단한 척도** 중에서 자신의 현재 기분을 선택·표현하는 능력.
- `can_do_examples`:
  - “Popo가 1/2/3을 설명했을 때, 그중 하나를 선택해 말하거나 손가락/버튼으로 고를 수 있다.”
  - “여러 세션을 거치며, 기분 변화가 있을 때 다른 값을 선택하는 모습이 관찰된다.”

---

### 5.2 EMO_RESPONSE_PRAISE_01

- `skill_id`: `EMO_RESPONSE_PRAISE_01`
- `name_kr`: 칭찬/격려에 대한 정서적 반응
- `name_en`: Emotional Response to Praise & Encouragement
- `category`: `emotional`
- `mode`: `receptive`
- `age_band`: `7-9`
- `unit`: `level_1_5`
- `is_core_metric`: `false`
- `description`:
  - “잘했어!”, “굉장히 용감했어.”와 같은 칭찬/격려 메시지를 들었을 때, 표정/목소리/행동으로 **긍정적인 반응**을 보이는 정도. (STT/음성/행동 로그 기반)
- `can_do_examples`:
  - “칭찬 이후, 목소리 톤이 밝아지거나 추가 시도를 하려는 모습이 늘어난다.”
  - “‘또 해볼래요.’, ‘한 번 더요.’ 등 긍정적인 반응을 보일 수 있다.”

---

### 5.3 EMO_EXPRESS_PREFERENCE_01

- `skill_id`: `EMO_EXPRESS_PREFERENCE_01`
- `name_kr`: 선호/비선호 정서 표현
- `name_en`: Emotional Valence in Preferences
- `category`: `emotional`
- `mode`: `expressive`
- `age_band`: `7-9`
- `unit`: `score_0_100`
- `is_core_metric`: `true`
- `description`:
  - “좋아해요 / 싫어해요”와 같은 **정서적 태도**를 언어·표정·제스처로 표현하는 능력.  
    (언어 스킬 `LANG_VOCAB_PREFERENCE_01`와 깊게 연결되지만, 보다 정서적인 측면에 초점을 둔 스킬)
- `can_do_examples`:
  - “좋아하는 것에 대해 이야기할 때 목소리와 표정이 밝아지며, ‘좋아요’, ‘재밌어요’ 등의 표현을 사용할 수 있다.”
  - “조금 무섭거나 싫어하는 대상에 대해 ‘무서워요’, ‘싫어요’ 등을 말해볼 수 있다.”

---

### 5.4 EMO_SAFETY_SIGNAL_01

- `skill_id`: `EMO_SAFETY_SIGNAL_01`
- `name_kr`: 불편/중단 의사 표현 (안전 신호)
- `name_en`: Safety Signal & Opt-out Expression
- `category`: `emotional`
- `mode`: `expressive`
- `age_band`: `7-9`
- `unit`: `boolean`
- `is_core_metric`: `true`
- `description`:
  - “Pass”, “하기 싫어요”, “쉬고 싶어요” 등 **중단/거부 의사**를 명시적으로 표현할 수 있는 능력.  
    (서비스 철학상 매우 중요한 안전 관련 스킬)
- `can_do_examples`:
  - “Popo가 ‘말하기 싫으면 Pass라고 말해도 된다’고 안내했을 때, 필요시 실제로 ‘Pass’ 또는 이에 해당하는 표현을 사용할 수 있다.”
  - “과도한 불편 상황에서도 침묵만 유지하지 않고, 최소한의 거부 의사를 표현할 수 있다.”

---

## 6. 향후 확장 메모 (v0.1 기준)

- `language` 카테고리
  - WH-질문 세분화 (who/what/where/why 별도 스킬)
  - 이야기 구성(narrative) 상위 단계 (3문장 이상 스토리)
- `cognitive` 카테고리
  - 작업 전환(Task-switching), 계획(Planning) 등 고급 기능 추가
- `emotional` 카테고리
  - 감정 라벨(행복/슬픔/분노/불안 등) 구분 및 표현 스킬 추가
  - 자기조절(Regulation) 스킬: 쉬기 요청, 호흡/스트레칭 등

Phase 1에서는 위에 정의된 스킬들만 실제 DB 인스턴스로 생성하고,  
추후 언어치료사/교육 전문가의 피드백에 따라 `Skill_Dictionary_v0.2` 이상 버전으로 확장/수정합니다.
