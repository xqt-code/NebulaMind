/**
 * API 抽象层
 * 支持三种模式：SSE（流式）、HTTP（普通请求）、Mock（开发调试）
 */
import request from './request'
import { createSSEStream } from '@/utils/sse'

const ENABLE_MOCK = import.meta.env.VITE_ENABLE_MOCK === 'true'

// ==================== Chat API ====================

/** Mock 聊天响应生成器 */
const mockChatComplete = async (message) => {
  // 由 chat store 的 createMockStream 处理
  return null
}

/**
 * 发送聊天消息（流式 SSE）
 * @param {object} params
 * @param {string} params.message - 用户消息
 * @param {string} params.conversationId - 会话 ID
 * @param {object} options - SSE 选项
 */
export const chatStream = (params, options = {}) => {
  if (ENABLE_MOCK) {
    // Mock 模式：由 chat store 的 createMockStream 处理
    throw new Error('MOCK_MODE')
  }

  return createSSEStream('/api/chat/stream', {
    body: params,
    ...options,
  })
}

/**
 * 发送聊天消息（非流式）
 */
export const chatSend = (params) => {
  if (ENABLE_MOCK) {
    return mockChatComplete(params.message)
  }
  return request.post('/api/chat/send', params)
}

// ==================== Documents API ====================

/** Mock 文档列表 */
const mockDocuments = [
  {
    id: 'doc_001',
    name: 'RAG 技术白皮书 v2.3.pdf',
    type: 'pdf',
    size: 2457600,
    uploadTime: Date.now() - 86400000 * 2,
    status: 'parsed',
    url: '/api/documents/doc_001/download',
  },
  {
    id: 'doc_002',
    name: '企业知识库架构设计.md',
    type: 'markdown',
    size: 51200,
    uploadTime: Date.now() - 86400000,
    status: 'parsed',
    url: '/api/documents/doc_002/download',
  },
]

/**
 * 获取文档列表
 */
export const getDocuments = (params = {}) => {
  if (ENABLE_MOCK) {
    return Promise.resolve({
      code: 200,
      data: {
        records: mockDocuments,
        total: mockDocuments.length,
      },
    })
  }
  return request.get('/api/documents', { params })
}

/**
 * 上传文档
 */
export const uploadDocument = (formData, onProgress) => {
  return request.post('/api/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: onProgress,
  })
}

/**
 * 删除文档
 */
export const deleteDocument = (docId) => {
  return request.delete(`/api/documents/${docId}`)
}

/**
 * 获取文档下载链接
 */
export const getDocumentUrl = (docId) => {
  return request.get(`/api/documents/${docId}/url`)
}

// ==================== System API ====================

/** Mock 健康状态 */
const mockHealth = {
  status: 'UP',
  components: {
    aiService: { status: 'UP', details: { model: 'qwen3-32b' } },
    embedding: { status: 'UP', details: { model: 'bge-large-zh-v1.5', dim: 768 } },
    milvus: { status: 'UP', details: { version: '2.4.0', collections: 3 } },
    redis: { status: 'UP', details: { version: '7.2', usedMemory: '128MB' } },
    llm: { status: 'UP', details: { provider: 'openai', latency: '120ms' } },
  },
}

/**
 * 获取系统健康状态
 */
export const getHealth = () => {
  if (ENABLE_MOCK) {
    return Promise.resolve({ code: 200, data: mockHealth })
  }
  return request.get('/actuator/health')
}

// ==================== Conversations API ====================

/**
 * 获取会话列表
 */
export const getConversations = (params = {}) => {
  if (ENABLE_MOCK) {
    return Promise.resolve({
      code: 200,
      data: {
        records: [],
        total: 0,
      },
    })
  }
  return request.get('/api/conversations', { params })
}

/**
 * 删除会话
 */
export const deleteConversation = (id) => {
  return request.delete(`/api/conversations/${id}`)
}

export default {
  chatStream,
  chatSend,
  getDocuments,
  uploadDocument,
  deleteDocument,
  getDocumentUrl,
  getHealth,
  getConversations,
  deleteConversation,
}