<script setup>
import { ref } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'

defineProps({
  detail: {
    type: Object,
    default: null,
  },
})

const activeTab = ref('vector')
</script>

<template>
  <div v-if="detail" class="retriever-detail">
    <div class="retriever-tabs">
      <button
        v-for="tab in ['vector', 'bm25', 'rrf', 'rerank']"
        :key="tab"
        class="retriever-tab"
        :class="{ active: activeTab === tab }"
        @click="activeTab = tab"
      >
        {{ tab.toUpperCase() }}
      </button>
    </div>

    <!-- Vector -->
    <div v-if="activeTab === 'vector'" class="retriever-panel">
      <div class="retriever-info">
        <span class="retriever-label">Top K:</span>
        <span class="retriever-value">{{ detail.vector.topK }}</span>
      </div>
      <table class="retriever-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Chunk ID</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, i) in detail.vector.results" :key="r.id">
            <td class="rank-cell">{{ i + 1 }}</td>
            <td><code>{{ r.id }}</code></td>
            <td class="score-cell" :class="scoreClass(r.score)">{{ r.score.toFixed(4) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- BM25 -->
    <div v-if="activeTab === 'bm25'" class="retriever-panel">
      <div class="retriever-info">
        <span class="retriever-label">Top K:</span>
        <span class="retriever-value">{{ detail.bm25.topK }}</span>
      </div>
      <table class="retriever-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Chunk ID</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, i) in detail.bm25.results" :key="r.id">
            <td class="rank-cell">{{ i + 1 }}</td>
            <td><code>{{ r.id }}</code></td>
            <td class="score-cell" :class="scoreClass(r.score)">{{ r.score.toFixed(4) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- RRF -->
    <div v-if="activeTab === 'rrf'" class="retriever-panel">
      <div class="retriever-info">
        <span class="retriever-label">Merged:</span>
        <span class="retriever-value">{{ detail.rrf.mergedCount }} chunks</span>
      </div>
      <table class="retriever-table">
        <thead>
          <tr>
            <th>Chunk ID</th>
            <th>RRF Score</th>
            <th>Vec Rank</th>
            <th>BM25 Rank</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in detail.rrf.results" :key="r.id">
            <td><code>{{ r.id }}</code></td>
            <td class="score-cell" :class="scoreClass(r.score)">{{ r.score.toFixed(4) }}</td>
            <td class="rank-cell">#{{ r.rankVector }}</td>
            <td class="rank-cell">#{{ r.rankBM25 }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Rerank -->
    <div v-if="activeTab === 'rerank'" class="retriever-panel">
      <div class="retriever-info">
        <span class="retriever-label">Top K:</span>
        <span class="retriever-value">{{ detail.rerank.topK }}</span>
      </div>
      <table class="retriever-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Chunk ID</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, i) in detail.rerank.results" :key="r.id">
            <td class="rank-cell">{{ i + 1 }}</td>
            <td><code>{{ r.id }}</code></td>
            <td class="score-cell final" :class="scoreClass(r.score)">{{ r.score.toFixed(4) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export function scoreClass(score) {
  if (score >= 0.8) return 'high'
  if (score >= 0.5) return 'medium'
  return 'low'
}
</script>

<style scoped>
.retriever-detail {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.retriever-tabs {
  display: flex;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-bg);
}

.retriever-tab {
  padding: var(--space-xs) var(--space-md);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-mono);
  color: var(--color-text-tertiary);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
  letter-spacing: 0.5px;
}

.retriever-tab:hover {
  color: var(--color-text-primary);
}

.retriever-tab.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.retriever-panel {
  padding: var(--space-md);
}

.retriever-info {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
  font-size: var(--font-size-xs);
}

.retriever-label {
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: var(--font-weight-semibold);
}

.retriever-value {
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-mono);
}

.retriever-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-xs);
  font-family: var(--font-mono);
}

.retriever-table th {
  text-align: left;
  padding: var(--space-xs) var(--space-sm);
  color: var(--color-text-tertiary);
  font-weight: var(--font-weight-semibold);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--color-border);
}

.retriever-table td {
  padding: var(--space-xs) var(--space-sm);
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border-light);
}

.retriever-table code {
  color: var(--color-accent);
  background: none;
  font-size: var(--font-size-xs);
}

.rank-cell {
  color: var(--color-text-tertiary) !important;
  text-align: center;
}

.score-cell {
  font-weight: var(--font-weight-bold);
}

.score-cell.high { color: #16A34A; }
.score-cell.medium { color: #D97706; }
.score-cell.low { color: #DC2626; }
.score-cell.final { color: var(--color-accent); }
</style>