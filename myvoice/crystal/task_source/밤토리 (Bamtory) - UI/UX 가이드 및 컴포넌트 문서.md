# 밤토리 (Bamtory) - UI/UX 가이드 및 컴포넌트 문서

**작성일:** 2026년 2월 13일  
**작성자:** Manus AI  
**버전:** 1.0

---

## 디자인 철학

밤토리는 Duolingo에서 영감을 받은 게임화된 학습 경험을 제공합니다. 디자인은 아이들이 좋아할 만한 친근하고 재미있는 스타일을 지향하며, 마이크로 인터랙션이 풍부하여 사용자의 참여를 유도합니다. 검은 테두리가 강한 네오-브루탈리즘 스타일은 피하고, 부드러운 그라디언트와 라운드 처리된 요소를 사용합니다.

### 핵심 디자인 원칙

밤토리의 디자인은 다음 원칙을 따릅니다.

**친근함과 재미**는 밝은 색상, 이모지, 애니메이션을 통해 학습을 즐겁게 만듭니다. 사용자는 Luna라는 캐릭터와 함께 여정을 떠나며, 미션을 완료할 때마다 성취감을 느낍니다.

**명확한 피드백**은 모든 액션에 즉각적인 시각적 피드백을 제공합니다. 별을 획득하면 반짝이는 애니메이션이 나타나고, 미션을 완료하면 축하 메시지가 표시됩니다.

**모바일 최적화**는 터치 인터랙션에 최적화된 UI를 제공합니다. 버튼은 충분히 크고, 스와이프와 풀투리프레시 같은 모바일 제스처를 지원합니다.

**일관성**은 전체 앱에서 동일한 색상, 타이포그래피, 간격을 사용하여 학습 곡선을 줄입니다. shadcn/ui 컴포넌트를 기반으로 일관된 디자인 시스템을 구축합니다.

---

## 색상 시스템

밤토리는 Duolingo 스타일의 밝고 활기찬 색상 팔레트를 사용합니다.

### 주요 색상

| 색상 이름 | CSS 변수 | 값 | 용도 |
|-----------|----------|-----|------|
| Duo Green | `--duo-green` | `#58CC02` | 주요 액션, 성공 메시지 |
| Duo Blue | `--duo-blue` | `#1CB0F6` | 정보, 링크 |
| Duo Yellow | `--duo-yellow` | `#FFC800` | 경고, 별 보상 |
| Duo Red | `--duo-red` | `#FF4B4B` | 하트, 오류 |
| Duo Purple | `--duo-purple` | `#CE82FF` | 프리미엄, 특별 기능 |
| Duo Orange | `--duo-orange` | `#FF9600` | 스트릭, 불꽃 |

### 배경 색상

| 색상 이름 | CSS 변수 | 값 | 용도 |
|-----------|----------|-----|------|
| Background | `--duo-bg` | `#F7F7F7` | 메인 배경 |
| Card Background | `--duo-card-bg` | `#FFFFFF` | 카드 배경 |
| Text Primary | `--duo-text` | `#3C3C3C` | 주요 텍스트 |
| Text Secondary | `--duo-text-secondary` | `#777777` | 보조 텍스트 |

### 그라디언트

밤토리는 부드러운 그라디언트를 사용하여 시각적 흥미를 더합니다.

```css
/* 스트릭 카드 그라디언트 */
.duo-streak-card {
  background: linear-gradient(135deg, #FF9600 0%, #FF6B00 100%);
}

/* 로그인 보너스 모달 그라디언트 */
.bonus-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 주간 목표 카드 그라디언트 */
.weekly-goal-gradient {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}
```

---

## 타이포그래피

밤토리는 가독성과 친근함을 위해 Pretendard 폰트를 사용합니다.

### 폰트 스케일

| 스타일 | 크기 | 용도 |
|--------|------|------|
| H1 | 24px (1.5rem) | 페이지 제목 |
| H2 | 20px (1.25rem) | 섹션 제목 |
| H3 | 18px (1.125rem) | 카드 제목 |
| Body | 16px (1rem) | 본문 텍스트 |
| Small | 14px (0.875rem) | 보조 정보 |
| XSmall | 12px (0.75rem) | 라벨, 캡션 |

### 폰트 웨이트

