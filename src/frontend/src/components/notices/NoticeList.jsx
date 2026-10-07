import React, { useEffect, useState, useMemo } from "react";
import PropTypes from "prop-types";
import { Trash2, Pencil, Megaphone } from "lucide-react";
import { timeAgo } from "../../utils/dateUtils";
import useRole from "../../hooks/useRole";
import { getDepartments } from "../../services/departmentService";

const DEFAULT_TAG_STYLE = {
  pin: "bg-event",
  bg: "bg-event/10",
  text: "text-event",
};

export default function NoticeList({
  notices,
  canDelete = false,
  canEdit = false,
  onDelete = () => {},
  onEdit = () => {},
  onSelect = undefined,
}) {
  const { role } = useRole();
  const canPost = ["faculty", "hod", "principal", "admin"].includes(role);

  const canSeeDept = role === "principal" || role === "admin";

  const [, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 30_000);
    return () => clearInterval(id);
  }, []);

  const [departments, setDepartments] = useState([]);

  useEffect(() => {
    if (!canSeeDept) return;
    getDepartments()
      .then((data) => setDepartments(Array.isArray(data) ? data : []))
      .catch(() => setDepartments([]));
  }, [canSeeDept]);

  const deptMap = useMemo(() => {
    const map = {};
    departments.forEach((d) => {
      map[d.id] = d.code || d.name || `DEPT ${d.id}`;
    });
    return map;
  }, [departments]);

  if (notices.length === 0) {
    return (
      <div className="text-center py-10">
        <Megaphone className="mx-auto text-slate/30 mb-2" size={32} />
        <p className="text-[13px] text-slate">
          {canPost
            ? "No notices yet — post one to get started!"
            : "No notices posted yet."}
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {notices.map((n) => {
        const style = DEFAULT_TAG_STYLE;

        const showEdit = typeof canEdit === "function" ? canEdit(n) : canEdit;
        const showDelete = typeof canDelete === "function" ? canDelete(n) : canDelete;

        const deptLabel =
          n.department_id == null
            ? "ALL DEPTS"
            : deptMap[n.department_id] || `DEPT ${n.department_id}`;

        return (
          <div
            key={n.id}
            onClick={onSelect ? () => onSelect(n) : undefined}
            className={`bg-paper-raised border border-hairline rounded-sm p-4 relative ${
              onSelect ? "cursor-pointer hover:shadow-md transition-shadow" : ""
            }`}
          >
            <span
              className={`absolute -top-[6px] left-5 w-[10px] h-[10px] rounded-full shadow ${style.pin}`}
            />
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                <span
                  className={`inline-block font-mono text-[10px] font-medium tracking-wide px-2 py-[3px] rounded-sm ${style.bg} ${style.text}`}
                >
                  NOTICE
                </span>
                {canSeeDept && (
                  <span className="inline-block font-mono text-[10px] font-medium tracking-wide px-2 py-[3px] rounded-sm bg-ink/5 text-slate border border-hairline">
                    {deptLabel}
                  </span>
                )}
              </div>
              {(showEdit || showDelete) && (
                <div className="flex items-center gap-2">
                  {showEdit && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onEdit(n);
                      }}
                      aria-label="Edit notice"
                    >
                      <Pencil size={13} className="text-slate" />
                    </button>
                  )}
                  {showDelete && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDelete(n.id);
                      }}
                      aria-label="Delete notice"
                    >
                      <Trash2 size={13} className="text-slate" />
                    </button>
                  )}
                </div>
              )}
            </div>
            <h4 className="font-serif text-[15px] font-semibold leading-snug mb-3 text-ink">
              {n.title}
            </h4>
            <div className="flex justify-between font-mono text-[10.5px] pt-2 border-t border-dashed border-hairline text-slate">
              <span>{n.meta}</span>
              <span>{timeAgo(n.createdAt)}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

NoticeList.propTypes = {
  notices: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      title: PropTypes.string.isRequired,
      meta: PropTypes.string,
      createdAt: PropTypes.string,
      department_id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    })
  ).isRequired,
  canDelete: PropTypes.oneOfType([PropTypes.bool, PropTypes.func]),
  canEdit: PropTypes.oneOfType([PropTypes.bool, PropTypes.func]),
  onDelete: PropTypes.func,
  onEdit: PropTypes.func,
  onSelect: PropTypes.func,
};