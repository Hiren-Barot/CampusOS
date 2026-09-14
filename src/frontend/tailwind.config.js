/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        paper: "rgb(var(--color-paper) / <alpha-value>)",
        "paper-raised": "rgb(var(--color-paper-raised) / <alpha-value>)",
        ink: "rgb(var(--color-ink) / <alpha-value>)",
        slate: "rgb(var(--color-slate) / <alpha-value>)",
        hairline: "rgb(var(--color-hairline) / <alpha-value>)",
        urgent: "rgb(var(--color-urgent) / <alpha-value>)",
        result: "rgb(var(--color-result) / <alpha-value>)",
        event: "rgb(var(--color-event) / <alpha-value>)",
      },
      fontFamily: {
        serif: ["Fraunces", "serif"],
        sans: ["Inter", "sans-serif"],
        mono: ['"JetBrains Mono"', "monospace"],
      },
    },
  },
  plugins: [],
};
