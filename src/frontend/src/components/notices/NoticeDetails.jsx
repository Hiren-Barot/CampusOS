import React from "react";
import PropTypes from "prop-types";
import { X } from "lucide-react";
import Modal from "../common/Modal.jsx";

export default function NoticeDetails({ notice, onClose }) {
  if (!notice) return null;
  const titleId = "notice-details-title";
  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="420px">
      <div className="flex items-center justify-between mb-4">
        <span className="font-mono text-[10px] text-slate tracking-wide">NOTICE</span>
        <button type="button" onClick={onClose} aria-label="Close"><X size={16} className="text-slate" /></button>
      </div>
      <h3 id={titleId} className="font-serif text-[19px] font-semibold text-ink mb-2">{notice.title}</h3>
      <p className="font-mono text-[11px] text-slate mb-3">{notice.meta}</p>
      {notice.content && <p className="text-[13px] text-ink whitespace-pre-wrap">{notice.content}</p>}
    </Modal>
  );
}

NoticeDetails.propTypes = {
  notice: PropTypes.object,
  onClose: PropTypes.func.isRequired,
};

NoticeDetails.defaultProps = { notice: null };