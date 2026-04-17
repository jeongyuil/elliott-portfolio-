# MyVoice (밤토리) - 배포 전 체크리스트

> 최종 업데이트: 2026-03-15

---

## P0: 필수 (없으면 앱 시작/핵심 기능 불가)

### 1. JWT Secret Key
- [ ] `JWT_SECRET_KEY` 생성 완료
- 용도: 모든 인증 토큰 서명
- 생성 방법:
  ```bash
  openssl rand -hex 32
  ```
- 주의: 기본값(`dev-secret-key-change-in-production`) 사용 시 프로덕션 앱 시작 실패

### 2. PostgreSQL 데이터베이스
- [ ] 프로덕션 DB 인스턴스 생성 완료
- [ ] `DATABASE_URL` 설정 완료
- [ ] Alembic 마이그레이션 실행 완료
- 권장: AWS RDS, GCP Cloud SQL, Supabase 등 관리형 서비스
- 형식: `postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}`
- 마이그레이션 실행:
  ```bash
  alembic upgrade head
  ```

### 3. Redis
- [ ] 프로덕션 Redis 인스턴스 생성 완료
- [ ] `REDIS_URL` 설정 완료
- 용도: 세션 상태 관리 (SessionOrchestrator), idempotency 캐시
- 권장: AWS ElastiCache, GCP Cloud Memorystore, Upstash 등
- 형식: `redis://{host}:{port}/{db}`

### 4. OpenAI API Key
- [ ] API 키 발급 완료
- [ ] 결제 수단 등록 완료
- [ ] 사용량 제한(Limits) 설정 완료
- 변수: `OPENAI_API_KEY`
- 용도: Whisper STT + GPT-4 대화 생성 + TTS 음성 합성
- 발급 위치: https://platform.openai.com/api-keys
- 설정 위치: https://platform.openai.com/settings/organization/billing
- 예상 비용: 아이 1회 세션(~5분) 약 $0.03~0.10
- 추천: Usage Limits에서 월간 상한 설정 (예: $50)

---

## P1: 중요 (핵심 사용자 경험에 영향)

### 5. Resend 이메일 서비스
- [ ] Resend 계정 생성 완료
- [ ] API 키 발급 완료
- [ ] 발송 도메인 인증 완료 (DNS 레코드 등록)
- 변수: `RESEND_API_KEY`, `EMAIL_FROM`, `EMAIL_FROM_NAME`
- 용도: 회원가입 인증 메일, 비밀번호 재설정 메일, 환영 메일
- 발급 위치: https://resend.com/api-keys
- 도메인 인증 절차:
  1. Resend Dashboard → Domains → "Add Domain" → `bamtory.com` 입력
  2. 표시되는 DNS 레코드 3개를 도메인 DNS에 추가:
     - SPF (TXT 레코드)
     - DKIM (TXT 레코드)
     - Return-Path (MX 또는 CNAME 레코드)
  3. DNS 전파 대기 (최대 48시간, 보통 수분~수시간)
  4. Resend에서 "Verify" 클릭
- 개발/테스트: 도메인 인증 없이 `onboarding@resend.dev`로 자기 이메일에만 발송 가능

### 6. Google OAuth
- [ ] GCP 프로젝트 생성 완료
- [ ] OAuth 동의 화면 구성 완료
- [ ] OAuth 2.0 클라이언트 ID 생성 완료
- [ ] 프로덕션 리디렉션 URI 등록 완료
- [ ] (프로덕션) OAuth 동의 화면 게시 완료
- 변수: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- 발급 위치: https://console.cloud.google.com
- 설정 절차:
  1. GCP Console → 새 프로젝트 생성 (예: "bamtori-prod")
  2. API 및 서비스 → OAuth 동의 화면
     - 앱 이름: 밤토리
     - 지원 이메일: 운영 이메일
     - 승인된 도메인: `bamtory.com`
     - 범위: `email`, `profile`, `openid`
  3. 사용자 인증 정보 → OAuth 클라이언트 ID 만들기
     - 애플리케이션 유형: 웹 애플리케이션
     - 승인된 리디렉션 URI: `https://api.bamtory.com/v1/auth/google/callback`
  4. 클라이언트 ID, 클라이언트 보안 비밀번호 복사
- 참고: 개발 모드에서는 테스트 사용자만 로그인 가능. 프로덕션 게시 시 Google 심사 1~2주 소요

### 7. Kakao OAuth
- [ ] Kakao Developers 앱 생성 완료
- [ ] 카카오 로그인 활성화 완료
- [ ] Redirect URI 등록 완료
- [ ] Client Secret 생성 완료
- [ ] 동의항목(닉네임, 이메일) 설정 완료
- [ ] (선택) 비즈 앱 전환 완료
- 변수: `KAKAO_CLIENT_ID`, `KAKAO_CLIENT_SECRET`
- 발급 위치: https://developers.kakao.com
- 설정 절차:
  1. 내 애플리케이션 → 앱 추가
  2. 앱 키 → REST API 키 = `KAKAO_CLIENT_ID`
  3. 제품 설정 → 카카오 로그인 → 활성화 ON
  4. 카카오 로그인 → Redirect URI 추가:
     `https://api.bamtory.com/v1/auth/kakao/callback`
  5. 보안 → Client Secret → 생성 = `KAKAO_CLIENT_SECRET`
     → 활성화 상태: "사용함"으로 변경
  6. 동의항목:
     - 닉네임: 필수 동의
     - 카카오계정(이메일): 필수 동의 (비즈 앱 필요)
