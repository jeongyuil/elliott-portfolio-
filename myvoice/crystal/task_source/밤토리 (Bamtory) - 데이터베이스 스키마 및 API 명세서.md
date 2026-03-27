# 밤토리 (Bamtory) - 데이터베이스 스키마 및 API 명세서

**작성일:** 2026년 2월 13일  
**작성자:** Manus AI  
**버전:** 1.0

---

## 데이터베이스 스키마

밤토리는 MySQL/TiDB 데이터베이스를 사용하며, Drizzle ORM을 통해 타입 안전한 데이터베이스 접근을 구현합니다. 다음은 전체 데이터베이스 스키마입니다.

### users 테이블

사용자 기본 정보와 게임 통계를 저장하는 핵심 테이블입니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 사용자 고유 ID |
| openId | VARCHAR(64) | NOT NULL, UNIQUE | - | Manus OAuth 식별자 |
| name | TEXT | - | - | 사용자 이름 |
| email | VARCHAR(320) | - | - | 이메일 주소 |
| loginMethod | VARCHAR(64) | - | - | 로그인 방법 (google, apple 등) |
| role | ENUM('user', 'admin') | NOT NULL | 'user' | 사용자 권한 |
| nickname | VARCHAR(100) | - | - | 닉네임 |
| avatar | VARCHAR(10) | - | '🐰' | 아바타 이모지 |
| stars | INT | NOT NULL | 120 | 보유 별 개수 |
| hearts | INT | NOT NULL | 3 | 현재 하트 개수 |
| maxHearts | INT | NOT NULL | 3 | 최대 하트 개수 |
| streak | INT | NOT NULL | 7 | 연속 로그인 일수 |
| level | INT | NOT NULL | 5 | 사용자 레벨 |
| xp | INT | NOT NULL | 1220 | 경험치 |
| lastLoginBonusDate | TIMESTAMP | - | - | 마지막 로그인 보너스 청구 날짜 |
| consecutiveLoginDays | INT | NOT NULL | 0 | 연속 로그인 일수 (보너스용) |
| onboardingCompleted | BOOLEAN | NOT NULL | false | 온보딩 완료 여부 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 (자동 업데이트) |
| lastSignedIn | TIMESTAMP | NOT NULL | NOW() | 마지막 로그인 시각 |

### weeklyGoals 테이블

사용자의 주간 학습 목표와 진행 상황을 추적합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 주간 목표 고유 ID |
| userId | INT | NOT NULL | - | 사용자 ID (외래키) |
| xpTarget | INT | NOT NULL | 1500 | XP 목표 |
| xpCurrent | INT | NOT NULL | 1220 | 현재 XP |
| missionsTarget | INT | NOT NULL | 25 | 미션 완료 목표 |
| missionsCurrent | INT | NOT NULL | 21 | 현재 완료 미션 수 |
| studyTimeTarget | FLOAT | NOT NULL | 15 | 학습 시간 목표 (시간) |
| studyTimeCurrent | FLOAT | NOT NULL | 12.5 | 현재 학습 시간 (시간) |
| wordsTarget | INT | NOT NULL | 200 | 단어 학습 목표 |
| wordsCurrent | INT | NOT NULL | 152 | 현재 학습 단어 수 |
| weekStartDate | TIMESTAMP | NOT NULL | - | 주 시작 날짜 |
| weekEndDate | TIMESTAMP | NOT NULL | - | 주 종료 날짜 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

### missions 테이블

사용 가능한 미션 목록을 저장합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 미션 고유 ID |
| title | VARCHAR(255) | NOT NULL | - | 미션 제목 |
| emoji | VARCHAR(10) | NOT NULL | - | 미션 이모지 |
| duration | INT | NOT NULL | - | 소요 시간 (분) |
| stars | INT | NOT NULL | - | 보상 별 개수 |
| difficulty | ENUM('beginner', 'intermediate', 'advanced') | NOT NULL | - | 난이도 |
| category | VARCHAR(100) | NOT NULL | - | 카테고리 |
| status | ENUM('completed', 'in_progress', 'locked') | NOT NULL | 'locked' | 상태 |
| scenarioCharacter | VARCHAR(255) | - | - | 시나리오 캐릭터 |
| scenarioSituation | TEXT | - | - | 시나리오 상황 |
| scenarioTargetWord | VARCHAR(100) | - | - | 목표 단어 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

