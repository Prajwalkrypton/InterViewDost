import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiPost } from "../lib/api";
import { useAuth } from "../context/AuthContext";

interface AuthLoginResponse {
  access_token: string;
  token_type: string;
  user: {
    user_id: number;
    name: string | null;
    email: string | null;
    role: string | null;
  };
}

export function LoginPage() {
  const { setState } = useAuth();
  const [email, setEmail] = useState("prajwalts.is23@rvce.edu.in");
  const [password, setPassword] = useState("1234");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const data = await apiPost<AuthLoginResponse>("/api/auth/login", {
        email,
        password,
      });
      setState({
        user: data.user,
        accessToken: data.access_token,
        resumeSummary: null,
        skills: [],
      });
      navigate("/profile");
    } catch (err: any) {
      setError(err.message ?? "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="w-full max-w-md bg-zinc-900 rounded-xl p-8 shadow-lg border border-zinc-700">
        <h1 className="text-2xl font-semibold mb-6 text-center">Sign in to InterviewDost</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-md bg-zinc-800 border border-zinc-700 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-md bg-zinc-800 border border-zinc-700 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
            />
          </div>
          {error && <p className="text-sm text-red-400">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-2 rounded-md bg-indigo-600 hover:bg-indigo-500 text-sm font-medium disabled:opacity-60"
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}
