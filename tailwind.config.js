/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    
    extend: {
      fontFamily: {
        rubik : ['Rubik, sans-serif'],
      }
    },
    colors: {
      ufcred: '#d20a0a',
      white: '#ffffff',
      lightgray: '#DCDCDC',
      darkred: '#8B0000'
    }

  },
  plugins: [],
}