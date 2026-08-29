# Phase 3: Backend Extension + Frontend API Integration — 밤토리 (Bamtory) MVP

> **상태**: ✅ **완료** (2026-02 완료)
> 이 프롬프트는 Gemini에게 전달되어 실행 완료되었습니다.
> 결과: 백엔드 모델 12개, 라우터 17개, 서비스 13개 구현. 프론트엔드 API 훅 10개 생성, mockData → 실제 API 연동 전환.

## 프로젝트 개요

밤토리는 4-12세 아이를 위한 Voice AI 영어 학습 앱입니다.
- **백엔드**: FastAPI (Python 3.11) + SQLAlchemy (async) + PostgreSQL — `myvoice/app/`
- **프론트엔드**: React 19 + Vite 7 + TailwindCSS 4 + React Query — `myvoice/frontend/`
- Phase 1에서 프론트엔드 기초 구조, Phase 2에서 11개 Kids View 페이지를 mock 데이터로 구현 완료
- **Phase 3 목표**: 백엔드에 필요한 API를 추가하고, 프론트엔드의 mock 데이터를 실제 API로 교체

## 전제 조건

> Phase 2까지 완료된 프로젝트입니다. 다음 파일들이 이미 존재합니다:
> - `app/main.py` — FastAPI 앱 (라우터 등록)
> - `app/core/security.py` — JWT 인증 (`get_current_child_id`, `get_current_family_id`)
> - `app/models/` — SQLAlchemy 모델 (family, session, skill, curriculum 등)
> - `app/routers/kid_sessions.py` — 기존 세션 라우터
> - `app/routers/auth.py`, `auth_child.py` — 인증 라우터
> - `frontend/src/api/client.ts` — REST API 클라이언트
> - `frontend/src/api/hooks/` — 6개 React Query 훅 (현재 mock 데이터 사용)
> - `frontend/src/lib/mockData.ts` — mock 데이터 파일

---

## 파트 A: 백엔드 API 확장

### 작업 1: 새 모델 추가

다음 SQLAlchemy 모델들을 추가하세요.

#### 1-1. `app/models/vocabulary.py` [NEW]

```python
# VocabularyCategory: 어휘 카테고리 (food, animals, colors 등)
class VocabularyCategory(Base):
    __tablename__ = "vocabulary_categories"
    
    id: str (PK)           # "food", "animals" 등
    name: str              # "음식", "동물" 등
    emoji: str             # "🍎", "🐶" 등
    total_words: int       # 10
    sort_order: int        # 정렬 순서

# VocabularyWord: 개별 단어
class VocabularyWord(Base):
    __tablename__ = "vocabulary_words"
    
    id: UUID (PK)
    category_id: str (FK -> vocabulary_categories.id)
    word: str              # "Apple"
    korean: str            # "사과"
    emoji: str             # "🍎"
    sort_order: int

# VocabularyProgress: 아이별 학습 진행
class VocabularyProgress(Base):
    __tablename__ = "vocabulary_progress"
    
    id: UUID (PK)
    child_id: UUID (FK -> children.child_id)
    category_id: str (FK -> vocabulary_categories.id)
    words_learned: int     # 학습 완료 단어 수
    last_learned_at: datetime
```

#### 1-2. `app/models/shop.py` [NEW]

```python
# ShopItem: 상점 아이템
class ShopItem(Base):
    __tablename__ = "shop_items"
    
    id: str (PK)           # "hint", "time_extension" 등
    name: str              # "힌트"
    description: str       # "어려운 문제에서 힌트를 얻을 수 있어요."
    emoji: str             # "💡"
    price: int             # 별 10개
    item_type: str         # "consumable" 또는 "permanent"

# ChildInventory: 아이별 인벤토리
class ChildInventory(Base):
    __tablename__ = "child_inventories"
    
    id: UUID (PK)
    child_id: UUID (FK -> children.child_id, unique)
    stars: int             # 보유 별 수
    hearts: int            # 보유 하트 수
    max_hearts: int        # 최대 하트 (기본 3)
    hints: int             # 보유 힌트 수
    time_extensions: int   # 보유 시간 연장 수
    heart_refills: int     # 보유 하트 충전 수
    streak: int            # 연속 학습 일수
    last_active_date: date # 마지막 활동 날짜 (스트릭 계산용)
```

