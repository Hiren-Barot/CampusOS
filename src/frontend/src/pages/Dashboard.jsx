import React from "react";
import useRole from "../hooks/useRole";
import StudentDashboard from "../components/dashboard/StudentDashboard.jsx";
import FacultyDashboard from "../components/dashboard/FacultyDashboard.jsx";
import HODDashboard from "../components/dashboard/HODDashboard.jsx";
import PrincipalDashboard from "../components/dashboard/PrincipalDashboard.jsx";
import AdminDashboard from "../components/dashboard/AdminDashboard.jsx";

const BY_ROLE = {
  student: StudentDashboard,
  faculty: FacultyDashboard,
  hod: HODDashboard,
  principal: PrincipalDashboard,
  admin: AdminDashboard,
};

export default function Dashboard() {
  const { role } = useRole();
  const RoleDashboard = BY_ROLE[role];

  return (
    <div>
      <div className="mb-6">
        <div className="font-mono text-[11px] tracking-wide mb-1 text-urgent">● {role?.toUpperCase()} VIEW</div>
        <h1 className="font-serif text-[26px] font-semibold text-ink">Dashboard</h1>
      </div>
      {RoleDashboard ? <RoleDashboard /> : <p className="text-slate">Unknown role.</p>}
    </div>
  );
}
