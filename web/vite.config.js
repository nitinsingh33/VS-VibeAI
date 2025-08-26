import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    hmr: {
      clientPort: 5173
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false
  },
  define: {
    'process.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL || 'http://localhost:8000'),
    'process.env.VITE_ANALYTICS_URL': JSON.stringify(process.env.VITE_ANALYTICS_URL || 'http://localhost:8501'),
    'process.env.VITE_PREMIUM_URL': JSON.stringify(process.env.VITE_PREMIUM_URL || 'http://localhost:8502')
  }
})