# 밤토리 (Bamtory) - 기능 구현 가이드 및 체크리스트

**작성일:** 2026년 2월 13일  
**작성자:** Manus AI  
**버전:** 1.0

---

## 구현 순서

밤토리를 처음부터 재구축할 때는 다음 순서로 진행하는 것을 권장합니다. 각 단계는 이전 단계에 의존하므로, 순서대로 완료해야 합니다.

### 1단계: 프로젝트 초기화 (1일차)

프로젝트의 기반을 설정하는 단계입니다.

**작업 목록:**
- [ ] Node.js 22.13.0 및 pnpm 설치 확인
- [ ] 프로젝트 디렉토리 생성 (`bamtory/`)
- [ ] `package.json` 생성 및 의존성 설치
- [ ] Vite 설정 (`vite.config.ts`)
- [ ] TypeScript 설정 (`tsconfig.json`)
- [ ] Tailwind CSS 설정 (`tailwind.config.ts`, `postcss.config.js`)
- [ ] ESLint 및 Prettier 설정
- [ ] Git 저장소 초기화 및 `.gitignore` 설정

**핵심 파일:**
```
bamtory/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
├── .eslintrc.json
├── .prettierrc
└── .gitignore
```

**검증 방법:**
```bash
pnpm install
pnpm dev
```

브라우저에서 `http://localhost:3000`에 접속하여 기본 페이지가 표시되는지 확인합니다.

### 2단계: 데이터베이스 및 인증 설정 (2일차)

데이터베이스 스키마와 인증 시스템을 구축합니다.

**작업 목록:**
- [ ] Drizzle ORM 설정 (`drizzle.config.ts`)
- [ ] 데이터베이스 스키마 정의 (`drizzle/schema.ts`)
- [ ] 환경 변수 설정 (`.env`)
- [ ] Manus OAuth 설정 (`server/_core/oauth.ts`)
- [ ] tRPC 서버 설정 (`server/_core/trpc.ts`, `server/_core/context.ts`)
- [ ] 데이터베이스 마이그레이션 실행 (`pnpm db:push`)

**핵심 파일:**
```
bamtory/
├── drizzle/
│   └── schema.ts
├── server/
│   └── _core/
│       ├── oauth.ts
│       ├── trpc.ts
│       └── context.ts
└── drizzle.config.ts
```

**검증 방법:**
```bash
pnpm db:push
```

데이터베이스에 모든 테이블이 생성되었는지 확인합니다.

### 3단계: 기본 UI 구조 (3일차)

레이아웃과 네비게이션을 구축합니다.

**작업 목록:**
- [ ] shadcn/ui 설치 및 설정
- [ ] 기본 컴포넌트 설치 (Button, Card, Dialog 등)
- [ ] 전역 스타일 설정 (`client/src/index.css`)
- [ ] 라우팅 설정 (`client/src/App.tsx`)
- [ ] 하단 네비게이션 구현 (`client/src/components/layout/BottomNav.tsx`)
- [ ] 기본 페이지 생성 (Home, Missions, Rewards, Vocabulary, Profile)

**핵심 파일:**
```
client/
├── src/
│   ├── components/
│   │   ├── ui/           # shadcn/ui 컴포넌트
│   │   └── layout/
│   │       └── BottomNav.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Missions.tsx
│   │   ├── Rewards.tsx
│   │   ├── Vocabulary.tsx
│   │   └── Profile.tsx
│   ├── App.tsx
│   └── index.css
```

**검증 방법:**

브라우저에서 하단 네비게이션을 클릭하여 각 페이지로 이동할 수 있는지 확인합니다.

### 4단계: 인증 및 온보딩 (4일차)

로그인, 로그아웃, 온보딩 튜토리얼을 구현합니다.

**작업 목록:**
- [ ] `useAuth` 훅 구현 (`client/src/_core/hooks/useAuth.ts`)
- [ ] `getLoginUrl` 함수 구현 (`client/src/const.ts`)
- [ ] `ProtectedRoute` 컴포넌트 구현
- [ ] 로그인 페이지 구현
- [ ] 로그아웃 기능 구현
- [ ] 온보딩 튜토리얼 컴포넌트 구현 (`OnboardingTutorial.tsx`)
- [ ] 온보딩 완료 API 구현 (`user.completeOnboarding`)

