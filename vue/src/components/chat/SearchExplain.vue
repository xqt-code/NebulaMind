<script setup>
import { TrendCharts } from '@element-plus/icons-vue'

defineProps({
  reference: {
    type: Object,
    required: true,
  },
  visible: {
    type: Boolean,
    default: false,
  },
})

/** 格式化分数 */
const formatScore = (score) => (score * 100).toFixed(0) + '%'
</script>

<template>
  <div v-if="visible" class="search-explain">
    <div class="explain-header">
      <el-icon :size="14"><TrendCharts /></el-icon>
      <span>引用解释 — 为什么检索到该片段？</span>
    </div>
    <div class="explain-scores">
      <div class="score-item">
        <div class="score-label">Semantic Score</div>
        <div class="score-bar-wrap">
          <div class="score-bar" :style="{ width: (reference.scores.semantic * 100) + '%' }" />
        </div>
        <span class="score-value">{{ reference.scores.semantic.toFixed(2) }}</span>
      </div>
      <div class="score-item">
        <div class="score-label">Keyword Score</div>
        <div class="score-bar-wrap">
          <div class="score-bar kw" :style="{ width: (reference.scores.keyword * 100) + '%' }" />
        </div>
        <span class="score-value">{{ reference.scores.keyword.toFixed(2) }}</span>
      </div>
      <div class="score-item">
        <div class="score-label">Final Score</div>
        <div class="score-bar-wrap">
          <div class="score-bar final" :style="{ width: (reference.scores.final * 100) + '%' }" />
        </div>
        <span class="score-value final-text">{{ reference.scores.final.toFixed(2) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-explain {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-md) var(--space-lg);
  margin-top: 4px;
}

.explain-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
}

.explain-scores {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.score-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.score-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  width: 100px;
  flex-shrink: 0;
}

.score-bar-wrap {
  flex: 1;
  height: 6px;
  background: var(--color-bg-alt);
  border-radius: 3px;
  overflow: hidden;
}

.score-bar {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
  transition: width 0.6s ease;
}

.score-bar.kw {
  background: linear-gradient(90deg, #6366F1, #818CF8);
}

.score-bar.final {
  background: linear-gradient(90deg, var(--color-accent), #A78BFA);
}

.score-value {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-mono);
  color: var(--color-text-primary);
  width: 36px;
  text-align: right;
}

.score-value.final-text {
  color: var(--color-accent);
}
</style>