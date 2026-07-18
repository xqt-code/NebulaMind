<!--
  文档上传组件
  位置： src/views/documents/DocumentUpload.vue

  职责：
    1. 提供文件拖拽上传和点击上传两种方式
    2. 文件上传前校验（类型、大小、数量）
    3. 显示文件上传进度
    4. 上传成功后通知父组件刷新列表
    5. 上传失败后展示错误信息并支持重试

  技术栈：
    - Vue 3 Composition API（script setup）
    - Element Plus UI 组件
    - Axios 请求库
    - Pinia 状态管理
-->

<script setup>
// ============================================================================
// 1. 导入依赖
// ============================================================================

// Vue 核心 API
import { ref, computed, onMounted } from 'vue'

// Element Plus 组件和工具
import { ElMessage, ElMessageBox } from 'element-plus'
import { UploadFilled, Document, Tickets, Memo } from '@element-plus/icons-vue'

// Pinia 状态管理
import { useDocumentsStore } from '@/stores/documents'

// HTTP 请求工具（项目统一封装的 axios 实例）
import request from '@/api/request'

// 日志工具（开发调试用）
import { getLogger } from '@/utils/logger'

// ============================================================================
// 2. 初始化状态
// ============================================================================

const logger = getLogger('DocumentUpload')

// Pinia store
const documentsStore = useDocumentsStore()

// ============================================================================
// 3. 响应式状态定义
// ============================================================================

/**
 * 文件列表 - 存储用户已选但尚未上传的文件
 * 每个文件对象包含：name, size, type, status, progress, uid, raw
 * status: 'ready' | 'uploading' | 'success' | 'error'
 */
const fileList = ref([])

/**
 * 是否正在上传
 */
const isUploading = ref(false)

/**
 * 当前上传进度（0-100）
 */
const uploadProgress = ref(0)

/**
 * 当前上传的 taskId（用于跟踪任务状态）
 */
const currentTaskId = ref(null)

// ============================================================================
// 4. 计算属性
// ============================================================================

/**
 * 是否有文件正在上传
 */
const hasUploading = computed(() => {
  return fileList.value.some(f => f.status === 'uploading')
})

/**
 * 是否所有文件都已上传完成
 */
const allUploaded = computed(() => {
  if (fileList.value.length === 0) return false
  return fileList.value.every(f => f.status === 'success')
})

/**
 * 已选文件总数
 */
const totalFiles = computed(() => fileList.value.length)

/**
 * 成功上传的文件数
 */
const successCount = computed(() => {
  return fileList.value.filter(f => f.status === 'success').length
})

/**
 * 上传按钮是否可用
 */
const canUpload = computed(() => {
  return fileList.value.length > 0 && !isUploading.value
})

/**
 * 是否有失败的文件
 */
const hasErrorFiles = computed(() => {
  return fileList.value.some(f => f.status === 'error')
})

// ============================================================================
// 5. 核心方法 - 文件校验
// ============================================================================

/**
 * 校验单个文件
 * @param {File} file - 要校验的文件
 * @returns {Object} { valid: boolean, message: string }
 */
const validateFile = (file) => {
  // 1. 校验文件大小（限制 50MB）
  const maxSize = 50 * 1024 * 1024  // 50MB
  if (file.size > maxSize) {
    return {
      valid: false,
      message: `文件 ${file.name} 大小超过 50MB 限制`
    }
  }

  // 2. 校验文件类型（只允许 PDF、Word、TXT、Markdown）
  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
    'text/markdown'
  ]
  // 如果 MIME 类型不在白名单中，再检查文件扩展名
  const isAllowedType = allowedTypes.includes(file.type)
  const allowedExtensions = ['.pdf', '.doc', '.docx', '.txt', '.md']
  const fileExtension = `.${file.name.split('.').pop().toLowerCase()}`
  const isAllowedExtension = allowedExtensions.includes(fileExtension)

  if (!isAllowedType && !isAllowedExtension) {
    return {
      valid: false,
      message: `文件 ${file.name} 类型不支持，仅支持 PDF、Word、TXT、Markdown`
    }
  }

  // 3. 校验文件名是否包含非法字符
  const illegalChars = /[<>:"/\\|?*]/
  if (illegalChars.test(file.name)) {
    return {
      valid: false,
      message: `文件 ${file.name} 包含非法字符`
    }
  }

  return { valid: true, message: '' }
}

/**
 * 校验所有文件
 * @param {Array} files - 文件列表
 * @returns {Object} { valid: boolean, errors: Array }
 */
