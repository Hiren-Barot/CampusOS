import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { X } from "lucide-react";
import toast from "react-hot-toast";
import Modal from "../common/Modal.jsx";
import { getUsersByRole } from "../../services/userService";

export default function DepartmentForm({ onClose, onSubmit, initialData, mode }) {
  const [name, setName] = useState(initialData?.name || "");
  const [code, setCode] = useState(initialData?.code || "");
  const [hodId, setHodId] = useState(initialData?.hod_id || "");
  const [faculty, setFaculty] = useState([]);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const isEdit = mode === "edit";
  const titleId = "department-form-title";

  useEffect(() => {
    getUsersByRole("faculty")
      .then(setFaculty)
      .catch(() => setFaculty([]));
  }, []);

  function validate() {
    const next = {};
    if (!name.trim()) next.name = "Department name is required";
    if (!code.trim()) next.code = "Department code is required";
    else if (code.length < 2 || code.length > 10) next.code = "Code must be 2-10 characters";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validate()) return;
    setSubmitting(true);
    try {
      await onSubmit({
        name: name.trim(),
        code: code.trim().toUpperCase(),
        hod_id: hodId ? Number(hodId) : null,
      });
      toast.success(isEdit ? "Department updated!" : "Department added!");
      onClose();
    } catch (err) {
      toast.error(err.message || (isEdit ? "Could not update department" : "Could not add department"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Modal titleId={titleId} onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <div className="flex items-center justify-between mb-5">
          <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">{isEdit ? "Edit department" : "Add department"}</span>
          <button type="button" onClick={onClose} aria-label="Close"><X size={16} className="text-slate" /></button>
        </div>
        <div className="flex flex-col gap-3">
          <div>
            <label htmlFor="department-name" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">DEPARTMENT NAME</label>
            <input id="department-name" className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.name ? "border-urgent" : "border-hairline"}`} value={name} onChange={(e) => setName(e.target.value)} />
            {errors.name && <p className="text-urgent text-[11px] mt-1">{errors.name}</p>}
          </div>
          <div>
            <label htmlFor="department-code" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">CODE (2-10 CHARS)</label>
            <input id="department-code" className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised uppercase ${errors.code ? "border-urgent" : "border-hairline"}`} value={code} onChange={(e) => setCode(e.target.value)} maxLength={10} />
            {errors.code && <p className="text-urgent text-[11px] mt-1">{errors.code}</p>}
          </div>
          <div>
            <label htmlFor="department-hod" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">HOD (OPTIONAL)</label>
            <select id="department-hod" className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised" value={hodId} onChange={(e) => setHodId(e.target.value)}>
              <option value="">— No HOD assigned —</option>
              {faculty.map((f) => (
                <option key={f.id} value={f.id}>{f.full_name} ({f.role})</option>
              ))}
            </select>
          </div>
        </div>
        <div className="flex gap-2 mt-6">
          <button type="button" onClick={onClose} className="flex-1 border border-hairline rounded-sm py-2 text-[13px] font-medium text-slate">Cancel</button>
          <button type="submit" disabled={submitting} className="flex-1 rounded-sm py-2 text-[13px] font-medium text-white bg-urgent disabled:opacity-50">{submitting ? "Saving…" : isEdit ? "Update" : "Save"}</button>
        </div>
      </form>
    </Modal>
  );
}

DepartmentForm.propTypes = {
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  initialData: PropTypes.object,
  mode: PropTypes.oneOf(["create", "edit"]),
};

DepartmentForm.defaultProps = {
  initialData: null,
  mode: "create",
};