import request from './request'

/**
 * 实验室 API
 */

/**
 * 获取实验室列表
 */
export function getLabList() {
  return request({
    url: '/laboratories/',
    method: 'get'
  })
}

/**
 * 获取单个实验室详情
 */
export function getLabById(id) {
  return request({
    url: `/laboratories/${id}`,
    method: 'get'
  })
}

/**
 * 创建实验室
 */
export function createLab(data) {
  return request({
    url: '/laboratories/',
    method: 'post',
    data
  })
}

/**
 * 更新实验室
 */
export function updateLab(id, data) {
  return request({
    url: `/laboratories/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除实验室
 */
export function deleteLab(id) {
  return request({
    url: `/laboratories/${id}`,
    method: 'delete'
  })
}

