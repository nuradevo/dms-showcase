import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import axios from "axios";

type AuthContextType = {
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const t = typeof window !== "undefined" ? localStorage.getItem("dms_token") : null;
    if (t) setToken(t);
  }, []);

  const login = async (email: string, password: string) => {
    const fd = new URLSearchParams();
    fd.append("username", email);
    fd.append("password", password);
    const res = await axios.post(`${apiBase}/token`, fd, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    const t = res.data?.access_token;
    if (!t) throw new Error("No token returned");
    setToken(t);
    if (typeof window !== "undefined") localStorage.setItem("dms_token", t);
  };

  const logout = () => {
    setToken(null);
    if (typeof window !== "undefined") localStorage.removeItem("dms_token");
  };

  return (
    <AuthContext.Provider value={{ token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}