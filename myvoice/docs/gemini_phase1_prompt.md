# Phase 1: Frontend Foundation — 밤토리 (Bamtory) MVP

> **상태**: ✅ **완료** (2026-02 완료)
> 이 프롬프트는 Gemini에게 전달되어 실행 완료되었습니다.
> 결과: `frontend/` 디렉토리에 React + Vite + TypeScript 프로젝트 생성, 디자인 시스템 이식, REST API 클라이언트 구축, 인증 컨텍스트 및 라우팅 설정 완료.

## 프로젝트 개요

밤토리는 4-12세 아이를 위한 Voice AI 영어 학습 앱입니다.
- 백엔드: FastAPI (Python 3.11) + PostgreSQL + Redis — 이미 `myvoice/app/` 에 구축됨
- 프론트엔드: 이번에 새로 구축 (아래 작업)
- 디자이너(Crystal)가 Manus 플랫폼에서 만든 React 프로토타입이 `myvoice/crystal/task_source/` 에 있음
- 이 프로토타입의 UI/UX 디자인을 최대한 살리면서, tRPC 통신을 REST API로 교체하여 FastAPI 백엔드와 연동할 것

### 현재 디렉토리 구조

```
myvoice/
├── app/                    # FastAPI 백엔드 (이미 구축됨 — 수정하지 않을 것)
│   ├── main.py            # FastAPI 엔트리포인트
│   ├── routers/           # /v1/auth/*, /v1/kid/*, /v1/parent/*
│   ├── models/            # SQLAlchemy 모델
│   ├── schemas/           # Pydantic 스키마
│   └── services/          # 비즈니스 로직
├── crystal/               # 디자이너 프로토타입 (참조용 — 수정하지 않을 것)
│   ├── task_source/       # React 소스 코드
│   └── screenshot/        # UI 스크린샷
├── migrations/            # Alembic DB 마이그레이션
├── frontend/              # ⬅️ [여기에 새로 생성할 것]
├── docker-compose.yml     # PostgreSQL + Redis
├── pyproject.toml         # Python 의존성
└── SPEC.md               # 기술 명세
```

## 프론트엔드 기술 스택 (확정)

| 항목 | 선택 |
|------|------|
| Framework | React 19 + TypeScript |
| Build | Vite 7 |
| Styling | TailwindCSS 4 + CSS Variables |
| UI Components | Radix UI + shadcn/ui (Crystal에서 가져옴) |
| Routing | **React Router v7** (wouter 대체) |
| Data Fetching | **TanStack React Query + fetch** (tRPC 대체) |
| Icons | Lucide React |
| Animation | Framer Motion |
| Font | Nunito (Google Fonts) |

---

## 작업 1: 프로젝트 초기화

`myvoice/frontend/` 디렉토리에 Vite + React + TypeScript 프로젝트를 생성하세요.

```bash
cd /Users/yuil/Documents/github/myvoice
npx -y create-vite@latest frontend -- --template react-ts
cd frontend
npm install
```

## 작업 2: 핵심 의존성 설치

```bash
cd /Users/yuil/Documents/github/myvoice/frontend
npm install react-router-dom@7 @tanstack/react-query framer-motion lucide-react sonner
npm install @radix-ui/react-dialog @radix-ui/react-progress @radix-ui/react-tabs @radix-ui/react-tooltip @radix-ui/react-select @radix-ui/react-avatar @radix-ui/react-switch @radix-ui/react-slot
npm install class-variance-authority clsx tailwind-merge
npm install -D tailwindcss @tailwindcss/vite
```

## 작업 3: Crystal 디자인 시스템 이식

Crystal의 `crystal/task_source/index.css` 파일에서 디자인 토큰을 가져와 `frontend/src/index.css`에 적용하세요.

주요 이식 항목:
- CSS 변수 (--duo-green, --duo-blue, --duo-yellow 등 전체 색상 팔레트)
- 커스텀 클래스 (.duo-card, .duo-badge, .duo-mic-button, .duo-speech-bubble 등)
- 애니메이션 (@keyframes bounce-in, pulse-scale 등)
- Nunito 폰트 설정
- TailwindCSS 4 import (`@import "tailwindcss"`)
- 스크롤바 숨김 설정

또한 `frontend/index.html`에 Nunito 폰트를 로드하세요:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
```

## 작업 4: REST API 클라이언트 레이어

`frontend/src/api/` 디렉토리에 API 클라이언트를 구축하세요.

### `frontend/src/api/client.ts` — 공통 API 함수

```typescript
const API_BASE = import.meta.env.VITE_API_BASE || '';

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const token = localStorage.getItem('child_token') || localStorage.getItem('family_token');
  
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
  });
  
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || `API Error: ${res.status}`);
  }
  
  return res.json();
}