**핵심 파일:**
```
client/src/
├── _core/hooks/
│   └── useAuth.ts
├── components/
│   ├── ProtectedRoute.tsx
│   └── OnboardingTutorial.tsx
└── const.ts

server/
└── routers.ts (user.completeOnboarding)
```

**검증 방법:**

비로그인 상태에서 페이지 접근 시 로그인 페이지로 리다이렉트되는지 확인합니다. 첫 로그인 시 온보딩 튜토리얼이 표시되는지 확인합니다.

### 5단계: 일일 로그인 보너스 (5일차)

일일 로그인 보너스 시스템을 구현합니다.

**작업 목록:**
- [ ] 데이터베이스 스키마에 `lastLoginBonusDate`, `consecutiveLoginDays` 추가
- [ ] 일일 보너스 API 구현 (`server/trpc/routers/dailyBonus.ts`)
- [ ] 일일 보너스 모달 컴포넌트 구현 (`DailyBonusModal.tsx`)
- [ ] 홈 화면에 보너스 청구 로직 추가
- [ ] 테스트 작성 (`server/dailyBonus.test.ts`)

**핵심 파일:**
```
server/
├── trpc/routers/
│   └── dailyBonus.ts
└── dailyBonus.test.ts

client/src/components/
└── DailyBonusModal.tsx
```

**검증 방법:**

매일 첫 로그인 시 보너스 모달이 표시되는지 확인합니다. 하루에 한 번만 청구 가능한지 확인합니다.

### 6단계: 주간 목표 시스템 (6일차)

주간 학습 목표 추적 시스템을 구현합니다.

**작업 목록:**
- [ ] `weeklyGoals` 테이블 스키마 정의
- [ ] 주간 목표 API 구현 (`weeklyGoals.getCurrent`, `updateProgress`, `updateTargets`)
- [ ] 주간 목표 UI 구현 (홈 화면)
- [ ] 프로그레스 바 컴포넌트 구현
- [ ] 자동 목표 생성 로직 구현

**핵심 파일:**
```
server/
├── db.ts (주간 목표 헬퍼 함수)
└── routers.ts (weeklyGoals 라우터)

client/src/pages/
└── Home.tsx (주간 목표 UI)
```

**검증 방법:**

홈 화면에서 주간 목표가 표시되고, 미션 완료 시 자동으로 업데이트되는지 확인합니다.

### 7단계: 미션 시스템 (7-8일차)

미션 목록, 상세, 완료 기능을 구현합니다.

**작업 목록:**
- [ ] `missions`, `userMissions` 테이블 스키마 정의
- [ ] 미션 API 구현 (`missions.getAll`, `getUserMissions`, `updateStatus`)
- [ ] 미션 카드 컴포넌트 구현 (`MissionCard.tsx`)
- [ ] 미션 목록 페이지 구현 (`Missions.tsx`)
- [ ] 미션 상세 페이지 구현 (`MissionDetail.tsx`)
- [ ] 미션 완료 로직 구현 (XP, 별 보상)

**핵심 파일:**
```
server/
├── db.ts (미션 헬퍼 함수)
└── routers.ts (missions 라우터)

client/src/
├── components/mission/
│   └── MissionCard.tsx
└── pages/
    ├── Missions.tsx
    └── MissionDetail.tsx
```

**검증 방법:**

미션 목록이 표시되고, 미션을 클릭하여 상세 페이지로 이동할 수 있는지 확인합니다. 미션 완료 시 별과 XP가 증가하는지 확인합니다.

### 8단계: 어휘 학습 시스템 (9-10일차)

어휘 카테고리와 학습 기능을 구현합니다.

