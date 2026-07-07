/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        wiki: {
          bg: '#0f1419',
          panel: '#1a2332',
          border: '#2d3a4f',
          accent: '#5b9fd4',
          glow: '#7ec8e3',
          warn: '#e8a838',
          ok: '#4caf7d',
        },
      },
      fontFamily: {
        sans: ['Segoe UI', 'system-ui', 'sans-serif'],
        mono: ['Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
};
