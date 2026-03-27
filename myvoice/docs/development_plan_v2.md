# MyVoice (밤토리) — 개발 계획서 v2.1

> **작성일**: 2026-02-15 | **최종 업데이트**: 2026-03-06
> **기준**: 코드 리뷰 결과 + SPEC.md v1.0
> **현재 상태**: M1 완료, 프론트엔드 Phase 1~3 완료, Phase 4A(Voice AI) 프롬프트 완료, Parent View 와이어프레임 4개 완성, Auth 전면 개편 플랜 승인 대기

---

## 목차

1. [현황 진단 요약](#1-현황-진단-요약)
2. [개발 원칙](#2-개발-원칙)
3. [Phase 0: 안정화 & 보안 패치](#3-phase-0-안정화--보안-패치-즉시)
4. [Phase 1: 음성 AI 파이프라인 (M2)](#4-phase-1-음성-ai-파이프라인-m2)
5. [Phase 2: 프론트엔드 핵심 완성](#5-phase-2-프론트엔드-핵심-완성)
6. [Phase 3: 평가 & 커리큘럼 엔진 (M3)](#6-phase-3-평가--커리큘럼-엔진-m3)
7. [Phase 4: 월간 리포트 & Parent View (M4)](#7-phase-4-월간-리포트--parent-view-m4)
8. [Phase 5: 품질 & Observability (M5)](#8-phase-5-품질--observability-m5)
9. [작업 분배 (역할별)](#9-작업-분배-역할별)
10. [리스크 & 대응 전략](#10-리스크--대응-전략)
11. [체크리스트](#11-최종-체크리스트)

---

## 1. 현황 진단 요약

### 1.1 코드 리뷰 결과 (2026-02-15)

| 영역 | 분석 파일 수 | 점수 | 핵심 문제 |
|------|------------|------|----------|
| 백엔드 코드 품질 | 55개 | ⭐⭐⭐ | 서비스 계층 대부분 stub, 에러 핸들링 부족 |
| 프론트엔드 코드 품질 | 56개 | ⭐⭐⭐⭐ | Kids View 11개 페이지 완성, Parent View 3개 페이지 완성 |
| 보안 | — | ⭐⭐ | CORS 전체 허용, JWT 시크릿 하드코딩, Rate limiting 없음 |
| 테스트 | — | ⭐ | 커버리지 ~5%, pytest 설정만 존재 |
| SPEC 준수 | — | ~50% | M1 완료, 프론트엔드 Phase 1~3 완료, M2~M5 미착수 |

### 1.2 발견된 이슈 총계 (2026-02-15 기준, 일부 해결됨)

- **보안 취약점**: 10건 (HIGH 5건, MEDIUM 5건) — Auth 전면 개편 플랜으로 대응 예정
- **버그**: 14건 (CRITICAL 3건, HIGH 4건, MEDIUM 7건)
- **SPEC 미준수**: 10개 영역
- **프론트엔드 미완성**: ~~핵심 페이지 3개~~ → Kids View 완성, Parent View 기본 완성

### 1.3 2026-03-06 기준 진행 현황

**완료된 작업:**
- Kids View 전체 11개 페이지 (KidHome, Adventures, AdventureDetail/Play/Result, Vocabulary/Learning/Result, KidProfile, KidSkills, KidShop)
- Parent View 3개 페이지 (Dashboard, ReportDetail, EditChild)
- 백엔드 라우터 17개, 서비스 13개, 모델 12개 구현
- API 훅 10개 (React Query 기반)
- 와이어프레임 4개 완성 (01-parent-dashboard, 02-report-detail, 03-edit-child, 04-skill-deep-report)
- 시드 데이터 스크립트 (app/seed.py)
- 오디오 녹음 유틸리티 (audioRecorder.ts)

**승인 대기:**
- Auth 전면 개편 플랜 (보안 강화 + OAuth 도입)

**미착수 (SPEC M2~M5):**
- 음성 AI 파이프라인 실제 구현 (STT → LLM → TTS)
- 세션 상태 머신 (Redis 기반)
- 평가 & 커리큘럼 엔진
- 월간 리포트 생성
- 테스트 커버리지 향상

---

## 2. 개발 원칙

### 2.1 Phase 진행 규칙

1. **각 Phase는 이전 Phase 완료 후 시작** — 단, Phase 0은 즉시 시작
2. **Phase 완료 기준**: 해당 Phase의 모든 Acceptance Criteria 통과 + 기존 테스트 깨지지 않음
3. **핫픽스**: 보안 이슈(S1~S5)는 Phase와 무관하게 즉시 수정

### 2.2 코드 컨벤션 (SPEC 1.4 준수)

- Python: PEP 8, type hints 필수
- API: RESTful, `/v1/` prefix, snake_case
- DB: Alembic migration 필수, raw SQL 금지
- Frontend: TypeScript strict mode, ESLint 준수
- 커밋: Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`)

### 2.3 역할

| 역할 | 담당 | 책임 |
|------|------|------|
| Senior Architect | Claude (Opus) | 기획 리뷰, 코드 리뷰, 아키텍처 결정 |
| Developer | Gemini | 실제 코딩, 테스트 작성, 구현 보고 |
| Product Owner | 정유일 | 최종 의사결정, 우선순위 조정 |

---

## 3. Phase 0: 안정화 & 보안 패치 (즉시)

> **목표**: 현재 코드베이스의 보안 취약점과 크리티컬 버그를 해결하여 안전한 개발 기반 확보
> **예상 소요**: 2~3일

### 3.1 보안 긴급 패치

#### P0-T1: CORS 환경별 분리
- **파일**: `app/main.py`
- **작업**: `allow_origins=["*"]` → 환경 변수 기반 화이트리스트
- **구현**:
  ```python
  # config.py에 추가
  cors_origins: list[str] = ["http://localhost:5173"]  # .env에서 오버라이드

  # main.py에서 사용
  app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, ...)
  ```
- **Acceptance**: `APP_ENV=production`일 때 `*` 불가, 명시적 도메인만 허용

#### P0-T2: JWT 시크릿 키 검증
- **파일**: `app/config.py`
- **작업**: 기본값 사용 시 경고, production 환경에서는 시작 차단
- **구현**:
  ```python
  @model_validator(mode='after')
  def validate_secrets(self):
      if self.app_env == "production" and "change" in self.jwt_secret_key:
          raise ValueError("JWT_SECRET_KEY must be changed in production")
      return self
  ```
- **Acceptance**: 프로덕션 환경에서 기본 시크릿 사용 시 앱 시작 실패

#### P0-T3: Mock 로그인 엔드포인트 제거
- **파일**: `app/routers/auth.py`
- **작업**: `/auth/login/mock` 엔드포인트를 `APP_ENV=development`에서만 등록
- **Acceptance**: production 빌드에서 mock 엔드포인트 접근 불가

#### P0-T4: 디버그 로그 제거
- **파일**: `app/routers/kid_adventures.py` 외 다수
- **작업**: `print("DEBUG: ...")` 및 설정값 출력 코드 전부 삭제
- **Acceptance**: `grep -r "print(" app/routers/` 결과 없음

#### P0-T5: Rate Limiting 기초 구현
- **파일**: `app/main.py`, 새로 `app/core/rate_limit.py`
- **작업**: 로그인/회원가입 엔드포인트에 IP 기반 rate limit 적용
- **구현**: `slowapi` 또는 Redis 기반 간단한 미들웨어
- **Acceptance**: 동일 IP에서 1분 내 10회 이상 로그인 시도 시 429 응답

---

### 3.2 크리티컬 버그 수정

#### P0-T6: Utterance 트랜잭션 관리
- **파일**: `app/routers/kid_sessions.py`
- **작업**:
  - STT → LLM → TTS 파이프라인을 단일 트랜잭션으로 래핑
  - 실패 시 부분 데이터 롤백
  - X-Idempotency-Key 헤더를 실제로 체크하여 중복 방지
- **Acceptance**: TTS 실패 시 Utterance(ai) 레코드가 DB에 남지 않음

#### P0-T7: 인증 실패 메시지 통일
- **파일**: `app/routers/auth_child.py`
- **작업**: "Child not found"와 "Invalid PIN" 에러를 동일 메시지로 통일
- **구현**: `raise HTTPException(status_code=401, detail="Authentication failed")`
- **Acceptance**: 잘못된 child_id와 잘못된 PIN이 동일한 응답 반환

#### P0-T8: 세션 상태 기본값 수정
- **파일**: `app/models/session.py`
- **작업**: `SessionActivity.status` 기본값을 `"pending"` → `"idle"`로 변경
- **Migration**: Alembic migration 생성 (기존 데이터 업데이트 포함)
- **Acceptance**: 새 세션 생성 시 status가 "idle"

#### P0-T9: N+1 쿼리 수정
- **파일**: `app/models/family.py`
- **작업**: `Child.sessions` relationship의 `lazy="selectin"` → `lazy="select"`
- **Acceptance**: Child 조회 시 Session 테이블 쿼리 미발생 (명시적 join 시에만 로드)

---

### 3.3 코드 정리

#### P0-T10: 에러 핸들링 기반 구축
- **파일**: `app/core/exceptions.py`, `app/main.py`
- **작업**:
  - Custom exception 클래스 확장: `NotFoundError`, `AuthError`, `ValidationError`, `ExternalServiceError`
  - `main.py`에 글로벌 exception handler 등록
  - 표준 에러 응답 포맷: `{"error": {"code": "...", "message": "...", "detail": ...}}`
- **Acceptance**: 모든 4xx/5xx 응답이 동일 포맷

#### P0-T11: 스크립트 → Alembic 마이그레이션 전환
- **파일**: `scripts/add_image_path_column.py`, `scripts/add_story_columns.py`
- **작업**: raw SQL 스크립트를 Alembic migration으로 변환
- **Acceptance**: `alembic upgrade head`만으로 전체 스키마 생성 가능

---

### Phase 0 완료 기준

> **상태**: Auth 전면 개편 플랜에 통합 예정 (승인 대기 중)

- [ ] 보안 패치 5건 (P0-T1 ~ T5) 모두 적용 → **Auth 개편 플랜에 포함**
- [ ] 크리티컬 버그 4건 (P0-T6 ~ T9) 모두 수정
- [ ] 코드 정리 2건 (P0-T10 ~ T11) 완료
- [x] `uvicorn app.main:app --reload` 정상 시작
- [x] 기존 API 동작 확인 (signup, login, select-child, create-child)

---

## 4. Phase 1: 음성 AI 파이프라인 (M2)

> **목표**: 아이가 실제로 말하면 AI가 대화로 응답하는 end-to-end 루프 완성
> **예상 소요**: 7~10일
> **선행 조건**: Phase 0 완료

### 4.1 Speech Pipeline 구현

#### P1-T1: STT 연결 (Whisper)
- **파일**: `app/services/speech_pipeline.py`
- **작업**:
  - `speech_to_text(audio_bytes, language="auto") -> SttResult` 구현
  - OpenAI Whisper API 호출 (16kHz mono 입력)
  - 언어 자동 감지 (영어/한국어 혼용 대응) — **P0에서 하드코딩 이슈 해결**
  - 빈 결과 / 소음 판별 로직 (`stt_confidence < 0.3` → 소음 처리)
  - Retry 로직: 429(Rate Limit) → 최대 3회 재시도 (exponential backoff)
- **반환 타입**:
  ```python
  @dataclass
  class SttResult:
      text: str
      language: str          # "en" | "ko"
      confidence: float      # 0.0 ~ 1.0
      is_empty: bool         # 소음/무발화 판별
      duration_ms: int       # 오디오 길이
  ```
- **Acceptance**: 오디오 파일 → 텍스트 변환 성공, 5초 이내 응답

#### P1-T2: LLM 대화 생성 (GPT-4o-mini)
- **파일**: `app/services/speech_pipeline.py`
- **작업**:
  - `generate_dialogue(context: ConversationContext) -> DialogueResult` 구현
  - 프롬프트 조립: 캐릭터 역할 + Activity 지시문 + 대화 맥락 + 스킬 레벨
  - Luna(영어 only) / Popo(한/영) 캐릭터별 언어 정책 적용
  - 안전 필터링: 입력/출력 양방향 (욕설, 위험 표현, 개인정보)
  - 응답 길이 제한: 1~2문장, max_tokens=150
- **프롬프트 구조**:
  ```
  [System] 캐릭터 역할 + 언어 정책 + 행동 규칙
  [Context] Activity 지시문 + 현재 Phase + 목표 스킬
  [History] 직전 N턴 대화 (최대 10턴)
  [User] 아이 발화 텍스트
  ```
- **Acceptance**: 맥락 기반 자연스러운 응답, 2초 이내

#### P1-T3: TTS 연결 (OpenAI TTS)
- **파일**: `app/services/speech_pipeline.py`
- **작업**:
  - `text_to_speech(text, character) -> bytes` 구현
  - 캐릭터별 보이스 매핑: Luna=`nova`, Popo=`shimmer`, Narrator=`onyx`
  - 오디오 포맷: MP3 (클라이언트 호환성)
  - 캐시: 동일 텍스트+캐릭터 조합은 Redis 캐시 (TTL 1시간)
- **Acceptance**: 텍스트 → 오디오 bytes 변환 성공, 1.5초 이내

#### P1-T4: 안전 필터링 서비스
- **파일**: 새로 `app/services/safety_filter.py`
- **작업**:
  - `filter_input(text) -> SafetyResult`: 아이 발화 필터링
  - `filter_output(text) -> SafetyResult`: AI 응답 필터링
  - 규칙 기반 1차 필터 (금지어 리스트) + LLM 2차 필터 (맥락 판단)
  - 위험 감지 시 안전한 대체 응답 제공
- **Acceptance**: 욕설/위험 표현 입력 시 필터링, 안전한 fallback 응답

---

### 4.2 세션 상태 머신

#### P1-T5: Redis 기반 상태 머신 구현
- **파일**: `app/services/session_orchestrator.py`
- **작업**:
  - Redis key: `session:{id}:state` (JSON)
  - 상태 전이: `IDLE → ACTIVE → PAUSED → ENDED`
  - 전이 규칙 강제: 잘못된 전이 시 `InvalidStateTransition` 예외
  - TTL: 세션 키 2시간 후 자동 만료
  ```python
  VALID_TRANSITIONS = {
      "idle": ["active"],
      "active": ["paused", "ended"],
      "paused": ["active", "ended"],
  }
  ```
- **Acceptance**: 상태 전이 정상 동작, Redis에 상태 저장, 잘못된 전이 시 에러

#### P1-T6: 3-Phase Flow 구현
- **파일**: `app/services/session_orchestrator.py`
- **작업**:
  - Phase 1 (NARRATOR_INTRO): Narrator TTS 자동 생성 → 클라이언트에 전송
  - Phase 2 (TRANSITION): Popo 안내 → 트리거 단어 대기 ("Go!", "시작" 등)
  - Phase 3 (INTERACTIVE): 양방향 대화 루프 (STT → LLM → TTS)
  - Phase 전환 이벤트를 Redis에 기록
- **Acceptance**: 세션 시작 → Narrator 오디오 → 전환 → 대화 루프 정상 동작

#### P1-T7: Utterance 라우터 리팩터링
- **파일**: `app/routers/kid_sessions.py`
- **작업**:
  - Audio 수신 → STT → Safety Filter → LLM → Safety Filter → TTS → Response
  - Utterance(child) + Utterance(ai) DB 저장
  - 현재 Phase에 따라 처리 분기:
    - Phase 1~2: 트리거 단어 감지만 수행
    - Phase 3: 전체 대화 파이프라인
  - 멱등성 보장 (Idempotency-Key 헤더 활용)
- **Acceptance**: `curl`로 오디오 전송 → AI 음성 응답 수신

#### P1-T8: Silence/Timeout 처리
- **파일**: `app/services/session_orchestrator.py`
- **작업**:
  - 연속 15초 무발화 → re-prompting (Popo: "괜찮아, 다시 한 번 해볼까?")
  - 연속 3회 timeout → 자동 일시정지 + Popo 안내
  - 클라이언트에 `re_prompt` 이벤트 반환
- **Acceptance**: timeout 이벤트 시 적절한 fallback 응답

---

### Phase 1 완료 기준

- [ ] STT/LLM/TTS 파이프라인 end-to-end 동작
- [ ] Redis 세션 상태 머신 동작
- [ ] 3-Phase Flow (Narrator → Transition → Interactive) 동작
- [ ] 안전 필터링 (입력/출력) 동작
- [ ] Silence/Timeout 처리 동작
- [ ] `scripts/verify_voice_flow.py` 통과
- [ ] 핵심 경로 pytest 3개 이상 작성

---

## 5. Phase 2: 프론트엔드 핵심 완성

> **목표**: Kids View 핵심 기능 완성 — 음성 대화 UI, 스킬 페이지, 접근성
> **예상 소요**: 7~10일
> **선행 조건**: Phase 1 완료 (음성 API 동작)
> **병렬 가능**: Phase 1과 UI 골격 작업은 병렬 진행 가능

### 5.1 AdventurePlay 핵심 완성

#### P2-T1: 음성 대화 루프 UI
- **파일**: `frontend/src/pages/kid/AdventurePlay.tsx`
- **작업**:
  - Phase 1 (Narrator): 전체화면 일러스트 + 나레이션 오디오 자동 재생
  - Phase 2 (Transition): Popo 캐릭터 + 트리거 안내 + 마이크 활성화
  - Phase 3 (Interactive): 대화 버블 UI + 마이크 녹음 + AI 오디오 재생
  - Activity 간 전환 (세션 내 여러 Activity 순차 진행)
  - 세션 종료 → 결과 화면 네비게이션
- **컴포넌트 분리**:
  ```
  AdventurePlay/
  ├── NarratorPhase.tsx      # Phase 1 - 나레이션 재생
  ├── TransitionPhase.tsx    # Phase 2 - 트리거 대기
  ├── InteractivePhase.tsx   # Phase 3 - 대화 루프
  ├── ConversationBubble.tsx # 채팅 버블 (child/ai)
  ├── MicButton.tsx          # 마이크 녹음 버튼 (60x60pt 이상)
  └── SessionTimer.tsx       # 세션 타이머
  ```
- **Acceptance**: 세션 시작 → 나레이션 → 트리거 → 대화 → 종료 전체 흐름 동작

#### P2-T2: 오디오 녹음 & 업로드
- **파일**: `frontend/src/lib/audioRecorder.ts`
- **작업**:
  - MediaRecorder API → WebM/OGG 녹음
  - 최대 녹음 시간: 30초 (자동 중단)
  - 최대 파일 크기: 5MB (초과 시 경고)
  - 녹음 → base64 → API 업로드 → 응답 오디오 재생
  - 에러 핸들링: 마이크 권한 거부, 녹음 실패
- **Acceptance**: 마이크 버튼 탭 → 녹음 → 업로드 → AI 응답 오디오 재생

#### P2-T3: KidSkills 페이지 완성
- **파일**: `frontend/src/pages/kid/KidSkills.tsx`
- **작업**:
  - 스킬별 레이더 차트 (Recharts)
  - 주간 목표 설정 모달
  - 스킬 카테고리 필터링 (Vocabulary, Pronunciation, Grammar, Fluency)
  - AI 추천 목표 연동 (`lib/goalRecommendation.ts` 활용)
- **Acceptance**: 스킬 차트 렌더링, 목표 설정/조회 동작

### 5.2 코드 품질 & 접근성

#### P2-T4: Error Boundary 적용
- **파일**: 새로 `frontend/src/components/ErrorBoundary.tsx`
- **작업**:
  - Kids View / Parent View 각각 Error Boundary 래핑
  - 아이 친화적 에러 UI (캐릭터 + "잠깐 쉬고 올게!" 메시지)
  - 에러 로깅 (추후 Sentry 연동 대비)
- **Acceptance**: 컴포넌트 크래시 시 앱 전체가 깨지지 않음

#### P2-T5: 접근성 (A11y) 개선
- **파일**: 전체 컴포넌트
- **작업**:
  - 모든 아이콘 버튼에 `aria-label` 추가
  - BottomNav, MissionCard 등 키보드 네비게이션 지원 (`tabindex`, `onKeyDown`)
  - 포커스 인디케이터 스타일 추가
  - 뮤테이션 로딩 상태 (구매, 제출 등 중복 클릭 방지)
  - 색상 대비 WCAG AA 준수 확인
- **Acceptance**: Lighthouse Accessibility 점수 80+ 달성

#### P2-T6: snake_case → camelCase 변환 레이어
- **파일**: `frontend/src/api/client.ts`
- **작업**:
  - API 응답 자동 변환 유틸리티: `snakeToCamel(obj)`
  - API 요청 자동 변환: `camelToSnake(obj)`
  - `apiRequest()` 내부에서 자동 적용
- **Acceptance**: 프론트엔드 코드에서 camelCase만 사용, API 통신은 snake_case

#### P2-T7: Code Splitting & 성능 최적화
- **파일**: `frontend/src/App.tsx`
- **작업**:
  - `React.lazy()` + `Suspense`로 라우트별 코드 스플리팅
  - Kids View / Parent View / Auth를 별도 chunk로 분리
  - 스켈레톤 로딩 UI (현재 "Loading..." 텍스트 대체)
- **Acceptance**: 초기 로드 번들 사이즈 30% 감소

#### P2-T8: console.log 정리 & 환경별 로깅
- **파일**: 프론트엔드 전체
- **작업**:
  - 모든 `console.log` / `console.error` 제거 또는 조건부 처리
  - `import.meta.env.DEV` 조건으로 개발 환경에서만 로깅
- **Acceptance**: production 빌드에서 console 출력 없음

---

### Phase 2 완료 기준

> **상태**: 프론트엔드 핵심 완성 (Phase 2 프롬프트 기반 구현 완료)

- [x] ~~AdventurePlay 전체 흐름~~ → mock 기반 UI 완성 (실제 Voice AI는 Phase 4A에서)
- [x] 오디오 녹음 유틸리티 구현 (audioRecorder.ts)
- [x] KidSkills 페이지 렌더링 및 목표 설정 동작
- [ ] Error Boundary 동작 확인
- [ ] Lighthouse Accessibility 80+
- [x] `npm run build` 에러 없음
- [ ] production 빌드에서 console 출력 없음

---

## 6. Phase 3: 평가 & 커리큘럼 엔진 (M3)

> **목표**: 아이의 발화를 분석하여 스킬 수준을 자동 평가하고, 적응형 커리큘럼 제공
> **예상 소요**: 7~10일
> **선행 조건**: Phase 1 완료

### 6.1 커리큘럼 시스템

#### P3-T1: Curriculum Seed Data
- **파일**: `scripts/seed_curriculum.py`
- **작업**:
  - W1~W4 주차별 커리큘럼 데이터 삽입
  - CurriculumUnit → Activity → TaskDefinition 계층 구조
  - 각 Activity에 `instructions_for_ai` (LLM 프롬프트 조각) 포함
  - 멱등성 보장: 중복 실행 시 데이터 중복 없음
- **Acceptance**: seed 스크립트 실행 → DB에 4주치 커리큘럼 데이터 존재

#### P3-T2: Curriculum Engine 서비스
- **파일**: 새로 `app/services/curriculum_engine.py`
- **작업**:
  - `get_next_activity(child_id) -> Activity`: 아이의 진행 상태에 따라 다음 Activity 결정
  - 진행 규칙: 순차 진행 (W1→W2→...) + 반복 조건 (correctness < 70%)
  - Session 시작 시 SessionActivity 리스트 자동 생성
  - 아이의 스킬 레벨에 따라 난이도 조절
- **Acceptance**: 세션 시작 → 적절한 Activity 순서 배정

### 6.2 평가 시스템

#### P3-T3: Evaluation Engine 서비스
- **파일**: 새로 `app/services/evaluation_service.py`
- **작업**:
  - AI 질문 후 child 발화를 묶어 TaskAttempt 자동 생성
  - Rule-based 1차 평가:
    - `correctness`: 키워드 매칭 + 문법 체크
    - `instruction_understood`: 질문 의도 파악 여부
    - `pronunciation_score`: STT confidence 활용
  - LLM 2차 평가 (선택적): 자연스러움, 문맥 적절성
  - TaskAttempt.activity_id에 적절한 FK 추가 (Alembic migration)
- **Acceptance**: 발화 교환 후 TaskAttempt 생성, 평가 값 저장

#### P3-T4: SkillLevel 배치 계산
- **파일**: 새로 `app/services/skill_service.py`
- **작업**:
  - 수동 트리거 (dev) / 월 1회 자동 (prod) SkillLevel 스냅샷 생성
  - 스킬별 계산 규칙:
    - Vocabulary: unique_word_count + 정답률
    - Pronunciation: 평균 STT confidence
    - Grammar: 문법 오류 비율
    - Fluency: 평균 발화 길이 + 응답 시간
  - score → level 매핑: 0~40=L1(Beginner), 40~70=L2(Intermediate), 70~100=L3(Advanced)
- **Acceptance**: 트리거 실행 → SkillLevel 테이블에 스냅샷 생성

---

### Phase 3 완료 기준

- [ ] Curriculum seed 데이터 로드 성공
- [ ] 세션 시작 시 Activity 자동 배정
- [ ] TaskAttempt 자동 생성 및 평가
- [ ] SkillLevel 스냅샷 생성
- [ ] 관련 pytest 5개 이상

---

## 7. Phase 4: 월간 리포트 & Parent View (M4)

> **목표**: 부모가 아이의 학습 성과를 한눈에 확인할 수 있는 대시보드 완성
> **예상 소요**: 7~10일
> **선행 조건**: Phase 3 완료
>
> **2026-03-06 현황**:
> - 와이어프레임 4개 완성 (`wireframes/01~04`)
> - 프론트엔드 Parent View 3개 페이지 구현 완료 (Dashboard, ReportDetail, EditChild)
> - 백엔드 parent_dashboard.py, parent_children.py 라우터 존재
> - 백엔드 report_service.py, aggregation_service.py 서비스 존재 (stub 가능성 있음)

### 7.1 백엔드 — 리포트 생성

#### P4-T1: Report 생성 서비스
- **파일**: 새로 `app/services/report_service.py`
- **작업**:
  - Session/Utterance/SkillLevel 데이터 수집
  - LLM으로 리포트 요약 생성:
    - `summary_text`: 한 달간 성장 요약 (한국어, 3~5문장)
    - `strengths`: 강점 (리스트)
    - `areas_to_improve`: 개선점 (리스트)
  - Report + ReportSkillSummary 테이블에 저장
- **Acceptance**: 트리거 → Report 생성, summary/strengths/improvements 포함

#### P4-T2: Reports API 실제 구현
- **파일**: `app/routers/parent_reports.py`
- **작업**:
  - Stub → 실제 DB 조회로 전환
  - 자녀별 리포트 목록 (페이지네이션: offset + limit)
  - 리포트 상세 조회 (스킬별 상세 포함)
  - `period_start`, `period_end` 필터링
- **Acceptance**: 생성된 리포트를 API로 조회 가능

#### P4-T3: Daily Aggregation 배치
- **파일**: 새로 `app/services/aggregation_service.py`
- **작업**:
  - 일별 집계: 세션 수, 총 발화 수, 평균 참여 시간
  - 스킬별 일별 점수 추이
  - 스크립트 또는 Celery task로 실행
- **Acceptance**: 배치 실행 → 집계 데이터 생성

### 7.2 프론트엔드 — Parent Dashboard

#### P4-T4: Parent Dashboard 구현
- **파일**: `frontend/src/pages/parent/Dashboard.tsx`
- **작업**:
  - 자녀 선택 탭 (다자녀 지원)
  - 핵심 지표 카드: 이번 주 세션 수, 총 발화 수, 참여도 추이
  - 스킬 레이더 차트 (이전 월 대비 변화)
  - 최근 리포트 미리보기
  - 10초 규칙: 핵심 변화를 카드로 즉시 파악 가능
- **Acceptance**: 대시보드 렌더링, 자녀별 데이터 전환

#### P4-T5: Report 상세 페이지
- **파일**: 새로 `frontend/src/pages/parent/ReportDetail.tsx`
- **작업**:
  - 리포트 요약 카드 (strengths, improvements)
  - 스킬별 상세 차트 (Recharts)
  - 월별 비교 기능
- **Acceptance**: 리포트 목록 → 상세 → 스킬 차트 렌더링

#### P4-T6: 자녀 관리 페이지
- **파일**: 새로 `frontend/src/pages/parent/ChildManagement.tsx`
- **작업**:
  - 자녀 추가/수정/프로필 관리
  - PIN 설정/변경
  - 아바타 선택
- **Acceptance**: 자녀 CRUD 동작

---

### Phase 4 완료 기준

- [ ] 월간 리포트 자동 생성
- [x] Parent Dashboard 렌더링 (프론트엔드 구현 완료, 백엔드 연동 필요)
- [x] 리포트 상세 페이지 (프론트엔드 구현 완료 + 와이어프레임 02, 04)
- [x] 자녀 관리 페이지 (프론트엔드 EditChild 구현 완료 + 와이어프레임 03)
- [ ] 일별 집계 배치 동작
- [x] 스킬 심층 리포트 와이어프레임 완성 (04-skill-deep-report.html)

### Phase 4 와이어프레임 (완성)

| 파일 | 설명 | 상태 |
|------|------|------|
| `wireframes/01-parent-dashboard.html` | 학부모 대시보드 | ✅ 완성 |
| `wireframes/02-report-detail.html` | 리포트 상세 (6축 레이더, 또래비교, 11개 스킬) | ✅ 완성 |
| `wireframes/03-edit-child.html` | 아이 프로필 수정 | ✅ 완성 |
| `wireframes/04-skill-deep-report.html` | 스킬 심층 리포트 (온톨로지 학습맵, CAN-DO, 발화예시) | ✅ 완성 |

---

## 8. Phase 5: 품질 & Observability (M5)

> **목표**: 프로덕션 배포 준비 — 테스트, 모니터링, 성능 최적화
> **예상 소요**: 5~7일
> **선행 조건**: Phase 4 완료

### 8.1 테스트

#### P5-T1: 백엔드 단위/통합 테스트
- **작업**:
  - Auth 플로우 테스트 (signup → login → select-child)
  - Session 플로우 테스트 (start → utterance → end)
  - Speech Pipeline 테스트 (mock OpenAI)
  - Safety Filter 테스트
  - 목표: 핵심 비즈니스 로직 커버리지 70%+
- **도구**: pytest + pytest-asyncio + httpx (TestClient)

#### P5-T2: 프론트엔드 테스트
- **작업**:
  - 컴포넌트 단위 테스트 (Jest + React Testing Library)
  - 인증 플로우 테스트
  - AdventurePlay 상태 전이 테스트
  - 목표: 핵심 컴포넌트 커버리지 60%+

#### P5-T3: E2E 테스트
- **작업**:
  - Playwright 기반 주요 시나리오 테스트
  - 시나리오: 로그인 → 자녀 선택 → 세션 시작 → 대화 → 종료
  - CI에서 자동 실행 가능하도록 설정

### 8.2 Observability

#### P5-T4: 구조화 로깅
- **작업**:
  - JSON 포맷 로깅 (structlog 또는 python-json-logger)
  - 요청별 correlation_id 추가
  - 로그 레벨: ERROR → 즉시 알림, WARN → 일일 집계, INFO → 기록만
- **Acceptance**: 모든 로그가 JSON 포맷, 요청 추적 가능

#### P5-T5: 핵심 메트릭
- **작업**:
  - 세션당 평균 발화 수 (목표: ≥15회)
  - TTFA (Time To First Audio, 목표: ≤2초)
  - API 에러율 (목표: <1%)
  - 세션당 비용 (목표: ~$0.21)
  - 엔드포인트별 응답 시간 P50/P95/P99

#### P5-T6: 에러 핸들링 강화
- **작업**:
  - OpenAI API 장애 시 Fallback: 캐시된 응답 또는 오프라인 메시지
  - DB 연결 실패 시 graceful degradation
  - Health check에 DB/Redis 상태 포함

### 8.3 보안 강화 (프로덕션 대비)

#### P5-T7: 토큰 관리 강화
- **작업**:
  - httpOnly 쿠키로 토큰 저장 방식 전환 (XSS 방어)
  - Refresh token 도입 (access token 수명 단축: 24h → 1h)
  - 토큰 블랙리스트 (Redis 기반)
- **Acceptance**: 로그아웃 시 토큰 즉시 무효화

#### P5-T8: 이메일 인증 플로우
- **작업**:
  - 회원가입 시 인증 이메일 발송
  - 인증 완료 전 family_token 발급 불가
  - 인증 재발송 API
- **Acceptance**: 미인증 이메일로 로그인 시 "이메일 인증 필요" 응답

---

### Phase 5 완료 기준

- [ ] 백엔드 테스트 커버리지 70%+
- [ ] 프론트엔드 테스트 커버리지 60%+
- [ ] E2E 테스트 주요 시나리오 통과
- [ ] JSON 구조화 로깅 적용
- [ ] 핵심 메트릭 수집 동작
- [ ] httpOnly 쿠키 토큰 전환
- [ ] Health check (DB + Redis) 동작

---

## 9. 작업 분배 (역할별)

### Senior Architect (Claude) 담당

| Phase | 작업 |
|-------|------|
| 전 Phase | SPEC.md 업데이트, 코드 리뷰, 아키텍처 결정 |
| Phase 0 | 보안 패치 설계, 에러 핸들링 구조 설계 |
| Phase 1 | 프롬프트 설계 (캐릭터별), 안전 필터 규칙 정의 |
| Phase 3 | 평가 규칙 설계, 스킬 매핑 정의 |
| Phase 4 | 리포트 프롬프트 설계 |

### Developer (Gemini) 담당

| Phase | 작업 |
|-------|------|
| Phase 0 | P0-T1 ~ T11 구현 |
| Phase 1 | P1-T1 ~ T8 구현 |
| Phase 2 | P2-T1 ~ T8 구현 |
| Phase 3 | P3-T1 ~ T4 구현 |
| Phase 4 | P4-T1 ~ T6 구현 |
| Phase 5 | P5-T1 ~ T8 구현 |

### Product Owner (정유일) 담당

| Phase | 작업 |
|-------|------|
| Phase 0 | 우선순위 확정, 완료 검증 |
| Phase 1 | 음성 품질 검수, 캐릭터 어조 확인 |
| Phase 2 | UI/UX 검수 (Kids View) |
| Phase 4 | 리포트 내용 검수, Parent View UX 확인 |
| Phase 5 | 프로덕션 배포 승인 |

---

## 10. 리스크 & 대응 전략

| # | 리스크 | 영향도 | 발생 확률 | 대응 전략 |
|---|--------|-------|----------|----------|
| R1 | OpenAI API 응답 지연 (>3초) | HIGH | 중 | TTS 캐싱 + LLM 스트리밍 응답 도입 |
| R2 | OpenAI API 비용 초과 | HIGH | 중 | 세션당 턴 수 제한 (max 20), 일일 사용량 캡 |
| R3 | 아이 음성 인식 정확도 낮음 | HIGH | 높 | Confidence threshold 튜닝 + fallback 메시지 + re-prompt |
| R4 | 마이크 권한 거부 (모바일) | MEDIUM | 중 | 권한 요청 UX 개선 + 텍스트 입력 폴백 |
| R5 | Redis 장애 | MEDIUM | 낮 | DB 폴백 (세션 상태를 DB에도 동기) |
| R6 | 동시 접속자 급증 | MEDIUM | 낮 | Rate limiting + 큐 기반 처리 (Phase 5+) |

---

## 11. 최종 체크리스트

### MVP 출시 전 필수 (Phase 0~4 완료 후)

- [ ] CORS 화이트리스트 적용
- [ ] JWT 시크릿 프로덕션용 설정
- [ ] Rate limiting 동작
- [ ] 음성 대화 E2E 동작 (STT → LLM → TTS)
- [ ] 안전 필터링 동작
- [ ] 세션 상태 머신 동작
- [ ] Kids View 핵심 기능 동작 (홈, 모험, 어휘, 상점, 프로필)
- [ ] Parent Dashboard 기본 동작
- [ ] 월간 리포트 생성 및 조회
- [ ] 에러 시 사용자에게 적절한 메시지 표시

### 프로덕션 배포 전 권장 (Phase 5 완료 후)

- [ ] 테스트 커버리지: BE 70%+, FE 60%+
- [ ] JSON 구조화 로깅
- [ ] 핵심 메트릭 대시보드
- [ ] httpOnly 쿠키 토큰
- [ ] 이메일 인증
- [ ] E2E 테스트 CI 연동
- [ ] SSL/TLS (HTTPS) 적용
- [ ] 백업 & 복구 계획

---

> **문서 버전**: v2.1 | **작성일**: 2026-02-15 | **최종 업데이트**: 2026-03-06 | **작성**: Claude Opus 4.6
> **기준 문서**: SPEC.md v1.0, 코드 리뷰 2026-02-15
> **변경 이력**: v2.1 — 프론트엔드 Phase 1~3 완료, Parent View 와이어프레임 4개 완성, Auth 개편 플랜 승인 대기 상태 반영
