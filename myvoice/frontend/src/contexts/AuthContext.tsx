import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/api/client';
import type { ChildProfile } from '@/api/types';

interface AuthContextType {
    // Parent Authentication
    familyToken: string | null;
    isParentAuthenticated: boolean;
    isCheckingAuth: boolean;
    loginAsParent: (token: string) => void;
    logoutParent: () => void;

    // Child Authentication
    childToken: string | null;
    isChildAuthenticated: boolean;
    user: ChildProfile | null;
    loginAsChild: (token: string) => void;
    logoutChild: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [familyToken, setFamilyToken] = useState<string | null>(localStorage.getItem('family_token'));
    const [childToken, setChildToken] = useState<string | null>(localStorage.getItem('child_token'));
    // True when we have confirmed cookie-only auth (e.g. after OAuth redirect)
    const [cookieAuthVerified, setCookieAuthVerified] = useState(false);
    const [isCheckingAuth, setIsCheckingAuth] = useState(!familyToken);

    // On mount, if no localStorage token, check if an HttpOnly cookie session exists
    useEffect(() => {
        if (familyToken) {
            setIsCheckingAuth(false);
            return;
        }
        api.get<unknown>('/v1/parent/children')
            .then(() => setCookieAuthVerified(true))
            .catch(() => {/* no cookie session — stay logged out */})
            .finally(() => setIsCheckingAuth(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // Fetch child profile when child token is present
    const { data: childProfile, error } = useQuery({
        queryKey: ['auth', 'child', childToken],
        queryFn: () => api.get<ChildProfile>('/v1/kid/profile'),
        enabled: !!childToken,
        retry: false,
    });

    useEffect(() => {
        if (error) {
            console.error('Failed to fetch child profile', error);
        }
    }, [error]);

    const isParentAuthenticated = !!familyToken || cookieAuthVerified;
    const isChildAuthenticated = !!childToken;

    const loginAsParent = (token: string) => {
        localStorage.setItem('family_token', token);
        setFamilyToken(token);
        setCookieAuthVerified(false);
    };

    const logoutParent = () => {
        localStorage.removeItem('family_token');
        localStorage.removeItem('child_token');
        setFamilyToken(null);
        setChildToken(null);
        setCookieAuthVerified(false);
    };

    const loginAsChild = (token: string) => {
        localStorage.setItem('child_token', token);
        setChildToken(token);
    };

    const logoutChild = () => {
        localStorage.removeItem('child_token');
        setChildToken(null);
    };

    return (
        <AuthContext.Provider
            value={{
                familyToken,
                isParentAuthenticated,
                isCheckingAuth,
                loginAsParent,
                logoutParent,
                childToken,
                isChildAuthenticated,
                user: childProfile ?? null,
                loginAsChild,
                logoutChild,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
