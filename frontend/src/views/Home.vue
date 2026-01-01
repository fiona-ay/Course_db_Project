<template>
  <div class="home-page">
    <!-- Hero Section & Login -->
    <section class="hero-section">
      <div class="hero-container">
        <!-- 左侧欢迎区域 -->
        <div class="hero-content">
          <h1 class="hero-title">
            欢迎使用<br />
            <span>高校大型仪器设备共享服务平台</span>
          </h1>
          <p class="hero-subtitle">
            为师生提供便捷、高效的仪器设备预约服务<br />
            让科研更简单，让创新更高效
          </p>
          <div class="hero-illustration">
            <div class="illustration-box box-1"></div>
            <div class="illustration-box box-2"></div>
            <div class="illustration-box box-3"></div>
          </div>
        </div>

        <!-- 右侧登录卡片 -->
        <div class="login-card-wrapper">
          <el-card class="login-card" shadow="hover">
            <template #header>
              <div class="login-header">
                <h3>用户登录</h3>
              </div>
            </template>
            <el-tabs v-model="activeRole" class="role-tabs">
              <el-tab-pane label="学生" name="student">
                <el-icon><User /></el-icon>
              </el-tab-pane>
              <el-tab-pane label="教师" name="teacher">
                <el-icon><Avatar /></el-icon>
              </el-tab-pane>
              <el-tab-pane label="管理员" name="admin">
                <el-icon><Setting /></el-icon>
              </el-tab-pane>
            </el-tabs>
            <el-form :model="loginForm" class="login-form">
              <el-form-item>
                <el-input
                  v-model="loginForm.username"
                  placeholder="请输入学号/工号"
                  size="large"
                  :prefix-icon="UserFilled"
                />
              </el-form-item>
              <el-form-item>
                <el-input
                  v-model="loginForm.password"
                  type="password"
                  placeholder="请输入密码"
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                />
              </el-form-item>
              <el-form-item>
                <el-button 
                  type="primary" 
                  size="large" 
                  class="login-btn" 
                  :loading="loading"
                  @click="handleLogin"
                >
                  {{ loading ? '登录中...' : '登录' }}
                </el-button>
              </el-form-item>
              <el-form-item class="forgot-password">
                <el-link type="primary" :underline="false" @click="handleForgotPassword">
                  忘记密码？
                </el-link>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </div>
    </section>

    <!-- Quick Access 快速入口 -->
    <section class="quick-access">
      <div class="container">
        <div class="quick-access-grid">
          <el-card
            v-for="(item, index) in quickAccessItems"
            :key="index"
            class="access-card"
            shadow="hover"
            @click="handleQuickAccess(item.path)"
          >
            <div class="access-icon" :style="{ background: item.color }">
              <el-icon :size="32"><component :is="item.icon" /></el-icon>
            </div>
            <h3 class="access-title">{{ item.title }}</h3>
            <p class="access-desc">{{ item.description }}</p>
          </el-card>
        </div>
      </div>
    </section>

    <!-- Main Content Grid 主体信息区 -->
    <section class="main-content">
      <div class="container">
        <el-row :gutter="24">
          <!-- 左侧：通知公告 -->
          <el-col :xs="24" :sm="24" :md="16" :lg="16">
            <el-card class="announcements-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <h3>
                    <el-icon><Bell /></el-icon>
                    通知公告
                  </h3>
                  <el-link type="primary" :underline="false" @click="handleMoreAnnouncements">
                    更多 <el-icon><ArrowRight /></el-icon>
                  </el-link>
                </div>
              </template>
              <div class="announcements-list">
                <div
                  v-for="(announcement, index) in announcements"
                  :key="index"
                  class="announcement-item"
                  @click="handleAnnouncementClick(announcement)"
                >
                  <div class="announcement-content">
                    <span class="announcement-title">{{ announcement.title }}</span>
                    <span class="announcement-date">{{ announcement.date }}</span>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>

          <!-- 右侧：热门设备预约排行 -->
          <el-col :xs="24" :sm="24" :md="8" :lg="8">
            <el-card class="equipment-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <h3>
                    <el-icon><Trophy /></el-icon>
                    热门设备预约排行
                  </h3>
                </div>
              </template>
              <el-tabs v-model="activeTimeRange" class="time-tabs">
                <el-tab-pane label="近一周" name="week"></el-tab-pane>
                <el-tab-pane label="近一月" name="month"></el-tab-pane>
              </el-tabs>
              <div class="equipment-list">
                <div
                  v-for="(equipment, index) in topEquipment"
                  :key="index"
                  class="equipment-item"
                  :class="{ 'top-three': index < 3 }"
                >
                  <div class="equipment-rank" :class="getRankClass(index)">
                    {{ index + 1 }}
                  </div>
                  <div class="equipment-info">
                    <span class="equipment-name">{{ equipment.name }}</span>
                    <span class="equipment-count">{{ equipment.count }}次预约</span>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </section>

    <!-- Footer 底部 -->
    <footer class="home-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h4>关于我们</h4>
            <p>高校大型仪器设备共享服务平台</p>
            <p>致力于为师生提供优质的设备预约服务</p>
          </div>
          <div class="footer-section">
            <h4>联系方式</h4>
            <p>电话：010-12345678</p>
            <p>邮箱：support@university.edu.cn</p>
            <p>地址：XX大学XX校区XX楼</p>
          </div>
          <div class="footer-section">
            <h4>技术支持</h4>
            <p>
              <el-link type="primary" :underline="false">使用帮助</el-link>
            </p>
            <p>
              <el-link type="primary" :underline="false">常见问题</el-link>
            </p>
            <p>
              <el-link type="primary" :underline="false">意见反馈</el-link>
            </p>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2024 高校大型仪器设备共享服务平台. 保留所有权利.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  User,
  Avatar,
  Setting,
  UserFilled,
  Lock,
  Calendar,
  Document,
  InfoFilled,
  Trophy,
  Bell,
  ArrowRight
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 登录表单
const loginForm = ref({
  username: '',
  password: ''
})

