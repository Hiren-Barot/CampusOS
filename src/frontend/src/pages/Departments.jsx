import React from "react";
import { useEffect, useState } from "react";
import { Plus, AlertTriangle, Search } from "lucide-react";
import toast from "react-hot-toast";
import { getDepartments, createDepartment, updateDepartment, deleteDepartment } from "../services/departmentService";
import useRole from "../hooks/useRole";
import DepartmentList from "../components/departments/DepartmentList.jsx";
import DepartmentForm from "../components/departments/DepartmentForm.jsx";
import DepartmentDetails from "../components/departments/DepartmentDetails.jsx";
import Spinner from "../components/common/Spinner.jsx";

export default function Departments() {
  const { canManageDepartments } = useRole();
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState(false);
  const [selected, setSelected] = useState(null);
  const [editing, setEditing] = useState(null);

  function refresh() {
    setLoading(true);
    setLoadError("");
    getDepartments()
      .then(setDepartments)
      .catch((err) => setLoadError(err.message || "Could not load departments"))
      .finally(() => setLoading(false));
  }

  useEffect(refresh, []);

  async function handleEdit(id, data) {
    await updateDepartment(id, data);
    setEditing(null);
    refresh();
  }

  async function handleDelete(id, name) {
    if (!window.confirm(`Delete department "${name}"? This can't be undone. All users will be unassigned.`)) {
      return;
    }
    try {
      await deleteDepartment(id);
      toast.success("Department deleted");
      refresh();
    } catch (err) {
      toast.error(err.message || "Could not delete department");
    }
  }

  const q = search.trim().toLowerCase();
  const filtered = q
    ? departments.filter((d) =>
        [d.name, d.code, d.hod_name].filter(Boolean).join(" ").toLowerCase().includes(q)
      )
    : departments;

  return (
    <div>
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h1 className="font-serif text-[26px] font-semibold text-ink">Departments</h1>
        {canManageDepartments && (
          <button
            onClick={() => setModal(true)}
            className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
          >
            <Plus size={12} /> Add department
          </button>
        )}
      </div>

      <div className="mb-5 relative max-w-md">
        <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate" />
        <label htmlFor="department-search" className="sr-only">Search departments</label>
        <input
          id="department-search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search department or HOD…"
          className="w-full border border-hairline rounded-sm pl-9 pr-3 py-2 text-[13px] text-ink bg-paper-raised"
        />
      </div>

      {modal && (
        <DepartmentForm
          onClose={() => setModal(false)}
          onSubmit={async (data) => {
            await createDepartment(data);
            refresh();
          }}
        />
      )}
      {editing && (
        <DepartmentForm
          initialData={editing}
          mode="edit"
          onClose={() => setEditing(null)}
          onSubmit={(data) => handleEdit(editing.id, data)}
        />
      )}
      {selected && <DepartmentDetails department={selected} onClose={() => setSelected(null)} />}

      {loading ? (
        <Spinner label="Loading departments…" />
      ) : loadError ? (
        <div role="alert" className="text-center py-10 border border-hairline rounded-sm bg-urgent/5">
          <AlertTriangle className="mx-auto text-urgent mb-2" size={28} />
          <p className="text-[13.5px] text-ink mb-3">{loadError}</p>
          <button onClick={refresh} className="font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]">
            Retry
          </button>
        </div>
      ) : (
        <DepartmentList
          departments={filtered}
          canManage={canManageDepartments}
          canEdit={canManageDepartments}
          onEdit={setEditing}
          onDelete={(id) => handleDelete(id, departments.find((d) => d.id === id)?.name)}
          onSelect={setSelected}
        />
      )}
    </div>
  );
}