const validateAllFiles = (files) => {
  const errors = []
  for (const file of files) {
    const result = validateFile(file)
    if (!result.valid) {
      errors.push(result.message)
    }
  }
  return {
    valid: errors.length === 0,
    errors
  }
}

// ============================================================================
// 6. 核心方法 - 文件上传
// ============================================================================

/**
 * 上传单个文件到后端
 * @param {File} file - 要上传的文件
 * @param {number} index - 文件在列表中的索引
 * @returns {Promise} 上传结果
 */
const uploadSingleFile = async (file, index) => {
  const startTime = Date.now()

  try {
    // 1. 更新文件状态为“上传中”
    file.status = 'uploading'
    file.progress = 0

    // 2. 构建 FormData
    const formData = new FormData()
    formData.append('file', file.raw || file)
    formData.append('tenantId', '1')  // 多租户场景，后续从用户上下文获取

    // 3. 发送上传请求（带进度回调）
    const response = await request.post('/api/v1/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      // 上传进度回调（由 axios 提供）
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percent = Math.round((progressEvent.loaded / progressEvent.total) * 100)
          file.progress = percent
          // 更新全局上传进度
          updateOverallProgress()
        }
      }
    })

    // 4. 处理响应
    // 响应结构：{ code, msg, data: { taskId, status } }
    const result = response.data || response
    if (result.code === 200 || result.code === '200') {
      // 上传成功
      file.status = 'success'
      file.taskId = result.data?.taskId || result.data
      file.uploadTime = new Date().toISOString()
      file.uploadDuration = Date.now() - startTime

      logger.info(`文件上传成功: ${file.name}, taskId: ${file.taskId}`)

      // 触发成功事件（通知父组件刷新列表）
      emit('upload-success', {
        file: file,
        taskId: file.taskId
      })

      // ========== 新增：启动轮询 ==========
      const taskId = file.taskId
      const timer = setInterval(async () => {
        try {
          const res = await request.get(`/api/v1/documents/${taskId}`)
          const data = res.data || res
          const status = data.parseStatus
          const progress = data.parseProgress || 0

          // 更新进度显示（在文件列表里展示）
          file.progress = progress
          file.parseStatus = status

          if (status === 'PARSED') {
            clearInterval(timer)
            ElMessage.success('文档解析完成！')
            documentsStore.updateDocumentStatus(taskId, 'parsed')
          } else if (status === 'FAILED') {
            clearInterval(timer)
            ElMessage.error(`文档解析失败：${data.errorMessage || '未知错误'}`)
            documentsStore.updateDocumentStatus(taskId, 'failed')
          } else {
            // PENDING 或 PARSING，继续等待
            console.log(`解析中... ${progress}%`)
          }
        } catch (error) {
          clearInterval(timer)
          ElMessage.error('查询解析状态失败')
        }
      }, 2000) // 每 2 秒轮询一次
// ========== 新增结束 ==========

      return { success: true, taskId: file.taskId }
    } else {
      // 业务错误
      throw new Error(result.msg || '上传失败')
    }
  } catch (error) {
    // 上传失败
    file.status = 'error'
    file.errorMessage = error.message || '上传失败，请稍后重试'

    logger.error(`文件上传失败: ${file.name}, 错误: ${error.message}`)

    // 触发失败事件
    emit('upload-error', {
      file: file,
      error: error
    })

    // 显示错误提示
    ElMessage.error(`文件 ${file.name} 上传失败: ${file.errorMessage}`)

    return { success: false, error: error.message }
  }
}

/**
 * 批量上传文件
 * 按顺序逐个上传（避免并发过多导致服务器压力）
 */