**작업 목록:**
- [ ] `vocabularyCategories`, `vocabularyWords`, `userVocabulary` 테이블 스키마 정의
- [ ] 어휘 API 구현 (`vocabulary.*`)
- [ ] 어휘 카테고리 목록 페이지 구현 (`Vocabulary.tsx`)
- [ ] 어휘 학습 페이지 구현 (`VocabularyLearn.tsx`)
- [ ] 발음 연습 기능 구현 (Web Speech API)
- [ ] 진행 상황 추적 및 업데이트

**핵심 파일:**
```
server/
├── db.ts (어휘 헬퍼 함수)
└── routers.ts (vocabulary 라우터)

client/src/pages/
├── Vocabulary.tsx
└── VocabularyLearn.tsx
```

**검증 방법:**

어휘 카테고리를 선택하여 단어 학습 페이지로 이동할 수 있는지 확인합니다. 발음 연습 후 정확도가 기록되는지 확인합니다.

### 9단계: 프로필 및 통계 (11일차)

사용자 프로필과 학습 통계를 구현합니다.

**작업 목록:**
- [ ] `learningHistory` 테이블 스키마 정의
- [ ] 학습 기록 API 구현 (`learningHistory.*`)
- [ ] 프로필 페이지 UI 구현 (`Profile.tsx`)
- [ ] 주간 학습량 그래프 구현 (Chart.js 또는 Recharts)
- [ ] 학습 통계 표시 (완료 미션, 학습 시간, 어휘 수, 발음 정확도)
- [ ] 배지 시스템 구현

**핵심 파일:**
```
server/
├── db.ts (학습 기록 헬퍼 함수)
└── routers.ts (learningHistory 라우터)

client/src/pages/
└── Profile.tsx
```

**검증 방법:**

프로필 페이지에서 사용자 정보와 학습 통계가 정확하게 표시되는지 확인합니다.

### 10단계: 상점 시스템 (12일차)

별을 사용하여 아이템을 구매하는 상점을 구현합니다.

**작업 목록:**
- [ ] `shopItems`, `userInventory` 테이블 스키마 정의
- [ ] 상점 API 구현 (`shop.*`)
- [ ] 상점 페이지 구현 (`Shop.tsx`)
- [ ] 아이템 구매 로직 구현
- [ ] 인벤토리 표시

**핵심 파일:**
```
server/
├── db.ts (상점 헬퍼 함수)
└── routers.ts (shop 라우터)

client/src/pages/
└── Shop.tsx
```

**검증 방법:**

상점에서 아이템을 구매할 수 있고, 별이 차감되는지 확인합니다.

### 11단계: 테스트 및 최적화 (13-14일차)

전체 시스템을 테스트하고 최적화합니다.

**작업 목록:**
- [ ] 모든 API 엔드포인트에 대한 테스트 작성
- [ ] 주요 컴포넌트에 대한 단위 테스트 작성
- [ ] E2E 테스트 작성 (Playwright)
- [ ] 성능 최적화 (코드 스플리팅, 이미지 최적화)
- [ ] 접근성 검사 (WAVE, axe DevTools)
- [ ] 크로스 브라우저 테스트

**검증 방법:**

모든 테스트가 통과하는지 확인합니다.

```bash
pnpm test
```

---

## 핵심 기능 구현 가이드

각 핵심 기능의 상세 구현 방법을 설명합니다.

### 일일 로그인 보너스

일일 로그인 보너스는 사용자의 참여를 유도하는 핵심 기능입니다.

**데이터베이스 스키마:**

`users` 테이블에 다음 필드를 추가합니다.

```typescript
lastLoginBonusDate: timestamp("lastLoginBonusDate"),
consecutiveLoginDays: int("consecutiveLoginDays").default(0).notNull(),
```

**API 구현:**

`server/trpc/routers/dailyBonus.ts` 파일을 생성하고 다음 로직을 구현합니다.

