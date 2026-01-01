import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, getUserInfo } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.user_type === 'admin')
  const isTeacher = computed(() => userInfo.value?.user_type === 'teacher')
  const isStudent = computed(() => userInfo.value?.user_type === 'student')

  // 登录
  const login = async (username, password, userType) => {
    try {
      const response = await loginApi(username, password, userType)
      if (response.code === 200) {
        token.value = response.data.token
        userInfo.value = response.data.user
        
        // 保存到本地存储
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('userInfo', JSON.stringify(response.data.user))
        
        return { success: true }
      } else {
        return { success: false, message: response.msg }
      }
    } catch (error) {
      return { success: false, message: error.message || '登录失败' }
    }
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const response = await getUserInfo()
      if (response.code === 200) {
        userInfo.value = response.data
        localStorage.setItem('userInfo', JSON.stringify(response.data))
        return { success: true }
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
      return { success: false }
    }
  }

  // 登出
  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    isAdmin,
    isTeacher,
    isStudent,
    login,
    fetchUserInfo,
    logout
  }
})

