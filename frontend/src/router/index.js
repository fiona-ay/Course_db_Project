import { createRouter, createWebHistory } from 'vue-router'
import LaboratoryList from '@/views/LaboratoryList.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/laboratories',
    name: 'LaboratoryList',
    component: LaboratoryList,
    meta: { title: '实验室管理' }
  },
  {
    path: '/equipment',
    name: 'Equipment',
    component: () => import('@/views/Equipment.vue'),
    meta: { title: '设备列表', requiresAuth: true }
  },
  {
    path: '/equipment/:id',
    name: 'EquipmentDetail',
    component: () => import('@/views/EquipmentDetail.vue'),
    meta: { title: '设备详情', requiresAuth: true }
  },
  {
    path: '/reservations',
    name: 'Reservations',
    component: () => import('@/views/Reservations.vue'),
    meta: { title: '预约管理' }
  },

  // --- 以下是模块6需要插入的部分 ---
  {
    path: '/help',
    name: 'Help',
    component: () => import('@/views/Help.vue'), // 确保你已经在 views 目录下创建了 Help.vue
    meta: { title: '帮助中心' }
  },
  {
    // 通配符路由，匹配所有不在上面的路径，必须放在最后
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'), // 确保你创建了 NotFound.vue
    meta: { title: '404 - 页面未找到' }
  }
  // ------------------------------
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ... 后面的 beforeEach 守卫代码保持不变

import { useUserStore } from '@/stores/user'

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 高校大型仪器设备共享服务平台` : '高校大型仪器设备共享服务平台'
  
  // 检查是否需要登录
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    // 需要登录但未登录，跳转到首页
    next('/')
  } else {
    next()
  }
})

export default router

