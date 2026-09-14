import React from "react";
import PropTypes from "prop-types";
import { X } from "lucide-react";
import Modal from "../common/Modal.jsx";
import { shortDate } from "../../utils/dateUtils";

export default function AssignmentDetails({ assignment, onClose }) {
  if (!assignment) return null;
  const titleId = "assignment-details-title";
  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="420px">
      <div className="flex items-center justify-between mb-4">
        <span className="font-mono text-[10px] text-slate tracking-wide">{`DUE ${shortDate(assignment.dueDate)}`}</span>
        <button type="button" onClick={onClose} aria-label="Close"><X size={16} className="text-slate" /></button>
      </div>
      <h3 id={titleId} className="font-serif text-[19px] font-semibold text-ink mb-2">{assignment.title}</h3>
      <p className="font-mono text-[11px] text-slate mb-3">{`Assigned by ${assignment.by}`}</p>
      {assignment.description && <p className="text-[13px] text-ink whitespace-pre-wrap">{assignment.description}</p>}
    </Modal>
  );
}

AssignmentDetails.propTypes = {
  assignment: PropTypes.object,
  onClose: PropTypes.func.isRequired,
};

AssignmentDetails.defaultProps = { assignment: null };