export const api = {
  get: <T>(endpoint: string) => apiRequest<T>(endpoint),
  post: <T>(endpoint: string, data?: unknown) =>
    apiRequest<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    }),
  put: <T>(endpoint: string, data?: unknown) =>
    apiRequest<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    }),
  delete: <T>(endpoint: string) =>
    apiRequest<T>(endpoint, { method: 'DELETE' }),
};
```

### `frontend/src/api/hooks/useAdventures.ts` — 모험(세션) 훅 예시

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../client';

export function useAdventures() {
  return useQuery({
    queryKey: ['adventures'],
    queryFn: () => api.get('/v1/kid/sessions'),
  });
}

export function useAdventureDetail(id: string) {
  return useQuery({
    queryKey: ['adventure', id],
    queryFn: () => api.get(`/v1/kid/sessions/${id}`),
    enabled: !!id,
  });
}
```

다른 훅들도 같은 패턴으로 만드세요:
- `useWeeklyGoals.ts` — GET /v1/kid/goals
- `useVocabulary.ts` — GET /v1/kid/vocabulary
- `useProfile.ts` — GET /v1/kid/profile
- `useShop.ts` — GET /v1/kid/shop

## 작업 5: 인증 컨텍스트

### `frontend/src/contexts/AuthContext.tsx`

듀얼 뷰 인증:
- `family_token`: 부모 인증 (Google/Apple OAuth)
- `child_token`: 아이 인증 (부모가 자녀 선택 후 발급)
- Kids View → child_token 필수
- Parent View → family_token 필수

Crystal의 `crystal/task_source/useAuth.ts`를 참조하되:
- Manus OAuth 코드는 사용하지 않음
- Phase 1에서는 인증 UI 골격만 구현
- 실제 OAuth 연동은 Phase 2+에서 진행
- 로그인/로그아웃 상태 관리와 토큰 저장/삭제 로직만 구현

AuthContext가 제공해야 할 값:
```typescript
interface AuthContextType {
  // 부모 인증
  familyToken: string | null;
  isParentAuthenticated: boolean;
  loginAsParent: (token: string) => void;
  logoutParent: () => void;
  
  // 아이 인증
  childToken: string | null;
  isChildAuthenticated: boolean;
  selectedChild: ChildProfile | null;
  selectChild: (childId: string) => void;
  
  // 현재 사용자
  user: UserProfile | null;
}
```

## 작업 6: 라우팅 설정

### `frontend/src/App.tsx`

React Router v7 기반 듀얼 뷰:

```
/                           → 랜딩 (비로그인 시)
/login                      → 로그인
/select-child               → 자녀 선택

/kid/home                   → Kids View 홈
/kid/adventures             → 모험 목록
/kid/adventure/:id          → 모험 상세
/kid/adventure/:id/play     → 모험 진행
/kid/adventure/:id/result   → 모험 결과
/kid/vocabulary             → 어휘 목록
/kid/vocabulary/:cat        → 어휘 학습
/kid/vocabulary/:cat/result → 어휘 결과
/kid/shop                   → 상점
/kid/profile                → 프로필
/kid/skills                 → 스킬 상세

/parent/dashboard           → Parent View 대시보드 (Phase 4, placeholder만)
/parent/reports/:childId    → 리포트 (Phase 4, placeholder만)
/parent/children            → 자녀 관리 (Phase 4, placeholder만)
/parent/settings            → 설정 (Phase 4, placeholder만)
```

- `/kid/*` 경로는 `KidProtectedRoute` 으로 감싸서 child_token 필요
- `/parent/*` 경로는 `ParentProtectedRoute` 으로 감싸서 family_token 필요
- Phase 4 경로들은 "준비 중입니다" placeholder 페이지로 구현

## 작업 7: 기본 레이아웃 컴포넌트 이식

Crystal에서 다음 컴포넌트를 이식:

### 7-1. BottomNav
- **참조:** `crystal/task_source/BottomNav.tsx`
- "미션" 탭 → "모험" 으로 라벨 변경
- 라우트를 `/kid/*` 경로로 수정
- 아이콘 유지 (Lucide React)
- 현재 경로 하이라이트 (React Router useLocation 사용)

### 7-2. KidProtectedRoute / ParentProtectedRoute
- **참조:** `crystal/task_source/ProtectedRoute.tsx`
- KidProtectedRoute: child_token 없으면 /select-child로 리다이렉트
- ParentProtectedRoute: family_token 없으면 /login으로 리다이렉트

### 7-3. KidLayout
- Kids View 전용 레이아웃: 콘텐츠 + BottomNav
- Crystal의 h-screen + overflow 패턴 적용 (모바일 최적화)