| 웨이트 | 값 | 용도 |
|--------|-----|------|
| Regular | 400 | 일반 텍스트 |
| Medium | 500 | 강조 텍스트 |
| Semibold | 600 | 버튼, 제목 |
| Bold | 700 | 중요 정보, 숫자 |

---

## 간격 시스템

밤토리는 8px 기반 간격 시스템을 사용합니다.

| 이름 | 값 | Tailwind 클래스 | 용도 |
|------|-----|-----------------|------|
| XS | 4px | `gap-1`, `p-1` | 아이콘과 텍스트 사이 |
| SM | 8px | `gap-2`, `p-2` | 작은 요소 간격 |
| MD | 12px | `gap-3`, `p-3` | 일반 요소 간격 |
| LG | 16px | `gap-4`, `p-4` | 카드 내부 패딩 |
| XL | 24px | `gap-6`, `p-6` | 섹션 간격 |
| 2XL | 32px | `gap-8`, `p-8` | 큰 섹션 간격 |

---

## 컴포넌트 라이브러리

밤토리는 shadcn/ui를 기반으로 커스텀 컴포넌트를 구축합니다.

### 기본 컴포넌트

#### Button

버튼은 사용자 액션의 주요 진입점입니다.

**변형:**
- `default`: 주요 액션 (Duo Green 배경)
- `outline`: 보조 액션 (투명 배경, 테두리)
- `ghost`: 텍스트 버튼 (배경 없음)
- `destructive`: 위험한 액션 (Duo Red 배경)

**크기:**
- `sm`: 작은 버튼 (높이 32px)
- `default`: 기본 버튼 (높이 40px)
- `lg`: 큰 버튼 (높이 48px)

**사용 예시:**
```tsx
<Button variant="default" size="lg">
  미션 시작하기
</Button>
```

#### Card

카드는 관련 정보를 그룹화하는 컨테이너입니다.

**스타일:**
- 흰색 배경 (`bg-white`)
- 부드러운 그림자 (`shadow-sm`)
- 라운드 코너 (`rounded-xl`)
- 내부 패딩 (`p-4`)

**사용 예시:**
```tsx
<div className="duo-card p-4">
  <h3 className="font-bold text-lg">Luna Meets Friends</h3>
  <p className="text-sm text-duo-text-secondary">5분 • +15별</p>
</div>
```

#### Dialog

다이얼로그는 중요한 정보나 액션을 모달로 표시합니다.

**특징:**
- 배경 오버레이 (반투명 검은색)
- 중앙 정렬
- 애니메이션 (페이드 인/아웃)
- 접근성 (DialogTitle, DialogDescription 필수)

**사용 예시:**
```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogTitle className="sr-only">일일 로그인 보너스</DialogTitle>
    <DialogDescription className="sr-only">
      오늘의 로그인 보너스를 획득했습니다
    </DialogDescription>
    {/* 모달 내용 */}
  </DialogContent>
</Dialog>
```

### 커스텀 컴포넌트

#### DailyBonusModal

일일 로그인 보너스를 표시하는 모달입니다.

**위치:** `client/src/components/DailyBonusModal.tsx`

**기능:**
- 그라디언트 배경 애니메이션
- 연속 로그인 일수 표시
- 별과 하트 보상 표시
- 슬라이드 인 애니메이션

**Props:**
```typescript
interface DailyBonusModalProps {
  isOpen: boolean;
  onClose: () => void;
  reward: {
    stars: number;
    hearts: number;
    consecutiveDays: number;
  };
}
```

**사용 예시:**
```tsx
<DailyBonusModal
  isOpen={showBonus}
  onClose={() => setShowBonus(false)}
  reward={{ stars: 5, hearts: 1, consecutiveDays: 3 }}
/>
```

#### OnboardingTutorial

신규 사용자를 위한 온보딩 튜토리얼입니다.

**위치:** `client/src/components/OnboardingTutorial.tsx`

**기능:**
- 5단계 슬라이드 (환영, 미션, 별, 일일보상, 주간목표)
- 프로그레스 닷 표시
- 이전/다음 버튼
- 건너뛰기 버튼 (X)

**Props:**
```typescript
interface OnboardingTutorialProps {
  isOpen: boolean;
  onComplete: () => void;
}
```

**사용 예시:**
```tsx
<OnboardingTutorial
  isOpen={!user?.onboardingCompleted}
  onComplete={handleOnboardingComplete}
/>
```

#### MissionCard

미션을 표시하는 카드 컴포넌트입니다.

