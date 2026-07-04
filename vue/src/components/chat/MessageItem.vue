<script setup>
import { computed, ref } from 'vue'
import { UserFilled, Cpu, ArrowDown } from '@element-plus/icons-vue'
import { renderStreamingMarkdown } from '@/utils/markdown'
import ReferenceCard from './ReferenceCard.vue'
import SearchExplain from './SearchExplain.vue'
import RetrievalTimeline from './RetrievalTimeline.vue'
import InspectorPanel from '@/components/inspector/InspectorPanel.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
})

/** 格式化时间 */
const formattedTime = computed(() => {
  const d = new Date(props.message.timestamp)
  return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
})

/** 渲染 Markdown 内容 */
const renderedContent = computed(() => {
  if (props.message.role !== 'assistant') return ''
  if (props.message.isStreaming) {
    return renderStreamingMarkdown(props.message.content)
  }
  return renderStreamingMarkdown(props.message.content)
})

/** 展开状态 */
const showReferences = ref(false)
const showSearchExplain = ref(false)
const showRetrieval = ref(false)
const activeReference = ref(null)

/** 切换引用解释面板 */
const toggleSearchExplain = (refId) => {
  if (activeReference.value === refId) {
    activeReference.value = null
  } else {
    activeReference.value = refId
  }
}

/** 格式化 Token 数 */
const formatNumber = (n) => (n ?? 0).toLocaleString()

/** 格式化延迟 */
const formatLatency = (ms) => {
  if (ms >= 1000) return `${(ms / 1000).toFixed(1)}s`
  return `${ms}ms`
}
</script>

<template>
  <!-- 用户消息 -->
  <div v-if="message.role === 'user'" class="message user-message">
    <div class="message-avatar user-avatar">
      <el-avatar :size="34" icon="UserFilled" />
    </div>
    <div class="message-body">
      <div class="message-header">
        <span class="message-sender">You</span>
        <span class="message-time">{{ formattedTime }}</span>
      </div>
      <div class="message-content user-content">
        {{ message.content }}
      </div>
    </div>
  </div>

  <!-- AI 消息 -->
  <div v-else class="message ai-message">
    <div class="message-avatar ai-avatar">
      <el-avatar :size="34" :icon="Cpu" />
    </div>
    <div class="message-body">
      <div class="message-header">
        <span class="message-sender">NebulaMind AI</span>
        <span class="message-time">{{ formattedTime }}</span>
        <span v-if="message.isStreaming" class="streaming-badge">
          <span class="pulse-dot" />
          {{ message.isStreaming ? '生成中...' : '' }}
        </span>
      </div>

      <!-- Markdown 内容 -->
      <div
        class="message-content markdown-body"
        v-html="renderedContent"
      />

      <!-- 已完成的消息：展示元数据 -->
      <div v-if="!message.isStreaming && message.content" class="message-meta">
        <!-- 引用来源卡片 -->
        <div v-if="message.references?.length" class="meta-section">
          <div class="meta-section-header" @click="showReferences = !showReferences">
            <el-icon :size="14"><ArrowDown /></el-icon>
            <span>引用来源 ({{ message.references.length }})</span>
            <el-icon
              :size="14"
              class="collapse-icon"
              :class="{ rotated: showReferences }"
            >
              <ArrowDown />
            </el-icon>
          </div>
          <div v-show="showReferences" class="references-grid">
            <ReferenceCard
              v-for="ref in message.references"
              :key="ref.id"
              :reference="ref"
              :show-explain="activeReference === ref.id"
              @toggle-explain="toggleSearchExplain(ref.id)"
            />
            <SearchExplain
              v-for="ref in message.references"
              :key="`explain-${ref.id}`"
              :reference="ref"
              :visible="activeReference === ref.id"
            />
          </div>
        </div>

        <!-- 模型信息 + Token 统计 + Confidence -->
        <div class="meta-stats">
          <div v-if="message.model" class="stat-group">
            <span class="stat-label">模型</span>
            <span class="stat-value">{{ message.model }}</span>
            <span class="stat-separator" />
            <span class="stat-label">Temp</span>
            <span class="stat-value">{{ message.temperature }}</span>
            <span class="stat-separator" />
            <span class="stat-label">Top_p</span>
            <span class="stat-value">{{ message.topP }}</span>
          </div>

          <div class="stat-divider" />

          <div class="stat-group">
            <span class="stat-label">Prompt</span>
            <span class="stat-value">{{ formatNumber(message.promptTokens) }}</span>
            <span class="stat-separator" />
            <span class="stat-label">Completion</span>
            <span class="stat-value">{{ formatNumber(message.completionTokens) }}</span>
            <span class="stat-separator" />
            <span class="stat-label">Total</span>
            <span class="stat-value">{{ formatNumber(message.totalTokens) }}</span>
            <span class="stat-label">tokens</span>
          </div>

          <div class="stat-divider" />

          <div class="stat-group">
            <span class="stat-label">Latency</span>
            <span class="stat-value">{{ formatLatency(message.latencyMs) }}</span>
          </div>

          <div class="stat-divider" />

          <div class="stat-group">
            <span class="stat-label">Confidence</span>
            <span
              class="confidence-badge"
              :class="{
                high: message.confidence >= 80,
                medium: message.confidence >= 60 && message.confidence < 80,
                low: message.confidence < 60,
              }"
            >
              {{ message.confidence }}%
            </span>
          </div>
        </div>

        <!-- 查看检索过程 -->
        <div class="meta-section">
          <div class="meta-section-header" @click="showRetrieval = !showRetrieval">
            <el-icon :size="14"><ArrowDown /></el-icon>
            <span>查看检索过程</span>
            <el-icon
              :size="14"
              class="collapse-icon"
              :class="{ rotated: showRetrieval }"
            >
              <ArrowDown />
            </el-icon>
          </div>
          <RetrievalTimeline
            v-if="message.ragTimeline?.length"
            :timeline="message.ragTimeline"
            :visible="showRetrieval"
          />
        </div>

        <!-- Developer Inspector Panel -->
        <InspectorPanel :message="message" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ---- Message Layout ---- */
