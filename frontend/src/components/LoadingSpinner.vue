<template>
  <div class="loading-spinner">
    <div class="spinner"></div>
    <p class="loading-text">{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: '加载中...'
  }
})
</script>

<style scoped lang="scss">
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;

  .spinner {
    width: 50px;
    height: 50px;
    border: 4px solid rgba(102, 126, 234, 0.2);
    border-top-color: #667eea;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  .loading-text {
    margin-top: 16px;
    color: #666;
    font-size: 14px;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

