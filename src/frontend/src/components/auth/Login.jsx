import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import useAuth from "../../hooks/useAuth";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function validate() {
    const next = {};
    if (!email.trim()) next.email = "Email is required";
    else if (!/^\S+@\S+\.\S+$/.test(email)) next.email = "Enter a valid email";
    if (!password) next.password = "Password is required";
    setFieldErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    if (!validate()) return;
    setLoading(true);
    try {
      await login(email.trim(), password);
      toast.success("Welcome back!");
      navigate("/dashboard");
    } catch (err) {
      const message = err.message || "Login failed";
      setError(message);
      toast.error(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full min-h-screen flex items-center justify-center bg-paper px-4">
      <div className="w-full max-w-[380px] bg-paper-raised border border-hairline rounded-sm p-8">
        <div className="font-serif text-[26px] font-bold text-ink mb-1">
          Campus<span className="text-urgent">OS</span>
        </div>
        <p className="font-mono text-[11px] text-slate mb-6">SIGN IN TO YOUR ACCOUNT</p>

        {error && (
          <div className="text-[12.5px] text-urgent bg-urgent/10 rounded-sm px-3 py-2 mb-4">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <div>
            <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">EMAIL</label>
            <input
              type="email"
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${fieldErrors.email ? "border-urgent" : "border-hairline"}`}
              placeholder="you@gtu.ac.in"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoFocus
            />
            {fieldErrors.email && <p className="text-urgent text-[11px] mt-1">{fieldErrors.email}</p>}
          </div>
          <div>
            <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">PASSWORD</label>
            <input
              type="password"
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${fieldErrors.password ? "border-urgent" : "border-hairline"}`}
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {fieldErrors.password && <p className="text-urgent text-[11px] mt-1">{fieldErrors.password}</p>}
          </div>
          <button
            type="submit"
            disabled={loading}
            className="mt-2 rounded-sm py-2 text-[13px] font-medium text-white bg-[#1B2430] hover:bg-urgent transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading && <span className="w-3.5 h-3.5 border-2 border-white/40 border-t-white rounded-full animate-spin" />}
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p className="text-[12.5px] text-slate mt-5">
          New student?{" "}
          <Link to="/register" className="text-urgent font-medium">
            Create an account
          </Link>
        </p>
      </div>
    </div>
  );
}