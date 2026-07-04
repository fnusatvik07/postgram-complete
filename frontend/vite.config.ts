import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// The dev server proxies /api to the FastAPI backend so the frontend can use
// same-origin relative URLs (see src/api/client.ts).
// Override the backend port with VITE_API_TARGET, e.g. when 8000 is taken:
//   VITE_API_TARGET=http://localhost:8001 npm run dev
const apiTarget = process.env.VITE_API_TARGET || 'http://localhost:8000';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: apiTarget,
        changeOrigin: true,
      },
    },
  },
});
