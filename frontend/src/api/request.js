import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const service = axios.create({
  baseURL: '/api/v1',
  timeout: 10000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 可以在这里添加 token 等认证信息
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
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

