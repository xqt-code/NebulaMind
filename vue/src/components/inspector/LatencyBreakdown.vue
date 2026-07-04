<script setup>
defineProps({
  breakdown: {
    type: Object,
    default: null,
  },
})

const formatMs = (ms) => {
  if (ms >= 1000) return `${(ms / 1000).toFixed(1)}s`
  return `${ms}ms`
}
</script>

<template>
  <div v-if="breakdown" class="latency-breakdown">
    <div class="latency-grid">
      <div class="latency-item">
        <span class="latency-label">Embedding</span>
        <span class="latency-value">{{ formatMs(breakdown.embedding) }}</span>
      </div>
      <div class="latency-item">
        <span class="latency-label">Vector Search</span>
        <span class="latency-value">{{ formatMs(breakdown.vectorSearch) }}</span>
      </div>
      <div class="latency-item">
        <span class="latency-label">BM25 Search</span>
        <span class="latency-value">{{ formatMs(breakdown.bm25Search) }}</span>
      </div>
      <div class="latency-item">
        <span class="latency-label">RRF Merge</span>
        <span class="latency-value">{{ formatMs(breakdown.rrfMerge) }}</span>
      </div>
      <div class="latency-item">
        <span class="latency-label">Rerank</span>
        <span class="latency-value">{{ formatMs(breakdown.rerank) }}</span>
      </div>
      <div class="latency-item">
        <span class="latency-label">Prompt Assemble</span>
        <span class="latency-value">{{ formatMs(breakdown.promptAssemble) }}</span>
      </div>
      <div class="latency-item">
        <span class="latency-label">LLM Generation</span>
        <span class="latency-value highlight">{{ formatMs(breakdown.llmGeneration) }}</span>
      </div>
    </div>

    <div class="latency-total">
      <div class="latency-bar">
        <div
          class="latency-segment"
          v-for="seg in [
            { key: 'embedding', color: '#6366F1', ms: breakdown.embedding },
            { key: 'vectorSearch', color: '#818CF8', ms: breakdown.vectorSearch },
            { key: 'bm25Search', color: '#A5B4FC', ms: breakdown.bm25Search },
            { key: 'rrfMerge', color: '#C7D2FE', ms: breakdown.rrfMerge },
            { key: 'rerank', color: '#8B5CF6', ms: breakdown.rerank },
            { key: 'promptAssemble', color: '#A78BFA', ms: breakdown.promptAssemble },
            { key: 'llmGeneration', color: '#7C3AED', ms: breakdown.llmGeneration },
          ]"
          :key="seg.key"
          :style="{ width: (seg.ms / breakdown.total * 100) + '%', background: seg.color }"
          :title="`${seg.key}: ${formatMs(seg.ms)}`"
        />
      </div>
      <div class="latency-total-text">
        <span>Total</span>
        <strong>{{ formatMs(breakdown.total) }}</strong>
      </div>
    </div>
  </div>
</template>

<style scoped>
.latency-breakdown {
  padding: var(--space-md);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.latency-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}

.latency-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--font-size-xs);
}

.latency-label {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-xs);
}

.latency-value {
  font-family: var(--font-mono);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  font-size: var(--font-size-xs);
}

.latency-value.highlight {
  color: var(--color-accent);
}

.latency-total {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.latency-bar {
  display: flex;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  background: var(--color-bg-alt);
}

.latency-segment {
  min-width: 2px;
  transition: width 0.3s ease;
}

.latency-segment:first-child {
  border-radius: 4px 0 0 4px;
}

.latency-segment:last-child {
  border-radius: 0 4px 4px 0;
}

.latency-total-text {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.latency-total-text strong {
  color: var(--color-text-primary);
  font-family: var(--font-mono);
}
</style>