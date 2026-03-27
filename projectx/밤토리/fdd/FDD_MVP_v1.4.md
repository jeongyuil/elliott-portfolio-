
# VOICE AI 교육 플랫폼 FDD (Final Design Document) – MVP v1.4

## 0. 문서 메타

- 문서명: VOICE AI 교육 플랫폼 FDD (Final Design Document) – MVP v1.4  
- 기준 온톨로지: **온톨로지 정의서 v0.1.1**  
- 작성자: 정유일 외 (Product / DS / Backend / ML 공동 문서)  
- 대상 시스템: 4~12세 아동 대상 음성 기반 영어 학습 AI “밤토리(가칭)” B2C 서비스  

---

## 1. 배경 및 목표

### 1.1 제품 목적

4–12세 아동을 대상으로, **대화형 Voice AI 튜터**를 통해  

- “재미있게 오래 말하게 하고”  
- “언어·인지 발달을 데이터로 추적”  
- “부모에게 이해하기 쉬운 리포트로 설명”  

하는 **구독형 영어/언어 학습 서비스**를 제공한다.

### 1.2 경쟁 포지셔닝

> **"Voice-First + 발달 추적"** 조합으로 차별화.  
> 듀오링고(게이미피케이션), 링고킥스(영상 콘텐츠) 대비 **음성 중심 인터랙션 + 언어 발달 데이터 기반 부모 리포트**가 핵심 가치.

### 1.3 핵심 성공 지표 (North Star Metrics)

| 지표 | 목표 | 측정 방식 |
|------|------|----------|
| **세션당 평균 발화 수** | ≥ 15회 | Utterance(speaker_type=child) 집계 |
| **D7 Retention** | ≥ 30% | 첫 세션 후 7일 내 재방문율 |
| **월간 리포트 열람률** | ≥ 60% | Report 생성 대비 delivered_at 비율 |

### 1.4 MVP 범위

**포함:**

1. 아동/부모 계정 & 기본 구독 상태 연동 (In-app billing 연동은 mock 또는 단순 플래그)
2. 음성 기반 세션:
   - 모바일 앱(또는 웹)에서 마이크 입력 → STT → LLM 대화 → TTS 응답  
   - 모바일 앱(또는 웹)에서 마이크 입력 → STT → LLM 대화 → TTS 응답  
   - **커리큘럼 Phase 1 (Week 1-4)만 포함**: 그 외 Phase는 v2.0 이후 적용
3. 도메인 온톨로지 기반 데이터 저장:
   - Child / FamilyAccount / Subscription / Session / Utterance / TaskAttempt / Skill / SkillLevel / Report
1. 월간(혹은 테스트 단계에서는 주단위) 리포트 자동 생성 (텍스트+그래프 중심, 템플릿 기반)
2. 내부용 간단 Admin/Console (optional):
   - Child/Session 리스트 조회
   - **Content Management**: 별도의 GUI CMS는 구축하지 않으며, Git + Script 기반의 파이프라인으로 관리 (비용 최소화)
   - 특정 Child의 SkillLevel, TaskAttempt, Utterance 히스토리 확인
6. **즉시 체험 모드 (Quick Trial)**:
   - 계정 생성 없이 device_id 기반 1회 무료 세션 제공
   - 체험 후 가입 유도 → Onboarding 마찰 감소
7. **Trial → Paid 전환 퍼널**:
   - D3: 푸시 알림 "아이가 3회 대화했어요! 리포트 미리보기"
   - D5: 이메일 "스킬 성장 그래프 공개"
   - D7: 인앱 배너 "Trial 종료 임박, 지금 구독 시 첫 달 20% 할인"

**제외(후속 버전):**

- 실제 결제 PG 연동  
- 전문 언어치료사 콘솔 & 코멘트 워크플로우  
- Neo4j 기반 추천/지식그래프 고급 분석  
- 정교한 레벨테스트/placement 테스트
- **프리토킹 모드 (Free Talk Mode)**: 자유 대화 기능은 v2.0에서 구현 예정 (Section 4.1 참고)

---


### 1.3 타깃 사용자 & 페르소나

- **🌟 Primary Learner (아동 = "이야기의 주인공")**  
  - 기준 페르소나: **7세, 내성적인 여자아이**, 한국어 모국어, 영어는 기초 수준  
  - 특성:
    - 새로운 사람/환경에서 긴장도가 높고 말을 꺼내기까지 시간이 걸림
    - 실수에 민감하고, 틀린 표현을 지적받으면 말하기 의욕이 빠르게 떨어질 수 있음
    - 좋아하는 주제(동물, 그림, 특정 캐릭터 등)에 대해선 길게 이야기할 여지는 있음
  - **역할 프레이밍: 주인공(Protagonist)**
    - 아이는 모든 스토리의 **주인공**이다. 단순한 학습자가 아니라, 우주 친구 Luna를 도와주는 "캡틴"이자 "모험의 리더"이다.
    - 제품 전반에서 **"네가 주인공이야"**라는 메시지를 일관되게 전달한다.
    - 큰 아이콘, 최소 텍스트, 듀오링고 스타일의 직관적인 UI (Kids View)
  - 제품 경험 목표:
    - "틀려도 괜찮은 안전한 공간"에서 **짧은 영어 문장이라도 스스로 말해본 경험**을 반복
    - Luna·Popo와의 관계를 통해 **'AI와 대화 = 재미있는 놀이'**로 인식하게 만들 것
    - **"내가 루나를 도와줬어!"**라는 성취감을 매 세션 느끼게 할 것

- **🤝 Parent (보호자 = "Helper")**  
  - 30–40대 맞벌이 또는 양육 전담 보호자
  - **역할 프레이밍: 헬퍼(Helper)**
    - 부모는 직접 학습에 참여하지 않으며, **아이의 성장을 지켜보고 응원하는 조력자** 역할이다.
    - Parent View에서 발달 리포트를 확인하고, 가정에서의 코칭 팁을 실천하는 데 집중한다.
    - 아이의 학습 세션에는 접근하지 않음으로써, **아이의 자율성과 주인공 의식**을 존중한다.
  - 니즈:
    - 아이가 "얼마나, 무엇을, 어떻게" 말하고 있는지 **정량 + 정성**으로 보고 싶음
    - 단순 점수보다 **강점/약점 스킬과 집에서의 구체적인 코칭 팁**을 선호
  - 제품 경험 목표:
    - 월 1회 리포트에서 "우리 아이의 지난달 변화"를 **1분 이내에 이해**할 수 있어야 함
    - 장기적으로는 "이 서비스 덕분에 우리 아이가 영어를 무서워하지 않는다"는 체감

- **확장 타깃**  
  - 온톨로지의 `age_band`(4–6, 7–9, 10–12)에 따라 대화 난이도와 스킬 목표를 확장하되,  
    FDD_MVP_v1.2는 **7세 페르소나**를 1차 기준으로 삼는다.
  - 향후 추가 개발 시 **7세 이상의 페르소나**를 우선순위로 삼는다.

### 1.4 교육 목표 & 핵심 평가 프레임워크

- **코어 교육 목표 (W1–W4 기준)**  
  1. 영어 말하기에 대한 **정서적 저항 감소**  
     - “영어로 말해보는 것 자체가 부담스럽지 않다”는 상태 만들기  
  2. 기본 **자기소개 + 일상 묘사 플로우** 형성  
     - 이름/나이/좋아하는 것/하루 루틴을 간단한 영어 문장으로 표현
  3. 언어 스킬의 **구조적 성장 데이터** 확보  
     - 어휘, 발음, 문장 구성, 화용(상황에 맞게 말하기) 영역별 TaskAttempt 기록
    
