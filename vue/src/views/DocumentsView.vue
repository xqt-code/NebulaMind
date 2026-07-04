<script setup>
import { ref } from 'vue'
import { Upload, RefreshRight } from '@element-plus/icons-vue'
import { useDocumentsStore } from '@/stores/documents'
import DocumentUpload from '@/components/documents/DocumentUpload.vue'
import DocumentList from '@/components/documents/DocumentList.vue'

const documentsStore = useDocumentsStore()
const uploadRef = ref(null)

/** 打开上传对话框 */
const handleOpenUpload = () => {
  uploadRef.value?.open()
}

/** 上传完成回调 */
const handleUploaded = () => {
  // 文档列表已自动刷新
}

/** 刷新列表 */
const handleRefresh = () => {
  // TODO: Phase 2 接入真实 API
  ElMessage.success('列表已刷新')
}
</script>

<template>
  <div class="documents-view">
    <div class="page-header">
      <div>
        <h1 class="page-title">知识库管理</h1>
        <p class="page-desc">管理您的知识库文档，上传文档以扩展 AI 的知识范围。</p>
      </div>
      <div class="page-actions">
        <el-button :icon="RefreshRight" @click="handleRefresh">
          刷新
        </el-button>
        <el-button type="primary" :icon="Upload" @click="handleOpenUpload">
          上传文档
        </el-button>
      </div>
    </div>

    <DocumentList />

    <DocumentUpload
      ref="uploadRef"
      @uploaded="handleUploaded"
    />
  </div>
</template>

<style scoped>
.documents-view {
  max-width: 1060px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
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

.page-actions {
  display: flex;
  gap: var(--space-sm);
  flex-shrink: 0;
}
</style>