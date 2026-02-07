/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Outfit', 'Inter', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'sans-serif'],
      },
      colors: {
        cream: '#F5F1ED',
        'cream-light': '#FAFAF8',
        'brown': '#2B2520',
        'brown-light': '#3D3630',
        'coral': '#E67E50',
        'coral-dark': '#D96E3F',
        'rust': '#8B6F47',
      },
    },
  },
  plugins: [],
};