#### 1-3. `app/models/weekly_goal.py` [NEW]

```python
# WeeklyGoal: 주간 목표
class WeeklyGoal(Base):
    __tablename__ = "weekly_goals"
    
    id: UUID (PK)
    child_id: UUID (FK -> children.child_id)
    week_start: date       # 주의 시작일 (월요일)
    xp_target: int         # 목표 XP (기본 1000)
    xp_current: int        # 현재 XP
    missions_target: int   # 목표 모험 수 (기본 7)
    missions_current: int  # 현재 완료 모험 수
    study_time_target: int # 목표 학습 시간(분) (기본 60)
    study_time_current: int# 현재 학습 시간(분)
    words_target: int      # 목표 단어 수 (기본 20)
    words_current: int     # 현재 학습 단어 수
```

#### 1-4. `app/models/__init__.py` 업데이트

새 모델들을 import에 추가하세요.

#### 1-5. `app/models/family.py` — Child 모델에 추가 필드

```python
# Child 모델에 다음 필드 추가:
nickname: str | None       # 닉네임 (e.g., "루나")
avatar_emoji: str | None   # 아바타 이모지 (e.g., "🐰")
level: int                 # 기본 1
xp: int                    # 총 XP
onboarding_completed: bool # 온보딩 완료 여부
```

---

### 작업 2: 새 스키마 추가

#### 2-1. `app/schemas/vocabulary.py` [NEW]

```python
class VocabularyCategoryResponse(BaseModel):
    id: str
    name: str
    emoji: str
    total_words: int
    words_learned: int  # 아이별 진행률 (join query)

class VocabularyWordResponse(BaseModel):
    word: str
    korean: str
    emoji: str

class VocabularyCompleteRequest(BaseModel):
    words_learned: int
    stars_earned: int
    xp_earned: int
```

#### 2-2. `app/schemas/shop.py` [NEW]

```python
class ShopItemResponse(BaseModel):
    id: str
    name: str
    description: str
    emoji: str
    price: int

class InventoryResponse(BaseModel):
    stars: int
    hearts: int
    max_hearts: int
    hints: int
    time_extensions: int
    heart_refills: int

class PurchaseRequest(BaseModel):
    item_id: str

class PurchaseResponse(BaseModel):
    success: bool
    new_stars: int
    inventory: InventoryResponse
```

#### 2-3. `app/schemas/kid.py` [NEW]

```python
class KidHomeResponse(BaseModel):
    child: ChildProfileResponse
    weekly_goals: WeeklyGoalResponse
    recent_adventures: list[AdventureSummary]
    streak: int
    hearts: int
    max_hearts: int
    stars: int
    daily_bonus_available: bool

class ChildProfileResponse(BaseModel):
    child_id: UUID
    name: str
    nickname: str | None
    avatar_emoji: str | None
    level: int
    xp: int
    streak: int
    stats: ChildStats

class ChildStats(BaseModel):
    total_study_time: int      # 총 학습 시간(분)
    missions_completed: int    # 완료 모험 수
    vocabulary_learned: int    # 학습 단어 수
    pronunciation_accuracy: float  # 평균 발음 정확도(%)

class WeeklyGoalResponse(BaseModel):
    xp_current: int
    xp_target: int
    missions_current: int
    missions_target: int
    study_time_current: int
    study_time_target: int
    words_current: int
    words_target: int

class AdventureSummary(BaseModel):
    session_id: UUID
    title: str
    emoji: str
    status: str  # "completed", "in_progress", "locked"
    difficulty: str
    earned_stars: int | None
    earned_xp: int | None

class DailyBonusResponse(BaseModel):
    stars_reward: int
    hearts_reward: int
    consecutive_days: int
    new_stars: int
    new_hearts: int
    new_streak: int
```

---

### 작업 3: 새 라우터 추가

