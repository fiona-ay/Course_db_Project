//Task 6
<template>
  <div class="not-found-container">
    <el-result
      icon="warning"
      title="404 - 页面走丢了"
      :sub-title="`抱歉，您访问的页面不存在。将在 ${countdown} 秒后自动返回首页...`"
    >
      <template #extra>
        <el-button type="primary" @click="goHome">立即返回首页</el-button>
        <el-button @click="goHelp">前往帮助中心</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const countdown = ref(5) // 设置 5 秒倒计时
let timer = null

// 返回首页的逻辑
const goHome = () => {
  router.push('/')
}

// 跳转帮助中心的逻辑
const goHelp = () => {
  router.push('/help')
}

onMounted(() => {
  // 开启定时器
  timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      goHome()
    }
  }, 1000)
})

// 组件销毁时清除定时器，防止内存泄漏
onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh; /* 居中显示 */
  background-color: #f5f7fa;
}

:deep(.el-result__title p) {
  font-size: 24px;
  color: #303133;
}
</style>

