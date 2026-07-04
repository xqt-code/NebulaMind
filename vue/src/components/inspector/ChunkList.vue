<script setup>
defineProps({
  chunks: {
    type: Array,
    default: () => [],
  },
})

const formatScore = (score) => (score * 100).toFixed(0) + '%'
</script>

<template>
  <div class="chunk-list">
    <div
      v-for="(chunk, index) in chunks"
      :key="chunk.id"
      class="chunk-item"
    >
      <div class="chunk-header">
        <span class="chunk-index">#{{ index + 1 }}</span>
        <code class="chunk-id">{{ chunk.id }}</code>
        <span class="chunk-score" :class="scoreClass(chunk.score)">
          {{ formatScore(chunk.score) }}
        </span>
      </div>
      <div class="chunk-doc-name">{{ chunk.docName }}</div>
      <p class="chunk-content">{{ chunk.content }}</p>
    </div>
  </div>
</template>

<script>
export function scoreClass(score) {
  if (score >= 0.9) return 'high'
  if (score >= 0.7) return 'medium'
  return 'low'
}
</script>

<style scoped>
.chunk-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.chunk-item {
  background: var(--color-bg);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-sm);
  padding: var(--space-md);
}

.chunk-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-xs);
}

.chunk-index {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-tertiary);
  font-family: var(--font-mono);
}

.chunk-id {
  font-size: var(--font-size-xs);
  font-family: var(--font-mono);
  color: var(--color-text-secondary);
  background: var(--color-bg-alt);
  padding: 1px 6px;
  border-radius: 3px;
}

.chunk-score {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  font-family: var(--font-mono);
  margin-left: auto;
  padding: 1px 6px;
  border-radius: 3px;
}

.chunk-score.high {
  color: #16A34A;
  background: var(--color-success-bg);
}

.chunk-score.medium {
  color: #D97706;
  background: rgba(245, 158, 11, 0.1);
}

.chunk-score.low {
  color: #DC2626;
  background: rgba(239, 68, 68, 0.1);
}

.chunk-doc-name {
  font-size: var(--font-size-xs);
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
  margin-bottom: var(--space-xs);
}

.chunk-content {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  line-height: var(--line-height-relaxed);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>