#### 3-1. `app/routers/kid_home.py` [NEW]

```
GET /v1/kid/home → KidHomeResponse
- 인증: child_token (get_current_child_id)
- 데이터: child 프로필 + ChildInventory + WeeklyGoal(이번 주) + 최근 세션 3개
- daily_bonus_available: ChildInventory.last_active_date < today 이면 true

POST /v1/kid/daily-bonus → DailyBonusResponse
- 인증: child_token
- 로직: last_active_date가 오늘이면 에러, 어제면 streak+1, 그 외 streak=1
- 보상: stars +50, hearts +1 (max 넘지 않도록)
```

#### 3-2. `app/routers/kid_vocabulary.py` [NEW]

```
GET /v1/kid/vocabulary → list[VocabularyCategoryResponse]
- 인증: child_token
- 데이터: 모든 카테고리 + 아이별 words_learned (LEFT JOIN)

GET /v1/kid/vocabulary/{category_id}/words → list[VocabularyWordResponse]
- 인증: child_token
- 데이터: 해당 카테고리의 단어 목록

POST /v1/kid/vocabulary/{category_id}/complete → VocabularyCompleteRequest
- 인증: child_token
- 로직: VocabularyProgress 업데이트 + ChildInventory에 stars/xp 추가 + WeeklyGoal words 업데이트
```

#### 3-3. `app/routers/kid_shop.py` [NEW]

```
GET /v1/kid/shop → { items: list[ShopItemResponse], inventory: InventoryResponse }
- 인증: child_token

POST /v1/kid/shop/purchase → PurchaseResponse
- 인증: child_token
- 로직: stars 차감, 해당 아이템에 맞는 inventory 필드 증가
- 에러: stars 부족 시 400
```

#### 3-4. `app/routers/kid_profile.py` [NEW]

```
GET /v1/kid/profile → ChildProfileResponse
- 인증: child_token
- 데이터: child 기본 정보 + ChildInventory + 통계 계산
  - total_study_time: sessions 테이블 duration_seconds 합산
  - missions_completed: sessions 테이블 status="ended" 카운트
  - vocabulary_learned: vocabulary_progress 합산
  - pronunciation_accuracy: task_attempts 평균 (없으면 0)
```

#### 3-5. `app/routers/kid_goals.py` [NEW]

```
GET /v1/kid/goals → WeeklyGoalResponse
- 인증: child_token
- 로직: 이번 주 WeeklyGoal 조회. 없으면 기본값으로 생성

POST /v1/kid/goals → WeeklyGoalResponse
- 인증: child_token
- body: { xp_target?, missions_target?, study_time_target?, words_target? }
- 로직: 이번 주 목표 수정
```

#### 3-6. `app/routers/kid_adventures.py` [NEW]

```
GET /v1/kid/adventures → list[AdventureSummary]
- 인증: child_token
- 데이터: CurriculumUnit 목록 + 아이별 완료 상태 (sessions JOIN)

GET /v1/kid/adventures/{id} → AdventureDetail
- 인증: child_token
- 데이터: CurriculumUnit 상세 + 보상 정보

POST /v1/kid/adventures/{id}/complete → { stars: int, xp: int }
- 인증: child_token
- 로직: 세션 종료 처리, ChildInventory에 stars/xp 추가, WeeklyGoal 업데이트
```

---

### 작업 4: main.py 라우터 등록

`app/main.py`에 새 라우터들을 등록하세요:

```python
from app.routers import kid_home, kid_vocabulary, kid_shop, kid_profile, kid_goals, kid_adventures

# === Kids View ===
app.include_router(kid_sessions.router, prefix="/v1/kid/sessions", tags=["Kid - Sessions"])
app.include_router(kid_home.router, prefix="/v1/kid", tags=["Kid - Home"])           # NEW
app.include_router(kid_adventures.router, prefix="/v1/kid/adventures", tags=["Kid - Adventures"])  # NEW
app.include_router(kid_vocabulary.router, prefix="/v1/kid/vocabulary", tags=["Kid - Vocabulary"])   # NEW
app.include_router(kid_shop.router, prefix="/v1/kid/shop", tags=["Kid - Shop"])      # NEW
app.include_router(kid_profile.router, prefix="/v1/kid/profile", tags=["Kid - Profile"])  # NEW
app.include_router(kid_goals.router, prefix="/v1/kid/goals", tags=["Kid - Goals"])   # NEW
```

