<script setup>
import { useAppStore } from '@/stores/app'
import SystemStatus from './SystemStatus.vue'

const appStore = useAppStore()
</script>

<template>
  <header class="topbar">
    <!-- 左侧：项目名称 -->
    <div class="topbar-left">
      <span class="project-name">NebulaMind</span>
      <span class="project-badge">Enterprise AI Client</span>
    </div>

    <!-- 右侧：AI System Status + Developer Mode + 用户头像 -->
    <div class="topbar-right">
      <SystemStatus />

      <div class="topbar-divider" />

      <div class="developer-mode-toggle" :class="{ active: appStore.developerMode }">
        <el-switch
          v-model="appStore.developerMode"
          size="small"
          inline-prompt
          active-text="DEV"
          inactive-text="DEV"
        />
      </div>

      <div class="topbar-divider" />

      <el-avatar :size="32" icon="UserFilled" class="topbar-avatar" />
    </div>
  </header>
</template>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--topbar-height);
  padding: 0 var(--space-xl);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

/* ---- Left ---- */
.topbar-left {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.project-name {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  letter-spacing: -0.2px;
}

.project-badge {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  background: var(--color-bg-alt);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-weight: var(--font-weight-medium);
}

/* ---- Right ---- */
.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
}

.topbar-divider {
  width: 1px;
  height: 20px;
  background: var(--color-border);
}

.developer-mode-toggle {
  display: flex;
  align-items: center;
}

.developer-mode-toggle.active :deep(.el-switch__label) {
  color: var(--color-primary);
  font-weight: var(--font-weight-semibold);
}

.topbar-avatar {
  flex-shrink: 0;
  cursor: pointer;
}
</style>