import React from "react";
import PropTypes from "prop-types";
import { Trash2, Pencil, Building2 } from "lucide-react";

export default function DepartmentList({ departments, canManage, canEdit, onDelete, onEdit, onSelect }) {
  if (departments.length === 0) {
    return (
      <div className="text-center py-10">
        <Building2 className="mx-auto text-slate/30 mb-2" size={32} />
        <p className="text-[13px] text-slate">No departments yet — add one to get started!</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      {departments.map((d) => (
        <div
          key={d.id}
          onClick={() => onSelect?.(d)}
          className={`flex items-center justify-between px-3 py-2.5 border border-hairline rounded-sm ${onSelect ? "cursor-pointer hover:shadow-sm" : ""}`}
        >
          <div>
            <div className="text-[13.5px] font-medium text-ink">{d.name}</div>
            <div className="font-mono text-[10.5px] mt-0.5 text-slate">
              CODE: {d.code} {d.hod_id ? `· HOD ID: ${d.hod_id}` : "· No HOD"}
            </div>
          </div>
          {(canEdit || canManage) && (
            <div className="flex items-center gap-2">
              {canEdit && <button onClick={(e) => { e.stopPropagation(); onEdit(d); }} aria-label="Edit department"><Pencil size={14} className="text-slate" /></button>}
              {canManage && (
                <button onClick={(e) => { e.stopPropagation(); onDelete(d.id); }} aria-label="Delete department">
                  <Trash2 size={14} className="text-urgent" />
                </button>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

DepartmentList.propTypes = {
  departments: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      name: PropTypes.string.isRequired,
      code: PropTypes.string,
      hod_id: PropTypes.number,
    })
  ).isRequired,
  canManage: PropTypes.bool,
  canEdit: PropTypes.bool,
  onDelete: PropTypes.func,
  onEdit: PropTypes.func,
  onSelect: PropTypes.func,
};

DepartmentList.defaultProps = {
  canManage: false,
  canEdit: false,
  onDelete: () => {},
  onEdit: () => {},
  onSelect: undefined,
};