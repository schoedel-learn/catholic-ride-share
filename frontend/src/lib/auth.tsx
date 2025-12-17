"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { getCurrentUser, login as apiLogin, type User } from "./api";

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

const TOKEN_KEY = "crs_token";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUserState] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Load token from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem(TOKEN_KEY);
    if (storedToken) {
      setToken(storedToken);
      // Fetch user data with the token
      getCurrentUser(storedToken)
        .then((userData) => {
          setUserState(userData);
        })
        .catch(() => {
          // Token is invalid, clear it
          localStorage.removeItem(TOKEN_KEY);
          setToken(null);
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await apiLogin(email, password);
    const newToken = response.access_token;

    // Store token
    localStorage.setItem(TOKEN_KEY, newToken);
    setToken(newToken);

    // Fetch user data
    const userData = await getCurrentUser(newToken);
    setUserState(userData);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUserState(null);
  }, []);

  const setUser = useCallback((updatedUser: User) => {
    setUserState(updatedUser);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, token, loading, login, logout, setUser }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
