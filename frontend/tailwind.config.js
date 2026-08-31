/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  darkMode: "class",

  theme: {
    extend: {
      colors: {
        brand: {
          50: "#F0FDF4",
          100: "#DCFCE7",
          200: "#BBF7D0",
          300: "#86EFAC",
          400: "#4ADE80",
          500: "#22C55E",
          600: "#16A34A",
          700: "#15803D",
          800: "#166534",
          900: "#14532D",
          950: "#052E16",
        },

        earth: {
          50: "#FEFCE8",
          100: "#FEF9C3",
          200: "#FEF08A",
          300: "#FDE047",
          400: "#FACC15",
          500: "#EAB308",
          600: "#CA8A04",
          700: "#A16207",
          800: "#854D0E",
          900: "#713F12",
        },

        soil: {
          50: "#FAF7F2",
          100: "#F3EDE3",
          200: "#E7DCCB",
          300: "#D6C4AA",
          400: "#BCA384",
          500: "#9F825F",
          600: "#806747",
          700: "#665038",
          800: "#4A3929",
          900: "#30251B",
        },

        success: "#16A34A",
        warning: "#EAB308",
        danger: "#DC2626",
        info: "#0284C7",
      },
    },
  },

  plugins: [],
};