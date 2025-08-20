import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: false,
    // allow ngrok subdomains (specific and wildcard)
    allowedHosts: ['1bc1fedec2f5.ngrok-free.app', 'b5836912dbe1.ngrok-free.app', '.ngrok-free.app'],
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
