function parseDate(input) {
  if (!input) return null;
  if (input instanceof Date) return input;

  const str = String(input).trim();

  if (str.endsWith("Z") || /[+-]\d{2}:?\d{2}$/.test(str)) {
    return new Date(str);
  }

  let normalized = str.includes(" ") ? str.replace(" ", "T") : str;

  normalized = normalized + "Z";

  const d = new Date(normalized);
  return Number.isNaN(d.getTime()) ? null : d;
}

export function timeAgo(input) {
  const d = parseDate(input);
  if (!d) return "JUST NOW";

  const diffMs = Date.now() - d.getTime();

  if (diffMs < 0) return "JUST NOW";

  const secs = Math.floor(diffMs / 1000);
  if (secs < 45) return "JUST NOW";

  const mins = Math.floor(secs / 60);
  if (mins < 60) return `${mins} MIN AGO`;

  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs} HR${hrs > 1 ? "S" : ""} AGO`;

  const days = Math.floor(hrs / 24);
  if (days < 7) return `${days} DAY${days > 1 ? "S" : ""} AGO`;

  const weeks = Math.floor(days / 7);
  if (weeks < 5) return `${weeks} WEEK${weeks > 1 ? "S" : ""} AGO`;

  const months = Math.floor(days / 30);
  return `${months} MONTH${months > 1 ? "S" : ""} AGO`;
}

export function shortDate(input) {
  if (!input) return "TBD";
  const d = parseDate(input);
  if (!d) return "TBD";
  return d
    .toLocaleDateString("en-GB", { day: "2-digit", month: "short" })
    .toUpperCase();
}

export function dateInputToISO(dateInputValue) {
  if (!dateInputValue) return null;
  const d = new Date(`${dateInputValue}T23:59:00`);
  return d.toISOString();
}

export function isoToDateInput(input) {
  if (!input) return "";
  const d = parseDate(input);
  if (!d) return "";
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}