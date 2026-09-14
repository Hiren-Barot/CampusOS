import React from "react";
import { useEffect, useState } from "react";
import { Megaphone, ClipboardList, AlertTriangle } from "lucide-react";
import { getNotices } from "../../services/noticeService";
import { getAssignments } from "../../services/assignmentService";
import { getUnreadCount } from "../../services/notificationService";
import StatCard from "./StatCard.jsx";
import NoticeList from "../notices/NoticeList.jsx";
import AssignmentList from "../assignments/AssignmentList.jsx";
import Spinner from "../common/Spinner.jsx";

export default function StudentDashboard() {
  const [notices, setNotices] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  function refresh() {
    setLoading(true);
    setLoadError("");
    Promise.all([
      getNotices(),
      getAssignments(),
      getUnreadCount().catch(() => 0),
    ])
      .then(([n, a, c]) => {
        setNotices(n);
        setAssignments(a);
        setUnreadCount(c);
      })
      .catch((err) => setLoadError(err.message || "Could not load your dashboard"))
      .finally(() => setLoading(false));
  }

  useEffect(refresh, []);

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
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-7">
        <StatCard label="NEW NOTICES" value={notices.length} />
        <StatCard label="UPCOMING ASSIGNMENTS" value={assignments.length} />
        <StatCard label="UNREAD" value={unreadCount} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="bg-paper-raised border border-hairline rounded-sm">
          <div className="flex items-center gap-2 px-5 py-4 border-b border-hairline">
            <Megaphone size={16} className="text-urgent" />
            <span className="font-serif text-[16px] font-semibold text-ink">Recent notices</span>
          </div>
          <div className="p-4">
            <NoticeList notices={notices.slice(0, 3)} canDelete={false} />
          </div>
        </div>

        <div className="bg-paper-raised border border-hairline rounded-sm">
          <div className="flex items-center gap-2 px-5 py-4 border-b border-hairline">
            <ClipboardList size={16} className="text-urgent" />
            <span className="font-serif text-[16px] font-semibold text-ink">Upcoming deadlines</span>
          </div>
          <div className="p-4">
            <AssignmentList assignments={assignments} canDelete={false} />
          </div>
        </div>
      </div>
    </>
  );
}