- **스킬 레벨링 프레임워크**  
  - 온톨로지 `Skill`–`SkillLevel`–`TaskAttempt` 구조를 그대로 사용한다.
  - W1–W4 동안 특히 아래 카테고리의 스킬을 집중 추적:
    - `phonology/pronunciation` (발음 명료도, pronunciation_score)
    - `vocabulary` (word_count, unique_word_count, 핵심 토픽 어휘 커버리지)
    - `grammar/syntax` (기본 SVO 구조, 간단한 현재형 문장 구성)
    - `pragmatics` (질문 이해도, on/off-topic 여부, 차례 지키기)
  - 각 스킬은 `mode`(receptive / expressive / both)와 `age_band`(예: 7–9세)를 가지며,  
    **“또래 대비 어느 수준인지”**를 `percentile_by_age`로 표현한다.
  - 실제 스킬 인스턴스 목록, 레벨 설명, `can_do_examples` 등 상세 정의는 별도 문서 **`Skill_Dictionary_v0.1.md`에서 관리하며,  
    이 FDD에서는 구조와 연계 방식만 정의한다.

- **평가 단위와 지표 연결**  
  - 미시 단위:
    - `TaskAttempt` 기준으로 **정답/부분정답/오답/오프토픽** 및 `instruction_understood`를 저장
    - 단일 과제 수준에서 “질문 이해 vs 표현 능력”을 분리 평가
  - 중간 단위:
    - 세션 단위로 `engagement_score`, `attention_score`, 시도된 TaskAttempt 수, 성공률을 집계
  - 거시 단위:
    - 월 단위로 `SkillLevel` 스냅샷을 생성하고, 3/6/12개월 시계열을 통해 추세를 관찰
    - `Metric` 엔티티를 통해 “어휘력 향상률, 발화량 증가율, 세션 유지율” 등을 정의

- **보호자 커뮤니케이션 원칙**  
  - 내부적으로는 세밀한 수치와 분포를 관리하되,  
    리포트에서는
    - 3~5개의 핵심 Skill에 대해
    - “지난달 대비 ↑ / → / ↓” 형태의 **간단한 시각 언어**와
    - “집에서 해볼 수 있는 1~2개 행동 가이드”를 함께 제공한다.

## 2. 전체 아키텍처

### 2.1 컴포넌트 개요

1. **Client (앱 또는 웹 MVP)**  
   - 마이크 입력 → 서버로 PCM/OGG 업로드  
   - 서버에서 받은 TTS 오디오 스트림 재생 (**Streaming supported**)
   - UI: 세션 시작/종료, 아바타 캐릭터, 부모용 대시보드(기초)
   - **Visual State Feedback**: 음성 인식 중/처리 중/발화 중 상태를 파형(Waveform)이나 캐릭터 애니메이션으로 명확히 시각화 (In-app visual feedback indispensable)
   - **Silence Detection**: 비용 및 지연 시간 최적화를 위해 **On-device VAD**(WebAudio/Native) 적용. 침묵 감지 시 서버 전송 중단 및 '재촉구' 이벤트 트리거.

2. **API Backend (FastAPI, Python)**  

   주요 모듈:
   - Auth & 계정 / Child 관리  
   - Session Orchestrator (세션 상태 머신)  
   - Curriculum Engine (Activity/Task 흐름 제어)  
   - Speech Pipeline (STT, **Streaming TTS**, LLM 호출)  
   - Evaluation Engine (TaskAttempt, SkillLevel 계산)  
   - Report Generator
   - **Fallback Handler**: 외부 서비스(STT/LLM/TTS) 장애 시 사전 정의된 응답 풀에서 대체 메시지 반환

3. **데이터베이스**

   - **PostgreSQL**
     - 모든 온톨로지 엔티티 테이블화  
     - 일부 JSONB 컬럼 (extra_features, topic_tags, metadata 등)
   - **Object Storage (S3 호환)**  
     - `Session.raw_audio_path`가 가리키는 오디오 파일
   - (옵션, v2) **GraphDB (Neo4j)**: 현재 FDD에서는 스키마 설계까지만, 실제 도입은 후속.

4. **ML/LLM 서비스**

   - STT 엔진 (예: OpenAI, Whisper, 기타 SaaS)  
   - LLM (대화/피드백 생성, 리포트 요약)  
   - 평가 모델 (발음/유창성/문법 스코어링; 초기에는 rule + LLM 기반)

### 2.2 오디오 규격

| 구분 | 규격 | 비고 |
|------|------|------|
| **업로드 포맷** | OGG Opus | 클라이언트 → 서버 (압축 효율 우수) |
| **다운로드 포맷** | MP3 / OGG | 서버 TTS → 클라이언트 |
| **샘플레이트** | 16kHz mono | STT 최적 성능 |
| **청크 크기** | 100ms | 스트리밍 전송 단위 |
| **최대 발화 길이** | 30초 | 단일 Utterance 제한 |

---

## 3. 도메인 모델 (온톨로지 v0.1.1 적용 요약)

> 상세 스키마/필드는 「온톨로지 정의서 v0.1.1」을 단일 소스로 사용하고,  
> 이 FDD에서는 **MVP 구현 시 반드시 사용하는 필드**만 강조한다.

### 3.1 핵심 엔티티 & MVP 사용 필드

### 3.1.1 FamilyAccount / Child

**FamilyAccount**

- `family_id`  
- `parent_name`  
- `contact_email`  
- `status`  

**Child**

- `child_id`, `family_id(FK)`  
- `name`  
- `birth_date`  
- `gender`  
- `primary_language`, `secondary_language`  
- `development_stage_language`  
- `preferences_topics`  

**MVP 사용 케이스**

- 부모 Onboarding: FamilyAccount 생성 + Child 1–2명 연결  
- UI에서 Child 프로필 기반으로 **커리큘럼 age band 추천**

---

### 3.1.2 SubscriptionPlan / Subscription

**SubscriptionPlan (seed 데이터)**

- `plan_id`  
- `plan_name` (basic/standard/premium)  
- `monthly_price`  
- `allowed_sessions_per_week`  
- `report_type`  

**Subscription**

- `subscription_id`  
- `family_id`  
- `plan_id`  
- `status` (paid_good_standing, trial, grace, …)  
- `start_date`  
- `billing_cycle`  
- `auto_renew`  

**MVP 정책**

- 결제 시스템 실제 연동 전까지는:
  - `trial` 또는 `paid_good_standing` 상태를 Admin에서 수동 세팅  
  - **활성 상태(active)** = status ∈ {`paid_good_standing`, `paid_pending_cancel`, `grace`, `trial`}  
  - inactive(`hold`, `stopped`)이면 Session 생성 불가
  - **Session Limits**: MVP 단계에서는 일일 최대 세션 수 또는 주간 총 발화량 제한을 두어 과금/중독 방지

---

### 3.1.3 Session / SessionActivity

**Session**

- `session_id`, `child_id`, `subscription_id`  
- `start_time`, `end_time`, `duration_seconds`  
- `session_type` (free_talk / curriculum / assessment / game)  
- `language_mode` (ko_only/en_only/mixed)  
- `curriculum_unit_id` (nullable)  
- `engagement_score`, `attention_score`, `emotional_state_overall`  
- `raw_audio_path`, `stt_processed`  
- `audio_retention_level`, `flag_for_expert_review`  

**SessionActivity**

- `session_activity_id`, `session_id`, `activity_id`  
- `order_index`, `started_at`, `ended_at`, `status`  

