<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, RefreshRight } from '@element-plus/icons-vue'
import { useDocumentsStore } from '@/stores/documents'
import DocumentUpload from '@/components/documents/DocumentUpload.vue'
import DocumentList from '@/components/documents/DocumentList.vue'

const documentsStore = useDocumentsStore()
const uploadRef = ref(null)

/** 打开上传对话框 - 改用弹窗或直接提示 */
const handleOpenUpload = () => {
  // 方法1：直接提示用户（推荐，因为上传组件始终可见）
  ElMessage.info('请直接在上方区域拖拽或点击上传文件')

  // 方法2（可选）：如果上传组件在弹窗里，控制弹窗显示
  // 这里暂时用方法1，因为你上传组件是始终显示的
}

/** 上传完成回调 */
const handleUploaded = (data) => {
  // data 结构：{ success: true, total: 1 }
  if (data && data.success) {
    ElMessage.success('文件上传成功，列表已更新')
  }
}

/** 刷新列表 */
const handleRefresh = () => {
  // TODO: Phase 2 接入真实 API
  ElMessage.success('列表已刷新')
}

/** 单个文件上传成功回调（收到 taskId 后启动轮询） */
const handleUploadSuccess = (payload) => {
  // payload 结构：{ file: file, taskId: taskId }
  console.log('上传成功，taskId:', payload.taskId)
  // 注意：轮询逻辑已经在 DocumentUpload 组件内部实现了，
  // 这里只做状态记录，不需要重复轮询
}
</script>

<template>
  <div class="documents-view">
    <div class="page-header">
      <div>
        <h1 class="page-title">知识库管理</h1>
        <p class="page-desc">管理您的知识库文档，上传文档以扩展电力智能助手的知识范围。</p>
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
        @upload-complete="handleUploaded"
        @upload-success="handleUploadSuccess"
    />
  </div>
</template>

<style scoped>
.documents-view {
  max-width: 1060px;
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a2e;
  letter-spacing: -0.3px;
}

.page-desc {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

.page-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}
</style>