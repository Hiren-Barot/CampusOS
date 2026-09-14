import React, { useEffect, useState } from "react";
import { Plus, AlertTriangle, Search } from "lucide-react";
import toast from "react-hot-toast";
import { getAssignments, createAssignment, updateAssignment, deleteAssignment } from "../services/assignmentService";
import useRole from "../hooks/useRole";
import AssignmentList from "../components/assignments/AssignmentList.jsx";
import AssignmentForm from "../components/assignments/AssignmentForm.jsx";
import AssignmentDetails from "../components/assignments/AssignmentDetails.jsx";
import Spinner from "../components/common/Spinner.jsx";

export default function Assignments() {
  const { canCreateAssignment } = useRole();
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState(false);
  const [selected, setSelected] = useState(null);
  const [editing, setEditing] = useState(null);

  function refresh() {
    setLoading(true);
    setLoadError("");
    getAssignments()
      .then(setAssignments)
      .catch((err) => setLoadError(err.message || "Could not load assignments"))
      .finally(() => setLoading(false));
  }

  useEffect(refresh, []);

  async function handleEdit(id, data) {
    await updateAssignment(id, data);
    setEditing(null);
    refresh();
  }

  async function handleDelete(id, title) {
  const displayTitle = title || "this assignment";
  if (!window.confirm(`Delete "${displayTitle}"? This can't be undone.`)) return;
  try {
    await deleteAssignment(id);
    toast.success("Assignment deleted");
    refresh();
  } catch (err) {
    toast.error(err.message || "Could not delete assignment");
  }
}

  const q = search.trim().toLowerCase();
  const filtered = q
    ? assignments.filter((a) =>
        [a.title, a.by].filter(Boolean).join(" ").toLowerCase().includes(q)
      )
    : assignments;

  return (
    <div>
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h1 className="font-serif text-[26px] font-semibold text-ink">Assignments</h1>
        {canCreateAssignment && (
          <button
            onClick={() => setModal(true)}
            className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
          >
            <Plus size={12} /> New assignment
          </button>
        )}
      </div>

      <div className="mb-5 relative max-w-md">
        <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate" />
        <label htmlFor="assignment-search" className="sr-only">Search assignments</label>
        <input
          id="assignment-search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search title or assigned by…"
          className="w-full border border-hairline rounded-sm pl-9 pr-3 py-2 text-[13px] text-ink bg-paper-raised"
        />
      </div>

      {modal && (
        <AssignmentForm
          onClose={() => setModal(false)}
          onSubmit={async (data) => {
            await createAssignment(data);
            refresh();
          }}
        />
      )}
      {editing && (
        <AssignmentForm
          initialData={editing}
          mode="edit"
          onClose={() => setEditing(null)}
          onSubmit={(data) => handleEdit(editing.id, data)}
        />
      )}
      {selected && <AssignmentDetails assignment={selected} onClose={() => setSelected(null)} />}

      {loading ? (
        <Spinner label="Loading assignments…" />
      ) : loadError ? (
        <div role="alert" className="text-center py-10 border border-hairline rounded-sm bg-urgent/5">
          <AlertTriangle className="mx-auto text-urgent mb-2" size={28} />
          <p className="text-[13.5px] text-ink mb-3">{loadError}</p>
          <button onClick={refresh} className="font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]">
            Retry
          </button>
        </div>
      ) : (
        <AssignmentList
          assignments={filtered}
          canDelete={canCreateAssignment}
          canEdit={canCreateAssignment}
          onEdit={setEditing}
          onDelete={(id) => handleDelete(id, assignments.find((a) => a.id === id)?.title)}
          onSelect={setSelected}
        />
      )}
    </div>
  );
}