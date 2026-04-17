# Phase 2: Kids View Frontend — 밤토리 (Bamtory) MVP

> **상태**: ✅ **완료** (2026-02 완료)
> 이 프롬프트는 Gemini에게 전달되어 실행 완료되었습니다.
> 결과: Kids View 11개 페이지 모두 Crystal 프로토타입 기반으로 구현 완료 (KidHome, Adventures, AdventureDetail/Play/Result, Vocabulary/Learning/Result, KidProfile, KidSkills, KidShop).

## 전제 조건

> **Phase 1이 완료된 상태**여야 합니다.
> 
> 다음이 이미 존재해야 합니다:
> - `myvoice/frontend/` React + Vite + TypeScript 프로젝트
> - `src/index.css` Crystal 디자인 시스템 (CSS 변수, 커스텀 클래스)
> - `src/api/client.ts` REST API 클라이언트
> - `src/api/hooks/` React Query 훅 (useAdventures, useWeeklyGoals 등)
> - `src/contexts/AuthContext.tsx` 인증 컨텍스트
> - `src/App.tsx` React Router 라우팅 (placeholder 페이지들)
> - `src/components/layout/BottomNav.tsx` 하단 네비게이션
> - `src/guards/KidProtectedRoute.tsx` 인증 가드

## 작업 0: Phase 1 누락사항 보완

Phase 1에서 누락된 항목들을 먼저 보완합니다.

### 0-1. `index.html` 타이틀 변경

```html
<!-- 변경 전 -->
<title>Vite + React + TS</title>

<!-- 변경 후 -->
<title>밤토리 (Bamtory) - Voice AI 영어 학습</title>
```

### 0-2. Toaster 컴포넌트 마운트

`frontend/src/main.tsx`에 `sonner`의 `<Toaster />` 컴포넌트를 추가하세요.
Phase 2의 여러 컴포넌트에서 `toast()` 함수를 사용합니다.

```typescript
import { Toaster } from 'sonner';

// ...기존 코드에 추가
<React.StrictMode>
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <AuthProvider>
        <App />
        <Toaster position="top-center" richColors /> {/* 추가 */}
      </AuthProvider>
    </BrowserRouter>
  </QueryClientProvider>
</React.StrictMode>
```

### 0-3. 세부 라우트 등록

`frontend/src/App.tsx`의 Kid 라우트에 다음 경로들을 추가하세요.
(해당 페이지 컴포넌트는 작업 6~9에서 만듭니다)

```typescript
<Route path="kid" element={<KidLayout />}>
  <Route path="home" element={<KidHome />} />
  <Route path="adventures" element={<Adventures />} />
  <Route path="adventure/:id" element={<AdventureDetail />} />        {/* 추가 */}
  <Route path="adventure/:id/play" element={<AdventurePlay />} />     {/* 추가 */}
  <Route path="adventure/:id/result" element={<AdventureResult />} /> {/* 추가 */}
  <Route path="vocabulary" element={<Vocabulary />} />
  <Route path="vocabulary/:cat" element={<VocabularyLearning />} />       {/* 추가 */}
  <Route path="vocabulary/:cat/result" element={<VocabularyResult />} />  {/* 추가 */}
  <Route path="shop" element={<Shop />} />
  <Route path="profile" element={<Profile />} />
  <Route path="skills" element={<Skills />} />
</Route>
```

---

## 목표

Phase 1에서 만든 placeholder 페이지들을 Crystal 프로토타입의 실제 UI로 교체합니다.
Kids View의 모든 화면을 완성하는 것이 목표입니다.

---

## 전환 규칙 (Crystal → Kids View 포팅 시 반드시 적용)

### 1. 라이브러리 전환

| Crystal (사용 금지) | → Kids View (사용할 것) |
|-------------------|----------------------|
| `import { useRoute, useLocation } from "wouter"` | `import { useParams, useNavigate, useLocation } from "react-router-dom"` |
| `import { trpc } from "@/lib/trpc"` | `import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"` + `import { api } from "@/api/client"` |
| `import { missions } from "@/lib/mockData"` | `import { missions } from "@/lib/mockData"` (Phase 2에서는 mockData 유지, Phase 3에서 API 연동) |

### 2. tRPC → React Query 변환 패턴

**Crystal (tRPC):**
```typescript
const { data } = trpc.weeklyGoals.getCurrent.useQuery();
const mutation = trpc.missions.updateStatus.useMutation({ onSuccess: () => {} });
```