```typescript
export const dailyBonusRouter = router({
  claim: protectedProcedure.mutation(async ({ ctx }) => {
    const user = ctx.user;
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    
    // 이미 오늘 청구했는지 확인
    if (user.lastLoginBonusDate) {
      const lastClaim = new Date(user.lastLoginBonusDate);
      const lastClaimDate = new Date(
        lastClaim.getFullYear(),
        lastClaim.getMonth(),
        lastClaim.getDate()
      );
      
      if (lastClaimDate.getTime() === today.getTime()) {
        throw new TRPCError({
          code: "BAD_REQUEST",
          message: "Already claimed today",
        });
      }
    }
    
    // 연속 로그인 일수 계산
    let consecutiveDays = 1;
    if (user.lastLoginBonusDate) {
      const lastClaim = new Date(user.lastLoginBonusDate);
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      
      const lastClaimDate = new Date(
        lastClaim.getFullYear(),
        lastClaim.getMonth(),
        lastClaim.getDate()
      );
      
      if (lastClaimDate.getTime() === yesterday.getTime()) {
        consecutiveDays = user.consecutiveLoginDays + 1;
      }
    }
    
    // 보상 계산 (연속 일수에 따라 증가)
    const stars = consecutiveDays >= 7 ? 20 : consecutiveDays * 5;
    const hearts = consecutiveDays >= 7 ? 3 : Math.floor(consecutiveDays / 2) + 1;
    
    // 사용자 데이터 업데이트
    await db.updateUserStats(user.id, {
      stars: user.stars + stars,
      hearts: Math.min(user.hearts + hearts, user.maxHearts),
      lastLoginBonusDate: now,
      consecutiveLoginDays: consecutiveDays,
    });
    
    return {
      success: true,
      reward: { stars, hearts, consecutiveDays },
    };
  }),
});
```

**UI 구현:**

`client/src/components/DailyBonusModal.tsx` 파일을 생성하고 모달을 구현합니다.

```typescript
export function DailyBonusModal({ isOpen, onClose, reward }: Props) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-sm">
        <DialogTitle className="sr-only">일일 로그인 보너스</DialogTitle>
        <DialogDescription className="sr-only">
          오늘의 로그인 보너스를 획득했습니다
        </DialogDescription>
        
        <div className="text-center space-y-4 py-6">
          <div className="text-6xl animate-bounce">🎉</div>
          <h2 className="text-2xl font-bold">
            {reward.consecutiveDays}일 연속 로그인!
          </h2>
          <div className="space-y-2">
            <p className="text-lg">⭐ {reward.stars}별 획득!</p>
            <p className="text-lg">❤️ {reward.hearts}하트 획득!</p>
          </div>
          <Button onClick={onClose} className="w-full">
            확인
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

**홈 화면 통합:**

`client/src/pages/Home.tsx`에서 보너스를 자동으로 청구합니다.

```typescript
const claimBonus = trpc.dailyBonus.claim.useMutation({
  onSuccess: (data) => {
    setReward(data.reward);
    setShowBonus(true);
  },
  onError: (error) => {
    if (error.message !== "Already claimed today") {
      toast.error("보너스 청구 실패");
    }
  },
});

useEffect(() => {
  if (user && !showBonus) {
    claimBonus.mutate();
  }
}, [user]);
```

### 온보딩 튜토리얼

신규 사용자를 위한 5단계 튜토리얼을 구현합니다.

**데이터베이스 스키마:**

`users` 테이블에 다음 필드를 추가합니다.

```typescript
onboardingCompleted: boolean("onboardingCompleted").default(false).notNull(),
```

**API 구현:**

`server/routers.ts`에 온보딩 완료 API를 추가합니다.

```typescript
user: router({
  completeOnboarding: protectedProcedure.mutation(async ({ ctx }) => {
    await db.updateUserStats(ctx.user.id, { onboardingCompleted: true });
    return { success: true };
  }),
}),
```

**UI 구현:**

`client/src/components/OnboardingTutorial.tsx` 파일을 생성합니다.

```typescript
const steps = [
  {
    icon: "🚀",
    title: "밤토리에 오신 것을 환영합니다!",
    description: "Luna와 함께 영어를 재미있게 배워보세요.",
  },
  {
    icon: "🎯",
    title: "미션을 완료하세요",
    description: "다양한 미션을 통해 영어 실력을 향상시키세요.",
  },
  // ... 나머지 단계
];

