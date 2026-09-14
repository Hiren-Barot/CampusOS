import React, { useState } from "react";
import PropTypes from "prop-types";
import { X } from "lucide-react";
import toast from "react-hot-toast";
import Modal from "../common/Modal.jsx";
import { dateInputToISO, isoToDateInput } from "../../utils/dateUtils";
import useAuth from "../../hooks/useAuth";

export default function AssignmentForm({ onClose, onSubmit, initialData, mode }) {
  const { user } = useAuth();
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(initialData?.description || "");
  const [dueDateInput, setDueDateInput] = useState(isoToDateInput(initialData?.dueDate));
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const isEdit = mode === "edit";
  const titleId = "assignment-form-title";

  function validate() {
    const next = {};
    if (!title.trim()) next.title = "Title is required";
    if (!dueDateInput) next.dueDateInput = "Due date is required";
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
        description: description.trim(),
        dueDate: dateInputToISO(dueDateInput),
        department_id: initialData?.department_id || user?.department_id,
      });
      toast.success(isEdit ? "Assignment updated!" : "Assignment created!");
      onClose();
    } catch (err) {
      toast.error(err.message || (isEdit ? "Could not update assignment" : "Could not create assignment"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Modal titleId={titleId} onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <div className="flex items-center justify-between mb-5">
          <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">{isEdit ? "Edit assignment" : "New assignment"}</span>
          <button type="button" onClick={onClose} aria-label="Close"><X size={16} className="text-slate" /></button>
        </div>
        <div className="flex flex-col gap-3">
          <div>
            <label htmlFor="assignment-title" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">TITLE</label>
            <input id="assignment-title" className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.title ? "border-urgent" : "border-hairline"}`} value={title} onChange={(e) => setTitle(e.target.value)} />
            {errors.title && <p className="text-urgent text-[11px] mt-1">{errors.title}</p>}
          </div>
          <div>
            <label htmlFor="assignment-description" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">DESCRIPTION (OPTIONAL)</label>
            <textarea id="assignment-description" rows={3} className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised resize-none" value={description} onChange={(e) => setDescription(e.target.value)} />
          </div>
          <div>
            <label htmlFor="assignment-due-date" className="font-mono text-[10px] tracking-wide block mb-1 text-slate">DUE DATE</label>
            <input id="assignment-due-date" type="date" className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.dueDateInput ? "border-urgent" : "border-hairline"}`} value={dueDateInput} onChange={(e) => setDueDateInput(e.target.value)} />
            {errors.dueDateInput && <p className="text-urgent text-[11px] mt-1">{errors.dueDateInput}</p>}
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

AssignmentForm.propTypes = {
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  initialData: PropTypes.object,
  mode: PropTypes.oneOf(["create", "edit"]),
};

AssignmentForm.defaultProps = {
  initialData: null,
  mode: "create",
};