const handleUpload = async () => {
  // 1. 前置校验：是否所有文件都已通过前端校验
  if (fileList.value.length === 0) {
    ElMessage.warning('请先选择文件')
    return
  }

  // 2. 检查是否有文件已经在上传中
  if (hasUploading.value) {
    ElMessage.warning('有文件正在上传中，请等待完成')
    return
  }

  // 3. 确认是否覆盖已上传的文件
  const hasSuccess = fileList.value.some(f => f.status === 'success')
  if (hasSuccess) {
    try {
      await ElMessageBox.confirm(
          '已有文件上传成功，继续上传将覆盖已有文件，是否继续？',
          '提示',
          {
            confirmButtonText: '继续上传',
            cancelButtonText: '取消',
            type: 'warning'
          }
      )
    } catch {
      return  // 用户取消
    }
  }

  // 4. 重置状态
  isUploading.value = true
  uploadProgress.value = 0
  currentTaskId.value = null

  // 5. 逐个上传
  let successCount = 0
  let failCount = 0

  try {
    for (let i = 0; i < fileList.value.length; i++) {
      const file = fileList.value[i]
      // 跳过已成功上传的文件（除非用户选择重新上传）
      if (file.status === 'success') continue

      const result = await uploadSingleFile(file, i)
      if (result.success) {
        successCount++
        // 更新全局进度
        uploadProgress.value = Math.round(((i + 1) / fileList.value.length) * 100)
      } else {
        failCount++
      }
    }

    // 6. 上传完成后的状态处理
    if (failCount === 0) {
      ElMessage.success(`全部 ${successCount} 个文件上传成功！`)
      // 上传成功后可自动触发刷新
      emit('upload-complete', { success: true, total: fileList.value.length })
    } else if (successCount === 0) {
      ElMessage.error('所有文件上传失败，请检查网络后重试')
    } else {
      ElMessage.warning(`上传完成：成功 ${successCount} 个，失败 ${failCount} 个`)
    }
  } catch (error) {
    logger.error('批量上传异常:', error)
    ElMessage.error('上传过程中发生异常，请刷新后重试')
  } finally {
    isUploading.value = false
    // 如果有失败的文件，允许用户重试
    const hasError = fileList.value.some(f => f.status === 'error')
    if (hasError) {
      // 保留失败的文件，让用户手动重试
    } else {
      // 全部成功，清空列表或保留成功列表
    }
  }
}

/**
 * 更新总体上传进度
 */
const updateOverallProgress = () => {
  const total = fileList.value.length
  if (total === 0) {
    uploadProgress.value = 0
    return
  }
  const sum = fileList.value.reduce((acc, f) => acc + (f.progress || 0), 0)
  uploadProgress.value = Math.round(sum / total)
}

// ============================================================================
// 7. 文件列表管理
// ============================================================================

/**
 * 添加文件到列表（由 el-upload 触发）
 */
const handleFileChange = (file, fileListData) => {
  // 1. 校验单个文件
  const validation = validateFile(file.raw)
  if (!validation.valid) {
    ElMessage.warning(validation.message)
    // 从列表中移除无效文件
    const index = fileList.value.findIndex(f => f.uid === file.uid)
    if (index !== -1) {
      fileList.value.splice(index, 1)
    }
    return
  }

  // 2. 检查是否已存在同名文件
  const exists = fileList.value.some(f => f.name === file.name && f.size === file.size)
  if (exists) {
    ElMessage.warning(`文件 ${file.name} 已存在，请勿重复添加`)
    return
  }

  // 3. 添加到文件列表
  fileList.value.push({
    uid: file.uid,
    name: file.name,
    size: file.size,
    type: file.type,
    raw: file.raw,
    status: 'ready',        // ready | uploading | success | error
    progress: 0,
    taskId: null,
    errorMessage: null,
    uploadTime: null,
    uploadDuration: null
  })

  logger.info(`已添加文件: ${file.name}`)
}

/**
 * 移除文件（用户主动删除）
 */
const handleRemoveFile = (file) => {
  const index = fileList.value.findIndex(f => f.uid === file.uid)
  if (index !== -1) {
    // 如果文件正在上传，不允许删除
    if (fileList.value[index].status === 'uploading') {
      ElMessage.warning('文件正在上传中，请等待完成后再删除')
      return
    }
    fileList.value.splice(index, 1)
    logger.info(`已移除文件: ${file.name}`)
    updateOverallProgress()
  }
}

/**
 * 清空所有文件
 */
const handleClearAll = () => {
  if (isUploading.value) {
    ElMessage.warning('有文件正在上传，请等待完成后再清空')
    return
  }
  ElMessageBox.confirm(
      '确定要清空所有文件吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
  ).then(() => {
    fileList.value = []
    uploadProgress.value = 0
    ElMessage.success('已清空所有文件')
  }).catch(() => {})
}

/**
 * 重试上传失败的文件
 */
const handleRetryFailed = () => {
  const failedFiles = fileList.value.filter(f => f.status === 'error')
  if (failedFiles.length === 0) {
    ElMessage.info('没有失败的文件需要重试')
    return
  }
  // 重置失败文件状态为 ready，然后触发上传
  failedFiles.forEach(f => {
    f.status = 'ready'
    f.progress = 0
    f.errorMessage = null
  })
  handleUpload()
}

