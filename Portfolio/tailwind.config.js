module.exports = {
  darkMode: 'class',
  content: ['./templates/**/*.html', './static/js/**/*.js'],
  theme: {
    extend: {
      colors: {
        neonBlue: '#3b82f6',
        neonPurple: '#8b5cf6',
        darkBg: '#0d1117',
        lightBg: '#f9fafb',
      },
      fontFamily: {
        sans: ['Poppins', 'Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
