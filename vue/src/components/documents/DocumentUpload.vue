<script setup>
import { ref, reactive, computed } from 'vue'
import { UploadFilled, Upload, Check, Loading, Close } from '@element-plus/icons-vue'
import { useDocumentsStore } from '@/stores/documents'
import { createUploadTracker } from '@/utils/websocket'

const emit = defineEmits(['uploaded'])
const documentsStore = useDocumentsStore()

/** 上传对话框可见性 */
const visible = ref(false)

/** 文件列表 */
const fileList = ref([])

/** 上传步骤定义 */
const steps = [
  { key: 'upload', label: 'Upload', desc: '上传文件' },
  { key: 'parse', label: 'Parse PDF', desc: '解析文档' },
  { key: 'chunk', label: 'Split Chunk', desc: '文本分块' },
  { key: 'embedding', label: 'Embedding', desc: '向量化' },
  { key: 'store', label: 'Store Vector', desc: '写入向量库' },
  { key: 'ready', label: 'Ready', desc: '完成' },
]

/** 上传任务状态 */
const taskState = reactive({
  active: false,
  taskId: '',
  fileName: '',
  currentStep: -1,
  completed: false,
  error: null,
  wsStatus: 'disconnected',
})

/** 当前步骤索引 */
const activeStep = computed(() => taskState.currentStep)

/** 上传前校验 */
const beforeUpload = (file) => {
  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
    'text/markdown',
    'text/x-markdown',
  ]
  const allowedExtensions = ['.pdf', '.doc', '.docx', '.txt', '.md', '.markdown']

  const ext = '.' + file.name.split('.').pop().toLowerCase()
  const isAllowedType = allowedTypes.includes(file.type) || allowedExtensions.includes(ext)

  if (!isAllowedType) {
    ElMessage.error('仅支持 PDF、Word、TXT、Markdown 格式')
    return false
  }

  const maxSize = 50 * 1024 * 1024
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过 50MB')
    return false
  }

  return true
}

/** 模拟上传及各阶段处理 */
const handleUpload = (options) => {
  const { file } = options
  taskState.active = true
  taskState.taskId = `task_${Date.now()}`
  taskState.fileName = file.name
  taskState.currentStep = 0
  taskState.completed = false
  taskState.error = null

  // 模拟上传进度（替代真实的上传请求）
  const simulateProgress = () => {
    const stepDurations = [800, 1200, 900, 1500, 600]
    let stepIndex = 0

    const advance = () => {
      if (stepIndex >= stepDurations.length) {
        // 全部完成
        taskState.currentStep = 5
        taskState.completed = true
        taskState.active = false

        // 添加文档到列表
        documentsStore.addDocument({
          id: taskState.taskId,
          name: file.name,
          type: getFileType(file.name),
          size: file.size,
          status: 'parsed',
        })

        emit('uploaded')
        return
      }

      taskState.currentStep = stepIndex
      setTimeout(() => {
        stepIndex++
        advance()
      }, stepDurations[stepIndex])
    }

    advance()
  }

  // 开始模拟
  simulateProgress()

  // ====== 真实 WebSocket 实现（Phase 2 启用） ======
  // const tracker = createUploadTracker(taskState.taskId, '/ws/task-progress', {
  //   onTaskStart(data) {
  //     taskState.currentStep = 0
  //   },
  //   onParsing(data) {
  //     taskState.currentStep = 1
  //   },
  //   onEmbedding(data) {
  //     taskState.currentStep = 3
  //   },
  //   onIndexing(data) {
  //     taskState.currentStep = 4
  //   },
  //   onSuccess(data) {
  //     taskState.currentStep = 5
  //     taskState.completed = true
  //     taskState.active = false
  //     documentsStore.addDocument({ ... })
  //     emit('uploaded')
  //     tracker.disconnect()
  //   },
  //   onError(data) {
  //     taskState.error = data.message
  //     taskState.active = false
  //     tracker.disconnect()
  //   },
  //   onStatusChange(status) {
  //     taskState.wsStatus = status
  //   },
  // })
}

/** 根据文件名推断类型 */
const getFileType = (name) => {
  const ext = name.split('.').pop().toLowerCase()
  const map = { pdf: 'pdf', doc: 'word', docx: 'word', txt: 'txt', md: 'markdown', markdown: 'markdown' }
  return map[ext] || 'unknown'
}

/** 打开对话框 */
const open = () => {
  visible.value = true
  resetTask()
}

/** 关闭对话框 */
const close = () => {
  visible.value = false
  resetTask()
}

/** 重置任务状态 */
const resetTask = () => {
  taskState.active = false
  taskState.taskId = ''
  taskState.fileName = ''
  taskState.currentStep = -1
  taskState.completed = false
  taskState.error = null
  fileList.value = []
}

defineExpose({ open, close })
</script>

