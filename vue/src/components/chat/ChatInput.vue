<script setup>
import { ref, computed } from 'vue'
import { Promotion, Close } from '@element-plus/icons-vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()
const inputText = ref('')
const textareaRef = ref(null)

/** 发送按钮是否禁用 */
const canSend = computed(() => inputText.value.trim().length > 0 && !chatStore.isStreaming)

/** 发送消息 */
const handleSend = () => {
  if (!canSend.value) return
  chatStore.sendMessage(inputText.value)
  inputText.value = ''
}

/** 停止生成 */
const handleStop = () => {
  chatStore.stopGeneration()
}

/** 键盘事件：Enter 发送，Shift+Enter 换行 */
const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}
</script>

<template>
  <div class="chat-input">
    <div class="input-wrapper">
      <el-input
        ref="textareaRef"
        v-model="inputText"
        type="textarea"
        :rows="1"
        :autosize="{ minRows: 1, maxRows: 6 }"
        placeholder="输入您的问题... (Shift+Enter 换行，Enter 发送)"
        :disabled="chatStore.isStreaming"
        resize="none"
        class="input-field"
        @keydown="handleKeydown"
      />
      <div class="input-actions">
        <div class="input-hint">
          <span v-if="chatStore.isStreaming" class="hint-streaming">
            <span class="pulse-dot" />
            {{ chatStore.streamingStatus }}
          </span>
          <span v-else class="hint-normal">
            <kbd>Enter</kbd> 发送 · <kbd>Shift+Enter</kbd> 换行
          </span>
        </div>
        <div class="input-buttons">
          <el-button
            v-if="chatStore.isStreaming"
            type="danger"
            :icon="Close"
            @click="handleStop"
          >
            停止生成
          </el-button>
          <el-button
            v-else
            type="primary"
            :icon="Promotion"
            :disabled="!canSend"
            @click="handleSend"
          >
            发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  flex-shrink: 0;
  padding: var(--space-lg) var(--space-xl);
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
}

.input-wrapper {
  max-width: 820px;
  margin: 0 auto;
}

.input-field {
  --el-input-bg-color: var(--color-bg-alt);
  --el-input-border-color: var(--color-border);
  --el-input-hover-border-color: var(--color-primary-light);
  --el-input-focus-border-color: var(--color-primary);
  --el-input-border-radius: var(--radius-lg);
}

.input-field :deep(.el-textarea__inner) {
  background: var(--color-bg-alt);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
  padding: var(--space-md) var(--space-lg);
  transition: border-color var(--transition-fast);
  font-family: var(--font-family);
}

.input-field :deep(.el-textarea__inner):focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
}

.input-field :deep(.el-textarea__inner):disabled {
  background: var(--color-bg);
  cursor: not-allowed;
}

.input-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: var(--space-sm);
}

.input-hint {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.hint-normal kbd {
  display: inline-block;
  padding: 1px 5px;
  font-size: 10px;
  font-family: var(--font-mono);
  background: var(--color-bg-alt);
  border: 1px solid var(--color-border);
  border-radius: 3px;
  line-height: 1.4;
}

.hint-streaming {
  display: flex;
  align-items: center;
  gap: 6px;
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

.input-buttons {
  display: flex;
  gap: var(--space-sm);
}
</style>