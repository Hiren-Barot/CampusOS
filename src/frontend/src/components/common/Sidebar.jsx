import React from "react";
import PropTypes from "prop-types";
import { NavLink } from "react-router-dom";
import {
  LayoutGrid, Megaphone, ClipboardList, Users, User, Building2, LogOut, X,
} from "lucide-react";
import useAuth from "../../hooks/useAuth";
import useRole from "../../hooks/useRole";

const ICON = {
  Dashboard: LayoutGrid,
  Notices: Megaphone,
  Assignments: ClipboardList,
  Users: Users,
  Departments: Building2,
  Profile: User,
};

const ROUTE = {
  Dashboard: "/dashboard",
  Notices: "/notices",
  Assignments: "/assignments",
  Users: "/users",
  Departments: "/departments",
  Profile: "/profile",
};

export default function Sidebar({ isOpen = false, onClose = () => {} }) {
  const { logout } = useAuth();
  const { navItems } = useRole();

  const content = (
    <>
      <div className="flex-1 overflow-y-auto">
        <div className="px-6 mb-8 flex items-center justify-between">
          <div className="font-serif text-[22px] font-bold text-white">
            Campus<span className="text-urgent">OS</span>
          </div>
          <button onClick={onClose} className="md:hidden text-white/60 hover:text-white" aria-label="Close menu">
            <X size={20} />
          </button>
        </div>
        <nav className="flex flex-col gap-1 px-3">
          {navItems.map((label) => {
            const Icon = ICON[label];
            return (
              <NavLink
                key={label}
                to={ROUTE[label]}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2 rounded-sm text-[13.5px] font-medium transition-colors ${
                    isActive ? "bg-urgent/15 text-white" : "text-white/65 hover:text-white"
                  }`
                }
              >
                <Icon size={16} />
                {label}
              </NavLink>
            );
          })}
        </nav>
      </div>
      <div className="px-6 pt-4 border-t border-white/10 flex-shrink-0">
        <button
          onClick={logout}
          className="flex items-center gap-2 text-[12.5px] font-medium text-white/50 hover:text-white/80 w-full"
        >
          <LogOut size={14} /> Sign out
        </button>
      </div>
    </>
  );

  return (
    <>
      <aside className="hidden md:flex w-[220px] flex-shrink-0 flex-col justify-between py-6 bg-[#1B2430] h-screen sticky top-0">
        {content}
      </aside>

      <div
        className={`md:hidden fixed inset-0 z-40 bg-black/50 transition-opacity ${
          isOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
        }`}
        onClick={onClose}
        aria-hidden="true"
      />
      <aside
        className={`md:hidden fixed inset-y-0 left-0 z-50 w-[240px] flex flex-col justify-between py-6 bg-[#1B2430] transition-transform duration-200 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {content}
      </aside>
    </>
  );
}

Sidebar.propTypes = {
  isOpen: PropTypes.bool,
  onClose: PropTypes.func,
};