---

### 작업 5: Seed 데이터

`app/seed.py` [NEW] — 초기 데이터 스크립트 생성:

```python
# 실행: python -m app.seed

# 1. VocabularyCategory 12개 (food, animals, colors, numbers, family, body, weather, clothes, school, toys, transportation, nature)
# 2. VocabularyWord 각 카테고리 10개씩 (frontend/src/lib/mockData.ts 및 VocabularyLearning.tsx 참조)
# 3. ShopItem 4개 (힌트, 시간 연장, 하트 충전, 불꽃 보호)
# 4. CurriculumUnit 6개 (missions[] mockData 참조 — 동물원, 과일가게, 가족, 학교, 우주, 색깔)
```

> **중요**: `frontend/src/lib/mockData.ts`의 데이터와 일치해야 합니다. 동일한 ID, 이름, 이모지를 사용하세요.

---

## 파트 B: 프론트엔드 API 연동

### 작업 6: API 훅 업데이트

모든 훅에서 **mock 데이터를 제거**하고 실제 API 호출로 교체합니다.

#### 6-1. `frontend/src/api/hooks/useAdventures.ts`

```typescript
// 변경 전: fetchAdventures에서 setTimeout으로 mock 반환
// 변경 후:
import { api } from '../client';

export function useAdventures() {
    return useQuery({
        queryKey: ['adventures'],
        queryFn: () => api.get<AdventureSummary[]>('/v1/kid/adventures'),
    });
}

export function useAdventureDetail(id: string) {
    return useQuery({
        queryKey: ['adventure', id],
        queryFn: () => api.get(`/v1/kid/adventures/${id}`),
        enabled: !!id,
    });
}

export function useCompleteAdventure() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (id: string) => api.post(`/v1/kid/adventures/${id}/complete`),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['adventures'] });
            queryClient.invalidateQueries({ queryKey: ['weeklyGoals'] });
        },
    });
}
```

#### 6-2. `frontend/src/api/hooks/useWeeklyGoals.ts`

```typescript
// 변경 전: fetchWeeklyGoals에서 mockData import
// 변경 후:
export function useWeeklyGoals() {
    return useQuery({
        queryKey: ['weeklyGoals'],
        queryFn: () => api.get<WeeklyGoalResponse>('/v1/kid/goals'),
    });
}
```

#### 6-3. `frontend/src/api/hooks/useClaimDailyBonus.ts`

```typescript
// 변경 전: localStorage 기반 mock
// 변경 후:
export function useClaimDailyBonus() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: () => api.post<DailyBonusResponse>('/v1/kid/daily-bonus'),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['kidHome'] });
        },
    });
}
```

#### 6-4. `useProfile.ts`, `useShop.ts`, `useVocabulary.ts`

이 3개 훅은 이미 올바른 API 경로를 사용 중이므로 **변경 불필요**.
단, 타입 제네릭을 추가하세요: `api.get<ChildProfileResponse>('/v1/kid/profile')`

#### 6-5. 신규 훅 추가

```typescript
// frontend/src/api/hooks/useKidHome.ts [NEW]
export function useKidHome() {
    return useQuery({
        queryKey: ['kidHome'],
        queryFn: () => api.get<KidHomeResponse>('/v1/kid/home'),
    });
}

// frontend/src/api/hooks/usePurchase.ts [NEW]
export function usePurchase() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (itemId: string) => api.post<PurchaseResponse>('/v1/kid/shop/purchase', { item_id: itemId }),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['shop'] });
            queryClient.invalidateQueries({ queryKey: ['kidHome'] });
        },
    });
}

// frontend/src/api/hooks/useVocabularyWords.ts [NEW]
export function useVocabularyWords(categoryId: string) {
    return useQuery({
        queryKey: ['vocabulary', categoryId, 'words'],
        queryFn: () => api.get<VocabularyWordResponse[]>(`/v1/kid/vocabulary/${categoryId}/words`),
        enabled: !!categoryId,
    });
}

export function useCompleteVocabulary() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: ({ categoryId, data }: { categoryId: string; data: VocabularyCompleteRequest }) =>
            api.post(`/v1/kid/vocabulary/${categoryId}/complete`, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['vocabulary'] });
            queryClient.invalidateQueries({ queryKey: ['weeklyGoals'] });
        },
    });
}
```

