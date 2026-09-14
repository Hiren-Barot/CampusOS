import React from "react";
import PropTypes from "prop-types";
import { X } from "lucide-react";
import Modal from "../common/Modal.jsx";

export default function UserDetails({ user, onClose }) {
  if (!user) return null;
  const titleId = "user-details-title";
  const displayName = user.full_name || user.name;
  const displayDept = user.department_name || user.dept || "—";
  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="420px">
      <div className="flex items-center justify-between mb-4">
        <span className="font-mono text-[10px] text-slate tracking-wide">{user.role?.toUpperCase()}</span>
        <button type="button" onClick={onClose} aria-label="Close"><X size={16} className="text-slate" /></button>
      </div>
      <h3 id={titleId} className="font-serif text-[19px] font-semibold text-ink mb-2">{displayName}</h3>
      <p className="font-mono text-[11px] text-slate">{`${user.email} · ${displayDept}`}</p>
    </Modal>
  );
}

UserDetails.propTypes = {
  user: PropTypes.object,
  onClose: PropTypes.func.isRequired,
};

UserDetails.defaultProps = { user: null };