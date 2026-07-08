<script setup>
/**
 * 会话历史页
 * 展示历史对话记录列表
 * Phase 4 实现完整历史管理
 */
</script>

<template>
  <div class="conversations-view">
    <div class="page-header">
      <div>
        <h1 class="page-title">会话历史</h1>
        <p class="page-desc">查看和管理您的历史对话记录。</p>
      </div>
    </div>

    <div class="conversations-empty">
      <el-empty description="暂无历史会话" />
    </div>
  </div>
</template>

<style scoped>
.conversations-view {
  max-width: 960px;
}

.page-header {
  margin-bottom: var(--space-2xl);
}

.page-title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  letter-spacing: -0.3px;
}

.page-desc {
  font-size: var(--font-size-base);
  color: var(--color-text-tertiary);
  margin-top: var(--space-xs);
}

.conversations-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
}
</style>