**MVP 전략**

- 1개의 Session은 보통 3–6개의 Activity로 구성  
- “권별(7세 여아 페르소나) 커리큘럼” 문서의 유닛을 `CurriculumUnit` / `Activity`로 맵핑 후,
  - Session 시작 시 CurriculumUnit 선택  
  - Activity 리스트 순차 실행 (단, 간단한 분기 정도 허용)

**Session 상태 머신 (State Machine)**:

```
[IDLE] --start--> [ACTIVE] --pause--> [PAUSED]
                      |                   |
                      v                   v
                  [ENDED] <--resume-- [PAUSED]
                      ^
                      |
               [ACTIVE] --timeout/error--> [ENDED]
```

- **IDLE**: 세션 생성 전
- **ACTIVE**: 대화 루프 진행 중 (child/ai 발화 교환)
- **PAUSED**: 연속 Timeout 또는 사용자 일시정지
- **ENDED**: 정상 종료 또는 비정상 종료

**비정상 종료 처리 정책**:
- 앱 강제 종료(App Kill) 시: 클라이언트 heartbeat 5분 미수신 → PAUSED 전환
- PAUSED 상태 5분 유지 후 미복귀 시 → ENDED 전환 (reason: `abnormal_termination`)
- 미완료 세션은 `flag_for_expert_review = false`, 통계 집계 시 별도 구분

상태 전이 시 Redis에 `session:{id}:state` 키로 현재 상태 저장하여 동시성 이슈 방지.

---

### 3.1.4 Utterance

**Utterance**

- `utterance_id`, `session_id`, `session_activity_id`  
- `turn_index`, `speaker_type (child/ai)`  
- `text_raw`, `text_normalized`, `is_text_normalized`  
- `language`, `dominant_language`, `language_mix_ratio_ko`, `language_mix_ratio_en`  
- `word_count`, `unique_word_count`, `avg_sentence_length`  
- `pronunciation_score`, `fluency_score`  
- `emotion_label`  
- `skill_ids` (array), `error_categories` (array)  
- `utterance_role`, `expected_child_response_type`  
- `stt_engine`, `stt_model_version`, `stt_confidence`  
- `scoring_model_version`, `scoring_reference`  

**구현 규칙**

- **child 발화:**
  - STT 결과 → `text_raw`  
  - normalization 로직 (기본 lower, punctuation 정리) → `text_normalized`  
  - 발음/유창성 점수는 평가 모델/LLM에서 계산 후 저장  

- **ai 발화:**
  - LLM 응답 텍스트 저장 (`text_raw = text_normalized`)  
  - `utterance_role`, `expected_child_response_type` 필수 세팅  
    (나중에 TaskAttempt 연결 키로 활용)

---

### 3.1.5 TaskDefinition / TaskAttempt

**TaskDefinition (템플릿)**

- `task_definition_id`, `activity_id`  
- `prompt_template`  
- `expected_response_pattern`  
- `target_skill_ids`  
- `difficulty_level`  

**TaskAttempt**

- `task_attempt_id`  
- `activity_id`, `child_id`, `session_id`  
- `task_definition_id (nullable)`  
- `expected_response_pattern`  
- `evaluated_correctness` (correct/partially_correct/incorrect/off_topic/not_applicable)  
- `related_utterance_ids (array<Utterance FK>)`  
- `instruction_understood` (yes/partially/no)  

**MVP 사용 시나리오**

- 커리큘럼 기획서에 있는 “질문/과제” 단위를 TaskDefinition으로 설계  
- 세션 중:
  1. AI가 질문(utterance_role = `prompt`, expected_child_response_type 지정)
  2. Child의 1~N개 발화 묶음을 하나의 TaskAttempt로 평가
  3. 평가 결과는 우선 LLM 기반 **룰+프롬프트 평가**로 구현

- `instruction_understood = no`인 TaskAttempt가 누적되면  
  커리큘럼 수정 대상 / 난이도 과도 신호로 활용

---

### 3.1.6 Skill / SkillLevel

**Skill**

- `skill_id`, `name`, `category (language/cognitive/emotional)`  
- `mode (receptive/expressive/both)`  
- `age_band`, `can_do_examples`  
- `skill_schema_version`  

**SkillLevel**

- `skill_level_id`, `child_id`, `skill_id`, `snapshot_date`  
- `raw_score`, `level`, `percentile_by_age`  
- `trend_direction`  
- `source (ai_auto/expert_manual/hybrid)`  
- `evaluation_method`, `evaluation_model_version`, `skill_schema_version`  

**MVP 정책**

- 처음엔 스킬 셋을 **얇게 시작**  
  - 예: `vocabulary_expressive_basic`, `pronunciation_en`, `sentence_grammar_basic`, `pragmatic_turn_taking`
- SkillLevel은 **월간 리포트 생성 직전** 최신 스냅샷 생성:
  - `source = ai_auto`  
  - `evaluation_method = "rule_v0.1"` (참조: **도메인 온톨로지 정의서 Appendix 9. 리포트 Metric 수식**)
  - `evaluation_model_version = "v0.1"`  
  - `skill_schema_version = "v0.1"`

---


### 3.1.7 CurriculumUnit / Activity

**CurriculumUnit**

- `curriculum_unit_id`, `title`, `description`  
- `age_min/age_max`, `target_skills`  
- `difficulty_level`, `language_mode`  

**Activity**

- `activity_id`, `curriculum_unit_id`, `name`  
- `activity_type (story/qa/role_play/game/assessment)`  
- `target_skills`  
- `instructions_for_ai`  
- `prompt_version` ← **신규**: 프롬프트 변경 시 버전 관리 (A/B 테스트, 롤백 지원)
- `estimated_duration_minutes`
- `intro_narrator_script` ← **신규**: 진입 전 나레이션 (제3자 관점, TTS Only)
- `transition_trigger` ← **신규**: 참여 모드 전환 트리거 (예: "Go!", "Open!")  

**MVP 연결**

- **권별(7세 여아 페르소나) 커리큘럼**  
  - CurriculumUnit: “권” 단위  
  - Activity: “에피소드/활동” 단위로 맵핑
- `instructions_for_ai`에는:
  - Activity에서 AI의 톤/질문 방식/피드백 규칙을 자연어로 담아  
  - 세션 중 LLM 프롬프트에 그대로 붙인다.

#### 캐릭터 시스템 (Triad Model)

| 캐릭터 | **Luna (루나)** | **Popo (포포)** | **별이 = 아이 (주인공)** |
|--------|----------------|-----------------|-----------------|
| **정체성** | 우주에서 온 아이 (주인공과 비슷한 나이대의 살아있는 생명체) | 정부에서 파견된 비밀 요원. 친절하고 아이를 사랑하는 마음의 소유자 | **이야기의 주인공** — 모험의 리더, 캡틴 |
| **역할** | The Learner (배우는 자) — 친구 같은 친밀감 형성 | The Coach (코치) — 훌륭한 코치, 정서적 공감 | The Protagonist (주인공) — 루나를 도와주는 선생님 |
| **언어** | **English Only** (100%) | 한국어+영어 (korean_ratio에 따라 비율 조정) | User Voice (한국어+영어) |
| **특성** | 엉뚱함, 실수 투성이, 호기심, **살아있는 친구 느낌** | 친절함, 따뜻함, 아이를 사랑하는 마음, 코칭 전문가 | 사용자 (주인공 역할) |
| **음성** | High-pitched (Disney Style, 활발한 어린 목소리) | 따뜻한 코치 목소리 (shimmer) | User Voice |