---

### 작업 7: 페이지 API 연동 업데이트

#### 7-1. `KidHome.tsx`

```diff
- import { missions, weeklyGoals, userData } from "@/lib/mockData";
+ import { useKidHome } from "@/api/hooks/useKidHome";
+ const { data: homeData, isLoading, error } = useKidHome();
```

- 로딩 상태 표시 (스켈레톤이나 스피너)
- 에러 상태 표시
- `homeData` 구조에 맞게 데이터 바인딩

#### 7-2. `Adventures.tsx`

```diff
- import { missions } from "@/lib/mockData";
+ import { useAdventures } from "@/api/hooks/useAdventures";
+ const { data: adventures, isLoading } = useAdventures();
```

#### 7-3. `AdventureResult.tsx`

```diff
+ import { useCompleteAdventure } from "@/api/hooks/useAdventures";
+ const completeMutation = useCompleteAdventure();
// 결과 화면 진입 시 completeMutation.mutate(id)
```

#### 7-4. `Vocabulary.tsx`

```diff
- import { vocabularyCategories } from "@/lib/mockData";
+ import { useVocabularyCategories } from "@/api/hooks/useVocabulary";
+ const { data: categories, isLoading } = useVocabularyCategories();
```

#### 7-5. `VocabularyLearning.tsx`

```diff
- const vocabularyData: Record<string, Array<...>> = { ... }; // 하드코딩 제거
+ import { useVocabularyWords } from "@/api/hooks/useVocabularyWords";
+ const { data: words, isLoading } = useVocabularyWords(categoryId || "");
```

#### 7-6. `VocabularyResult.tsx`

```diff
+ import { useCompleteVocabulary } from "@/api/hooks/useVocabularyWords";
+ const completeMutation = useCompleteVocabulary();
// 결과 화면 진입 시 completeMutation.mutate({ categoryId, data: { words_learned, stars_earned, xp_earned } })
```

#### 7-7. `KidShop.tsx`

```diff
- import { shopItems, userData } from "@/lib/mockData";
+ import { useShop } from "@/api/hooks/useShop";
+ import { usePurchase } from "@/api/hooks/usePurchase";
+ const { data: shopData, isLoading } = useShop();
+ const purchaseMutation = usePurchase();
```

#### 7-8. `KidProfile.tsx`

```diff
- import { userData } from "@/lib/mockData";
+ import { useProfile } from "@/api/hooks/useProfile";
+ const { data: profile, isLoading } = useProfile();
```

#### 7-9. `KidSkills.tsx`

스킬 페이지는 현재 mock 데이터가 `skillsData.ts`에 별도 존재하므로, Phase 3에서는 기존 mock 유지 가능.
단, 주간 목표 부분만 `useWeeklyGoals()` 훅으로 교체하세요.

---

### 작업 8: 인증 연동 (AuthContext 업데이트)

`frontend/src/contexts/AuthContext.tsx`에서 mock 로직을 실제 API로 교체:

```typescript
const loginAsParent = async (email: string, password: string) => {
    const res = await api.post<{ access_token: string; family_id: string }>('/v1/auth/login', { email, password });
    localStorage.setItem('family_token', res.access_token);
    setFamilyToken(res.access_token);
};

const selectChild = async (childId: string, pin?: string) => {
    const res = await api.post<{ child_token: string; child_id: string; child_name: string }>(
        '/v1/auth/select-child', { child_id: childId, pin }
    );
    localStorage.setItem('child_token', res.child_token);
    setChildToken(res.child_token);
};
```

