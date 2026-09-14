import React from "react";

export default function Spinner({ label = "Loading…" }) {
  return (
    <div className="flex items-center gap-2 text-slate py-8 justify-center">
      <span className="w-4 h-4 border-2 border-hairline border-t-urgent rounded-full animate-spin" />
      <span className="font-mono text-[11.5px]">{label}</span>
    </div>
  );
}
