import React from "react";
import { createContext, useState, useEffect } from "react";
import * as authService from "../services/authService";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const existing = authService.getCurrentUser();
    if (existing) {
      setUser(existing);
    }
    setLoading(false);
  }, []);

  async function login(email, password) {
    const session = await authService.login(email, password);
    setUser(session);
    return session;
  }

  async function register(data) {
    const session = await authService.register(data);
    setUser(session);
    return session;
  }

  function logout() {
    authService.logout();
    setUser(null);
  }

  function updateProfile(updates) {
    setUser((prev) => {
      if (!prev) return prev;
      const next = { ...prev, ...updates };
      authService.setStoredUser(next);
      return next;
    });
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateProfile }}>
      {children}
    </AuthContext.Provider>
  );
}