/**
 * 重试单个文件
 */
const handleRetrySingle = (file) => {
  if (file.status !== 'error') {
    ElMessage.info('该文件无需重试')
    return
  }
  // 重置状态为 ready
  file.status = 'ready'
  file.progress = 0
  file.errorMessage = null
  // 触发上传
  handleUpload()
}

// ============================================================================
// 8. 格式化工具函数
// ============================================================================

/**
 * 格式化文件大小
 */
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 获取文件状态对应的标签类型
 */
const getStatusType = (status) => {
  const map = {
    'ready': 'info',
    'uploading': 'warning',
    'success': 'success',
    'error': 'danger'
  }
  return map[status] || 'info'
}

/**
 * 获取文件状态对应的显示文字
 */
const getStatusText = (status) => {
  const map = {
    'ready': '待上传',
    'uploading': '上传中',
    'success': '已上传',
    'error': '上传失败'
  }
  return map[status] || '未知'
}

/**
 * 根据文件名获取对应的图标名称
 */
const getFileIcon = (fileName) => {
  if (!fileName) return 'Document'
  const ext = fileName.split('.').pop().toLowerCase()
  const iconMap = {
    pdf: 'Document',
    doc: 'Document',
    docx: 'Document',
    txt: 'Tickets',
    md: 'Memo',
    markdown: 'Memo',
  }
  return iconMap[ext] || 'Document'
}

// ============================================================================
// 9. 组件事件
// ============================================================================

/**
 * 组件事件定义
 * - upload-success: 单个文件上传成功
 * - upload-error: 单个文件上传失败
 * - upload-complete: 所有文件上传完成
 */
const emit = defineEmits([
  'upload-success',
  'upload-error',
  'upload-complete'
])

// ============================================================================
// 10. 生命周期
// ============================================================================

onMounted(() => {
  logger.info('DocumentUpload 组件已挂载')
})

// ============================================================================
// 11. 暴露给父组件的方法
// ============================================================================

defineExpose({
  upload: handleUpload,
  clear: handleClearAll,
  retry: handleRetryFailed
})
</script>

<template>
  <!-- ========================================================================== -->
  <!-- 模板部分 -->
  <!-- ========================================================================== -->

  <div class="document-upload">

    <!-- -------- 1. 上传区域（el-upload） -------- -->
    <el-upload
        ref="uploadRef"
        class="upload-area"
        drag
        multiple
        :auto-upload="false"
        :limit="10"
        :on-change="handleFileChange"
        :on-remove="handleRemoveFile"
        :file-list="fileList"
        :disabled="isUploading"
    >
      <!-- 上传区域内容 -->
      <template #default>
        <div class="upload-content">
          <!-- 图标 -->
          <el-icon class="upload-icon" :size="48">
            <UploadFilled />
          </el-icon>
          <div class="upload-text">
            <span class="upload-title">拖拽文件到此处，或点击选择文件</span>
            <span class="upload-hint">
              支持 PDF、Word、TXT、Markdown 格式
            </span>
            <span class="upload-limit">
              单个文件不超过 50MB，单次最多上传 10 个文件
            </span>
          </div>
        </div>
      </template>
      <!-- 文件列表插槽（自定义展示） -->
      <template #file="{ file }">
        <!-- 我们在下面的文件列表中统一展示，所以这里留空 -->
      </template>
    </el-upload>

    <!-- -------- 2. 文件列表 -------- -->
    <div v-if="fileList.length > 0" class="file-list">
      <div class="file-list-header">
        <span class="file-list-title">
          已选文件（{{ fileList.length }} 个）
        </span>
        <span class="file-list-actions">
          <el-button
              v-if="hasErrorFiles"
              type="warning"
              size="small"
              @click="handleRetryFailed"
          >
            全部重试
          </el-button>
          <el-button
              size="small"
              @click="handleClearAll"
              :disabled="isUploading"
          >
            清空
          </el-button>
        </span>
      </div>

      <!-- 文件列表网格 -->
      <div class="file-grid">
        <div
            v-for="file in fileList"
            :key="file.uid"
            class="file-item"
            :class="`file-item--${file.status}`"
        >
          <!-- 文件图标 -->
          <div class="file-icon">
            <el-icon :size="24">
              <component :is="getFileIcon(file.name)" />
            </el-icon>
          </div>

          <!-- 文件信息 -->
          <div class="file-info">
            <div class="file-name" :title="file.name">
              {{ file.name }}
            </div>
            <div class="file-meta">
              <span class="file-size">{{ formatFileSize(file.size) }}</span>
              <el-tag
                  :type="getStatusType(file.status)"
                  size="small"
                  effect="plain"
              >
                {{ getStatusText(file.status) }}
              </el-tag>
            </div>
          </div>

          <!-- 进度条（上传中显示） -->
          <div v-if="file.status === 'uploading'" class="file-progress">
            <el-progress
                :percentage="file.progress || 0"
                :stroke-width="6"
                :text-inside="true"
            />
          </div>

          <!-- 错误信息（失败时显示） -->
          <div v-if="file.status === 'error'" class="file-error">
            <el-text type="danger" size="small">
              {{ file.errorMessage || '上传失败' }}
            </el-text>
          </div>

          <!-- 操作按钮 -->
          <div class="file-actions">
            <el-button
                v-if="file.status === 'error'"
                type="primary"
                size="small"
                plain
                @click="handleRetrySingle(file)"
            >
              重试
            </el-button>
            <el-button
                type="danger"
                size="small"
                plain
                :disabled="file.status === 'uploading'"
                @click="handleRemoveFile(file)"
            >
              移除
            </el-button>
          </div>
        </div>
      </div>

      <!-- 总体进度 -->
      <div v-if="isUploading" class="upload-overall-progress">
        <el-progress
            :percentage="uploadProgress"
            :stroke-width="8"
            :text-inside="true"
            status="active"
        />
      </div>

      <!-- 上传按钮 -->
      <div class="upload-actions">
        <el-button
            type="primary"
            size="large"
            :loading="isUploading"
            :disabled="!canUpload"
            @click="handleUpload"
        >
          {{ isUploading ? '上传中...' : '开始上传' }}
        </el-button>
        <span v-if="isUploading" class="upload-tip">
          正在上传 {{ successCount }}/{{ totalFiles }} 个文件
        </span>
      </div>
    </div>

    <!-- -------- 3. 空状态 -------- -->
    <el-empty
        v-else
        description="暂无文件，请点击上方区域上传"
        :image-size="120"
    />
  </div>
