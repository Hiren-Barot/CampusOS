import React from "react";
import { X } from "lucide-react";
import Modal from "../common/Modal.jsx";

const PERSONAL = [
  { key: "phone", label: "PHONE" },
  { key: "gender", label: "GENDER" },
  { key: "date_of_birth", label: "DATE OF BIRTH" },
  { key: "address", label: "ADDRESS" },
];

const STUDENT = [
  { key: "enrollment_no", label: "ENROLLMENT NO" },
  { key: "course", label: "COURSE" },
  { key: "semester", label: "SEMESTER" },
  { key: "admission_year", label: "ADMISSION YEAR" },
  { key: "parent_name", label: "PARENT NAME" },
  { key: "parent_phone", label: "PARENT PHONE" },
];

const FACULTY = [
  { key: "qualification", label: "QUALIFICATION" },
  { key: "specialization", label: "SPECIALIZATION" },
  { key: "experience_years", label: "EXPERIENCE (YEARS)" },
  { key: "joining_date", label: "JOINING DATE" },
  { key: "designation", label: "DESIGNATION" },
];

export default function UserDetails({ user, onClose }) {
  const titleId = "user-details-title";
  if (!user) return null;

  const role = (user.role || "").toLowerCase();
  const isStudent = role === "student";
  const isFacultyRole = ["faculty", "hod", "principal"].includes(role);
  const profile = user.profile || {};

  return (
    <Modal titleId={titleId} onClose={onClose} maxWidth="600px">
      <div className="flex items-center justify-between mb-5">
        <span id={titleId} className="font-serif text-[18px] font-semibold text-ink">
          User Details
        </span>
        <button type="button" onClick={onClose} aria-label="Close">
          <X size={16} className="text-slate" />
        </button>
      </div>

      <div className="flex flex-col gap-5 max-h-[65vh] overflow-y-auto pr-1">
        <div>
          <p className="font-mono text-[10.5px] tracking-wide text-slate mb-3">ACCOUNT</p>
          <div className="grid grid-cols-2 gap-x-4 gap-y-3">
            <ReadField label="NAME" value={user.full_name || user.name} />
            <ReadField label="EMAIL" value={user.email} />
            <ReadField label="ROLE" value={user.role} capitalize />
            <ReadField label="DEPARTMENT" value={user.department_name || user.dept || "—"} />
            <ReadField label="STATUS" value={user.is_active ? "Active" : "Inactive"} />
          </div>
        </div>

        <div className="border-t border-hairline pt-4">
          <p className="font-mono text-[10.5px] tracking-wide text-slate mb-3">
            PERSONAL INFORMATION
          </p>
          <div className="grid grid-cols-2 gap-x-4 gap-y-3">
            {PERSONAL.map((f) => (
              <ReadField key={f.key} label={f.label} value={profile[f.key]} />
            ))}
          </div>
        </div>

        {isStudent && (
          <div className="border-t border-hairline pt-4">
            <p className="font-mono text-[10.5px] tracking-wide text-slate mb-3">
              STUDENT DETAILS
            </p>
            <div className="grid grid-cols-2 gap-x-4 gap-y-3">
              {STUDENT.map((f) => (
                <ReadField key={f.key} label={f.label} value={profile[f.key]} />
              ))}
            </div>
          </div>
        )}

        {isFacultyRole && (
          <div className="border-t border-hairline pt-4">
            <p className="font-mono text-[10.5px] tracking-wide text-slate mb-3">
              FACULTY DETAILS
            </p>
            <div className="grid grid-cols-2 gap-x-4 gap-y-3">
              {FACULTY.map((f) => (
                <ReadField key={f.key} label={f.label} value={profile[f.key]} />
              ))}
            </div>
          </div>
        )}
      </div>

      <button
        onClick={onClose}
        className="w-full mt-6 rounded-sm py-2 text-[13px] font-medium text-white bg-[#1B2430]"
      >
        Close
      </button>
    </Modal>
  );
}

function ReadField({ label, value, capitalize }) {
  const display =
    value === null || value === undefined || value === ""
      ? "—"
      : String(value);
  return (
    <div>
      <p className="font-mono text-[10px] tracking-wide text-slate mb-1">{label}</p>
      <p className={`text-[13px] text-ink ${capitalize ? "capitalize" : ""}`}>
        {display}
      </p>
    </div>
  );
}