`pages/Login.tsx` 및 `pages/SelectChild.tsx`도 실제 API 호출로 업데이트하세요.

---

### 작업 9: API 타입 정의

`frontend/src/api/types.ts` [NEW] — 백엔드 응답 타입 정의:

```typescript
// 백엔드 스키마와 1:1 매핑
export interface KidHomeResponse { ... }
export interface ChildProfileResponse { ... }
export interface WeeklyGoalResponse { ... }
export interface AdventureSummary { ... }
export interface VocabularyCategoryResponse { ... }
export interface VocabularyWordResponse { ... }
export interface ShopItemResponse { ... }
export interface InventoryResponse { ... }
export interface PurchaseResponse { ... }
export interface DailyBonusResponse { ... }
```

---

## 검증 기준

### 백엔드

1. `uvicorn app.main:app --reload` 실행 시 에러 없음
2. Swagger UI (`http://localhost:8000/docs`)에 새 엔드포인트 모두 표시
3. `python -m app.seed` 실행 시 seed 데이터 정상 삽입
4. 각 엔드포인트 curl/Swagger 테스트 성공:
   - `POST /v1/auth/signup` → `POST /v1/auth/login` → `POST /v1/auth/select-child` → `GET /v1/kid/home`
   - `GET /v1/kid/vocabulary` → `GET /v1/kid/vocabulary/food/words`
   - `GET /v1/kid/shop` → `POST /v1/kid/shop/purchase`

### 프론트엔드

1. `cd frontend && npx tsc --noEmit` — TypeScript 에러 없음
2. `npm run build` — 빌드 성공
3. `npm run dev` 후 `/kid/home` 접근 시 API에서 데이터 로드 (network 탭 확인)
4. 로딩 상태가 UI에 표시됨 (스피너 또는 스켈레톤)
5. API 에러 시 사용자 친화적 에러 메시지 표시

---

## 금지 사항

1. **tRPC 사용 금지** — REST API + fetch만 사용
2. **Crystal의 Express/Drizzle 코드 복사 금지** — FastAPI + SQLAlchemy 패턴 따르기
3. **DB 직접 접근 금지 (프론트엔드)** — 반드시 API를 통해 데이터 접근
4. **mockData.ts 삭제 금지** — import만 제거하고 파일은 유지 (Phase 5 테스트에 재사용)
5. **기존 라우터 구조 변경 금지** — 새 라우터만 추가
6. **동기 DB 호출 금지** — AsyncSession만 사용 (기존 패턴 따르기)

---

## 참조 파일

### 백엔드 (기존 패턴 참고용)

| 파일 | 참조 내용 |
|------|----------|
| `app/routers/kid_sessions.py` | 라우터 구조, `get_current_child_id` 사용법 |
| `app/routers/auth.py` | 인증 라우터 패턴 |
| `app/routers/auth_child.py` | `select-child` 엔드포인트 구조 |
| `app/models/family.py` | Child 모델 구조 |
| `app/models/session.py` | Session 모델 구조 |
| `app/core/security.py` | JWT 의존성 주입 패턴 |
| `app/schemas/session.py` | Pydantic 스키마 패턴 |
| `app/database.py` | DB 세션, Base 클래스 |

### 프론트엔드 (mock → API 전환 참고용)

| 파일 | 참조 내용 |
|------|----------|
| `frontend/src/api/client.ts` | API 클라이언트 (사용법) |
| `frontend/src/api/hooks/*.ts` | 현재 mock 훅들 (교체 대상) |
| `frontend/src/lib/mockData.ts` | seed 데이터 기준 (카테고리, 아이템, 미션 데이터) |
| `frontend/src/pages/kid/KidHome.tsx` | 홈 페이지 (API 연동 대상) |
| `frontend/src/pages/kid/KidShop.tsx` | 상점 페이지 (구매 로직) |
| `frontend/src/pages/kid/VocabularyLearning.tsx` | 어휘 학습 (단어 데이터 하드코딩 제거) |
| `frontend/src/contexts/AuthContext.tsx` | 인증 (mock → 실제 API) |
