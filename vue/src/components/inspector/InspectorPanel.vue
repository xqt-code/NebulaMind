<script setup>
import { ref } from 'vue'
import { ArrowDown, Monitor } from '@element-plus/icons-vue'
import { useAppStore } from '@/stores/app'
import TraceIDBar from './TraceIDBar.vue'
import PromptPreview from './PromptPreview.vue'
import ChunkList from './ChunkList.vue'
import RetrieverDetail from './RetrieverDetail.vue'
import LatencyBreakdown from './LatencyBreakdown.vue'
import RawResponse from './RawResponse.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
})

const appStore = useAppStore()

/** 各面板展开状态 */
const panelState = ref({
  traceId: true,
  prompt: false,
  timeline: false,
  chunks: true,
  retriever: false,
  latency: true,
  raw: false,
})

const togglePanel = (key) => {
  panelState.value[key] = !panelState.value[key]
}
</script>

<template>
  <div v-if="appStore.developerMode && !message.isStreaming" class="inspector-panel">
    <!-- Panel Header -->
    <div class="inspector-header">
      <el-icon :size="14"><Monitor /></el-icon>
      <span>Developer Inspector</span>
      <span class="inspector-badge">DEV</span>
    </div>

    <!-- 1. TraceID -->
    <div class="inspector-section">
      <div class="section-toggle" @click="togglePanel('traceId')">
        <el-icon :size="12" class="toggle-icon" :class="{ rotated: panelState.traceId }">
          <ArrowDown />
        </el-icon>
        <span>Trace ID</span>
      </div>
      <div v-show="panelState.traceId" class="section-body">
        <TraceIDBar :trace-id="message.traceId || 'N/A'" />
      </div>
    </div>

    <!-- 2. Prompt Preview -->
    <div class="inspector-section">
      <div class="section-toggle" @click="togglePanel('prompt')">
        <el-icon :size="12" class="toggle-icon" :class="{ rotated: panelState.prompt }">
          <ArrowDown />
        </el-icon>
        <span>Prompt Preview</span>
      </div>
      <div v-show="panelState.prompt" class="section-body">
        <PromptPreview
          :system-prompt="message.systemPrompt"
          :user-prompt="message.userPrompt"
        />
      </div>
    </div>

    <!-- 3. RAG Timeline -->
    <div class="inspector-section">
      <div class="section-toggle" @click="togglePanel('timeline')">
        <el-icon :size="12" class="toggle-icon" :class="{ rotated: panelState.timeline }">
          <ArrowDown />
        </el-icon>
        <span>RAG Timeline</span>
      </div>
      <div v-show="panelState.timeline" class="section-body">
        <RetrievalTimeline
          :timeline="message.ragTimeline"
          :visible="true"
        />
      </div>
    </div>

    <!-- 4. Chunk Hits -->
    <div class="inspector-section">
      <div class="section-toggle" @click="togglePanel('chunks')">
        <el-icon :size="12" class="toggle-icon" :class="{ rotated: panelState.chunks }">
          <ArrowDown />
        </el-icon>
        <span>Chunk Hits ({{ message.chunks?.length || 0 }})</span>
      </div>
      <div v-show="panelState.chunks" class="section-body">
        <ChunkList :chunks="message.chunks" />
      </div>
    </div>

    <!-- 5. Retriever Detail -->
    <div class="inspector-section">
      <div class="section-toggle" @click="togglePanel('retriever')">
        <el-icon :size="12" class="toggle-icon" :class="{ rotated: panelState.retriever }">
          <ArrowDown />
        </el-icon>
        <span>Retriever Detail</span>
      </div>
      <div v-show="panelState.retriever" class="section-body">
        <RetrieverDetail :detail="message.retrieverDetail" />
      </div>
    </div>

    <!-- 6. Token Usage + Latency -->
    <div class="inspector-section">
      <div class="section-toggle" @click="togglePanel('latency')">
        <el-icon :size="12" class="toggle-icon" :class="{ rotated: panelState.latency }">
          <ArrowDown />
        </el-icon>
        <span>Token Usage &amp; Latency</span>
      </div>
      <div v-show="panelState.latency" class="section-body">
        <!-- Token Usage -->
        <div class="token-grid">
          <div class="token-item">
            <span class="token-label">Prompt</span>
            <span class="token-value">{{ (message.promptTokens || 0).toLocaleString() }}</span>
          </div>
          <div class="token-item">
            <span class="token-label">Completion</span>
            <span class="token-value">{{ (message.completionTokens || 0).toLocaleString() }}</span>
          </div>
          <div class="token-item">
            <span class="token-label">Total</span>
            <span class="token-value highlight">{{ (message.totalTokens || 0).toLocaleString() }}</span>
          </div>
        </div>
        <div style="margin-top: 16px;">
          <LatencyBreakdown :breakdown="message.latencyBreakdown" />
        </div>
      </div>
    </div>

    <!-- 7. Raw Response -->
    <div class="inspector-section">
      <div class="section-toggle" @click="togglePanel('raw')">
        <el-icon :size="12" class="toggle-icon" :class="{ rotated: panelState.raw }">
          <ArrowDown />
        </el-icon>
        <span>Raw Response</span>
      </div>
      <div v-show="panelState.raw" class="section-body">
        <RawResponse :data="message.rawResponse" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.inspector-panel {
  margin-top: var(--space-xl);
  border: 1px solid var(--color-accent);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--color-surface);
}

/* ---- Header ---- */
.inspector-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-lg);
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.08), rgba(79, 70, 229, 0.06));
  border-bottom: 1px solid rgba(124, 58, 237, 0.15);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-accent);
}

.inspector-badge {
  margin-left: auto;
  font-size: 10px;
  font-family: var(--font-mono);
  font-weight: var(--font-weight-bold);
  padding: 1px 8px;
  border-radius: 10px;
  background: var(--color-accent);
  color: white;
  letter-spacing: 0.5px;
}

/* ---- Section ---- */
.inspector-section {
  border-bottom: 1px solid var(--color-border-light);
}

.inspector-section:last-child {
  border-bottom: none;
}

.section-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-lg);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  cursor: pointer;
  user-select: none;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: background var(--transition-fast);
}

.section-toggle:hover {
  background: var(--color-bg);
}

.toggle-icon {
  transition: transform var(--transition-fast);
  flex-shrink: 0;
}

.toggle-icon.rotated {
  transform: rotate(90deg);
}

.section-body {
  padding: 0 var(--space-lg) var(--space-lg);
}

/* ---- Token Grid ---- */
.token-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-sm);
}

.token-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-md);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.token-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-xs);
}

.token-value {
  font-family: var(--font-mono);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
}

.token-value.highlight {
  color: var(--color-accent);
}
</style>