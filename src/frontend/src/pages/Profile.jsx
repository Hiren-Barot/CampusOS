import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { KeyRound } from "lucide-react";
import toast from "react-hot-toast";
import useAuth from "../hooks/useAuth";
import { updateUser } from "../services/userService";

const PERSONAL_FIELDS = [
  { key: "phone", label: "PHONE", placeholder: "+91 98765 43210" },
  { key: "gender", label: "GENDER", type: "select", options: ["Male", "Female", "Other"] },
  { key: "date_of_birth", label: "DATE OF BIRTH", type: "date" },
  { key: "address", label: "ADDRESS", placeholder: "Ahmedabad, Gujarat" },
];

const STUDENT_FIELDS = [
  { key: "enrollment_no", label: "ENROLLMENT NO", placeholder: "22CE001" },
  { key: "course", label: "COURSE", placeholder: "Computer Engineering" },
  { key: "semester", label: "SEMESTER", type: "number", min: 1, max: 12 },
  { key: "admission_year", label: "ADMISSION YEAR", type: "number", min: 2000, max: 2100 },
  { key: "parent_name", label: "PARENT NAME" },
  { key: "parent_phone", label: "PARENT PHONE", placeholder: "+91 98765 43210" },
];

const FACULTY_FIELDS = [
  { key: "qualification", label: "QUALIFICATION", placeholder: "M.Tech, PhD" },
  { key: "specialization", label: "SPECIALIZATION", placeholder: "AI/ML, DBMS" },
  { key: "experience_years", label: "EXPERIENCE (YEARS)", type: "number", min: 0, max: 60 },
  { key: "joining_date", label: "JOINING DATE", type: "date" },
  { key: "designation", label: "DESIGNATION", placeholder: "Assistant Professor" },
];

const NUMERIC_KEYS = ["semester", "admission_year", "experience_years"];

function buildProfileState(user) {
  const p = user?.profile || {};
  return {
    phone: p.phone || "",
    gender: p.gender || "",
    date_of_birth: p.date_of_birth || "",
    address: p.address || "",
    enrollment_no: p.enrollment_no || "",
    course: p.course || "",
    semester: p.semester ?? "",
    admission_year: p.admission_year ?? "",
    parent_name: p.parent_name || "",
    parent_phone: p.parent_phone || "",
    qualification: p.qualification || "",
    specialization: p.specialization || "",
    experience_years: p.experience_years ?? "",
    joining_date: p.joining_date || "",
    designation: p.designation || "",
  };
}