> 💡 **역멘토링(Reverse Mentoring)**: 아이(주인공)가 우주에서 온 친구(루나)에게 영어를 가르쳐주는 구조.
> 아이는 단순 학습자가 아닌 **"캡틴", "선생님"**으로서 주도권을 갖는다.

#### 3.1.7.1 [신규] 나레이터-주인공 전환 구조 (Interactive Story Flow)

모든 커리큘럼 세션은 **"동화책을 듣는 청중"**에서 **"이야기 속 주인공"**으로 자연스럽게 전환되는 3단계 플로우를 따른다.

1.  **Phase 1: Listen Mode (동화책 나레이션)**
    - **화자:** Narrator (동화책을 읽어주는 따뜻한 화자)
    - **화면:** 3인칭 관점 (시네마틱 연출)
    - **상태:** 마이크 Off / 터치 Off
    - **내용:** "옛날 옛적에~" 식으로 시작하여, 세계관 설정, 이전 줄거리 요약, 현재 상황 설명
    - **목적:** 동화책을 읽어주듯이 몰입감을 조성하여 아이가 이야기 세계로 자연스럽게 진입

2.  **Phase 2: Transition Mode (주인공 진입)**
    - **화자:** Popo (코치) 또는 Narrator
    - **화면:** 1인칭 시점으로 줌인(Zoom-in) 또는 전환 효과
    - **상태:** 마이크 **On** (특정 트리거 단어 대기)
    - **내용:** "이제 네 차례야!", "주문을 외쳐봐!"라며 **주인공으로서의 참여** 유도
    - **트리거:** "Go!", "Open!", "Start!" 등 간단한 발화 감지 시 Phase 3으로 진입

3.  **Phase 3: Participation Mode (상호작용)**
    - **화자:** Luna & Popo & 아이(주인공)
    - **화면:** 1인칭 시점 (루나와 눈맞춤)
    - **상태:** Interactive Loop (STT/LLM/TTS)
    - **내용:** 본 세션의 핵심 활동 진행 — 아이가 **주인공으로서** 루나를 도와주는 구조

#### Phase 구조 (MVP Scope: Phase 1 Only)

|     Phase      | 주제                      |  Week   | CurriculumUnit 예시                                            | 비고         |
| :------------: | ----------------------- | :-----: | ------------------------------------------------------------ | ---------- |
| 🟢 **Phase 1** | Bonding (관계 형성)         |  W1~W4  | Earth Crew, Lost Parts, Rocket Fuel, Disguise                | **MVP 대상** |
| 🔵 **Phase 2** | Adventure (생활 규칙)       |  W5~W8  | Alien Virus, School Infiltration, Weather Error, Galaxy Shop | v2.0 예정    |
| 🟣 **Phase 3** | Galaxy Report (표현/창작)   | W9~W12  | My Crew, Emotion Chip, Dream Planet, Message to Space        | v2.0 예정    |
| 🎓 **Phase 4** | Galaxy Academy (사회성/리딩) | W13~W16 | Hologram Call, Show & Tell, Playground Rules, Alien Alphabet | v2.0 예정    |

#### Phase 1 상세 커리큘럼 (Week 1-4)

**W1: Earth Crew (대원 등록)**
- **목표 스킬**: Greeting, Self-Introduction, Asking Names
- **주요 문장**: "Hello", "What is your name?", "I am [Name]"
- **시나리오**:
  1. 루나가 불시착 후 별이를 처음 만남. (경계/호기심)
  2. 포포가 "지구 대원으로 등록하려면 이름을 알려줘"라고 코칭.
  3. 별이가 이름을 말하면 루나가 "Captain [Name]!"이라고 부르며 따름.

**W2: Lost Parts (사라진 부품)**
- **목표 스킬**: Furniture nouns, Prepositions (in, on, under)
- **주요 문장**: "Where is it?", "It is on the bed", "Table/Chair/Bed"
- **시나리오**:
  1. 우주선 수리를 위해 부품(톱니바퀴 등)을 찾아야 함.
  2. 루나가 "Where is the gear?"라고 물으며 방을 뒤짐.
  3. 별이가 가구 위/아래를 가리키며 위치를 알려줌.

**W3: Rocket Fuel (로켓 연료 구하기)**
- **목표 스킬**: Fruits, Colors, "I like/don't like"
- **주요 문장**: "Do you have an Apple?", "Red/Blue/Yellow", "Yummy/Yucky"
- **시나리오**:
  1. 루나가 배고파서(연료 부족) 힘이 없음.
  2. 냉장고를 열고 색깔/과일을 물어봄. (빨간 공 = 사과 오해)
  3. 별이가 과일을 주면 색깔과 맛을 이야기함.

**W4: Disguise (지구인 변장)**
- **목표 스킬**: Clothing, Body parts, "Put on"
- **주요 문장**: "Put on the shirt", "Hat/Shoes/Pants", "It fits!"
- **시나리오**:
  1. 밖(놀이터)에 나가기 위해 루나를 지구 아이처럼 변장시켜야 함.
  2. 루나가 바지를 머리에 쓰는 등 실수 연발.
  3. 별이가 올바른 착용법(Put on your pants)을 알려줌.

#### Triad 대화 흐름 (4단계 루프)

```
[상황 발생] → [포포의 코칭] → [아이(주인공)의 발화] → [루나의 리액션]
```

1. **상황 발생**: 루나가 지구 물건을 보고 놀라거나 혼란 (예: "Is that a Bomb?")
2. **포포 코칭**: 한국어로 힌트 제공 (예: "캑틴! Apple이라고 알려줘")
3. **아이(주인공) 발화**: 사용자가 영어로 대답 (예: "No, it's an Apple!")
4. **루나 리액션**: 이해 및 감사 (예: "Apple is safe! Thank you, Captain!")

#### 난이도 파라미터

| 파라미터 | 설명 | MVP 기본값 | 조정 시점 |
|----------|------|-----------|----------|
| `clumsiness_level` | 루나의 멍청함 정도 (0~100) | 80 | Phase 진행 시 감소 |
| `korean_ratio` | 포포의 한국어 비율 (0~100) | 50 | Phase 진행 시 감소 |
| `response_latency_target` | 루나 응답 목표 시간 | 1.5초 | 고정 |

#### 안전 키워드 (Red Flag Alert)

- **위기 키워드**: "무서워", "싫어", "때렸어" 등 반복 감지 시
- **동작**: 즉시 부모에게 푸시 알림 발송 (Event: `RedFlagDetected`)
- **PII 마스킹**: 주소, 전화번호 발화 시 즉시 마스킹 처리 및 저장 금지

#### CurriculumUnit Seed 데이터 예시

```json
{
  "curriculum_unit_id": "phase1_w1_earth_crew",
  "title": "Earth Crew (대원 등록)",
  "phase": 1,
  "week": 1,
  "age_min": 4,
  "age_max": 7,
  "target_skills": ["greeting", "self_introduction", "name"],
  "difficulty_level": 1,
  "language_mode": "mixed",
  "clumsiness_level": 80,
  "korean_ratio": 50
}
```

---

### 3.1.8 Report / ReportSkillSummary

**Report**

- `report_id`, `child_id`, `family_id`  
- `period_start_date`, `period_end_date`  
- `report_type` (pdf_basic/pdf_ai_video/pdf_ai_video_expert)  
- `template_id`, `locale (ko_KR/en_US)`  
- `summary_text`, `strengths_summary`, `areas_to_improve`, `recommendations_next_month`  
- `delivery_channel`, `delivered_at`  

**ReportSkillSummary**

