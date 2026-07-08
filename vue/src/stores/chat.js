import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { createSSEStream, createMockStream } from '@/utils/sse'

// 在文件顶部引入真实的 API（确保 `api/chat.js` 已存在）
// 确保顶部已经导入了 askQuestion 和 ElMessage
import { askQuestion } from '@/api/chat'
import { ElMessage } from 'element-plus'

/**
 * 聊天功能 Store
 * 管理消息列表、流式状态、会话控制
 */
export const useChatStore = defineStore('chat', () => {
  /** 消息列表 */
  const messages = ref([])

  /** 是否正在流式生成 */
  const isStreaming = ref(false)

  /** 流式生成状态提示 */
  const streamingStatus = ref('')

  /** 当前流式 AI 消息索引 */
  const streamingIndex = ref(-1)

  /** 取消流函数 */
  let cancelStream = null

  /** 消息 ID 计数器 */
  let messageIdCounter = 0

  /** 是否超过虚拟滚动阈值 */
  const useVirtualScroll = computed(() => messages.value.length > 100)

  /**
   * 生成唯一消息 ID
   */
  const generateId = () => `msg_${Date.now()}_${++messageIdCounter}`

  /**
   * 生成 TraceID（24 位十六进制）
   */
  const generateTraceId = () => {
    const chars = '0123456789abcdef'
    let id = ''
    for (let i = 0; i < 24; i++) {
      id += chars[Math.floor(Math.random() * 16)]
    }
    return id
  }

  /**
   * 构建原始响应 JSON（Mock）
   */
  const buildRawResponse = (userQuery) => ({
    id: 'chatcmpl-' + Math.random().toString(36).slice(2, 10),
    object: 'chat.completion',
    created: Math.floor(Date.now() / 1000),
    model: 'qwen3-32b',
    choices: [
      {
        index: 0,
        message: {
          role: 'assistant',
          content: '...',
        },
        finish_reason: 'stop',
      },
    ],
    usage: {
      prompt_tokens: 1247,
      completion_tokens: 389,
      total_tokens: 1636,
    },
    metadata: {
      trace_id: generateTraceId(),
      latency_ms: 1316,
      retriever_top_k: 3,
      confidence: 0.92,
      query: userQuery,
      timestamp: new Date().toISOString(),
    },
  })

  /**
   * 创建用户消息
   */
  const createUserMessage = (content) => ({
    id: generateId(),
    role: 'user',
    content,
    timestamp: Date.now(),
  })

  /**
   * 创建 AI 消息骨架
   */
  const createAIMessage = () => ({
    id: generateId(),
    role: 'assistant',
    content: '',
    timestamp: Date.now(),
    references: [],
    model: '',
    temperature: null,
    topP: null,
    promptTokens: 0,
    completionTokens: 0,
    totalTokens: 0,
    latencyMs: 0,
    confidence: 0,
    ragTimeline: [],
    /** Inspector 数据 */
    traceId: '',
    systemPrompt: '',
    userPrompt: '',
    chunks: [],
    retrieverDetail: null,
    latencyBreakdown: null,
    rawResponse: null,
    isStreaming: true,
  })

  /**
   * 发送消息（真实调用后端）
   */
  const sendMessage = async (content) => {
    if (!content.trim() || isStreaming.value) return

    // 添加用户消息
    const userMsg = createUserMessage(content.trim())
    messages.value.push(userMsg)

    // 创建 AI 消息占位
    const aiMsg = createAIMessage()
    messages.value.push(aiMsg)
    streamingIndex.value = messages.value.length - 1

    isStreaming.value = true
    streamingStatus.value = '思考中...'

    try {
      // askQuestion 返回的已经是 { answer, references, confidence }
      const result = await askQuestion({ question: content.trim() })

      const answer = result?.answer || '抱歉，没有获取到回答。'
      const idx = streamingIndex.value
      if (idx >= 0 && messages.value[idx]) {
        messages.value[idx].content = answer
        messages.value[idx].isStreaming = false
        if (result?.references) {
          messages.value[idx].references = result.references
        }
        if (result?.confidence) {
          messages.value[idx].confidence = result.confidence
        }
      }
    } catch (error) {
      console.error('聊天请求失败:', error)
      // 错误已经在拦截器中提示了，这里可以只做日志记录或补充提示
      // 但如果拦截器已经弹了错误，这里不要再重复弹
      // ElMessage.error('网络错误，请稍后重试')
      messages.value.pop()
    } finally {
      isStreaming.value = false
      streamingStatus.value = ''
      streamingIndex.value = -1
    }
  }

    // ====== 真实 SSE 接口调用（Phase 2 启用） ======
    // cancelStream = createSSEStream('/api/chat/stream', {
    //   body: { message: content.trim(), conversationId: currentConversationId.value },
    //   onMessage(chunk) { ... },
    //   onStatusChange(status) { ... },
    //   onComplete(metadata) { ... },
    //   onError(error) { ... },
    // })

  /**
   * 停止生成
   */
  const stopGeneration = () => {
    if (cancelStream) {
      cancelStream()
      cancelStream = null
    }
    const idx = streamingIndex.value
    if (idx >= 0 && messages.value[idx]) {
      messages.value[idx].isStreaming = false
    }
    finishStreaming()
  }

  /**
   * 清理流式状态
   */
  const finishStreaming = () => {
    isStreaming.value = false
    streamingStatus.value = ''
    streamingIndex.value = -1
    cancelStream = null
  }

  /**
   * 清空消息
   */
  const clearMessages = () => {
    stopGeneration()
    messages.value = []
  }

  return {
    messages,
    isStreaming,
    streamingStatus,
    useVirtualScroll,
    sendMessage,
    stopGeneration,
    clearMessages,
  }
})