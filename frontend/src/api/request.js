import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'

// 创建 axios 实例
// 使用相对路径，让 Vite 代理处理
const service = axios.create({
  baseURL: '/api/v1',  // 相对路径，会通过 Vite 代理
  timeout: 10000,
  // 确保请求头正确设置
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 登录接口和 OPTIONS 预检请求不需要 token
    if (config.url === '/auth/login' || config.method?.toUpperCase() === 'OPTIONS') {
      return config
    }
    
    // 添加 token 认证信息（优先从 localStorage 读取，确保最新）
    const token = localStorage.getItem('token')
    
    if (token) {
      // 确保 Authorization header 包含 Bearer 前缀
      config.headers.Authorization = token.startsWith('Bearer ') ? token : `Bearer ${token}`
      console.log('[DEBUG] 请求添加 token:', config.method, config.url, 'Token:', token.substring(0, 20) + '...')
    } else {
      console.warn('[DEBUG] 请求缺少 token:', config.method, config.url)
      console.warn('[DEBUG] localStorage token:', localStorage.getItem('token'))
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 后端统一响应格式: { code, msg, data }
    if (res.code === 200) {
      return res
    } else {
      // 非 200 状态码，显示错误消息
      ElMessage.error(res.msg || '请求失败')
      return Promise.reject(new Error(res.msg || '请求失败'))
    }
  },
  error => {
    console.error('Response error:', error)
    
    let message = '请求失败'
    
    if (error.response) {
      // 服务器返回了错误状态码
      const res = error.response.data
      message = res?.msg || res?.message || `请求失败 (${error.response.status})`
      
      // 401 未授权，清除token并跳转到登录页
      if (error.response.status === 401) {
        // 使用 store 的 logout 方法，确保状态同步
        const userStore = useUserStore()
        userStore.logout()
        
        // 使用 router 跳转，避免强制刷新
        if (router.currentRoute.value.path !== '/') {
          router.push('/')
        }
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      message = '网络错误，请检查网络连接'
    } else {
      // 其他错误
      message = error.message || '请求失败'
    }
    
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export default service

