<script setup>
import Sidebar from '@/components/Sidebar.vue'
import TopBar from '@/components/TopBar.vue'
</script>

<template>
  <div class="app-layout">
    <Sidebar />
    <div class="app-main">
      <TopBar />
      <main class="app-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100vh;
}

.app-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-xl);
  background: var(--color-bg);
}

/* 路由切换过渡 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-fast);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>