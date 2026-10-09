import React, { useState } from "react";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";
import { Mail } from "lucide-react";
import { forgotPassword } from "../services/authService";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  function validate() {
    const next = {};
    const trimmed = email.trim();
    if (!trimmed) next.email = "Email is required";
    else if (!/^\S+@\S+\.\S+$/.test(trimmed)) next.email = "Enter a valid email";
    setFieldErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    try {
      await forgotPassword(email.trim());
      setSent(true);
      toast.success("Check your inbox for the reset link.");
    } catch (err) {
      toast.error(err.message || "Something went wrong");
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
        <p className="font-mono text-[11px] text-slate mb-6">RESET YOUR PASSWORD</p>

        {sent ? (
          <div className="text-center py-4">
            <Mail size={32} className="mx-auto text-urgent mb-3" />
            <p className="text-[13px] text-ink mb-2">
              If an account exists for <strong>{email}</strong>, a reset link has been sent.
            </p>
            <p className="text-[12px] text-slate mb-5">
              The link expires in 30 minutes. Check your spam folder too.
            </p>
            <Link to="/login" className="text-[12.5px] text-urgent font-medium">
              ← Back to sign in
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-col gap-3">
            <p className="text-[12.5px] text-slate">
              Enter your email — we'll send you a link to reset your password.
            </p>
            <div>
              <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">EMAIL</label>
              <input
                type="email"
                className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${fieldErrors.email ? "border-urgent" : "border-hairline"}`}
                placeholder="your.email@campusos.app"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoFocus
              />
              {fieldErrors.email && (
                <p className="text-urgent text-[11px] mt-1">{fieldErrors.email}</p>
              )}
            </div>
            <button
              type="submit"
              disabled={loading}
              className="mt-2 rounded-sm py-2 text-[13px] font-medium text-white bg-[#1B2430] hover:bg-urgent transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading && <span className="w-3.5 h-3.5 border-2 border-white/40 border-t-white rounded-full animate-spin" />}
              {loading ? "Sending…" : "Send reset link"}
            </button>
            <Link to="/login" className="text-[12.5px] text-slate hover:text-urgent text-center mt-2">
              ← Back to sign in
            </Link>
          </form>
        )}
      </div>
    </div>
  );
}