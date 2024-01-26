/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    fontFamily: {
      "poppins": ["Poppins", "sans-serif"]
    },
    extend: {
      colors: {
        "accent": "#FF4F00",
        "bg": "#FFFFFF",
        "fg": "#000000",
        "divider": "#D1D5DB"
      }
    },
  },
  plugins: [],
}