**Kids View (React Query):**
```typescript
const { data } = useQuery({
  queryKey: ['weeklyGoals'],
  queryFn: () => api.get('/v1/kid/goals'),
});
const queryClient = useQueryClient();
const mutation = useMutation({
  mutationFn: (data) => api.post('/v1/kid/sessions/complete', data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['weeklyGoals'] });
  },
});
```

### 3. wouter → React Router 변환 패턴

**Crystal (wouter):**
```typescript
const [, params] = useRoute("/mission/:id/play");
const [, setLocation] = useLocation();
setLocation("/missions");
```

**Kids View (React Router):**
```typescript
const { id } = useParams();
const navigate = useNavigate();
navigate("/kid/adventures");
```

### 4. 용어 변환

| Crystal | → Kids View |
|---------|------------|
| 미션 (Mission) | 모험 (Adventure) |
| 미션 목록 | 모험 목록 |
| 미션 상세 | 모험 상세 |
| 미션 완료 | 모험 완료 |
| 미션을 찾을 수 없습니다 | 모험을 찾을 수 없습니다 |
| `/missions` | `/kid/adventures` |
| `/mission/:id` | `/kid/adventure/:id` |
| `/mission/:id/play` | `/kid/adventure/:id/play` |
| `/mission/:id/result` | `/kid/adventure/:id/result` |

---

## 작업 1: MockData 이식

Crystal의 `mockData.ts`를 `frontend/src/lib/mockData.ts`로 복사하세요.

**참조:** `crystal/task_source/mockData.ts`

Phase 2에서는 mockData를 그대로 사용합니다. Phase 3에서 실제 API로 교체할 예정입니다.
이렇게 하면 백엔드 없이도 UI를 완성하고 테스트할 수 있습니다.

> **주의:** mockData 내의 필드명은 유지하되, UI 라벨에서 "미션"은 "모험"으로 변경하세요.

## 작업 2: 음성 인식 유틸리티 이식

Crystal의 `speechRecognition.ts`를 `frontend/src/lib/speechRecognition.ts`로 복사하세요.

**참조:** `crystal/task_source/speechRecognition.ts`

이 파일은 Web Speech API 래퍼이며, Phase 2에서는 그대로 사용합니다.
Phase 3에서 서버사이드 Whisper로 교체할 예정입니다.

## 작업 3: UI 컴포넌트 이식

Crystal에서 재사용 가능한 컴포넌트를 이식하세요:

### `src/components/mission/MissionCard.tsx`
- **참조:** `crystal/task_source/MissionCard.tsx`
- 라벨만 "미션" → "모험"으로 변경
- Link 경로를 `/kid/adventure/:id`로 수정
- wouter Link → react-router-dom Link

### `src/components/DailyBonusModal.tsx`
- **참조:** `crystal/task_source/DailyBonusModal.tsx`
- 그대로 이식 (tRPC 의존 없음)

### `src/components/OnboardingTutorial.tsx`
- **참조:** `crystal/task_source/OnboardingTutorial.tsx`
- "미션" 텍스트 → "모험"으로 변경

### `src/components/ProgressCard.tsx`
- **참조:** `crystal/task_source/ProgressCard.tsx`
- 그대로 이식

### `src/components/SkillProgress.tsx`
- **참조:** `crystal/task_source/SkillProgress.tsx`
- 그대로 이식

## 작업 4: 홈 화면 (KidHome)

**참조:** `crystal/task_source/Home.tsx` (347줄)

### `src/pages/kid/KidHome.tsx`

Crystal의 Home.tsx를 포팅하면서 다음을 변경:

1. **tRPC 호출 → React Query 훅 사용**
   - `trpc.weeklyGoals.getCurrent.useQuery()` → `useWeeklyGoals()` (Phase 1에서 만든 훅)
   - `trpc.missions.getUserMissions.useQuery()` → `useAdventures()`
   - `trpc.dailyBonus.claimDailyBonus.useMutation()` → `useClaimDailyBonus()`
   - `trpc.user.completeOnboarding.useMutation()` → `useMutation(...)` 직접 구현

2. **wouter → React Router**
   - `<Link href="/missions">` → `<Link to="/kid/adventures">`
   - `<Link href="/vocabulary">` → `<Link to="/kid/vocabulary">`
   - `<Link href="/shop">` → `<Link to="/kid/shop">`
   - `<Link href="/skills">` → `<Link to="/kid/skills">`

