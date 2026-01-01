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
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        // 确保转发所有请求头，特别是自定义的 Authorization header
        // 使用 rewrite 确保路径正确，同时保持所有 header
        rewrite: (path) => path,
        configure: (proxy, _options) => {
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            // 获取 authorization header（HTTP 头在 Node.js 中是小写）
            const authHeader = req.headers.authorization || req.headers.Authorization
            
            if (authHeader) {
              // 关键：必须在请求发送前设置 Authorization header
              // 直接设置 header，确保它被转发到后端
              proxyReq.setHeader('Authorization', authHeader)
              
              // 验证 header 是否已设置
              const headers = proxyReq.getHeaders()
              const sentAuth = headers.authorization || headers.Authorization
              if (sentAuth) {
                console.log('[VITE PROXY] ✓ Authorization header 已设置并准备发送')
                console.log('[VITE PROXY] 发送的 header 值:', sentAuth.substring(0, 30) + '...')
              } else {
                console.log('[VITE PROXY] ✗ 警告：Authorization header 设置失败')
              }
            } else {
              console.log('[VITE PROXY] 警告：请求中没有 Authorization header')
            }
          })
        }
      }
    }
  }
})