- `report_skill_summary_id`, `report_id`, `skill_id`  
- `level`, `summary_for_parent`  

**MVP 리포트 플로우**

1. 기간 내 Session/TaskAttempt/SkillLevel 집계  
2. 스킬별 핵심 문장 생성:
   - 예: “단문 자기소개는 대부분 자연스럽게 말할 수 있어요.”
3. LLM에 템플릿 + 요약 데이터 입력 →  
   `summary_text`, `strengths_summary`, `areas_to_improve`, `recommendations_next_month` 생성
4. Report + ReportSkillSummary DB에 저장  
5. 부모 앱/웹에서 카드 형태로 표시

---

### 3.2 Event / Metric / ErrorCategory

**Event**

- `event_id`, `event_type`, `occurred_at`  
- `child_id`, `family_id`, `session_id`, `subscription_id` (optional)

**Metric**

- `metric_id`, `name`, `category`, `description`, `calculation_formula`, `unit`, `target_value`

**ErrorCategory**

- `error_category_id`, `name`, `description`, `category`  
  - 예: `pronunciation_error`, `grammar_error`, `off_topic`

**MVP 최소 구현**

- Event:
  - SessionStarted, SessionEnded, UtteranceRecorded, ReportGenerated 구현
- Metric/ErrorCategory:
  - 코드 테이블 정의 후, 향후 Admin/대시보드에서 활용

---

## 4. 기능 설계

### 4.0 API 엔드포인트 명세 (Dual-View Architecture)

> 아이(Kids View)와 부모(Parent View)의 API를 네임스페이스로 덮리 분리한다.

**인증 (Auth)** — `/v1/auth/*`

| Method | Endpoint | 설명 | 주요 Request/Response |
|--------|----------|------|----------------------|
| `POST` | `/v1/auth/signup` | 부모 계정 생성 | `{email, password, parent_name}` → `{family_id, access_token}` |
| `POST` | `/v1/auth/login` | 로그인 | `{email, password}` → `{access_token, family_id}` |
| `POST` | `/v1/auth/select-child` | 아이 프로필 선택 → child_token 발급 | `{child_id, pin?}` → `{child_token, child_name}` |

**Parent View** — `/v1/parent/*` (Bearer family_token)

| Method | Endpoint | 설명 | 주요 Request/Response |
|--------|----------|------|----------------------|
| `POST` | `/v1/parent/children` | 자녀 프로필 생성 | `{name, birth_date, pin?, avatar_id?}` → `{child_id}` |
| `GET` | `/v1/parent/children` | 자녀 목록 조회 | → `[{child_id, name, avatar_id, ...}]` |
| `GET` | `/v1/parent/children/{child_id}` | 자녀 정보 조회 | → `{child_id, name, birth_date, ...}` |
| `GET` | `/v1/parent/reports` | 리포트 목록 조회 | `?child_id=` → `[{report_id, period, ...}]` |
| `GET` | `/v1/parent/reports/{id}` | 리포트 상세 조회 | → `{summary, skills, ...}` |

**Kids View** — `/v1/kid/*` (Bearer child_token)

| Method | Endpoint | 설명 | 주요 Request/Response |
|--------|----------|------|----------------------|
| `POST` | `/v1/kid/sessions` | 세션 시작 | `{session_type}` → `{session_id}` |
| `POST` | `/v1/kid/sessions/{id}/utterances` | 발화 업로드 | `{audio_chunk}` → `{utterance_id, ai_response_audio_url}` |
| `POST` | `/v1/kid/sessions/{id}/end` | 세션 종료 | → `{duration, engagement_score}` |

> Kids View에서는 `child_id`를 body에 보내지 않습니다. 토큰에서 자동 추출됩니다.

**체험 (Trial)** — `/v1/trial/*` (비인증)

| Method | Endpoint | 설명 | 주요 Request/Response |
|--------|----------|------|----------------------|
| `POST` | `/v1/trial/quick-start` | **즉시 체험** (계정 없이) | `{device_id}` → `{temp_session_id, token}` |

> 상세 스키마는 OpenAPI 3.0 문서로 별도 관리

#### User Journey Note: One-Handed Onboarding
- **원칙**: 바쁜 부모(Helper)를 위해 "가입보다 가치 전달을 먼저" 수행한다.
- **Flow**: [앱 설치] → [Quick Trial (즉시 체험)] → [아이의 반응 확인] → [계정 생성 (자동 연동)]
- 모든 입력 폼은 한 손으로 조작 가능해야 하며, 복잡한 설정은 가입 후로 지연시킨다.

**멱등성(Idempotency) 정책**:
- `POST /v1/kid/sessions/{id}/utterances` 호출 시 `X-Idempotency-Key` 헤더 필수
- 동일 키로 재전송 시 기존 응답 반환 (네트워크 재시도로 인한 중복 발화 방지)
- 키 유효 기간: 5분 (Redis TTL)

---

### 4.1 프리토킹 모드 (Free Talk Mode) – **v2.0 예정**

> ⚠️ **MVP 제외**: 본 섹션은 v2.0에서 구현 예정입니다. 현재 MVP에서는 제외됩니다.

> 💡 **차별화 포인트**: 경쟁사(듀오링고, 링고킥스)는 구조화된 레슨만 제공.  
> 밤토리는 **자유 대화 모드**로 "진짜 영어 친구"처럼 느껴지는 경험 제공.

#### 목적 및 포지셔닝

| 구분 | 커리큘럼 모드 | 프리토킹 모드 |
|------|-------------|--------------|
| **목표** | 체계적 스킬 학습 | 자유로운 표현력 및 자신감 향상 |
| **구조** | Phase/Week 기반 진행 | 주제 자유 선택 |
| **평가** | TaskAttempt 기반 정량 평가 | 발화량/다양성 중심 정성 평가 |
| **비즈니스** | 구독 핵심 가치 | **리텐션 부스터** (매일 돌아오게) |

#### 프리토킹 대화 흐름

```
[1. 주제 선택] → [2. 루나의 호기심 질문] → [3. 자유 대화] → [4. 하이라이트 저장]
```

1. **주제 선택**: 아동이 관심사 선택 (우주, 공룡, 케이크 만들기 등)
   - 또는 "오늘 뭐 했어?" 일상 기반 시작
2. **루나의 호기심 질문**: Luna가 주제에 대해 영어로 질문 (멍청한 외계인 톤 유지)
3. **자유 대화**: 정해진 스크립트 없이 LLM 기반 자연스러운 대화
4. **하이라이트 저장**: 가장 긴/창의적 발화를 30초 클립으로 저장 → 부모 리포트

#### 세션 파라미터

| 파라미터 | 값 | 설명 |
|----------|---|------|
| `session_type` | `free_talk` | 세션 유형 |
| `max_duration` | 15분 | 과몰입 방지 |
| `max_turns` | 30턴 | 비용 제한 |
| `topic` | 사용자 선택 or `random` | 주제 |
| `curriculum_unit_id` | `null` | 커리큘럼 미연결 |

#### 수집 데이터 및 활용

| 데이터 | 활용 |
|--------|------|
| **총 발화량** | 리포트 "이번 주 자유 대화 시간" |
| **새로운 단어** | 어휘 확장 그래프 |
| **주제 선호도** | 커리큘럼 개인화 추천 |
| **감정 분석** | 긍정적 경험 빈도 추적 |

#### 수익화 전략 (Premium Upsell)

| 플랜 | 프리토킹 제공량 | 가격 신호 |
|------|---------------|----------|
| **Basic** | 주 1회, 5분 | 맛보기 |
| **Standard** | 주 3회, 10분 | 핵심 가치 |
| **Premium** | 무제한, 15분 | 파워 유저 |