### 7-4. Placeholder Pages
- `/kid/home` → "Kids View 홈 (Phase 2에서 구현)" 텍스트 + BottomNav
- `/kid/adventures` → "모험 목록 (Phase 2에서 구현)" 텍스트 + BottomNav
- 나머지 경로도 placeholder로 최소 구현

## 작업 8: Vite 설정

### `frontend/vite.config.ts`

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/v1': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

## 작업 9: 환경 변수

### `frontend/.env`
```
VITE_API_BASE=
```

> API_BASE가 빈 문자열이면 Vite 프록시를 통해 /v1/* 요청이 localhost:8000으로 전달됩니다.

---

## 검증 기준

Phase 1 완료 후 다음을 확인하세요:

1. ✅ `cd myvoice/frontend && npm run dev` → 로컬 서버 정상 실행 (port 5173)
2. ✅ `npm run build` → 빌드 에러 없음
3. ✅ 브라우저에서 `http://localhost:5173` 접속 시:
   - 라우팅 동작 (`/kid/home`, `/kid/adventures` 등 이동 가능)
   - Crystal 디자인 토큰 (색상, 폰트 Nunito) 적용됨
   - BottomNav 네비게이션 동작 (탭 전환, 현재 위치 하이라이트)
   - KidProtectedRoute가 미인증 시 /login으로 리다이렉트
4. ✅ Vite 프록시가 `/v1/*` 요청을 `localhost:8000`으로 전달

## ⛔ 금지 사항

- ❌ tRPC 사용 금지 — REST API (fetch + React Query)만 사용
- ❌ MySQL 접근 금지 — PostgreSQL만 사용 (백엔드)
- ❌ Manus OAuth 코드 복사 금지 — Google OAuth 기반
- ❌ `wouter` 사용 금지 — React Router v7 사용
- ❌ Crystal `db.ts`, `routers.ts`, `schema.ts` 등 백엔드 코드 복사 금지
- ❌ `app/` 디렉토리 수정 금지 — 기존 FastAPI 백엔드는 건드리지 않음
- ❌ `crystal/` 디렉토리 수정 금지 — 참조만 할 것

## 참조할 Crystal 파일 목록

| 파일 | 용도 | 이식 방법 |
|------|------|----------|
| `crystal/task_source/index.css` | 디자인 시스템 (색상, 애니메이션) | CSS 변수와 클래스 복사 |
| `crystal/task_source/App.tsx` | 라우팅 구조 참조 | 구조만 참조, React Router로 다시 작성 |
| `crystal/task_source/BottomNav.tsx` | 하단 네비게이션 | 라벨/경로 수정 후 이식 |
| `crystal/task_source/ProtectedRoute.tsx` | 인증 가드 | AuthContext 기반으로 재작성 |
| `crystal/task_source/index.html` | HTML 템플릿 | Nunito 폰트 링크만 가져옴 |
| `crystal/task_source/useAuth.ts` | 인증 훅 참조 | 구조 참조, OAuth는 다시 작성 |
| `crystal/task_source/vite.config.ts` | Vite 설정 참조 | 별칭(@) 설정, 프록시 설정 참조 |
| `crystal/task_source/package.json` | 의존성 참조 | 필요한 패키지만 선별 설치 |

## 결과물 디렉토리 구조 (예상)

```
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── client.ts              # REST API 클라이언트
│   │   └── hooks/
│   │       ├── useAdventures.ts
│   │       ├── useWeeklyGoals.ts
│   │       ├── useVocabulary.ts
│   │       ├── useProfile.ts
│   │       └── useShop.ts
│   ├── components/
│   │   ├── layout/
│   │   │   ├── BottomNav.tsx
│   │   │   ├── KidLayout.tsx
│   │   │   └── ParentLayout.tsx
│   │   └── ui/                    # shadcn/ui (Phase 2에서 채움)
│   ├── contexts/
│   │   ├── AuthContext.tsx
│   │   └── ThemeContext.tsx
│   ├── pages/
│   │   ├── kid/
│   │   │   ├── KidHome.tsx        # placeholder
│   │   │   ├── Adventures.tsx     # placeholder
│   │   │   ├── Vocabulary.tsx     # placeholder
│   │   │   ├── Shop.tsx           # placeholder
│   │   │   ├── Profile.tsx        # placeholder
│   │   │   └── Skills.tsx         # placeholder
│   │   ├── parent/
│   │   │   └── Dashboard.tsx      # placeholder
│   │   ├── Login.tsx
│   │   ├── SelectChild.tsx
│   │   └── Landing.tsx
│   ├── guards/
│   │   ├── KidProtectedRoute.tsx
│   │   └── ParentProtectedRoute.tsx
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css                  # Crystal 디자인 시스템
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── .env
└── package.json
```