### userMissions 테이블

사용자별 미션 진행 상황을 추적합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 고유 ID |
| userId | INT | NOT NULL | - | 사용자 ID |
| missionId | INT | NOT NULL | - | 미션 ID |
| status | ENUM('completed', 'in_progress', 'locked') | NOT NULL | 'locked' | 상태 |
| score | INT | - | - | 발음 정확도 점수 |
| completedAt | TIMESTAMP | - | - | 완료 시각 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

### vocabularyCategories 테이블

어휘 카테고리 목록을 저장합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 카테고리 고유 ID |
| name | VARCHAR(100) | NOT NULL | - | 카테고리 이름 |
| emoji | VARCHAR(10) | NOT NULL | - | 카테고리 이모지 |
| wordCount | INT | NOT NULL | - | 단어 개수 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

### vocabularyWords 테이블

어휘 단어 목록을 저장합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 단어 고유 ID |
| categoryId | INT | NOT NULL | - | 카테고리 ID |
| word | VARCHAR(100) | NOT NULL | - | 영어 단어 |
| translation | VARCHAR(100) | NOT NULL | - | 한국어 번역 |
| emoji | VARCHAR(10) | NOT NULL | - | 단어 이모지 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

### userVocabulary 테이블

사용자별 어휘 학습 진행 상황을 추적합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 고유 ID |
| userId | INT | NOT NULL | - | 사용자 ID |
| wordId | INT | NOT NULL | - | 단어 ID |
| learned | BOOLEAN | NOT NULL | false | 학습 완료 여부 |
| accuracy | INT | - | - | 발음 정확도 (%) |
| attempts | INT | NOT NULL | 0 | 시도 횟수 |
| lastPracticedAt | TIMESTAMP | - | - | 마지막 연습 시각 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

### skills 테이블

사용자의 스킬 진행 상황을 추적합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 고유 ID |
| userId | INT | NOT NULL | - | 사용자 ID |
| skillId | VARCHAR(100) | NOT NULL | - | 스킬 ID (예: "daily_vocab") |
| category | ENUM('language', 'cognitive', 'emotional') | NOT NULL | - | 카테고리 |
| score | INT | NOT NULL | 0 | 점수 |
| level | INT | NOT NULL | 1 | 레벨 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

### badges 테이블

사용자가 획득한 배지를 저장합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 고유 ID |
| userId | INT | NOT NULL | - | 사용자 ID |
| badgeId | VARCHAR(100) | NOT NULL | - | 배지 ID (예: "first_mission") |
| name | VARCHAR(255) | NOT NULL | - | 배지 이름 |
| description | TEXT | - | - | 배지 설명 |
| emoji | VARCHAR(10) | NOT NULL | - | 배지 이모지 |
| earnedAt | TIMESTAMP | NOT NULL | NOW() | 획득 시각 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |

### shopItems 테이블

상점 아이템 목록을 저장합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 아이템 고유 ID |
| name | VARCHAR(255) | NOT NULL | - | 아이템 이름 |
| emoji | VARCHAR(10) | NOT NULL | - | 아이템 이모지 |
| price | INT | NOT NULL | - | 가격 (별 개수) |
| category | VARCHAR(100) | NOT NULL | - | 카테고리 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

### userInventory 테이블

사용자의 인벤토리를 저장합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 고유 ID |
| userId | INT | NOT NULL | - | 사용자 ID |
| itemId | INT | NOT NULL | - | 아이템 ID |
| quantity | INT | NOT NULL | 1 | 수량 |
| purchasedAt | TIMESTAMP | NOT NULL | NOW() | 구매 시각 |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

### learningHistory 테이블

일일 학습 활동을 추적합니다.

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | - | 고유 ID |
| userId | INT | NOT NULL | - | 사용자 ID |
| date | TIMESTAMP | NOT NULL | - | 날짜 |
| xpEarned | INT | NOT NULL | 0 | 획득 XP |
| missionsCompleted | INT | NOT NULL | 0 | 완료 미션 수 |
| wordsLearned | INT | NOT NULL | 0 | 학습 단어 수 |
| studyTimeMinutes | INT | NOT NULL | 0 | 학습 시간 (분) |
| createdAt | TIMESTAMP | NOT NULL | NOW() | 생성 시각 |
| updatedAt | TIMESTAMP | NOT NULL | NOW() | 수정 시각 |