- 참고: 이메일 필수 동의를 위해 비즈 앱 전환 권장 (사업자등록증 필요)

---

## P2: 권장 (없어도 대체 수단 있음)

### 8. Apple Sign In
- [ ] Apple Developer Program 가입 완료 ($99/년)
- [ ] App ID 등록 완료
- [ ] Services ID 등록 완료 (웹 로그인용)
- [ ] Sign In with Apple 키 생성 완료
- [ ] `.p8` 키 파일 보관 완료
- 변수: `APPLE_TEAM_ID`, `APPLE_KEY_ID`, `APPLE_PRIVATE_KEY`, `APPLE_BUNDLE_ID`
- 발급 위치: https://developer.apple.com/account
- 비용: Apple Developer Program 연 $99
- 설정 절차:
  1. Certificates, Identifiers & Profiles → Identifiers
  2. App ID 등록 → Capabilities에서 "Sign In with Apple" 체크
  3. Services ID 등록 (웹 로그인용):
     - Identifier: `com.bamtory.auth` (예시)
     - Sign In with Apple → Configure
     - Domains: `api.bamtory.com`
     - Return URLs: `https://api.bamtory.com/v1/auth/apple/callback`
  4. Keys → 새 키 생성 → "Sign In with Apple" 체크
     - `.p8` 파일 다운로드 (1회만 가능, 안전하게 보관)
  5. 값 매핑:
     - `APPLE_TEAM_ID`: 개발자 계정 페이지 우측 상단 Team ID
     - `APPLE_KEY_ID`: 키 생성 시 표시되는 10자리 Key ID
     - `APPLE_PRIVATE_KEY`: `.p8` 파일 내용 (줄바꿈을 `\n`으로 치환)
     - `APPLE_BUNDLE_ID`: Services ID (웹용, 예: `com.bamtory.auth`)
- 대안: Apple 로그인 없이 Google/Kakao/이메일 로그인으로 운영 가능

---

## P3: 선택 (향후 확장)

### 9. Azure OpenAI Realtime API
- [ ] Azure 구독 생성 완료
- [ ] Azure OpenAI 리소스 생성 완료
- [ ] gpt-4o-realtime-preview 모델 배포 완료
- [ ] (필요 시) Whisper 모델 별도 배포 완료
- 변수:
  - `VOICE_MODE=websocket` (전환 시)
  - `AZURE_REALTIME_API_KEY`, `AZURE_REALTIME_ENDPOINT`
  - `AZURE_REALTIME_API_VERSION` (기본: `2025-04-01-preview`)
  - `AZURE_REALTIME_DEPLOYMENT` (기본: `gpt-4o-realtime-preview`)
  - `AZURE_WHISPER_*` (별도 Whisper 배포 시, 없으면 Realtime 설정 사용)
- 발급 위치: https://portal.azure.com
- 설정 절차:
  1. Azure Portal → 리소스 만들기 → "Azure OpenAI" 검색
  2. 리소스 생성 (리전: East US 또는 Sweden Central - Realtime 지원 리전)
  3. Azure AI Studio (https://ai.azure.com) → 배포 → 모델 배포:
     - `gpt-4o-realtime-preview` 배포
     - (선택) `whisper` 배포
  4. Azure Portal → 리소스 → 키 및 엔드포인트:
     - KEY1 → `AZURE_REALTIME_API_KEY`
     - 엔드포인트 → `AZURE_REALTIME_ENDPOINT` (예: `https://myvoice-ai.openai.azure.com`)
- 참고: Realtime API는 현재 특정 리전에서만 사용 가능. 별도 액세스 신청 필요할 수 있음
- 대안: `VOICE_MODE=http`로 기존 OpenAI API 사용 (현재 기본값)

---

## 인프라 설정

### 10. 도메인 및 URL
- [ ] 백엔드 도메인 확보 (예: `api.bamtory.com`)
- [ ] 프론트엔드 도메인 확보 (예: `app.bamtory.com`)
- [ ] SSL 인증서 설정 완료
- [ ] `APP_BASE_URL` 설정 (예: `https://api.bamtory.com`)
- [ ] `FRONTEND_URL` 설정 (예: `https://app.bamtory.com`)
- [ ] `CORS_ORIGINS` 설정 (예: `["https://app.bamtory.com"]`)

### 11. 환경 변수
- [ ] `APP_ENV=production` 설정
- [ ] `DEBUG=false` 설정

---

## 최종 검증

- [ ] `docker compose -f docker-compose.prod.yml up` 정상 기동
- [ ] `/health` 엔드포인트 200 응답
- [ ] `/health/deep` 엔드포인트 200 응답 (DB + Redis 연결 확인)
- [ ] 이메일 회원가입 → 인증 메일 수신 확인
- [ ] 소셜 로그인 플로우 (Google/Kakao) 정상 작동
- [ ] 아이 모드 음성 세션 정상 작동
- [ ] 모바일 브라우저에서 전체 플로우 확인
