<template>
  <div class="reservations-page">
    <div class="page-header animate__animated animate__fadeInDown">
      <div class="header-icon float">
        <el-icon :size="48"><Calendar /></el-icon>
      </div>
      <div>
        <h2 class="page-title gradient-text">预约管理</h2>
        <p class="page-subtitle">功能开发中，敬请期待...</p>
      </div>
    </div>

    <el-card class="main-card glass-card animate__animated animate__fadeInUp">
      <div class="coming-soon">
        <div class="coming-soon-icon pulse">
          <el-icon :size="120"><Calendar /></el-icon>
        </div>
        <h3>功能即将上线</h3>
        <p>我们正在努力开发中，很快就能和大家见面了！</p>
        <el-button type="primary" class="cute-button" round @click="$router.push('/laboratories')">
          先去管理实验室
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { Calendar } from '@element-plus/icons-vue'
</script>

<style scoped lang="scss">
.reservations-page {
  max-width: 1400px;
  margin: 0 auto;
  animation: slideInUp 0.6s ease-out;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
  padding: 24px 32px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);

  .header-icon {
    width: 80px;
    height: 80px;
    border-radius: 20px;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 0 8px 24px rgba(79, 172, 254, 0.4);
  }

  .page-title {
    margin: 0 0 8px 0;
    font-size: 28px;
    font-weight: 700;
  }

  .page-subtitle {
    margin: 0;
    color: #666;
    font-size: 14px;
  }
}

.coming-soon {
  text-align: center;
  padding: 80px 20px;

  .coming-soon-icon {
    margin: 0 auto 32px;
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(79, 172, 254, 0.2) 0%, rgba(0, 242, 254, 0.2) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #4facfe;
  }

  h3 {
    font-size: 24px;
    color: #333;
    margin: 0 0 16px 0;
  }

  p {
    font-size: 16px;
    color: #999;
    margin: 0 0 32px 0;
  }
}
</style>
