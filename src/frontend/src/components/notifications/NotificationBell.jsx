import React from "react";
import { useEffect, useRef, useState } from "react";
import { Bell } from "lucide-react";
import { getNotifications, getUnreadCount, markAllAsRead } from "../../services/notificationService";
import NotificationPanel from "./NotificationPanel.jsx";

export default function NotificationBell() {
  const [open, setOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const ref = useRef(null);

  useEffect(() => {
    getNotifications()
      .then((all) => setNotifications(all.slice(0, 5)))
      .catch(() => setNotifications([]));

    getUnreadCount()
      .then(setUnreadCount)
      .catch(() => setUnreadCount(0));
  }, []);

  useEffect(() => {
    function handleClickOutside(e) {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    }
    if (open) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  function handleToggle() {
    setOpen((o) => {
      const next = !o;
      if (next) {
        markAllAsRead()
          .then(() => setUnreadCount(0))
          .catch(() => {});
      }
      return next;
    });
  }

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={handleToggle}
        className="relative"
        aria-label={unreadCount > 0 ? `Notifications, ${unreadCount} unread` : "Notifications"}
      >
        <Bell size={18} className="text-ink" />
        {unreadCount > 0 && (
          <span className="absolute -top-1.5 -right-1.5 min-w-[14px] h-[14px] px-[3px] rounded-full bg-urgent text-white text-[9px] font-mono font-medium flex items-center justify-center">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>
      {open && <NotificationPanel notifications={notifications} />}
    </div>
  );
}