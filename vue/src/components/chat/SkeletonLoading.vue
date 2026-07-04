<script setup>
import { Cpu } from '@element-plus/icons-vue'

defineProps({
  status: {
    type: String,
    default: 'thinking',
  },
})

const statusMap = {
  thinking: 'Thinking...',
  searching: 'Searching documents...',
  ranking: 'Ranking results...',
  generating: 'Generating answer...',
}
</script>

<template>
  <div class="skeleton-message">
    <div class="message-avatar">
      <el-avatar :size="34" :icon="Cpu" class="ai-avatar" />
    </div>
    <div class="skeleton-body">
      <div class="skeleton-header">
        <span class="skeleton-sender">NebulaMind AI</span>
        <span class="skeleton-status">{{ statusMap[status] || status }}</span>
      </div>

      <!-- 骨架屏线条 -->
      <div class="skeleton-lines">
        <div class="skeleton-line" style="width: 100%" />
        <div class="skeleton-line" style="width: 92%" />
        <div class="skeleton-line" style="width: 85%" />
        <div class="skeleton-line" style="width: 70%" />
        <div class="skeleton-line" style="width: 45%" />
      </div>

      <!-- 骨架卡片 -->
      <div class="skeleton-card">
        <div class="skeleton-line short" style="width: 40%" />
        <div class="skeleton-line short" style="width: 60%" />
        <div class="skeleton-line short" style="width: 35%" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.skeleton-message {
  display: flex;
  gap: var(--space-lg);
  padding: 0 var(--space-xl);
}

.skeleton-body {
  flex: 1;
  min-width: 0;
}

.ai-avatar {
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  color: white;
}

.skeleton-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-lg);
}

.skeleton-sender {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.skeleton-status {
  font-size: var(--font-size-xs);
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
}

/* ---- Skeleton Lines ---- */
.skeleton-lines {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  margin-bottom: var(--space-xl);
}

.skeleton-line {
  height: 12px;
  border-radius: 6px;
  background: linear-gradient(
    90deg,
    var(--color-bg-alt) 25%,
    rgba(79, 70, 229, 0.06) 50%,
    var(--color-bg-alt) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.8s ease-in-out infinite;
}

.skeleton-line.short {
  height: 10px;
}

/* ---- Skeleton Card ---- */
.skeleton-card {
  padding: var(--space-lg);
  background: var(--color-bg-alt);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>