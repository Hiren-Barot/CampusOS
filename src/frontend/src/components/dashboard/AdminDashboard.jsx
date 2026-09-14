import React from "react";
import { useEffect, useState } from "react";
import { Users, Building2, Plus, AlertTriangle } from "lucide-react";
import toast from "react-hot-toast";
import { getUsers, createUser, updateUser, deleteUser } from "../../services/userService";
import { getDepartments } from "../../services/departmentService";
import useRole from "../../hooks/useRole";
import StatCard from "./StatCard.jsx";
import UserList from "../users/UserList.jsx";
import UserForm from "../users/UserForm.jsx";
import Spinner from "../common/Spinner.jsx";

export default function AdminDashboard() {
  const { canManageUser, creatableRoles } = useRole();
  const [users, setUsers] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [modal, setModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [shouldRefresh, setShouldRefresh] = useState(false);

  function refresh() {
    setLoading(true);
    setLoadError("");
    Promise.all([getUsers(), getDepartments()])
      .then(([u, d]) => {
        setUsers(u);
        setDepartments(d);
      })
      .catch((err) => setLoadError(err.message || "Could not load system overview"))
      .finally(() => setLoading(false));
  }

  useEffect(refresh, []);

  function closeModal() {
    setModal(false);
    if (shouldRefresh) {
      refresh();
      setShouldRefresh(false);
    }
  }

  async function handleDelete(id, name) {
    if (!window.confirm(`Delete "${name}"? This can't be undone.`)) return;
    try {
      await deleteUser(id);
      toast.success("User deleted");
      refresh();
    } catch (err) {
      toast.error(err.message || "Could not delete user");
    }
  }

  async function handleEdit(id, data) {
    const original = users.find((u) => u.id === id);
    if (
      original &&
      data.department_id !== undefined &&
      original.department_id !== data.department_id
    ) {
      const confirmed = window.confirm(
        `Change ${original.full_name}'s department?`
      );
      if (!confirmed) return;
    }
    await updateUser(id, data);
    setEditing(null);
    refresh();
  }

  if (loading) return <Spinner label="Loading system overview…" />;

  if (loadError) {
    return (
      <div role="alert" className="text-center py-10 border border-hairline rounded-sm bg-urgent/5">
        <AlertTriangle className="mx-auto text-urgent mb-2" size={28} />
        <p className="text-[13.5px] text-ink mb-3">{loadError}</p>
        <button onClick={refresh} className="font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]">
          Retry
        </button>
      </div>
    );
  }

  const activeRoles = new Set(users.map((u) => u.role)).size;

  return (
    <>
      {modal && (
        <UserForm
          roleOptions={creatableRoles}
          onClose={closeModal}
          onSubmit={async (data) => {
            const result = await createUser(data);
            setShouldRefresh(true);
            return result;
          }}
        />
      )}
      {editing && (
        <UserForm
          initialData={editing}
          mode="edit"
          roleOptions={creatableRoles.length ? creatableRoles : [editing.role]}
          onClose={() => setEditing(null)}
          onSubmit={(data) => handleEdit(editing.id, data)}
        />
      )}

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-7">
        <StatCard label="TOTAL USERS" value={users.length} />
        <StatCard label="DEPARTMENTS" value={departments.length} />
        <StatCard label="ACTIVE ROLES" value={activeRoles} />
      </div>

      <div className="bg-paper-raised border border-hairline rounded-sm">
        <div className="flex items-center justify-between px-5 py-4 border-b border-hairline">
          <div className="flex items-center gap-2">
            <Users size={16} className="text-urgent" />
            <span className="font-serif text-[16px] font-semibold text-ink">User management</span>
          </div>
          <button
            onClick={() => setModal(true)}
            className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
          >
            <Plus size={12} /> Add user
          </button>
        </div>
        <div className="p-4">
          <UserList
            users={users}
            canManageRow={(target) => canManageUser(target.role, target.id)}
            canEditRow={(target) => canManageUser(target.role, target.id)}
            onEdit={setEditing}
            onDelete={(id) => handleDelete(id, users.find((u) => u.id === id)?.full_name)}
          />
        </div>
      </div>
    </>
  );
}