import React, { useEffect, useState, useMemo } from "react";
import PropTypes from "prop-types";
import { Trash2, Pencil, ClipboardList } from "lucide-react";
import useRole from "../../hooks/useRole";

const ROLE_RANK = {
  admin: 5,
  principal: 4,
  hod: 3,
  faculty: 2,
  student: 1,
};

function isPastDate(input) {
  if (!input) return false;
  let s = String(input).trim();
  if (!s.endsWith("Z") && !/[+-]\d{2}:?\d{2}$/.test(s)) {
    s = s.includes(" ") ? s.replace(" ", "T") : s;
  }
  const d = new Date(s);
  if (Number.isNaN(d.getTime())) return false;
  return d.getTime() < Date.now();
}

function formatDeadline(input) {
  if (!input) return "TBD";
  let s = String(input).trim();
  if (!s.endsWith("Z") && !/[+-]\d{2}:?\d{2}$/.test(s)) {
    s = s.includes(" ") ? s.replace(" ", "T") : s;
  }
  const d = new Date(s);
  if (Number.isNaN(d.getTime())) return "TBD";
  
  return d.toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  }).toUpperCase();
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

  const [, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 30_000);
    return () => clearInterval(id);
  }, []);

  const sorted = useMemo(() => {
    const list = [...assignments];
    list.sort((a, b) => {
      const ao = isPastDate(a.dueDate);
      const bo = isPastDate(b.dueDate);
      if (ao !== bo) return ao ? -1 : 1;

      const ra = ROLE_RANK[a.faculty_role] || 0;
      const rb = ROLE_RANK[b.faculty_role] || 0;
      if (rb !== ra) return rb - ra;

      const ta = new Date(a.createdAt || 0).getTime();
      const tb = new Date(b.createdAt || 0).getTime();
      return tb - ta;
    });
    return list;
  }, [assignments]);

  if (assignments.length === 0) {
    return (
      <div className="text-center py-10">
        <ClipboardList className="mx-auto text-slate/30 mb-2" size={32} />
        <p className="text-[13px] text-slate">
          {canCreate ? "No assignments yet — create one to get started!" : "No assignments posted yet."}
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
        
        const rawDate = a.dueDate || a.deadline;
        const formattedDate = formatDeadline(rawDate);

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
              <span
                className={`font-mono text-[10.5px] px-2 py-1 rounded-sm ${
                  overdue ? "bg-urgent/10 text-urgent" : "bg-event/10 text-event"
                }`}
              >
                {overdue ? "EXPIRED · " : "DUE "}
                {formattedDate}
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
      deadline: PropTypes.string,
      by: PropTypes.string,
      faculty_id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
      faculty_role: PropTypes.string,
    })
  ).isRequired,
  canDelete: PropTypes.oneOfType([PropTypes.bool, PropTypes.func]),
  canEdit: PropTypes.oneOfType([PropTypes.bool, PropTypes.func]),
  onDelete: PropTypes.func,
  onEdit: PropTypes.func,
  onSelect: PropTypes.func,
};