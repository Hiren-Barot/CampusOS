import React, { useState } from "react";
import PropTypes from "prop-types";
import { X, Upload, FileText } from "lucide-react";
import toast from "react-hot-toast";
import Modal from "../common/Modal.jsx";

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ALLOWED_EXT = [".pdf", ".ppt", ".pptx", ".doc", ".docx", ".jpg", ".jpeg", ".png"];

export default function AssignmentForm({ onClose, onSubmit, initialData, mode }) {
  const isEdit = mode === "edit";
  const titleId = "assignment-form-title";

  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(initialData?.description || "");
  const [deadline, setDeadline] = useState(
    initialData?.deadline ? initialData.deadline.slice(0, 16) : ""
  );
  const [file, setFile] = useState(null);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  function handleFileChange(e) {
    const f = e.target.files?.[0];
    if (!f) {
      setFile(null);
      return;
    }
    const ext = "." + f.name.split(".").pop().toLowerCase();
    if (!ALLOWED_EXT.includes(ext)) {
      toast.error(`File type ${ext} not allowed`);
      e.target.value = "";
      return;
    }
    if (f.size > MAX_FILE_SIZE) {
      toast.error(`File too large (${(f.size / 1024 / 1024).toFixed(1)} MB). Max 10 MB.`);
      e.target.value = "";
      return;
    }
    setFile(f);
  }

  function validate() {
    const next = {};
    if (!title.trim()) next.title = "Title is required";
    if (!deadline) next.deadline = "Deadline is required";
    else if (new Date(deadline) <= new Date()) next.deadline = "Deadline must be in the future";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validate()) return;
    setSubmitting(true);

    try {
      const deadlineISO = deadline.length === 16 ? `${deadline}:00` : deadline;

      const payload = {
        title: title.trim(),
        description: description.trim(),
        deadline: deadlineISO,
      };

      if (!isEdit && file) payload.file = file;

      await onSubmit(payload);
      toast.success(isEdit ? "Assignment updated!" : "Assignment created!");
      onClose();
    } catch (err) {
      toast.error(err.message || "Could not save assignment");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="600px">
      <form onSubmit={handleSubmit}>
        <div className="flex items-center justify-between mb-5">
          <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">
            {isEdit ? "Edit Assignment" : "New Assignment"}
          </span>
          <button type="button" onClick={onClose} aria-label="Close">
            <X size={16} className="text-slate" />
          </button>
        </div>

        <div className="flex flex-col gap-4 max-h-[65vh] overflow-y-auto pr-1">
          <div>
            <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              TITLE
            </label>
            <input
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.title ? "border-urgent" : "border-hairline"}`}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. DBMS Assignment 3"
            />
            {errors.title && <p className="text-urgent text-[11px] mt-1">{errors.title}</p>}
          </div>

          <div>
            <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              DESCRIPTION
            </label>
            <textarea
              rows={4}
              className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised resize-y"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Instructions for students…"
            />
          </div>

          <div>
            <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              DEADLINE
            </label>
            <input
              type="datetime-local"
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${errors.deadline ? "border-urgent" : "border-hairline"}`}
              value={deadline}
              onChange={(e) => setDeadline(e.target.value)}
            />
            {errors.deadline && <p className="text-urgent text-[11px] mt-1">{errors.deadline}</p>}
          </div>

          {!isEdit && (
            <div className="border-t border-hairline pt-4">
              <label className="font-mono text-[10px] tracking-wide block mb-2 text-slate">
                ATTACHMENT (OPTIONAL)
              </label>

              {!file ? (
                <label className="flex items-center gap-2 border border-dashed border-hairline rounded-sm px-4 py-3 cursor-pointer hover:bg-paper text-[13px] text-slate">
                  <Upload size={16} />
                  <span>Choose file (PDF, PPT, DOCX, JPG, PNG — max 10 MB)</span>
                  <input
                    type="file"
                    className="hidden"
                    accept=".pdf,.ppt,.pptx,.doc,.docx,.jpg,.jpeg,.png"
                    onChange={handleFileChange}
                  />
                </label>
              ) : (
                <div className="flex items-center justify-between border border-hairline rounded-sm px-3 py-2 bg-paper">
                  <div className="flex items-center gap-2 text-[13px] text-ink">
                    <FileText size={16} className="text-urgent" />
                    <span className="truncate max-w-[300px]">{file.name}</span>
                    <span className="text-slate text-[11px]">
                      ({(file.size / 1024).toFixed(0)} KB)
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => setFile(null)}
                    className="text-urgent hover:opacity-70"
                  >
                    <X size={14} />
                  </button>
                </div>
              )}
            </div>
          )}

          {isEdit && initialData?.has_file && (
            <div className="border-t border-hairline pt-4">
              <p className="font-mono text-[10.5px] tracking-wide text-slate">
                FILE: {initialData.file_name} (existing — not editable)
              </p>
            </div>
          )}
        </div>

        <div className="flex gap-2 mt-6">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 border border-hairline rounded-sm py-2 text-[13px] font-medium text-slate"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="flex-1 rounded-sm py-2 text-[13px] font-medium text-white bg-urgent disabled:opacity-50"
          >
            {submitting ? "Saving…" : isEdit ? "Update" : "Create"}
          </button>
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