/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0B0F19",
        card: "#141A24",
        primary: "#4F46E5",
        accent: "#7C3AED",
        text: "#F8FAFC",
        muted: "#94A3B8",
      },
      borderRadius: {
        xl2: "1rem",
      },
    },
  },
  plugins: [],
};
