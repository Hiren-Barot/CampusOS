import React from "react";
import { useState } from "react";
import toast from "react-hot-toast";
import useAuth from "../hooks/useAuth";
import { updateUser } from "../services/userService";

export default function Profile() {
  const { user, updateProfile } = useAuth();
  const [name, setName] = useState(user?.full_name || user?.name || "");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  async function handleSave() {
    setError("");
    if (!name.trim()) {
      setError("Name cannot be empty");
      return;
    }
    setSaving(true);
    try {
      const updates = { name: name.trim() };
      await updateUser(user.id, updates);

      updateProfile({ full_name: name.trim(), name: name.trim() });
      toast.success("Profile updated!");
    } catch (err) {
      const message = err.message || "Could not save changes";
      setError(message);
      toast.error(message);
    } finally {
      setSaving(false);
    }
  }

  const displayName = user?.full_name || user?.name || "—";
  const displayDept = user?.department_name || user?.dept || "—";

  return (
    <div>
      <h1 className="font-serif text-[26px] font-semibold text-ink mb-6">Profile</h1>

      <div className="bg-paper-raised border border-hairline rounded-sm max-w-[440px] p-5 flex flex-col gap-3">
        {error && (
          <div className="text-[12.5px] text-urgent bg-urgent/10 rounded-sm px-3 py-2">{error}</div>
        )}
        <div>
          <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">NAME</label>
          <input
            className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div>
          <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">EMAIL</label>
          <input
            className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper"
            value={user?.email || ""}
            disabled
          />
        </div>
        <div>
          <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">DEPARTMENT</label>
          <input
            className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper"
            value={displayDept}
            disabled
          />
        </div>
        <div>
          <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">ROLE</label>
          <input
            className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper capitalize"
            value={user?.role || ""}
            disabled
          />
        </div>
        <button
          onClick={handleSave}
          disabled={saving}
          className="mt-2 rounded-sm py-2 text-[13px] font-medium text-white w-fit px-5 bg-[#1B2430] disabled:opacity-50 flex items-center gap-2"
        >
          {saving && <span className="w-3.5 h-3.5 border-2 border-white/40 border-t-white rounded-full animate-spin" />}
          {saving ? "Saving…" : "Save changes"}
        </button>
      </div>
    </div>
  );
}