3. **인증**
   - `useAuth()` → Phase 1에서 만든 AuthContext의 `useAuth()` 사용
   - `getLoginUrl()` → `/login`으로 변경

4. **라벨 변경**
   - "오늘의 미션" → "오늘의 모험"
   - "전체보기" 링크 → `/kid/adventures`

5. **나머지는 Crystal 그대로 유지**
   - Pull-to-refresh
   - Weekly goals summary card
   - Quick actions grid
   - Learning tips section
   - Daily bonus modal
   - Onboarding tutorial

## 작업 5: 모험 목록 (Adventures)

**참조:** `crystal/task_source/MissionList.tsx` (72줄)

### `src/pages/kid/Adventures.tsx`

간단한 포팅:
- 필터 탭 (전체/쉬움/보통/어려움) 유지
- 그리드 레이아웃 유지
- `<BottomNav />` → Phase 1의 KidLayout에서 이미 포함되므로, 여기서는 제거
- "미션" → "모험" 라벨 변경
- `missions` mock 데이터 사용

## 작업 6: 모험 상세 (AdventureDetail)

**참조:** `crystal/task_source/MissionDetail.tsx` (153줄)

### `src/pages/kid/AdventureDetail.tsx`

1. **wouter → React Router**
   - `useParams()` from react-router-dom
   - `useNavigate()` for navigation

2. **tRPC → React Query**
   - `trpc.missions.updateStatus.useMutation()` → 직접 mutation 구현
   - 낙관적 업데이트 패턴을 React Query로 변환

3. **라벨 변경**
   - "미션 상세" → "모험 상세"
   - "미션 완료하기" → "모험 시작하기" (이 버튼은 play 페이지로 이동)

4. **네비게이션 변경**
   - 뒤로가기 → `/kid/adventures`
   - "시작하기" → `/kid/adventure/:id/play`

## 작업 7: 모험 진행 (AdventurePlay)

**참조:** `crystal/task_source/MissionPlay.tsx` (270줄) — 가장 복잡한 화면

### `src/pages/kid/AdventurePlay.tsx`

이 화면은 음성 인식을 사용하는 핵심 학습 인터페이스입니다.

1. **wouter → React Router**
   - `useRoute("/mission/:id/play")` → `useParams()`

2. **음성 인식 유지**
   - `speechRecognition.ts` 유틸리티 그대로 사용 (Phase 3에서 Whisper로 교체 예정)
   - 마이크 버튼, 듣기 표시기, 발음 결과 UI 모두 그대로 유지

3. **네비게이션 변경**
   - 포기 시 → `/kid/home`
   - 성공 시 → `/kid/adventure/:id/result?success=true&stars=...&xp=...`
   - 실패(타임아웃) 시 → `/kid/adventure/:id/result?success=false`

4. **UI 그대로 유지**
   - 타이머 (3분)
   - 난이도 표시
   - 힌트/포기 버튼
   - 시나리오 텍스트
   - 포포 가이드 말풍선
   - 발음 결과 카드 (정확도 %)
   - 듣기 중 오버레이

## 작업 8: 모험 결과 (AdventureResult)

**참조:** `crystal/task_source/MissionResult.tsx` (99줄)

### `src/pages/kid/AdventureResult.tsx`

1. **tRPC → React Query**: 낙관적 업데이트 → React Query mutation
2. **wouter → React Router**: 경로 변경
3. **라벨 변경**: "미션" → "모험"
4. **네비게이션**: 홈(`/kid/home`), 목록(`/kid/adventures`)

## 작업 9: 어휘 학습 화면들

### `src/pages/kid/Vocabulary.tsx` — 어휘 목록
- **참조:** `crystal/task_source/VocabularyList.tsx`
- 카테고리 그리드 (음식, 동물, 색깔 등)
- 진행률 표시 (X/10 단어, N%)
- 상태 뱃지 (완료/진행중/새로운)
- BottomNav는 KidLayout에서 제공

### `src/pages/kid/VocabularyLearning.tsx` — 어휘 학습
- **참조:** `crystal/task_source/VocabularyLearning.tsx` (298줄)
- 플래시카드 UI (이모지 + 영어 + 한국어)
- 듣기 (TTS) + 말하기 (Web Speech API) 기능
- 진행 바 (현재/전체 단어)
- 이전/다음 네비게이션 버튼
- wouter → React Router, 경로를 `/kid/vocabulary/:cat`으로

