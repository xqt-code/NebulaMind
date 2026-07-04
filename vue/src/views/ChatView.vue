<script setup>
import { ChatDotRound } from '@element-plus/icons-vue'
import { useChatStore } from '@/stores/chat'
import MessageList from '@/components/chat/MessageList.vue'
import ChatInput from '@/components/chat/ChatInput.vue'

const chatStore = useChatStore()
</script>

<template>
  <div class="chat-view">
    <!-- 顶部：知识库信息 -->
    <header class="chat-header">
      <div class="chat-header-left">
        <el-icon class="chat-header-icon" :size="18">
          <ChatDotRound />
        </el-icon>
        <div>
          <h1 class="chat-header-title">NebulaMind 知识库</h1>
          <p class="chat-header-desc">基于 RAG 架构的企业级智能问答</p>
        </div>
      </div>
      <div class="chat-header-right">
        <el-tag size="small" type="info" effect="plain">
          {{ chatStore.messages.length }} 条消息
        </el-tag>
      </div>
    </header>

    <!-- 中间：消息列表 -->
    <MessageList />

    <!-- 底部：输入框 -->
    <ChatInput />
  </div>
</template>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* ---- Header ---- */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg) var(--space-xl);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.chat-header-left {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.chat-header-icon {
  color: var(--color-primary);
}

.chat-header-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  line-height: 1.3;
}

.chat-header-desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin-top: 2px;
}

.chat-header-right {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}
</style>