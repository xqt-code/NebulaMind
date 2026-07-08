<script setup>
import { ref } from 'vue'
import { ArrowDown, Document, ChatDotRound } from '@element-plus/icons-vue'

defineProps({
  systemPrompt: { type: String, default: '' },
  userPrompt: { type: String, default: '' },
})

const expanded = ref(false)
</script>

<template>
  <div class="prompt-preview">
    <div class="section-header" @click="expanded = !expanded">
      <el-icon :size="14"><ArrowDown /></el-icon>
      <span>Prompt Preview</span>
      <el-icon
        :size="14"
        class="collapse-icon"
        :class="{ rotated: expanded }"
      >
        <ArrowDown />
      </el-icon>
    </div>

    <div v-show="expanded" class="prompt-content">
      <div class="prompt-block">
        <div class="prompt-block-header">
          <el-icon :size="12"><Document /></el-icon>
          <span>System Prompt</span>
          <span class="prompt-token-count">{{ systemPrompt.length }} chars</span>
        </div>
        <pre class="prompt-text">{{ systemPrompt }}</pre>
      </div>

      <div class="prompt-block">
        <div class="prompt-block-header">
          <el-icon :size="12"><ChatDotRound /></el-icon>
          <span>User Prompt</span>
          <span class="prompt-token-count">{{ userPrompt.length }} chars</span>
        </div>
        <pre class="prompt-text">{{ userPrompt }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.prompt-preview {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  cursor: pointer;
  user-select: none;
  background: var(--color-bg);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: background var(--transition-fast);
}

.section-header:hover {
  background: var(--color-bg-alt);
}

.collapse-icon {
  margin-left: auto;
  transition: transform var(--transition-fast);
}

.collapse-icon.rotated {
  transform: rotate(180deg);
}

.prompt-content {
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.prompt-block {
  background: var(--color-bg);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.prompt-block-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-xs) var(--space-md);
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  border-bottom: 1px solid var(--color-border-light);
  background: var(--color-bg-alt);
}

.prompt-token-count {
  margin-left: auto;
  font-family: var(--font-mono);
  font-size: 10px;
}

.prompt-text {
  padding: var(--space-md);
  margin: 0;
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  line-height: var(--line-height-relaxed);
  color: var(--color-text-secondary);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 300px;
  overflow-y: auto;
}
</style>