> 💰 **리텐션 효과**: 프리토킹은 "매일 루나랑 놀고 싶어" 심리 유발 → D7/D30 Retention 핵심 드라이버

---

### 4.2 세션 생성 플로우

1. 클라이언트에서 “세션 시작” 요청  
2. API:
   - Subscription 상태 체크 (active 아니면 4xx 반환)
   - Session row 생성 (session_type, curriculum_unit_id 결정)
   - SessionActivity 리스트 생성 (해당 CurriculumUnit의 Activity 순서대로)
3. 클라이언트에 `session_id` 반환

---

### 4.3 대화 루프

반복:

1. 클라이언트: 음성 Chunk 업로드 (child 발화)
2. Backend:
   - STT 호출 → `text_raw`, `stt_confidence`
   - Utterance row 생성 (speaker_type = child)
   - **예외 처리**: `text_raw`가 비어있거나 소음만 있는 경우, LLM 호출 없이 "잘 못 들었어" 등의 Fallback 메시지 처리 (비용 절감)
   - **아동 발화 안전 필터링**: 욕설/위험 표현 감지 시 → Utterance에 `flag_safety_concern = true` 세팅, 세션 종료 후 보호자에게 알림 발송 (Event: `SafetyConcernDetected`)
3. 현재 `SessionActivity`와 관련 TaskDefinition 조회
4. LLM 프롬프트 구성:
   - Activity.instructions_for_ai  
   - 직전 TaskAttempt/Utterance 요약  
   - Child 스킬 레벨 요약 (optional)
5. LLM 응답:
   - AI 발화 텍스트  
   - 필요 시 평가/피드백 문장 포함
   - **Safety Check**: 욕설/유해 표현 필터링 (Rule-based or LLM guardrail)후 최종 텍스트 확정
6. Utterance row 생성 (speaker_type = ai, utterance_role 등 세팅)
7. TTS 호출 → 오디오 URL → 클라이언트 전달
8. 특정 조건 시 TaskAttempt 평가 수행:
   - “질문 후, child 발화 N개 묶음”을 하나의 TaskAttempt로 판단  
   - LLM/RULE 기반으로 `evaluated_correctness`, `instruction_understood` 계산

8. **Silence / Timeout 처리 (Loop Exception)**:
   - 클라이언트 VAD에서 N초(예: 7초)간 발화가 없으면 `TIMEOUT` 이벤트 전송
   - Backend:
     - `re-prompting` 로직 수행 (다시 질문하거나, 힌트를 주는 짧은 AI 발화 생성)
     - 연속 M회 Timeout 시 세션 자동 일시정지 또는 '다음에 할까?' 유도

---

### 4.4 세션 종료

- 클라이언트에서 “종료” or 타임아웃  
- Backend:
  - `end_time`, `duration_seconds` 계산  
  - engagement_score, attention_score:
    - 세션 길이 + child 발화 비율 + 오프토픽 비율 등으로 rule-based 계산
  - Event(SessionEnded) 기록  
  - 필요 시 `flag_for_expert_review` 세팅 로직:
    - 특정 오류 패턴/감정(negative) 과다 시 True

---

### 4.5 SkillLevel 계산 (스냅샷 생성)

**주기:**  

- MVP에서는 **월 1회 배치 (또는 dev 단계에서 수동 트리거)**

**로직(예시):**

1. 해당 기간 내 TaskAttempt, Utterance 집계
2. 스킬별 rule:
   - vocabulary_expressive_basic:
     - unique_word_count 평균 / 특정 기준 이상이면 score ↑
   - pronunciation_en:
     - child utterance의 pronunciation_score 평균
3. score → level 매핑:
   - 예: 0–40: level 1, 40–70: level 2, 70–100: level 3
4. SkillLevel row upsert:
   - `source = ai_auto`  
   - `evaluation_method = "rule_v0.1"` (참조: **도메인 온톨로지 정의서 Appendix 9. 리포트 Metric 수식**)
   - `evaluation_model_version = "v0.1"`  
   - `skill_schema_version = "v0.1"`

---

### 4.6 Report 생성

1. 기간 내 데이터 수집:
   - Session, TaskAttempt, Utterance, SkillLevel
2. Feature 정리:
   - 총 세션 수, 총 발화 수, 평균 발화 길이  
   - 스킬별 level 변화, trend_direction
3. LLM Prompt:
   - “아동의 한 달간 학습 활동 요약을 부모에게 설명하라” 템플릿  
   - 입력: 수치, 예시 발화 일부, 스킬 수준 변화
4. LLM 결과를 Report + ReportSkillSummary에 저장
5. 부모 화면에서 카드 형태로 표시

---


### 4.3 대화 에이전트(Luna & Popo) 행동 명세

본 절은 **세션 Orchestrator가 LLM 프롬프트를 구성할 때 반드시 준수해야 할 계약**을 정의한다.  
목표는 “누가, 어떤 언어로, 어떤 역할로 말하는지”를 일관되게 유지하여, 교육 효과와 로그 분석 품질을 동시에 확보하는 것이다.

#### 4.3.1 캐릭터 & 언어 정책

- **Luna**
  - 정체성: 우주에서 온 아이 (주인공과 비슷한 나이대의 **살아있는 생명체**)
  - 언어: **영어 only**
  - 역할:
    - 주요 학습 타겟 언어 노출 (모델 입력 기준 `speaker_type = 'ai'`, `language = 'en'`)
    - 짧고 명료한 문장으로 질문·모델 제시
    - 과도한 메타 설명은 피하고, Popo가 이미 한국어로 설명한 내용을 반복 번역하지 않음
    - **친구 같은 친밀감** 형성 — 로봇이 아닌 살아있는 존재로서 아이와 정서적 유대감 형성

- **Popo**
  - 정체성: 정부에서 파견된 **비밀 요원**. 친절하고 아이를 사랑하는 마음의 소유자
  - 언어: **한국어 + 영어 모두 가능**
  - 역할:
    - **훌륭한 코치** — 안전장치 및 정서적 공감
    - 과제 설명, 규칙 안내, 감정 공감 등은 주로 **한국어**
    - 아이가 말한 영어/한국어를 받아서 **부드러운 리폼(reformulation)** 제공
    - 필요 시 한 단어 수준의 영어 모델링 (예: "cat, dog, rabbit" 리스트 제시)
    - 아이를 **"캑틴"**이라고 부르며, 주인공으로서의 자부심을 불어넣음

- **언어 정책 요약**
  - 아이의 **이해와 안정감**이 최우선일 때 → Popo의 한국어 비중 증가
  - **표현 연습**이 핵심인 턴 → Luna의 영어 발화 후, Popo가 짧게 보조

#### 4.3.2 턴테이킹 & 안전 장치

- **Pass 규칙**  (pending)
  - 매 세션 R0에서 “말하기 싫으면 ‘패스(pass)’라고 말해도 된다”는 규칙을 명시
  - 음성 인식 결과에 “패스 / pass”가 감지되면:
    - 해당 TaskAttempt는 `not_applicable`로 종료
    - Orchestrator는 즉시 다음 Activity 또는 관계 블록(R1/R2)로 이동

- **침묵 처리**
  - 일정 시간(예: 7~10초) 무응답 시:
    1. Popo가 한국어로 재질문 또는 선택지 축소 제안
    2. 그래도 응답이 없으면, 해당 질문은 `skipped` 처리 후 다음 단계 진행
  - 이는 `SessionActivity.status` 및 `TaskAttempt.evaluated_correctness = not_applicable`로 기록