### `src/pages/kid/VocabularyResult.tsx` — 어휘 결과
- **참조:** `crystal/task_source/VocabularyResult.tsx` (177줄)
- 성공 애니메이션 + 보상 표시
- tRPC → React Query mutation
- 네비게이션: 홈(`/kid/home`), 다음 학습(`/kid/vocabulary`)

## 작업 10: 프로필 & 스킬

### `src/pages/kid/KidProfile.tsx`
- **참조:** `crystal/task_source/Profile.tsx`
- 아바타/이름, 레벨, XP 바
- 통계 그리드 (완료 모험, 학습 시간, 어휘 수, 발음 정확도)
- 주간 학습량 막대 그래프
- 배지 목록
- 로그아웃 버튼 → AuthContext의 `logout()` 호출
- "미션" 텍스트 → "모험"

### `src/pages/kid/KidSkills.tsx`
- **참조:** `crystal/task_source/Skills.tsx` (473줄)
- 이번 주 목표 (XP, 모험, 시간, 단어)
- 목표 수정 모달 (AI 추천 포함)
- 스킬 진행도 (11개 스킬 카테고리)
- 학습 분석 (기간별 그래프, 또래 비교)
- wouter Link → react-router-dom Link

## 작업 11: 상점

### `src/pages/kid/KidShop.tsx`
- **참조:** `crystal/task_source/Shop.tsx` (112줄)
- 보유 별 표시
- 인벤토리 (힌트, 시간 연장, 하트 충전)
- 상점 아이템 그리드 + 구매 버튼
- 구매 로직은 local state로 유지 (Phase 3에서 API 연동)
- toast 알림 유지

---

## 라우팅 업데이트

Phase 1의 `App.tsx`에서 placeholder 페이지들을 실제 컴포넌트로 교체:

```typescript
// Phase 2에서 교체하는 import
import KidHome from '@/pages/kid/KidHome';
import Adventures from '@/pages/kid/Adventures';
import AdventureDetail from '@/pages/kid/AdventureDetail';
import AdventurePlay from '@/pages/kid/AdventurePlay';
import AdventureResult from '@/pages/kid/AdventureResult';
import Vocabulary from '@/pages/kid/Vocabulary';
import VocabularyLearning from '@/pages/kid/VocabularyLearning';
import VocabularyResult from '@/pages/kid/VocabularyResult';
import KidProfile from '@/pages/kid/KidProfile';
import KidSkills from '@/pages/kid/KidSkills';
import KidShop from '@/pages/kid/KidShop';
```

---

## 검증 기준

Phase 2 완료 후 다음을 확인하세요:

1. ✅ `npm run build` — 빌드 에러 없음
2. ✅ `npm run dev` → 모든 페이지가 정상 렌더링됨
3. ✅ 홈 화면 (`/kid/home`):
   - 주간 목표 카드 표시 (mockData 기반)
   - 오늘의 모험 카드 3개 표시
   - 어휘 학습 / 상점 퀵 액션
   - BottomNav 동작
4. ✅ 모험 플로우:
   - 목록 → 카드 클릭 → 상세 → "시작하기" → 플레이 → 결과
   - 필터 동작 (전체/쉬움/보통/어려움)
5. ✅ 모험 플레이:
   - 타이머 카운트다운
   - 마이크 버튼 → 음성 인식 시작/정지
   - 발음 결과 표시 (정확도 %)
   - 성공/실패 시 결과 페이지로 이동
6. ✅ 어휘 학습:
   - 카테고리 목록 → 카테고리 선택 → 플래시카드 학습 → 결과
   - 듣기/말하기 버튼 동작
7. ✅ 프로필/스킬/상점:
   - 통계 표시, 배지 표시
   - 스킬 목표 수정 가능
   - 상점 아이템 구매 (local state)

## ⛔ 금지 사항

- ❌ tRPC 사용 금지
- ❌ wouter 사용 금지
- ❌ 백엔드 API 호출 금지 (Phase 2는 mockData 기반. API 훅은 만들어두되 실제 호출하지 않음)
- ❌ Crystal의 서버 코드 복사 금지 (db.ts, routers.ts, schema.ts)
- ❌ `app/` 디렉토리 수정 금지
- ❌ `crystal/` 디렉토리 수정 금지

## 참조 Crystal 파일 전체 목록

