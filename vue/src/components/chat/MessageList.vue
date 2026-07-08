<script setup>
import { ref, watch, nextTick, computed } from 'vue'
import { useChatStore } from '@/stores/chat'
import MessageItem from './MessageItem.vue'
import SkeletonLoading from './SkeletonLoading.vue'



const chatStore = useChatStore()
const listRef = ref(null)
const containerRef = ref(null)

/**
 * 点击推荐问题，自动发送消息
 */
const handleSuggestionClick = (question) => {
  if (chatStore.isStreaming) return
  chatStore.sendMessage(question)
}

/** 自动滚动到底部 */
const scrollToBottom = async () => {
  await nextTick()
  if (containerRef.value) {
    containerRef.value.scrollTop = containerRef.value.scrollHeight
  }
}

/** 监听消息变化 */
watch(
  () => chatStore.messages.length,
  () => scrollToBottom(),
  { flush: 'post' }
)

/** 监听流式内容变化 */
watch(
  () => {
    const msgs = chatStore.messages
    if (msgs.length === 0) return ''
    const last = msgs[msgs.length - 1]
    return last.role === 'assistant' ? last.content : ''
  },
  () => scrollToBottom(),
  { flush: 'post' }
)

/** 是否显示空状态 */
const isEmpty = computed(() => chatStore.messages.length === 0)
</script>

<template>
  <div ref="containerRef" class="message-list" :class="{ 'is-empty': isEmpty }">
    <!-- 空状态 -->
    <div v-if="isEmpty" class="empty-state">
      <div class="empty-icon">
        <svg width="56" height="56" viewBox="0 0 56 56" fill="none">
          <rect width="56" height="56" rx="14" fill="rgba(79, 70, 229, 0.06)" />
          <path
            d="M18 28C18 23.582 21.582 20 26 20C28.842 20 31.293 21.54 32.64 23.84L35.6 20.88C33.618 17.555 30.164 15.5 26 15.5C18.55 15.5 12.5 21.55 12.5 29C12.5 36.45 18.55 42.5 26 42.5C30.164 42.5 33.618 40.445 35.6 37.12L32.64 34.16C31.293 36.46 28.842 38 26 38C21.582 38 18 34.418 18 28Z"
            fill="#4F46E5"
            opacity="0.5"
          />
          <circle cx="38" cy="28" r="8" fill="#4F46E5" opacity="0.25" />
        </svg>
      </div>
      <h2 class="empty-title">开始对话</h2>
      <p class="empty-desc">
        向 AI 助手提问，探索 NebulaMind 知识库中的智慧。
      </p>
      <div class="empty-suggestions">
        <span class="suggestion-label">试试这些：</span>
        <div class="suggestion-chips">
          <el-tag
            v-for="q in ['什么是 RAG？', 'Milvus 有哪些索引类型？', 'RAG 和 Fine-tuning 的区别？']"
            :key="q"
            class="suggestion-chip"
            type="info"
            effect="plain"
            @click="handleSuggestionClick(q)"
          >
            {{ q }}
          </el-tag>
        </div>
      </div>
    </div>

    <!-- 消息列表 -->
    <div v-else ref="listRef" class="message-items">
      <MessageItem
        v-for="msg in chatStore.messages"
        :key="msg.id"
        :message="msg"
      />

      <!-- 流式生成中的骨架屏 -->
      <SkeletonLoading
        v-if="chatStore.isStreaming && chatStore.messages.length > 0"
        :status="chatStore.streamingStatus"
      />
    </div>
  </div>
</template>

<style scoped>
.message-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  scroll-behavior: smooth;
}

.message-list.is-empty {
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-items {
  max-width: 820px;
  margin: 0 auto;
  padding: var(--space-xl) 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

/* ---- Empty State ---- */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-md);
  padding: var(--space-3xl);
}

.empty-icon {
  margin-bottom: var(--space-sm);
}

.empty-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.empty-desc {
  font-size: var(--font-size-base);
  color: var(--color-text-tertiary);
  max-width: 360px;
  line-height: var(--line-height-relaxed);
}

.empty-suggestions {
  margin-top: var(--space-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
}

.suggestion-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  font-weight: var(--font-weight-medium);
}

.suggestion-chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  justify-content: center;
}

.suggestion-chip {
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: var(--font-size-sm);
}

.suggestion-chip:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}
</style>