const API_BASE = import.meta.env.VITE_API_BASE || '';

// ---------------------------------------------------------------------------
// snake_case ↔ camelCase conversion
// ---------------------------------------------------------------------------

export function toCamel(s: string): string {
    return s.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
}

export function toSnake(s: string): string {
    return s.replace(/([A-Z])/g, (c) => `_${c.toLowerCase()}`);
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function snakeToCamel<T>(obj: unknown): T {
    if (Array.isArray(obj)) return obj.map(snakeToCamel) as T;
    if (obj !== null && typeof obj === 'object') {
        return Object.fromEntries(
            Object.entries(obj as Record<string, unknown>).map(([k, v]) => [
                toCamel(k),
                snakeToCamel(v),
            ])
        ) as T;
    }
    return obj as T;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function camelToSnake<T>(obj: unknown): T {
    if (Array.isArray(obj)) return obj.map(camelToSnake) as T;
    if (obj !== null && typeof obj === 'object') {
        return Object.fromEntries(
            Object.entries(obj as Record<string, unknown>).map(([k, v]) => [
                toSnake(k),
                camelToSnake(v),
            ])
        ) as T;
    }
    return obj as T;
}

// ---------------------------------------------------------------------------
// API request helper
// ---------------------------------------------------------------------------

export async function apiRequest<T>(
    endpoint: string,
    options?: RequestInit & { skipCamelConversion?: boolean }
): Promise<T> {
    const token = localStorage.getItem('child_token') || localStorage.getItem('family_token');

    const res = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        credentials: 'include', // Send cookies (HttpOnly)
        headers: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            ...options?.headers,
        },
    });

    if (!res.ok) {
        // Support both new {"error": {...}} format and legacy {"detail": ...}
        const errorBody = await res.json().catch(() => ({}));
        const message =
            errorBody?.error?.message ||
            errorBody?.detail ||
            `API Error: ${res.status}`;
        throw new Error(message);
    }

    const data = await res.json();

    // Auto-convert snake_case → camelCase unless caller opts out
    if (options?.skipCamelConversion) return data as T;
    return snakeToCamel<T>(data);
}

export const api = {
    get: <T>(endpoint: string) => apiRequest<T>(endpoint),
    post: <T>(endpoint: string, data?: unknown, options?: RequestInit & { skipCamelConversion?: boolean }) =>
        apiRequest<T>(endpoint, {
            ...options,
            method: 'POST',
            // Convert camelCase request body → snake_case for backend
            body: data ? JSON.stringify(camelToSnake(data)) : undefined,
        }),
    put: <T>(endpoint: string, data?: unknown, options?: RequestInit & { skipCamelConversion?: boolean }) =>
        apiRequest<T>(endpoint, {
            ...options,
            method: 'PUT',
            body: data ? JSON.stringify(camelToSnake(data)) : undefined,
        }),
    patch: <T>(endpoint: string, data?: unknown, options?: RequestInit & { skipCamelConversion?: boolean }) =>
        apiRequest<T>(endpoint, {
            ...options,
            method: 'PATCH',
            body: data ? JSON.stringify(camelToSnake(data)) : undefined,
        }),
    delete: <T>(endpoint: string) =>
        apiRequest<T>(endpoint, { method: 'DELETE' }),
};

// Phase 3: Skills API
export async function getKidSkills() {
    return api.get<{ items: import('./types').SkillLevelResponse[] }>('/v1/kid/skills');
}

// Phase 4: Gamification & Avatar
export async function updateAvatar(avatarId: string) {
    return api.patch<{ status: string; avatarId: string }>('/v1/kid/profile/avatar', {
        avatarId, // Snake case conversion will handle naming if needed, but endpoint expects avatar_id
    });
}

// Phase 5: Parent Dashboard
export const parentApi = {
    listChildren: () => api.get<import('./types').ChildProfile[]>('/v1/parent/children'),
    createChild: (data: import('./types').ChildCreate) => api.post<import('./types').ChildProfile>('/v1/parent/children', data),
    updateChild: (childId: string, data: import('./types').ChildUpdate) => api.patch<import('./types').ChildProfile>(`/v1/parent/children/${childId}`, data),
    getDashboardStats: (childId: string) => api.get<import('./types').DashboardStats>(`/v1/parent/dashboard/stats?child_id=${childId}`),
    listReports: (childId: string) => api.get<import('./types').Report[]>(`/v1/parent/reports?child_id=${childId}`),
    getReport: (reportId: string) => api.get<import('./types').Report>(`/v1/parent/reports/${reportId}`),

    // Insights
    getKeywords: (childId: string, days = 30) => api.get<import('./types').KeywordItem[]>(`/v1/parent/insights/keywords?child_id=${childId}&days=${days}`),
    getSentiment: (childId: string, days = 30) => api.get<import('./types').SentimentSummary>(`/v1/parent/insights/sentiment?child_id=${childId}&days=${days}`),
    getTimeline: (childId: string, days = 14) => api.get<import('./types').TimelineDay[]>(`/v1/parent/insights/timeline?child_id=${childId}&days=${days}`),
    getLanguageMix: (childId: string, days = 30) => api.get<import('./types').LanguageMix>(`/v1/parent/insights/language-mix?child_id=${childId}&days=${days}`),
    getBehavior: (childId: string, days = 30) => api.get<import('./types').BehaviorPatterns>(`/v1/parent/insights/behavior?child_id=${childId}&days=${days}`),
};
