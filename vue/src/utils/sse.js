/**
 * SSE 流式请求工具
 * 使用 fetch + ReadableStream + AbortController 实现
 * 支持流式读取、动态状态提示、取消请求
 */

/**
 * 创建 SSE 流式连接
 * @param {string} url - SSE 端点
 * @param {object} options - 配置项
 * @param {object} options.body - 请求体（POST）
 * @param {AbortSignal} options.signal - 取消信号
 * @param {function} options.onMessage - 收到消息片段回调 (text: string)
 * @param {function} options.onStatusChange - 状态变更回调 (status: string)
 * @param {function} options.onComplete - 流完成回调 (metadata: object)
 * @param {function} options.onError - 错误回调 (error: Error)
 * @returns {function} cancel - 取消函数
 */
export function createSSEStream(url, options = {}) {
  const {
    body = {},
    signal,
    onMessage,
    onStatusChange,
    onComplete,
    onError,
  } = options

  let cancelled = false

  const statusSequence = [
    { delay: 0, status: 'thinking' },
    { delay: 800, status: 'searching' },
    { delay: 2000, status: 'ranking' },
    { delay: 3000, status: 'generating' },
  ]

  const statusTimers = statusSequence.map(({ delay, status }) =>
    setTimeout(() => {
      if (!cancelled && onStatusChange) {
        onStatusChange(status)
      }
    }, delay)
  )

  const clearStatusTimers = () => {
    statusTimers.forEach(clearTimeout)
  }

  const controller = new AbortController()
  const combinedSignal = signal
    ? combineSignals(signal, controller.signal)
    : controller.signal

  const request = async () => {
    try {
      // 使用 POST 方式发送请求，适配后端 SSE 接口
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'text/event-stream',
        },
        body: JSON.stringify(body),
        signal: combinedSignal,
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()

        if (done) {
          clearStatusTimers()
          if (onComplete && !cancelled) {
            onComplete({})
          }
          break
        }

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6).trim()

            if (data === '[DONE]') {
              clearStatusTimers()
              if (onComplete && !cancelled) {
                onComplete({})
              }
              return
            }

            try {
              const parsed = JSON.parse(data)
              if (parsed.content && onMessage) {
                onMessage(parsed.content)
              }
              if (parsed.status && onStatusChange) {
                clearStatusTimers()
                onStatusChange(parsed.status)
              }
            } catch {
              // 非 JSON 数据，直接作为文本处理
              if (onMessage) {
                onMessage(data)
              }
            }
          }
        }
      }
    } catch (error) {
      clearStatusTimers()
      if (error.name === 'AbortError') {
        return
      }
      if (onError && !cancelled) {
        onError(error)
      }
    }
  }

  request()

  return () => {
    cancelled = true
    clearStatusTimers()
    controller.abort()
  }
}

/**
 * 合并多个 AbortSignal
 */
function combineSignals(...signals) {
  const controller = new AbortController()

  for (const signal of signals) {
    if (signal.aborted) {
      controller.abort(signal.reason)
      return controller.signal
    }
    signal.addEventListener('abort', () => controller.abort(signal.reason), {
      once: true,
    })
  }

  return controller.signal
}

/**
 * 模拟 SSE 流式响应（开发阶段 Mock 数据）
 */
