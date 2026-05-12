import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/analiz-et': {
        target: 'http://127.0.0.1:8000', // Backend adresin
        changeOrigin: true,
        timeout: 120000, // 2 dakika bekleme süresi (Hata almanı engeller)
      }
    }
  }
})