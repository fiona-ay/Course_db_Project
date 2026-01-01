import request from './request'

/**
 * 设备 API
 */

/**
 * 获取设备列表
 * @param {object} params - 查询参数
 * @param {number} params.lab_id - 实验室ID（可选）
 * @param {string} params.keyword - 关键词搜索（可选）
 * @param {string} params.category - 设备类别（可选）
 * @param {string} params.status - 设备状态（可选）
 * @param {number} params.page - 页码（可选）
 * @param {number} params.page_size - 每页数量（可选）
 */
export function getEquipmentList(params = {}) {
  return request({
    url: '/equipments/',  // 确保末尾有斜杠，避免 Flask 重定向
    method: 'get',
    params
  })
}

/**
 * 获取设备详情
 * @param {number} id - 设备ID
 */
export function getEquipmentById(id) {
  return request({
    url: `/equipments/${id}`,
    method: 'get'
  })
}

/**
 * 管理员：创建设备
 * @param {object} data - 设备数据
 */
export function createEquipment(data) {
  return request({
    url: '/admin/equipments',
    method: 'post',
    data
  })
}

/**
 * 管理员：更新设备
 * @param {number} id - 设备ID
 * @param {object} data - 设备数据
 */
export function updateEquipment(id, data) {
  return request({
    url: `/admin/equipments/${id}`,
    method: 'put',
    data
  })
}

/**
 * 管理员：删除设备
 * @param {number} id - 设备ID
 */
export function deleteEquipment(id) {
  return request({
    url: `/admin/equipments/${id}`,
    method: 'delete'
  })
}

