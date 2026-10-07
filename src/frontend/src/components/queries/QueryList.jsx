import React from "react";
import PropTypes from "prop-types";
import { MessageCircle, CheckCircle2, Clock, Trash2 } from "lucide-react";

export default function QueryList({ queries, onSelect, onDelete, canDelete }) {
  if (!queries || queries.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-slate">
        <MessageCircle size={32} className="opacity-30 mb-2" />
        <p className="font-serif text-[16px] mb-1">No queries yet</p>
        <p className="text-[12.5px]">Ask a question to get started.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {queries.map((q) => {
        const isAnswered = q.status === "answered";
        return (
          <div
            key={q.id}
            onClick={() => onSelect(q)}
            className="bg-paper-raised border border-hairline rounded-sm p-4 flex flex-col gap-2 cursor-pointer hover:border-urgent/40 transition-colors"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <h3 className="font-serif text-[15px] font-semibold text-ink truncate">
                  {q.title}
                </h3>
                <p className="text-[11.5px] text-slate mt-0.5">
                  Asked by {q.student_name}
                  {q.department_name ? ` · ${q.department_name}` : ""}
                </p>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                {isAnswered ? (
                  <span className="flex items-center gap-1 font-mono text-[10.5px] text-green-700 bg-green-50 border border-green-200 px-2 py-0.5 rounded-sm uppercase">
                    <CheckCircle2 size={11} />
                    Answered
                  </span>
                ) : (
                  <span className="flex items-center gap-1 font-mono text-[10.5px] text-urgent bg-urgent/10 border border-urgent/20 px-2 py-0.5 rounded-sm uppercase">
                    <Clock size={11} />
                    Open
                  </span>
                )}
                {canDelete?.(q) && onDelete && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDelete(q.id, q.title);
                    }}
                    className="text-urgent hover:opacity-70"
                    aria-label="Delete"
                  >
                    <Trash2 size={14} />
                  </button>
                )}
              </div>
            </div>

            <p className="text-[13px] text-ink/80 line-clamp-2">{q.description}</p>

            {isAnswered && q.reply && (
              <div className="pt-2 border-t border-hairline">
                <p className="font-mono text-[10px] tracking-wide text-slate mb-1">
                  REPLY FROM {q.replied_by_name?.toUpperCase() || "FACULTY"}
                </p>
                <p className="text-[12.5px] text-ink/90 line-clamp-2">{q.reply}</p>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

QueryList.propTypes = {
  queries: PropTypes.array,
  onSelect: PropTypes.func,
  onDelete: PropTypes.func,
  canDelete: PropTypes.func,
};

QueryList.defaultProps = {
  queries: [],
};