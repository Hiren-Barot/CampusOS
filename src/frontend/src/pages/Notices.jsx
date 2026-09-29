import React, { useEffect, useState } from "react";
import { Plus, AlertTriangle } from "lucide-react";
import toast from "react-hot-toast";
import {
  getNotices,
  createNotice,
  updateNotice,
  deleteNotice,
} from "../services/noticeService";
import useRole from "../hooks/useRole";
import useAuth from "../hooks/useAuth";
import NoticeList from "../components/notices/NoticeList.jsx";
import NoticeForm from "../components/notices/NoticeForm.jsx";
import NoticeDetails from "../components/notices/NoticeDetails.jsx";
import Spinner from "../components/common/Spinner.jsx";

export default function Notices() {
  const { canCreateNotice } = useRole();
  const { user } = useAuth();
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [modal, setModal] = useState(false);
  const [selected, setSelected] = useState(null);
  const [editing, setEditing] = useState(null);

  function refresh() {
    setLoading(true);
    setLoadError("");
    getNotices()
      .then(setNotices)
      .catch((err) => setLoadError(err.message || "Could not load notices"))
      .finally(() => setLoading(false));
  }

  useEffect(refresh, []);

  async function handleEdit(id, data) {
    await updateNotice(id, data);
    setEditing(null);
    refresh();
  }

  async function handleDelete(id, title) {
    const displayTitle = title || "this notice";
    if (!window.confirm(`Delete "${displayTitle}"? This can't be undone.`)) return;
    try {
      await deleteNotice(id);
      toast.success("Notice deleted");
      refresh();
    } catch (err) {
      toast.error(err.message || "Could not delete notice");
    }
  }

  // ✅ Only the original author can edit or delete
  const isAuthor = (notice) => {
    const authorId =
      notice.faculty_id ??
      notice.author_id ??
      notice.created_by ??
      notice.user_id ??
      notice.user?.id;

    // Compare loosely to handle string vs number mismatch
    return user?.id != null && authorId != null && String(authorId) === String(user.id);
  };

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="font-serif text-[26px] font-semibold text-ink">Notices</h1>
        {canCreateNotice && (
          <button
            onClick={() => setModal(true)}
            className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
          >
            <Plus size={12} /> New notice
          </button>
        )}
      </div>

      {modal && (
        <NoticeForm
          onClose={() => setModal(false)}
          onSubmit={async (data) => {
            await createNotice(data);
            refresh();
          }}
        />
      )}
      {editing && (
        <NoticeForm
          initialData={editing}
          mode="edit"
          onClose={() => setEditing(null)}
          onSubmit={(data) => handleEdit(editing.id, data)}
        />
      )}
      {selected && <NoticeDetails notice={selected} onClose={() => setSelected(null)} />}

      {loading ? (
        <Spinner label="Loading notices…" />
      ) : loadError ? (
        <div role="alert" className="text-center py-10 border border-hairline rounded-sm bg-urgent/5">
          <AlertTriangle className="mx-auto text-urgent mb-2" size={28} />
          <p className="text-[13.5px] text-ink mb-3">{loadError}</p>
          <button onClick={refresh} className="font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]">
            Retry
          </button>
        </div>
      ) : (
        <NoticeList
          notices={notices}
          canEdit={isAuthor}
          canDelete={isAuthor}
          onEdit={setEditing}
          onDelete={(id) => handleDelete(id, notices.find((n) => n.id === id)?.title)}
          onSelect={setSelected}
        />
      )}
    </div>
  );
}