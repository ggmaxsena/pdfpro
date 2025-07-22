/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      colors:{
        sedam:{
          DEFAULT:'#006C3A',
          dark:'#004F2A',
          blue:'#003B7A',
          yellow:'#FFD600'
        }
      },
      fontFamily:{
        sans:['Inter','Roboto','sans-serif']
      },
      container:{
        center:true,
        padding:'1rem'
      }
    },
  },
  plugins: [],
}