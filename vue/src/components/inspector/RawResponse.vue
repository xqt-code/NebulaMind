<script setup>
import { CopyDocument } from '@element-plus/icons-vue'

defineProps({
  data: {
    type: Object,
    default: null,
  },
})

const handleCopy = async (data) => {
  try {
    await navigator.clipboard.writeText(JSON.stringify(data, null, 2))
    ElMessage.success('原始响应已复制')
  } catch {
    ElMessage.info('复制失败')
  }
}
</script>

<template>
  <div v-if="data" class="raw-response">
    <div class="raw-header">
      <span class="raw-label">Raw Response JSON</span>
      <el-button
        :icon="CopyDocument"
        link
        type="primary"
        size="small"
        @click="handleCopy(data)"
      />
    </div>
    <pre class="raw-json">{{ JSON.stringify(data, null, 2) }}</pre>
  </div>
</template>

<style scoped>
.raw-response {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.raw-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-xs) var(--space-md);
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
}

.raw-label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.raw-json {
  padding: var(--space-md);
  margin: 0;
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  line-height: 1.6;
  color: var(--color-text-secondary);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 400px;
  overflow-y: auto;
  background: var(--color-surface);
}
</style>