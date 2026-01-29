/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#6BA368',
        'primary-light': '#a5c9a3',
        'bg-body': '#EAF4F4',
        dark: '#2C3E50'
      }
    },
  },
  plugins: [],
}