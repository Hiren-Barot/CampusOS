import React, { useEffect, useState } from "react";
import { Plus, AlertTriangle, Search } from "lucide-react";
import toast from "react-hot-toast";
import {
  getQueries,
  createQuery,
  deleteQuery,
} from "../services/queryService";
import useAuth from "../hooks/useAuth";
import QueryList from "../components/queries/QueryList.jsx";
import QueryForm from "../components/queries/QueryForm.jsx";
import QueryDetails from "../components/queries/QueryDetails.jsx";
import Spinner from "../components/common/Spinner.jsx";

export default function Queries() {
  const { user } = useAuth();
  const [queries, setQueries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState(false);
  const [selected, setSelected] = useState(null);

  const isStudent = user?.role === "student";
  const canReply = ["faculty", "hod"].includes(user?.role);

  function refresh() {
    setLoading(true);
    setLoadError("");
    getQueries()
      .then(setQueries)
      .catch((err) => setLoadError(err.message || "Could not load queries"))
      .finally(() => setLoading(false));
  }

  useEffect(refresh, []);

const canDelete = (q) => isStudent && q.student_id === user?.id && q.status === "open";

  async function handleDelete(id, title) {
    if (!window.confirm(`Delete "${title}"? This can't be undone.`)) return;
    try {
      await deleteQuery(id);
      toast.success("Query deleted");
      refresh();
    } catch (err) {
      toast.error(err.message || "Could not delete query");
    }
  }

  const q = search.trim().toLowerCase();
  const filtered = q
    ? queries.filter((item) =>
        [item.title, item.description, item.student_name]
          .filter(Boolean)
          .join(" ")
          .toLowerCase()
          .includes(q)
      )
    : queries;

  return (
    <div>
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h1 className="font-serif text-[26px] font-semibold text-ink">Queries</h1>
        {isStudent && (
          <button
            onClick={() => setModal(true)}
            className="flex items-center gap-1 font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
          >
            <Plus size={12} /> Ask a Question
          </button>
        )}
      </div>

      <div className="mb-5 relative max-w-md">
        <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate" />
        <label htmlFor="query-search" className="sr-only">Search queries</label>
        <input
          id="query-search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder={isStudent ? "Search your queries…" : "Search title or student…"}
          className="w-full border border-hairline rounded-sm pl-9 pr-3 py-2 text-[13px] text-ink bg-paper-raised"
        />
      </div>

      {modal && (
        <QueryForm
          onClose={() => setModal(false)}
          onSubmit={async (data) => {
            await createQuery(data);
            refresh();
          }}
        />
      )}

      {selected && (
        <QueryDetails
          query={selected}
          onClose={() => setSelected(null)}
          onReplied={() => {
            refresh();
            setSelected(null);
          }}
          canReply={canReply}
        />
      )}

      {loading ? (
        <Spinner label="Loading queries…" />
      ) : loadError ? (
        <div role="alert" className="text-center py-10 border border-hairline rounded-sm bg-urgent/5">
          <AlertTriangle className="mx-auto text-urgent mb-2" size={28} />
          <p className="text-[13.5px] text-ink mb-3">{loadError}</p>
          <button
            onClick={refresh}
            className="font-mono text-[11px] font-medium px-3 py-[6px] rounded-sm text-white bg-[#1B2430]"
          >
            Retry
          </button>
        </div>
      ) : (
        <QueryList
          queries={filtered}
          onSelect={setSelected}
          onDelete={handleDelete}
          canDelete={canDelete}
        />
      )}
    </div>
  );
}