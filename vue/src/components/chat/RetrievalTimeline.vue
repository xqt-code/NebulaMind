<script setup>
import { Loading, Check, Promotion } from '@element-plus/icons-vue'

defineProps({
  timeline: {
    type: Array,
    required: true,
  },
  visible: {
    type: Boolean,
    default: false,
  },
})

/** 格式化耗时 */
const formatDuration = (ms) => {
  if (ms === 0 || ms == null) return ''
  if (ms >= 1000) return `${(ms / 1000).toFixed(1)}s`
  return `${ms}ms`
}
</script>

<template>
  <div v-if="visible" class="retrieval-timeline">
    <div
      v-for="(item, index) in timeline"
      :key="item.step"
      class="timeline-item"
      :class="{ 'is-first': index === 0, 'is-last': index === timeline.length - 1 }"
    >
      <!-- 时间线连接线 -->
      <div class="timeline-line">
        <div class="timeline-dot" :class="{ active: index < timeline.length - 1 }">
          <el-icon v-if="index < timeline.length - 1" :size="10"><Check /></el-icon>
          <el-icon v-else :size="10"><Promotion /></el-icon>
        </div>
        <div v-if="index < timeline.length - 1" class="timeline-connector" />
      </div>

      <!-- 时间线内容 -->
      <div class="timeline-content">
        <div class="timeline-header">
          <span class="timeline-step">{{ index + 1 }}. {{ item.label }}</span>
          <span v-if="item.duration" class="timeline-duration">
            {{ formatDuration(item.duration) }}
          </span>
        </div>
        <p v-if="item.detail" class="timeline-detail">{{ item.detail }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.retrieval-timeline {
  padding: var(--space-md) 0 var(--space-md) var(--space-sm);
  margin-top: var(--space-sm);
}

.timeline-item {
  display: flex;
  gap: var(--space-md);
  padding-bottom: var(--space-md);
}

.timeline-item.is-last {
  padding-bottom: 0;
}

/* ---- Timeline Line ---- */
.timeline-line {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.timeline-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--color-bg-alt);
  border: 2px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
  transition: all var(--transition-fast);
}

.timeline-dot.active {
  background: var(--color-primary-bg);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.timeline-item.is-first .timeline-dot {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.timeline-item.is-last .timeline-dot {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: white;
}

.timeline-connector {
  width: 2px;
  flex: 1;
  min-height: 24px;
  background: var(--color-border);
  margin: 4px 0;
}

/* ---- Timeline Content ---- */
.timeline-content {
  flex: 1;
  min-width: 0;
  padding-top: 1px;
}

.timeline-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.timeline-step {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
}

.timeline-duration {
  font-size: var(--font-size-xs);
  font-family: var(--font-mono);
  font-weight: var(--font-weight-semibold);
  color: var(--color-primary);
  background: var(--color-primary-bg);
  padding: 1px 6px;
  border-radius: 4px;
}

.timeline-detail {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin: 2px 0 0;
  font-family: var(--font-mono);
}
</style>