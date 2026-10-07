import React, { useState } from "react";
import PropTypes from "prop-types";
import { X } from "lucide-react";
import toast from "react-hot-toast";
import Modal from "../common/Modal.jsx";

export default function QueryForm({ onClose, onSubmit }) {
  const titleId = "query-form-title";
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  function validate() {
    const next = {};
    if (!title.trim() || title.trim().length < 3) next.title = "Title must be at least 3 characters";
    if (!description.trim() || description.trim().length < 10)
      next.description = "Description must be at least 10 characters";
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
      });
      toast.success("Query submitted!");
      onClose();
    } catch (err) {
      toast.error(err.message || "Could not submit query");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="560px">
      <form onSubmit={handleSubmit}>
        <div className="flex items-center justify-between mb-5">
          <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">
            Ask a Question
          </span>
          <button type="button" onClick={onClose} aria-label="Close">
            <X size={16} className="text-slate" />
          </button>
        </div>

        <div className="flex flex-col gap-4">
          <div>
            <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              TITLE
            </label>
            <input
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised ${
                errors.title ? "border-urgent" : "border-hairline"
              }`}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Short summary of your question"
            />
            {errors.title && <p className="text-urgent text-[11px] mt-1">{errors.title}</p>}
          </div>

          <div>
            <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              DESCRIPTION
            </label>
            <textarea
              rows={6}
              className={`w-full border rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised resize-y ${
                errors.description ? "border-urgent" : "border-hairline"
              }`}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Explain your question in detail…"
            />
            {errors.description && (
              <p className="text-urgent text-[11px] mt-1">{errors.description}</p>
            )}
          </div>

          <p className="text-[11.5px] text-slate bg-paper rounded-sm px-3 py-2">
            ℹ️ Your query will be sent to faculty and HOD of your department. Only they can see it.
          </p>
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
            {submitting ? "Submitting…" : "Submit Query"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

QueryForm.propTypes = {
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
};