---

## API 명세서

밤토리는 tRPC를 사용하여 타입 안전한 API를 제공합니다. 모든 API는 `/api/trpc` 경로를 통해 접근하며, 클라이언트는 `trpc` 객체를 통해 호출합니다.

### 인증 API (auth)

#### auth.me

현재 로그인한 사용자 정보를 반환합니다.

**타입:** Query  
**인증:** Public  
**입력:** 없음  
**출력:** `User | null`

**사용 예시:**
```typescript
const { data: user } = trpc.auth.me.useQuery();
```

#### auth.logout

현재 사용자를 로그아웃합니다.

**타입:** Mutation  
**인증:** Public  
**입력:** 없음  
**출력:** `{ success: true }`

**사용 예시:**
```typescript
const logout = trpc.auth.logout.useMutation();
await logout.mutateAsync();
```

### 주간 목표 API (weeklyGoals)

#### weeklyGoals.getCurrent

현재 주간 목표를 조회합니다. 목표가 없으면 자동으로 생성합니다.

**타입:** Query  
**인증:** Protected  
**입력:** 없음  
**출력:** `WeeklyGoal`

**사용 예시:**
```typescript
const { data: goals } = trpc.weeklyGoals.getCurrent.useQuery();
```

#### weeklyGoals.updateProgress

주간 목표 진행 상황을 업데이트합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:**
```typescript
{
  xpCurrent?: number;
  missionsCurrent?: number;
  studyTimeCurrent?: number;
  wordsCurrent?: number;
}
```
**출력:** `{ success: true }`

**사용 예시:**
```typescript
const updateProgress = trpc.weeklyGoals.updateProgress.useMutation();
await updateProgress.mutateAsync({ xpCurrent: 1300 });
```

#### weeklyGoals.updateTargets

주간 목표 타겟을 업데이트합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:**
```typescript
{
  xpTarget?: number;
  missionsTarget?: number;
  studyTimeTarget?: number;
  wordsTarget?: number;
}
```
**출력:** `{ success: true }`

### 미션 API (missions)

#### missions.getAll

모든 미션 목록을 조회합니다.

**타입:** Query  
**인증:** Public  
**입력:** 없음  
**출력:** `Mission[]`

#### missions.getUserMissions

사용자의 미션 진행 상황을 조회합니다.

**타입:** Query  
**인증:** Protected  
**입력:** 없음  
**출력:** `UserMission[]`

#### missions.updateStatus

미션 상태를 업데이트합니다. 완료 시 주간 목표도 자동 업데이트됩니다.

**타입:** Mutation  
**인증:** Protected  
**입력:**
```typescript
{
  missionId: number;
  status: "completed" | "in_progress" | "locked";
  score?: number;
  earnedXp?: number;
}
```
**출력:** `{ success: true }`

**사용 예시:**
```typescript
const updateStatus = trpc.missions.updateStatus.useMutation();
await updateStatus.mutateAsync({
  missionId: 1,
  status: "completed",
  score: 95,
  earnedXp: 50
});
```

### 어휘 API (vocabulary)

#### vocabulary.getCategories

모든 어휘 카테고리를 조회합니다.

**타입:** Query  
**인증:** Public  
**입력:** 없음  
**출력:** `VocabularyCategory[]`

#### vocabulary.getWordsByCategory

특정 카테고리의 단어 목록을 조회합니다.

**타입:** Query  
**인증:** Public  
**입력:** `{ categoryId: number }`  
**출력:** `VocabularyWord[]`

#### vocabulary.getUserProgress

사용자의 어휘 학습 진행 상황을 조회합니다.

**타입:** Query  
**인증:** Protected  
**입력:** 없음  
**출력:** `UserVocabulary[]`

#### vocabulary.updateProgress

어휘 학습 진행 상황을 업데이트합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:**
```typescript
{
  wordId: number;
  learned?: boolean;
  accuracy?: number;
  attempts?: number;
}
```
**출력:** `{ success: true }`

#### vocabulary.completeCategory

카테고리 학습을 완료하고 보상을 지급합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:**
```typescript
{
  categoryId: number;
  wordsLearned: number;
  earnedStars: number;
  earnedXp: number;
}
```
**출력:** `{ success: true }`

