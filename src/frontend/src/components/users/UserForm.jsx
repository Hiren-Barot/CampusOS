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

  const showDepartmentSelector = user?.role === "admin" || user?.role === "principal";

  useEffect(() => {
    if (showDepartmentSelector) {
      getDepartments().then(setDepartments).catch(() => setDepartments([]));
    }
  }, [showDepartmentSelector]);

  function validate() {
    const next = {};
    if (!name.trim()) next.name = "Name is required";
    if (!email.trim()) next.email = "Email is required";
    else if (!/^\S+@\S+\.\S+$/.test(email.trim())) next.email = "Enter a valid email";
    if (showDepartmentSelector && role !== "admin" && role !== "principal" && !departmentId) {
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
    const result = await onSubmit({
      name: name.trim(),
      email: email.trim().toLowerCase(),
      role,
      department_id: departmentId ? Number(departmentId) : null,
    });

    if (!isEdit && result?.temp_password) {
      setTempPassword(result.temp_password);
      toast.success("User created!");
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
            User created
          </span>
          <button type="button" onClick={onClose} aria-label="Close">
            <X size={16} className="text-slate" />
          </button>
        </div>

        <p className="text-[13px] text-ink mb-4">
          Share this temporary password with <strong>{name}</strong>.
          They will be able to change it after first login.
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

        <div className="bg-urgent/5 border border-hairline rounded-sm px-3 py-2 mb-4">
          <p className="font-mono text-[10.5px] text-slate">
            <strong className="text-ink">Email:</strong> {email}
          </p>
        </div>

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
    <Modal titleId={titleId} onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <div className="flex items-center justify-between mb-5">
          <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">
            {isEdit ? "Edit user" : "Add user"}
          </span>
          <button type="button" onClick={onClose} aria-label="Close">
            <X size={16} className="text-slate" />
          </button>
        </div>

        <div className="flex flex-col gap-3">
          <div>
            <label htmlFor="user-name" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              NAME
            </label>
            <input
              id="user-name"
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.name ? "border-urgent" : "border-hairline"}`}
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            {errors.name && <p className="text-urgent text-[11px] mt-1">{errors.name}</p>}
          </div>

          <div>
            <label htmlFor="user-email" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              EMAIL
            </label>
            <input
              id="user-email"
              type="email"
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.email ? "border-urgent" : "border-hairline"}`}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            {errors.email && <p className="text-urgent text-[11px] mt-1">{errors.email}</p>}
          </div>

          <div>
            <label htmlFor="user-role" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              ROLE
            </label>
            <select
              id="user-role"
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
              <label htmlFor="user-department" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
                DEPARTMENT
              </label>
              <select
                id="user-department"
                className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.departmentId ? "border-urgent" : "border-hairline"}`}
                value={departmentId}
                onChange={(e) => setDepartmentId(e.target.value)}
              >
                <option value="">— Select department —</option>
                {departments.map((d) => (
                  <option key={d.id} value={d.id}>{d.name} ({d.code})</option>
                ))}
              </select>
              {errors.departmentId && <p className="text-urgent text-[11px] mt-1">{errors.departmentId}</p>}
            </div>
          )}

          {!isEdit && (
            <p className="font-mono text-[10.5px] text-slate bg-paper rounded-sm px-3 py-2">
              A temporary password will be auto-generated and shown after saving.
            </p>
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