const activeRole = ref('student')
const loading = ref(false)

// 图标映射
const iconMap = {
  Calendar,
  Document,
  InfoFilled
}

// 快速入口数据
const quickAccessItems = ref([
  {
    title: '仪器预约',
    description: '快速预约所需仪器设备',
    icon: Calendar,
    path: '/reservations',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    title: '规章制度',
    description: '查看设备使用相关规定',
    icon: Document,
    path: '/rules',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    title: '开放流程',
    description: '了解设备预约流程',
    icon: InfoFilled,
    path: '/process',
    color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  }
])

// 通知公告数据
const announcements = ref([
  {
    title: '关于寒假期间设备维护的通知',
    date: '2024-01-15'
  },
  {
    title: '2024年春季学期设备开放时间安排',
    date: '2024-01-10'
  },
  {
    title: '部分设备系统升级维护公告',
    date: '2024-01-08'
  },
  {
    title: '新增高精度显微镜设备开放预约',
    date: '2024-01-05'
  },
  {
    title: '春节期间设备预约服务暂停通知',
    date: '2024-01-03'
  }
])

// 热门设备数据
const topEquipment = ref([
  { name: '扫描电子显微镜 SEM-3000', count: 156 },
  { name: 'X射线衍射仪 XRD-5000', count: 142 },
  { name: '原子力显微镜 AFM-2000', count: 128 },
  { name: '透射电子显微镜 TEM-4000', count: 115 },
  { name: '傅里叶变换红外光谱仪 FTIR-8000', count: 98 },
  { name: '核磁共振波谱仪 NMR-600', count: 87 },
  { name: '激光共聚焦显微镜 CLSM-500', count: 76 },
  { name: '质谱仪 MS-2000', count: 65 }
])

const activeTimeRange = ref('week')

// 处理登录
const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入学号/工号和密码')
    return
  }
  
  loading.value = true
  try {
    const result = await userStore.login(
      loginForm.value.username,
      loginForm.value.password,
      activeRole.value
    )
    
    if (result.success) {
      ElMessage.success('登录成功！')
      // 确保 token 已保存到 localStorage
      const token = localStorage.getItem('token')
      if (!token) {
        ElMessage.error('Token 保存失败，请重新登录')
        return
      }
      console.log('[DEBUG] 登录成功，token 已保存:', token.substring(0, 20) + '...')
      // 等待一下确保状态同步，再跳转
      await new Promise(resolve => setTimeout(resolve, 200))
      // 登录成功后跳转到设备列表页
      router.push('/equipment')
    } else {
      ElMessage.error(result.message || '登录失败')
    }
  } catch (error) {
    ElMessage.error('登录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 处理忘记密码
const handleForgotPassword = () => {
  ElMessage.info('忘记密码功能开发中...')
}

// 处理快速入口点击
const handleQuickAccess = (path) => {
  if (path === '/rules' || path === '/process') {
    ElMessage.info('该功能开发中...')
    return
  }
  router.push(path)
}

// 处理更多公告
const handleMoreAnnouncements = () => {
  ElMessage.info('更多公告功能开发中...')
}

// 处理公告点击
const handleAnnouncementClick = (announcement) => {
  ElMessage.info(`查看公告：${announcement.title}`)
}

// 获取排名样式类
const getRankClass = (index) => {
  if (index === 0) return 'rank-gold'
  if (index === 1) return 'rank-silver'
  if (index === 2) return 'rank-bronze'
  return ''
}
</script>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Hero Section */
.hero-section {
  padding: 60px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>');
    opacity: 0.3;
  }
}

.hero-container {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  position: relative;
  z-index: 1;

  @media (max-width: 968px) {
    grid-template-columns: 1fr;
    gap: 40px;
  }
}

.hero-content {
  color: white;
}

.hero-title {
  font-size: 36px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 20px;
  color: white;

  @media (max-width: 768px) {
    font-size: 24px;
  }
}

.hero-subtitle {
  font-size: 18px;
  line-height: 1.8;
  opacity: 0.95;
  margin-bottom: 40px;

  @media (max-width: 768px) {
    font-size: 16px;
  }
}

.hero-illustration {
  display: flex;
  gap: 20px;
  margin-top: 40px;
}

.illustration-box {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  animation: float 3s ease-in-out infinite;

  &.box-1 {
    animation-delay: 0s;
  }

  &.box-2 {
    animation-delay: 1s;
    width: 100px;
    height: 100px;
  }

  &.box-3 {
    animation-delay: 2s;
  }
}

/* Login Card */
.login-card-wrapper {
  position: relative;
  z-index: 2;
}

.login-card {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: none;
}

.login-header {
  text-align: center;

  h3 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
}

.role-tabs {
  margin-bottom: 20px;

  :deep(.el-tabs__item) {
    font-weight: 500;
  }
}

.login-form {
  .el-form-item {
    margin-bottom: 20px;
  }
}

.login-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;

  &:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  }
}

