<script setup>
import { CopyDocument } from '@element-plus/icons-vue'

const props = defineProps({
  traceId: {
    type: String,
    required: true,
  },
})

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(props.traceId)
    ElMessage.success('TraceID 已复制')
  } catch {
    ElMessage.info(props.traceId)
  }
}
</script>

<template>
  <div class="traceid-bar">
    <span class="traceid-label">Trace ID</span>
    <code class="traceid-value">{{ traceId }}</code>
    <el-button
      :icon="CopyDocument"
      link
      type="primary"
      size="small"
      class="traceid-copy"
      @click="handleCopy"
    />
  </div>
</template>

<style scoped>
.traceid-bar {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
}

.traceid-label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

.traceid-value {
  font-size: var(--font-size-xs);
  color: var(--color-accent);
  font-weight: var(--font-weight-medium);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.traceid-copy {
  flex-shrink: 0;
  margin-left: auto;
}
</style>