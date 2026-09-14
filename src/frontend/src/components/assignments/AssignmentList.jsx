import React from "react";
import PropTypes from "prop-types";
import { Trash2, Pencil, ClipboardList } from "lucide-react";
import { shortDate } from "../../utils/dateUtils";

export default function AssignmentList({ assignments, canDelete, canEdit, onDelete, onEdit, onSelect }) {
  if (assignments.length === 0) {
    return (
      <div className="text-center py-10">
        <ClipboardList className="mx-auto text-slate/30 mb-2" size={32} />
        <p className="text-[13px] text-slate">No assignments yet — create one to get started!</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      {assignments.map((a) => (
        <div
          key={a.id}
          onClick={() => onSelect?.(a)}
          className={`flex items-center justify-between px-3 py-3 border border-hairline rounded-sm ${onSelect ? "cursor-pointer hover:shadow-sm" : ""}`}
        >
          <div>
            <div className="text-[13.5px] font-medium text-ink">{a.title}</div>
            <div className="font-mono text-[10.5px] mt-1 text-slate">{a.by}</div>
          </div>
          <div className="flex items-center gap-2">
            <span className="font-mono text-[10.5px] px-2 py-1 rounded-sm bg-event/10 text-event">
              DUE {shortDate(a.dueDate)}
            </span>
            {(canEdit || canDelete) && (
              <div className="flex items-center gap-2">
                {canEdit && <button onClick={(e) => { e.stopPropagation(); onEdit(a); }} aria-label="Edit assignment"><Pencil size={13} className="text-slate" /></button>}
                {canDelete && (
                  <button onClick={(e) => { e.stopPropagation(); onDelete(a.id); }} aria-label="Delete assignment">
                    <Trash2 size={13} className="text-slate" />
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

AssignmentList.propTypes = {
  assignments: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      title: PropTypes.string.isRequired,
      dueDate: PropTypes.string,
      by: PropTypes.string,
    })
  ).isRequired,
  canDelete: PropTypes.bool,
  canEdit: PropTypes.bool,
  onDelete: PropTypes.func,
  onEdit: PropTypes.func,
  onSelect: PropTypes.func,
};

AssignmentList.defaultProps = {
  canDelete: false,
  canEdit: false,
  onDelete: () => {},
  onEdit: () => {},
  onSelect: undefined,
};