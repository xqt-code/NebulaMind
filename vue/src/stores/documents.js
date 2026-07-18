import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 文档管理 Store
 * 管理文档列表、上传状态、搜索过滤
 */
export const useDocumentsStore = defineStore('documents', () => {
  /** 文档列表 */
  const documents = ref([
    {
      id: 'doc_001',
      name: '国家电网有限公司配电网工程典型设计10kV架空线路分册_2024版.pdf',
      type: 'pdf',
      size: 81717416,
      uploadTime: Date.now() - 86400000 * 2,
      status: 'parsed',
      description: '2024版10kV架空线路典型设计',
      url: '/api/documents/doc_001/download',
    },
    {
      id: 'doc_002',
      name: '湘电公司设备〔2026〕117号 国网湖南省电力有限公司关于印发配电网防雷指导意见的通知',
      type: 'pdf',
      size: 2646445,
      uploadTime: Date.now() - 86400000,
      status: 'parsed',
      description: '2026版10kV防雷指导意见',
      url: '/api/documents/doc_002/download',
    },
    {
      id: 'doc_003',
      name: '国家电网有限公司配电网工程典型设计10kV配电站房分册_2024.pdf',
      type: 'pdf',
      size: 33790247,
      uploadTime: Date.now() - 3600000,
      status: 'parsing',
      description: '2024版10kV配电站房分册',
      url: '/api/documents/doc_003/download',
    },
  ])

  /** 搜索关键词 */
  const searchQuery = ref('')

  /** 上传中任务列表 */
  const uploadingTasks = ref([])

  /** 过滤后的文档列表 */
  const filteredDocuments = computed(() => {
    if (!searchQuery.value.trim()) return documents.value
    const q = searchQuery.value.toLowerCase()
    return documents.value.filter((doc) =>
      doc.name.toLowerCase().includes(q)
    )
  })

  /** 状态映射 */
  const statusMap = {
    pending: { label: '待解析', type: 'info' },
    parsing: { label: '解析中', type: 'warning' },
    parsed: { label: '已解析', type: 'success' },
    failed: { label: '解析失败', type: 'danger' },
  }

  /**
   * 添加文档
   */
  const addDocument = (doc) => {
    documents.value.unshift({
      ...doc,
      id: doc.id || `doc_${Date.now()}`,
      uploadTime: Date.now(),
      status: 'pending',
    })
  }

  /**
   * 更新文档状态
   */
  const updateDocumentStatus = (docId, status) => {
    const doc = documents.value.find((d) => String(d.id) === String(docId))
    if (doc) {
      doc.status = status
    }
  }

  /**
   * 删除文档
   */
  const removeDocument = (docId) => {
    documents.value = documents.value.filter((d) => d.id !== docId)
  }

  /**
   * 获取文档状态配置
   */
  const getStatusConfig = (status) => {
    return statusMap[status] || statusMap.pending
  }

  /**
   * 格式化文件大小
   */
  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  /**
   * 格式化时间
   */
  const formatTime = (timestamp) => {
    const d = new Date(timestamp)
    const now = new Date()
    const diff = now - d

    if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`
    if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`
    if (diff < 604800000) return `${Math.floor(diff / 86400000)} 天前`

    return d.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    })
  }

  /**
   * 获取文件类型图标
   */
  const getFileTypeIcon = (type) => {
    const icons = {
      pdf: 'Document',
      word: 'Document',
      markdown: 'Memo',
      txt: 'Tickets',
    }
    return icons[type] || 'Document'
  }

  return {
    documents,
    searchQuery,
    uploadingTasks,
    filteredDocuments,
    addDocument,
    updateDocumentStatus,
    removeDocument,
    getStatusConfig,
    formatFileSize,
    formatTime,
    getFileTypeIcon,
  }
})