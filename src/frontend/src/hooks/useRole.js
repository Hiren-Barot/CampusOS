import useAuth from "./useAuth";

const NAV_BY_ROLE = {
  student: ["Dashboard", "Notices", "Assignments", "Profile"],
  faculty: ["Dashboard", "Notices", "Assignments", "Users", "Profile"],
  hod: ["Dashboard", "Users", "Notices", "Assignments", "Profile"],
  principal: ["Dashboard", "Departments", "Users", "Notices", "Profile"],
  admin: ["Dashboard", "Users", "Departments", "Notices", "Profile"],
};

const CAN_CREATE_ASSIGNMENT = ["faculty"];
const CAN_CREATE_NOTICE = ["admin", "principal", "hod", "faculty"];
const CAN_MANAGE_DEPARTMENTS = ["principal", "admin"];

const ROLE_RANK = { student: 1, faculty: 2, hod: 3, principal: 4, admin: 5 };

const CREATABLE_ROLES = {
  faculty: ["student"],
  hod: ["faculty", "student"],
  principal: ["hod", "faculty", "student"],
  admin: ["admin", "principal", "hod", "faculty", "student"],
};

export default function useRole() {
  const { user } = useAuth();
  const role = user?.role;
  const myRank = ROLE_RANK[role] || 0;

  function canManageUser(targetRole, targetUserId) {
    if (!role) return false;
    if (targetUserId && targetUserId === user.id) return false;
    if (role === "admin") return true;
    return myRank > (ROLE_RANK[targetRole] || 0);
  }

  return {
    role,
    myRank,
    navItems: NAV_BY_ROLE[role] || [],
    canCreateNotice: CAN_CREATE_NOTICE.includes(role),
    canCreateAssignment: CAN_CREATE_ASSIGNMENT.includes(role),
    canManageUsers: Boolean(CREATABLE_ROLES[role]),
    canManageDepartments: CAN_MANAGE_DEPARTMENTS.includes(role),
    canManageUser,
    creatableRoles: CREATABLE_ROLES[role] || [],
  };
}