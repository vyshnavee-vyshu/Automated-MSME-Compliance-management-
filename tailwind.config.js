/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#f4f6f9',
          100: '#e6eaf1',
          200: '#c7d0e0',
          300: '#9aa9c4',
          400: '#6a7ea3',
          500: '#4a6084',
          600: '#37496a',
          700: '#293754',
          800: '#1b2740',
          900: '#101a2e',
          950: '#0a1220',
        },
        surface: {
          DEFAULT: '#fbfbfa',
          alt: '#f4f5f7',
        },
      },
      fontFamily: {
        sans: ['"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['"Source Serif 4"', 'Georgia', 'serif'],
      },
      boxShadow: {
        subtle: '0 1px 2px 0 rgba(16, 26, 46, 0.04), 0 1px 3px 0 rgba(16, 26, 46, 0.06)',
        card: '0 1px 3px 0 rgba(16, 26, 46, 0.06), 0 4px 12px -2px rgba(16, 26, 46, 0.06)',
        raised: '0 4px 16px -4px rgba(16, 26, 46, 0.12), 0 2px 6px -2px rgba(16, 26, 46, 0.08)',
      },
      borderRadius: {
        md: '8px',
        lg: '10px',
        xl: '14px',
      },
    },
  },
  plugins: [],
}