- **관계 블록 호출 규칙**
  - R0~R4는 **주차/세션에 상관없이 재사용 가능한 공통 모듈**로 구현
  - Orchestrator는 다음 타이밍에 필수 호출:
    - 세션 시작: R0(안전) → R2(클럽 인사) → R3(기분 체크)
    - 세션 중간: 아이의 피로도가 높거나 실패가 연속될 때 R1 또는 R2 삽입
    - 세션 종료: R4(마무리 & 다음 예고)
  - 각 블록은 템플릿 ID로 관리되며, 실제 발화는 LLM 프롬프트에 “캐릭터 톤 가이드 + 상황 요약”과 함께 전달

#### 4.3.3 Utterance 필드와의 매핑 규칙

에이전트 발화는 온톨로지 `Utterance` 스키마와 다음과 같이 매핑된다.

- `speaker_type`
  - Luna, Popo 모두 `speaker_type = 'ai'`
  - 아동 발화는 `speaker_type = 'child'`
- `utterance_role`
  - Luna:
    - 질문/모델 제시: `prompt`
    - 강화 피드백(“Great job!”, “Nice try!”): `feedback`
    - 연결 멘트: `filler`
  - Popo:
    - 과제 설명/규칙 안내: `instruction`
    - 정서적 공감/칭찬: `feedback`
    - 관계 블록(R0~R4) 수행: `filler` 또는 `instruction` (상황에 따라)
- `expected_child_response_type`
  - yes_no, wh_answer, choice_selection, repetition, narrative, opinion 등
  - Curriculum 엔진에서 TaskAttempt 템플릿 기준으로 결정하고, Orchestrator가 LLM 프롬프트에 포함
- `skill_ids`
  - 한 턴에 **2개 이하**의 Skill만 태깅하도록 설계 (예: `vocabulary`, `pronunciation`)
  - 복잡한 메타 학습 목표는 세션 다수 턴에 걸쳐 분산

#### 4.3.4 Prompting 가이드 (엔지니어용 요약)

LLM 호출 시 Orchestrator는 아래 정보를 묶어서 전달한다.

- 아동 컨텍스트 요약
  - 나이, 이름(또는 가명), 선호 주제 일부
  - 최근 N세션의 핵심 히스토리(예: “동물 주제를 좋아함”, “숫자 말하기는 아직 힘들어함”)
- 현재 Curriculum 컨텍스트
  - Week / Session / Task ID (예: `W1_S2_T3_food`)
  - 목표 Skill 및 난이도
- 에이전트 역할 지정
  - 현재 발화 주체: Luna 또는 Popo
  - 사용 언어: `en` 또는 `ko` (Popo는 혼합 가능하나, 한 문장 내 언어 전환은 최소화)
  - 허용 길이: 예를 들어 Luna는 **1~2문장**, Popo는 상황에 따라 1~3문장
- 안전 규칙
  - 패스 키워드(`pass`, `패스`) 존중
  - 아이에게 부담을 줄 수 있는 **평가적 언어**(“틀렸어”, “그건 잘못이야”)는 사용 금지
  - 대신 “좋은 시도였어”, “이렇게도 말할 수 있어” 식의 리폼 중심 피드백 사용

위 규칙을 통해,  
**온톨로지(데이터 구조) – 커리큘럼(교육 설계) – 에이전트 행동(LLM 프롬프트)**가 하나의 폐루프를 이루도록 한다.


## 5. 비기능 요구사항

### 5.1 성능 / 지연 시간 목표

- STT + LLM + TTS 왕복:  
  - 1 턴당 **TTFA (Time To First Audio) 2.0초 이내** 목표 (Streaming 적용 시)
  - 전체 응답 완료는 문장 길이에 따라 5초 허용
- 동시 세션:
  - MVP: 동시 50 세션까지 안정 동작
- 스토리지:
  - audio_retention_level에 따라:
    - `full` 세션은 S3에 3년 보관
    - `partial`은 대표 세션만(정책에 맞게 선정)
    - `none`은 오디오 저장 안함

### 5.2 보안 / 개인정보

- PII(부모 이메일, 전화번호, 아이 이름)는 암호화/마스킹 처리된 채로 로그에 남기지 않는다.  
- raw_audio_path는 **원격 스토리지 private bucket**에 저장,  
  접근은 백엔드 사인드 URL 통해서만 가능.  
- 데이터 거버넌스 원칙은 온톨로지 문서의 data governance 섹션과 서비스 이용약관/개인정보 처리방침을 기준으로 상세화한다.

### 5.3 비용 추정 (Unit Economics 신호)

| 항목 | 예상 비용/세션 | 비고 |
|------|---------------|------|
| STT (Whisper API) | $0.006/분 × 5분 = **$0.03** | 평균 세션 5분 가정 |
| LLM (GPT-4o-mini) | $0.01 × 15턴 = **$0.15** | 세션당 15턴 평균 |
| TTS (OpenAI TTS) | $0.015/1K chars × 2K = **$0.03** | AI 발화 2000자 가정 |
| **총합** | **~$0.21/세션** | 마진 확보 위해 구독료 설계 필요 |

> 💡 월 30세션 기준 = $6.30/user. 구독료 $9.99~$14.99 권장 (마진 30~50%).

### 5.4 UI/UX & 디자인 가이드라인

#### 5.4.1 Kids UI (Learner View)
- **Safety Touch Targets**: 4~7세 아동의 소근육 발달을 고려하여 모든 인터랙션 버튼은 **최소 60x60pt** 이상으로 설계한다.
- **Calm Tech Aesthetics**: 과도한 자극(번쩍거림, 빠른 화면 전환)을 지양하고, 부드러운 호흡(Breathing) 애니메이션과 파스텔/중채도 컬러를 사용한다.
- **Icon/Avatar-First**: 텍스트 읽기가 서툰 아동을 위해 메뉴와 피드백은 직관적인 아이콘과 아바타 표정으로 전달한다.

#### 5.4.2 Parent UI (Dashboard)
- **Glanceability (10-Second Rule)**: 리포트와 대시보드는 부모가 퇴근 후 **10초 안에** 핵심 변화(성장/기분)를 파악할 수 있도록 카드(Card) UI 중심으로 구성한다.
- **Dark Mode**: 취침 전 아이 곁에서 앱을 확인하는 상황을 고려하여 **완벽한 다크 모드**를 지원한다.

---

## 6. 기술 스택 & 코드 구조 제안

### 6.1 백엔드

- Python 3.11 (pyenv + uv)
- FastAPI
- SQLModel 또는 SQLAlchemy + Alembic
- Pydantic (DTO / 스키마)
- Postgres (RDS or Managed)
- Redis (선택: 세션 state cache 및 rate limiting)

**폴더 구조 예시**

```bash
app/
  main.py
  api/
    v1/
      sessions.py
      reports.py
      children.py
  core/
    config.py
    security.py
  models/
    child.py
    family.py
    subscription.py
    session.py
    utterance.py
    task.py
    skill.py
    report.py
    event.py
  services/
    stt_service.py
    tts_service.py
    llm_service.py
    curriculum_engine.py
    evaluation_service.py
    report_service.py
  repositories/
    session_repo.py
    utterance_repo.py
    report_repo.py
  schemas/
    session_schemas.py
    report_schemas.py
```

### 6.2 인프라

- 초기: Docker + 단일 서버(or Heroku/Render/GCP Cloud Run)  
- 로깅: 구조화 로그(JSON) + APM (Sentry 등)  
- 모니터링: 세션 수, STT/LLM/TTS 오류율, 평균 응답 시간  