</template>

<!-- ========================================================================== -->
<!-- 样式 -->
<!-- ========================================================================== -->

<style scoped lang="scss">
.document-upload {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: var(--el-bg-color-page);
}

/* -------- 上传区域 -------- */
.upload-area {
  flex-shrink: 0;
}

.upload-area :deep(.el-upload-dragger) {
  padding: 40px 20px;
  border: 2px dashed var(--el-border-color);
  border-radius: 12px;
  transition: all 0.3s ease;
  background-color: var(--el-bg-color);
}

.upload-area :deep(.el-upload-dragger:hover) {
  border-color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}

.upload-area :deep(.el-upload-dragger.is-dragover) {
  border-color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-8);
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload-icon {
  color: var(--el-color-primary);
  font-size: 48px;
}

.upload-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.upload-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.upload-hint {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.upload-limit {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
}

/* -------- 文件列表 -------- */
.file-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 200px;
  padding: 16px;
  background-color: var(--el-bg-color);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.file-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.file-list-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.file-list-actions {
  display: flex;
  gap: 8px;
}

/* -------- 文件网格 -------- */
.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  max-height: 400px;
  overflow-y: auto;
}

.file-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px 16px;
  background-color: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.file-item:hover {
  border-color: var(--el-color-primary-light-5);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.file-item--success {
  border-color: var(--el-color-success-light-5);
  background-color: var(--el-color-success-light-9);
}

.file-item--error {
  border-color: var(--el-color-danger-light-5);
  background-color: var(--el-color-danger-light-9);
}

.file-item--uploading {
  border-color: var(--el-color-warning-light-5);
  background-color: var(--el-color-warning-light-9);
}

.file-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
}

.file-size {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.file-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
}

.file-progress {
  margin: 4px 0;
}

.file-error {
  font-size: 12px;
  color: var(--el-color-danger);
}

.file-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 4px;
}

/* -------- 整体进度 -------- */
.upload-overall-progress {
  padding: 8px 0;
}

/* -------- 上传按钮 -------- */
.upload-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-light);
}

.upload-tip {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

/* -------- 滚动条样式 -------- */
.file-grid::-webkit-scrollbar {
  width: 4px;
}

.file-grid::-webkit-scrollbar-track {
  background: transparent;
}

.file-grid::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 4px;
}

.file-grid::-webkit-scrollbar-thumb:hover {
  background: var(--el-text-color-placeholder);
}
</style>