export default function Profile() {
  const { user, updateProfile } = useAuth();

  const [name, setName] = useState("");
  const [profile, setProfile] = useState({});
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [loadedUserId, setLoadedUserId] = useState(null);

  useEffect(() => {
    if (!user) return;
    if (loadedUserId === user.id) return;
    setName(user.full_name || user.name || "");
    setProfile(buildProfileState(user));
    setLoadedUserId(user.id);
  }, [user, loadedUserId]);

  if (!user) {
    return <div className="text-slate text-[13px]">Loading profile…</div>;
  }

  const role = (user.role || "").toLowerCase();
  const isStudent = role === "student";
  const isFacultyRole = ["faculty", "hod", "principal"].includes(role);

  function updateField(key, value) {
    setProfile((p) => ({ ...p, [key]: value }));
  }

  function buildProfilePayload() {
    const out = {};
    const keysToSend = [
      ...PERSONAL_FIELDS.map((f) => f.key),
      ...(isStudent ? STUDENT_FIELDS.map((f) => f.key) : []),
      ...(isFacultyRole ? FACULTY_FIELDS.map((f) => f.key) : []),
    ];
    keysToSend.forEach((k) => {
      const val = profile[k];
      if (val === "" || val === null || val === undefined) {
        out[k] = null;
      } else if (NUMERIC_KEYS.includes(k)) {
        out[k] = Number(val);
      } else {
        out[k] = val;
      }
    });
    return out;
  }

  async function handleSave() {
    setError("");
    if (!name.trim()) {
      setError("Name cannot be empty");
      return;
    }
    setSaving(true);
    try {
      const payload = {
        full_name: name.trim(),
        profile: buildProfilePayload(),
      };

      const updated = await updateUser(user.id, payload);

      updateProfile({
        full_name: name.trim(),
        name: name.trim(),
        profile: updated?.profile || payload.profile,
      });

      toast.success("Profile updated!");
    } catch (err) {
      const message = err.message || "Could not save changes";
      setError(message);
      toast.error(message);
    } finally {
      setSaving(false);
    }
  }

  function handleReset() {
    if (!user) return;
    setName(user.full_name || user.name || "");
    setProfile(buildProfileState(user));
    setError("");
    toast.success("Reverted changes");
  }

  return (
    <div>
      <h1 className="font-serif text-[26px] font-semibold text-ink mb-6">Profile</h1>

      <div className="bg-paper-raised border border-hairline rounded-sm max-w-[640px] p-5 flex flex-col gap-5">
        {error && (
          <div className="text-[12.5px] text-urgent bg-urgent/10 rounded-sm px-3 py-2">
            {error}
          </div>
        )}

        <div className="flex flex-col gap-3">
          <p className="font-mono text-[10.5px] tracking-wide text-slate">ACCOUNT</p>

          <div className="grid grid-cols-2 gap-3">
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
                value={user.email || ""}
                disabled
              />
            </div>
            <div>
              <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">DEPARTMENT</label>
              <input
                className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper"
                value={user.department_name || user.dept || "—"}
                disabled
              />
            </div>
            <div>
              <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">ROLE</label>
              <input
                className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper capitalize"
                value={user.role || ""}
                disabled
              />
            </div>
          </div>

          <div className="pt-2">
            <Link
              to="/change-password"
              className="inline-flex items-center gap-2 text-[12.5px] font-medium text-urgent hover:opacity-70"
            >
              <KeyRound size={14} />
              Change Password →
            </Link>
          </div>
        </div>

        <div className="border-t border-hairline pt-4 flex flex-col gap-3">
          <p className="font-mono text-[10.5px] tracking-wide text-slate">PERSONAL INFORMATION</p>
          <div className="grid grid-cols-2 gap-3">
            {PERSONAL_FIELDS.map((f) => (
              <FieldInput
                key={f.key}
                field={f}
                value={profile[f.key]}
                onChange={(v) => updateField(f.key, v)}
              />
            ))}
          </div>
        </div>

        {isStudent && (
          <div className="border-t border-hairline pt-4 flex flex-col gap-3">
            <p className="font-mono text-[10.5px] tracking-wide text-slate">STUDENT DETAILS</p>
            <div className="grid grid-cols-2 gap-3">
              {STUDENT_FIELDS.map((f) => (
                <FieldInput
                  key={f.key}
                  field={f}
                  value={profile[f.key]}
                  onChange={(v) => updateField(f.key, v)}
                />
              ))}
            </div>
          </div>
        )}

        {isFacultyRole && (
          <div className="border-t border-hairline pt-4 flex flex-col gap-3">
            <p className="font-mono text-[10.5px] tracking-wide text-slate">FACULTY DETAILS</p>
            <div className="grid grid-cols-2 gap-3">
              {FACULTY_FIELDS.map((f) => (
                <FieldInput
                  key={f.key}
                  field={f}
                  value={profile[f.key]}
                  onChange={(v) => updateField(f.key, v)}
                />
              ))}
            </div>
          </div>
        )}

        <div className="flex items-center gap-2 mt-2">
          <button
            onClick={handleSave}
            disabled={saving}
            className="rounded-sm py-2 text-[13px] font-medium text-white px-5 bg-[#1B2430] disabled:opacity-50 flex items-center gap-2"
          >
            {saving && (
              <span className="w-3.5 h-3.5 border-2 border-white/40 border-t-white rounded-full animate-spin" />
            )}
            {saving ? "Saving…" : "Save changes"}
          </button>
          <button
            type="button"
            onClick={handleReset}
            disabled={saving}
            className="rounded-sm py-2 text-[13px] font-medium text-slate border border-hairline px-5 hover:bg-paper disabled:opacity-50"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

function FieldInput({ field, value, onChange }) {
  return (
    <div>
      <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
        {field.label}
      </label>
      {field.type === "select" ? (
        <select
          className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
          value={value ?? ""}
          onChange={(e) => onChange(e.target.value)}
        >
          <option value="">— Select —</option>
          {field.options.map((o) => (
            <option key={o} value={o}>{o}</option>
          ))}
        </select>
      ) : (
        <input
          type={field.type || "text"}
          min={field.min}
          max={field.max}
          placeholder={field.placeholder || ""}
          className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
          value={value ?? ""}
          onChange={(e) => onChange(e.target.value)}
        />
      )}
    </div>
  );
}