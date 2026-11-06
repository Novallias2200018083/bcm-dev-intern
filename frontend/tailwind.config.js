/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cimb: {
          50: '#fdf2f3',
          100: '#fce7e9',
          200: '#f8c8cd',
          300: '#f199a3',
          400: '#e45e6f',
          500: '#d12e43',
          600: '#b51a30',
          700: '#971224',
          800: '#7e1322', // Official CIMB Deep Burgundy Red
          900: '#681420',
          950: '#3b050d',
        },
        octo: {
          50: '#ecfdf5',
          100: '#d1fae5',
          500: '#10b981',
          600: '#008752', // OCTO Green
          700: '#047857',
        }
      }
    },
  },
  plugins: [],
}
