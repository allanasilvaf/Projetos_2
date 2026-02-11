import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  
server: {
    host: true,      // Permite acesso externo (0.0.0.0)
    port: 5174,      // Sua porta
    strictPort: true,
    watch: {
      usePolling: true, // <--- ISSO RESOLVE O SEU PROBLEMA
    },
    hmr: {
      port: 5174, // Garante que o hot reload bata na porta certa
    }
  }
})