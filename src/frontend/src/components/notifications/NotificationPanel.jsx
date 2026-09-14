import React from "react";

export default function NotificationPanel({ notifications }) {
  return (
    <div className="absolute right-0 top-8 w-[280px] bg-paper-raised border border-hairline rounded-sm shadow-lg z-40 max-h-[400px] overflow-y-auto">
      <div className="px-4 py-3 border-b border-hairline font-mono text-[10.5px] tracking-wide text-slate sticky top-0 bg-paper-raised">
        NOTIFICATIONS
      </div>
      {notifications.length === 0 && (
        <div className="px-4 py-3 text-[12.5px] text-slate">No notifications yet.</div>
      )}
      {notifications.map((n) => (
        <div
          key={n.id}
          className="px-4 py-3 border-b border-hairline text-[12.5px] text-ink flex items-start gap-2"
        >
          {!n.is_read && (
            <span className="mt-1.5 w-[6px] h-[6px] rounded-full bg-urgent flex-shrink-0" aria-hidden="true" />
          )}
          <div className="flex-1">
            <div className={`font-medium ${n.is_read ? "text-slate" : "text-ink"}`}>{n.title}</div>
            {n.message && <div className="text-[11.5px] text-slate mt-0.5">{n.message}</div>}
          </div>
        </div>
      ))}
    </div>
  );
}