**위치:** `client/src/components/mission/MissionCard.tsx`

**기능:**
- 미션 이모지, 제목, 소요 시간, 보상 표시
- 상태별 스타일 (완료, 진행 중, 잠김)
- 클릭 시 미션 상세 페이지로 이동

**Props:**
```typescript
interface MissionCardProps {
  id: number;
  emoji: string;
  title: string;
  duration: number;
  stars: number;
  status: "completed" | "in_progress" | "locked";
}
```

#### BottomNav

하단 네비게이션 바입니다.

**위치:** `client/src/components/layout/BottomNav.tsx`

**기능:**
- 5개 탭 (홈, 미션, 보상, 어휘, 프로필)
- 현재 페이지 하이라이트
- 아이콘 + 라벨

**사용 예시:**
```tsx
<BottomNav />
```

#### ProtectedRoute

인증이 필요한 라우트를 보호하는 컴포넌트입니다.

**위치:** `client/src/components/ProtectedRoute.tsx`

**기능:**
- 비로그인 사용자 자동 리다이렉트
- 로딩 중 스피너 표시

**사용 예시:**
```tsx
<ProtectedRoute>
  <Home />
</ProtectedRoute>
```

---

## 페이지 구조

밤토리는 5개의 주요 페이지로 구성됩니다.

### Home (홈)

**경로:** `/`  
**파일:** `client/src/pages/Home.tsx`

**구성 요소:**
- 사용자 정보 (닉네임, 아바타, 하트)
- 스트릭 카드 (연속 로그인 일수)
- 오늘의 미션 (3개 미리보기)
- 빠른 액션 (어휘 학습, 상점)
- 이번 주 목표 (4개 지표)
- 학습 팁

**특징:**
- 풀투리프레시 지원
- 스크롤 가능 (스크롤바 숨김)
- 하단 네비게이션

### Missions (미션)

**경로:** `/missions`  
**파일:** `client/src/pages/Missions.tsx`

**구성 요소:**
- 미션 목록 (카테고리별)
- 필터 (전체, 완료, 진행 중)
- 미션 카드 (이모지, 제목, 소요 시간, 보상)

**특징:**
- 상태별 색상 구분
- 클릭 시 미션 상세 페이지로 이동

### Rewards (보상)

**경로:** `/rewards`  
**파일:** `client/src/pages/Rewards.tsx`

**구성 요소:**
- 일일 보상 캘린더
- 연속 로그인 보너스 표시
- 특별 이벤트 보상

### Vocabulary (어휘)

**경로:** `/vocabulary`  
**파일:** `client/src/pages/Vocabulary.tsx`

**구성 요소:**
- 카테고리 목록 (이모지, 이름, 단어 수)
- 진행 상황 표시
- 카테고리 클릭 시 단어 학습 페이지로 이동

### Profile (프로필)

**경로:** `/profile`  
**파일:** `client/src/pages/Profile.tsx`

**구성 요소:**
- 사용자 정보 (아바타, 닉네임, 레벨, XP)
- 로그아웃 버튼 (우측 상단)
- 주간 학습량 그래프
- 학습 통계 (완료 미션, 학습 시간, 어휘 수, 발음 정확도)
- 획득 배지

**특징:**
- 실시간 데이터 동기화 (useAuth 훅)
- 프로그레스 바로 XP 시각화

---

## 애니메이션 및 인터랙션

밤토리는 마이크로 인터랙션을 통해 사용자 경험을 향상시킵니다.

### 페이드 인 애니메이션

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}
```

### 슬라이드 인 애니메이션

```css
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-in {
  animation: slideIn 0.4s ease-out;
}
```

### 펄스 애니메이션 (하트)

```css
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.duo-heart {
  animation: pulse 1s ease-in-out infinite;
}
```

### 호버 효과

모든 클릭 가능한 요소는 호버 시 시각적 피드백을 제공합니다.

```css
.duo-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.duo-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```

### 풀투리프레시

홈 화면은 아래로 당겨서 새로고침 기능을 지원합니다.

**구현:** `client/src/hooks/usePullToRefresh.ts`

**사용 예시:**
```tsx
const { containerRef, isPulling, isRefreshing, pullDistance } = usePullToRefresh({
  onRefresh: handleRefresh,
  threshold: 80,
});

<div ref={containerRef} className="overflow-y-auto">
  {/* 콘텐츠 */}