.message {
  display: flex;
  gap: var(--space-lg);
  padding: 0 var(--space-xl);
}

.message-body {
  flex: 1;
  min-width: 0;
}

.message-avatar {
  flex-shrink: 0;
  padding-top: 2px;
}

.user-avatar :deep(.el-avatar) {
  background: var(--color-primary);
  color: white;
}

.ai-avatar :deep(.el-avatar) {
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  color: white;
}

/* ---- Message Header ---- */
.message-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-sm);
}

.message-sender {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.message-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.streaming-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
}

.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

/* ---- Message Content ---- */
.message-content {
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
  color: var(--color-text-primary);
}

.user-content {
  background: var(--color-primary-bg);
  padding: var(--space-md) var(--space-lg);
  border-radius: var(--radius-lg);
  display: inline-block;
  max-width: 100%;
  word-break: break-word;
}

/* ---- Markdown Body ---- */
.markdown-body {
  padding: 0;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4) {
  margin: var(--space-xl) 0 var(--space-md);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  line-height: var(--line-height-tight);
}

.markdown-body :deep(h1) { font-size: var(--font-size-2xl); }
.markdown-body :deep(h2) { font-size: var(--font-size-xl); }
.markdown-body :deep(h3) { font-size: var(--font-size-lg); }

.markdown-body :deep(p) {
  margin: var(--space-sm) 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: var(--space-xl);
  margin: var(--space-sm) 0;
}

.markdown-body :deep(li) {
  margin: 4px 0;
}

.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--color-primary);
  padding: var(--space-sm) var(--space-lg);
  margin: var(--space-md) 0;
  background: rgba(79, 70, 229, 0.04);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  color: var(--color-text-secondary);
}

.markdown-body :deep(code) {
  font-family: var(--font-mono);
  font-size: 0.875em;
  background: var(--color-bg-alt);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--color-primary-dark);
}

.markdown-body :deep(pre) {
  margin: var(--space-md) 0;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.markdown-body :deep(pre code) {
  display: block;
  padding: var(--space-lg);
  overflow-x: auto;
  font-size: var(--font-size-sm);
  line-height: 1.6;
  background: #f8f9fb;
  color: var(--color-text-primary);
  border-radius: 0;
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: var(--space-md) 0;
  font-size: var(--font-size-sm);
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid var(--color-border);
  padding: var(--space-sm) var(--space-md);
  text-align: left;
}

.markdown-body :deep(th) {
  background: var(--color-bg-alt);
  font-weight: var(--font-weight-semibold);
}

.markdown-body :deep(.math-block) {
  margin: var(--space-md) 0;
  padding: var(--space-md);
  overflow-x: auto;
  font-size: var(--font-size-lg);
  text-align: center;
  background: var(--color-bg-alt);
  border-radius: var(--radius-md);
}

.markdown-body :deep(.katex) {
  font-size: 1.1em;
}

.markdown-body :deep(input[type="checkbox"]) {
  margin-right: 6px;
  accent-color: var(--color-primary);
}

.markdown-body :deep(hr) {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: var(--space-xl) 0;
}

/* ---- Meta Sections ---- */
.message-meta {
  margin-top: var(--space-xl);
  border-top: 1px solid var(--color-border-light);
  padding-top: var(--space-lg);
}

.meta-section {
  margin-bottom: var(--space-md);
}

.meta-section-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: var(--space-sm) 0;
  user-select: none;
  transition: color var(--transition-fast);
}

.meta-section-header:hover {
  color: var(--color-text-primary);
}

.collapse-icon {
  transition: transform var(--transition-fast);
  margin-left: auto;
}

.collapse-icon.rotated {
  transform: rotate(180deg);
}

.references-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  margin-top: var(--space-sm);
}

/* ---- Stats ---- */
.meta-stats {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-sm) var(--space-md);
  padding: var(--space-md) var(--space-lg);
  background: var(--color-bg-alt);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-md);
  font-size: var(--font-size-xs);
}

.stat-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-label {
  color: var(--color-text-tertiary);
  font-weight: var(--font-weight-medium);
}

.stat-value {
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
}

.stat-separator {
  width: 1px;
  height: 10px;
  background: var(--color-border);
  margin: 0 4px;
}

.stat-divider {
  width: 1px;
  height: 16px;
  background: var(--color-border);
}

/* ---- Confidence Badge ---- */
.confidence-badge {
  font-weight: var(--font-weight-bold);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: var(--font-size-xs);
}

.confidence-badge.high {
  background: var(--color-success-bg);
  color: #16A34A;
}

.confidence-badge.medium {
  background: rgba(245, 158, 11, 0.1);
  color: #D97706;
}

.confidence-badge.low {
  background: rgba(239, 68, 68, 0.1);
  color: #DC2626;
}
</style>