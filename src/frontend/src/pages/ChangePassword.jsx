import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import useAuth from "../hooks/useAuth";
import { changePassword } from "../services/authService";

export default function ChangePassword() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  function validate() {
    const next = {};
    if (!currentPassword) next.currentPassword = "Current password is required";
    if (!newPassword) next.newPassword = "New password is required";
    else if (newPassword.length < 6) next.newPassword = "Must be at least 6 characters";
    if (newPassword !== confirmPassword) next.confirmPassword = "Passwords do not match";
    if (currentPassword && newPassword && currentPassword === newPassword) {
      next.newPassword = "New password must be different from current";
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    try {
      await changePassword(currentPassword, newPassword);
      toast.success("Password changed successfully!");
      // Logout and force re-login with new password
      setTimeout(() => {
        logout();
        navigate("/login");
      }, 1500);
    } catch (err) {
      toast.error(err.message || "Could not change password");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="font-serif text-[26px] font-semibold text-ink mb-6">Change Password</h1>

      <div className="bg-paper-raised border border-hairline rounded-sm max-w-[440px] p-5 flex flex-col gap-3">
        <div className="bg-urgent/5 border border-urgent/20 rounded-sm px-3 py-2 mb-2">
          <p className="font-mono text-[10.5px] text-slate">
            ⚠️ You will be logged out after changing your password. Use your new password to log in.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <div>
            <label htmlFor="current-password" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              CURRENT PASSWORD
            </label>
            <input
              id="current-password"
              type="password"
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.currentPassword ? "border-urgent" : "border-hairline"}`}
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              autoFocus
            />
            {errors.currentPassword && <p className="text-urgent text-[11px] mt-1">{errors.currentPassword}</p>}
          </div>

          <div>
            <label htmlFor="new-password" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              NEW PASSWORD
            </label>
            <input
              id="new-password"
              type="password"
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.newPassword ? "border-urgent" : "border-hairline"}`}
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
            {errors.newPassword && <p className="text-urgent text-[11px] mt-1">{errors.newPassword}</p>}
            <p className="font-mono text-[10px] text-slate mt-1">Minimum 6 characters</p>
          </div>

          <div>
            <label htmlFor="confirm-password" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              CONFIRM NEW PASSWORD
            </label>
            <input
              id="confirm-password"
              type="password"
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.confirmPassword ? "border-urgent" : "border-hairline"}`}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            {errors.confirmPassword && <p className="text-urgent text-[11px] mt-1">{errors.confirmPassword}</p>}
          </div>

          <div className="flex gap-2 mt-3">
            <button
              type="button"
              onClick={() => navigate("/profile")}
              className="flex-1 border border-hairline rounded-sm py-2 text-[13px] font-medium text-slate"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 rounded-sm py-2 text-[13px] font-medium text-white bg-urgent disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading && <span className="w-3.5 h-3.5 border-2 border-white/40 border-t-white rounded-full animate-spin" />}
              {loading ? "Changing…" : "Change Password"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}