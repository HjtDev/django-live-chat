/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*/templates/*/*.html',
    './*/templates/*/*/*.html',
    './*/*.py',
    './*/*.js',
    './*/*/*.js',
    './*/*/*/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
