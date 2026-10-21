import React from "react";
import PropTypes from "prop-types";
import { X } from "lucide-react";
import { shortDate } from "../../utils/dateUtils";
import Modal from "../common/Modal.jsx";

export default function AssignmentDetails({ assignment, onClose }) {
  if (!assignment) return null;
  
  const rawDate = assignment.dueDate || assignment.deadline;
  const authorName = assignment.by || assignment.faculty_name || "Unknown";
  const description = assignment.description || "No description provided.";
  const titleId = "assignment-details-title";

  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="420px">
      <div className="flex items-center justify-between mb-4">
        <span className="font-mono text-[10px] text-event tracking-wide">
          DUE {shortDate(rawDate)}
        </span>
        <button onClick={onClose} aria-label="Close">
          <X size={16} className="text-slate" />
        </button>
      </div>
      
      <h3 id={titleId} className="font-serif text-[19px] font-semibold text-ink mb-2">
        {assignment.title}
      </h3>
      
      <p className="font-mono text-[11px] text-slate mb-4">
        Assigned by {authorName}
      </p>
      
      {description && (
        <p className="text-[13px] text-ink leading-relaxed bg-paper p-3 rounded-sm border border-hairline max-h-[200px] overflow-y-auto">
          {description}
        </p>
      )}
    </Modal>
  );
}

AssignmentDetails.propTypes = {
  assignment: PropTypes.shape({
    title: PropTypes.string,
    dueDate: PropTypes.string,
    deadline: PropTypes.string,
    by: PropTypes.string,
    faculty_name: PropTypes.string,
    description: PropTypes.string,
  }),
  onClose: PropTypes.func.isRequired,
};

AssignmentDetails.defaultProps = {
  assignment: null,
};