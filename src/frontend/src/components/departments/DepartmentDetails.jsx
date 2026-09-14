import React from "react";
import PropTypes from "prop-types";
import { X } from "lucide-react";
import Modal from "../common/Modal.jsx";

export default function DepartmentDetails({ department, onClose }) {
  if (!department) return null;
  const titleId = "department-details-title";
  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="420px">
      <div className="flex items-center justify-between mb-4">
        <span className="font-mono text-[10px] text-slate tracking-wide">DEPARTMENT · {department.code}</span>
        <button type="button" onClick={onClose} aria-label="Close"><X size={16} className="text-slate" /></button>
      </div>
      <h3 id={titleId} className="font-serif text-[19px] font-semibold text-ink mb-2">{department.name}</h3>
      <p className="font-mono text-[11px] text-slate">
        {department.hod_id ? `HOD ID: ${department.hod_id}` : "No HOD assigned"}
      </p>
    </Modal>
  );
}

DepartmentDetails.propTypes = {
  department: PropTypes.object,
  onClose: PropTypes.func.isRequired,
};

DepartmentDetails.defaultProps = { department: null };