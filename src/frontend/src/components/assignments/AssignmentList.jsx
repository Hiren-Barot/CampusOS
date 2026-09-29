import React, { useEffect, useState, useMemo } from "react";
import PropTypes from "prop-types";
import { Trash2, Pencil, ClipboardList } from "lucide-react";
import { shortDate } from "../../utils/dateUtils";
import useRole from "../../hooks/useRole";

// Returns true if the given date is in the past
function isPastDate(input) {
  if (!input) return false;
  let s = String(input).trim();
  // No timezone marker → treat as local (matches dateUtils.js behavior)
  if (!s.endsWith("Z") && !/[+-]\d{2}:?\d{2}$/.test(s)) {
    s = s.includes(" ") ? s.replace(" ", "T") : s;
  }
  const d = new Date(s);
  if (Number.isNaN(d.getTime())) return false;
  return d.getTime() < Date.now();
}

export default function AssignmentList({
  assignments,
  canDelete = false,
  canEdit = false,
  onDelete = () => {},
  onEdit = () => {},
  onSelect = undefined,
}) {
  const { role } = useRole();
  const canCreate = role === "faculty";

  // Auto-refresh tick — updates due dates every 30 seconds
  const [, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 30_000);
    return () => clearInterval(id);
  }, []);

  // Sort: overdue first, then keep original order
  const sorted = useMemo(() => {
    const list = [...assignments];
    list.sort((a, b) => {
      const ao = isPastDate(a.dueDate);
      const bo = isPastDate(b.dueDate);
      if (ao !== bo) return ao ? -1 : 1;
      return 0;
    });
    return list;
  }, [assignments]);

  if (assignments.length === 0) {
    return (
      <div className="text-center py-10">
        <ClipboardList className="mx-auto text-slate/30 mb-2" size={32} />
        <p className="text-[13px] text-slate">
          {canCreate
            ? "No assignments yet — create one to get started!"
            : "No assignments posted yet."}
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      {sorted.map((a) => {
        const showEdit = typeof canEdit === "function" ? canEdit(a) : canEdit;
        const showDelete = typeof canDelete === "function" ? canDelete(a) : canDelete;
        const overdue = isPastDate(a.dueDate);

        return (
          <div
            key={a.id}
            onClick={() => onSelect?.(a)}
            className={`flex items-center justify-between px-3 py-3 border border-hairline rounded-sm ${
              onSelect ? "cursor-pointer hover:shadow-sm" : ""
            }`}
          >
            <div>
              <div className="text-[13.5px] font-medium text-ink">{a.title}</div>
              <div className="font-mono text-[10.5px] mt-1 text-slate">{a.by}</div>
            </div>
            <div className="flex items-center gap-2">
              {/* Overdue badge: red if past, gold if future */}
              <span
                className={`font-mono text-[10.5px] px-2 py-1 rounded-sm ${
                  overdue
                    ? "bg-urgent/10 text-urgent"
                    : "bg-event/10 text-event"
                }`}
              >
                {overdue ? "OVERDUE · " : "DUE "}
                {shortDate(a.dueDate)}
              </span>
              {(showEdit || showDelete) && (
                <div className="flex items-center gap-2">
                  {showEdit && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onEdit(a);
                      }}
                      aria-label="Edit assignment"
                    >
                      <Pencil size={13} className="text-slate" />
                    </button>
                  )}
                  {showDelete && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDelete(a.id);
                      }}
                      aria-label="Delete assignment"
                    >
                      <Trash2 size={13} className="text-slate" />
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>
        );
      })}
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
      faculty_id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    })
  ).isRequired,
  canDelete: PropTypes.oneOfType([PropTypes.bool, PropTypes.func]),
  canEdit: PropTypes.oneOfType([PropTypes.bool, PropTypes.func]),
  onDelete: PropTypes.func,
  onEdit: PropTypes.func,
  onSelect: PropTypes.func,
};