### 일일 로그인 보너스 API (dailyBonus)

#### dailyBonus.claim

일일 로그인 보너스를 청구합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:** 없음  
**출력:**
```typescript
{
  success: true;
  reward: {
    stars: number;
    hearts: number;
    consecutiveDays: number;
  };
}
```

**사용 예시:**
```typescript
const claimBonus = trpc.dailyBonus.claim.useMutation();
const result = await claimBonus.mutateAsync();
console.log(`${result.reward.stars}별, ${result.reward.hearts}하트 획득!`);
```

### 사용자 API (user)

#### user.getStats

사용자 통계를 조회합니다.

**타입:** Query  
**인증:** Protected  
**입력:** 없음  
**출력:** `User`

#### user.updateStats

사용자 통계를 업데이트합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:**
```typescript
{
  stars?: number;
  hearts?: number;
  streak?: number;
  level?: number;
  xp?: number;
}
```
**출력:** `{ success: true }`

#### user.completeOnboarding

온보딩을 완료합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:** 없음  
**출력:** `{ success: true }`

### 스킬 API (skills)

#### skills.getUserSkills

사용자의 스킬 목록을 조회합니다.

**타입:** Query  
**인증:** Protected  
**입력:** 없음  
**출력:** `Skill[]`

#### skills.updateSkill

스킬 정보를 업데이트합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:**
```typescript
{
  skillId: string;
  score?: number;
  level?: number;
}
```
**출력:** `{ success: true }`

### 배지 API (badges)

#### badges.getUserBadges

사용자가 획득한 배지 목록을 조회합니다.

**타입:** Query  
**인증:** Protected  
**입력:** 없음  
**출력:** `Badge[]`

### 상점 API (shop)

#### shop.getItems

상점 아이템 목록을 조회합니다.

**타입:** Query  
**인증:** Public  
**입력:** 없음  
**출력:** `ShopItem[]`

#### shop.getUserInventory

사용자의 인벤토리를 조회합니다.

**타입:** Query  
**인증:** Protected  
**입력:** 없음  
**출력:** `UserInventoryItem[]`

#### shop.purchaseItem

아이템을 구매합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:** `{ itemId: number }`  
**출력:** `{ success: true }`

### 학습 기록 API (learningHistory)

#### learningHistory.getHistory

특정 기간의 학습 기록을 조회합니다.

**타입:** Query  
**인증:** Protected  
**입력:**
```typescript
{
  startDate: Date;
  endDate: Date;
}
```
**출력:** `LearningHistory[]`

#### learningHistory.updateHistory

학습 기록을 업데이트합니다.

**타입:** Mutation  
**인증:** Protected  
**입력:**
```typescript
{
  date: Date;
  xpEarned?: number;
  missionsCompleted?: number;
  wordsLearned?: number;
  studyTimeMinutes?: number;
}
```
**출력:** `{ success: true }`

---

## 데이터베이스 마이그레이션

밤토리는 Drizzle Kit을 사용하여 데이터베이스 마이그레이션을 관리합니다.

### 마이그레이션 생성 및 적용

```bash
# 스키마 변경 후 마이그레이션 생성 및 적용
pnpm db:push
```

이 명령은 `drizzle-kit generate`와 `drizzle-kit migrate`를 순차적으로 실행하여 스키마 변경사항을 데이터베이스에 반영합니다.

### 마이그레이션 파일 위치

생성된 마이그레이션 파일은 `drizzle/migrations/` 디렉토리에 저장됩니다.

---

## 에러 처리

tRPC는 타입 안전한 에러 처리를 제공합니다. 모든 API 호출은 다음과 같이 에러를 처리할 수 있습니다.

```typescript
const claimBonus = trpc.dailyBonus.claim.useMutation({
  onError: (error) => {
    if (error.message === "Already claimed today") {
      toast.error("오늘 이미 보너스를 받았습니다!");
    } else {
      toast.error("오류가 발생했습니다. 다시 시도해주세요.");
    }
  },
  onSuccess: (data) => {
    toast.success(`${data.reward.stars}별과 ${data.reward.hearts}하트를 획득했습니다!`);
  }
});
```

---

이 문서는 밤토리의 데이터베이스 스키마와 API 명세를 상세히 설명합니다. 다음 문서에서는 UI/UX 가이드와 컴포넌트 구조를 다룹니다.
