/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef4ff",
          100: "#d9e6ff",
          200: "#b3ccff",
          300: "#82abff",
          400: "#5285ff",
          500: "#2f63f5",
          600: "#1f49d1",
          700: "#1c3ba8",
          800: "#1c3486",
          900: "#1c306e",
        },
      },
    },
  },
  plugins: [],
};
