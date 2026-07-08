/**
 * 全局错误处理
 * 统一错误边界、提示、日志
 */
import { ElMessage } from 'element-plus'

/**
 * 错误类型枚举
 */
export const ErrorType = {
  NETWORK: 'network',
  API: 'api',
  SSE: 'sse',
  WEBSOCKET: 'websocket',
  RUNTIME: 'runtime',
  UNKNOWN: 'unknown',
}

/**
 * 全局错误处理
 * @param {Error|string} error - 错误对象或消息
 * @param {string} type - 错误类型
 * @param {object} context - 错误上下文
 */
export function handleError(error, type = ErrorType.UNKNOWN, context = {}) {
  const message = getErrorMessage(error, type)

  // 开发环境输出详细日志
  if (import.meta.env.DEV) {
    console.group(`[NebulaMind Error] ${type}`)
    console.error('Error:', error)
    console.error('Context:', context)
    console.groupEnd()
  }

  // 非流式错误才弹提示（流式错误由 SSE 回调处理）
  if (type !== ErrorType.SSE) {
    ElMessage.error(message)
  }
}

/**
 * 提取错误消息
 */
function getErrorMessage(error, type) {
  if (typeof error === 'string') return error

  if (error?.message) {
    // 常见错误简化
    if (error.message === 'Network Error') return '网络连接失败，请检查网络'
    if (error.message.includes('timeout')) return '请求超时，请稍后重试'
    if (error.message.includes('abort')) return '请求已取消'
    return error.message
  }

  // 按类型提供默认消息
  const defaults = {
    [ErrorType.NETWORK]: '网络连接失败',
    [ErrorType.API]: '接口请求失败',
    [ErrorType.SSE]: '流式连接中断',
    [ErrorType.WEBSOCKET]: 'WebSocket 连接异常',
    [ErrorType.RUNTIME]: '应用运行异常',
    [ErrorType.UNKNOWN]: '未知错误',
  }

  return defaults[type] || defaults[ErrorType.UNKNOWN]
}

/**
 * 全局未捕获错误处理
 */
export function setupGlobalErrorHandler() {
  // Vue 组件错误
  window.addEventListener('error', (event) => {
    // 忽略资源加载错误（如图片、字体等）
    if (event.target !== window) return

    handleError(event.error, ErrorType.RUNTIME, {
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
    })
  })

  // Promise 未捕获错误
  window.addEventListener('unhandledrejection', (event) => {
    handleError(event.reason, ErrorType.RUNTIME, {
      type: 'unhandledrejection',
    })
    // 阻止默认控制台输出
    event.preventDefault()
  })
}

/**
 * 全局 Vue 错误处理器
 */
export function setupVueErrorHandler(app) {
  app.config.errorHandler = (err, instance, info) => {
    handleError(err, ErrorType.RUNTIME, {
      component: instance?.$options?.name || instance?.__name || 'Unknown',
      info,
    })
  }

  app.config.warnHandler = (msg, instance, trace) => {
    if (import.meta.env.DEV) {
      console.warn(`[Vue warn]: ${msg}`, trace)
    }
  }
}

export default { handleError, setupGlobalErrorHandler, setupVueErrorHandler, ErrorType }