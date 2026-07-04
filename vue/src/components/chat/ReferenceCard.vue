<script setup>
import { Document, Search } from '@element-plus/icons-vue'

defineProps({
  reference: {
    type: Object,
    required: true,
  },
  showExplain: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggleExplain'])
</script>

<template>
  <div class="reference-card">
    <div class="ref-header">
      <el-icon :size="14" class="ref-icon"><Document /></el-icon>
      <span class="ref-name">{{ reference.docName }}</span>
      <el-button
        link
        type="primary"
        :icon="Search"
        class="ref-explain-btn"
        @click="emit('toggleExplain')"
      >
        {{ showExplain ? '收起解释' : '查看解释' }}
      </el-button>
    </div>
    <p class="ref-snippet">{{ reference.snippet }}</p>
  </div>
</template>

<style scoped>
.reference-card {
  background: var(--color-bg-alt);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-md) var(--space-lg);
  transition: border-color var(--transition-fast);
}

.reference-card:hover {
  border-color: var(--color-primary-light);
}

.ref-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-xs);
}

.ref-icon {
  color: var(--color-primary);
  flex-shrink: 0;
}

.ref-name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ref-explain-btn {
  font-size: var(--font-size-xs);
  flex-shrink: 0;
}

.ref-snippet {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: var(--line-height-relaxed);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>