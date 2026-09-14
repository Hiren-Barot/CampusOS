import React, { useEffect, useState } from "react";
import { Megaphone, ClipboardList, Plus, AlertTriangle } from "lucide-react";
import toast from "react-hot-toast";
import { getMyNotices, createNotice, updateNotice, deleteNotice } from "../../services/noticeService";
import { getAssignments, createAssignment, updateAssignment, deleteAssignment } from "../../services/assignmentService";
import { getUsersByRole } from "../../services/userService";
import StatCard from "./StatCard.jsx";
import NoticeList from "../notices/NoticeList.jsx";
import NoticeForm from "../notices/NoticeForm.jsx";
import AssignmentList from "../assignments/AssignmentList.jsx";
import AssignmentForm from "../assignments/AssignmentForm.jsx";
import Spinner from "../common/Spinner.jsx";

export default function FacultyDashboard() {
  const [notices, setNotices] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [modal, setModal] = useState(null);
  const [editing, setEditing] = useState(null);

  function refresh() {
    setLoading(true);
    setLoadError("");
    Promise.all([
      getMyNotices(),
      getAssignments(),
      getUsersByRole("student"),
    ])
      .then(([n, a, s]) => {
        setNotices(n);
        setAssignments(a);
        setStudents(s);
      })
      .catch((err) => setLoadError(err.message || "Could not load your dashboard"))
      .finally(() => setLoading(false));
  }

  useEffect(refresh, []);

  async function saveEdit(data) {
    if (editing.type === "notice") await updateNotice(editing.item.id, data);
    else await updateAssignment(editing.item.id, data);
    setEditing(null);
    refresh();
  }

  async function handleDeleteNotice(id) {
    const title = notices.find((n) => n.id === id)?.title || "this notice";
    if (!window.confirm(`Delete "${title}"? This can't be undone.`)) return;
    try {
      await deleteNotice(id);
      toast.success("Notice deleted");
      refresh();
    } catch (err) {
      toast.error(err.message || "Could not delete notice");
    }
  }

  async function handleDeleteAssignment(id) {
    const title = assignments.find((a) => a.id === id)?.title || "this assignment";
    if (!window.confirm(`Delete "${title}"? This can't be undone.`)) return;
    try {
      await deleteAssignment(id);
      toast.success("Assignment deleted");
      refresh();
    } catch (err) {
      toast.error(err.message || "Could not delete assignment");
    }
  }

  if (loading) return <Spinner label="Loading your dashboard…" />;

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
      {modal === "notice" && (
        <NoticeForm
          onClose={() => setModal(null)}
          onSubmit={async (d) => {
            await createNotice(d);
            refresh();
          }}
        />
      )}
      {modal === "assignment" && (
        <AssignmentForm
          onClose={() => setModal(null)}
          onSubmit={async (d) => {
            await createAssignment(d);
            refresh();
          }}
        />
      )}
      {editing?.type === "notice" && (
        <NoticeForm
          initialData={editing.item}
          mode="edit"
          onClose={() => setEditing(null)}
          onSubmit={saveEdit}
        />
      )}
      {editing?.type === "assignment" && (
        <AssignmentForm
          initialData={editing.item}
          mode="edit"
          onClose={() => setEditing(null)}
          onSubmit={saveEdit}
        />
      )}

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-7">
        <StatCard label="MY NOTICES" value={notices.length} />
        <StatCard label="MY ASSIGNMENTS" value={assignments.length} />
        <StatCard label="DEPT. STUDENTS" value={students.length} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="bg-paper-raised border border-hairline rounded-sm">
          <div className="flex items-center justify-between px-5 py-4 border-b border-hairline">
            <div className="flex items-center gap-2">
              <Megaphone size={16} className="text-urgent" />
              <span className="font-serif text-[16px] font-semibold text-ink">My notices</span>
            </div>
            <button
              onClick={() => setModal("notice")}
              className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
            >
              <Plus size={12} /> New notice
            </button>
          </div>
          <div className="p-4">
            <NoticeList
              notices={notices}
              canDelete
              canEdit
              onEdit={(n) => setEditing({ type: "notice", item: n })}
              onDelete={handleDeleteNotice}
            />
          </div>
        </div>

        <div className="bg-paper-raised border border-hairline rounded-sm">
          <div className="flex items-center justify-between px-5 py-4 border-b border-hairline">
            <div className="flex items-center gap-2">
              <ClipboardList size={16} className="text-urgent" />
              <span className="font-serif text-[16px] font-semibold text-ink">My assignments</span>
            </div>
            <button
              onClick={() => setModal("assignment")}
              className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
            >
              <Plus size={12} /> New assignment
            </button>
          </div>
          <div className="p-4">
            <AssignmentList
              assignments={assignments}
              canDelete
              canEdit
              onEdit={(a) => setEditing({ type: "assignment", item: a })}
              onDelete={handleDeleteAssignment}
            />
          </div>
        </div>
      </div>
    </>
  );
}