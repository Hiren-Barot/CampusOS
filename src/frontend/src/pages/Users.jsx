import React, { useEffect, useState } from "react";
import { Plus, AlertTriangle, Search } from "lucide-react";
import toast from "react-hot-toast";
import { getUsers, createUser, updateUser, deleteUser } from "../services/userService";
import useRole from "../hooks/useRole";
import UserList from "../components/users/UserList.jsx";
import UserForm from "../components/users/UserForm.jsx";
import UserDetails from "../components/users/UserDetails.jsx";
import Spinner from "../components/common/Spinner.jsx";

export default function Users() {
  const { role, canManageUsers, canManageUser, creatableRoles } = useRole();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState(false);
  const [selected, setSelected] = useState(null);
  const [editing, setEditing] = useState(null);

  function refresh() {
    setLoading(true);
    setLoadError("");
    getUsers()
      .then(setUsers)
      .catch((err) => setLoadError(err.message || "Could not load users"))
      .finally(() => setLoading(false));
  }

  useEffect(refresh, []);

  const q = search.trim().toLowerCase();
  const filtered = q
    ? users.filter((u) =>
        [u.full_name, u.name, u.email].filter(Boolean).join(" ").toLowerCase().includes(q)
      )
    : users;

  async function handleEdit(id, data) {
    const original = users.find((u) => u.id === id);
    if (
      original &&
      data.department_id !== undefined &&
      original.department_id !== data.department_id
    ) {
      const originalDept = original.department_name || "—";
      const confirmed = window.confirm(
        `Change ${original.full_name}'s department from "${originalDept}" to the new one?`
      );
      if (!confirmed) return;
    }
    await updateUser(id, data);
    setEditing(null);
    refresh();
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

  return (
    <div>
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h1 className="font-serif text-[26px] font-semibold text-ink">
          {role === "faculty" ? "Students" : "Users"}
        </h1>
        {canManageUsers && creatableRoles.length > 0 && (
          <button
            onClick={() => setModal(true)}
            className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
          >
            <Plus size={12} /> Add user
          </button>
        )}
      </div>

      <div className="mb-5 relative max-w-md">
        <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate" />
        <label htmlFor="user-search" className="sr-only">Search users</label>
        <input
          id="user-search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search name or email…"
          className="w-full border border-hairline rounded-sm pl-9 pr-3 py-2 text-[13px] text-ink bg-paper-raised"
        />
      </div>

      {modal && (
        <UserForm
          roleOptions={creatableRoles}
          onClose={() => setModal(false)}
          onSubmit={async (data) => {
            const result = await createUser(data);
            refresh();
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
      {selected && <UserDetails user={selected} onClose={() => setSelected(null)} />}

      {loading ? (
        <Spinner label="Loading users…" />
      ) : loadError ? (
        <div role="alert" className="text-center py-10 border border-hairline rounded-sm bg-urgent/5">
          <AlertTriangle className="mx-auto text-urgent mb-2" size={28} />
          <p className="text-[13.5px] text-ink mb-3">{loadError}</p>
          <button onClick={refresh} className="font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]">
            Retry
          </button>
        </div>
      ) : (
        <UserList
          users={filtered}
          canManageRow={(u) => canManageUser(u.role, u.id)}
          canEditRow={(u) => canManageUser(u.role, u.id)}
          onEdit={setEditing}
          onDelete={(id) => handleDelete(id, users.find((u) => u.id === id)?.full_name)}
          onSelect={setSelected}
        />
      )}
    </div>
  );
}