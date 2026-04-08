import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Dev + Docker preview: browser uses /api → proxy to FastAPI (compose service `api` in containers).
const apiProxyTarget = process.env.API_PROXY_TARGET ?? 'http://127.0.0.1:8000'
const apiProxy = {
  '/api': {
    target: apiProxyTarget,
    changeOrigin: true,
    rewrite: (path: string) => path.replace(/^\/api/, ''),
  },
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: apiProxy,
  },
  preview: {
    proxy: apiProxy,
  },
})
