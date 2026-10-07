import React from "react";
import PropTypes from "prop-types";
import { Pencil, Trash2, Download, Paperclip, Calendar } from "lucide-react";

export default function AssignmentList({
  assignments,
  onEdit,
  onDelete,
  onDownload,
  onSelect,
  canEdit,
  canDelete,
}) {
  if (!assignments || assignments.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-slate">
        <p className="font-serif text-[16px] mb-1">No assignments yet</p>
        <p className="text-[12.5px]">Check back later.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {assignments.map((a) => {
        const deadline = new Date(a.deadline);
        const isExpired = deadline < new Date();
        const deadlineStr = deadline.toLocaleString("en-IN", {
          day: "2-digit",
          month: "short",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        });

        const showEdit = typeof canEdit === "function" ? canEdit(a) : false;
        const showDelete = typeof canDelete === "function" ? canDelete(a) : false;

        return (
          <div
            key={a.id}
            onClick={() => onSelect?.(a)}
            className="bg-paper-raised border border-hairline rounded-sm p-4 flex flex-col gap-2 cursor-pointer hover:border-urgent/40 transition-colors"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <h3 className="font-serif text-[15px] font-semibold text-ink truncate">
                  {a.title}
                </h3>
                <p className="text-[11.5px] text-slate mt-0.5">
                  {a.faculty_name || "Unknown"} · Dept #{a.department_id}
                </p>
              </div>

              {(showEdit || showDelete) && (
                <div className="flex gap-2 shrink-0">
                  {showEdit && onEdit && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onEdit(a);
                      }}
                      className="text-slate hover:text-ink"
                      aria-label="Edit"
                    >
                      <Pencil size={15} />
                    </button>
                  )}
                  {showDelete && onDelete && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDelete(a.id);
                      }}
                      className="text-urgent hover:opacity-70"
                      aria-label="Delete"
                    >
                      <Trash2 size={15} />
                    </button>
                  )}
                </div>
              )}
            </div>

            {a.description && (
              <p className="text-[13px] text-ink/80 line-clamp-2">{a.description}</p>
            )}

            <div className="flex items-center justify-between gap-3 pt-2 border-t border-hairline">
              <div className="flex items-center gap-3 text-[11.5px] flex-wrap">
                <span
                  className={`flex items-center gap-1 font-mono ${
                    isExpired ? "text-urgent" : "text-slate"
                  }`}
                >
                  <Calendar size={12} />
                  {deadlineStr}
                  {isExpired && " (expired)"}
                </span>

                {a.has_file && (
                  <span className="flex items-center gap-1 text-slate font-mono">
                    <Paperclip size={12} />
                    {a.file_name || "attachment"}
                  </span>
                )}
              </div>

              {a.has_file && onDownload && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDownload(a);
                  }}
                  className="flex items-center gap-1 text-[12px] font-medium text-urgent hover:opacity-70"
                >
                  <Download size={14} />
                  Download
                </button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

AssignmentList.propTypes = {
  assignments: PropTypes.array,
  onEdit: PropTypes.func,
  onDelete: PropTypes.func,
  onDownload: PropTypes.func,
  onSelect: PropTypes.func,
  canEdit: PropTypes.func,
  canDelete: PropTypes.func,
};

AssignmentList.defaultProps = {
  assignments: [],
};