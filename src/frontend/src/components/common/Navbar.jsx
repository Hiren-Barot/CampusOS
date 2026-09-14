import React from "react";
import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { Search, Menu, Sun, Moon } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import NotificationBell from "../notifications/NotificationBell.jsx";

const INITIALS = {
  student: "ST", faculty: "FA", hod: "HD", principal: "PR", admin: "AD",
};

const THEME_KEY = "campos_theme";

export default function Navbar({ onMenuClick = () => {} }) {
  const { user } = useAuth();
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  const [isDark, setIsDark] = useState(() => {
    if (typeof window === "undefined") return false;
    const stored = localStorage.getItem(THEME_KEY);
    if (stored) return stored === "dark";
    return window.matchMedia?.("(prefers-color-scheme: dark)").matches ?? false;
  });

  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDark);
    localStorage.setItem(THEME_KEY, isDark ? "dark" : "light");
  }, [isDark]);

  function handleSearch(e) {
    e.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) return;
    navigate(`/notices?search=${encodeURIComponent(trimmed)}`);
  }

  return (
    <div className="flex items-center justify-between px-4 md:px-8 py-4 border-b border-hairline bg-paper-raised">
      <div className="flex items-center gap-3">
        <button onClick={onMenuClick} className="md:hidden text-ink" aria-label="Open menu">
          <Menu size={22} />
        </button>

        <form onSubmit={handleSearch} className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-sm border border-hairline w-[220px] md:w-[280px]">
          <Search size={14} className="text-slate" />
          <input
            className="font-mono text-[12px] outline-none w-full bg-transparent text-ink"
            placeholder="Search notices…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </form>
      </div>

      <div className="flex items-center gap-3 md:gap-5">
        <button
          onClick={() => setIsDark((d) => !d)}
          className="text-ink hover:text-urgent transition-colors"
          aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
        >
          {isDark ? <Sun size={18} /> : <Moon size={18} />}
        </button>

        <NotificationBell />

        <Link
          to="/profile"
          className="flex items-center gap-2 hover:opacity-80 transition-opacity"
          aria-label="Go to profile"
        >
          <div className="w-8 h-8 rounded-full flex items-center justify-center font-mono text-[11px] font-medium text-white bg-[#1B2430]">
            {INITIALS[user?.role] || "?"}
          </div>
          <span className="hidden sm:inline text-[13px] font-medium text-ink capitalize">
            {user?.role}
          </span>
        </Link>
      </div>
    </div>
  );
}

Navbar.propTypes = {
  onMenuClick: PropTypes.func,
};