### 6.3 커리큘럼/스킬 데이터 플로우 (W1~W4 반영)

#### 6.3.1 정적 스펙 계층 (Git → DB Seed)

- 소스:
  - `W1_Week1_Spec_v0.1.md`
  - `W2_Week2_Spec_v0.1.md`
  - `W3_Week3_Spec_v0.1.md`
  - `W4_Week4_Spec_v0.1.md`
  - `W1/2/3/4_Task_Activity_Skill_Mapping_v0.1.md`
  - `Skill_Dictionary_v0.1.md`
- 위 문서는 Git 리포지토리에서 관리하며, 아래 테이블의 **seed 데이터**로 사용한다.
  - `curriculum_unit` (Week, Session 메타)
  - `activity` (각 세션 내 Activity 정의)
  - `activity_skill_map` (Activity → Skill N:M 매핑)
  - (옵션) `task_skill_map` (Task 템플릿 → Skill 매핑)
  - `skill` / `skill_level_schema` (스킬 메타데이터 및 레벨링 정의)
- 원칙:
  - 문서 상의 ID(`W1_S1_intro`, `A_W1_S1_01` 등)는 DB 코드와 **1:1**로 매핑한다.
  - 커리큘럼 수정은 항상 Git 문서(PR) → Seed 스크립트 → DB 반영의 순서로 진행한다.

#### 6.3.2 런타임 세션 로깅 계층

- 런타임에서 사용하는 핵심 ID:
  - `curriculum_unit_id` (세션 템플릿)
  - `activity_id` (세션 내 현재 Activity)
  - `task_attempt_template_id` (필요 시, Task 템플릿 ID)
  - `session_id`, `session_activity_id`, `utterance_id`
- 서버가 관리하는 주요 엔티티:
  - `Session`
  - `SessionActivity`
  - `Utterance`
  - `TaskAttempt`
- 구현 원칙:
  - 프론트/Orchestrator는 **현재 Activity/TaskAttempt 템플릿 ID**만 서버에 전달하고,
  - 서버는 모든 이벤트를 타임스탬프와 함께 위 엔티티에 기록한다.
  - `TaskAttempt`에는
    - `evaluated_correctness`
    - `instruction_understood`
    - `related_utterance_ids`
    가 저장되며, 교육 효과 분석의 기본 단위가 된다.

#### 6.3.3 Daily Aggregation (일 단위 집계 테이블)

- 매일 1회 배치 잡으로 아래 집계 테이블을 생성/업데이트한다.
  - `agg_child_session_daily`
    - child_id, date, session_count, total_duration, avg_engagement_score, …
  - `agg_child_skill_daily`
    - child_id, date, skill_id, attempts, correct_attempts, accuracy, …
    - 계산식 예: `accuracy = correct_attempts / attempts`
  - `agg_child_error_daily`
    - child_id, date, error_category_id, count, …
- 집계 로직 개요:
  - `TaskAttempt` × `activity_skill_map` 조인 → child × skill × date 단위의 시도/정답 수 계산
  - `Utterance.skill_ids`, `Utterance.error_categories`를 이용해 발화량/에러 패턴 보정값 추가

#### 6.3.4 SkillLevel & 월간 Report 생성 플로우

1. `agg_child_skill_daily`를 기준으로 월 단위 롤업
   - skill별 raw_score, accuracy, 시도 횟수, 최근 3개월 트렌드 계산
2. 위 값을 이용해 `SkillLevel` 업데이트
   - `raw_score`, `level`, `percentile_by_age`, `trend_direction` 산출
3. `SkillLevel` + `agg_child_session_daily` + 대표 Utterance/TaskAttempt 샘플을 묶어
   - LLM 프롬프트에 투입 → `Report.summary_text`, `strengths_summary`, `areas_to_improve`, `recommendations_next_month` 생성
4. `ReportSkillSummary`에는
   - 부모가 바로 행동으로 옮길 수 있는 집 활동 가이드를 2~3개 저장
   - 예: “그림 그리기 놀이를 할 때, 영어 색깔 단어 2개만 함께 말해보기”

#### 6.3.5 분석/실험 확장 포인트

- 실험/AB 테스트를 위해 `Session` 및 `Event`에 아래 필드를 둔다.
  - `Session.experiment_arm` (예: `w1_prompt_style_a`, `w2_feedback_dense`)
  - `Event.metadata` 내에 실험 태그 포함 가능
- 이를 통해 다음과 같은 분석이 가능하다.
  - 피드백 밀도가 다른 두 그룹 간 스킬 향상 속도 비교
  - 캐릭터 설정/세계관(예: Popo 코치 톤) 변주에 따른 참여도/발화량 차이 분석
- 모든 실험은 `agg_*` 집계 테이블과 결합 가능하도록
  - child_id, session_id, curriculum_unit_id, activity_id를 공통 키로 유지한다.

---

## 7. 개발 단계 (마일스톤)

**M1. 도메인 스키마 & 기본 API**

- Postgres 스키마 생성 (온톨로지 v0.1.1 기준, 일부 테이블은 컬럼 subset)
- Child / Family / Subscription / Session 기본 CRUD API

**M2. 세션 + 음성 파이프라인**

- STT + LLM + TTS 통합
- Utterance 저장 + SessionActivity 최소 흐름 구현

**M3. TaskAttempt / SkillLevel 기초 평가**

- TaskDefinition seed  
- TaskAttempt 생성 로직  
- Rule 기반 SkillLevel 계산 배치  

**M4. 월간 리포트 MVP**

- Report / ReportSkillSummary 테이블 및 API  
- LLM 기반 리포트 텍스트 생성  
- 부모용 웹/앱 화면  

**M5. Observability & 품질**

- 주요 메트릭 및 이벤트 로깅 정리  
- error_category 샘플 집계 대시보드  

---

## 8. FDD와 온톨로지/스킬 사전의 관계 선언

> 본 FDD에 명시되지 않은 엔티티/필드/관계에 대한 정의,  
> enum 값, 데이터 거버넌스 원칙은  
> **온톨로지 정의서 v0.1.1**를 단일 소스로 참조한다.  
> 스킬 체계(카테고리, 모드, 레벨 서술, can-do 예시 등)에 대한 상세 정의는  
> **`Skill_Dictionary_v0.1.md`를 표준 참조 문서로 사용한다.  
> 만약 본 FDD와 온톨로지 정의서/스킬 사전 간에 불일치가 발생할 경우,  
> 온톨로지 정의서 및 스킬 사전의 최신 버전을 우선한다.**

---

## 9. 문서 변경 이력 (Change Log)

| 버전 | 날짜 | 작성자/수정자 | 내용 |
|:---:|:---:|:---:|---|
| v1.0 | 2026.01.10 | 정유일 | 최초 작성 (Architecture, Domain Model, MVP Scope 정의) |
| v1.1 | 2026.01.15 | 정유일 | 온톨로지 v0.1.1 스키마 반영, Session State Machine 구체화 |
| v1.2 | 2026.01.20 | 정유일 | 7세 여아 페르소나 적용, Triad Model 상세화, Phase 1 커리큘럼 추가 |
| v1.3 | 2026.01.21 | 정유일 | Agent Behavior 명세, Report 생성 로직 강화, Reference 문서 링크 |
| **v1.4** | **2026.01.21** | **정유일** | **UX/UI 가이드라인 추가, On-device VAD/Visual Feedback 명시, Admin 스코프 조정, Onboarding UX 개선** |

