import React, { useEffect, useState } from "react";
import { Users, Plus, AlertTriangle } from "lucide-react";
import { getUsersByRole, createUser, updateUser, deleteUser } from "../../services/userService";
import { getNotices } from "../../services/noticeService";
import toast from "react-hot-toast";
import useRole from "../../hooks/useRole";
import StatCard from "./StatCard.jsx";
import UserList from "../users/UserList.jsx";
import UserForm from "../users/UserForm.jsx";
import Spinner from "../common/Spinner.jsx";

export default function HODDashboard() {
  const { canManageUser, creatableRoles } = useRole();
  const [faculty, setFaculty] = useState([]);
  const [students, setStudents] = useState([]);
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [modal, setModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [shouldRefresh, setShouldRefresh] = useState(false);

  function refresh() {
    setLoading(true);
    setLoadError("");
    Promise.all([
      getUsersByRole("faculty"),
      getUsersByRole("student"),
      getNotices(),
    ])
      .then(([f, s, n]) => {
        setFaculty(f);
        setStudents(s);
        setNotices(n);
      })
      .catch((err) => setLoadError(err.message || "Could not load department overview"))
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
    const original = [...faculty, ...students].find((u) => u.id === id);
    if (
      original &&
      data.department_id !== undefined &&
      original.department_id !== data.department_id
    ) {
      if (!window.confirm(`Change ${original.full_name}'s department?`)) return;
    }
    await updateUser(id, data);
    setEditing(null);
    refresh();
  }

  if (loading) return <Spinner label="Loading department overview…" />;

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
        <StatCard label="FACULTY" value={faculty.length} />
        <StatCard label="STUDENTS" value={students.length} />
        <StatCard label="DEPT. NOTICES" value={notices.length} />
      </div>

      <div className="bg-paper-raised border border-hairline rounded-sm">
        <div className="flex items-center justify-between px-5 py-4 border-b border-hairline">
          <div className="flex items-center gap-2">
            <Users size={16} className="text-urgent" />
            <span className="font-serif text-[16px] font-semibold text-ink">Faculty management</span>
          </div>
          <button
            onClick={() => setModal(true)}
            className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
          >
            <Plus size={12} /> Add faculty
          </button>
        </div>
        <div className="p-4">
          <UserList
            users={faculty}
            canManageRow={(u) => canManageUser(u.role, u.id)}
            canEditRow={(u) => canManageUser(u.role, u.id)}
            onEdit={setEditing}
            onDelete={(id) => handleDelete(id, faculty.find((u) => u.id === id)?.full_name)}
          />
        </div>
      </div>
    </>
  );
}