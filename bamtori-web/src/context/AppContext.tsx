"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define types for our state
interface ChildProfile {
  name: string;
  age: number;
  gender: 'male' | 'female' | '';
  interests: string[];
}

interface AppState {
  isLoggedIn: boolean;
  childProfile: ChildProfile | null;
  subscription: 'basic' | 'standard' | 'premium' | null;
  mode: 'parent' | 'child' | null;
}

interface AppContextType extends AppState {
  login: () => void;
  setChildProfileData: (data: ChildProfile) => void;
  setSubscriptionPlan: (plan: 'basic' | 'standard' | 'premium') => void;
  setAppMode: (mode: 'parent' | 'child') => void;
  reset: () => void;
}

const defaultState: AppState = {
  isLoggedIn: false,
  childProfile: null,
  subscription: null,
  mode: null,
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  // Initialize state with default values
  // We'll hydrate from localStorage in useEffect to avoid hydration mismatch
  const [state, setState] = useState<AppState>(defaultState);
  const [isLoaded, setIsLoaded] = useState(false);

  // Hydrate from localStorage on mount
  useEffect(() => {
    const storedState = localStorage.getItem('bamtori_state');
    if (storedState) {
      try {
        setState(JSON.parse(storedState));
      } catch (e) {
        console.error("Failed to parse stored state", e);
      }
    }
    setIsLoaded(true);
  }, []);

  // Persist to localStorage whenever state changes
  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem('bamtori_state', JSON.stringify(state));
    }
  }, [state, isLoaded]);

  const login = () => {
    setState(prev => ({ ...prev, isLoggedIn: true }));
  };

  const setChildProfileData = (data: ChildProfile) => {
    setState(prev => ({ ...prev, childProfile: data }));
  };

  const setSubscriptionPlan = (plan: 'basic' | 'standard' | 'premium') => {
    setState(prev => ({ ...prev, subscription: plan }));
  };

  const setAppMode = (mode: 'parent' | 'child') => {
    setState(prev => ({ ...prev, mode }));
  };
  
  const reset = () => {
    setState(defaultState);
    localStorage.removeItem('bamtori_state');
  }

  // Prevent flash of unhydrated content if needed, though for this simple app it's fine
  // to render with default state initially.

  return (
    <AppContext.Provider value={{
      ...state,
      login,
      setChildProfileData,
      setSubscriptionPlan,
      setAppMode,
      reset
    }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
