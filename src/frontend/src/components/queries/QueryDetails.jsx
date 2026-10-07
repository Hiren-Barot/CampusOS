import React, { useState } from "react";
import PropTypes from "prop-types";
import { X, Send, CheckCircle2, Clock } from "lucide-react";
import toast from "react-hot-toast";
import Modal from "../common/Modal.jsx";
import { replyToQuery } from "../../services/queryService";

export default function QueryDetails({ query, onClose, onReplied, canReply }) {
  const titleId = "query-details-title";
  const [reply, setReply] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const isAnswered = query.status === "answered";

  async function handleReply() {
    if (!reply.trim()) {
      toast.error("Reply cannot be empty");
      return;
    }
    setSubmitting(true);
    try {
      const updated = await replyToQuery(query.id, reply.trim());
      toast.success("Reply sent!");
      onReplied?.(updated);
      onClose();
    } catch (err) {
      toast.error(err.message || "Could not send reply");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="620px">
      <div className="flex items-center justify-between mb-5">
        <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">
          Query Details
        </span>
        <button type="button" onClick={onClose} aria-label="Close">
          <X size={16} className="text-slate" />
        </button>
      </div>

      <div className="flex flex-col gap-4 max-h-[65vh] overflow-y-auto pr-1">
        <div className="flex items-center gap-2">
          {isAnswered ? (
            <span className="flex items-center gap-1 font-mono text-[10.5px] text-green-700 bg-green-50 border border-green-200 px-2 py-0.5 rounded-sm uppercase">
              <CheckCircle2 size={11} /> Answered
            </span>
          ) : (
            <span className="flex items-center gap-1 font-mono text-[10.5px] text-urgent bg-urgent/10 border border-urgent/20 px-2 py-0.5 rounded-sm uppercase">
              <Clock size={11} /> Open
            </span>
          )}
          <span className="text-[11.5px] text-slate">
            Asked by {query.student_name} · {query.department_name || "—"}
          </span>
        </div>

        <div>
          <p className="font-mono text-[10px] tracking-wide text-slate mb-1">QUESTION</p>
          <h3 className="font-serif text-[16px] font-semibold text-ink mb-2">{query.title}</h3>
          <p className="text-[13.5px] text-ink/90 whitespace-pre-wrap">{query.description}</p>
        </div>

        {isAnswered && query.reply ? (
          <div className="border-t border-hairline pt-4">
            <p className="font-mono text-[10px] tracking-wide text-slate mb-1">
              REPLY · {query.replied_by_name || "Faculty"}
            </p>
            <p className="text-[13.5px] text-ink/90 whitespace-pre-wrap bg-paper border border-hairline rounded-sm px-3 py-2">
              {query.reply}
            </p>
          </div>
        ) : canReply ? (
          <div className="border-t border-hairline pt-4">
            <label className="font-mono text-[10px] tracking-wide block mb-1 text-slate">
              YOUR REPLY
            </label>
            <textarea
              rows={5}
              className="w-full border border-hairline rounded-sm px-3 py-2 text-[13px] text-ink bg-paper-raised resize-y"
              value={reply}
              onChange={(e) => setReply(e.target.value)}
              placeholder="Type your answer to the student…"
            />
            <button
              onClick={handleReply}
              disabled={submitting}
              className="mt-3 flex items-center gap-2 rounded-sm py-2 px-4 text-[13px] font-medium text-white bg-urgent disabled:opacity-50"
            >
              <Send size={14} />
              {submitting ? "Sending…" : "Send Reply"}
            </button>
          </div>
        ) : (
          <div className="border-t border-hairline pt-4">
            <p className="text-[12.5px] text-slate italic">
              Waiting for a reply from your department's faculty or HOD.
            </p>
          </div>
        )}
      </div>

      <button
        onClick={onClose}
        className="w-full mt-6 rounded-sm py-2 text-[13px] font-medium text-white bg-[#1B2430]"
      >
        Close
      </button>
    </Modal>
  );
}

QueryDetails.propTypes = {
  query: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired,
  onReplied: PropTypes.func,
  canReply: PropTypes.bool,
};

QueryDetails.defaultProps = {
  canReply: false,
};