<template>
  <el-dialog
    v-model="visible"
    title="上传文档"
    width="560px"
    :close-on-click-modal="false"
    destroy-on-close
  >
    <!-- 上传区域 -->
    <div v-if="!taskState.active && !taskState.completed" class="upload-area">
      <el-upload
        v-model:file-list="fileList"
        class="upload-dropzone"
        drag
        multiple
        :auto-upload="false"
        :http-request="handleUpload"
        :before-upload="beforeUpload"
        :limit="20"
        :show-file-list="true"
      >
        <el-icon class="upload-icon" :size="48">
          <UploadFilled />
        </el-icon>
        <div class="upload-text">
          <p class="upload-title">拖拽文件到此处，或<span class="upload-link">点击上传</span></p>
          <p class="upload-hint">支持 PDF、Word、TXT、Markdown，单文件不超过 50MB</p>
        </div>
      </el-upload>
    </div>

    <!-- 处理进度 Timeline -->
    <div v-if="taskState.active || taskState.completed" class="upload-timeline">
      <div class="timeline-file-info">
        <el-icon :size="16"><Document /></el-icon>
        <span class="timeline-filename">{{ taskState.fileName }}</span>
      </div>

      <div class="timeline-steps">
        <div
          v-for="(step, index) in steps"
          :key="step.key"
          class="timeline-step"
          :class="{
            active: index === activeStep,
            done: index < activeStep,
            pending: index > activeStep,
          }"
        >
          <!-- 连接线 -->
          <div class="step-line">
            <div class="step-dot">
              <el-icon v-if="index < activeStep" :size="12"><Check /></el-icon>
              <el-icon v-else-if="index === activeStep" :size="12" class="is-loading"><Loading /></el-icon>
              <span v-else class="step-dot-empty" />
            </div>
            <div v-if="index < steps.length - 1" class="step-connector" :class="{ filled: index < activeStep }" />
          </div>

          <!-- 步骤内容 -->
          <div class="step-content">
            <span class="step-label">{{ step.label }}</span>
            <span class="step-desc">{{ step.desc }}</span>
          </div>
        </div>
      </div>

      <!-- 完成状态 -->
      <div v-if="taskState.completed" class="timeline-success">
        <el-icon :size="18" color="#22C55E"><Check /></el-icon>
        <span>文档处理完成，已加入知识库</span>
      </div>

      <!-- 错误状态 -->
      <div v-if="taskState.error" class="timeline-error">
        <el-icon :size="18"><Close /></el-icon>
        <span>{{ taskState.error }}</span>
      </div>
    </div>

    <template #footer>
      <el-button @click="close">关闭</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
/* ---- Upload Area ---- */
.upload-area {
  padding: var(--space-sm) 0;
}

.upload-dropzone :deep(.el-upload-dragger) {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-xl);
  background: var(--color-bg);
  padding: var(--space-3xl);
  transition: all var(--transition-fast);
}

.upload-dropzone :deep(.el-upload-dragger:hover) {
  border-color: var(--color-primary);
  background: var(--color-primary-bg);
}

.upload-icon {
  color: var(--color-primary);
  margin-bottom: var(--space-lg);
}

.upload-text {
  text-align: center;
}

.upload-title {
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  margin-bottom: var(--space-xs);
}

.upload-link {
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
}

.upload-hint {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

/* ---- Timeline ---- */
.upload-timeline {
  padding: var(--space-lg) 0;
}

.timeline-file-info {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-lg);
  background: var(--color-bg-alt);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-xl);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: var(--font-weight-medium);
}

.timeline-filename {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.timeline-steps {
  display: flex;
  flex-direction: column;
  padding: 0 var(--space-sm);
}

.timeline-step {
  display: flex;
  gap: var(--space-md);
  padding-bottom: var(--space-md);
}

.timeline-step:last-child {
  padding-bottom: 0;
}

/* ---- Step Line ---- */
.step-line {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.step-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-tertiary);
  transition: all var(--transition-normal);
}

.timeline-step.done .step-dot {
  background: var(--color-success);
  border-color: var(--color-success);
  color: white;
}

.timeline-step.active .step-dot {
  border-color: var(--color-primary);
  color: var(--color-primary);
  animation: step-pulse 1.5s ease-in-out infinite;
}

.step-dot-empty {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-text-disabled);
}

.step-connector {
  width: 2px;
  flex: 1;
  min-height: 20px;
  background: var(--color-border);
  margin: 4px 0;
  transition: background var(--transition-normal);
}

.step-connector.filled {
  background: var(--color-success);
}

/* ---- Step Content ---- */
.step-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding-top: 3px;
}

.step-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  font-family: var(--font-mono);
}

.timeline-step.pending .step-label {
  color: var(--color-text-disabled);
}

.step-desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.timeline-step.active .step-label {
  color: var(--color-primary);
}

/* ---- Success / Error ---- */
.timeline-success {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-top: var(--space-xl);
  padding: var(--space-md) var(--space-lg);
  background: var(--color-success-bg);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: #16A34A;
  font-weight: var(--font-weight-medium);
}

.timeline-error {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-top: var(--space-xl);
  padding: var(--space-md) var(--space-lg);
  background: rgba(239, 68, 68, 0.08);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: #DC2626;
  font-weight: var(--font-weight-medium);
}

@keyframes step-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.3); }
  50% { box-shadow: 0 0 0 6px rgba(79, 70, 229, 0); }
}
</style>