import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { createSSEStream, createMockStream } from '@/utils/sse'

<<<<<<< HEAD
// 在文件顶部引入真实的 API（确保 `api/chat.js` 已存在）
// 确保顶部已经导入了 askQuestion 和 ElMessage
import { askQuestion } from '@/api/chat'
import { ElMessage } from 'element-plus'

=======
>>>>>>> ab1e264e0129d4ed3b7ffc3a0970dfb17aba3f34
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
<<<<<<< HEAD
   * 发送消息（真实调用后端）
=======
   * 发送消息
   * @param {string} content - 用户输入内容
>>>>>>> ab1e264e0129d4ed3b7ffc3a0970dfb17aba3f34
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

<<<<<<< HEAD
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
=======
    // 开始流式
    isStreaming.value = true
    streamingStatus.value = 'thinking'

    let accumulatedContent = ''

    // 使用 Mock 流（开发阶段）
    // TODO: Phase 2 替换为 SSE 真实接口
    cancelStream = createMockStream({
      onMessage(chunk) {
        accumulatedContent += chunk
        const idx = streamingIndex.value
        if (idx >= 0 && messages.value[idx]) {
          messages.value[idx].content = accumulatedContent
        }
      },
      onStatusChange(status) {
        streamingStatus.value = status
      },
      onComplete(metadata) {
        const idx = streamingIndex.value
        if (idx >= 0 && messages.value[idx]) {
          messages.value[idx] = {
            ...messages.value[idx],
            ...metadata,
            isStreaming: false,
            references: [
              {
                id: 'ref_1',
                docName: 'RAG 技术白皮书 v2.3.pdf',
                snippet:
                  'RAG (Retrieval-Augmented Generation) 通过将外部知识检索与文本生成相结合，有效解决了大语言模型的知识边界问题...',
                scores: {
                  semantic: 0.92,
                  keyword: 0.81,
                  final: 0.94,
                },
              },
              {
                id: 'ref_2',
                docName: '企业知识库架构设计.md',
                snippet:
                  '向量数据库（如 Milvus）在 RAG 架构中承担核心检索角色，支持 HNSW 索引和 IVF 索引...',
                scores: {
                  semantic: 0.88,
                  keyword: 0.76,
                  final: 0.89,
                },
              },
              {
                id: 'ref_3',
                docName: 'LLM 应用开发指南.pdf',
                snippet:
                  '在实际应用中，RAG 方案相比纯 Fine-tuning 具有更低的成本和更好的可解释性...',
                scores: {
                  semantic: 0.85,
                  keyword: 0.72,
                  final: 0.86,
                },
              },
            ],
            ragTimeline: [
              {
                step: 'Query',
                label: '用户问题',
                duration: 0,
                detail: content.trim().slice(0, 50) + (content.trim().length > 50 ? '...' : ''),
              },
              {
                step: 'Embedding',
                label: 'Embedding',
                duration: 18,
                detail: '768 dim',
              },
              {
                step: 'VectorSearch',
                label: 'Vector Search',
                duration: 42,
                detail: 'Top 10',
              },
              {
                step: 'BM25Search',
                label: 'BM25 Search',
                duration: 17,
                detail: 'Top 10',
              },
              {
                step: 'RRFMerge',
                label: 'RRF Merge',
                duration: 3,
                detail: 'Merged 12',
              },
              {
                step: 'BGERerank',
                label: 'BGE Rerank',
                duration: 34,
                detail: 'Top 3',
              },
              {
                step: 'PromptAssemble',
                label: 'Prompt Assemble',
                duration: 2,
                detail: '',
              },
              {
                step: 'LLMGeneration',
                label: 'LLM Generation',
                duration: 1200,
                detail: '',
              },
              {
                step: 'Output',
                label: 'Output',
                duration: 0,
                detail: '',
              },
            ],
            traceId: generateTraceId(),
            systemPrompt: `你是一个专业的企业级 AI 助手，名为 NebulaMind。你的回答基于提供的知识库文档。

## 规则
1. 回答必须基于检索到的文档内容，不得捏造信息
2. 如果文档中没有相关信息，请明确告知用户
3. 使用 Markdown 格式组织回答，使其清晰易读
4. 引用来源时标注文档名称和片段编号
5. 回答应当专业、准确、简洁`,
            userPrompt: content.trim(),
            chunks: [
              {
                id: 'chunk_001',
                docName: 'RAG 技术白皮书 v2.3.pdf',
                score: 0.94,
                content: 'RAG (Retrieval-Augmented Generation) 是一种结合了信息检索与文本生成的 AI 架构。它通过先从外部知识库中检索相关文档片段，再将这些片段作为上下文提供给大语言模型，从而生成更准确、更具时效性的回答...',
              },
              {
                id: 'chunk_002',
                docName: '企业知识库架构设计.md',
                score: 0.89,
                content: '向量数据库（如 Milvus）在 RAG 架构中承担核心检索角色。Milvus 支持多种索引类型：HNSW（分层导航小世界图）适用于高召回场景，IVF_FLAT 适用于平衡精度与速度，IVF_PQ 通过乘积量化大幅压缩内存...',
              },
              {
                id: 'chunk_003',
                docName: 'LLM 应用开发指南.pdf',
                score: 0.86,
                content: '在实际应用中，RAG 方案相比纯 Fine-tuning 具有显著优势：1) 成本更低，无需重新训练模型；2) 知识更新实时，只需更新知识库；3) 可解释性强，可追溯每个回答的引用来源...',
              },
              {
                id: 'chunk_004',
                docName: 'RAG 技术白皮书 v2.3.pdf',
                score: 0.78,
                content: 'RAG 的核心组件包括：Embedding 模型（将文本转换为向量）、向量数据库（存储和检索向量）、重排序模型（对检索结果精排）、大语言模型（生成最终回答）...',
              },
              {
                id: 'chunk_005',
                docName: '企业知识库架构设计.md',
                score: 0.72,
                content: '在企业级 RAG 架构中，推荐使用混合检索策略：结合向量检索（语义匹配）和 BM25 检索（关键词匹配），通过 RRF（倒数排名融合）算法合并结果，再使用 BGE-Reranker 进行精排...',
              },
            ],
            retrieverDetail: {
              vector: {
                topK: 10,
                results: [
                  { id: 'chunk_001', score: 0.94 },
                  { id: 'chunk_004', score: 0.78 },
                  { id: 'chunk_006', score: 0.71 },
                  { id: 'chunk_009', score: 0.65 },
                  { id: 'chunk_012', score: 0.58 },
                  { id: 'chunk_015', score: 0.52 },
                  { id: 'chunk_018', score: 0.47 },
                  { id: 'chunk_021', score: 0.43 },
                  { id: 'chunk_024', score: 0.39 },
                  { id: 'chunk_027', score: 0.35 },
                ],
              },
              bm25: {
                topK: 10,
                results: [
                  { id: 'chunk_003', score: 0.86 },
                  { id: 'chunk_002', score: 0.82 },
                  { id: 'chunk_005', score: 0.72 },
                  { id: 'chunk_008', score: 0.61 },
                  { id: 'chunk_001', score: 0.55 },
                  { id: 'chunk_011', score: 0.48 },
                  { id: 'chunk_014', score: 0.42 },
                  { id: 'chunk_017', score: 0.38 },
                  { id: 'chunk_020', score: 0.33 },
                  { id: 'chunk_023', score: 0.29 },
                ],
              },
              rrf: {
                mergedCount: 12,
                results: [
                  { id: 'chunk_001', score: 0.94, rankVector: 1, rankBM25: 5 },
                  { id: 'chunk_002', score: 0.89, rankVector: 6, rankBM25: 2 },
                  { id: 'chunk_003', score: 0.86, rankVector: 7, rankBM25: 1 },
                  { id: 'chunk_004', score: 0.78, rankVector: 2, rankBM25: 8 },
                  { id: 'chunk_005', score: 0.72, rankVector: 8, rankBM25: 3 },
                ],
              },
              rerank: {
                topK: 3,
                results: [
                  { id: 'chunk_001', score: 0.94 },
                  { id: 'chunk_002', score: 0.89 },
                  { id: 'chunk_003', score: 0.86 },
                ],
              },
            },
            latencyBreakdown: {
              embedding: 18,
              vectorSearch: 42,
              bm25Search: 17,
              rrfMerge: 3,
              rerank: 34,
              promptAssemble: 2,
              llmGeneration: 1200,
              total: 1316,
            },
            rawResponse: buildRawResponse(content.trim()),
          }
        }
        finishStreaming()
      },
    })
>>>>>>> ab1e264e0129d4ed3b7ffc3a0970dfb17aba3f34

    // ====== 真实 SSE 接口调用（Phase 2 启用） ======
    // cancelStream = createSSEStream('/api/chat/stream', {
    //   body: { message: content.trim(), conversationId: currentConversationId.value },
    //   onMessage(chunk) { ... },
    //   onStatusChange(status) { ... },
    //   onComplete(metadata) { ... },
    //   onError(error) { ... },
    // })
<<<<<<< HEAD
=======
  }
>>>>>>> ab1e264e0129d4ed3b7ffc3a0970dfb17aba3f34

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