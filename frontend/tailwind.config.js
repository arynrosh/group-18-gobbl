/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['Fredoka', 'ui-rounded', 'system-ui', 'sans-serif'],
        sans: ['Nunito', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        gobbl: {
          cream: '#fff8ef',
          peach: '#ffe5d4',
          tomato: '#ff5c4d',
          mango: '#ffb347',
          lemon: '#ffe566',
          mint: '#3ecf9b',
          teal: '#2bb3c0',
          ink: '#2d2a32',
        },
      },
    },
  },
  plugins: [],
}
