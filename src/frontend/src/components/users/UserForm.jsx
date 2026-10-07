import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { X, Copy, Check } from "lucide-react";
import toast from "react-hot-toast";
import Modal from "../common/Modal.jsx";
import useAuth from "../../hooks/useAuth";
import { getDepartments } from "../../services/departmentService";

export default function UserForm({ onClose, onSubmit, roleOptions, initialData, mode }) {
  const { user } = useAuth();
  const isEdit = mode === "edit";
  const titleId = "user-form-title";

  const [name, setName] = useState(initialData?.full_name || initialData?.name || "");
  const [email, setEmail] = useState(initialData?.email || "");
  const [role, setRole] = useState(initialData?.role || roleOptions[0] || "student");
  const [departmentId, setDepartmentId] = useState(initialData?.department_id || user?.department_id || "");
  const [departments, setDepartments] = useState([]);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [tempPassword, setTempPassword] = useState(null);
  const [copied, setCopied] = useState(false);

  const initialProfile = initialData?.profile || {};
  const [profile, setProfile] = useState({
    phone: initialProfile.phone || "",
    gender: initialProfile.gender || "",
    date_of_birth: initialProfile.date_of_birth || "",
    address: initialProfile.address || "",
    enrollment_no: initialProfile.enrollment_no || "",
    course: initialProfile.course || "",
    semester: initialProfile.semester || "",
    admission_year: initialProfile.admission_year || "",
    parent_name: initialProfile.parent_name || "",
    parent_phone: initialProfile.parent_phone || "",
    qualification: initialProfile.qualification || "",
    specialization: initialProfile.specialization || "",
    experience_years: initialProfile.experience_years || "",
    joining_date: initialProfile.joining_date || "",
    designation: initialProfile.designation || "",
  });

  const showDepartmentSelector = user?.role === "admin" || user?.role === "principal";
  const isStudent = role === "student";
  const isFacultyRole = ["faculty", "hod", "principal"].includes(role);

  useEffect(() => {
    if (showDepartmentSelector) {
      getDepartments().then(setDepartments).catch(() => setDepartments([]));
    }
  }, [showDepartmentSelector]);

  function updateProfile(key, value) {
    setProfile((p) => ({ ...p, [key]: value }));
  }

  function validate() {
    const next = {};
    if (!name.trim()) next.name = "Name is required";
    if (!email.trim()) next.email = "Email is required";
    else if (!/^\S+@\S+\.\S+$/.test(email.trim())) next.email = "Enter a valid email";
    if (showDepartmentSelector && !isStudent && role !== "admin" && role !== "principal" && !departmentId) {
      next.departmentId = "Department is required";
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validate()) return;
    setSubmitting(true);

    try {
      const filteredProfile = {};
      Object.keys(profile).forEach((key) => {
        if (profile[key] !== "" && profile[key] !== null && profile[key] !== undefined) {
          filteredProfile[key] = profile[key];
        }
      });

      const result = await onSubmit({
        name: name.trim(),
        email: email.trim().toLowerCase(),
        role,
        department_id: departmentId ? Number(departmentId) : null,
        profile: Object.keys(filteredProfile).length > 0 ? filteredProfile : null,
      });

      if (!isEdit && result?.temp_password) {
        setTempPassword(result.temp_password);
        toast.success("User created! Email sent.");
      } else {
        toast.success(isEdit ? "User updated!" : "User added!");
        onClose();
      }
    } catch (err) {
      toast.error(err.message || "Could not save user");
    } finally {
      setSubmitting(false);
    }
  }

  function copyPassword() {
    navigator.clipboard.writeText(tempPassword);
    setCopied(true);
    toast.success("Password copied!");
    setTimeout(() => setCopied(false), 2000);
  }

  if (tempPassword) {
    return (
      <Modal titleId={titleId} onClose={onClose}>
        <div className="flex items-center justify-between mb-5">
          <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">
            ✅ User Created
          </span>
          <button type="button" onClick={onClose} aria-label="Close">
            <X size={16} className="text-slate" />
          </button>
        </div>

        <p className="text-[13px] text-ink mb-4">
          Welcome email sent to <strong>{email}</strong>.
        </p>

        <div className="bg-paper border border-hairline rounded-sm px-3 py-3 flex items-center justify-between mb-4">
          <span className="font-mono text-[14px] text-ink select-all">{tempPassword}</span>
          <button
            type="button"
            onClick={copyPassword}
            className="text-urgent hover:opacity-70 flex items-center gap-1 font-mono text-[11px]"
          >
            {copied ? <Check size={14} /> : <Copy size={14} />}
            {copied ? "Copied" : "Copy"}
          </button>
        </div>

        <p className="font-mono text-[10.5px] text-slate bg-paper rounded-sm px-3 py-2 mb-4">
          🔐 Backup password — only share if user didn't receive email
        </p>

        <button
          onClick={onClose}
          className="w-full rounded-sm py-2 text-[13px] font-medium text-white bg-urgent"
        >
          Done
        </button>
      </Modal>
    );
  }

  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="600px">
      <form onSubmit={handleSubmit}>
        <div className="flex items-center justify-between mb-5">
          <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">
            {isEdit ? "Edit User" : "Add User"}
          </span>
          <button type="button" onClick={onClose} aria-label="Close">
            <X size={16} className="text-slate" />
          </button>
        </div>

        <div className="flex flex-col gap-4 max-h-[65vh] overflow-y-auto pr-1">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">FULL NAME</label>
              <input
                className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.name ? "border-urgent" : "border-hairline"}`}
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
              {errors.name && <p className="text-urgent text-[11px] mt-1">{errors.name}</p>}
            </div>
            <div>
              <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">EMAIL</label>
              <input
                type="email"
                className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.email ? "border-urgent" : "border-hairline"}`}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              {errors.email && <p className="text-urgent text-[11px] mt-1">{errors.email}</p>}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">ROLE</label>
              <select
                disabled={isEdit}
                className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised capitalize disabled:opacity-60"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                {roleOptions.map((r) => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>

            {showDepartmentSelector && role !== "admin" && role !== "principal" && (
              <div>
                <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">DEPARTMENT</label>
                <select
                  className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.departmentId ? "border-urgent" : "border-hairline"}`}
                  value={departmentId}
                  onChange={(e) => setDepartmentId(e.target.value)}
                >
                  <option value="">— Select —</option>
                  {departments.map((d) => (
                    <option key={d.id} value={d.id}>{d.name} ({d.code})</option>
                  ))}
                </select>
                {errors.departmentId && <p className="text-urgent text-[11px] mt-1">{errors.departmentId}</p>}
              </div>
            )}
          </div>

          <div className="border-t border-hairline pt-4">
            <p className="font-mono text-[10.5px] tracking-wide text-slate mb-3">PERSONAL INFORMATION</p>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">PHONE</label>
                <input
                  className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                  value={profile.phone}
                  onChange={(e) => updateProfile("phone", e.target.value)}
                  placeholder="+91 98765 43210"
                />
              </div>
              <div>
                <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">GENDER</label>
                <select
                  className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                  value={profile.gender}
                  onChange={(e) => updateProfile("gender", e.target.value)}
                >
                  <option value="">— Select —</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">DATE OF BIRTH</label>
                <input
                  type="date"
                  className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                  value={profile.date_of_birth}
                  onChange={(e) => updateProfile("date_of_birth", e.target.value)}
                />
              </div>
              <div>
                <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">ADDRESS</label>
                <input
                  className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                  value={profile.address}
                  onChange={(e) => updateProfile("address", e.target.value)}
                  placeholder="Ahmedabad, Gujarat"
                />
              </div>
            </div>
          </div>

          {isStudent && (
            <div className="border-t border-hairline pt-4">
              <p className="font-mono text-[10.5px] tracking-wide text-slate mb-3">STUDENT DETAILS</p>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">ENROLLMENT NO</label>
                  <input
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.enrollment_no}
                    onChange={(e) => updateProfile("enrollment_no", e.target.value)}
                    placeholder="22CE001"
                  />
                </div>
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">COURSE</label>
                  <input
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.course}
                    onChange={(e) => updateProfile("course", e.target.value)}
                    placeholder="Computer Engineering"
                  />
                </div>
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">SEMESTER</label>
                  <input
                    type="number"
                    min="1"
                    max="12"
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.semester}
                    onChange={(e) => updateProfile("semester", e.target.value)}
                  />
                </div>
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">ADMISSION YEAR</label>
                  <input
                    type="number"
                    min="2000"
                    max="2100"
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.admission_year}
                    onChange={(e) => updateProfile("admission_year", e.target.value)}
                  />
                </div>
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">PARENT NAME</label>
                  <input
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.parent_name}
                    onChange={(e) => updateProfile("parent_name", e.target.value)}
                  />
                </div>
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">PARENT PHONE</label>
                  <input
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.parent_phone}
                    onChange={(e) => updateProfile("parent_phone", e.target.value)}
                    placeholder="+91 98765 43210"
                  />
                </div>
              </div>
            </div>
          )}

          {isFacultyRole && (
            <div className="border-t border-hairline pt-4">
              <p className="font-mono text-[10.5px] tracking-wide text-slate mb-3">FACULTY DETAILS</p>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">QUALIFICATION</label>
                  <input
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.qualification}
                    onChange={(e) => updateProfile("qualification", e.target.value)}
                    placeholder="M.Tech, PhD"
                  />
                </div>
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">SPECIALIZATION</label>
                  <input
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.specialization}
                    onChange={(e) => updateProfile("specialization", e.target.value)}
                    placeholder="AI/ML, DBMS"
                  />
                </div>
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">EXPERIENCE (YEARS)</label>
                  <input
                    type="number"
                    min="0"
                    max="60"
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.experience_years}
                    onChange={(e) => updateProfile("experience_years", e.target.value)}
                  />
                </div>
                <div>
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">JOINING DATE</label>
                  <input
                    type="date"
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.joining_date}
                    onChange={(e) => updateProfile("joining_date", e.target.value)}
                  />
                </div>
                <div className="col-span-2">
                  <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">DESIGNATION</label>
                  <input
                    className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                    value={profile.designation}
                    onChange={(e) => updateProfile("designation", e.target.value)}
                    placeholder="Assistant Professor, HOD, Principal"
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="flex gap-2 mt-6">
          <button type="button" onClick={onClose} className="flex-1 border border-hairline rounded-sm py-2 text-[13px] font-medium text-slate">
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="flex-1 rounded-sm py-2 text-[13px] font-medium text-white bg-urgent disabled:opacity-50"
          >
            {submitting ? "Saving…" : isEdit ? "Update" : "Save"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

UserForm.propTypes = {
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  roleOptions: PropTypes.arrayOf(PropTypes.string),
  initialData: PropTypes.object,
  mode: PropTypes.oneOf(["create", "edit"]),
};

UserForm.defaultProps = {
  roleOptions: ["student"],
  initialData: null,
  mode: "create",
};