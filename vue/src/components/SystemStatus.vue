<script setup>
import { useSystemStore } from '@/stores/system'

const systemStore = useSystemStore()
</script>

<template>
  <div class="system-status">
    <div
      v-for="comp in systemStore.components"
      :key="comp.key"
      class="status-item"
      :title="`${comp.label}: ${comp.status === 'up' ? '正常' : '异常'}`"
    >
      <span class="status-dot" :class="comp.status"></span>
      <span class="status-label">{{ comp.label }}</span>
    </div>
  </div>
</template>

<style scoped>
.system-status {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
}

.status-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: default;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-dot.up {
  background: var(--color-success);
  box-shadow: 0 0 4px rgba(34, 197, 94, 0.4);
}

.status-dot.down {
  background: var(--color-error);
  box-shadow: 0 0 4px rgba(239, 68, 68, 0.4);
}

.status-dot.unknown {
  background: var(--color-text-disabled);
}

.status-label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-tertiary);
  white-space: nowrap;
}
</style>