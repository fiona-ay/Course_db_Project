<template>
  <div class="app-wrapper">
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="floating-circle circle-1"></div>
      <div class="floating-circle circle-2"></div>
      <div class="floating-circle circle-3"></div>
      <div class="floating-circle circle-4"></div>
    </div>

    <el-container class="app-container">
      <!-- 可爱的顶部导航栏 -->
      <el-header class="app-header animate__animated animate__slideInDown">
        <div class="header-content">
          <div class="logo-section" @click="$router.push('/')">
            <div class="logo-icon float">
              <el-icon :size="32"><Document /></el-icon>
            </div>
            <h1 class="title gradient-text">
              高校大型仪器设备共享服务平台
            </h1>
          </div>
          
          <div class="header-right">
            <el-menu
              :default-active="activeMenu"
              mode="horizontal"
              router
              class="header-menu cute-menu"
            >
              <el-menu-item index="/" class="menu-item">
                <el-icon><HomeFilled /></el-icon>
                <span>首页</span>
              </el-menu-item>
              <el-menu-item index="/equipment" class="menu-item">
                <el-icon><Box /></el-icon>
                <span>仪器目录</span>
              </el-menu-item>
              <el-menu-item index="/help" class="menu-item">
                <el-icon><QuestionFilled /></el-icon>
                <span>帮助中心</span>
              </el-menu-item>
            </el-menu>
            <div class="header-actions">
              <template v-if="userStore.isLoggedIn">
                <el-dropdown @command="handleCommand">
                  <span class="user-info">
                    <el-icon><User /></el-icon>
                    {{ userStore.userInfo?.name || '用户' }}
                    <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                  </span>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item disabled>
                        <span style="color: #999; font-size: 12px">
                          {{ userStore.userInfo?.user_type === 'student' ? '学生' : 
                             userStore.userInfo?.user_type === 'teacher' ? '教师' : '管理员' }}
                        </span>
                      </el-dropdown-item>
                      <el-dropdown-item command="logout" divided>
                        <el-icon><SwitchButton /></el-icon>
                        退出登录
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </template>
              <template v-else>
                <el-button type="primary" plain @click="handleLogin">
                  登录
                </el-button>
                <el-button type="primary" @click="handleRegister">
                  注册
                </el-button>
              </template>
            </div>
          </div>
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main class="app-main">
        <transition name="page" mode="out-in">
          <router-view />
        </transition>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Document, HomeFilled, Box, QuestionFilled, User, ArrowDown, SwitchButton } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const activeMenu = computed(() => route.path)

const handleLogin = () => {
  router.push('/')
}

const handleRegister = () => {
  ElMessage.info('注册功能开发中...')
}

const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/')
    }).catch(() => {})
  }
}
</script>

<style scoped lang="scss">
.app-wrapper {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.background-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.floating-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  animation: float 6s ease-in-out infinite;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 200px;
  height: 200px;
  top: 20%;
  right: -50px;
  animation-delay: 2s;
}

.circle-3 {
  width: 250px;
  height: 250px;
  bottom: 10%;
  left: 10%;
  animation-delay: 4s;
}

.circle-4 {
  width: 180px;
  height: 180px;
  bottom: -50px;
  right: 10%;
  animation-delay: 1s;
}

.app-container {
  position: relative;
  z-index: 1;
  min-height: 100vh;
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
  padding: 0;
  border-bottom: 2px solid rgba(102, 126, 234, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 30px;
  max-width: 1400px;
  margin: 0 auto;
  gap: 20px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;

  @media (max-width: 768px) {
    gap: 10px;
  }
}

.header-actions {
  display: flex;
  gap: 12px;
  margin-left: 10px;

  @media (max-width: 768px) {
    margin-left: 0;
    
    .el-button {
      padding: 8px 12px;
      font-size: 12px;
    }
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-wrap: wrap;
    padding: 0 15px;
  }

  .title {
    font-size: 18px !important;
  }

  .logo-icon {
    width: 36px !important;
    height: 36px !important;
  }

  .header-menu {
    :deep(.el-menu-item) {
      margin: 0 4px;
      font-size: 14px;
      padding: 0 12px !important;
    }
  }
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.05);
  }
}

.logo-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-menu {
  background: transparent !important;
  border-bottom: none !important;

  :deep(.el-menu-item) {
    margin: 0 8px;
    border-radius: 12px;
    color: #666;
    border-bottom: none !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;

    &::before {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      width: 0;
      height: 3px;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
      border-radius: 2px;
      transform: translateX(-50%);
      transition: width 0.3s ease;
    }

    &:hover {
      background: rgba(102, 126, 234, 0.1) !important;
      color: #667eea;
      transform: translateY(-2px);
    }

    &.is-active {
      background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%) !important;
      color: #667eea;
      font-weight: 600;

      &::before {
        width: 80%;
      }
    }

    .el-icon {
      margin-right: 6px;
      font-size: 18px;
    }
  }
}

.app-main {
  background: transparent;
  padding: 30px;
  overflow-y: auto;
  min-height: calc(100vh - 60px);
}

/* 页面过渡动画 */
.page-enter-active,
.page-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.95);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-30px) scale(0.95);
}
</style>
