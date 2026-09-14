import React, { useEffect, useState } from "react";
import { Building2, Plus, AlertTriangle } from "lucide-react";
import toast from "react-hot-toast";
import {
  getDepartments,
  createDepartment,
  updateDepartment,
  deleteDepartment,
} from "../../services/departmentService";
import { getUsersByRole } from "../../services/userService";
import StatCard from "./StatCard.jsx";
import DepartmentList from "../departments/DepartmentList.jsx";
import DepartmentForm from "../departments/DepartmentForm.jsx";
import Spinner from "../common/Spinner.jsx";

export default function PrincipalDashboard() {
  const [departments, setDepartments] = useState([]);
  const [faculty, setFaculty] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [modal, setModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [shouldRefresh, setShouldRefresh] = useState(false);

  function refresh() {
    setLoading(true);
    setLoadError("");
    Promise.all([
      getDepartments(),
      getUsersByRole("faculty"),
      getUsersByRole("student"),
    ])
      .then(([d, f, s]) => {
        setDepartments(d);
        setFaculty(f);
        setStudents(s);
      })
      .catch((err) => setLoadError(err.message || "Could not load college overview"))
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

  async function handleEdit(id, data) {
    await updateDepartment(id, data);
    setEditing(null);
    refresh();
  }

  if (loading) return <Spinner label="Loading college overview…" />;

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
        <DepartmentForm
          onClose={closeModal}
          onSubmit={async (d) => {
            const result = await createDepartment(d);
            setShouldRefresh(true);
            return result;
          }}
        />
      )}
      {editing && (
        <DepartmentForm
          initialData={editing}
          mode="edit"
          onClose={() => setEditing(null)}
          onSubmit={(d) => handleEdit(editing.id, d)}
        />
      )}

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-7">
        <StatCard label="DEPARTMENTS" value={departments.length} />
        <StatCard label="FACULTY" value={faculty.length} />
        <StatCard label="STUDENTS" value={students.length} />
      </div>

      <div className="bg-paper-raised border border-hairline rounded-sm">
        <div className="flex items-center justify-between px-5 py-4 border-b border-hairline">
          <div className="flex items-center gap-2">
            <Building2 size={16} className="text-urgent" />
            <span className="font-serif text-[16px] font-semibold text-ink">All departments</span>
          </div>
          <button
            onClick={() => setModal(true)}
            className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
          >
            <Plus size={12} /> Add department
          </button>
        </div>
        <div className="p-4">
          <DepartmentList
            departments={departments}
            canManage
            canEdit
            onEdit={setEditing}
            onDelete={(id) => handleDelete(id, departments.find((d) => d.id === id)?.name)}
          />
        </div>
      </div>
    </>
  );
}