import request from './request'

/**
 * 认证 API
 */

/**
 * 用户登录
 * @param {string} username - 学号/工号
 * @param {string} password - 密码
 * @param {string} userType - 用户类型: 'student' | 'teacher' | 'admin'
 */
export function login(username, password, userType) {
  return request({
    url: '/auth/login',
    method: 'post',
    data: {
      username,
      password,
      user_type: userType
    }
  })
}

/**
 * 获取当前用户信息
 */
export function getUserInfo() {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