| 파일 | 줄 수 | 포팅 대상 | 변경 수준 |
|------|-------|----------|----------|
| `Home.tsx` | 347 | `KidHome.tsx` | 높음 (tRPC→RQ, 경로, 라벨) |
| `MissionList.tsx` | 72 | `Adventures.tsx` | 낮음 (경로, 라벨) |
| `MissionDetail.tsx` | 153 | `AdventureDetail.tsx` | 중간 (tRPC→RQ, 경로) |
| `MissionPlay.tsx` | 270 | `AdventurePlay.tsx` | 중간 (경로만, 음성인식 유지) |
| `MissionResult.tsx` | 99 | `AdventureResult.tsx` | 중간 (tRPC→RQ, 경로) |
| `VocabularyList.tsx` | - | `Vocabulary.tsx` | 낮음 (경로) |
| `VocabularyLearning.tsx` | 298 | `VocabularyLearning.tsx` | 중간 (경로, 음성인식 유지) |
| `VocabularyResult.tsx` | 177 | `VocabularyResult.tsx` | 중간 (tRPC→RQ, 경로) |
| `Profile.tsx` | - | `KidProfile.tsx` | 중간 (인증, 경로) |
| `Skills.tsx` | 473 | `KidSkills.tsx` | 높음 (tRPC→RQ, 경로, 모달) |
| `Shop.tsx` | 112 | `KidShop.tsx` | 낮음 (local state 유지) |
| `MissionCard.tsx` | - | `MissionCard.tsx` | 낮음 (Link 경로) |
| `DailyBonusModal.tsx` | - | `DailyBonusModal.tsx` | 없음 (그대로) |
| `OnboardingTutorial.tsx` | - | `OnboardingTutorial.tsx` | 낮음 (라벨만) |
| `ProgressCard.tsx` | - | `ProgressCard.tsx` | 없음 (그대로) |
| `SkillProgress.tsx` | - | `SkillProgress.tsx` | 없음 (그대로) |
| `mockData.ts` | - | `mockData.ts` | 없음 (그대로 복사) |
| `speechRecognition.ts` | - | `speechRecognition.ts` | 없음 (그대로 복사) |

## 결과물 디렉토리 구조 (예상)

```
frontend/src/
├── api/                        # (Phase 1에서 생성됨)
├── components/
│   ├── layout/
│   │   ├── BottomNav.tsx      # (Phase 1)
│   │   └── KidLayout.tsx      # (Phase 1)
│   ├── mission/
│   │   └── MissionCard.tsx    # [Phase 2] Crystal에서 이식
│   ├── DailyBonusModal.tsx    # [Phase 2] Crystal에서 이식
│   ├── OnboardingTutorial.tsx # [Phase 2] Crystal에서 이식
│   ├── ProgressCard.tsx       # [Phase 2] Crystal에서 이식
│   └── SkillProgress.tsx      # [Phase 2] Crystal에서 이식
├── contexts/                   # (Phase 1)
├── guards/                     # (Phase 1)
├── lib/
│   ├── mockData.ts            # [Phase 2] Crystal에서 복사
│   └── speechRecognition.ts   # [Phase 2] Crystal에서 복사
├── pages/
│   ├── kid/
│   │   ├── KidHome.tsx        # [Phase 2] Crystal Home.tsx 포팅
│   │   ├── Adventures.tsx     # [Phase 2] Crystal MissionList.tsx 포팅
│   │   ├── AdventureDetail.tsx # [Phase 2] Crystal MissionDetail.tsx 포팅
│   │   ├── AdventurePlay.tsx  # [Phase 2] Crystal MissionPlay.tsx 포팅
│   │   ├── AdventureResult.tsx # [Phase 2] Crystal MissionResult.tsx 포팅
│   │   ├── Vocabulary.tsx     # [Phase 2] Crystal VocabularyList.tsx 포팅
│   │   ├── VocabularyLearning.tsx # [Phase 2] Crystal VocabularyLearning.tsx 포팅
│   │   ├── VocabularyResult.tsx   # [Phase 2] Crystal VocabularyResult.tsx 포팅
│   │   ├── KidProfile.tsx     # [Phase 2] Crystal Profile.tsx 포팅
│   │   ├── KidSkills.tsx      # [Phase 2] Crystal Skills.tsx 포팅
│   │   └── KidShop.tsx        # [Phase 2] Crystal Shop.tsx 포팅
│   ├── parent/                # (Phase 4)
│   ├── Login.tsx              # (Phase 1)
│   └── Landing.tsx            # (Phase 1)
├── App.tsx                     # Phase 2에서 import 교체
├── main.tsx
└── index.css
```