.forgot-password {
  margin-bottom: 0;
  text-align: center;
}

/* Quick Access */
.quick-access {
  padding: 60px 20px;
  background: #fff;
}

.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;

  @media (max-width: 968px) {
    grid-template-columns: 1fr;
  }
}

.access-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  border-radius: 16px;
  text-align: center;
  padding: 30px 20px;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  }
}

.access-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.access-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.access-desc {
  font-size: 14px;
  color: #666;
  margin: 0;
}

/* Main Content */
.main-content {
  padding: 60px 20px;
  background: #f5f7fa;
}

.announcements-card,
.equipment-card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: #333;
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

.announcements-list {
  .announcement-item {
    padding: 16px 0;
    border-bottom: 1px solid #f0f0f0;
    cursor: pointer;
    transition: all 0.3s ease;

    &:last-child {
      border-bottom: none;
    }

    &:hover {
      background: #f8f9fa;
      padding-left: 8px;
      border-radius: 8px;
    }
  }

  .announcement-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
  }

  .announcement-title {
    flex: 1;
    font-size: 15px;
    color: #333;
    font-weight: 500;
  }

  .announcement-date {
    font-size: 13px;
    color: #999;
    white-space: nowrap;
  }
}

.time-tabs {
  margin-bottom: 20px;
}

.equipment-list {
  .equipment-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 0;
    border-bottom: 1px solid #f0f0f0;

    &:last-child {
      border-bottom: none;
    }

    &.top-three {
      .equipment-rank {
        font-weight: 700;
        font-size: 18px;
      }
    }
  }

  .equipment-rank {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 600;
    color: #666;
    background: #f0f0f0;
    flex-shrink: 0;

    &.rank-gold {
      background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
      color: #fff;
      box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
    }

    &.rank-silver {
      background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
      color: #fff;
      box-shadow: 0 4px 12px rgba(192, 192, 192, 0.4);
    }

    &.rank-bronze {
      background: linear-gradient(135deg, #cd7f32 0%, #e6a857 100%);
      color: #fff;
      box-shadow: 0 4px 12px rgba(205, 127, 50, 0.4);
    }
  }

  .equipment-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .equipment-name {
    font-size: 14px;
    color: #333;
    font-weight: 500;
  }

  .equipment-count {
    font-size: 12px;
    color: #999;
  }
}

/* Footer */
.home-footer {
  background: #2c3e50;
  color: #ecf0f1;
  padding: 60px 20px 30px;

  .footer-content {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 40px;
    margin-bottom: 40px;

    @media (max-width: 768px) {
      grid-template-columns: 1fr;
      gap: 30px;
    }
  }

  .footer-section {
    h4 {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 20px;
      color: #fff;
    }

    p {
      font-size: 14px;
      line-height: 1.8;
      margin-bottom: 10px;
      color: #bdc3c7;

      &:last-child {
        margin-bottom: 0;
      }
    }

    :deep(.el-link) {
      color: #3498db;

      &:hover {
        color: #5dade2;
      }
    }
  }

  .footer-bottom {
    text-align: center;
    padding-top: 30px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);

    p {
      margin: 0;
      font-size: 14px;
      color: #95a5a6;
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}
</style>
