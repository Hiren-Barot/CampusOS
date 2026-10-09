import React, { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import toast from "react-hot-toast";
import { CheckCircle2 } from "lucide-react";
import { resetPassword } from "../services/authService";

export default function ResetPassword() {
  const [params] = useSearchParams();
  const token = params.get("token") || "";
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const [done, setDone] = useState(false);
  const [loading, setLoading] = useState(false);

  function validate() {
    const next = {};
    if (!password) next.password = "Password is required";
    else if (password.length < 6) next.password = "Must be at least 6 characters";
    if (!confirm) next.confirm = "Please confirm your password";
    else if (confirm !== password) next.confirm = "Passwords do not match";
    setFieldErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    try {
      await resetPassword(token, password);
      setDone(true);
      toast.success("Password updated!");
      setTimeout(() => navigate("/login"), 2500);
    } catch (err) {
      toast.error(err.message || "Could not reset password");
    } finally {
      setLoading(false);
    }
  }

  if (!token) {
    return (
      <div className="w-full min-h-screen flex items-center justify-center bg-paper px-4">
        <div className="w-full max-w-[380px] bg-paper-raised border border-hairline rounded-sm p-8 text-center">
          <h2 className="font-serif text-[18px] font-semibold text-ink mb-2">Invalid link</h2>
          <p className="text-[13px] text-slate mb-5">
            This reset link is missing or invalid. Please request a new one.
          </p>
          <Link to="/forgot-password" className="text-[12.5px] text-urgent font-medium">
            Request a new link →
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full min-h-screen flex items-center justify-center bg-paper px-4">
      <div className="w-full max-w-[380px] bg-paper-raised border border-hairline rounded-sm p-8">
        <div className="font-serif text-[26px] font-bold text-ink mb-1">
          Campus<span className="text-urgent">OS</span>
        </div>
        <p className="font-mono text-[11px] text-slate mb-6">SET A NEW PASSWORD</p>

        {done ? (
          <div className="text-center py-4">
            <CheckCircle2 size={32} className="mx-auto text-result mb-3" />
            <p className="text-[13px] text-ink mb-2">Password updated!</p>
            <p className="text-[12px] text-slate">Redirecting you to sign in…</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-col gap-3">
            <div>
              <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">NEW PASSWORD</label>
              <input
                type="password"
                className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${fieldErrors.password ? "border-urgent" : "border-hairline"}`}
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoFocus
              />
              {fieldErrors.password && (
                <p className="text-urgent text-[11px] mt-1">{fieldErrors.password}</p>
              )}
            </div>
            <div>
              <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">CONFIRM PASSWORD</label>
              <input
                type="password"
                className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${fieldErrors.confirm ? "border-urgent" : "border-hairline"}`}
                placeholder="••••••••"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
              />
              {fieldErrors.confirm && (
                <p className="text-urgent text-[11px] mt-1">{fieldErrors.confirm}</p>
              )}
            </div>
            <button
              type="submit"
              disabled={loading}
              className="mt-2 rounded-sm py-2 text-[13px] font-medium text-white bg-[#1B2430] hover:bg-urgent transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading && <span className="w-3.5 h-3.5 border-2 border-white/40 border-t-white rounded-full animate-spin" />}
              {loading ? "Updating…" : "Update password"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}