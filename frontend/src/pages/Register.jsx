import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../lib/api.js";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const { data } = await api.post("/auth/register", { email, password });
      localStorage.setItem("chronicle_token", data.access_token);
      navigate("/");
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-bg text-text">
      <form onSubmit={handleSubmit} className="glass rounded-xl2 p-8 w-full max-w-sm space-y-4">
        <h1 className="text-xl font-semibold">Create your Chronicle AI account</h1>
        <input
          className="w-full bg-bg border border-white/10 rounded-xl2 px-3 py-2"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="w-full bg-bg border border-white/10 rounded-xl2 px-3 py-2"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button
          disabled={loading}
          className="w-full bg-gradient-to-r from-primary to-accent rounded-xl2 py-2.5 font-medium disabled:opacity-50"
        >
          {loading ? "Creating…" : "Create Account"}
        </button>
        <p className="text-sm text-muted text-center">
          Already have an account? <Link to="/login" className="text-text underline">Sign in</Link>
        </p>
      </form>
    </div>
  );
}
