/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: "class",
  theme: {
    fontFamily: {
      "poppins": ["Poppins", "sans-serif"]
    },
    extend: {
      colors: {
        "dark-complement": "#333333",
        "dark": "#191919",
        "dark-light": "#4D4D4D",
        "light": "#F8F8F8",
        "light-gray": "#D1D5DB",
        "dark-gray": "#818181"
      },
      screens: {
        "phablet-max": {max: "599px"},
        "lg-max": {max: "1024px"},
        phablet: '600px',
      }
    },
  },
  plugins: [],
}

