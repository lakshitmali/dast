// DAST Platform — Auth Hook

'use client';

import { useState, useEffect, createContext, useContext, useCallback } from 'react';
import { api } from '@/lib/api';
import type { User } from '@/types/user';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  // Authentication is intentionally disabled for this local deployment.
  const [user, setUser] = useState<User | null>({
    id: 'local-demo-user',
    email: 'demo@localhost',
    username: 'demo',
    full_name: 'Demo User',
    is_active: true,
    is_admin: true,
    tos_accepted_at: new Date().toISOString(),
    created_at: new Date().toISOString(),
  });
  const [loading, setLoading] = useState(false);

  const refreshUser = useCallback(async () => {
    setLoading(false);
  }, []);

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  const login = async (email: string, password: string) => {
    await api.login(email, password);
    await refreshUser();
  };

  const register = async (email: string, username: string, password: string, fullName?: string) => {
    await api.register(email, username, password, fullName);
  };

  const logout = () => {
    // Keep the local app usable without a login screen.
    setUser({
      id: 'local-demo-user', email: 'demo@localhost', username: 'demo',
      full_name: 'Demo User', is_active: true, is_admin: true,
      tos_accepted_at: new Date().toISOString(), created_at: new Date().toISOString(),
    });
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser }}>
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
