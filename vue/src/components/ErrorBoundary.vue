<script setup>
import { onErrorCaptured, ref } from 'vue'
import { WarningFilled, RefreshRight } from '@element-plus/icons-vue'
import { handleError, ErrorType } from '@/utils/errorHandler'

const hasError = ref(false)
const errorMessage = ref('')

onErrorCaptured((err, instance, info) => {
  hasError.value = true
  errorMessage.value = err?.message || '组件渲染异常'
  handleError(err, ErrorType.RUNTIME, {
    component: instance?.$options?.name || instance?.__name || 'Unknown',
    info,
  })
  return false // 阻止错误继续传播
})

const handleRetry = () => {
  hasError.value = false
  errorMessage.value = ''
}
</script>

<template>
  <div v-if="hasError" class="error-boundary">
    <div class="error-content">
      <el-icon :size="40" color="var(--el-color-danger)"><WarningFilled /></el-icon>
      <h2 class="error-title">页面渲染异常</h2>
      <p class="error-desc">{{ errorMessage }}</p>
      <el-button type="primary" :icon="RefreshRight" @click="handleRetry">
        重试
      </el-button>
    </div>
  </div>
  <slot v-else />
</template>

<style scoped>
.error-boundary {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: var(--space-3xl);
}

.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-md);
  max-width: 400px;
}

.error-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.error-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  line-height: var(--line-height-relaxed);
  word-break: break-word;
}
</style>