import React from "react";
import PropTypes from "prop-types";
import { Trash2, Pencil, Users as UsersIcon } from "lucide-react";

export default function UserList({ users, canManageRow, canEditRow, onDelete, onEdit, onSelect }) {
  if (users.length === 0) {
    return (
      <div className="text-center py-10">
        <UsersIcon className="mx-auto text-slate/30 mb-2" size={32} />
        <p className="text-[13px] text-slate">No users found.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {users.map((u) => {
        const showDelete = canManageRow ? canManageRow(u) : false;
        const showEdit = canEditRow ? canEditRow(u) : false;
        const displayName = u.full_name || u.name;
        const displayDept = u.department_name || u.dept || "—";
        return (
          <div
            key={u.id}
            onClick={() => onSelect?.(u)}
            className={`flex items-center justify-between px-3 py-2.5 border border-hairline rounded-sm ${onSelect ? "cursor-pointer hover:shadow-sm" : ""}`}
          >
            <div>
              <div className="text-[13.5px] font-medium text-ink">{displayName}</div>
              <div className="font-mono text-[10.5px] mt-0.5 text-slate capitalize">{u.role} · {displayDept}</div>
            </div>
            {(showEdit || showDelete) && (
              <div className="flex items-center gap-2">
                {showEdit && <button onClick={(e) => { e.stopPropagation(); onEdit(u); }} aria-label="Edit user"><Pencil size={14} className="text-slate" /></button>}
                {showDelete && (
                  <button onClick={(e) => { e.stopPropagation(); onDelete(u.id); }} aria-label="Delete user">
                    <Trash2 size={14} className="text-urgent" />
                  </button>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

UserList.propTypes = {
  users: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      full_name: PropTypes.string,
      name: PropTypes.string,
      role: PropTypes.string,
      department_name: PropTypes.string,
      dept: PropTypes.string,
    })
  ).isRequired,
  canManageRow: PropTypes.func,
  canEditRow: PropTypes.func,
  onDelete: PropTypes.func,
  onEdit: PropTypes.func,
  onSelect: PropTypes.func,
};

UserList.defaultProps = {
  canManageRow: undefined,
  canEditRow: undefined,
  onDelete: () => {},
  onEdit: () => {},
  onSelect: undefined,
};