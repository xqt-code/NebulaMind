<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ChatDotRound, Document, ChatLineSquare } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

/** 导航菜单项 */
const menuItems = [
  { path: '/chat', label: '智能问答', icon: ChatDotRound },
  { path: '/documents', label: '知识库', icon: Document },
  { path: '/conversations', label: '会话历史', icon: ChatLineSquare },
]

const activeMenu = computed(() => route.path)

const handleMenuSelect = (path) => {
  router.push(path)
}
</script>

<template>
  <aside class="sidebar">
    <!-- Logo 区域 -->
    <div class="sidebar-brand">
      <div class="sidebar-logo">
        <svg class="logo-icon" viewBox="0 0 32 32" fill="none">
          <rect width="32" height="32" rx="8" fill="url(#logo-grad)" />
          <path
            d="M8 16C8 12.686 10.686 10 14 10C15.894 10 17.56 10.895 18.66 12.3L20.5 10.4C18.92 8.36 16.4 7 14 7C9.03 7 5 11.03 5 16C5 20.97 9.03 25 14 25C16.4 25 18.92 23.64 20.5 21.6L18.66 19.7C17.56 21.105 15.894 22 14 22C10.686 22 8 19.314 8 16Z"
            fill="white"
          />
          <circle cx="22" cy="16" r="5" fill="white" opacity="0.9" />
          <defs>
            <linearGradient id="logo-grad" x1="0" y1="0" x2="32" y2="32">
              <stop stop-color="#4F46E5" />
              <stop offset="1" stop-color="#7C3AED" />
            </linearGradient>
          </defs>
        </svg>
      </div>
      <span class="brand-text">NebulaMind</span>
    </div>

    <!-- 导航菜单 -->
    <nav class="sidebar-nav">
      <div
        v-for="item in menuItems"
        :key="item.path"
        class="nav-item"
        :class="{ active: activeMenu === item.path }"
        @click="handleMenuSelect(item.path)"
      >
        <el-icon class="nav-icon" :size="18">
          <component :is="item.icon" />
        </el-icon>
        <span class="nav-label">{{ item.label }}</span>
      </div>
    </nav>

    <!-- 底部用户信息 -->
    <div class="sidebar-footer">
      <div class="user-avatar">
        <el-avatar :size="32" icon="UserFilled" />
      </div>
      <div class="user-info">
        <span class="user-name">Admin</span>
        <span class="user-role">管理员</span>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  width: var(--sidebar-width);
  height: 100vh;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  flex-shrink: 0;
  user-select: none;
}

/* ---- Brand ---- */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  height: var(--topbar-height);
  padding: 0 var(--space-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.logo-icon {
  width: 28px;
  height: 28px;
}

.brand-text {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  letter-spacing: -0.3px;
}

/* ---- Navigation ---- */
.sidebar-nav {
  flex: 1;
  padding: var(--space-md) var(--space-sm);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.nav-item:hover {
  background: var(--color-bg-alt);
  color: var(--color-text-primary);
}

.nav-item.active {
  background: var(--color-primary-bg);
  color: var(--color-primary);
}

.nav-icon {
  flex-shrink: 0;
}

.nav-label {
  white-space: nowrap;
}

/* ---- Footer ---- */
.sidebar-footer {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md) var(--space-lg);
  border-top: 1px solid var(--color-border-light);
}

.user-avatar {
  flex-shrink: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
}

.user-role {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}
</style>