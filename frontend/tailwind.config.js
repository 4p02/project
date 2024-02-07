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
      // colors: {
      //   "accent": "#FF4F00",
      //   "bg": "#FFFFFF",
      //   "fg": "#000000",
      //   "divider": "#D1D5DB"
      // }
      screens: {
        "phablet-max": {max: "599px"},
        "lg-max": {max: "1024px"},
        phablet: '600px',
      }
    },
  },
  plugins: [],
}

