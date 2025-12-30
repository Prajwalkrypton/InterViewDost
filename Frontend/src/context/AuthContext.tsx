import { createContext, useContext, useState, ReactNode } from "react";

export type AuthUser = {
  user_id: number;
  name: string | null;
  email: string | null;
  role: string | null;
};

export type AuthState = {
  user: AuthUser | null;
  accessToken: string | null;
  resumeSummary: string | null;
  skills: string[];
};

const AuthContext = createContext<{
  state: AuthState;
  setState: (next: AuthState) => void;
} | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    accessToken: null,
    resumeSummary: null,
    skills: [],
  });

  return (
    <AuthContext.Provider value={{ state, setState }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
