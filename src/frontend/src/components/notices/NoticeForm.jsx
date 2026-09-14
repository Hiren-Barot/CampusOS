import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { X } from "lucide-react";
import toast from "react-hot-toast";
import Modal from "../common/Modal.jsx";
import useAuth from "../../hooks/useAuth";
import { getDepartments } from "../../services/departmentService";

export default function NoticeForm({ onClose, onSubmit, initialData, mode }) {
  const { user } = useAuth();
  const isEdit = mode === "edit";
  const titleId = "notice-form-title";

  const [title, setTitle] = useState(initialData?.title || "");
  const [content, setContent] = useState(initialData?.content || "");
  const [departmentId, setDepartmentId] = useState(
    initialData?.department_id ?? (user?.department_id || "")
  );
  const [departments, setDepartments] = useState([]);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const canChooseDepartment = user?.role === "admin" || user?.role === "principal";

  useEffect(() => {
    if (canChooseDepartment) {
      getDepartments().then(setDepartments).catch(() => setDepartments([]));
    }
  }, [canChooseDepartment]);

  function validate() {
    const next = {};
    if (!title.trim()) next.title = "Title is required";
    if (!content.trim()) next.content = "Content is required";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validate()) return;
    setSubmitting(true);
    try {
      await onSubmit({
        title: title.trim(),
        content: content.trim(),
        department_id: departmentId ? Number(departmentId) : null,
      });
      toast.success(isEdit ? "Notice updated!" : "Notice posted!");
      onClose();
    } catch (err) {
      toast.error(err.message || "Could not save notice");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Modal titleId={titleId} onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <div className="flex items-center justify-between mb-5">
          <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">
            {isEdit ? "Edit notice" : "New notice"}
          </span>
          <button type="button" onClick={onClose} aria-label="Close">
            <X size={16} className="text-slate" />
          </button>
        </div>

        <div className="flex flex-col gap-3">
          {canChooseDepartment && (
            <div>
              <label htmlFor="notice-department" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
                DEPARTMENT
              </label>
              <select
                id="notice-department"
                className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised"
                value={departmentId}
                onChange={(e) => setDepartmentId(e.target.value)}
              >
                <option value="">— All Departments —</option>
                {departments.map((d) => (
                  <option key={d.id} value={d.id}>{d.name} ({d.code})</option>
                ))}
              </select>
              <p className="font-mono text-[10px] text-slate mt-1">
                Leave empty to send to ALL departments
              </p>
            </div>
          )}

          <div>
            <label htmlFor="notice-title" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              TITLE
            </label>
            <input
              id="notice-title"
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.title ? "border-urgent" : "border-hairline"}`}
              placeholder="e.g. Library closed on Sunday"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            {errors.title && <p className="text-urgent text-[11px] mt-1">{errors.title}</p>}
          </div>

          <div>
            <label htmlFor="notice-content" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              CONTENT
            </label>
            <textarea
              id="notice-content"
              rows={4}
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised resize-none ${errors.content ? "border-urgent" : "border-hairline"}`}
              placeholder="Write the notice content here…"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
            {errors.content && <p className="text-urgent text-[11px] mt-1">{errors.content}</p>}
          </div>
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

NoticeForm.propTypes = {
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  initialData: PropTypes.object,
  mode: PropTypes.oneOf(["create", "edit"]),
};

NoticeForm.defaultProps = {
  initialData: null,
  mode: "create",
};