</div>
```

---

## 반응형 디자인

밤토리는 모바일 우선 디자인을 채택하며, 다양한 화면 크기에 대응합니다.

### 브레이크포인트

| 이름 | 최소 너비 | Tailwind 클래스 | 용도 |
|------|-----------|-----------------|------|
| Mobile | 0px | (기본) | 모바일 (320px~) |
| Tablet | 640px | `sm:` | 태블릿 |
| Desktop | 1024px | `lg:` | 데스크톱 |

### 반응형 패턴

**그리드 레이아웃:**
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* 카드 */}
</div>
```

**플렉스 레이아웃:**
```tsx
<div className="flex flex-col sm:flex-row gap-3">
  {/* 버튼 */}
</div>
```

**텍스트 크기:**
```tsx
<h1 className="text-xl sm:text-2xl lg:text-3xl">제목</h1>
```

---

## 접근성

밤토리는 WCAG 2.1 AA 수준의 접근성을 목표로 합니다.

### 색상 대비

모든 텍스트는 배경과 최소 4.5:1의 대비율을 유지합니다.

### 키보드 네비게이션

모든 인터랙티브 요소는 키보드로 접근 가능하며, 포커스 링이 명확하게 표시됩니다.

```css
*:focus-visible {
  outline: 2px solid var(--duo-blue);
  outline-offset: 2px;
}
```

### 스크린 리더

모든 다이얼로그는 `DialogTitle`과 `DialogDescription`을 포함하며, 필요시 `sr-only` 클래스로 시각적으로 숨깁니다.

```tsx
<DialogTitle className="sr-only">일일 로그인 보너스</DialogTitle>
<DialogDescription className="sr-only">
  오늘의 로그인 보너스를 획득했습니다
</DialogDescription>
```

### ARIA 속성

인터랙티브 요소는 적절한 ARIA 속성을 사용합니다.

```tsx
<button aria-label="로그아웃" onClick={logout}>
  <LogOut size={20} />
</button>
```

---

## 스타일링 가이드라인

밤토리는 Tailwind CSS를 사용하며, 다음 가이드라인을 따릅니다.

### 유틸리티 클래스 우선

커스텀 CSS보다 Tailwind 유틸리티 클래스를 우선 사용합니다.

```tsx
// ✅ 좋은 예
<div className="flex items-center gap-2 p-4 bg-white rounded-xl shadow-sm">

// ❌ 나쁜 예
<div className="custom-card">
```

### 재사용 가능한 스타일

반복되는 스타일은 `client/src/index.css`에 정의합니다.

```css
.duo-card {
  @apply bg-white rounded-xl shadow-sm p-4 transition-all duration-200;
}

.duo-card:hover {
  @apply shadow-md -translate-y-0.5;
}
```

### 색상 변수 사용

하드코딩된 색상 대신 CSS 변수를 사용합니다.

```tsx
// ✅ 좋은 예
<div style={{ background: 'var(--duo-green)' }}>

// ❌ 나쁜 예
<div style={{ background: '#58CC02' }}>
```

---

## 성능 최적화

밤토리는 다음 기법을 사용하여 성능을 최적화합니다.

### 이미지 최적화

이미지는 WebP 형식으로 제공하며, 적절한 크기로 리사이즈합니다.

### 코드 스플리팅

페이지별로 코드를 분할하여 초기 로딩 시간을 단축합니다.

```tsx
const Profile = lazy(() => import('./pages/Profile'));
```

### 메모이제이션

비용이 큰 계산은 `useMemo`로 메모이제이션합니다.

```tsx
const xpToNextLevel = useMemo(() => {
  return (user.level + 1) * 100 - user.xp;
}, [user.level, user.xp]);
```

### 옵티미스틱 업데이트

사용자 액션에 즉각적인 피드백을 제공하기 위해 옵티미스틱 업데이트를 사용합니다.

```tsx
const claimBonus = trpc.dailyBonus.claim.useMutation({
  onMutate: () => {
    // 즉시 UI 업데이트
    setShowBonus(true);
  },
  onError: () => {
    // 오류 시 롤백
    setShowBonus(false);
  }
});
```

---

이 문서는 밤토리의 UI/UX 디자인 원칙과 컴포넌트 구조를 상세히 설명합니다. 다음 문서에서는 기능 구현 가이드와 체크리스트를 제공합니다.