export function createMockStream(callbacks) {
  const { onMessage, onStatusChange, onComplete } = callbacks
  let cancelled = false

  const mockStatuses = [
    { delay: 300, status: 'thinking' },
    { delay: 1200, status: 'searching' },
    { delay: 2500, status: 'ranking' },
    { delay: 3500, status: 'generating' },
  ]

  const statusTimers = mockStatuses.map(({ delay, status }) =>
    setTimeout(() => {
      if (!cancelled && onStatusChange) onStatusChange(status)
    }, delay)
  )

  const mockAnswer = `## 关于 RAG 技术的详细解答\n\n**RAG (Retrieval-Augmented Generation)** 是一种结合了信息检索与文本生成的 AI 架构。\n\n### 核心原理\n\nRAG 在生成回答之前，先从外部知识库中检索相关文档片段，然后将这些片段作为上下文提供给 LLM。\n\n### 工作流程\n\n1. **用户提问** → 将问题向量化\n2. **向量检索** → 在知识库中找到最相关的文档片段\n3. **重排序** → 对检索结果进行精排\n4. **生成回答** → LLM 基于检索到的上下文生成答案\n\n### 代码示例\n\n\`\`\`python\nfrom langchain.embeddings import OpenAIEmbeddings\nfrom langchain.vectorstores import Milvus\n\n# 初始化向量存储\nembeddings = OpenAIEmbeddings()\nvector_store = Milvus(\n    embedding_function=embeddings,\n    collection_name=\"knowledge_base\"\n)\n\n# 检索相关文档\nresults = vector_store.similarity_search(\n    query=\"什么是 RAG？\",\n    k=3\n)\n\`\`\`\n\n### 数学公式\n\n相似度计算公式（余弦相似度）：\n\n$$\\text{similarity}(A, B) = \\frac{A \\cdot B}{\\|A\\| \\|B\\|} = \\frac{\\sum_{i=1}^{n} A_i B_i}{\\sqrt{\\sum_{i=1}^{n} A_i^2} \\sqrt{\\sum_{i=1}^{n} B_i^2}}$$\n\n> **提示**：RAG 可以有效减少 LLM 的幻觉问题，特别适合企业知识库问答场景。\n\n- [x] 减少幻觉\n- [x] 实时知识更新\n- [ ] 多模态支持（规划中）\n\n| 方案 | 优点 | 缺点 |\n|------|------|------|\n| RAG | 实时、可解释 | 检索质量依赖 |\n| Fine-tuning | 深度理解 | 成本高、更新慢 |\n| Prompt Engineering | 简单快速 | 上下文有限 |`

  const chunks = mockAnswer.match(/.{1,8}/g) || [mockAnswer]

  let index = 0
  const interval = setInterval(() => {
    if (cancelled) {
      clearInterval(interval)
      return
    }
    if (index < chunks.length) {
      if (onMessage) onMessage(chunks[index])
      index++
    } else {
      clearInterval(interval)
      statusTimers.forEach(clearTimeout)
      if (onComplete) {
        onComplete({
          model: 'Qwen3-32B',
          temperature: 0.7,
          top_p: 0.9,
          promptTokens: 1247,
          completionTokens: 389,
          totalTokens: 1636,
          latencyMs: 1423,
          confidence: 92,
        })
      }
    }
  }, 30)

  return () => {
    cancelled = true
    clearInterval(interval)
    statusTimers.forEach(clearTimeout)
  }
}

/**
 * 带自动重连的 SSE 流式连接
 * 连接断开后自动重试，最多重连 maxRetries 次
 * @param {number} maxRetries - 最大重连次数，默认 3
 * @param {number} retryDelay - 重连延迟 ms，默认 2000
 */
export function createSSEStreamWithRetry(url, options = {}, maxRetries = 3, retryDelay = 2000) {
  let retryCount = 0
  let cancelFn = null
  let currentOnMessage = null
  let currentOnComplete = null
  let currentOnError = null
  let accumulatedContent = ''

  const {
    onMessage: origOnMessage,
    onComplete: origOnComplete,
    onError: origOnError,
    ...restOptions
  } = options

  const start = () => {
    cancelFn = createSSEStream(url, {
      ...restOptions,
      onMessage(chunk) {
        accumulatedContent += chunk
        if (origOnMessage) origOnMessage(chunk)
      },
      onComplete(metadata) {
        if (origOnComplete) origOnComplete(metadata)
      },
      onError(error) {
        if (retryCount < maxRetries) {
          retryCount++
          setTimeout(() => {
            start()
          }, retryDelay * retryCount)
        } else {
          if (origOnError) origOnError(error)
        }
      },
    })
  }

  start()

  return () => {
    retryCount = maxRetries // 阻止重连
    if (cancelFn) cancelFn()
  }
}