export function OnboardingTutorial({ isOpen, onComplete }: Props) {
  const [currentStep, setCurrentStep] = useState(0);
  const completeOnboarding = trpc.user.completeOnboarding.useMutation({
    onSuccess: onComplete,
  });
  
  const handleComplete = () => {
    completeOnboarding.mutate();
  };
  
  return (
    <Dialog open={isOpen}>
      <DialogContent>
        {/* 단계별 콘텐츠 */}
        <div className="text-center space-y-4">
          <div className="text-6xl">{steps[currentStep].icon}</div>
          <h2 className="text-2xl font-bold">{steps[currentStep].title}</h2>
          <p>{steps[currentStep].description}</p>
        </div>
        
        {/* 네비게이션 버튼 */}
        <div className="flex justify-between mt-6">
          <Button
            variant="outline"
            onClick={() => setCurrentStep(s => s - 1)}
            disabled={currentStep === 0}
          >
            이전
          </Button>
          <Button
            onClick={() => {
              if (currentStep === steps.length - 1) {
                handleComplete();
              } else {
                setCurrentStep(s => s + 1);
              }
            }}
          >
            {currentStep === steps.length - 1 ? "시작하기" : "다음"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

### 주간 목표 자동 생성

주간 목표가 없으면 자동으로 생성하는 로직을 구현합니다.

**API 구현:**

`server/routers.ts`의 `weeklyGoals.getCurrent`에 자동 생성 로직을 추가합니다.

```typescript
weeklyGoals: router({
  getCurrent: protectedProcedure.query(async ({ ctx }) => {
    let goal = await db.getCurrentWeeklyGoal(ctx.user.id);
    
    // 목표가 없거나 만료되었으면 새로 생성
    if (!goal || new Date(goal.weekEndDate) < new Date()) {
      const now = new Date();
      const weekStart = new Date(now);
      weekStart.setDate(now.getDate() - now.getDay()); // 일요일
      weekStart.setHours(0, 0, 0, 0);
      
      const weekEnd = new Date(weekStart);
      weekEnd.setDate(weekStart.getDate() + 6); // 토요일
      weekEnd.setHours(23, 59, 59, 999);
      
      await db.createWeeklyGoal({
        userId: ctx.user.id,
        xpTarget: 1500,
        xpCurrent: 0,
        missionsTarget: 25,
        missionsCurrent: 0,
        studyTimeTarget: 15,
        studyTimeCurrent: 0,
        wordsTarget: 200,
        wordsCurrent: 0,
        weekStartDate: weekStart,
        weekEndDate: weekEnd,
      });
      
      goal = await db.getCurrentWeeklyGoal(ctx.user.id);
    }
    
    return goal;
  }),
}),
```

---

## 테스트 작성 가이드

모든 API 엔드포인트와 주요 컴포넌트에 대한 테스트를 작성합니다.

### API 테스트 예시

`server/dailyBonus.test.ts` 파일을 생성합니다.

```typescript
import { describe, it, expect, beforeEach } from "vitest";
import { appRouter } from "./routers";
import * as db from "./db";

describe("Daily Bonus", () => {
  let userId: number;
  
  beforeEach(async () => {
    // 테스트 사용자 생성
    userId = await db.createUser({
      openId: "test-user",
      name: "Test User",
    });
  });
  
  it("should claim daily bonus successfully", async () => {
    const caller = appRouter.createCaller({
      user: { id: userId },
    });
    
    const result = await caller.dailyBonus.claim();
    
    expect(result.success).toBe(true);
    expect(result.reward.stars).toBeGreaterThan(0);
    expect(result.reward.hearts).toBeGreaterThan(0);
  });
  
  it("should not allow claiming twice in one day", async () => {
    const caller = appRouter.createCaller({
      user: { id: userId },
    });
    
    await caller.dailyBonus.claim();
    
    await expect(caller.dailyBonus.claim()).rejects.toThrow(
      "Already claimed today"
    );
  });
  
  it("should increase consecutive days correctly", async () => {
    const caller = appRouter.createCaller({
      user: { id: userId },
    });
    
    // 첫 번째 청구
    const day1 = await caller.dailyBonus.claim();
    expect(day1.reward.consecutiveDays).toBe(1);
    
    // 하루 뒤 청구 (시뮬레이션)
    // ... 날짜 조작 로직
  });
});
```

---

## 배포 체크리스트

프로덕션 배포 전에 다음 항목을 확인합니다.

### 코드 품질

- [ ] 모든 TypeScript 오류 해결
- [ ] ESLint 경고 해결
- [ ] Prettier로 코드 포맷팅
- [ ] 사용하지 않는 코드 제거
- [ ] console.log 제거

### 테스트

- [ ] 모든 단위 테스트 통과
- [ ] 모든 통합 테스트 통과
- [ ] E2E 테스트 통과
- [ ] 크로스 브라우저 테스트 완료

### 성능

- [ ] Lighthouse 점수 90 이상
- [ ] 이미지 최적화 완료
- [ ] 코드 스플리팅 적용
- [ ] 번들 크기 최적화

### 보안

- [ ] 환경 변수 확인
- [ ] API 인증 확인
- [ ] XSS 방어 확인
- [ ] CSRF 방어 확인

### 접근성

- [ ] WCAG 2.1 AA 준수
- [ ] 스크린 리더 테스트
- [ ] 키보드 네비게이션 테스트
- [ ] 색상 대비 확인

### 데이터베이스

- [ ] 마이그레이션 스크립트 확인
- [ ] 백업 전략 수립
- [ ] 인덱스 최적화
- [ ] 쿼리 성능 확인

### 문서

- [ ] README.md 작성
- [ ] API 문서 작성
- [ ] 배포 가이드 작성
- [ ] 트러블슈팅 가이드 작성

---

## 문제 해결 가이드

개발 중 자주 발생하는 문제와 해결 방법입니다.

### TypeScript 오류

**문제:** `Property 'user' does not exist on type 'Context'`

**해결:** `server/_core/context.ts`에서 컨텍스트 타입을 올바르게 정의했는지 확인합니다.

### tRPC 오류

**문제:** `TRPCClientError: UNAUTHORIZED`

**해결:** 세션 쿠키가 올바르게 설정되었는지 확인합니다. `credentials: "include"`가 fetch 옵션에 포함되어 있는지 확인합니다.

### 데이터베이스 오류

**문제:** `Connection refused`

**해결:** `DATABASE_URL` 환경 변수가 올바르게 설정되었는지 확인합니다. 데이터베이스 서버가 실행 중인지 확인합니다.

### Vite 빌드 오류

**문제:** `Module not found`

**해결:** `vite.config.ts`의 alias 설정을 확인합니다. `tsconfig.json`의 paths 설정과 일치하는지 확인합니다.

---

## 다음 단계

밤토리의 기본 기능을 모두 구현한 후, 다음 기능을 추가로 고려할 수 있습니다.

**프리미엄 기능**은 유료 구독을 통해 무제한 하트, 광고 제거, 특별 미션 등을 제공할 수 있습니다.

**소셜 기능**은 친구 추가, 리더보드, 그룹 챌린지 등을 통해 경쟁과 협력을 유도할 수 있습니다.

**AI 튜터**는 GPT-4를 활용하여 개인화된 학습 피드백과 대화 연습을 제공할 수 있습니다.

**오프라인 모드**는 Service Worker를 사용하여 오프라인에서도 학습할 수 있도록 지원할 수 있습니다.

**다국어 지원**은 i18n을 사용하여 여러 언어로 서비스를 제공할 수 있습니다.

---

이 문서는 밤토리를 처음부터 재구축하는 데 필요한 모든 단계와 체크리스트를 제공합니다. 각 단계를 순서대로 완료하면 완전히 작동하는 영어 학습 앱을 구축할 수 있습니다.
