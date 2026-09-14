import React from "react";
import PropTypes from "prop-types";

export default function StatCard({ label, value }) {
  return (
    <div className="bg-paper-raised border border-hairline rounded-sm px-5 py-4">
      <div className="font-serif text-3xl font-bold text-ink">{value}</div>
      <div className="font-mono text-[10.5px] tracking-wide mt-1 text-slate">{label}</div>
    </div>
  );
}

StatCard.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
};
