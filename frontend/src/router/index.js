import { createRouter, createWebHistory } from 'vue-router'
import LaboratoryList from '@/views/LaboratoryList.vue'

const routes = [
  {
    path: '/',
    redirect: '/laboratories'
  },
  {
    path: '/laboratories',
    name: 'LaboratoryList',
    component: LaboratoryList,
    meta: {
      title: '实验室管理'
    }
  },
  {
    path: '/equipment',
    name: 'Equipment',
    component: () => import('@/views/Equipment.vue'),
    meta: {
      title: '设备管理'
    }
  },
  {
    path: '/reservations',
    name: 'Reservations',
    component: () => import('@/views/Reservations.vue'),
    meta: {
      title: '预约管理'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 高校仪器预约系统` : '高校仪器预约系统'
  next()
})

export default router

