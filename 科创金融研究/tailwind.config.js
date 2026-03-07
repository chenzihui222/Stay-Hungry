/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'tech-dark': '#0a0a0f',
        'tech-card': '#12121a',
        'tech-border': '#1e1e2e',
        'tech-accent': '#00d4ff',
        'tech-accent-dim': 'rgba(0, 212, 255, 0.1)',
        'tech-text': '#e0e0e0',
        'tech-text-muted': '#888888',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
